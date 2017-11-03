// generic list view - reads entity's objectstore and prepares table using templates declared in entity's config
define(['jquery', 'underscore', 'datatables', 'indexeddb_backbone_config', 'layoutmanager', 'views/notification', 'configs', 'offline_utils', 'models/user_model', 'indexeddb-backbone', 'TableTools'], function ($, pass, pass, indexeddb, layoutmanager, notifs_view, all_configs, Offline, User) {


    var ListView = Backbone.Layout.extend({

        template: "#list_view_template",

        //params passed contains the name of the entity whose listing is to be shown
        initialize: function (params) {
            this.entity_config = all_configs[params.entity_name];
            //TODO: if !entity_config, handle error etc
            //now context of all fuctions in this view would always be the view object
            _.bindAll(this);
            this.render();
            User.on('change', this.render);
        },

        serialize: function () {
            //send these to the list page template
            var language = User.get('language');
            return {
                page_header: this.entity_config['config_'+language],
                list_page_help: all_configs['misc']['meta_'+language]['list_page_help']
            };
        },

        afterRender: function () {
            //Fetch entity's full data from offline DB and call render_data when fetched
            Offline.fetch_collection(this.entity_config.entity_name)
                .done(this.render_data)
                .fail(function () {
                    notifs_view.add_alert({
                        notif_type: "error",
                        message: "Error reading data for listing."
                    });
                });
        },
        
        get_row_header: function () {
            var language = User.get('language');
            var list_elements = this.entity_config['list_elements_'+language];
            var header_row = $.map(list_elements, function (column_definition) {
                var header = "";
                if ('header' in column_definition) {
                    header = column_definition["header"];
                }
                else if ('element' in column_definition) {
                    // Split column_definition to get the very last field.
                    // For instance, extract block_name from village.block.block_name
                    element = column_definition["element"].split(".").pop().replace(/_/g, " ");
                    header = element[0].toUpperCase() + element.slice(1);
                }
                return {sTitle: header};
            });
            if (!('dashboard_display' in this.entity_config) || (!('add' in this.entity_config.dashboard_display)) || this.entity_config['dashboard_display']['add'] != false) {
                header_row.push({sTitle: all_configs['misc']['meta_'+language]['edit']});
            }
            return header_row;
        },
        
        get_row: function (model_object) {
            var language = User.get('language');
            var list_elements = this.entity_config['list_elements_'+language];
            var row = $.map(list_elements, function (column_definition) {
                var cell = '';
                if ('element' in column_definition) {
                    if ('subelement' in column_definition) {
                        var subelement_definition = column_definition['subelement'];
                        cell = $.map(model_object[column_definition['element']],function (val) {
                            return val[subelement_definition];
                        }).join("; ");
                    }
                    else {
                        var element_definition = column_definition['element'];
                        var element_parts = element_definition.split(".");
                        var object = model_object;
                        for (var i = 0; i < element_parts.length; i++) {
                            // To check if the entry is made online or offline. Display "Not uploaded in place of id in case of offline entry"
                            if(element_parts.length == 1 && element_parts[i] == "online_id" && object.online_id == undefined){
                                object = "Not Uploaded"
                            }
                            else{
                                    object = object[element_parts[i]];
                            }
                        }
                    }
                    if (object != null) {
                        cell = object;
                    }
                }
                else {
                    // Developer needs to be told that 'element' is compulsory.
                    alert('Error: Add element in list_elements parameter in configs.js');
                }
                return cell;
            });
            if (!('dashboard_display' in this.entity_config) || (!('add' in this.entity_config.dashboard_display)) || this.entity_config['dashboard_display']['add'] != false) {
                row.push('<a href="#' + this.entity_config.entity_name + '/edit/' + model_object['id'] + '" class="edit" title="Edit this entry"><i class="glyphicon glyphicon-pencil"></i></a>');

            }
            return row;
        },

        render_data: function (entity_collection) {
            // render data and call function get_row() to make array_table_values which is assigned to aaData later to
            // fill the table with the relevant values.
            var self = this;
            var language = User.get('language');
            if (this.entity_config.entity_name == this.entity_config.list_var_check){
                var filtered_collection = new Backbone.Collection(entity_collection.filter(function(model) {
                    return model.get('parentcategory').id == User.get("type_of_cocouser")|model.get('parentcategory').id == null;
                    entity_collection = entity_collection
                })); 
            }
            else{
                entity_collection = entity_collection
            }
            console.log("in render_data...change in collection...rendering list view");
            var array_table_values = $.map(entity_collection.toJSON(), function (model) {
                return [self.get_row(model)];
            });            
            aoColumns = this.get_row_header();
            this.$('#list_table')
                .DataTable({
                    "sDom": 'T<"clear">lfrtip',
                    "bDeferRender": true,
                    "aoColumns": aoColumns,
                    "bAutoWidth":false,
                    "aaData": array_table_values,       //aaData takes array_table_values and push data in the table.
                    "bAutoWidth":false,
                    "bDestroy": true,
                    "oLanguage": {
                        "sSearch": all_configs['misc']['meta_'+language]['search'],
                        "sLengthMenu": all_configs['misc']['meta_'+language]['enteries']+"_MENU_",
                        "sInfo": all_configs['misc']['meta_'+language]['total_enteries']+"_TOTAL_",
                        "oPaginate": {
                            "sNext": all_configs['misc']['meta_'+language]['next'],
                            "sPrevious": all_configs['misc']['meta_'+language]['previous']
                        },
                    },
                    "oTableTools": {
                        "sSwfPath": "/media/coco/app/scripts/libs/tabletools_media/swf/copy_csv_xls.swf",
                        "aButtons": [
                            {
                                "sExtends": "copy",
                                "sButtonText": all_configs['misc']['meta_'+language]['copy_clipboard']
                            },
                            {
                                "sExtends": "xls",
                                "sButtonText": all_configs['misc']['meta_'+language]['excel_download']
                            }
                        ]

                    }
                });
            $("#loaderimg")
                .hide();
            $("#sort-helptext").show();
        }
    });
    return ListView;
});

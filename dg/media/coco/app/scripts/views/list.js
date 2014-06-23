// generic list view - reads entity's objectstore and prepares table using templates declared in entity's config
define(['jquery', 'underscore', 'datatable', 'indexeddb_backbone_config', 'layoutmanager', 'views/notification', 'configs', 'offline_utils', 'indexeddb-backbone', 'tabletools', 'zeroclipboard'], function ($, pass, pass, indexeddb, layoutmanager, notifs_view, all_configs, Offline) {


    var ListView = Backbone.Layout.extend({

        template: "#list_view_template",

        //params passed contains the name of the entity whose listing is to be shown
        initialize: function (params) {
            this.entity_config = all_configs[params.entity_name];
            //TODO: if !entity_config, handle error etc
            //TODO: instead of html of header, we can ask for coloumn headers as array
            //get the template for table header
            this.table_header = $('#' + this.entity_config.list_table_header_template)
                .html();
            //get the template for a row of table
            this.row_template = _.template($('#' + this.entity_config.list_table_row_template)
                .html());
            //now context of all fuctions in this view would always be the view object
            _.bindAll(this);
            this.render();
        },

        serialize: function () {
            //send these to the list page template
            return {
                page_header: this.entity_config.page_header,
                table_header: this.table_header
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

        get_row: function (model_object) {
            var list_elements = this.entity_config.list_elements;
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
                            object = object[element_parts[i]];
                        }
                        if (object != null) {
                            cell = object;
                        }
                    }
                }
                else {
                    // Developer needs to be told that 'element' is compulsory.
                    alert('Error: Add element in list_elements parameter in configs.js');
                }
                return cell;
            });
            if (!('dashboard_display' in this.entity_config) || (!('add' in this.entity_config.dashboard_display)) || this.entity_config['dashboard_display']['add'] != false) {
                row.push('<a href="#' + this.entity_config.entity_name + '/edit/' + model_object['id'] + '" class="edit" title="Edit this entry"><i class="icon-pencil"></i></a>');

            }
            return row;
        },

        render_data: function (entity_collection) {
            // render data and call function get_row() to make array_table_values which is assigned to aaData later to
            // fill the table with the relevant values.
            var self = this;
            var start = new Date().getTime();
            console.log("in render_data...change in collection...rendering list view");
            var array_table_values = $.map(entity_collection.toJSON(), function (model) {
                return [self.get_row(model)];
            });

            this.$('#list_table')
                .dataTable({
                    "sDom": 'T<"clear">lfrtip',
                    "bDeferRender": true,
                    "aaData": array_table_values,       //aaData takes array_table_values and push data in the table.
                    "oTableTools": {
                        "sSwfPath": "/media/coco/app/scripts/libs/tabletools_media/swf/copy_csv_xls.swf",
                        "aButtons": [
                            {
                                "sExtends": "copy",
                                "sButtonText": "Copy to Clipboard"
                            },
                            {
                                "sExtends": "xls",
                                "sButtonText": "Download in Excel"
                            }
                        ]

                    }
                });
            $("#loaderimg")
                .hide();
            $("#sort-helptext").show();
            var end = new Date().getTime();
            var time = end - start;
            console.log('Execution time:', time);

        }
    });
    return ListView;
});

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


        modify_row_object: function (model_object){
            var row_elements_keys_array = this.entity_config.list_elements;
            var row_value = [];
            for (var k=0; k<row_elements_keys_array.length; k++){
                if(row_elements_keys_array[k].subelement){
                element_value_in_list_elements = row_elements_keys_array[k]['element'];
                subelement_value_in_list_elements = row_elements_keys_array[k]['subelement'];
                    if (model_object[element_value_in_list_elements].length!=0){
                    }
                    var data_value = $.map(model_object[element_value_in_list_elements], function(val){
                         return val[subelement_value_in_list_elements];
                     }).join("; ");
                     row_value.push(data_value);
                }
                else{
                    if(row_elements_keys_array[k]['element'].indexOf('.')!=-1){
                        var element_parts = row_elements_keys_array[k]['element'].split(".");
                        var push_in_array = model_object[element_parts[0]];
                        console.log('push', push_in_array);
                        for( var i=1; i<element_parts.length; i++){
                           push_in_array = push_in_array[element_parts[i]];
                        }
                        row_value.push(push_in_array);
                    }
                    else{
                    row_value.push(model_object[row_elements_keys_array[k]['element']]);
                    }
                }
            }
//            console.log('test', row_value);
            row_value.push('<a href="#'+this.entity_config.entity_name+'/edit/'+ model_object[row_elements_keys_array[0]['element']]+'" class="edit" title="Edit this entry"><i class="icon-pencil"></i></a>');
            return row_value;
        },

        render_data: function (entity_collection) {

// Method 1 for better performance as well as better readability after optimization
            var self = this;
            var start = new Date().getTime();
            console.log("in render_data...change in collection...rendering list view");
            var that = this;
            var array_table_values = []
            array_table_values = $.map(entity_collection.toJSON(), function(model){
                var output = [self.modify_row_object(model)];
                return output;
            });


// Method 2 for better performance after optimization
//            var that = this;
//            var array_table_values = $.map(entity_collection.toJSON(), function(model){
//                return that.entity_config.object_to_array(model);
//            });


// Method 3 for poor performance
//            var array_table_values = [];
//            entity_collection.each(function (model) {
//                console.log('log item', model.toJSON());
//                a = model.toJSON();
//                array_table_values.push(this.entity_config.object_to_array(a));
//            }, this);

//           console.log('check2', array_table_values);

            this.$('#list_table')
                .dataTable({
                    "sDom": 'T<"clear">lfrtip',
                    "bDeferRender": true,
                    "aaData": array_table_values,
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

            //alternate 1 - using raw string to build table rows
            //     $tbody = this.$("tbody");
            //     $tbody.html('');
            //     var all_items= '';
            //     this.collection.each(function(model) {
            //         all_items+=(this.row_template(model.toJSON()));
            //     }, this);
            //     // console.log(all_items);
            //     $tbody.html(all_items);
            ////////////

            //alternate 2 - using a separate view for each row
            //     this.collection.each(function(model) {
            //         tbody.append(new ListItemView({
            //             model: model,
            //             entity_config: this.entity_config,
            //             appRouter: this.appRouter
            //
            //         })
            //             .render()
            //             .el);
            //     }, this);
            ////////////
            var end = new Date().getTime();
            var time = end - start;
            alert('Execution time: ' + time);

        }
    });
    return ListView;
});

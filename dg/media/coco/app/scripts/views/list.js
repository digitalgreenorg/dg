// generic list view - reads entity's objectstore and prepares table using templates declared in entity's config
define(['jquery', 'underscore', 'datatable', 'indexeddb_backbone_config', 'layoutmanager', 'views/notification', 'configs', 'offline_utils', 'indexeddb-backbone'], function($, pass, pass, indexeddb, layoutmanager, notifs_view, all_configs, Offline) {

    var ListView = Backbone.Layout.extend({

        template: "#list_view_template",

        //params passed contains the name of the entity whose listing is to be shown
        initialize: function(params) {
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

        serialize: function() {
            //send these to the list page template
            return {
                page_header: this.entity_config.page_header,
                table_header: this.table_header
            };
        },

        afterRender: function() {
            //Fetch entity's full data from offline DB and call render_data when fetched
            Offline.fetch_collection(this.entity_config.entity_name)
                .done(this.render_data)
                .fail(function() {
                notifs_view.add_alert({
                    notif_type: "error",
                    message: "Error reading data for listing."
                });
            });
        },

        
        render_data: function(entity_collection) {
            console.log("in render_data...change in collection...rendering list view");
            //create table body in memory
            tbody = $('<tbody>');
            tbody.html('');
            //iterate over the collection, fill row template with each object and append the row to table
            entity_collection.each(function(model) {
                tbody.append(this.row_template(model.toJSON()));
            }, this);
            //put table body in DOM
            this.$('#list_table')
                .append(tbody);
            //initialize datatable lib on the table    
            this.$('#list_table')
                .dataTable();
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
        },

    });
    return ListView;
});

define(['jquery', 'underscore', 'datatable', 'indexeddb_backbone_config', 'layoutmanager', 'views/notification', 'configs', 'offline_utils', 'indexeddb-backbone'], function($, pass, pass, indexeddb, layoutmanager, notifs_view, all_configs, Offline) {

    var ListView = Backbone.Layout.extend({

        template: "#list_view_template",

        initialize: function(params) {
            this.entity_config = all_configs[params.entity_name];
            //TODO: if !entity_config, show 404 etc?
            //TODO: instead of html of header, we can ask for coloumn headers as array
            this.table_header = $('#' + this.entity_config.list_table_header_template)
                .html();
            this.row_template = _.template($('#' + this.entity_config.list_table_row_template)
                .html());
            _.bindAll(this); //now context of all fuctions in this view would always be view object
            this.render();
        },

        serialize: function() {
            return {
                page_header: this.entity_config.page_header,
                table_header: this.table_header
            };
        },

        afterRender: function() {
            //$("#loaderimg")
                //.show();
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
            tbody = $('<tbody>');
            tbody.html('');
            entity_collection.each(function(model) {
                tbody.append(this.row_template(model.toJSON()));
            }, this);
            this.$('#list_table')
                .append(tbody);
            this.$('#list_table')
                .dataTable();
            $("#loaderimg")
                .hide();

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

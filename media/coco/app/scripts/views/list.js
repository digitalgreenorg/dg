define([
  'jquery',
  'underscore',
  'backbone',
  'datatable'

  // Using the Require.js text! plugin, we are loaded raw text
  // which will be used as our views primary template
  // 'text!templates/project/list.html'
], function($){
    
    var ListView = Backbone.View.extend({

        events: {
            "click button#add": "addNew",
        },

        initialize: function(params) {
            this.view_configs = params.view_configs;
            this.collection = new params.view_configs.backbone_collection();
            this.table_template_name = params.view_configs.table_template_name;
            console.log("template_name : " + this.table_template_name)
            this.template = _.template($('#' + 'list_view_template')
                .html());
            this.table_template = _.template($('#' + this.table_template_name)
                .html());
            this.collection.bind('all', this.render_data, this);
            this.datatable = null;
            this.appRouter = params.router;

        },

        render: function(show_heading) {
            $(this.el)
                .html(this.template({
                header_name: show_heading
            }));
            console.log(show_heading);
            $(this.el)
                .append(this.table_template());
                console.log(this.collection);
            this.collection.fetch();


            return this;
        },
        render_data: function() {
            if (this.datatable) {
                this.datatable.fnDestroy();
            }
            $tbody = this.$("tbody");
            $tbody.html('');
            console.log("in render_data...change in collection...rendering list view");

            this.collection.each(function(model) {
                $tbody.append(new list_item_view({
                    model: model,
                    view_configs: this.view_configs
                })
                    .render()
                    .el);
            }, this);
            this.datatable = this.$('table')
                .dataTable({
                "bDestroy": true
            });
        },
        addNew: function() {
            this.appRouter.navigate('person/add', true);
        },



    });
    
    
  // Our module now returns our view
  return ListView;
});
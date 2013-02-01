define([
  'jquery',
  'underscore',
  'backbone',
  'datatable',
  'views/list_item',
  'collections/person_collection'
  
  // Using the Require.js text! plugin, we are loaded raw text
  // which will be used as our views primary template
  // 'text!templates/project/list.html'
], function($,pass,pass,pass,ListItemView){
    
    var ListView = Backbone.Layout.extend({
        
        events: {
            "click button#add": "addNew",
        },
        
        template: "#list_view_template",
        
        initialize: function(params) {
            this.view_configs = params.initialize.view_configs;
            this.collection = new params.initialize.view_configs.backbone_collection();
            this.table_template_name = params.initialize.view_configs.table_template_name;
            console.log("template_name : " + this.table_template_name)
            console.log(params.data);
            this.table_header = $('#' + this.table_template_name)
                .html();
            this.collection.bind('all', this.render_data, this);
            this.datatable = null;
            this.appRouter = params.initialize.router;

        },
        
        serialize:function(){
          return { 
              header_name: this.view_configs.page_header, 
              table_header:$('#' + this.table_template_name).html()
           };  
        },
        
        afterRender: function() {
            /* Work with the View after render. */
            this.collection.fetch();
        },

        render_data: function() {
            if (this.datatable) {
                this.datatable.fnDestroy();
            }
            $tbody = this.$("tbody");
            $tbody.html('');
            console.log("in render_data...change in collection...rendering list view");

            this.collection.each(function(model) {
                $tbody.append(new ListItemView({
                    model: model,
                    view_configs: this.view_configs,
                    appRouter: this.appRouter
                    
                })
                    .render()
                    .el);
            }, this);
            console.log(this.$('#list_table'));
            this.datatable = this.$('#list_table')
                .dataTable();
        },

        addNew: function() {
            this.appRouter.navigate('person/add', true);
        },



    });
    
    
  // Our module now returns our view
  return ListView;
});
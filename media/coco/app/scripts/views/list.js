define([
  'jquery',
  'underscore',
  'datatable',
  'indexeddb_backbone_config',
  'layoutmanager',
  'indexeddb-backbone'      
  
  // Using the Require.js text! plugin, we are loaded raw text
  // which will be used as our views primary template
  // 'text!templates/project/list.html'
], function($, pass, pass, indexeddb, layoutmanager){
    
    var ListView = Backbone.Layout.extend({
        
        template: "#list_view_template",
        
        initialize: function(params) {
            this.view_configs = params.initialize.view_configs;
            
            generic_collection = Backbone.Collection.extend({
                database: indexeddb,
                storeName: this.view_configs.entity_name,
            });
            this.collection = new generic_collection();
            this.table_header = $('#' + params.initialize.view_configs.table_template_name)
                .html();
            this.item_template = _.template($('#' + params.initialize.view_configs.list_item_template_name)
            .html());
            this.collection.bind('all', this.render_data, this);
            this.datatable = null;
        },
        
        serialize:function(){
          return { 
              header_name: this.view_configs.page_header, 
              table_header:this.table_header
           };  
        },
        
        afterRender: function() {
            /* Work with the View after render. */
			$("#loaderimg").show();
            this.collection.fetch();
        },

        render_data: function() {
            if (this.datatable) {
                this.datatable.fnDestroy();
            }
            console.log("in render_data...change in collection...rendering list view");
            tbody = $('<tbody>');
            tbody.html('');
            this.collection.each(function(model) {
                tbody.append(this.item_template(model.toJSON()));
            }, this);
            this.$('#list_table').append(tbody);
			$("#loaderimg").hide();
            
            //alternate 1 - using raw string to build table rows
            //     $tbody = this.$("tbody");
            //     $tbody.html('');
            //     var all_items= '';
            //     this.collection.each(function(model) {
            //         all_items+=(this.item_template(model.toJSON()));
            //     }, this);
            //     // console.log(all_items);
            //     $tbody.html(all_items);
            ////////////
            
            //alternate 2 - using a separate view for each row
            //     this.collection.each(function(model) {
            //         tbody.append(new ListItemView({
            //             model: model,
            //             view_configs: this.view_configs,
            //             appRouter: this.appRouter
            //             
            //         })
            //             .render()
            //             .el);
            //     }, this);
            ////////////
            
            this.datatable = this.$('#list_table')
                .dataTable();
        },
        
    });
    
    
  // Our module now returns our view
  return ListView;
});
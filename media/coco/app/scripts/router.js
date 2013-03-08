// Filename: router.js
define([
  'jquery',
  'underscore',
  'backbone',
  'views/app_layout',
  'configs',
  'layoutmanager'
  
], function($, _, Session, AppLayout,configs){
  
    var AppRouter = Backbone.Router.extend({
        routes: {
            "": "showDashboard",
            ":entity": "list",
            ":entity/add": "addPerson",
            ":entity/edit/:id": "editPerson"
        },
        showDashboard: function() {
            console.log("ROUTER: dashboard url caught");
            
            this.app_v.render_dashboard();
        },
        list: function(entity) {
            console.log("ROUTER: list "+entity+" url caught");
            this.app_v.render_list_view({view_configs:this.configs[entity],router:this});
        },
        addPerson: function(entity) {
            console.log("ROUTER: add "+entity+" url caught");
            this.app_v.render_add_edit_view({view_configs:this.configs[entity],router:this}, null);
        },
        editPerson: function(entity,id) {
            console.log("ROUTER: edit "+entity+" url caught id = " + id);
            this.app_v.render_add_edit_view({view_configs:this.configs[entity],router:this}, parseInt(id));
        },
        
        initialize: function(app_v, configs){
            this.app_v = app_v;
            this.configs = configs;
        }

    });
  
  var initialize = function(){
    
    // var app_v = new AppView();
    $("#app").empty().append(AppLayout.el);

    // Render the Layout.
    AppLayout.render();
    var app_router = new AppRouter(AppLayout,configs);
    
    Backbone.history.start();
  };
  return {
    initialize: initialize
  };
});
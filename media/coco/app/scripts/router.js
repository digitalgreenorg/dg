// Filename: router.js
define([
  'jquery',
  'underscore',
  'backbone',
  'views/app_view',
  'configs'
], function($, _, Session, AppView,configs){
  
    var AppRouter = Backbone.Router.extend({
        routes: {
            "": "showDashboard",
            "person": "listPerson",
            "person/add": "addPerson",
            "person/edit/:id": "editPerson"
        },
        showDashboard: function() {
            console.log("showdashboard url caught");
            
            this.app_v.render_dashboard();
        },
        listPerson: function() {
            console.log("list person url caught");
            this.app_v.render_list_view({view_configs:this.configs.person_list_view_configs,router:this});
        },
        addPerson: function() {
            console.log("add person url caught");
            this.app_v.render_add_edit_view(this.configs.person_list_view_configs, null);
        },
        editPerson: function(id) {
            console.log("edit person url caught, id = " + id);
            this.app_v.render_add_edit_view(this.configs.person_list_view_configs, id);
        },
        initialize: function(app_v, configs){
            this.app_v = app_v;
            this.configs = configs;
        }

    });
  
  var initialize = function(){
    
    var app_v = new AppView();
    var app_router = new AppRouter(app_v,configs);
    
    Backbone.history.start();
  };
  return {
    initialize: initialize
  };
});
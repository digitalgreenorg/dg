// Filename: router.js
define([
  'jquery',
  'underscore',
  'backbone',
  'views/app_view',
], function($, _, Session, AppView){
  
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
            this.app_v.render_list_view(person_list_view_configs);
        },
        addPerson: function() {
            console.log("add person url caught");
            this.app_v.render_add_edit_view(person_list_view_configs, null);
        },
        editPerson: function(id) {
            console.log("edit person url caught, id = " + id);
            this.app_v.render_add_edit_view(person_list_view_configs, id);
        },
        initialize: function(app_v){
            this.app_v = app_v;
        }

    });
  
  var initialize = function(){
    
    var app_v = new AppView();
    var app_router = new AppRouter(app_v);
    
    Backbone.history.start();
  };
  return {
    initialize: initialize
  };
});
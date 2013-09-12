// Filename: router.js
define([
  'jquery',
  'underscore',
  'backbone',
  'views/app_layout',
  'configs',
  'auth'
], function(jquery, underscore, backbone, AppLayout, configs, Auth){
  
    var AppRouter = Backbone.Router.extend({
        routes: {
            "": "home",
            ":entity/list": "list",
            ":entity/add": "add",
            ":entity/edit/:id": "edit",
            "login": "login"
        },
        home: function() {
            this.check_login_wrapper()
                .done(function(){
                    AppLayout.render_home_view();
                });
        },
        list: function(entity_name) {
            this.check_login_wrapper()
                .done(function(){
                    AppLayout.render_list_view(entity_name);
                });
        },
        add: function(entity_name) {
            this.check_login_wrapper()
                .done(function(){
                    AppLayout.render_add_edit_view(entity_name, null);
                });
        },
        edit: function(entity_name, id) {
            this.check_login_wrapper()
                .done(function(){
                    AppLayout.render_add_edit_view(entity_name, parseInt(id));
                });
        },
        login: function(){
            AppLayout.render_login();
        },
                
        check_login_wrapper: function(){
            var dfd = new $.Deferred();
            console.log("Authenticating before routing");
            Auth.check_login()
                .fail(function(err){
                    console.log("UnAuthenticated");
                    dfd.reject();
                    window.Router.navigate("login",{
                        trigger:true
                    });
                })
                .done(function(){
                    console.log("Authenticated");
                    dfd.resolve();
                });
            return dfd;    
        }

    });
  
  var initialize = function(){
    console.log("Initializing router");
    var app_router = new AppRouter();
    window.Router = app_router;
    Backbone.history.start();
  };
  
  return {
    initialize: initialize
  };
});
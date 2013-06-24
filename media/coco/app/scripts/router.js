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
            ":entity/add": "addPerson",
            ":entity/edit/:id": "editPerson",
            "login": "login"
        },
        home: function() {
            console.log("ROUTER: dashboard url caught");
            this.check_login_wrapper()
                .done(function(){
                    AppLayout.render_home_view();
                });
        },
        list: function(entity) {
            console.log("ROUTER: list "+entity+" url caught");
            this.check_login_wrapper()
                .done(function(){
                    AppLayout.render_list_view({view_configs:configs[entity],router:window.Router});
                });
        },
        addPerson: function(entity) {
            console.log("ROUTER: add "+entity+" url caught");
            this.check_login_wrapper()
                .done(function(){
                    AppLayout.render_add_edit_view({view_configs:configs[entity],router:window.Router}, null);
                });
        },
        editPerson: function(entity,id) {
            console.log("ROUTER: edit "+entity+" url caught id = " + id);
            this.check_login_wrapper()
                .done(function(){
                    AppLayout.render_add_edit_view({view_configs:configs[entity],router:window.Router}, parseInt(id));
                });
        },
        login: function(){
            AppLayout.render_login(this);
        },
                
        initialize: function(){
            // this.app_v = app_v;
            // this.configs = configs;
            // this.bind( "route", this.check_login)
        },
        
        check_login_wrapper: function(){
            var dfd = new $.Deferred();
            console.log("Authenticating before routing");
            Auth.check_login()
                .fail(function(err){
                    console.log("UnAuthenticated");
                    dfd.reject();
                    window.Router.navigate("login",{trigger:true});
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
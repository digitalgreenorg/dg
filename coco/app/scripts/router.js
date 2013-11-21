// Backbone router
define(['jquery', 'underscore', 'backbone', 'views/app_layout', 'configs', 'auth'], function(jquery, underscore, backbone, AppLayout, configs, Auth) {

    var initialize = function() {
        console.log("Initializing router");
        //create a router
        var app_router = new AppRouter();
        //set it on global object to make it easily accessible
        window.Router = app_router;
        //begin monitoring hashchange events
        Backbone.history.start();
    };

    var AppRouter = Backbone.Router.extend({
        //define the routes and the function callbacks
        routes: {
            "": "home",
            ":entity/list": "list",
            ":entity/add": "add",
            ":entity/edit/:id": "edit",
            "login": "login"
        },
        home: function() {
            this.check_login_wrapper()
                .done(function() {
                AppLayout.render_home_view();
            });
        },
        list: function(entity_name) {
            this.check_login_wrapper()
                .done(function() {
                AppLayout.render_list_view(entity_name);
            });
        },
        add: function(entity_name) {
            this.check_login_wrapper()
                .done(function() {
                AppLayout.render_add_edit_view(entity_name, null);
            });
        },
        edit: function(entity_name, id) {
            this.check_login_wrapper()
                .done(function() {
                AppLayout.render_add_edit_view(entity_name, parseInt(id));
            });
        },
        login: function() {
            AppLayout.render_login();
        },

        //check_login wrapper for checking whether user is logged in before routing to any of the above defined routes 
        check_login_wrapper: function() {
            var dfd = new $.Deferred();
            console.log("Authenticating before routing");
            Auth.check_login()
                .fail(function(err) {
                console.log("UnAuthenticated");
                dfd.reject();
                //navigate to login url if user is not logged in
                window.Router.navigate("login", {
                    trigger: true
                });
            })
                .done(function() {
                console.log("Authenticated");
                dfd.resolve();
            });
            return dfd;
        }

    });

    return {
        initialize: initialize
    };
});

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
        	//Check if entity present in url is valid or not and if list view of that entity is enable in case it is valid
        	if(this.entity_valid(entity_name) && this.entity_list_enabled(entity_name)){
        		this.check_login_wrapper()
                .done(function(){
                    AppLayout.render_list_view(entity_name);
                });
        	}
        	else{
        		alert("You are not authorized to view this page. Please contact your administrator.");
        	}
        },
        add: function(entity_name) {
        	//Check if entity present in url is valid or not and if add view of that entity is enable in case it is valid
        	if(this.entity_valid(entity_name) && this.entity_add_enabled(entity_name)){
        		this.check_login_wrapper()
                .done(function(){
                    AppLayout.render_add_edit_view(entity_name, null);
                });
        	}
        	else{
        		alert("You are not authorized to view this page. Please contact your administrator.");
        	}
            
        },
        edit: function(entity_name, id) {
        	//Check if entity present in url is valid or not and if edit view of that entity is enable in case it is valid
        	if(this.entity_valid(entity_name) && this.entity_add_enabled(entity_name)){
        		this.check_login_wrapper()
                .done(function(){
                    AppLayout.render_add_edit_view(entity_name, parseInt(id));
                });
        	}
        	else{
        		alert("You are not authorized to view this page. Please contact your administrator.");
        	}
        },
        login: function() {
            AppLayout.render_login();
        },
        //Check if user entered wrong entity name in url.
        entity_valid: function(entity_name){
        	if(typeof configs[entity_name] == 'undefined'){
        		return false;
        	}
        	else{
        		return true;
        	}
        },
        //Check if list view was allowed in configs so that user may not directly enter the url and access table
        entity_list_enabled: function(entity_name){
            var listing = false;
            if(configs[entity_name].dashboard_display)
            {
            	listing = configs[entity_name].dashboard_display.listing;
            }
            return listing;
        },
      //Check if add view was allowed in configs so that user may not directly enter the url and access form
        entity_add_enabled: function(entity_name){
            var add = true;
            var enable_months = [];
            if(configs[entity_name].dashboard_display)
            {
                add = configs[entity_name].dashboard_display.add;
                enable_months = configs[entity_name].dashboard_display.enable_months;
            }
            if(typeof enable_months != 'undefined'){
            	var d = new Date();
                n = d.getMonth();
                n=n+1;
                res=$.inArray(n, enable_months);
                if(res === -1){
                	add=false;
                }
            }
            return add;
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

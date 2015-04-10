//The parent view containing the side panel and the content panel. It will hold all other views as subviews - dashboard view goes into the side panel and the status/list/add_edit view goes into contant panel based on current url.
define(['views/dashboard', 'views/app_header', 'views/list', 'views/form_controller', 'views/status', 'layoutmanager', 'views/login', 'models/user_model', 'auth'], function(DashboardView, HeaderView, ListView, FormControllerView, StatusView, layoutmanager, LoginView, User, Auth) {

    var AppLayout = Backbone.Layout.extend({
        template: "#page_layout",
        
        initialize: function() {
            console.log("initializing app layout");
        },
        
        serialize: function() {
            // send username to the template 
            var username = User.get("username");
            console.log(User);
            return {
                username: username,
            }
                
        },
        
        //when layout is rendered, create and put the dashboard view in the side panel - constant across all routes
        afterRender: function() {
            console.log("app layout rendered");
            var header_view = new HeaderView();
            this.setView("#header", header_view);
            header_view.render();
            var dashboard_view = new DashboardView();
            this.setView("#side_panel", dashboard_view);
            dashboard_view.render();
        },

        //content panel will be filled with a subview by one of the following functions based on the current url
        render_login: function() {
            var login_view = new LoginView();
            this.setView("#content", login_view);
        },

        render_home_view: function() {
            var s_view = new StatusView();
            this.setView("#content", s_view);
        },

        render_list_view: function(entity_name) {
            var l_view = new ListView({
                entity_name: entity_name
            });
            this.setView("#content", l_view);
        },

        render_add_edit_view: function(entity_name, id) {
            var formcontroller_view = new FormControllerView({
                entity_name: entity_name,
                model_id: id,
            });
            this.setView("#content", formcontroller_view);
            formcontroller_view.render(); //bcoz Its afterRender assumes its elements are in DOM
        }
    });
    return new AppLayout;
});

define(['views/dashboard', 'views/list', 'views/form_controller', 'views/status', 'layoutmanager', 'views/login'], function(DashboardView, ListView, FormControllerView, StatusView, layoutmanager, LoginView) {

    var AppLayout = Backbone.Layout.extend({
        template: "#page_layout",
        initialize: function() {
            console.log("initilizing app layout");
        },

        //when layout is rendered, put the dashboard in the side panel - constant across all routes
        afterRender: function() {
            console.log("app layout rendered");
            var dashboard_view = new DashboardView();
            this.setView("#side_panel", dashboard_view);
            dashboard_view.render();
        },

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
            formcontroller_view.render();  //bcoz Its afterRender assumes its elements are in DOM
        }

    });
    return new AppLayout;
});

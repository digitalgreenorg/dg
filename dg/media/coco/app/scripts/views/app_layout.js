//The parent view containing the side panel and the content panel. It will hold all other views as subviews - dashboard view goes into the side panel and the status/list/add_edit view goes into contant panel based on current url.
define(['views/dashboard', 'views/app_header', 'views/list', 'views/form_controller', 'views/status', 'layoutmanager', 'views/login','views/offline_analytics', 'models/user_model', 'auth','configs'], function(DashboardView, HeaderView, ListView, FormControllerView, StatusView, layoutmanager, LoginView, AnalyticsView, User, Auth,configs) {

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

        render_analytics: function(){
            var i;
            var contaianerCount=1;
            for(i=1; i<=configs.misc.analytics_entities.length; i++)
            {
                var entity = configs.misc.analytics_entities[i-1];
                
                for(j=0;j<configs[entity]['xaxis'].length;j++){
                var analytics_view = new AnalyticsView({
                tabId :i,
                entities : configs.misc.analytics_entities[i-1],
                container: 'container'+(contaianerCount++),
                xaxis : configs[entity]['xaxis'][j],
                j : j
                });
              this.setView("#content", analytics_view);
            } 
        }
        nestContainer =1;
        for(i=1; i<=configs.misc.analytics_entities.length; i++)
            {
            
                var analytics_view = new AnalyticsView({
                    tabId:3,
                    entities : configs.misc.analytics_entities[i-1],
                    container: 'container'+(contaianerCount++),
                    key : [1],
                    j:0
                });
             this.setView("#content", analytics_view);
            
        }
        for(i=0;i<configs.misc.overall_numbers.length;i++){
            var analytics_view = new AnalyticsView({
                    tabId:3,
                    entities :configs.misc.overall_numbers[i],
                    container:'container'+(contaianerCount++),
                    key :[0],
                    j:0
            });
        this.setView("#content",analytics_view);
            
        }
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

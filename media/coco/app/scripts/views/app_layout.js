define([
    'views/dashboard',
    'views/list',
    'views/form_controller',
    'views/status',
    'layoutmanager',  
    'views/login'    
  ], function(DashboardView, ListView, FormControllerView, StatusView, layoutmanager, LoginView){
                  
    var AppLayout = Backbone.Layout.extend({
      template: "#page_layout",
      initialize: function() {
          console.log("initilizing app layout");
          curr_list_view = null;
          current_add_edit_view = null;
      },
      
      //when layout is rendered, put the dashboard in the side panel - constant across all routes
      afterRender: function(){
          console.log("app layout rendered");
          var dashboard_view = new DashboardView();
          this.setView("#side_panel", dashboard_view);
          dashboard_view.render();
      },
      
      render_login: function(router){
          var login_view = new LoginView(router);
          this.setView("#content", login_view);
      },    
          
      render_home_view: function() {
          var s_view = new StatusView();
          this.setView("#content", s_view);
      },
      
      render_list_view: function(params) {
          var l_view = new ListView({initialize:params});
          this.setView("#content",l_view);
      },
      
      render_add_edit_view: function(params, data) {
          // var add_or_edit = "add";
//           if (data) add_or_edit = "edit";
          // var bcrumb_template = _.template($('#add_edit_breadcrumb').html());
//           this.setView("#header", new HeaderView({serialize: { breadcrumb: bcrumb_template({bread1:params.view_configs.page_header.toLowerCase(),bread2:params.view_configs.page_header,add_or_edit:add_or_edit}) }}));
          
          
          if(!this.formcontroller_v)
          {
              this.formcontroller_v = new FormControllerView({
                            serialize: {
                                button1: "Save and Add Another",
                                button2: null
                            },
                            initialize: params,
                            model_id: data,
                            model_json: null
          
                        });
          }
          else
          {
              this.formcontroller_v.params = {
                            serialize: {
                                button1: "Save and Add Another",
                                button2: null
                            },
                            initialize: params,
                            model_id: data,
                            model_json: null
          
                        };
            this.formcontroller_v.options = {
                          serialize: {
                              button1: "Save and Add Another",
                              button2: null
                          },
                          initialize: params,
                          model_id: data,
                          model_json: null
          
                      };            
          }
          var that = this;
          this.setView("#content", this.formcontroller_v);
          this.formcontroller_v.render();
          
          return this;
      }
   
    });
  return new AppLayout;
});
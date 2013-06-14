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
          this.setView("#side_panel", new DashboardView());
                
      },
      
      // hide_side_panel: function(){
//           console.log("HIDE SIDE PANEL");
//           console.log($("#side_panel"));
//           this.$("#side_panel").hide();
//           $("#content").removeClass('span10');
//           $("#content").addClass('span12');
//           $("#content").prepend("<div><a id='right_arrow'><img style='width:30px;' src='/media/coco/app/images/right_arrow.png'/></a></div>");
//           $("#right_arrow").click(function() {
//               $("#content").removeClass('span12');
//               $("#content").addClass('span10');
//               $('#right_arrow').remove();
//               $("#side_panel").show();
//           });
//       },
      render_login: function(router){
          var l_view = new LoginView(router);
          this.setView("#content", l_view);
          // l_view.render();
          
      },    
          
      render_dashboard: function() {
          // $(this.el)
          //     .html('');
          // $(this.el)
          //     .append(header.render("<li class='active' >Dashboard</li>")
          //     .el);
          // this.setView("#header", new HeaderView({serialize: { breadcrumb: $('#dashboard_breadcrumb').html() }}));
          var s_view = new StatusView()
          this.setView("#content", s_view);
          s_view.render();
          
          //         
          // $(this.el)
          //               .append(dashboard.render()
          //               .el);
          return this;
                   
      },
      render_list_view: function(params) {
          // var bcrumb_template = _.template($('#list_breadcrumb').html());
          // this.setView("#header", new HeaderView({serialize: { breadcrumb: bcrumb_template({bread:params.view_configs.page_header}) }}));
          var that = this;
          var l_view = new ListView({initialize:params});
          this.setView("#content",l_view);
          l_view.render();
          
          return this;
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
                                button1: "Save",
                                button2: "Save and Add Another"
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
                                button1: "Save",
                                button2: "Save and Add Another"
                            },
                            initialize: params,
                            model_id: data,
                            model_json: null
          
                        };
            this.formcontroller_v.options = {
                          serialize: {
                              button1: "Save",
                              button2: "Save and Add Another"
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
define([
  'jquery',
  'underscore',
  'backbone',
  'views/header',
  'views/dashboard',
  'views/list',
  'views/person_add_edit'
  ], function($, underscore, Session, HeaderView, DashboardView, ListView, PersonAddEditView){
                  
    var AppLayout = Backbone.View.extend({
      template: "#page_layout",
      manage : true,
      
      initialize: function() {
          console.log("initilizing app layout");
          curr_list_view = null;
          current_add_edit_view = null;
                
      },
          
      render_dashboard: function() {
          // $(this.el)
          //     .html('');
          // $(this.el)
          //     .append(header.render("<li class='active' >Dashboard</li>")
          //     .el);
          this.setView("#header", new HeaderView({serialize: { breadcrumb: $('#dashboard_breadcrumb').html() }}));
          this.setView("#content", new DashboardView());
          this.render();
          //         
          // $(this.el)
          //               .append(dashboard.render()
          //               .el);
          return this;
                   
      },
      render_list_view: function(params) {
          var bcrumb_template = _.template($('#list_breadcrumb').html());
          this.setView("#header", new HeaderView({serialize: { breadcrumb: bcrumb_template({bread:params.view_configs.page_header}) }}));
          this.setView("#content", new ListView({initialize:params}));
          this.render();
          
          // curr_list_view = new ListView(params); // delete the previous curr_list_view ??
          //           $(this.el).append(curr_list_view.render(params.view_configs.page_header)
          //                         .el);
          //             curr_list_view.render(params.view_configs.page_header)
          //           
          return this;
      },
      render_add_edit_view: function(view_configs, data) {
          var add_or_edit = "add";
          if (data) add_or_edit = "edit";
          var bcrumb_template = _.template($('#add_edit_breadcrumb').html());
          
          // $(this.el)
          //               .html('');
          this.setView("#header", new HeaderView({serialize: { breadcrumb: bcrumb_template({bread1:view_configs.page_header.toLowerCase(),bread2:view_configs.page_header,add_or_edit:add_or_edit}) }}));
          // $(this.el)
          //     .append(header.render(bcrumb_template({bread1:view_configs.page_header.toLowerCase(),bread2:view_configs.page_header,add_or_edit:"Add"}))
          //     .el);
          if (view_configs.page_header == "Person") {
              current_add_edit_view = PersonAddEditView;
          } else {
              console.log("not person");
              return this;
          }
          
          this.setView("#content", new current_add_edit_view({
              view_configs: view_configs,
              model_id: data
          }));
          
          this.render();
          
          // $(this.el)
          //              .append(new current_add_edit_view({
          //              view_configs: view_configs,
          //              model_id: data
          //          })
          //              .render()
          //              .el);
          return this;
      }
   
    });
  return new AppLayout;
});
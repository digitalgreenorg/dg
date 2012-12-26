define([
  'jquery',
  'underscore',
  'backbone',
  'views/header',
  'views/dashboard'
  // Using the Require.js text! plugin, we are loaded raw text
  // which will be used as our views primary template
  // 'text!templates/project/list.html'
], function($, _, Session, HeaderView, DashboardView){
    var AppView = Backbone.View.extend({
        el: '#app',
        initialize: function() {
            console.log(HeaderView);
            header = new HeaderView();
            dashboard = new DashboardView({
                                       app: this
                                   });
            curr_list_view = null;
            current_add_edit_view = null;

        },
        render_dashboard: function() {
            $(this.el)
                .html('');
            $(this.el)
                .append(header.render("<li class='active' >Dashboard</li>")
                .el);

            $(this.el)
                .append(dashboard.render()
                .el);
            return this;

        },
        render_list_view: function(view_configs) {
            $(this.el)
                .html('');
            $(this.el)
                .append(header.render("<li><a href='#'>Dashboard</a> <span class='divider'>/</span></li><li class='active'>" + view_configs.page_header + "</li>")
                .el);
            curr_list_view = new list_view(view_configs); // delete the previous curr_list_view ??
            $(this.el)
                .append(curr_list_view.render(view_configs.page_header)
                .el);
            return this;
        },
        render_add_edit_view: function(view_configs, data) {
            console.log("list view seen in add: ");
            console.log(curr_list_view);
            if (curr_list_view) {
                // ToDO: destroy this view, right now just turning off events for its collection 
                // curr_list_view.collection.off();
            }
            var edit_case = false;
            if (data) edit_case = true;
            $(this.el)
                .html('');
            $(this.el)
                .append(header.render('<li><a href="#">Dashboard</a> <span class="divider">/</span></li>\
<li><a href="#' + view_configs.page_header.toLowerCase() + '">' + view_configs.page_header + '</a> <span class="divider">/</span></li>\
<li class="active">' + (edit_case ? 'Edit' : 'Add') + '</li>')
                .el);
            if (view_configs.page_header == "Person") {
                current_add_edit_view = person_add_edit_view;
            } else {
                console.log("not person");
                return this;
            }
            $(this.el)
                .append(new current_add_edit_view({
                view_configs: view_configs,
                model_id: data
            })
                .render()
                .el);
            return this;
        }

    });
  
  // Our module now returns our view
  return AppView;
});
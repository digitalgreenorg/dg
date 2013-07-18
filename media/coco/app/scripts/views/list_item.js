define([
  'jquery',
  'underscore',
  'backbone',
  'form_field_validator',
  'views/notification',
  // Using the Require.js text! plugin, we are loaded raw text
  // which will be used as our views primary template
  // 'text!templates/project/list.html'
], function($,pas,pass, pass,notifs_view){
    

    var ListItemView = Backbone.View.extend({
        tagName: 'tr',
        events: {
            "click a.edit": "edit",
            "click a.destroy": "remove"
        },

        initialize: function(params) {
            this.template = _.template($('#' + params.view_configs.list_item_template_name)
                .html());
            this.error_notif_template = _.template($('#' + 'error_notifcation_template')
                .html());
            this.success_notif_template = _.template($('#' + 'success_notifcation_template')
                .html());
            this.appRouter = params.appRouter;    

        },

        edit: function(event) {
            event.preventDefault();
            event.stopImmediatePropagation();
            this.appRouter.navigate(this.options.view_configs.entity_name+'/edit/' + this.model.id, true);

        },

        remove: function(event) {
            event.stopImmediatePropagation();
            event.preventDefault();
            var context = this;
            if (confirm("Are you sure you want to delete this entry?")) {
                this.model.destroy({
                    error: function() {
                        console.log("error deleting a model");
                        
						notifs_view.add_alert({
						notif_type: "error",
						message: "Failed to Delete the "+ context.options.view_configs.page_header
						});


                    },
                    success: function() {
                        console.log("deleted a model");
                       
						notifs_view.add_alert({
						notif_type: "success",
						message: "Deleted the " + context.options.view_configs.page_header
						});

                    }
                });
            }


        },

        render: function() {
            $(this.el)
                .html(this.template(this.model.toJSON()));
            return this;
        }
    });
    
  // Our module now returns our view
  return ListItemView;
});
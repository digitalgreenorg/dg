define([
  'jquery',
  'underscore',
  'backbone',
  'models/person_model',
  'collections/person_collection',
  'collections/persongroup_collection',
  'collections/village_collection',
  'form_field_validator'
  // Using the Require.js text! plugin, we are loaded raw text
  // which will be used as our views primary template
  // 'text!templates/project/list.html'
], function($,pas,pass, person_model, person_collection, persongroup_collection, village_collection){
    

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

        },

        edit: function(event) {
            event.preventDefault();
            event.stopImmediatePropagation();
            appRouter.navigate('person/edit/' + this.model.id, true);

        },

        remove: function(event) {
            event.stopImmediatePropagation();
            event.preventDefault();
            var context = this;
            if (confirm("Are you sure you want to delete this entry?")) {
                this.model.destroy({
                    error: function() {
                        console.log("error deleting a model");
                        $(notifs_view.el)
                            .append(context.error_notif_template({
                            msg: "Failed to Delete the " + context.options.view_configs.page_header
                        }));


                    },
                    success: function() {
                        console.log("deleted a model");
                        $(notifs_view.el)
                            .append(context.success_notif_template({
                            msg: "Deleted the " + context.options.view_configs.page_header
                        }));

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
define([
  'backbone',
  'indexeddb_backbone_config'
  
], function(_){
    var persongroup_offline_model = Backbone.Model.extend({
        remove: function() {
            this.destroy();
        },
        database: databasev1,
        storeName: "persongroup"

    });
  // Return the model for the module
  return persongroup_offline_model;
});
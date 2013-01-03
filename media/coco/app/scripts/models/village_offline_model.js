define([
  'backbone',
  'indexeddb_backbone_config'
  
], function(_){
    var village_offline_model = Backbone.Model.extend({
        // Common functions
        remove: function() {
            this.destroy();
        },
        database: databasev1,
        storeName: "village"
    });
  
  // Return the model for the module
  return village_offline_model;
});
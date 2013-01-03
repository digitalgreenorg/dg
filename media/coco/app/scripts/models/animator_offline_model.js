define([
  'backbone',
  'indexeddb_backbone_config'
  
], function(_){
    var animator_offline_model = Backbone.Model.extend({
        remove: function() {
            this.destroy();
        },
        database: databasev1,
        storeName: "animator",

    });
  // Return the model for the module
  return animator_offline_model;
});
define([
  'backbone',
  'indexeddb_backbone_config'
  
], function(_){
    var screening_offline_model = Backbone.Model.extend({
        remove: function() {
            this.destroy();
        },
        database: databasev1,
        storeName: "screening",

    });
  // Return the model for the module
  return screening_offline_model;
});
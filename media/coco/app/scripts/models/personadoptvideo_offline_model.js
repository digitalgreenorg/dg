define([
  'backbone',
  'indexeddb_backbone_config'
  
], function(_){
    var personadoptvideo_offline_model = Backbone.Model.extend({
        remove: function() {
            this.destroy();
        },
        database: databasev1,
        storeName: "personadoptvideo",

    });
  // Return the model for the module
  return personadoptvideo_offline_model;
});
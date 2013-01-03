define([
  'backbone',
  'indexeddb_backbone_config'
  
], function(_){
    var video_offline_model = Backbone.Model.extend({
        remove: function() {
            this.destroy();
        },
        database: databasev1,
        storeName: "video",

    });
  // Return the model for the module
  return video_offline_model;
});
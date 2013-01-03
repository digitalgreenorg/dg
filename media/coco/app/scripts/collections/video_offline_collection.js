define([
  'backbone',
  // Pull in the Model module from above
  'models/video_offline_model',
  'indexeddb_backbone_config'
  
], function(_, video_offline_model){
    var video_offline_collection = Backbone.Collection.extend({
        model: video_offline_model,
        database: databasev1,
        storeName: "video",
    });
  
  // You don't usually return a collection instantiated
  return video_offline_collection;
});
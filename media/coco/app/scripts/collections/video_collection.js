define([
  'backbone',
  // Pull in the Model module from above
  'models/video_model',
  'indexeddb_backbone_config'
  
], function(_, video_model){
    var video_offline_collection = Backbone.Collection.extend({
        model: video_model.video_offline_model,
        database: databasev1,
        storeName: "video",
    });
    var video_online_collection = Backbone.Collection.extend({
        model: video_model.video_online_model,
        url: '/api/v1/video/?limit=0',
        sync: Backbone.ajaxSync,
        parse: function(data) {
            return data.objects;
        }

    });
    
  
  // You don't usually return a collection instantiated
  return {
      video_offline_collection: video_offline_collection,
      video_online_collection:video_online_collection
  };
});
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
    
    var video_online_model = Backbone.Model.extend({
        remove: function() {
            this.destroy();
        },
        sync: Backbone.ajaxSync,
        url: function() {
            return this.id ? '/api/v1/video/' + this.id + "/" : '/api/v1/video/?limit=0';
        }

    });
    
  // Return the model for the module
  return {
      video_offline_model : video_offline_model,
      video_online_model : video_online_model
  }
});
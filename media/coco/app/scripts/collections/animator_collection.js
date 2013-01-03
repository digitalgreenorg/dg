define([
  'backbone',
  // Pull in the Model module from above
  'models/animator_model',
  'indexeddb_backbone_config'
  
], function(_, animator_model){
    var animator_offline_collection = Backbone.Collection.extend({
        model: animator_model.animator_offline_model,
        database: databasev1,
        storeName: "animator",
    });
    
    var animator_online_collection = Backbone.Collection.extend({
        model:animator_model.animator_online_model,
        url: '/api/v1/animator/?limit=0',
        sync: Backbone.ajaxSync,
        parse: function(data) {
            return data.objects;
        }

    });
    
  
  // You don't usually return a collection instantiated
  return{ 
      animator_offline_collection:animator_offline_collection,
      animator_online_collection:animator_online_collection
  };
});
define([
  'backbone',
  // Pull in the Model module from above
  'models/screening_model',
  'indexeddb_backbone_config'
  
], function(_, screening_model){
    var screening_offline_collection = Backbone.Collection.extend({
        model: screening_model.screening_offline_model,
        database: databasev1,
        storeName: "screening",
    });
    
    var screening_online_collection = Backbone.Collection.extend({
        model: screening_model.screening_online_model,
        url: '/api/v1/screening/?limit=0',
        sync: Backbone.ajaxSync,
        parse: function(data) {
            return data.objects;
        }

    });
    
  
  // You don't usually return a collection instantiated
  return {
      screening_offline_collection:screening_offline_collection,
      screening_online_collection:screening_online_collection
  };
      
});
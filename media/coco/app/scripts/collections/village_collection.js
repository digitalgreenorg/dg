define([
  'backbone',
  // Pull in the Model module from above
  'models/village_model',
  'indexeddb_backbone_config'
  
], function(_, village_model){
    var village_offline_collection = Backbone.Collection.extend({
        model: village_model.village_offline_model,
        database: databasev1,
        storeName: "village",
    });
    
    var village_online_collection = Backbone.Collection.extend({
        model: village_model.village_online_model,
        url: '/api/v1/village/?limit=0',
        sync: Backbone.ajaxSync,
        parse: function(data) {
            return data.objects;
        }

    });
    
  // You don't usually return a collection instantiated
  return {
      village_offline_collection:village_offline_collection,
      village_online_collection:village_online_collection
  };
});
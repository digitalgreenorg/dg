define([
  'backbone',
  // Pull in the Model module from above
  'models/village_offline_model',
  'indexeddb_backbone_config'
  
], function(_, village_offline_model){
    var village_offline_collection = Backbone.Collection.extend({
        model: village_offline_model,
        database: databasev1,
        storeName: "village",
    });
  // You don't usually return a collection instantiated
  return village_offline_collection;
});
define([
  'backbone',
  // Pull in the Model module from above
  'models/animator_offline_model',
  'indexeddb_backbone_config'
  
], function(_, animator_offline_model){
    var animator_offline_collection = Backbone.Collection.extend({
        model: animator_offline_model,
        database: databasev1,
        storeName: "animator",
    });
  
  // You don't usually return a collection instantiated
  return animator_offline_collection;
});
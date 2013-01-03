define([
  'backbone',
  // Pull in the Model module from above
  'models/screening_offline_model',
  'indexeddb_backbone_config'
  
], function(_, screening_offline_model){
    var screening_offline_collection = Backbone.Collection.extend({
        model: screening_offline_model,
        database: databasev1,
        storeName: "screening",
    });
  
  // You don't usually return a collection instantiated
  return screening_offline_collection;
});
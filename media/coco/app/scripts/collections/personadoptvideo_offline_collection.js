define([
  'backbone',
  // Pull in the Model module from above
  'models/personadoptvideo_offline_model',
  'indexeddb_backbone_config'
  
], function(_, personadoptvideo_offline_model){
    var personadoptvideo_offline_collection = Backbone.Collection.extend({
        model: personadoptvideo_offline_model,
        database: databasev1,
        storeName: "personadoptvideo",
    });

  
  // You don't usually return a collection instantiated
  return personadoptvideo_offline_collection;
});
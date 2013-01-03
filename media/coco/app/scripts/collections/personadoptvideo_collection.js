define([
  'backbone',
  // Pull in the Model module from above
  'models/personadoptvideo_model',
  'indexeddb_backbone_config'
  
], function(_, personadoptvideo_model){
    var personadoptvideo_offline_collection = Backbone.Collection.extend({
        model: personadoptvideo_model.personadoptvideo_offline_model,
        database: databasev1,
        storeName: "personadoptvideo",
    });
    
    var personadoptvideo_online_collection = Backbone.Collection.extend({
        model: personadoptvideo_model.personadoptvideo_online_model,
        url: '/api/v1/personadoptvideo/?limit=0',
        sync: Backbone.ajaxSync,
        parse: function(data) {
            return data.objects;
        }

    });
    

  
  // You don't usually return a collection instantiated
  return {
      personadoptvideo_offline_collection:personadoptvideo_offline_collection,
      personadoptvideo_online_collection:personadoptvideo_online_collection
  };
});
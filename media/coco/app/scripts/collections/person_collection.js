define([
  'backbone',
  'indexeddb-backbone',
  // Pull in the Model module from above
  'models/person_model',
  'indexeddb_backbone_config'
  
], function(_, pass, person_model){
  var person_offline_collection = Backbone.Collection.extend({
    model: person_model.person_offline_model,
    database: databasev1,
    storeName: "person",
});

var person_online_collection = Backbone.Collection.extend({
    model: person_model.person_online_model,
    url: '/api/v1/person/',
    sync: Backbone.ajaxSync,
    parse: function(data) {
        return data.objects;
    }

});

  return {
      person_offline_collection:person_offline_collection,
      person_online_collection:person_online_collection
  };
});
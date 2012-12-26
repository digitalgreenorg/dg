define([
  'underscore',
  'backbone',
  // Pull in the Model module from above
  'models/person_offline_model'
], function(_, person_offline_model){
  var person_offline_collection = Backbone.Collection.extend({
    model: person_offline_model,
    database: databasev1,
    storeName: "person",
});
  // You don't usually return a collection instantiated
  return person_offline_collection;
});
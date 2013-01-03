define([
  'backbone',
  // Pull in the Model module from above
  'models/persongroup_offline_model',
  'indexeddb_backbone_config'
  
], function(_, persongroup_offline_model){
    var persongroup_offline_collection = Backbone.Collection.extend({
        model: persongroup_offline_model,
        database: databasev1,
        storeName: "persongroup",


        by_village: function(vill_id) {
            return this.filter(function(pg) {
                return pg.get("village")
                    .id == vill_id;
            });
        }
    });
  
  // You don't usually return a collection instantiated
  return persongroup_offline_collection;
});
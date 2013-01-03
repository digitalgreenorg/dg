define([
  'backbone',
  // Pull in the Model module from above
  'models/persongroup_model',
  'indexeddb_backbone_config'
  
], function(_, persongroup_model){
    var persongroup_offline_collection = Backbone.Collection.extend({
        model: persongroup_model.persongroup_offline_model,
        database: databasev1,
        storeName: "persongroup",


        by_village: function(vill_id) {
            return this.filter(function(pg) {
                return pg.get("village")
                    .id == vill_id;
            });
        }
    });
    
    var persongroup_online_collection = Backbone.Collection.extend({
        model: persongroup_model.persongroup_online_model,
        url: '/api/v1/group/?limit=0',
        sync: Backbone.ajaxSync,
        parse: function(data) {
            return data.objects;
        }

    });
    
  
  // You don't usually return a collection instantiated
  return {
      persongroup_offline_collection:persongroup_offline_collection,
      persongroup_online_collection:persongroup_online_collection
  };
});
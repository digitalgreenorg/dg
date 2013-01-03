define([
  'backbone',
  'indexeddb_backbone_config'
  
], function(_){
    var persongroup_offline_model = Backbone.Model.extend({
        remove: function() {
            this.destroy();
        },
        database: databasev1,
        storeName: "persongroup"

    });
    
    var persongroup_online_model = Backbone.Model.extend({
        remove: function() {
            this.destroy();
        },
        sync: Backbone.ajaxSync,
        url: function() {
            return this.id ? '/api/v1/group/' + this.id + "/" : '/api/v1/group/?limit=0';
        }

    });
    
  // Return the model for the module
  return {
      persongroup_offline_model : persongroup_offline_model,
      persongroup_online_model : persongroup_online_model
  } 
  
});
define([
  'backbone',
  'indexeddb_backbone_config'
  
], function(_){
    var village_offline_model = Backbone.Model.extend({
        // Common functions
        remove: function() {
            this.destroy();
        },
        database: databasev1,
        storeName: "village"
    });
    
    var village_online_model = Backbone.Model.extend({
        remove: function() {
            this.destroy();
        },
        sync: Backbone.ajaxSync,
        url: function() {
            return this.id ? '/api/v1/village/' + this.id + "/" : '/api/v1/village/?limit=0';
        }

    });
    
  
  // Return the model for the module
  return {
      village_offline_model : village_offline_model,
      village_online_model : village_online_model
  };

});
define([
  'backbone',
  'indexeddb_backbone_config'
  
], function(_){
    var animator_offline_model = Backbone.Model.extend({
        remove: function() {
            this.destroy();
        },
        database: databasev1,
        storeName: "animator",

    });
    
    var animator_online_model = Backbone.Model.extend({
        remove: function() {
            this.destroy();
        },
        sync: Backbone.ajaxSync,
        url: function() {
            return this.id ? '/api/v1/animator/' + this.id + "/" : '/api/v1/animator/?limit=0';
        }

    });
    
  // Return the model for the module
  return{ 
      animator_offline_model : animator_offline_model,
      animator_online_model : animator_online_model
  }
  
});
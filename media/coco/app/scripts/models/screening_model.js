define([
  'backbone',
  'indexeddb_backbone_config'
  
], function(_){
    var screening_offline_model = Backbone.Model.extend({
        remove: function() {
            this.destroy();
        },
        database: databasev1,
        storeName: "screening",

    });
    
    var screening_online_model = Backbone.Model.extend({
        remove: function() {
            this.destroy();
        },
        sync: Backbone.ajaxSync,
        url: function() {
            return this.id ? '/api/v1/screening/' + this.id + "/" : '/api/v1/screening/?limit=0';
        }

    });
    
  // Return the model for the module
  return {
      screening_offline_model : screening_offline_model,
       screening_online_model : screening_online_model
  }
});
define([
  'backbone',
  'indexeddb_backbone_config'
  
], function(_){
    var personadoptvideo_offline_model = Backbone.Model.extend({
        remove: function() {
            this.destroy();
        },
        database: databasev1,
        storeName: "personadoptvideo",

    });
    
    var personadoptvideo_online_model = Backbone.Model.extend({
        remove: function() {
            this.destroy();
        },
        sync: Backbone.ajaxSync,
        url: function() {
            return this.id ? '/api/v1/personadoptvideo/' + this.id + "/" : '/api/v1/personadoptvideo/?limit=0';
        }

    });
    
  // Return the model for the module
  return {
       personadoptvideo_offline_model : personadoptvideo_offline_model,
       personadoptvideo_online_model : personadoptvideo_online_model
   
    }
});
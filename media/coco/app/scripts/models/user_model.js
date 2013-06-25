define([
  'jquery',
  'backbone',
  'indexeddb_backbone_config',
  'indexeddb-backbone',
  'collections/upload_collection'
  // Using the Require.js text! plugin, we are loaded raw text
  // which will be used as our views primary template
  // 'text!templates/project/list.html'
], function(jquery, backbone, indexeddb, idb_backbone_adapter, UploadCollection){
    
    var generic_model_offline = Backbone.Model.extend({
        database: indexeddb,
        storeName: "user",
        isOnline: function(){
            return navigator.onLine;
        },
        isLoggedIn: function(){
            //TODO: should fetch itself first to get latest state?
            // should this be handled by the auth module
            return this.get("loggedin");
        },
        canSaveOnline: function(){
            return this.isOnline() && UploadCollection.fetched && UploadCollection.length===0
        }
    });
    var user_model = new generic_model_offline();
    user_model.set({key: "user_info"});
    
  return user_model;
});
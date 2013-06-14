define([
  'jquery',
  'backbone',
  'indexeddb_backbone_config',
  'indexeddb-backbone',
  // Using the Require.js text! plugin, we are loaded raw text
  // which will be used as our views primary template
  // 'text!templates/project/list.html'
], function(jquery, backbone, indexeddb, idb_backbone_adapter){
    
    var generic_model_offline = Backbone.Model.extend({
        database: indexeddb,
        storeName: "user",
    });
    var user_model = new generic_model_offline();
    user_model.set({key: "user_info"});
    
  return user_model;
});
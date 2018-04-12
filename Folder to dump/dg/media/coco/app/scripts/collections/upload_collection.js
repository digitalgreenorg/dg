define([
  'jquery',
  'backbone',
  'indexeddb_backbone_config',
  'indexeddb-backbone'      
  // Using the Require.js text! plugin, we are loaded raw text
  // which will be used as our views primary template
  // 'text!templates/project/list.html'
], function(jquery, backbone, indexeddb){
    
    var generic_model_offline = Backbone.Model.extend({
        database: indexeddb,
        storeName: "uploadqueue",
    });

    var generic_upload_collection = Backbone.Collection.extend({
        model: generic_model_offline,
        database: indexeddb,
        storeName: "uploadqueue",
        fetched: false
    });
    var upload_collection = new generic_upload_collection();
    upload_collection.fetch({
        success: function(coll){
            console.log("UPLOADCOLLECTION : successfully fetched");
            coll.fetched = true; 
        },
        error: function(){
            console.log("UPLOADCOLLECTION :  fetch failed")            
        }        
    });
    
    // upload_collection.on('add')
            
  // Our module now returns our view
  return upload_collection;
});
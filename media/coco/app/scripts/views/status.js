define([
  'jquery',
  'underscore',
  'backbone',
      'indexeddb_backbone_config',
'views/full_download',
          'configs',
    'collections/upload_collection'                
  // Using the Require.js text! plugin, we are loaded raw text
  // which will be used as our views primary template
  // 'text!templates/project/list.html'
], function($,_,pass,indexeddb,FullDownloadView, configs, upload_collection){
    
    var StatusView = Backbone.Layout.extend({
        template: "#status",
        events: {
            "click button#download": "download",
        },
        serialize: function(){
            return {
                timestamp: this.timestamp,
                upload_entries: this.upload_entries
            }
        },
        timestamp: null,
        upload_entries: null,                    
        initialize: function(){
            var generic_model_offline = Backbone.Model.extend({
                database: indexeddb,
                storeName: "meta_data",
            });
            var meta_model = new generic_model_offline();
            meta_model.set({key: "last_downloaded"});
            var that = this;
            meta_model.fetch({
                success: function(model){
                    console.log("STATUS: last_downloaded fetched from meta_data objectStore:");
                    console.log(JSON.stringify(model.toJSON()));
                    that.timestamp = model.get('timestamp');
                    that.upload_entries =  upload_collection.length;
                    //TODO: set template when db is populated
                    that.template = "#sync_status_template";
                    that.render();    
                    
                },
                error: function(error){
                    console.log("STATUS: error while fetching last_downloaded from meta_data objectStore");
                    console.log(error);
                    if(error == "Not Found")
                        {
                           that.template = "#first_time_status";
                           that.render();
                        }    
                }        
            });
        },
        download: function(){
            this.setView("#download_modal",new FullDownloadView());
            this.render();
        }    
    
          
    });
    
  // Our module now returns our view
  return StatusView;
});
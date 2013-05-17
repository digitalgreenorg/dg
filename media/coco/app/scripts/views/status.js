define([
    'jquery',
    'underscore',
    'backbone',
    'indexeddb_backbone_config',
    'views/full_download',
    'configs',
    'collections/upload_collection'                
], function($,p,pass,indexeddb,FullDownloadView, configs, upload_collection){
    
    var StatusView = Backbone.Layout.extend({
        template: "#sync_status_template",
        events: {
            "click button#download": "download",
            "click button#reset_database": "reset"
        },
        serialize: function(){
            return {
                timestamp: this.timestamp,
                num_upload_entries: this.upload_entries,
                upload_collection: upload_collection.toJSON()
            }
        },
        timestamp: null,
        upload_entries: null,
        fill_status: function(){
            var that = this;
            // this.template = "#sync_status_template";
            that.upload_entries =  upload_collection.length;
            var generic_model_offline = Backbone.Model.extend({
                database: indexeddb,
                storeName: "meta_data",
            });
            var meta_model = new generic_model_offline();
            meta_model.set({key: "last_full_download"});
            meta_model.fetch({
                success: function(model){
                    console.log("STATUS: last_downloaded fetched from meta_data objectStore:");
                    console.log(JSON.stringify(model.toJSON()));
                    that.timestamp = model.get('timestamp');
                    //TODO: set template when db is populated
                    // that.template = "#sync_status_template";
                    console.log(that.template);
                    // that.render();
                    that.render().done(function(){console.log("finished after download render");});    
                    
                },
                error: function(error){
                    console.log("STATUS: error while fetching last_downloaded from meta_data objectStore");
                    console.log(error);
                    if(error == "Not Found")
                        {
                            //Start download automatically
                           // that.template = "#first_time_status";
                           // that.template = "#first_time_status";
                           that.render()
                               .done(function(){
                                   that.download();
                               });
                           // that.download();
                        }    
                }        
            });
        },                        
        initialize: function(){
            _(this).bindAll('fill_status');
            // upload_collection.bind('reset',this.fill_status);   
//             upload_collection.bind('remove',this.fill_status);   
            
            this.fill_status();
            
        },
        download: function(){
            var dfd = new $.Deferred();
            if(!this.full_download_v)
            {
                this.full_download_v = new FullDownloadView();
            }
            this.setView("#modal",this.full_download_v).render();
            var that = this;
            this.full_download_v.start_full_download()
                .done(function(){
                    that.fill_status();
                    dfd.resolve();
                })
                .fail(function(){
                   dfd.reject(); 
                });
            return dfd;
        },
        
        reset: function(){
            var request = indexedDB.deleteDatabase("offline-database");
            request.onerror = function(event) {
                console.log(event);
                console.log("RESET DATABASE:Error!");
                alert("Error while resetting database! Refresh the page and try again.");
            };
            request.onsuccess = function(event) {
                console.log("RESET DATABASE:Success!");
                location.reload();
            }
            request.onblocked = function(event) {
                console.log("RESET DATABASE:Blocked!");
                location.reload();
            };
        }    
    
          
    });
    
  // Our module now returns our view
  return StatusView;
});
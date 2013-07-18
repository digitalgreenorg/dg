define([
    'jquery',
    'underscore',
    'layoutmanager',
    'indexeddb_backbone_config',
    'views/full_download',
    'configs',
    'collections/upload_collection',
    'views/notification',
    'offline_utils',                
    'indexeddb-backbone'
], function(jquery, underscore, layoutmanager, indexeddb, FullDownloadView, configs, upload_collection, notifs_view, Offline){
    
    var StatusView = Backbone.Layout.extend({
        template: "#status",
        timestamp: null,
        upload_entries: null,
        events: {
            "click button#download": "download",
            "click button#reset_database": "reset"
        },
        
        initialize: function(){
            _(this).bindAll('fill_status');
            //upload_collection.on("all",this.fill_status);
            this.fill_status();
        },
        
        serialize: function(){
            return {
                full_d_timestamp: this.full_download_timestamp,
                inc_d_timestamp: this.inc_download_timestamp,
                num_upload_entries: this.upload_entries,
				db_version: this.db_version,
                upload_collection: upload_collection.toJSON()
            }
        },
       
        fill_status: function(){
            var that = this;
            that.upload_entries =  upload_collection.length;
			that.db_version = indexeddb.migrations[0].version;
            
            Offline.fetch_object("meta_data", "key", "last_full_download")
                .done(function(model){
                    that.full_download_timestamp = new Date(model.get('timestamp'));
                    Offline.fetch_object("meta_data", "key", "last_inc_download")
                        .done(function(model){
                            that.inc_download_timestamp = new Date(model.get('timestamp'));
                            that.render();
                        })
                        .fail(function(model, error){
                            that.inc_download_timestamp = "Never";
                            that.render();
                        });
                    that.render();
                })
                .fail(function(model, error){
                    console.log("STATUS: error while fetching last_downloaded from meta_data objectStore");
                    console.log(error);
                    if(error == "Not Found")
                        {
                            that.full_download_timestamp = "Never";
                            //Start download automatically
                            that.render()
                               .done(function(){
                                   that.download();
                               });
                        }    
                });
                
            
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
                
                    notifs_view.add_alert({
						notif_type: "success",
						message: "Successfully downloaded the database"
					});
					dfd.resolve();
                })
                .fail(function(error){
                    
					notifs_view.add_alert({
						notif_type: "error",
						message: "Failed to download the database : "+error
					});
                   dfd.reject(); 
                });
            return dfd;
        },
        
        reset: function(){
            Offline.reset_database();
        }    
    
          
    });
    
  // Our module now returns our view
  return StatusView;
});
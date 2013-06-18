define([
    'jquery', 
    'underscore', 
    'configs', 
    'indexeddb_backbone_config', 
    'collections/upload_collection',
    'views/upload', 
    'views/incremental_download',
    'views/notification',
    'layoutmanager',      
    'models/user_model',
    'auth'
    ],
 function(jquery, pass, configs, indexeddb, upload_collection, UploadView, IncDownloadView, notifs_view, layoutmanager,User, Auth) {

    var DashboardView = Backbone.Layout.extend({
        template: "#dashboard",
        events: {
            // "click button#download": "Download",
            "click #sync": "sync",
            "click #inc_download": "inc_download",
            "click #logout": "logout"
        },
        
        item_template: _.template($("#dashboard_item_template")
            .html()),
        initialize: function() {
            this.upload_v = null;
            this.inc_download_v = null;
            this.background_download();
            _(this).bindAll('render');
            User.on('change',this.render);
        },
        serialize: function(){
            var username =  User.get("username");
            return {
                username:username
            }
        },
        afterRender: function() { /* Work with the View after render. */
            // this.collection.fetch();
            console.log("rendering dashboard");
            for (var member in configs) {
                // console.log(configs[member]);
                if(member=="misc")
                    continue;
                var listing =true;
                var add = true;
                if(configs[member].dashboard_display)
                {
                    listing = configs[member].dashboard_display.listing;
                    add = configs[member].dashboard_display.add;
                }
                if(listing||add)
                {
                    if(listing)
                    {
                        $('#dashboard_items')
                            .append(this.item_template({
                            name: member+"/list",
                            title: configs[member]["page_header"]
                        }));
                    }
                    if(add)
                    {
                        $('#dashboard_items_add')
                            .append(this.item_template({
                            name: member+"/add",
                            title: '<i class="icon-plus-sign"></i>'
                        }));
                    }
                    else
                    {
                        $('#dashboard_items_add')
                            .append("<li><i class='icon-white icon-plus-sign'></li>");
                    }
                }
                    

            }
        },
        
        sync: function(){
            var that = this;
            //If background inc download is in progress, tel user to wait till its finished
            //TODO: alterntely we can interrupt inc download and start with sync
            if(this.inc_download_v)
            {
                if(this.inc_download_v.in_progress)
                {
                    alert("Please wait till download is finished");
                    return;
                }
            }
            this.sync_in_progress = true;
            this.upload()
                .done(function(){
                    console.log("UPLOAD FINISHED");
                    notifs_view.add_alert({
						notif_type: "success",
						message: "Upload successfully finished"
						});
                })
                .fail(function(error){
                    console.log("ERROR IN UPLOAD");
                    console.log(error);
                   
					notifs_view.add_alert({
						notif_type: "error",
						message: "Sync Incomplete. Failed to finish upload : "+error
					});
                })
                .always(function(){
                    that.inc_download({background:false})
                        .done(function(){
                            console.log("INC DOWNLOAD FINISHED");
                            that.sync_in_progress = false;
                            
							notifs_view.add_alert({
								notif_type: "success",
								message: "Incremental download successfully finished"
							});
                        })
                        .fail(function(error){
                            console.log("ERROR IN INC DOWNLOAD");
                            console.log(error);
                            that.sync_in_progress = false;
                            
							notifs_view.add_alert({
								notif_type: "error",
								message: "Sync Incomplete. Failed to do Incremental Download: "+error
							});
							
                        });
                });
        },
        
        upload: function(){
            var dfd = $.Deferred();
            if(!this.upload_v){
                this.upload_v = new UploadView();
            }
            this.setView("#upload_modal_ph",this.upload_v);
            this.upload_v.render();
            this.upload_v.start_upload()
                .done(function(){
                    return dfd.resolve();
                })
                .fail(function(error){
                   return dfd.reject(error); 
                });
            return dfd;
        },
            
        inc_download: function(options){
            var dfd = $.Deferred();
            var that = this;
            if(!this.inc_download_v)
            {
                this.inc_download_v = new IncDownloadView();
            }
            if(this.inc_download_v.in_progress)
            {
                return dfd.resolve();
            }
            this.setView("#upload_modal_ph",this.inc_download_v);
            this.inc_download_v.render();
            this.inc_download_v.start_incremental_download(options)
                .done(function(){
                    return dfd.resolve();
                })
                .fail(function(error){
                    return dfd.reject(); 
                });
            return dfd;
        },
        
        background_download: function(){
            var that = this;
            console.log("Going for background inc download");
            var call_again = function(){
                setTimeout(function(){that.background_download();}, configs.misc.background_download_interval);
            };
            //check if uploadqueue is empty and internet is connected - if both true do the background download
            if(this.is_uploadqueue_empty() && this.is_internet_connected() && !this.sync_in_progress)
            {
                this.inc_download({background:true})
                    .always(call_again);
            }
            else{
                call_again();
            }
        },
        
        is_uploadqueue_empty : function(){
            return upload_collection.fetched&&upload_collection.length<=0;    
        },
        
        is_internet_connected : function(){
            return navigator.onLine;
        },               

        logout: function(){
            Auth.logout()
                .always(function(){
                    window.Router.navigate('login', {trigger:true});
                });
        }
    });


    // Our module now returns our view
    return DashboardView;
});

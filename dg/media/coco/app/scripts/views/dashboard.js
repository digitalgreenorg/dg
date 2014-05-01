//This view contains the links to add and list pages of entities, the sync button, logout link, online-offline indicator
define(['jquery', 'underscore', 'configs', 'indexeddb_backbone_config', 'collections/upload_collection', 'views/upload', 'views/incremental_download', 'views/notification', 'layoutmanager', 'models/user_model', 'auth', 'offline_utils', 'views/full_download' ],

function(jquery, pass, configs, indexeddb, upload_collection, UploadView, IncDownloadView, notifs_view, layoutmanager, User, Auth, Offline, FullDownloadView) {

    var DashboardView = Backbone.Layout.extend({
        template: "#dashboard",
        events: {
            "click #sync": "sync",
            "click #inc_download": "inc_download",
            "click #logout": "logout"
        },
        item_template: _.template($("#dashboard_item_template")
            .html()),

        initialize: function() {
            this.upload_v = null;
            this.inc_download_v = null;
            //start the background inc download process
            this.background_download();
            _(this)
                .bindAll('render');
            //re-render the view when User model changes - to keep username updated    
            User.on('change', this.render);
            this.upload_entries = upload_collection.length;
        },

        serialize: function() {
            // send username and # of uploadQ items to the template 
            var username = User.get("username");
            return {
                username: username,
                upload_entries: this.upload_entries
            }
        },

        afterRender: function() { 
            console.log("rendering dashboard");
            //iterate over entities defined in config and create their "list" and "add" rows 
            for (var member in configs) {
                if (member == "misc") continue;
                var listing = true;
                var add = true;
                var enable_months;
                // check entity's config for whether to show list/add links for this entity
                if (configs[member].dashboard_display) {
                    listing = configs[member].dashboard_display.listing;
                    add = configs[member].dashboard_display.add;
                    enable_months = configs[member].dashboard_display.enable_months;
                }
                if(typeof enable_months != 'undefined'){
                	var d = new Date();
                    n = d.getMonth() + 1;
                    res = $.inArray(n, enable_months);
                    if(res === -1){
                    	add = false;
                    }
                }
                if (listing || add) {
                    if (listing) $('#dashboard_items')
                        .append(this.item_template({
                        name: member + "/list",
                        title: configs[member]["page_header"] + 's'
                    }));

                    if (add) $('#dashboard_items_add')
                        .append(this.item_template({
                        name: member + "/add",
                        title: '<i class="glyphicon glyphicon-plus-sign"></i>'
                    }));
                    else $('#dashboard_items_add')
                        .append("<li class='disabled'><a><i class='glyphicon glyphicon-plus-sign' title='You are not allowed to add this currently'></a></li>");
                }
            }
            
            //keep the # uploadq entries shown on view up-to-date
            upload_collection.on('all', function() {
                $("#upload_num")
                    .html(function() {
                    return upload_collection.length;
                });
            });
            
            //keep the online-offline indicator up-to-date
            window.addEventListener("offline", this.user_offline);
            //keep the online-offline indicator up-to-date
            window.addEventListener("online", this.user_online);

            //set the online-offline indicator
            if (User.isOnline()) {
                this.user_online();
            } else {
                this.user_offline();
            }
            var that = this;
            
            //disable all links of db not yet downloaded
            Offline.fetch_object("meta_data", "key", "last_full_download")
                .done(function(model) {
                that.db_downloaded();
            })
                .fail(function(model, error) {
                that.db_not_downloaded();
            });
        },
        
        //enable sync button, show online indicator
        user_online: function() {
            $('#sync')
                .removeAttr("disabled");
            $('#offline')
                .hide();
            $('#online')
                .show();
        },

        //disable sync button, show offline indicator
        user_offline: function() {
            $('#sync')
                .attr('disabled', true);
            $('#online')
                .hide();
            $('#offline')
                .show();
        },

        //enable add, list links
        db_downloaded: function() {
            $('.list_items')
                .unbind('click', false);
            $('.list_items')
                .removeClass("disabled");
            console.log("Dashboard links enabled");
            $("#helptext")
                .hide();
        },

        //disable add, list links
        db_not_downloaded: function() {
            $('.list_items')
                .bind('click', false);
            $('.list_items')
                .addClass("disabled");
            console.log("Dashboard links disabled");
            $("#helptext")
                .show();
        },

        //if DB exists initiate upload and then inc download otherwise start full download
        sync: function() {
            var that = this;
            if (this.inc_download_v && this.inc_download_v.in_progress) {
                alert("Please wait till background download is finished.");
                return;
            }
            Offline.fetch_object("meta_data", "key", "last_full_download")
                .done(function(model) {
                console.log("In Sync: db completely downloaded");
                that.sync_in_progress = true;
                //start upload
                that.upload()
                    .done(function() {
                    console.log("UPLOAD FINISHED");
                    notifs_view.add_alert({
                        notif_type: "success",
                        message: "Sync successfully finished"
                    });
                })
                    .fail(function(error) {
                    console.log("ERROR IN UPLOAD :" + error);
                    notifs_view.add_alert({
                        notif_type: "error",
                        message: "Sync Incomplete. Failed to finish upload : " + error
                    });
                })
                    .always(function() {
                    //upload finished
                    //start inc download - even if upload failed    
                    that.inc_download({
                        background: false
                    })
                        .done(function() {
                        console.log("INC DOWNLOAD FINISHED");
                        that.sync_in_progress = false;
                        notifs_view.add_alert({
                            notif_type: "success",
                            message: "Incremental download successfully finished"
                        });
                    })
                        .fail(function(error) {
                        console.log("ERROR IN INC DOWNLOAD");
                        console.log(error);
                        that.sync_in_progress = false;
                        notifs_view.add_alert({
                            notif_type: "error",
                            message: "Sync Incomplete. Failed to do Incremental Download: " + error
                        });

                    });
                });

            })
                .fail(function(model, error) {
                // if DB is not downloaded, start the full download    
                if (error == "Not Found") {
                    that.render()
                        .done(function() {
                        console.log("In Sync: db not completely downloaded");
                        that.download();
                    });
                }
            });

        },
        
        //method to initiate full download
        download: function() {
            var dfd = new $.Deferred();
            //create full download view
            if (!this.full_download_v) {
                this.full_download_v = new FullDownloadView();
            }
            //this view has a modal interface therefore appending to body
            $(this.full_download_v.el)
                .appendTo('body');
            this.full_download_v.render();
            var that = this;
            //start full download
            this.full_download_v.start_full_download()
                .done(function() {
                notifs_view.add_alert({
                    notif_type: "success",
                    message: "Successfully downloaded the database"
                });
                dfd.resolve();
            })
                .fail(function(error) {
                notifs_view.add_alert({
                    notif_type: "error",
                    message: "Failed to download the database : " + error
                });
                dfd.reject();
            });
            return dfd;
        },

        //method to initiate upload
        upload: function() {
            var dfd = $.Deferred();
            if (!this.upload_v) {
                this.upload_v = new UploadView();
            }
            $(this.upload_v.el)
                .appendTo('body');
            this.upload_v.render();
            this.upload_v.start_upload()
                .done(function() {
                return dfd.resolve();
            })
                .fail(function(error) {
                return dfd.reject(error);
            });
            return dfd;
        },

        //method to initiate inc download
        inc_download: function(options) {
            var dfd = $.Deferred();
            var that = this;
            if (!this.inc_download_v) {
                this.inc_download_v = new IncDownloadView();
            }
            if (this.inc_download_v.in_progress) {
                return dfd.resolve();
            }
            $(this.inc_download_v.el)
                .appendTo('body');
            //options contains whether to show modal or do it in background    
            this.inc_download_v.start_incremental_download(options)
                .done(function() {
                return dfd.resolve();
            })
                .fail(function(error) {
                return dfd.reject();
            });
            return dfd;
        },
        
        //starts the background inc download process
        background_download: function() {
            var that = this;
            console.log("Going for background inc download");
            
            //function to set timer to start inc download after time interval defined in config file
            var call_again = function() {
                setTimeout(function() {
                    that.background_download();
                }, configs.misc.background_download_interval);
            };

            //check if uploadqueue is empty and internet is connected - if both true do the background download
            if (this.is_uploadqueue_empty() && this.is_internet_connected() && !this.sync_in_progress) this.inc_download({
                background: true
            })
            //when the inc download is finished set the timer to start it again later
                .always(call_again);
            //if cant do inc download right now, just set the timer to start it again later    
            else call_again();
        },

        // check emptiness of uploadQ
        is_uploadqueue_empty: function() {
            //return false if the check is made before uploadQ collection could be fetched from DB
            return upload_collection.fetched && upload_collection.length <= 0;
        },

        // check internet connection
        is_internet_connected: function() {
            return navigator.onLine;
        },
        
        // logout and navigate to login url
        logout: function() {
            Auth.logout()
                .always(function() {
                window.Router.navigate('login', {
                    trigger: true
                });
            });
        }
    });


    // Our module now returns our view
    return DashboardView;
});

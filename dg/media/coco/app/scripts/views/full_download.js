// Performs the full database download. For each entity defined in configs, creates chunked requests to fetch data 
// from server and saves it in offline db. To make it resumable, it does not clear the database before starting downloading. 
// For each chunk request created, it checks if that chunk request was already downloaded by looking into the full_download_info store in offline DB. 
// Since it continues from the present state of database found - In order to do a fresh download, there needs to be some 
// external code which flushes the database before calling this module.
// 
// To use the module, initialize a new object and call start_full_download on it.

define([
    'jquery',
    'underscore',
    'layoutmanager',
    'indexeddb_backbone_config',
    'configs',
    'offline_utils',
    'bootstrapjs'
], function(jquery, underscore, layoutmanager, indexeddb, all_configs, Offline) {


    var FullDownloadView = Backbone.Layout.extend({

        initialize: function() {
            _.bindAll(this);
        },

        template: "#download_template",

        internet_connected: function() {
            return navigator.onLine;
        },

        //send the list of entities to the template 
        serialize: function() {
            return {
                all_configs: all_configs
            }
        },

        events: {
            'click #stop_full_download': 'stop_download'
        },

        //executed when user clicks stop donwload button 
        stop_download: function() {
            console.log("stopping download");
            //remove the view
            this.remove_ui();
            //abort all the network requests made by this module
            $.each(this.network_requests, function(index, xhr) {
                xhr.abort();
            });

            this.full_download_dfd.reject("User stopped download");

        },

        remove_ui: function() {
            // calling remove without hiding modal causes modal's backdrop to remain
            this.$('#full_download_modal').modal('hide');
            this.remove();
        },

        // Checks internet connectivity
        // Initializes UI and objects used to update status. 
        // Fetches the full_download_info objectStore to resume download, if that's the case
        // Stores the start time for download
        initialize_download: function() {
            //Django complains when Z is present in timestamp bcoz timezone capab is off
            this.start_time = new Date().toJSON().replace("Z", "");

            //check whether internet is accessible - if not, abort full download
            if (!this.internet_connected()) {
                // this function is expected to return a dfd, so create a new dfd, reject it and return it
                var dfd = new $.Deferred();
                dfd.reject("Can't download database. Internet is not connected");
                return dfd;
            }
            //intialize UI objects
            this.$('#full_download_modal').modal({
                keyboard: false,
                backdrop: "static",
            });
            this.$('#full_download_modal').modal('show');
            
            //used to store the current download-status of each entity  
            this.download_status = {};

            //every request made to server will be stored in this, - to abort them if user chooses to stop download
            this.network_requests = [];

            //get the list of chunks that exists already downloaded - to resume download 
            var already_downloaded_chunks_dfd = this.get_already_downloaded_chunks();
            
            //get the original start time if download is resumed or else set th current time as the start time
            var start_time_dfd = this.fetch_or_set_download_start_time();
            
            //return combined dfd 
            return $.when.apply($, [already_downloaded_chunks_dfd, start_time_dfd]);
        },

        // fetching the full_download_info table to get all already downloaded chunks - to be used for resuming download
        get_already_downloaded_chunks: function() {
            var dfd = new $.Deferred();
            var that = this;
            Offline.fetch_collection("full_download_info")
                .done(function(coll) {
                    that.full_download_info_coll = coll;
                    dfd.resolve();
                })
                .fail(function(error) {
                    dfd.reject(error);
                });
            return dfd;

        },

        //if download is resuming then get the original start time other wise record current time as start time
        fetch_or_set_download_start_time: function() {
            var dfd = new $.Deferred();
            var that = this;
            Offline.fetch_object("meta_data", "key", "last_full_download_start")
                .fail(function(model, error) {
                    that.set_timestamp(model, that.start_time)
                        .done(function() {
                            dfd.resolve();
                        })
                        .fail(function(error) {
                            dfd.reject(error);
                        });
                })
                .done(function(model) {
                    that.start_time = model.get("timestamp");
                    dfd.resolve();
                });
            return dfd;
        },

        set_timestamp: function(model, timestamp) {
            model.set('timestamp', timestamp);
            //returns a promise object
            return model.save(); 
        },

        // this starts the full download process 
        start_full_download: function() {
            this.full_download_dfd = new $.Deferred();
            var that = this;
            //run some intitialization logic - check internt, setup ui etc
            this.initialize_download()
                .done(function() {
                    //iterate over entities and start their download
                    that.iterate_object_stores()
                        .done(function() {
                            //run some finish logic - save the timsetamp 
                            that.finish_download()
                                .done(function() {
                                    //run any after download logic defined by user
                                    that.call_after_download()
                                        .done(function() {
                                            // full download finised successfully
                                            that.remove_ui();
                                            that.full_download_dfd.resolve();
                                        })
                                        .fail(function(error) {
                                            //user defined after download failed
                                            that.remove_ui();
                                            that.full_download_dfd.reject(error);
                                        });
                                })
                                .fail(function(error) {
                                    //something in finish download failed
                                    that.remove_ui();
                                    that.full_download_dfd.reject(error);
                                });
                        })
                        .fail(function(error) {
                            //soemthing failed while iterating entities and their download
                            that.remove_ui();
                            that.full_download_dfd.reject(error);
                        })
                })
                .fail(function(error) {
                    //something failed in intialization
                    that.remove_ui();
                    that.full_download_dfd.reject(error);
                });

            return this.full_download_dfd;
        },

        //executed at the end of full download
        call_after_download: function() {
            //if user has defined afterFullDownload in configs, then execute it
            //must return a promise
            if (all_configs.misc.afterFullDownload)
                return all_configs.misc.afterFullDownload(this.start_time, this.download_status) 
            else
                return new $.Deferred().resolve();
        },

        // Starts download for all tables defined in config object. Rejects when any of them fails, Resolves when all are 
//         successfully downloaded
        iterate_object_stores: function() {
            var dfd = new $.Deferred();
            this.$('#stop_full_download').prop("disabled", false);
            //stores the dfds for each entity's download process
            var entity_dfds = [];
            
            //iterate over the entities
            for (var member in all_configs) {
                if (member == "misc")
                    continue;
                //initialize the current download-status for entity    
                this.download_status[member] = {
                    total: null,
                    downloaded: 0
                };
                //start full download for entity
                var entity_dfd = this.start_full_download_for_entity(all_configs[member]["entity_name"]);
                entity_dfds.push(entity_dfd);
            }
            
            //resolve when all entities have been downloaded, reject if any fails
            $.when.apply($, entity_dfds)
                .done(function() {
                    dfd.resolve();
                })
                .fail(function(error) {
                    dfd.reject(error);
                });
            return dfd;
        },

        //updates the progress bar
        update_pb_ui: function() {
            //can't fill progress bar untill total num of objects is known
            var ready_to_show = true;
            var total = 0;
            var downloaded = 0;
            //calculate the current status of download by looking at status of each entity
            _.each(this.download_status, function(status, entity) {
                //if total objects for any entity are not yet known, then can't show the progress
                if (status.total == null) {
                    ready_to_show = false;
                    return;
                } else {
                    //calculate the total num of objects bieng downloaded
                    total += status.total;
                    //calculate the total num of objects that have been downloaded
                    downloaded += status.downloaded;
                }
            });

            if (!ready_to_show)
                return;
            //set the progress bar with current progress    
            var percent_complete = (downloaded / total) * 100 + "%";
            $('#pbar').css("width", percent_complete);
        },
        
        //updates download-status display for an entity - entity_name | status(In Progress/Done) | #downloaded/#total
        update_status_ui: function(entity_name) {
            //get the # of downloaded objects for thi entity
            var downloaded = this.download_status[entity_name].downloaded;
            //get the # of total objects for thi entity
            var total = this.download_status[entity_name].total;
            //set the text
            var s_text = "In Progress";
            if (downloaded >= total)
                s_text = "Done";
            //set the num
            var s_num = String(downloaded) + "/" + String(total);
            
            //update the view
            this.$('#' + entity_name).find('.status_text').html(s_text);
            this.$('#' + entity_name).find('.status_numbers').html(s_num);
        },

        //starts download for an entity 
        start_full_download_for_entity: function(entity_name) {
            var dfd = new $.Deferred();
            var that = this;
            //get the num of objects to be downloaded for this entity 
            that.get_num_of_objects_to_download(entity_name)
                .done(function(total_num_objects) {
                    //do the chunked download
                    that.chunk_it_fetch_it_save_it(entity_name, total_num_objects)
                        .done(function() {
                            //entity successfully downloaded
                            console.log("FINISHED DOWNLOADING - " + entity_name);
                            return dfd.resolve();
                        })
                        .fail(function(error) {
                            //error while downloading entity
                            return dfd.reject(error);
                        });
                })
                .fail(function() {
                    //error while retrieving total # of objects
                    console.log("DASHBOARD:DOWNLOAD:UnexpectedError: Error fetching num of objects to download for - " + entity_name);
                    return dfd.reject("Failed to fetch num of objects for - " + entity_name);
                });
            return dfd;
        },

        //does a small GET request to retrieve total # of objects to be downloaded for an entity
        get_num_of_objects_to_download: function(entity_name) {
            var dfd = new $.Deferred();
            console.log("DASHBOARD:DOWNLOAD: Fetching num of objects to download for - " + entity_name);
            //send GET request to download 1 object of entity type - the api must return the total # of objects info too
            var xhr = $.get(all_configs[entity_name].rest_api_url, {
                limit: 1,
                offset: 0
            }, function(data) {
                //return the total_count param
                if (data && data.meta)
                    return dfd.resolve(data.meta.total_count);
                else
                    return dfd.reject();
            });
            this.network_requests.push(xhr);
            return dfd;
        },
        
        //update the downlaod status of an entity - key= total/downloaded
        update_download_status: function(entity_name, key, increment) {
            var s_obj = this.download_status[entity_name];
            if (!s_obj[key])
                s_obj[key] = increment;
            else
                s_obj[key] += increment;
            
            //update the view     
            this.update_status_ui(entity_name);
            this.update_pb_ui();

        },

        chunk_it_fetch_it_save_it: function(entity_name, total_num_objects) {
            var dfd = new $.Deferred();
            this.update_download_status(entity_name, "total", total_num_objects);
            //default chunk size
            var limit = 1500; 
            //get entity specific config if defined by user
            if (all_configs[entity_name].download_chunk_size) 
                limit = all_configs[entity_name].download_chunk_size;
            // else get global option if defined by user   
            else if (all_configs.misc.download_chunk_size) 
                limit = all_configs.misc.download_chunk_size;
            
            //calc num of chunks    
            var num_chunks = Math.ceil(total_num_objects / limit);
            console.log("Num of chunks for - " + entity_name + " = " + num_chunks);
            var offset = 0;
            var chunk_dfds = [];
            var that = this;
            //process each chunk
            for (var i = 0; i < num_chunks; i++) {
                var chunk_dfd = this.process_chunk(entity_name, offset, limit);
                chunk_dfd.done(function(num_objects_saved) {
                    //update download-status of this entity with the num of objects that were downloaded in this chunk
                    that.update_download_status(entity_name, "downloaded", num_objects_saved);
                });
                chunk_dfds.push(chunk_dfd);
                offset += limit;
            }

            // resolve when all chunks of this entity are processed...
            $.when.apply($, chunk_dfds)
                .done(function() {
                    return dfd.resolve();
                })
                .fail(function(error) {
                    return dfd.reject(error);
                });
            return dfd;
        },

        process_chunk: function(entity_name, offset, limit) {
            var dfd = new $.Deferred();
            var that = this;
            //check whether chunks is already downloaded
            var num_downloaded = this.is_already_downloaded(entity_name, offset, limit);
            //return if chunk already downloaded
            if (num_downloaded != -1)
                dfd.resolve(num_downloaded);
            else {
                //fetach and save the chunk
                this.fetch_save(entity_name, offset, limit)
                    .done(function(num_downloaded) {
                        //record the chunk as downloaded when successfully downloaded
                        that.save_as_downloaded(entity_name, offset, limit, num_downloaded);
                        //return the num of objects that were downloaded in this chunk
                        dfd.resolve(num_downloaded);
                    })
                    .fail(function(error) {
                        //chunk download failed
                        dfd.reject(error);
                    });
            }

            return dfd;
        },

        //checks if (entity_name, offset, limit) chunk exists in full_download_info
        is_already_downloaded: function(entity_name, offset, limit) {
            var exists = this.full_download_info_coll.where({
                entity_name: entity_name,
                offset: offset,
                limit: limit
            });
            // return num of objects that were downloaded if it exists, -1 otherwise
            if (exists.length) {
                console.log("CHUNK ALREADY EXISTS DOWNLOADED");
                return exists[0].get("num_objects_downloaded");
            }
            return -1
        },

        // creates (entity_name, offset, limit, num_downloaded) object in full_download_info 
        save_as_downloaded: function(entity_name, offset, limit, num_downloaded) {
            this.full_download_info_coll.create({
                entity_name: entity_name,
                offset: offset,
                limit: limit,
                num_objects_downloaded: num_downloaded
            }, {
                success: function(model) {
                    console.log("CHUNK SAVED AS DOWNLOADED-" + JSON.stringify(model));
                }
            });
        },
        
        //fetch and save the chunk
        fetch_save: function(entity_name, offset, limit) {
            var dfd = new $.Deferred();
            var that = this;
            //fetches the chunk from server 
            this.fetch_collection(entity_name, offset, limit)
                .done(function(collection) {
                    //saves the fetched chunk 
                    that.save_collection(entity_name, collection)
                        .done(function() {
                            //successfully fetched and saved
                            //return the number of objects downloaded in this chunk
                            return dfd.resolve(collection.length);
                        })
                        .fail(function(error) {
                            //error while saving chunk
                            return dfd.reject("DOWNLOAD: Failed to save an object of " + entity_name + " - " + error);
                        });
                })
                .fail(function() {
                    //error while fetching chunk
                    console.log("DASHBOARD:DOWNLOAD: error fetching collection from server");
                    return dfd.reject("DOWNLOAD: Failed to fetch collection for " + entity_name);
                });
            return dfd;
        },
        
        //shd be removed and online_utils shd be used instead
        //fetches the chunk from server and returns as a backbone collection
        fetch_collection: function(entity_name, offset, limit) {
            var dfd = new $.Deferred();
            var generic_collection_online = Backbone.Collection.extend({
                url: all_configs[entity_name].rest_api_url,
                sync: Backbone.ajaxSync,
                parse: function(data) {
                    return data.objects;
                }
            });
            var collection_online = new generic_collection_online();
            var xhr = collection_online.fetch({
                data: {
                    limit: limit,
                    offset: offset
                },
                success: function(collection) {
                    return dfd.resolve(collection);
                },
                error: function() {
                    return dfd.reject();
                }
            });
            this.network_requests.push(xhr);
            return dfd;
        },

        save_collection: function(entity_name, collection) {
            var dfd = new $.Deferred();
            var objects = collection.toJSON();
            var dfds = [];
            for (var i = 0; i < objects.length; i++) {
                objects[i]['id'] = parseInt(objects[i]['id']);
                //in each object, inject 'online_id' 
                objects[i]['online_id'] = parseInt(objects[i]['id']);
                //save the object
                var s_dfd = this.save_object(entity_name, objects[i]);
                dfds.push(s_dfd);
            }
            //resolve when all objects are successfully saved, reject if any save fails
            $.when.apply($, dfds)
                .done(function() {
                    return dfd.resolve();
                })
                .fail(function(error) {
                    console.log(error);
                    return dfd.reject();
                });
            return dfd;
        },

        // custom save to allow constraint error fails - can't use the offline_utils save
        save_object: function(entity_name, json) {
            var dfd = new $.Deferred();
            var model = Offline.create_b_model(entity_name);
            model.save(json, {
                success: function() {
                    return dfd.resolve();
                },
                error: function(model, error) {
                    //pass the save as successful if it is a constraint/unique_together error
                    if (error.srcElement.error.name == "ConstraintError") {
                        return dfd.resolve();
                    }
                    return dfd.reject();
                }
            });
            return dfd;
        },

        finish_download: function() {
            var dfd = new $.Deferred();
            console.log("DASHBOARD:DOWNLOAD: In finish download");
            var that = this;
            that.db_downloaded();

            //save the start time of download in meta_data table - used later as an indicator that database has been fully downloaded and also as a timestamp for first inc download
            Offline.fetch_object("meta_data", "key", "last_full_download")
                .done(function(model) {
                    that.set_timestamp(model, that.start_time)
                        .done(function() {
                            dfd.resolve();
                        })
                        .fail(function(error) {
                            dfd.reject(error);
                        });
                })
                .fail(function(model, error) {
                    that.set_timestamp(model, that.start_time)
                        .done(function() {
                            dfd.resolve();
                        })
                        .fail(function(error) {
                            dfd.reject(error);
                        });
                });

            return dfd;
        },
        
        //enable links in dashboard
        db_downloaded: function() {
            $('.list_items').unbind('click', false);
            $('.list_items').removeClass("disabled");
            console.log("Dashboard links enabled");
            $("#helptext").hide();
        }




    });

    return FullDownloadView;
});

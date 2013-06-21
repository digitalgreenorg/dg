/* Performs the full database download. For each table listed in configs, creates chunked requests to fetch data 
from server and saves it in offline db. To make it resumable, it does not clear the database before starting downloading. 
For each chunk request created, it checks if that chunk request was already downloaded by looking into the meta data store 
in offline DB. 
Since it continues from the present state of database found - In order to do a fresh download, there needs to be some 
external code which flushes the database before calling this module.
*/
define([
  'jquery',
  'underscore',
  'layoutmanager',
  'indexeddb_backbone_config',
  'configs',
  'offline_utils',
  'bootstrapjs'                            
], function(jquery,underscore,layoutmanager,indexeddb, all_configs, Offline){
    
    
    //clears objectstores - meta_data, uploadqueue, all config-defined objectstores
    //refills all config-defined objectstores
    //fills the last_downlaoded timestamp in meta_data
    var FullDownloadView = Backbone.Layout.extend({
        template: "#download_template",
        
        internet_connected : function(){
            return navigator.onLine;
        },
        
        initialize: function(){
            _(this).bindAll('stop_download');
        },
        
        serialize: function(){
            return {
                all_configs: all_configs
            }
        },
        
        events:{
            'click #stop_full_download': 'stop_download'
        },
        
        afterRender: function(){
        },
        
        stop_download: function(){
            console.log("stopping download");
            this.remove_ui();
            this.full_download_dfd.reject("User stopped download");
            $.each(this.network_requests, function(index, xhr){
                xhr.abort();
            });
        },

        /* 
        TODO Checks if their is already a full downloaded database, alert user thar this db should be removed before proceeding 
        Initializes UI and objects used for progress bar. 
        Fetches the full_download_info objectStore collection to resume download, if that's the case
        TODO Stores the start time for download
        */    
        initialize_download: function(){
            var dfd = new $.Deferred();
            
            if(!this.internet_connected())
            {
                dfd.reject("Can't download database. Internet is not connected");
                return dfd;
            }
            //intialize UI objects
            this.$('#full_download_modal').modal({
                keyboard: false,
                backdrop: "static",
            });
            this.$('#full_download_modal').modal('show');
            var num_of_entities = Object.keys(all_configs).length; 
            this.progress_bar_step = 100 / num_of_entities;
            this.fetch_status = {};
            /////////////////////////////////////////
            
            //every request made to server will be stored in this, - to abort if user chooses to stop download
            this.network_requests = [];
            /////////////////////////////////////////
            
            // fetching the full_download_info collection to be used for resuming download
            var that = this;
            Offline.fetch_collection("full_download_info")
                .done(function(coll){
                    that.full_download_info_coll = coll;
                    dfd.resolve();
                })
                .fail(function(error){
                    dfd.reject(error);
                });
            //////////////////////////////////////////    
            return dfd;
        },
        
        remove_ui: function(){
            this.$('#full_download_modal').modal('hide'); // calling remove without hiding modal causes modal's backdrop to remain
            this.remove();
            
        },
        
        start_full_download: function(){
            this.full_download_dfd = new $.Deferred();
            var that = this;
            this.initialize_download()
                .done(function(){
                    that.iterate_object_stores()
                        .done(function(){
                            that.finish_download()
                                .done(function(){
                                    that.remove_ui();
                                    that.full_download_dfd.resolve();
                                })
                                .fail(function(error){
                                    that.remove_ui();
                                    that.full_download_dfd.reject(error);
                                });
                        })
                        .fail(function(error){
                            that.remove_ui();
                            that.full_download_dfd.reject(error);
                        })
                })
                .fail(function(error){
                    that.remove_ui();
                    that.full_download_dfd.reject(error);
                });
                
            return this.full_download_dfd;    
        },
        
        /* Starts download for all tables defined in config object. Rejects when any of them fails, Resolves when all are 
        successfully downloaded*/
        iterate_object_stores: function(){
            var dfd = new $.Deferred();
            this.$('#stop_full_download').prop("disabled", false);
            var entity_dfds = [];
            for (var member in all_configs) {
                if(member == "misc")
                    continue;
                var entity_dfd = this.start_full_download_for_entity(all_configs[member]["entity_name"]);
                entity_dfds.push(entity_dfd);
                this.fetch_status[member] = {};
            }
            
            $.when.apply($, entity_dfds)
                .done(function(){
                    dfd.resolve();
                })
                .fail(function(error){
                    dfd.reject(error);
                });
            return dfd;    
        },
        
        increment_pb: function() {
            w = parseFloat(document.getElementById('pbar').style.width);
            document.getElementById('pbar').style.width= (w + this.progress_bar_step) +'%';
        },
        
        update_status: function(entity_name, status){
            $('#'+entity_name).find('.status').html(status);
        },
        
        clear_object_store: function(entity_name){
            var dfd = new $.Deferred();
            console.log("clearing object store - "+entity_name);
            var request = indexedDB.open("offline-database");
            request.onerror = function(event) {
                console.log("DASHBOARD:DOWNLOAD: Why didn't you allow my web app to use IndexedDB?!");
                return dfd.reject();
            };
            request.onsuccess = function(event) {
                var db = request.result;
                var clearTransaction = db.transaction([entity_name], "readwrite");
                var clearRequest = clearTransaction.objectStore(entity_name)
                    .clear();
                clearRequest.onsuccess = function(event) {
                    console.log("DASHBOARD:DOWNLOAD: " + entity_name + ' objectstore cleared');
                    return dfd.resolve();
                };
                clearRequest.onerror = function(event) {
                    console.log("DASHBOARD:DOWNLOAD: Error while clearing objectstore - " + entity_name);
                    return dfd.reject();
                };
            }    
            return dfd;
        },
        
        start_full_download_for_entity: function(entity_name){
            var dfd = new $.Deferred();
            var that = this;
            that.get_num_of_objects_to_download(entity_name)
                .done(function(total_num_objects){
                    console.log("DASHBOARD:DOWNLOAD: Total num of objects for - "+entity_name+" - = "+total_num_objects);
                    that.fetch_status[entity_name]["total"] = total_num_objects;
                    that.fetch_status[entity_name]["downloaded"] = 0;
                    that.update_status(entity_name, "In progress <span style='float:right'>"+"0/"+total_num_objects+"</span>");
                    that.chunk_it_fetch_it_save_it(entity_name, total_num_objects)
                        .done(function(){
                            console.log("FINISHED DOWNLOADING - " + entity_name);
                            that.increment_pb();
                            that.update_status(entity_name, "Done <span style='float:right'>"+that.fetch_status[entity_name]["downloaded"]+"/"+total_num_objects+"</span>");
                            return dfd.resolve();
                        })
                        .fail(function(error){
                            return dfd.reject(error);
                        });
                })
                .fail(function(){
                    console.log("DASHBOARD:DOWNLOAD:UnexpectedError: Error fetching num of objects to download for - " + entity_name);
                    alert("DASHBOARD:DOWNLOAD:UnexpectedError: Error fetching num of objects to download for - " + entity_name);
                    return dfd.reject("Failed to fetch num of objects for - "+entity_name);
                });
            return dfd;
        },
        
        get_num_of_objects_to_download: function(entity_name){
            var dfd = new $.Deferred();
            console.log("DASHBOARD:DOWNLOAD: Fetching num of objects to download for - "+entity_name);
            var xhr = $.get(all_configs[entity_name].rest_api_url, {limit:1,offset:0}, function(data){
                if(data){
                    if(data.meta){
                        return dfd.resolve(data.meta.total_count);
                    }
                    else
                        return dfd.reject();
                }
                else
                    return dfd.reject();
            });
            this.network_requests.push(xhr);
            return dfd;
        },
        
        chunk_it_fetch_it_save_it: function(entity_name, total_num_objects){
            var dfd = new $.Deferred();
            var limit = 1500;
            if(all_configs[entity_name].download_chunk_size)
            {
                limit = all_configs[entity_name].download_chunk_size;
            }
            else if(all_configs.misc.download_chunk_size)
            {
                limit = all_configs.misc.download_chunk_size;
            }
            var num_chunks = Math.ceil(total_num_objects/ limit); 
            console.log("Num of chunks for - "+entity_name+" = "+num_chunks);
            var offset = 0;
            var chunk_dfds = [];
            var that = this;
            for(var i=0; i<num_chunks; i++)
            {
                var chunk_dfd = this.process_chunk(entity_name, offset, limit);
                chunk_dfd.done(function(num_objects_saved){
                    that.fetch_status[entity_name]["downloaded"] += num_objects_saved;
                    that.update_status(entity_name, "In progress <span style='float:right'>"+ that.fetch_status[entity_name]["downloaded"] +"/"+that.fetch_status[entity_name]["total"]+"</span>");
                });
                chunk_dfds.push(chunk_dfd);
                offset +=limit;
            }
            $.when.apply($,chunk_dfds)
                .done(function(){
                    return dfd.resolve();
                })
                .fail(function(error){
                    return dfd.reject(error);
                });
            return dfd;
        },
        
        process_chunk: function(entity_name, offset, limit){
            var dfd = new $.Deferred();
            var that = this;
            //TODO check if this chunk is already downloaded, if not call fetch_save
            var num_downloaded = this.is_already_downloaded(entity_name, offset, limit);
            if(num_downloaded!=-1)
                dfd.resolve(num_downloaded);
            else
            {
                this.fetch_save(entity_name, offset, limit)
                    .done(function(num_downloaded){
                        that.save_as_downloaded(entity_name, offset, limit, num_downloaded);
                        dfd.resolve(num_downloaded);
                    })
                    .fail(function(error){
                        dfd.reject(error);
                    });
            }
            
            return dfd;    
        },
        
        /*checks if (entity_name, offset, limit) exists in full_download_info
        return num of objects that were downloaded if it exists, -1 otherwise*/
        is_already_downloaded: function(entity_name, offset, limit){
            var exists = this.full_download_info_coll.where({entity_name:entity_name, offset:offset, limit: limit});
            if(exists.length)
            {
                console.log("CHUNK ALREADY EXISTS DOWNLOADED");
                return exists[0].get("num_objects_downloaded");
            }
            return -1    
        },
        
        /*creates (entity_name, offset, limit, num_downloaded) object in full_download_info - which means 
        this chunk won't be downloaded again in case download interrupts and is resumed again*/
        save_as_downloaded: function(entity_name, offset, limit, num_downloaded){
            this.full_download_info_coll.create({entity_name:entity_name, offset:offset, limit: limit, num_objects_downloaded: num_downloaded},{
                success:function(model){
                    console.log("CHUNK SAVED AS DOWNLOADED-"+JSON.stringify(model));
                }
            });
        },
        
        fetch_save: function(entity_name, offset, limit){
            var dfd = new $.Deferred();
            var that = this;
            this.fetch_collection(entity_name, offset, limit)
                .done(function(collection){
                    that.save_collection(entity_name, collection)
                        .done(function(){
                            return dfd.resolve(collection.length);    
                        })
                        .fail(function(error){
                            return dfd.reject("DOWNLOAD: Failed to save an object of "+entity_name+" - "+error);
                        });
                })
                .fail(function(){
                    console.log("DASHBOARD:DOWNLOAD: error fetching collection from server");
                    return dfd.reject("DOWNLOAD: Failed to fetch collection for "+entity_name);
                });
            return dfd;    
        },
        
        fetch_collection: function(entity_name, offset, limit){
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
                success: function(collection){
                    return dfd.resolve(collection);
                },
                error: function(){
                    return dfd.reject();
                }
            });
            this.network_requests.push(xhr);
            return dfd;
        },
        
        save_collection: function(entity_name, collection){
            var dfd = new $.Deferred();
            objects = collection.toJSON();
            var dfds = [];
            for (var i = 0; i < objects.length; i++) {
                objects[i]['id'] = parseInt(objects[i]['id']);
                objects[i]['online_id'] = parseInt(objects[i]['id']);
                var s_dfd = this.save_object(entity_name, objects[i]);
                dfds.push(s_dfd);
            }
            $.when.apply($,dfds)
                .done(function(){
                    return dfd.resolve();
                })
                .fail(function(error){
                    console.log(error);
                    return dfd.reject();
                })
            return dfd;    
        },
        
        /* custom save to allow constraint error fails */
        save_object: function(entity_name, json){
            var dfd = new $.Deferred();
            var model =  Offline.create_b_model(entity_name);
            model.save(json,{
                success: function(){
                    return dfd.resolve();
                },
                error: function(model,error){
                    if(error.srcElement.error.name=="ConstraintError")
                    {
                        return dfd.resolve();
                    }
                    return dfd.reject();
                }
            });
            return dfd;
        },
                        
        finish_download: function(){
            var dfd = new $.Deferred();
            console.log("DASHBOARD:DOWNLOAD: In finish downlaod");
            var generic_model_offline = Backbone.Model.extend({
                database: indexeddb,
                storeName: "meta_data",
            });
            var meta_model = new generic_model_offline();
            meta_model.set({key: "last_full_download"});
            meta_model.fetch({
                success: function(model){
                    console.log("DASHBOARD:DOWNLOAD: last_full_download fetched from meta_data objectStore:");
                    console.log(JSON.stringify(model.toJSON()));
                    model.set('timestamp',new Date());
                    model.save(null,{
                        success: function(){
                            console.log("DASHBOARD:DOWNLOAD: last_full_download updated in meta_data objectStore:");    
                            console.log(JSON.stringify(model.toJSON()));
                            dfd.resolve();
                        },
                        error: function(model,error){
                            console.log("DASHBOARD:DOWNLOAD: error updating last_full_download in meta_data objectStore");    
                            dfd.reject("error updating last_full_download in meta_data objectStore");
                        }
                    });
                },
                error: function(model, error){
                    console.log("DASHBOARD:DOWNLOAD: error while fetching last_full_download from meta_data objectStore");
                    if(error == "Not Found")
                        {
                            meta_model.set('timestamp',new Date());
                            meta_model.save(null,{
                                success: function(model){
                                    console.log("DASHBOARD:DOWNLOAD: last_full_download created in meta_data objectStore:");    
                                    console.log(JSON.stringify(model.toJSON()));
                                    dfd.resolve();
                                },
                                error: function(model,error){
                                    console.log("DASHBOARD:DOWNLOAD: error creating last_full_download in meta_data objectStore : ");
                                    console.log(error);    
                                    dfd.reject("error creating last_full_download in meta_data objectStore");
                                }
                            });
                            
                        }    
                }        
            });
            return dfd;
        }        
        
                
    
          
    });
    
  // Our module now returns our view
  return FullDownloadView;
});
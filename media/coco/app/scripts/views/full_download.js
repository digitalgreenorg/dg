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
            _.bindAll(this);
        },
        
        serialize: function(){
            return {
                all_configs: all_configs
            }
        },
        
        events:{
            'click #stop_full_download': 'stop_download'
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
        TODO Checks if there is already a full downloaded database, alert user that this db should be removed before proceeding 
        Checks internet connectivity
        Initializes UI and objects used to update status. 
        Fetches the full_download_info objectStore to resume download, if that's the case
        Stores the start time for download
        */    
        initialize_download: function(){
            var dfd = new $.Deferred();
            //Django complains when Z is present in timestamp bcoz timezone capab is off
            this.start_time = new Date().toJSON().replace("Z", "");
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
            this.download_status = {};
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
            // calling remove without hiding modal causes modal's backdrop to remain
            this.$('#full_download_modal').modal('hide'); 
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
                this.download_status[member] = {
                    total:null,
                    downloaded:0
                };
                var entity_dfd = this.start_full_download_for_entity(all_configs[member]["entity_name"]);
                entity_dfds.push(entity_dfd);
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
        
        update_pb_ui: function() {
            //can't show progress bar untill total num of objects is known
            var ready_to_show = true; 
            var total = 0;
            var downloaded = 0;
            _.each(this.download_status, function(status, entity){
                //if total objects for any entity are not yet known, then can't show the progress
                if(status.total==null)
                {
                    ready_to_show = false;
                    return;    
                }
                else
                {
                    total += status.total;
                    downloaded += status.downloaded;
                }
            });
            
            if(!ready_to_show)
                return;

            var percent_complete = (downloaded/total)*100 +"%";
            $('#pbar').css("width", percent_complete);
        },
        
        update_status_ui: function(entity_name){
            var downloaded = this.download_status[entity_name].downloaded;
            var total = this.download_status[entity_name].total;
            var s_text = "In Progress";
            if(downloaded>=total)
                s_text = "Done";
            var s_num = String(downloaded)+"/"+String(total);    
                
            this.$('#'+entity_name).find('.status_text').html(s_text);
            this.$('#'+entity_name).find('.status_numbers').html(s_num);
        },
        
        start_full_download_for_entity: function(entity_name){
            var dfd = new $.Deferred();
            var that = this;
            that.get_num_of_objects_to_download(entity_name)
                .done(function(total_num_objects){
                    that.chunk_it_fetch_it_save_it(entity_name, total_num_objects)
                        .done(function(){
                            console.log("FINISHED DOWNLOADING - " + entity_name);
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
                if(data && data.meta)
                    return dfd.resolve(data.meta.total_count);
                else
                    return dfd.reject();
            });
            this.network_requests.push(xhr);
            return dfd;
        },
        
        update_download_status: function(entity_name, key, increment){
            var s_obj = this.download_status[entity_name];
            if(!s_obj[key])
                s_obj[key] = increment;
            else
                s_obj[key] += increment;
                
            this.update_status_ui(entity_name);
            this.update_pb_ui();
                    
        },
        
        chunk_it_fetch_it_save_it: function(entity_name, total_num_objects){
            var dfd = new $.Deferred();
            this.update_download_status(entity_name, "total", total_num_objects);
            
            var limit = 1500; //default
            if(all_configs[entity_name].download_chunk_size)    //entity specific option
                limit = all_configs[entity_name].download_chunk_size;
            else if(all_configs.misc.download_chunk_size)    // global option
                limit = all_configs.misc.download_chunk_size;
            var num_chunks = Math.ceil(total_num_objects/ limit); 
            console.log("Num of chunks for - "+entity_name+" = "+num_chunks);
            var offset = 0;
            var chunk_dfds = [];
            var that = this;
            for(var i=0; i<num_chunks; i++)
            {
                var chunk_dfd = this.process_chunk(entity_name, offset, limit);
                chunk_dfd.done(function(num_objects_saved){
                    that.update_download_status(entity_name, "downloaded", num_objects_saved);
                });
                chunk_dfds.push(chunk_dfd);
                offset += limit;
            }
            
            // when all chunks of this entity are downloaded...
            $.when.apply($, chunk_dfds)
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
            var objects = collection.toJSON();
            var dfds = [];
            for (var i = 0; i < objects.length; i++) {
                objects[i]['id'] = parseInt(objects[i]['id']);
                objects[i]['online_id'] = parseInt(objects[i]['id']);
                var s_dfd = this.save_object(entity_name, objects[i]);
                dfds.push(s_dfd);
            }
            $.when.apply($, dfds)
                .done(function(){
                    return dfd.resolve();
                })
                .fail(function(error){
                    console.log(error);
                    return dfd.reject();
                });
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
            console.log("DASHBOARD:DOWNLOAD: In finish download");
            var that = this;
            //that.db_downloaded();
			
            Offline.fetch_object("meta_data", "key", "last_full_download")
                .done(function(model){
                    set_timestamp(model);
                })
                .fail(function(model, error){
                    set_timestamp(model);
                });
            
            function set_timestamp(model){
                model.set('timestamp',that.start_time);
                model.save(null,{
                    success: function(){
                        dfd.resolve();
                    },
                    error: function(model,error){
                        dfd.reject("error updating last_full_download in meta_data objectStore");
                    }
                });
            };
            
            return dfd;
        },

		db_downloaded: function(){
			$('.list_items').unbind('click', false);
			$('.list_items').removeClass("disabled");
			console.log("Dashboard links enabled");
			$("#helptext").hide();
		}
        
                
    
          
    });
    
  return FullDownloadView;
});
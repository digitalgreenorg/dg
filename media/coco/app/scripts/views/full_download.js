define([
  'jquery',
  'underscore',
  'backbone',
  'indexeddb_backbone_config',
  'configs'
  // Using the Require.js text! plugin, we are loaded raw text
  // which will be used as our views primary template
  // 'text!templates/project/list.html'
], function($,_,pass,indexeddb, all_configs){
    
    var FullDownloadView = Backbone.Layout.extend({
        template: "#download_template",

        initialize: function(){
        },
        
        serialize: function(){
            return {
                all_configs: all_configs
            }
        },

        afterRender: function(){
            this.$('#full_download_modal').modal('show');
            this.Download();
        },
        
        increment_pb: function() {
            w = parseInt(document.getElementById('pbar').style.width);
            document.getElementById('pbar').style.width= (w + this.progress_bar_step) +'%';
        },
        
        update_status: function(entity_name, status){
            $('#'+entity_name).find('.status').html(status);
        },
            
        Download: function() {
            console.log("DASHBOARD:DOWNLOAD: starting download");
            //Download:fetch each model from server and save it to the indexeddb
            var that = this;
            this.num_of_entities = Object.keys(all_configs).length; // Number of foreign entities referenced in this model.
            this.progress_bar_step = 100 / this.num_of_entities;
            this.fetch_status = {};
            var entity_dfds = [];
            for (var member in all_configs) {
                if(member == "misc")
                    continue;
                var entity_dfd = this.start_full_download(all_configs[member]["entity_name"]);
                entity_dfds.push(entity_dfd);
                this.fetch_status[member] = {};
            }
            $.when.apply($, entity_dfds)
                .done(function(){
                    console.log("Finished full download.");
                    that.finish_download();
                })
                .fail(function(){
                    console.log("Error while downloading.");
                });
        },
        
        start_full_download: function(entity_name){
            var dfd = new $.Deferred();
            var that = this;
            this.clear_object_store(entity_name)
                .done(function(){
                    console.log("DASHBOARD:DOWNLOAD: objectstore cleared - " + entity_name);
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
                                .fail(function(){
                                    return dfd.reject();
                                });
                        })
                        .fail(function(){
                            console.log("DASHBOARD:DOWNLOAD:UnexpectedError: Error fetching num of objects to download for - " + entity_name);
                            alert("DASHBOARD:DOWNLOAD:UnexpectedError: Error fetching num of objects to download for - " + entity_name);
                            return dfd.reject();
                        });
                })
                .fail(function(){
                    console.log("DASHBOARD:DOWNLOAD:UnexpectedError: Error while clearing objectstore - " + entity_name);
                    alert("DASHBOARD:DOWNLOAD:UnexpectedError: Error while clearing objectstore - " + entity_name);
                    return dfd.reject();
                });
            return dfd;
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
        
        get_num_of_objects_to_download: function(entity_name){
            var dfd = new $.Deferred();
            console.log("DASHBOARD:DOWNLOAD: Fetching num of objects to download for - "+entity_name);
            $.get(all_configs[entity_name].rest_api_url, {limit:1,offset:0}, function(data){
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
            return dfd;
        },
        
        chunk_it_fetch_it_save_it: function(entity_name, total_num_objects){
            var dfd = new $.Deferred();
            var num_chunks = Math.ceil(total_num_objects/ all_configs.misc.download_size); 
            console.log("Num of chunks for - "+entity_name+" = "+num_chunks);
            var limit = all_configs.misc.download_size;
            var offset = 0;
            var chunk_dfds = [];
            var that = this;
            for(var i=0; i<num_chunks; i++)
            {
                var chunk_dfd = this.fetch_save(entity_name, offset, limit);
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
                .fail(function(){
                    return dfd.reject();
                });
            return dfd;
        },
        
        fetch_save: function(entity_name, offset, limit){
            var dfd = new $.Deferred();
            var that = this;
            this.fetch_collection(entity_name, offset, limit)
                .done(function(collection){
                    that.save_collection(entity_name, collection);
                    return dfd.resolve(collection.length);    
                })
                .fail(function(){
                    console.log("DASHBOARD:DOWNLOAD: error fetching collection from server");
                    return dfd.reject();
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
            collection_online.fetch({
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
            return dfd;
        },
        
        save_collection: function(entity_name, collection){
            //Not treating as async bcoz individual async calls of create are too many to monitor and they return almost instantly
            var generic_model_offline = Backbone.Model.extend({
                database: indexeddb,
                storeName: entity_name,
            });
            var generic_collection_offline = Backbone.Collection.extend({
                model: generic_model_offline,
                database: indexeddb,
                storeName: entity_name,
            });
            var collection_offline = new generic_collection_offline();
            objects = collection.toJSON();
            for (var i = 0; i < objects.length; i++) {
                objects[i]['id'] = parseInt(objects[i]['id']);
                objects[i]['online_id'] = objects[i]['id'];
                collection_offline.create(objects[i],{
                    success: function(){
                        // console.log("created");
                    }
                });
            }
        },
                
        finish_download: function(){
            console.log("DASHBOARD:DOWNLOAD: In finish downlaod");
            var generic_model_offline = Backbone.Model.extend({
                database: indexeddb,
                storeName: "meta_data",
            });
            var meta_model = new generic_model_offline();
            meta_model.set({key: "last_downloaded"});
            meta_model.fetch({
                success: function(model){
                    console.log("DASHBOARD:DOWNLOAD: ast_downloaded fetched from meta_data objectStore:");
                    console.log(JSON.stringify(model.toJSON()));
                    model.set('timestamp',new Date());
                    model.save(null,{
                        success: function(){
                            console.log("DASHBOARD:DOWNLOAD: last_downloaded updated in meta_data objectStore:");    
                            console.log(JSON.stringify(model.toJSON()));
                            
                        },
                        error: function(one,two,three){
                            console.log("DASHBOARD:DOWNLOAD: error updating last_downloaded in meta_data objectStore");    
                            console.log(one);
                            console.log(two);
                            console.log(three);
                        }
                    });
                },
                error: function(error){
                    console.log("DASHBOARD:DOWNLOAD: error while fetching last_downloaded from meta_data objectStore");
                    if(error == "Not Found")
                        {
                            meta_model.set('timestamp',new Date());
                            meta_model.save(null,{
                                success: function(model){
                                    console.log("DASHBOARD:DOWNLOAD: last_downloaded created in meta_data objectStore:");    
                                    console.log(JSON.stringify(model.toJSON()));
                                    this.$('#full_download_modal').modal('hide');
                            
                                },
                                error: function(error){
                                    console.log("DASHBOARD:DOWNLOAD: error creating last_downloaded in meta_data objectStore : ");
                                    console.log(error);    
                                }
                            });
                            
                        }    
                }        
            });
        }        
        
                
    
          
    });
    
  // Our module now returns our view
  return FullDownloadView;
});
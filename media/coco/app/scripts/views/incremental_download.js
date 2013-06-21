define([
  'jquery',
  'underscore',
  'layoutmanager',
  'indexeddb_backbone_config',
  'configs',
  'online_to_offline',
  'indexeddb-backbone',
  'bootstrapjs'                            
], function(jquery,underscore,layoutmanager,indexeddb, all_configs, OnlineToOffline){
    
    var IncrementalDownloadView = Backbone.Layout.extend({
        
        template: "#incremental_download_template",
        events:{
            "click #stop_inc_download": "stop_inc_download"
        },
        increment_pb: function() {
            w = parseFloat(document.getElementById('inc_pbar').style.width);
            document.getElementById('inc_pbar').style.width= (w + this.progress_bar_step) +'%';
        },
        
        update_status: function(status){
            console.log(status);
            $('#inc_status').html(status);
        },
        
        update_action: function(action){
            $('#inc_action').html(action);
        },
        
        initialize: function(){
            console.log("UPLOAD: initializing new incremental_download view");
            _(this)
                .bindAll('iterate_incd_objects');
            _(this)
                .bindAll('pick_next');
            _(this)
                .bindAll('stop_inc_download');
            this.start_timestamp = null;
            this.in_progress = false;
        },  
        
        stop_inc_download: function(){
            console.log("stopping inc download");
            this.user_interrupt = true;
        },
        
        //initializes the global vars used, ui
        initialize_inc_download: function(options){
            this.in_progress = true;
            this.user_interrupt = false;
            var that = this;
            if(!(options.background))
            {
                this.template = incremental_download_template;
                this.render()
                    .done(function(){
                        that.$('#incremental_download_modal').modal({
                            keyboard: false,
                            backdrop: "static",
                        });
                        that.$('#incremental_download_modal').modal('show');                    
                    });
            }
            else
            {
                this.template = incremental_download_background_template;
                this.render();
            }
        },
        
        tear_down: function(){
            this.$('#incremental_download_modal').modal('hide');                    
            this.remove();
            this.in_progress = false;
        },
              
        start_incremental_download: function(options) {
            var dfd = new $.Deferred();
            var that = this;        
            this.initialize_inc_download(options);    
            console.log("INCREMENTAL DOWNLOAD: start the incremental_download");
            var that = this;
            this.getIncObjects()
                .done(function(objects){
                    that.iterate_incd_objects(objects)
                        .done(function(last_object_timestamp){
                            that.finish_download(last_object_timestamp)
                                .done(function(){
                                    that.tear_down();
                                    dfd.resolve();
                                })
                                .fail(function(error){
                                    that.tear_down();
                                    dfd.reject(error);
                                });
                        })
                        .fail(function(error){
                            //when user interrupts
                            if(error.last_object_timestamp)
                            {
                                that.finish_download(error.last_object_timestamp)
                                    .always(function(){
                                        that.tear_down();
                                        dfd.reject(error.err_msg);
                                    });
                            }
                            dfd.reject(error.err_msg)
                        });
                })
                .fail(function(error){
                    that.tear_down();
                    dfd.reject(error);
                });
            return dfd;    
        },

        getIncObjects: function(){
            var dfd = new $.Deferred();
            this.start_timestamp = new Date();
            this.get_last_download_timestamp()
                .done(function(timestamp){
                    console.log("Timestamp for inc download - "+timestamp);
                    $.get(all_configs.misc.inc_download_url,{
                        timestamp:timestamp
                    }, function(){},"json")
                        .fail(function(){ 
                            dfd.reject("Incremental download objects fetch failed!");
                        })
                        .done(function(objects){
                            dfd.resolve(objects);
                        });
                })
                .fail(function(error){
                    dfd.reject(error);
                });
            return dfd;    
        },    
            
        get_last_download_timestamp: function(){
            var dfd = new $.Deferred();
            var that = this;
            var generic_model_offline = Backbone.Model.extend({
                database: indexeddb,
                storeName: "meta_data",
            });
            this.meta_model = new generic_model_offline();
            this.meta_model.set({key: "last_inc_download"});
            this.meta_model.fetch({
                success: function(model){
                    var timestamp = model.get('timestamp');
                    dfd.resolve(timestamp);
                },
                error: function(model,error){
                    that.meta_model.clear();
                    that.meta_model.set({key: "last_full_download"});
                    that.meta_model.fetch({
                        success: function(model){
                            var timestamp = model.get('timestamp');
                            timestamp = timestamp.toJSON();
                            timestamp = timestamp.replace("T"," ");
                            timestamp = timestamp.replace("Z","");
                            dfd.resolve(timestamp);
                        },
                        error: function(model,error){
                            dfd.reject("Neither inc download has happened before nor full download.");
                        }        
                    });
                }        
            });
            return dfd;    
        },
            
        iterate_incd_objects: function(incd_objects){
            var dfd = new $.Deferred();
            this.incd_objects = incd_objects;
            if(!this.incd_objects.length || this.incd_objects==0)
                return dfd.resolve();
            this.progress_bar_step = 100/incd_objects.length;
            this.download_status = {};
            this.download_status["total"] = incd_objects.length;
            this.download_status["downloaded"] = 0;
            console.log("INCD objects received");
            console.log(incd_objects);
            this.pick_next(dfd);
            return dfd;
        },  
        
        pick_next: function(whole_download_dfd){
            var that = this;
            this.prev_incd_o = this.cur_incd_o;
            this.update_status(this.download_status["downloaded"]+"/"+this.download_status["total"]);
            this.cur_incd_o = this.incd_objects.shift();
            if(!this.cur_incd_o)
            {
                var update_timestamp;
                if(this.prev_incd_o)
                    update_timestamp = this.get_timestamp(this.prev_incd_o)
                else
                    update_timestamp = this.start_timestamp;    
                return whole_download_dfd.resolve(update_timestamp);
            }
            else if(this.user_interrupt)
            {
                var update_timestamp;
                if(this.prev_incd_o)
                    update_timestamp = this.get_timestamp(this.prev_incd_o)
                else
                    update_timestamp = null;
                return whole_download_dfd.reject({
                    err_msg:"User stopped Sync", 
                    last_object_timestamp: update_timestamp
                });
            }
            else
            {   
                this.process_incd_object(this.cur_incd_o)
                    .fail(function(error){
                        console.log("FAILED TO INC DOWNLOAD AN OBJECT: ");
                        console.log(error);
                    })
                    .done(function(){
                        console.log("SUCESSFULLY DOWNLOADED AN OBJECT");
                    })
                    .always(function(){
                        that.increment_pb();
                        that.download_status["downloaded"]++;
                        that.pick_next(whole_download_dfd);
                    });
            }
        },     
        
        // {"pk":9372,"model":"dashboard.serverlog","fields":{"action":1,"timestamp":"2013-04-15T06:47:35","entry_table":"Screening","model_id":10000000132086}}
        get_timestamp: function(obj){
            return obj.fields.timestamp;
        },
        
        get_entity_name: function(obj){
            for (var member in all_configs) {
                if (member == obj.fields.entry_table.toLowerCase())
                {
                    return all_configs[member].entity_name;
                }
                else if((all_configs[member].inc_table_name)&&(all_configs[member].inc_table_name == obj.fields.entry_table.toLowerCase()))
                {
                    return all_configs[member].entity_name;
                }
            }
            return -1;
        },
            
        get_action: function(obj){
            return obj.fields.action;
        },    
        
        get_online_id: function(obj){
            return parseInt(obj.fields.model_id);
        },
        
        get_foreign_field_desc: function(obj){
            var entity_name = this.get_entity_name(obj);    
            if(all_configs[entity_name].edit)
            {
                return all_configs[entity_name].edit.foreign_entities;
            }
            else
                return all_configs[entity_name].foreign_entities;
        },    
                
        process_incd_object: function(incd_o){
            var dfd = new $.Deferred();
            // console.log("INCD object received - "+JSON.stringify(incd_o));
            // $.get("/get_log/",{timestamp:"2012-03-10 12:06:04"},function(){console.log("suc it");return dfd.resolve();});
            var generic_model_offline = Backbone.Model.extend({
                database: indexeddb,
                storeName: this.get_entity_name(incd_o),
            });
            var that = this;    
            var generic_model_online = Backbone.Model.extend({
                sync: Backbone.ajaxSync,
                url: function() {
                    return this.id ? all_configs[that.get_entity_name(incd_o)].rest_api_url + this.id + "/" : all_configs[that.get_entity_name(incd_o)].rest_api_url;
                },
            });
                
            this.offline_model = new generic_model_offline();
            this.online_model = new generic_model_online();
            this.update_action("Downloading "+this.get_entity_name(incd_o));
            
            switch(this.get_action(incd_o))
                {
                    case 1: 
                    // console.log("its add");
                    this.incd_add(incd_o, dfd);
                    break;
                    case 0: 
                    // console.log("its edit");
                    this.incd_edit(incd_o, dfd);
                    break;
                    case -1: 
                    // console.log("its delete");
                    this.incd_delete(incd_o, dfd);
                    break;
                    default: 
                    console.log("ambiguous case");    
                    dfd.reject("ambiguous case. None of add, edit , delete!");
                }    
            return dfd.promise();    
        },
        
        incd_add: function(incd_o, dfd){
            // console.log("processing add - "+JSON.stringify(incd_o));
            var that = this;
            this.fetch_from_offline(this.get_online_id(incd_o))
                .fail(function(error){
                    if(error == "Not Found")
                    {
                        that.fetch_from_online(that.get_online_id(incd_o))
                            .done(function(on_model){
                                OnlineToOffline.convert(on_model.toJSON(), that.get_foreign_field_desc(incd_o))
                                    .done(function(on_off_obj){
                                        that.add_offline(on_off_obj.off_json)
                                            .done(function(off_model){
                                                // console.log("INCD:ADD: Successfully added model in offline db. Added model - "+JSON.stringify(off_model.toJSON()));
                                                dfd.resolve();
                                            })
                                            .fail(function(error){
                                                // console.log("INCD:ADD: Error saving model in offline db - "+error);
                                                // console.log(error);
                                                // alert("Unexpected error:INCD:ADD: Error saving new model in offline db - "+error);
                                                dfd.reject(error);
                                            });    
                                    })
                                    .fail(function(error){
                                        // console.log("INCD:ADD: Not saving object to offlinedb coz onlineTOoffline failed");
                                        dfd.reject(error);
                                    });    
                            })
                            .fail(function(response){
                                // console.log("INCD: Error fetching model from server - "+response.statusText);
                                dfd.reject(response);
                            });
                    }
                })
                .done(function(off_model){
                    // console.log("INCD: The model supposed to be added already exists. Moving on...");
                    dfd.reject("INCD: The model supposed to be added already exists. Moving on...");    
                });    
        },    
        
        incd_edit: function(incd_o, dfd){
            // console.log("processing edit - "+JSON.stringify(incd_o));
            var that = this;
            this.fetch_from_offline(this.get_online_id(incd_o))
                .done(function(off_model){
                    that.fetch_from_online(that.get_online_id(incd_o))
                        .done(function(on_model){
                            OnlineToOffline.convert(on_model.toJSON(), that.get_foreign_field_desc(incd_o))
                                .done(function(on_off_obj){
                                    that.edit_offline(off_model, on_off_obj.off_json)
                                        .done(function(off_model){
                                            // console.log("INCD:EDIT: Successfully edited model in offline db. Edited model - "+JSON.stringify(off_model.toJSON()));
                                            dfd.resolve();
                                        })
                                        .fail(function(error){
                                            // console.log("INCD:EDIT: Error saving model in offline db. Moving on... - "+error);
                                            // alert("Unexpected error:INCD:EDIT: Error saving new model in offline db. Moving on... - "+error);
                                            dfd.reject(error);
                                        });    
                                })
                                .fail(function(error){
                                    // console.log("INCD:EDIT: Not saving object to offlinedb coz onlineTOoffline failed");
                                    dfd.reject(error);
                                });    
                        })
                        .fail(function(response){
                            // console.log("INCD:EDIT: Error fetching model from server. Moving on... - "+response.statusText);
                            dfd.reject(response);
                        });
                })
                .fail(function(error){
                    // console.log("INCD:EDIT: Error fetching model(to be edited) from offline db. Moving on... - "+error);
                    dfd.reject("Error fetching model(to be edited) from offline db. Moving on..."+error);    
                });    
        },
                
        incd_delete: function(incd_o, dfd){
            console.log("processing delete - "+JSON.stringify(incd_o));
            var that = this;
            this.fetch_from_offline(this.get_online_id(incd_o))
                .done(function(off_model){
                    off_model.destroy({
                        success: function(){
                            // console.log("INCD:DELETE: Successfully deleted model from offline db.");
                            dfd.resolve();
                        },
                        error: function(error){
                            // console.log("INCD:DELETE: Error deleteing model from offline db. Moving on... - "+error);
                            // alert("Unexpected error:INCD:DELETE: Error deleteing model from offline db. Moving on... - "+error);
                            dfd.reject();
                        }    
                    })
                })
                .fail(function(error){
                    // console.log("INCD:DELETE: Error fetching model(to be deleted) from offline db. Moving on... - "+error);
                    dfd.resolve(error);    
                });    
        },
        
        fetch_from_offline: function(online_id){
            var dfd = new $.Deferred();
            // console.log("fetching from offline db");
            this.offline_model.clear();
            this.offline_model.set({online_id:parseInt(online_id)});
            // console.log(this.offline_model.toJSON());
            this.offline_model.fetch({
                success: function(off_model){
                    // console.log("offline model successfully fetched");
                    // console.log(off_model);
                    dfd.resolve(off_model);
                },
                error: function(model,error){
                    // console.log("offline model could not be fetched - "+error);
                    dfd.reject(error);
                }    
            });
            return dfd.promise();    
        },
          
        fetch_from_online: function(online_id){
            var dfd = new $.Deferred();
            // console.log("fetching from online db");
            this.online_model.clear();
            this.online_model.set('id',parseInt(online_id));
            this.online_model.fetch({
                success: function(on_model,response){
                    // console.log("online model successfully fetched");
                    // console.log(on_model);
                    dfd.resolve(on_model);
                },
                error: function(model, response, options){
                    // console.log("online model could not be fetched - "+response);
                    dfd.reject(response);
                }    
            });
            return dfd.promise();    
        },
        
        add_offline: function(json){
            var dfd = new $.Deferred();
            //TODO: convert json online to offline
            this.offline_model.clear();
            this.offline_model.set(json);
            this.offline_model.set('online_id',parseInt(json.id));
            this.offline_model.unset('id');  //new id would be generated, not saving by server id
            this.offline_model.save(null,{
                success: function(off_model){
                    dfd.resolve(off_model);
                },
                error: function(model,error){
                    // console.log(error);
                    dfd.reject(error);
                }    
            });
            return dfd.promise();    
        },
                   
        edit_offline: function(off_model, json){
            var dfd = new $.Deferred();
            //TODO: convert json online to offline
            var offline_id = off_model.get("id");
            var online_id = json.id;
            off_model.set(json);
            off_model.set('id', parseInt(offline_id));
            off_model.set('online_id', parseInt(online_id));
            off_model.save(null,{
                success: function(off_model){
                    // console.log(off_model);
                    // console.log(online_id);
                    dfd.resolve(off_model);
                },
                error: function(model,error){
                    dfd.reject("ERRO EDITING model in IDB: ");
                }    
            });
            return dfd.promise();    
        },
        
        finish_download: function(last_object_timestamp){
            var dfd = new $.Deferred();
            
            //possible if timestamp of last object in incd was not present or no objects were returned
            if(!last_object_timestamp)
                last_object_timestamp = this.start_timestamp;
            console.log("DASHBOARD:DOWNLOAD: In finish downlaod");
            var that = this;
            var generic_model_offline = Backbone.Model.extend({
                database: indexeddb,
                storeName: "meta_data",
            });
            var meta_model = new generic_model_offline();
            meta_model.set({key: "last_inc_download"});
            meta_model.fetch({
                success: function(model){
                    console.log("DASHBOARD:DOWNLOAD: last_inc_download fetched from meta_data objectStore:");
                    console.log(JSON.stringify(model.toJSON()));
                    model.set('timestamp',last_object_timestamp);
                    model.save(null,{
                        success: function(){
                            console.log("DASHBOARD:DOWNLOAD: last_inc_download updated in meta_data objectStore:");    
                            console.log(JSON.stringify(model.toJSON()));
                            dfd.resolve();
                        },
                        error: function(model,error){
                            console.log("DASHBOARD:DOWNLOAD: error updating last_inc_download in meta_data objectStore");  
                            console.log(error);
                            dfd.reject(error);  
                        }
                    });
                },
                error: function(model,error){
                    console.log("DASHBOARD:DOWNLOAD: error while fetching last_inc_download from meta_data objectStore");
                    if(error == "Not Found")
                        {
                            meta_model.set('timestamp',last_object_timestamp);
                            meta_model.save(null,{
                                success: function(model){
                                    console.log("DASHBOARD:DOWNLOAD: last_inc_download created in meta_data objectStore:");    
                                    console.log(JSON.stringify(model.toJSON()));
                                    dfd.resolve();
                                },
                                error: function(model,error){
                                    console.log("DASHBOARD:DOWNLOAD: error creating last_inc_download in meta_data objectStore : ");
                                    console.log(error);   
                                    dfd.reject(error); 
                                }
                            });
                            
                        }    
                }        
            });
            return dfd;
        }
        
        

              
    });
    
    
    
  // Our module now returns our view
  return IncrementalDownloadView;
});
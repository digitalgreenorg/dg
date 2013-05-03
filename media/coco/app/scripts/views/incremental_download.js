define([
  'jquery',
  'underscore',
  'backbone',
  'indexeddb_backbone_config',
  'configs',
  'collections/upload_collection',
  'online_to_offline'      
], function($,pas,pass,indexeddb, all_configs,upload_collection, OnlineToOffline){
    
    var IncrementalDownloadView = Backbone.Layout.extend({
        
        template: "#incremental_download_template",
        increment_pb: function() {
            w = parseFloat(document.getElementById('inc_pbar').style.width);
            document.getElementById('inc_pbar').style.width= (w + this.progress_bar_step) +'%';
            // alert(w);
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
                .bindAll('json_converted');
            _(this)
                .bindAll('iterate_incd_objects');
            _(this)
                .bindAll('pick_next');
        },  
              
        start_incremental_download: function() {
            this.$('#incremental_download_modal').modal('show');
            console.log("UPLOAD: start the fuckin incremental_download");
            this.getIncObjects();
            
        },

        getIncObjects: function(){
            var fetch_inc_d_objects = $.get("/get_log/",{timestamp:"2012-03-10 12:06:04"});
            fetch_inc_d_objects.fail(function(){ 
                alert("Incremental download fetch failed!"); 
            });
            fetch_inc_d_objects.done(this.iterate_incd_objects);
        },    
            
        iterate_incd_objects: function(incd_objects){
            this.incd_objects = incd_objects;
            this.in_progress = true;
            this.progress_bar_step = 100/incd_objects.length;
            this.download_status = {};
            this.download_status["total"] = incd_objects.length;
            this.download_status["downloaded"] = 0;
            console.log("INCD objects received");
            console.log(incd_objects);
            this.pick_next();
        },  
        
        pick_next: function(){
            var that = this;
            this.update_status(this.download_status["downloaded"]+"/"+this.download_status["total"]);
            this.cur_incd_o = this.incd_objects.shift();
            if(this.cur_incd_o)
            {
                this.process_incd_object(this.cur_incd_o)
                    .fail(function(){
                        console.log("FAILED TO INC DOWNLOAD AN OBJECT");
                    })
                    .always(function(){
                        that.increment_pb();
                        that.download_status["downloaded"]++;
                        that.pick_next();
                    })
            }
        },     
        
        // {"pk":9372,"model":"dashboard.serverlog","fields":{"action":1,"timestamp":"2013-04-15T06:47:35","entry_table":"Screening","model_id":10000000132086}}
        get_entity_name: function(obj){
            return obj.fields.entry_table.toLowerCase();
        },
            
        get_action: function(obj){
            return obj.fields.action;
        },    
        
        get_online_id: function(obj){
            return obj.fields.model_id;
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
            console.log("INCD object received - "+JSON.stringify(incd_o));
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
                    case 1: console.log("its add");
                    this.incd_add(incd_o, dfd);
                    break;
                    case 0: console.log("its edit");
                    this.incd_edit(incd_o, dfd);
                    break;
                    case -1: console.log("its delete");
                    this.incd_delete(incd_o, dfd);
                    break
                    default: console.log("ambiguous case");    
                }    
            return dfd.promise();    
        },
        
        incd_add: function(incd_o, dfd){
            console.log("processing add - "+JSON.stringify(incd_o));
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
                                                console.log("INCD:ADD: Successfully added model in offline db. Added model - "+JSON.stringify(off_model.toJSON()));
                                                dfd.resolve();
                                            })
                                            .fail(function(error){
                                                console.log("INCD:ADD: Error saving model in offline db - "+error);
                                                console.log(error);
                                                alert("Unexpected error:INCD:ADD: Error saving new model in offline db - "+error);
                                                dfd.reject();
                                            });    
                                    })
                                    .fail(function(){
                                        console.log("INCD:ADD: Not saving object to offlinedb coz onlineTOoffline failed");
                                        dfd.reject();
                                    });    
                            })
                            .fail(function(response){
                                console.log("INCD: Error fetching model from server - "+response.statusText);
                                dfd.reject();
                            });
                    }
                })
                .done(function(off_model){
                    console.log("INCD: The model supposed to be added already exists. Moving on...");
                    dfd.reject();    
                });    
        },    
        
        incd_edit: function(incd_o, dfd){
            console.log("processing edit - "+JSON.stringify(incd_o));
            var that = this;
            this.fetch_from_offline(this.get_online_id(incd_o))
                .done(function(off_model){
                    that.fetch_from_online(that.get_online_id(incd_o))
                        .done(function(on_model){
                            OnlineToOffline.convert(on_model.toJSON(), that.get_foreign_field_desc(incd_o))
                                .done(function(on_off_obj){
                                    that.edit_offline(off_model, on_off_obj.off_json)
                                        .done(function(off_model){
                                            console.log("INCD:EDIT: Successfully edited model in offline db. Edited model - "+JSON.stringify(off_model.toJSON()));
                                            dfd.resolve();
                                        })
                                        .fail(function(error){
                                            console.log("INCD:EDIT: Error saving model in offline db. Moving on... - "+error);
                                            alert("Unexpected error:INCD:EDIT: Error saving new model in offline db. Moving on... - "+error);
                                            dfd.reject();
                                        });    
                                })
                                .fail(function(){
                                    console.log("INCD:EDIT: Not saving object to offlinedb coz onlineTOoffline failed");
                                    dfd.reject();
                                });    
                        })
                        .fail(function(response){
                            console.log("INCD:EDIT: Error fetching model from server. Moving on... - "+response.statusText);
                            dfd.reject();
                        });
                })
                .fail(function(error){
                    console.log("INCD:EDIT: Error fetching model(to be edited) from offline db. Moving on... - "+error);
                    dfd.reject();    
                });    
        },
                
        incd_delete: function(incd_o, dfd){
            console.log("processing delete - "+JSON.stringify(incd_o));
            var that = this;
            this.fetch_from_offline(this.get_online_id(incd_o))
                .done(function(off_model){
                    off_model.destroy({
                        success: function(){
                            console.log("INCD:DELETE: Successfully deleted model from offline db.");
                            dfd.resolve();
                        },
                        error: function(error){
                            console.log("INCD:DELETE: Error deleteing model from offline db. Moving on... - "+error);
                            alert("Unexpected error:INCD:DELETE: Error deleteing model from offline db. Moving on... - "+error);
                            dfd.resolve();
                        }    
                    })
                })
                .fail(function(error){
                    console.log("INCD:DELETE: Error fetching model(to be deleted) from offline db. Moving on... - "+error);
                    dfd.resolve();    
                });    
        },
        
        fetch_from_offline: function(online_id){
            var dfd = new $.Deferred();
            console.log("fetching from offline db");
            this.offline_model.clear();
            this.offline_model.set({online_id:parseInt(online_id)});
            console.log(this.offline_model.toJSON());
            this.offline_model.fetch({
                success: function(off_model){
                    console.log("offline model successfully fetched");
                    console.log(off_model);
                    dfd.resolve(off_model);
                },
                error: function(error){
                    console.log("offline model could not be fetched - "+error);
                    dfd.reject(error);
                }    
            });
            return dfd.promise();    
        },
          
        fetch_from_online: function(online_id){
            var dfd = new $.Deferred();
            console.log("fetching from online db");
            this.online_model.clear();
            this.online_model.set('id',parseInt(online_id));
            this.online_model.fetch({
                success: function(on_model,response){
                    console.log("online model successfully fetched");
                    console.log(on_model);
                    dfd.resolve(on_model);
                },
                error: function(model, response, options){
                    console.log("online model could not be fetched - "+response);
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
                error: function(error){
                    console.log(error);
                    dfd.reject(error);
                }    
            });
            return dfd.promise();    
        },
                   
        edit_offline: function(off_model, json){
            var dfd = new $.Deferred();
            //TODO: convert json online to offline
            var offline_id = this.off_model.get("id");
            this.off_model.set(json);
            this.off_model.set('id', offline_id);
            this.off_model.set('online_id', json.id);
            this.off_model.save(null,{
                success: function(off_model){
                    dfd.resolve(off_model);
                },
                error: function(error){
                    dfd.reject(error);
                }    
            });
            return dfd.promise();    
        },
                       
        json_converted: function(something){
            console.log("Gotcha B****: conv json");
            console.log(something);
            // if (this.current_entry.get("action") == "A") {
//                 console.log("UPLOAD: its add action");
//                 this.upload_add(something.on_json);
//             } else if (this.current_entry.get("action") == "E") {
//                 console.log("UPLOAD: its edit action");
//                 this.upload_edit(something.on_json);
//             }
        },
        
        
        

              
    });
    
    
    
  // Our module now returns our view
  return IncrementalDownloadView;
});
// Retrieves updates on server since a timestamp, runs those updates on the offline DB thus keeping the offline db in sync with server db
// To use the module create an instance and call start_incremental_download on it 
define([
    'jquery',
    'underscore',
    'layoutmanager',
    'indexeddb_backbone_config',
    'configs',
    'convert_namespace',
    'offline_utils',
    'indexeddb-backbone',
    'bootstrapjs',
], function(jquery, underscore, layoutmanager, indexeddb, all_configs, ConvertNamespace, Offline) {

    var IncrementalDownloadView = Backbone.Layout.extend({

        initialize: function() {
            console.log("UPLOAD: initializing new incremental_download view");
            _.bindAll(this);
            this.start_timestamp = null;
            this.in_progress = false;
        },

        template: "#incremental_download_template",
        events: {
            "click #stop_inc_download": "stop_inc_download"
        },

        //increment the progress bar
        increment_pb: function() {
            //get the current width of progress bar
            w = parseFloat(document.getElementById('inc_pbar').style.width);
            //increment the width with the step
            document.getElementById('inc_pbar').style.width = (w + this.progress_bar_step) + '%';
        },

        //update the status on the view - # of downloaded/# of total objects
        update_status: function(status) {
            console.log(status);
            $('#inc_status').html(status);
        },

        //update the action on the view - for eg - "downloading person"
        update_action: function(action) {
            $('#inc_action').html(action);
        },

        //set the user_interrupt flag when user clicks on stop button - flag is checked before starting to process each update. So inc download would be stopped after the current object bieng downloaded is finished bieng processed
        stop_inc_download: function() {
            console.log("stopping inc download");
            this.user_interrupt = true;
        },

        //initializes the global vars used, ui
        initialize_inc_download: function(options) {
            var dfd = new $.Deferred();
            this.in_progress = true;
            this.user_interrupt = false;
            var that = this;

            //set ui for foreground inc download
            if (!(options.background)) {
                this.template = "#incremental_download_template";
                this.render()
                    .done(function() {
                        that.$('#incremental_download_modal').modal({
                            keyboard: false,
                            backdrop: "static",
                        });
                        //modal takes time to animate and show up - so wait till it is completely visible to the user
                        that.$('#incremental_download_modal').on('shown', function() {
                            dfd.resolve();
                        });
                        that.$('#incremental_download_modal').modal('show');
                    });
            }
            //set ui for background inc download
            else {
                this.template = "#incremental_download_background_template";
                this.render()
                    .done(function() {
                        dfd.resolve();
                    });
            }
            return dfd.promise();
        },

        //remove the view
        tear_down: function() {
            this.$('#incremental_download_modal').modal('hide');
            this.remove();
            this.in_progress = false;
        },

        //starts the inc download process          
        start_incremental_download: function(options) {
            var dfd = new $.Deferred();
            var that = this;
            console.log("INCREMENTAL DOWNLOAD: start the incremental_download");
            var that = this;
            //initialization logic - like setting up ui, initializing global vars
            this.initialize_inc_download(options)
                .done(function() {
                    //query the endpoint to get the list of updates
                    that.getIncObjects()
                        .done(function(objects) {
                            //serially process each update
                            that.iterate_incd_objects(objects)
                                .done(function(last_object_timestamp) {
                                    //some finish logic -  save the timestamp
                                    that.finish_download(last_object_timestamp)
                                        .done(function() {
                                            //inc download successfuly finished
                                            //remove the view
                                            that.tear_down();
                                            //resolve the process
                                            dfd.resolve();
                                        })
                                        .fail(function(error) {
                                            //something failed in finish download
                                            that.tear_down();
                                            dfd.reject(error);
                                        });
                                })
                                .fail(function(error) {
                                    //error while saving some update
                                    if (error.last_object_timestamp) {
                                        //save the timestamp of last object successfully processed so that next inc download resumes from this point
                                        that.finish_download(error.last_object_timestamp)
                                            .always(function() {
                                                that.tear_down();
                                                dfd.reject(error.err_msg);
                                            });
                                    }
                                    dfd.reject(error.err_msg)
                                });
                        })
                        .fail(function(error) {
                            //something failed while getting the updates from server
                            that.tear_down();
                            dfd.reject(error);
                        });
                });
            return dfd;
        },

        //gets the list of updates from server
        getIncObjects: function() {
            var dfd = new $.Deferred();
            //Recording the time when the request for update was sent, to update last_inc_downloaded ts if required.
            this.start_timestamp = new Date().toJSON().replace("Z", "");
            //get the timestamp since when updates have to be fetched = timestamp when last inc download was run
            this.get_last_download_timestamp()
                .done(function(timestamp) {
                    console.log("Timestamp for inc download - " + timestamp);
                    //send the get request 
                    $.get(all_configs.misc.inc_download_url, {
                        timestamp: timestamp
                    }, function() {}, "json")
                        .fail(function() {
                            dfd.reject("Incremental download objects fetch failed!");
                        })
                        .done(function(objects) {
                            //resolve and return the objects
                            dfd.resolve(objects);
                        });
                })
                .fail(function(error) {
                    dfd.reject(error);
                });
            return dfd;
        },

        //the timestamp of the time when last inc download was run is returned or if no inc download has run till now, timestamp of full download is returned
        get_last_download_timestamp: function() {
            var dfd = new $.Deferred();
            //fetch last_inc_download timestamp from meta_data table
            Offline.fetch_object("meta_data", "key", "last_inc_download")
                .done(function(model) {
                    dfd.resolve(model.get('timestamp'));
                })
                .fail(function(model, error) {
                    //no last_inc_download timestamp found
                    //fetch and  return the timestamp of last full download
                    Offline.fetch_object("meta_data", "key", "last_full_download")
                        .done(function(model) {
                            dfd.resolve(model.get('timestamp'));
                        })
                        .fail(function(model, error) {
                            dfd.reject("Neither inc download has happened before nor full download.");
                        });
                });

            return dfd;
        },

        iterate_incd_objects: function(incd_objects) {
            var dfd = new $.Deferred();
            this.incd_objects = incd_objects;
            if (!this.incd_objects.length || this.incd_objects == 0)
                return dfd.resolve();

            //step for progress bar increments    
            this.progress_bar_step = 100 / incd_objects.length;
            //stores the current download status
            this.download_status = {};
            this.download_status["total"] = incd_objects.length;
            this.download_status["downloaded"] = 0;
            console.log("INCD objects received");
            console.log(incd_objects);
            this.pick_next(dfd);
            return dfd;
        },

        //recursively iterates over the incd_objects list till its empty
        pick_next: function(whole_download_dfd) {
            var that = this;
            this.prev_incd_o = this.cur_incd_o;
            this.update_status(this.download_status["downloaded"] + "/" + this.download_status["total"]);
            this.cur_incd_o = this.incd_objects.shift();
            //all updates processed
            if (!this.cur_incd_o) {
                var update_timestamp;
                //get the timestamp of last object processed 
                if (this.prev_incd_o)
                    update_timestamp = this.get_timestamp(this.prev_incd_o)
                    //if no object was processed use the start time of inc download    
                else
                    update_timestamp = this.start_timestamp;
                return whole_download_dfd.resolve(update_timestamp);
            }
            //user interrupt flag is set - user clicked on stop button
            else if (this.user_interrupt) {
                var update_timestamp;
                //get the timestamp of last object processed 
                if (this.prev_incd_o)
                    update_timestamp = this.get_timestamp(this.prev_incd_o)
                else
                    update_timestamp = null;
                return whole_download_dfd.reject({
                    err_msg: "User stopped Sync",
                    last_object_timestamp: update_timestamp
                });
            }
            // process the object
            else {
                this.process_incd_object(this.cur_incd_o)
                    .fail(function(error) {
                        console.log("FAILED TO INC DOWNLOAD AN OBJECT: ");
                        console.log(error);
                    })
                    .done(function() {
                        console.log("SUCESSFULLY DOWNLOADED AN OBJECT");
                    })
                    .always(function() {
                        // continue processing the objects even if this object failed
                        //  increment progress bar
                        that.increment_pb();
                        // increment download status
                        that.download_status["downloaded"]++;
                        //recursively process the rest of the objects
                        that.pick_next(whole_download_dfd);
                    });
            }
        },

        //format of each object: {"pk":9372,"model":"dashboard.serverlog","fields":{"action":1,"timestamp":"2013-04-15T06:47:35","entry_table":"Screening","model_id":10000000132086}}
        // get the timestamp from object
        get_timestamp: function(obj) {
            return obj.fields.timestamp;
        },
        //get entity_name from object
        get_entity_name: function(obj) {
            for (var member in all_configs) {
                if (member == obj.fields.entry_table.toLowerCase()) {
                    return all_configs[member].entity_name;
                } else if ((all_configs[member].inc_table_name) && (all_configs[member].inc_table_name == obj.fields.entry_table.toLowerCase())) {
                    return all_configs[member].entity_name;
                }
            }
            return -1;
        },
        //get action from object
        get_action: function(obj) {
            return obj.fields.action;
        },
        //get online_id from object
        get_online_id: function(obj) {
            return parseInt(obj.fields.model_id);
        },
        //get foreign field desc object for this object
        get_foreign_field_desc: function(obj) {
            var entity_name = this.get_entity_name(obj);
            if (all_configs[entity_name].edit) {
                return all_configs[entity_name].edit.foreign_entities;
            } else
                return all_configs[entity_name].foreign_entities;
        },

        //runs an update object on the offline db             
        process_incd_object: function(incd_o) {
            var dfd = new $.Deferred();
            var that = this;
            // create online and offline backbone models for this entity
            // should be using the offline_utils and online_utils instead
            var generic_model_offline = Backbone.Model.extend({
                database: indexeddb,
                storeName: this.get_entity_name(incd_o),
            });
            var generic_model_online = Backbone.Model.extend({
                sync: Backbone.ajaxSync,
                url: function() {
                    return this.id ? all_configs[that.get_entity_name(incd_o)].rest_api_url + this.id + "/" : all_configs[that.get_entity_name(incd_o)].rest_api_url;
                },
            });
            this.offline_model = new generic_model_offline();
            this.online_model = new generic_model_online();
            
            //update action on the view
            this.update_action("Downloading " + this.get_entity_name(incd_o));
            
            switch (this.get_action(incd_o)) {
                // add case
                case 1:
                    this.incd_add(incd_o, dfd);
                    break;
                // edit case
                case 0:
                    this.incd_edit(incd_o, dfd);
                    break;
                // delete case    
                case -1:
                    this.incd_delete(incd_o, dfd);
                    break;
                default:
                    console.log("ambiguous case");
                    dfd.reject("ambiguous case. None of add, edit , delete!");
            }
            return dfd.promise();
        },
        
        // runs an add-update on offline db
        incd_add: function(incd_o, dfd) {
            var that = this;
            //fetch object from offline db - check whether it already exists
            this.fetch_from_offline(this.get_online_id(incd_o))
                .fail(function(error) {
                    if (error == "Not Found") {
                        fetch_and_add();
                    }
                })
                .done(function(off_model) {
                    // console.log("INCD: The model supposed to be added already exists. Moving on...");
                    fetch_and_add(off_model);
                });

            function fetch_and_add(existing_model) {
                //fetch update object from server
                that.fetch_from_online(that.get_online_id(incd_o))
                    .done(function(on_model) {
                        //convert namespace from online to offline
                        ConvertNamespace.convert(on_model.toJSON(), that.get_foreign_field_desc(incd_o), "onlinetooffline")
                            .done(function(on_off_obj) {
                                var off_json = on_off_obj.off_json;
                                //inject online id and remove server id so that offline DB generate its own id for this object
                                if (off_json.id) {
                                    off_json.online_id = parseInt(off_json.id);
                                    delete off_json.id;
                                }
                                //if the object with this online id already existed in offline DB it wud be over-written otherwise new one wud be created
                                Offline.save(existing_model, that.get_entity_name(incd_o), off_json)
                                    .done(function(off_model) {
                                        dfd.resolve();
                                    })
                                    .fail(function(error) {
                                        dfd.reject(error);
                                    });
                            })
                            .fail(function(error) {
                            	console.log("INCD: Failed convertnamespace..not saving ");
                            	dfd.reject(error);
                            });
                    })
                    .fail(function(response) {
                        // console.log("INCD: Error fetching model from server - "+response.statusText);
                        dfd.reject(response);
                    });
            }
        },

        // runs an edit-update on offline db
        incd_edit: function(incd_o, dfd) {
            var that = this;
            //fetch this object from offline db
            this.fetch_from_offline(this.get_online_id(incd_o))
                .done(function(off_model) {
                    //fetch the object from server
                    that.fetch_from_online(that.get_online_id(incd_o))
                        .done(function(on_model) {
                            //convert namespace of foreign elements in server object from online to offline
                            ConvertNamespace.convert(on_model.toJSON(), that.get_foreign_field_desc(incd_o), "onlinetooffline")
                                .done(function(on_off_obj) {
                                    //save the edit on offline db - remove this and use offline_utils instead
                                    that.edit_offline(off_model, on_off_obj.off_json)
                                        .done(function(off_model) {
                                            //  successfully edited in offline db
                                            dfd.resolve();
                                        })
                                        .fail(function(error) {
                                            //edit save failed
                                            dfd.reject(error);
                                        });
                                })
                                .fail(function(error) {
                                    //namespace conversion failed
                                    dfd.reject(error);
                                });
                        })
                        .fail(function(response) {
                            //server fetch failed
                            dfd.reject(response);
                        });
                })
                .fail(function(error) {
                    // object which was edited on server does not exist in offline DB...doing nothing...
                    dfd.reject("Error fetching model(to be edited) from offline db. Moving on..." + error);
                });
        },

        // runs a delete-update on offline db
        incd_delete: function(incd_o, dfd) {
            console.log("processing delete - " + JSON.stringify(incd_o));
            var that = this;
            //fetch object from offline db
            this.fetch_from_offline(this.get_online_id(incd_o))
                .done(function(off_model) {
                    //delete the object 
                    off_model.destroy({
                        success: function() {
                            dfd.resolve();
                        },
                        error: function(error) {
                            dfd.reject();
                        }
                    })
                })
                .fail(function(error) {
                    // object to be deleted already doesn't exists in offline db 
                    dfd.resolve(error);
                });
        },

        //executed at end of the inc download process
        finish_download: function(last_object_timestamp) {
            var dfd = new $.Deferred();
            var that = this;
            //possible if timestamp of last object in incd was not present or no objects were returned
            if (!last_object_timestamp)
                last_object_timestamp = this.start_timestamp;

            //update timestamp of last inc download in meta_data table    
            Offline.fetch_object("meta_data", "key", "last_inc_download")
                .done(function(model) {
                    set_timestamp(model);
                })
                .fail(function(model, error) {
                    set_timestamp(model);
                });

            function set_timestamp(model) {
                model.set('timestamp', last_object_timestamp);
                model.save(null, {
                    success: function() {
                        dfd.resolve();
                    },
                    error: function(model, error) {
                        dfd.reject("error updating last_full_download in meta_data objectStore");
                    }
                });
            };

            return dfd;
        },

        // all of the following functions should be removed and offline_utils and online_utils should be used instead - the dependence on global offline_model and online_model would also have to be removed
        
        //fetch object with online_id=online_id from offline db
        fetch_from_offline: function(online_id) {
            var dfd = new $.Deferred();
            this.offline_model.clear();
            this.offline_model.set({
                online_id: parseInt(online_id)
            });
            this.offline_model.fetch({
                success: function(off_model) {
                    dfd.resolve(off_model);
                },
                error: function(model, error) {
                    dfd.reject(error);
                }
            });
            return dfd.promise();
        },

        // fetch object with id=online_id from server 
        fetch_from_online: function(online_id) {
            var dfd = new $.Deferred();
            this.online_model.clear();
            this.online_model.set('id', parseInt(online_id));
            this.online_model.fetch({
                success: function(on_model, response) {
                    dfd.resolve(on_model);
                },
                error: function(model, response, options) {
                    dfd.reject(response);
                }
            });
            return dfd.promise();
        },

        // adds json object in offline db using offline_model
        add_offline: function(json) {
            var dfd = new $.Deferred();
            this.offline_model.clear();
            this.offline_model.set(json);
            this.offline_model.set('online_id', parseInt(json.id));
            this.offline_model.unset('id'); //new id would be generated, not saving by server id
            this.offline_model.save(null, {
                success: function(off_model) {
                    dfd.resolve(off_model);
                },
                error: function(model, error) {
                    dfd.reject(error);
                }
            });
            return dfd.promise();
        },

        // edits the object in off_model to json
        edit_offline: function(off_model, json) {
            var dfd = new $.Deferred();
            var offline_id = off_model.get("id");
            var online_id = json.id;
            off_model.set(json);
            off_model.set('id', parseInt(offline_id));
            off_model.set('online_id', parseInt(online_id));
            off_model.save(null, {
                success: function(off_model) {
                    dfd.resolve(off_model);
                },
                error: function(model, error) {
                    dfd.reject("ERRO EDITING model in IDB: ");
                }
            });
            return dfd.promise();
        },

    });

    return IncrementalDownloadView;
});

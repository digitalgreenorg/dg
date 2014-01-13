// Uploads any data that is present in the uploadq to the server
// To use the module create an instance and call start_upload on it 
define([
    'jquery',
    'underscore',
    'layoutmanager',
    'configs',
    'views/form',
    'collections/upload_collection',
    'convert_namespace',
    'offline_utils',
    'online_utils',
    'indexeddb-backbone',
    'bootstrapjs'
], function(jquery, underscore, layoutmanager, configs, Form, upload_collection, ConvertNamespace, Offline, Online) {

    var UploadView = Backbone.Layout.extend({

        initialize: function() {
            console.log("UPLOAD: initializing new upload view");
            _(this).bindAll('stop_upload');
        },

        template: "#upload_template",

        events: {
            "click #stop_upload": "stop_upload"
        },

        //set the user_interrupt flag when user clicks on stop button - flag is checked before starting to process each upload object. So upload would be stopped after the current object bieng uploaded is finished bieng processed
        stop_upload: function() {
            console.log("stopping upload");
            this.user_interrupt = true;
        },

        //increment the progress bar
        increment_pb: function() {
            //get the current width of progress bar
            w = parseFloat(document.getElementById('pbar').style.width);
            //increment the width with the step
            document.getElementById('pbar').style.width = (w + progress_bar_step) + '%';
        },

        //update the status on the view - # of uploaded/# of total objects
        update_status: function(status) {
            $('#upl_status').html(status);
        },

        //update the action on the view - for eg - "uploading person"
        update_action: function(action) {
            $('#upl_action').html(action);
        },

        //initializes the global vars used, ui
        initialize_upload: function() {
            this.user_interrupt = false;
            this.in_progress = true;
            this.$('#upload_modal').modal({
                keyboard: false,
                backdrop: "static",
            });
            this.$('#upload_modal').modal('show');

        },

        //removes the view
        tear_down: function() {
            var dfd = new $.Deferred();
            this.in_progress = false;
            var that = this;
            //modal takes time to hide. Needed to get the correct point of time when upload has finished.
            $('#upload_modal').on('hidden', function() {
                that.remove();
                dfd.resolve();
            });
            $('#upload_modal').modal('hide');
            return dfd.promise();
        },

        // starts the upload process      
        start_upload: function() {
            var dfd = new $.Deferred();
            console.log("UPLOAD: start the upload");
            var that = this;
            //run the inititalization logic - setup global vars , ui
            this.initialize_upload();
            //retrieve the collection of objects to be uploaded
            this.get_uploadq()
                .done(function(collection) {
                    //process each object serially in the upload collection
                    that.iterate_uploadq(collection)
                        .done(function() {
                            // upload successfully finished
                            that.tear_down()
                                .done(function() {
                                    dfd.resolve();
                                });
                        })
                        .fail(function(error) {
                            // upload failed
                            that.tear_down()
                                .done(function() {
                                    dfd.reject(error);
                                });
                        });
                })
                .fail(function(error) {
                    // failed to retrieve objects to be uploaded
                    that.tear_down()
                        .done(function() {
                            dfd.reject(error);
                        });
                });
            return dfd;
        },

        //Reads the uploadQ table through the upload_collection backbone collection
        get_uploadq: function() {
            var dfd = new $.Deferred();
            // upload_collection is a pre-defined backbone collection attached to the uploadQ table in offline db
            upload_collection.fetch({
                success: function(collection) {
                    dfd.resolve(collection);
                },
                error: function(error) {
                    dfd.reject(error);
                }
            });
            return dfd;
        },

        // process each object serially in the uploadQ
        iterate_uploadq: function(uploadq) {
            var dfd = new $.Deferred();
            this.upload_collection = uploadq;
            console.log("UPLOAD: inside upload queue: " + this.upload_collection.length + " entries");
            $('#num_upload').html(this.upload_collection.length);

            //step for progress bar increments    
            progress_bar_step = 100 / this.upload_collection.length;
            //stores the current download status
            this.upload_status = {};
            this.upload_status["total"] = this.upload_collection.length;
            this.upload_status["uploaded"] = 0;
            this.pick_next(dfd);
            return dfd;
        },

        //returns the entity name of the object to be uploaded
        get_entity_name: function(upload_model) {
            return upload_model.get('entity_name')
        },

        //returns the action of the object to be uploaded
        get_action: function(upload_model) {
            return upload_model.get('action');
        },

        //returns the json of the object
        get_json: function(upload_model) {
            return upload_model.get('data');
        },

        //returns the foregn field desc of the object 
        get_foreign_field_desc: function(upload_model) {
            var entity_name = this.get_entity_name(upload_model);
            if (configs[entity_name].edit) {
                return configs[entity_name].edit.foreign_entities;
            } else
                return configs[entity_name].foreign_entities;
        },

        //returns the offline id of the object 
        get_offline_id: function(upload_model) {
            return parseInt(this.get_json(upload_model).id);
        },

        //returns the online id of the object 
        get_online_id: function(upload_model) {
            return parseInt(this.get_json(upload_model).online_id);
        },

        //recursively iterates over the uploadq list till its empty
        pick_next: function(whole_upload_dfd) {
            console.log("in pick_next");
            var that = this;
            this.update_status(this.upload_status["uploaded"] + "/" + this.upload_status["total"]);
            this.current_entry = this.upload_collection.shift();
            //all uploads processed
            if (!this.current_entry) {
                return whole_upload_dfd.resolve();
            }
            //user interrupt flag is set - user clicked on stop button
            else if (this.user_interrupt) {
                //put the upload object back
                this.upload_collection.unshift(this.current_entry);
                //stop the process
                return whole_upload_dfd.reject("User stopped Sync");
            }
            // process the object
            else {
                this.process_upload_entry(this.current_entry)
                    .fail(function(error) {
                        console.log("FAILED TO UPLOAD AN OBJECT: ");
                        console.log(error);
                        //it would be reached in foll cases:
                        //object to be uploaded doesn't exists in offline anymore
                        //ConvertNamespace failed
                        //online_id couldn't be injected
                        //The object discarded in upload error form could not be deleted
                    })
                    .done(function() {
                        console.log("SUCESSFULLY UPLOADED AN OBJECT");
                    })
                    .always(function() {
                        // delete the object..finished processing it
                        that.current_entry.destroy();
                        // continue processing the objects even if this object failed
                        //  increment progress bar
                        that.increment_pb();
                        // increment upload status
                        that.upload_status["uploaded"]++;
                        //recursively process the rest of the objects
                        that.pick_next(whole_upload_dfd);
                    });
            }

        },

        //starts processing of a single upload object             
        process_upload_entry: function(up_entry) {
            var dfd = new $.Deferred();
            //update action on the view
            this.update_action("Uploading " + this.get_entity_name(up_entry));

            switch (this.get_action(up_entry)) {
                case 'A':
                    //add case
                    this.upload_add_edit(up_entry, dfd);
                    break;
                case 'E':
                    //edit case
                    this.upload_add_edit(up_entry, dfd);
                    break;
                case 'D':
                    //delete case
                    this.upload_delete(up_entry, dfd);
                    break;
                default:
                    console.log("ambiguous case");
                    dfd.reject("UPLOAD:UNEXPECTED ERROR: Ambiguous case. None of add, edit , delete!");
            }
            return dfd.promise();

        },

        upload_add_edit: function(up_model, dfd) {
            var that = this;
            //check whether the object to be added/edited still exists, get the online_id for edit case
            Offline.fetch_object(this.get_entity_name(up_model), "id", this.get_offline_id(up_model))
                .done(function(off_model) {
                    console.log("Off model fetched - " + JSON.stringify(off_model.toJSON()));
                    // convert namespace from offline to online 
                    ConvertNamespace.convert(that.get_json(up_model), that.get_foreign_field_desc(up_model), "offlinetoonline")
                        .done(function(on_off_obj) {
                            //add case - remove the offline id - server will generate its own id
                            if (that.get_action(up_model) == "A") {
                                delete on_off_obj.on_json.id;
                            } else {
                                //edit case - put the online_id as id
                                on_off_obj.on_json.id = parseInt(off_model.get("online_id"));
                                delete on_off_obj.on_json.online_id;
                            }
                            // save the object on server
                            Online.save(null, that.get_entity_name(up_model), on_off_obj.on_json)
                                .done(function(on_model) {
                                    console.log("INCD:ADD: Successfully uploaded model. uploaded model - " + JSON.stringify(on_model.toJSON()));
                                    var off_json = off_model.toJSON();
                                    // inject the online id returned by server in offline object
                                    off_json.online_id = parseInt(on_model.get("id"));
                                    Offline.save(off_model, that.get_entity_name(up_model), off_json)
                                        .done(function(off_model) {
                                            // successfully uploaded
                                            console.log("OFF model after all upload - " , JSON.stringify(off_model.toJSON()));
                                            dfd.resolve();
                                        })
                                        .fail(function(error) {
                                            dfd.reject("UPLOAD: Error saving online_id in offline obj: ", error);
                                        });
                                })
                                .fail(function(error) {
                                    // server returned error when uploading object
                                    console.log("Error while saving oject on server");
                                    that.curr_entry_dfd = dfd;
                                    // show the object in its form with the error - to let user fix it and continue with upload
                                    that.show_form(that.get_entity_name(up_model), on_off_obj.off_json, error.responseText);
                                });
                        })
                        .fail(function(model, error) {
                            // namespace conversion failed
                            console.log("UPLOAD: Not uploading object coz ConvertNamespace failed");
                            dfd.reject(error);
                        });
                })
                .fail(function(error) {
                    // the object to be added/edited doesn't exist anymore....move on
                    if (error == "Not Found") {
                        return dfd.reject("The object to be uploaded doesn't exists anymore.")
                    } else
                        dfd.reject(error);
                });
        },

        // show the json in its form with the error returned by server - let user fix it
        show_form: function(entity_name, json, err_msg) {
            console.log("UPLOAD:ERROR: need to show this json -" + JSON.stringify(json));
            // create a form instance with that json
            p = new Form({
                serialize: {
                    button1: "Save again",
                    button2: "Discard"
                },
                entity_name: entity_name,
                model_json: json
            });
            p.render();
            // show the error on form
            p.show_errors(err_msg);
            // listen to when the user clicks save on the form
            this.listenTo(p, 'save_clicked', this.after_upload_error_save_again);
            // listen to when the user clicks discard on the form
            this.listenTo(p, 'button2_clicked', this.after_upload_error_discard);
            this.$('#upload_form')
                .html(p.el);
        },

        // executed when user has corrected an object and retried upload after server returned error
        after_upload_error_save_again: function(e) {
            console.log("UPLOAD:ERROR: edit and retry");
            console.log("UPLOAD:ERROR: json from form - " + JSON.stringify(e.context.final_json));
            // corrected object
            var after_upload_error_json = e.context.final_json;
            var that = this;
            // save the corrected json in offline db
            Offline.save(null, this.get_entity_name(this.current_entry), after_upload_error_json)
                .done(function(off_model) {
                    // remove the form
                    that.$('#upload_form')
                        .empty();
                    // edit the current upload object to set the corrected json    
                    that.current_entry.set('data', after_upload_error_json);
                    // retry uploading the corrected object 
                    that.upload_add_edit(that.current_entry, that.curr_entry_dfd);
                })
                .fail(function(error) {
                    // the corrected json is not accepted by offline db - show the new error on form
                    e.context.show_errors(error);
                });
        },

        // executed when user discards the object after server returned error
        after_upload_error_discard: function(e) {
            console.log("DISCARD");
            var that = this;
            if (this.get_action(this.current_entry) == "A") {
                // delete the object from offline db if its add case
                Offline.delete_object(null, this.get_entity_name(this.current_entry), this.get_offline_id(this.current_entry))
                    .done(function() {
                        return that.curr_entry_dfd.resolve();
                    })
                    .fail(function(error) {
                        return that.curr_entry_dfd.reject("The object discarded in upload error form could not be deleted - " , error);
                    });
            } else {
                // edit case not handled - need to revert the edit in offline db!!
                this.curr_entry_dfd.resolve();
            }
            this.$('#upload_form')
                .html("");
        },

        upload_delete: function(up_model, dfd) {
            if (this.get_online_id(up_model)) {
                // delete the object from server
                Online.delete_object(null, this.get_entity_name(up_model), this.get_online_id(up_model))
                    .done(function() {
                        return dfd.resolve();
                    })
                    .fail(function(error) {
                        return dfd.reject("The object discarded in upload error form could not be deleted - " + error);
                    });
            } else {
                // No online_id was found on the model when deleted. Therefore it was never uploaded on server. Hence taking no action.
                return dfd.resolve();
            }
        },


    });



    // Our module now returns our view
    return UploadView;
});

// This module is responsible for supporting Add/Edit functionalities. This is the container view of Form view for ADD/EDIT. Uses Form view to show the form. When Form has to be saved - gets the json from Form view and processes it to save the object depending upon the internet connectivity of the user.
define([
    'jquery',
    'underscore',
    'layoutmanager',
    'views/notification',
    'indexeddb_backbone_config',
    'configs',
    'views/form',
    'collections/upload_collection',
    'convert_namespace',
    'offline_utils',
    'online_utils',
    'indexeddb-backbone'
], function(jquery, underscore, layoutmanager, notifs_view, indexeddb, configs, Form, upload_collection, ConvertNamespace, Offline, Online) {

    // FormController: Brings up the Add/Edit form

    /*
    If we are saving offline - we set the json from the form, (we denormalize it), save it in the model and save the model in the upload queue.
    If we are saving online - we set the json from the form, (we denormalize it), we convert foreign keys ids to the online namespace, save the offline model, and then save it on server.
    If server save succeeds, then we set the online_id in the offline model.
    */


var message_combined_success = "";
var message_combined_failure = "";

    var FormControllerView = Backbone.Layout.extend({

        initialize: function(params) {
            console.log("FORMCONTROLLER: initializing a new FormControllerView");
            this.params = params;
            _.bindAll(this);
        },
        template: "<div><div id = 'form'></div></div>",

        //setting up the form view
        beforeRender: function() {
            console.log(this.params);
            // pass on the params to the form view - also add desired names of the buttons on form - null hides the button
            this.params = $.extend(this.params, {
                serialize: {
                    button1: "Save and Add Another",
                    button2: null
                }
            });
            // initialize the form view
            var form_v = new Form(this.params);
            // #form is the id of the element inside template where the form view will be inserted.
            this.setView("#form", form_v);
            // listen to when form view sends these events 
            // this view now does nothing till these events are triggered by the form view
            this.listenTo(form_v, 'save_clicked', this.on_save);
            this.listenTo(form_v, 'button2_clicked', this.on_button2);
        },

        // Called when form view triggers save_clicked event(triggered after form has been converted to json, json has been cleaned and denormalised). 
        // Identifies type of final_json and saves it
        // After Save is finished calls an after_form_save function
        on_save: function(e) {
            //event contains the form view object itself
            // Set the count of successful and failed saves. These are later used to give notifications
            counts_success = new Object();
            counts_failure = new Object();
            
            // Reset the notification messages because if the person is adding multiple persons, the message does not get duplicated
            message_combined_failure=""
            message_combined_success=""
            this.form = e.context; 
            console.log("FORMCONTROLLER: cleaned, denormalised json from form.js-" + JSON.stringify(this.form.final_json));
            var that = this;
            //stores dfds of all objects bieng saved in this form - form is completely saved when all dfd in this list are resolved
            var save_complete_dfds = []; 

            if (this.form.bulk) {
                // Save each object in bulk form individually
                $.each(this.form.final_json.bulk, function(ind, obj) {
                    // index is maintained in each object to find its location on the form
                    var bulk_index = obj.index;
                    delete obj.index;
                    // save the object
                    var save_object_dfd = that.save_object(obj, that.form.bulk.foreign_fields, that.form.entity_name);
                    save_object_dfd
                        .fail(function(error) {
                            // error while saving object
                            // show the error on the form right above the object
                            that.form.show_errors(that.convert_to_row_error(error, that.form.entity_name, bulk_index));
                        });
                    // put dfd for this object-save in the save_complete_dfds list
               
                    save_object_dfd.done(function(){
                        //When the saving is done, add the notification.
                        notifs_view.add_alert({
                        notif_type: "success",
                        message: message_combined_success});
                    });
                    save_complete_dfds.push(save_object_dfd);
                });
            } 
            else 
            {
                //normal or inlines
                
                if (this.form.inline) {
                    // its an inline form
                    console.log("FORMCONTROLLER: separating inlines from final json");
                    // list of all inlines
                    this.inline_models = this.form.final_json.inlines;
                    //separate inlines from final json - since they would be saved separately
                    delete this.form.final_json.inlines;
                    // add a dummy dfd for inlines - resolve it when inlines have been saved
                    var inlines_dfd = new $.Deferred();
                    save_complete_dfds.push(inlines_dfd);
                }
                // save the normal form object or the inline parent form
                var save_object_dfd = this.save_object(this.form.final_json, this.form.foreign_entities, this.form.entity_name);
                save_object_dfd
                    .done(function(off_json) {
                        // parent form saved
                        if (that.form.inline)
                            //If inline form - save inlines now
                            that.save_inlines(that.inline_models, off_json, that.form.inline)
                                .done(function(all_inlines) {
                                    console.log("ALL INLINES SAVED");
                                    inlines_dfd.resolve(all_inlines);
                                    
                                })
                                .fail(function() {
                                    console.log("FAILED AT INLINES SAVE");
                                    show_inline_error();
                                    inlines_dfd.reject();
                                });
                    })
                    .fail(function(error) {
                        that.form.show_errors(error);
                    });
                save_complete_dfds.push(save_object_dfd);
            }

            //When all objects in form are saved...
            $.when.apply(null, save_complete_dfds)
                .done(function() {
                    console.log("Everything saved");
                    that.after_form_save(that.form.entity_name);
                    if (message_combined_success!="")
                    {
                        notifs_view.add_alert({
                            notif_type: "success",
                            message: message_combined_success});
                    }
                })
                .fail(function() {
                    if (that.form.bulk)
                        show_bulk_error();
                    if (message_combined_success!="")
                        notifs_view.add_alert({
                            notif_type: "success",
                            message: message_combined_success});

                    notifs_view.add_alert({
                        notif_type: "error",
                        message: message_combined_failure
                    });
                });

            //shown if any inline could not be saved
            function show_inline_error() {
                var err = {};
                err[that.form.entity_name] = {
                    __all__: ["Some " + that.form.inline.entity + " (in red below) could not be saved. To correct errors and try saving them again - go to list page and edit this " + that.form.entity_name]
                };
                that.form.show_errors(err, true);
            };

            //shown if any bulk could not be saved
            function show_bulk_error() {
                var err = {};
                err[that.form.entity_name] = {
                    __all__: ["Some " + that.form.entity_name + " (in red below) could not be saved. To correct errors and try saving them again - open a new add form"]
                };
                that.form.show_errors(err, true);
            };
        },

        //converts the error for an inline/bulk into a format which makes it show up at its own row
        convert_to_row_error: function(error, row_entity_name, row_index) {
            error = $.parseJSON(error);
            error["row" + row_index] = error[row_entity_name];
            delete error[row_entity_name];
            return error;
        },
        
        // iterates over the inlines list and saves them serially
        save_inlines: function(inlines, parent_off_json, inline_config) {
            var dfd = new $.Deferred();
            var that = this;
            this.complete_inlines(inlines, parent_off_json, inline_config);
            iterate_inlines();
            return dfd;

            //saves inlines serially    
            function iterate_inlines() {
                if (!inlines.length)
                    return dfd.resolve();
                save_inline(inlines.shift())
                    .done(function() {
                        iterate_inlines();
                    })
                    .fail(function() {
                        dfd.reject();
                    });
            };
            // saves an inline
            function save_inline(inl) {
                var inl_dfd = $.Deferred();
                // index maintained to find its location on the form
                var inl_index = inl.index;
                delete inl.index;
                that.save_object(inl, inline_config.foreign_entities, inline_config.entity)
                    .fail(function(error) {
                        that.form.show_errors(that.convert_to_row_error(error, inline_config.entity, inl_index));
                        return inl_dfd.reject();
                    })
                    .done(function() {
                        return inl_dfd.resolve();
                    });
                return inl_dfd.promise();
            };
        },

        //put in the borrowed attributes and the joining attribute in inlines from the parent form
        complete_inlines: function(inlines, parent_off_json, inline_config) {
            var host_attr_json = {};
            // get the host attr from parent object
            host_attr_json[inline_config.joining_attribute.inline_attribute] = {}
            _.each(inline_config.joining_attribute.host_attribute, function(attr, index) {
                host_attr_json[inline_config.joining_attribute.inline_attribute][attr] = parent_off_json[attr];
            }, this);

            // get the borrowed attrs from parent object
            var borr_json = {}
            $.each(inline_config.borrow_attributes, function(index, b_attr) {
                borr_json[b_attr.inline_attribute] = parent_off_json[b_attr.host_attribute];
            });
            
            // substitute the host and borrowed attributes in each inline
            _.each(inlines, function(inl, index) {
                console.log("inl before extension - " + JSON.stringify(inl));
                $.extend(true, inl, host_attr_json);
                $.extend(true, inl, borr_json);
                console.log("inl after extension - " + JSON.stringify(inl));
            });
        },
        
        // save an object depending upon the internet connectivity of user
        save_object: function(json, foreign_entities, entity_name) {
            var dfd = new $.Deferred();
            var that = this;
            if (this.is_uploadqueue_empty() && this.is_internet_connected()) {
                //Online mode
                // convert namespace of object from offline to online
                ConvertNamespace.convert(json, foreign_entities, "offlinetoonline")
                    .done(function(on_off_jsons) {
                        // save in online mode
                        that.save_when_online(entity_name, on_off_jsons)
                            .done(function(off_json) {
                                // call any user defined after-save
                                call_after_save(off_json)
                                    .done(function() {
                                        // successfully saved
                                        show_suc_notif();
                                        dfd.resolve(off_json);
                                    })
                                    .fail(function(error) {
                                        // user defined after-save failed
                                        alert("afterSave failed for entity - " + entity_name + " - " + error);
                                    });
                            })
                            .fail(function(error) {
                                // error saving the object
                                // show error on form
                                show_err_notif();
                                dfd.reject(error);
                            });
                    })
                    .fail(function(error) {
                        // namespace conversion failed
                        show_err_notif();
                        return dfd.reject(error);
                    });
            } else {
                //Offline mode
                // save in offline mode
                this.save_when_offline(entity_name, json)
                    .done(function(off_json) {
                        // call any user defined after-save
                        call_after_save(off_json)
                            .done(function() {
                                // successfully saved
                                show_suc_notif();
                                dfd.resolve(off_json);
                            })
                            .fail(function(error) {
                                // user defined after-save failed
                                alert("afterSave failed for entity - " + entity_name + " - " + error);
                            });
                    })
                    .fail(function(error) {
                        // error saving the object
                        // show error on form
                        show_err_notif();
                        return dfd.reject(error);
                    });
            }
            
            function call_after_save(saved_off_json) {
                var dfd = new $.Deferred();
                // get the user defined after-save for this entity
                var afterSave = configs[entity_name].afterSave;
                if (afterSave)
                    afterSave(saved_off_json, Offline)
                        .done(function() {
                            dfd.resolve();
                        })
                        .fail(function(error) {
                            dfd.reject(error);
                        });
                else dfd.resolve();
                return dfd.promise();
            };

            function show_suc_notif() {
               
               // function counts the successful operations and creates the notification message. Has to be done BEFORE the notification is added, hence here.
                console.log(message_combined_success);
                if (counts_success.hasOwnProperty(entity_name)){
                    counts_success[entity_name] +=1;
                }
                else
                {
                    counts_success[entity_name] = 1;
                }
                message_combined_success="";
                for (var title in counts_success)
                {
                    if (counts_success[title]>0)
                        message_combined_success = message_combined_success + "<br>" + "Saved " + counts_success[title] + " " +title;
                }       
            };

            function show_err_notif() {
            // function counts the errors and creates the notification message
               if (counts_failure.hasOwnProperty(entity_name)){
                    counts_failure[entity_name] +=1;
                }
                else{
                    counts_failure[entity_name] = 1;
                }
                message_combined_failure="";
                for (var title in counts_failure)
                {
                    if (counts_failure[title]>0)
                        message_combined_failure = message_combined_failure + "<br>" + "Error saving " + counts_failure[title] + " " +title;

                }
            };
            return dfd.promise();
        },

        // saves the object in offline mode - in offline db and uploadQ
        save_when_offline: function(entity_name, off_json) {
            var dfd = new $.Deferred();
            var action, that = this;
            if (off_json.id)
                action = "E"
            else
                action = "A"

            // save in offline db and then the uploadQ
            Offline.save(null, entity_name, off_json)
                .done(function(off_m) {
                    // succesfully saved in offline db
                    console.log("SAVED IN OFFLINE - " + JSON.stringify(off_m.toJSON()));
                    upload_collection.create({
                        data: off_m.toJSON(),
                        action: action,
                        entity_name: entity_name
                    }, {
                        success: function(u_model) {
                            // successfully saved in uploadQ
                            console.log("FORMCNTROLLER: model added to uploadqueue - " + JSON.stringify(u_model.toJSON()));
                            return dfd.resolve(off_m.toJSON());
                        },
                        error: function(error) {
                            // failed to save in uploadQ
                            alert("Unexepected Error- error adding model to uploadqueue");
                            //TODO: Unexpected but should delete the model from offline db as well?
                            return dfd.reject(error);
                        }
                    });
                })
                .fail(function(error) {
                    // failed to save in offline db - return the error
                    return dfd.reject(error);
                });

            return dfd.promise();
        },

        // saves the object in online mode - on the server and then the offline db
        save_when_online: function(entity_name, on_off_jsons) {
            var dfd = new $.Deferred();
            var on_json = on_off_jsons.on_json;
            var off_json = on_off_jsons.off_json
            console.log("FORMCONTROLLER: Got this json to save online - " + JSON.stringify(on_json));
            var that = this;
            //if edit case, substitute id with online id TODO: move it to convertnamespace?
            if (off_json.id) {
                on_json.id = parseInt(off_json.online_id);
                delete on_json.online_id;
            }
            // save on server
            Online.save(null, entity_name, on_json)
                .done(function(on_m) {
                    // successfully saved on server
                    console.log("SAVED IN ONLINE - " + JSON.stringify(on_m.toJSON()));
                    // inject the online id returned by server in the offline object
                    off_json.online_id = parseInt(on_m.get("id"));
                    // save offline object in offline db
                    Offline.save(null, entity_name, off_json)
                        .done(function(off_m) {
                            // successfully saved in offline and online
                            console.log("SAVED IN OFFLINE - " + JSON.stringify(off_m.toJSON()));
                            return dfd.resolve(off_m.toJSON());
                        })
                        .fail(function(error) {
                            //TODO: what to do abt the model just saved on server? 
                            return dfd.reject(error);
                        });
                })
                .fail(function(xhr) {
                    // failed to save on server - return the error
                    return dfd.reject(xhr.responseText);
                });
            return dfd.promise();
        },
        
        // checks whether the uploadQ is empty or not
        is_uploadqueue_empty: function() {
            console.log("FORMCONTROLLER: length of upload_collection - " + upload_collection.length);
            console.log(upload_collection);

            return upload_collection.length <= 0;
        },

        // checks whther internet is available
        is_internet_connected: function() {
            return navigator.onLine;
        },
        
        // button2 is made null - so this is nevr used 
        on_button2: function(e) {
            console.log("FORMCONTROLLER: Button 2 clicked on form");
        },
        
        // route to a fresh add form for this entity
        after_form_save: function(entity_name) {
            window.Router.navigate(entity_name + '/add');
            //since may already be on the add page, therefore have to call this explicitly
            window.Router.add(entity_name); 
        }




    });

    // Our module now returns our view
    return FormControllerView;
});

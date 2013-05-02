define(['jquery', 'underscore', 'backbone', 'form_field_validator', 'syphon', 
    'views/notification', 'indexeddb_backbone_config', 'configs', 'views/form', 'collections/upload_collection', 'offline_to_online'
// Using the Require.js text! plugin, we are loaded raw text
// which will be used as our views primary template
// 'text!templates/project/list.html'
], function($, pas, pass, pass, pass, notifs_view, indexeddb, configs, Form, upload_collection, OfflineToOnline) {

    // FormController: Brings up the Add/Edit form
    
    /*
    If we are saving offline - we set the json from the form, (we denormalize it), save it in the model and save the model in the upload queue.
    If we are saving online - we set the json from the form, (we denormalize it), we convert foreign keys ids to the online namespace, save the offline model, and then save it on server.
    If server save succeeds, then we set the online_id in the offline model.
    */
    
    
    var FormControllerView = Backbone.Layout.extend({

        initialize: function(params) {
            console.log("FORMCONTROLLER: initializing a new object");
            this.params = params;
            console.log(this.params);
            console.log("FORMCONTROLLER: upload_collection recvd - ")
            console.log(upload_collection.models);   
            _(this)
                .bindAll('on_save');
            _(this)
                .bindAll('on_button2');
            _(this)
                .bindAll('json_converted');
            $(document)
                .on("save_clicked", this.on_save);
            $(document)
                .on("button2_clicked", this.on_button2);
             

        },
        template: "<div><div id = 'form'></div></div>",
        
        beforeRender: function() {
            // #form is the id of the element inside in template where the new view will be inserted.
            this.setView("#form", new Form(this.params));
            

        },
        error_notif_template: _.template($('#' + 'error_notifcation_template').html()),
            
        json_converted: function(something){
            console.log("Gotcha B****: conv json");
            console.log(something);
            this.after_offline_to_online_success(something.on_json, something.off_json)
        },    

        on_save: function(e) {
            e.stopPropagation();
            console.log("ADD/EDIT: Save clicked on form - ");
            // console.log(e);
            this.form = e.context; // form_view
            console.log("FORMCONTROLLER: cleaned, denormalised json from form.js-"+JSON.stringify(this.form.final_json));
            
            //TODO: if inline present, separate it
            
            if(this.form.inline)
            {
                console.log("FORMCONTROLLER: separating inlines from final json");
                this.inline_models = $.extend(null,this.form.final_json.inlines);
                delete this.form.final_json.inlines;
                console.log(this.inline_models);
                // $.each(this.inline_models,function(index, imodel){
//                     console.log(imodel);
//                 });
            }
            
            this.form.offline_model.set(this.form.final_json);
            var that = this; // Please change to form_controller or something else which makes the content clear.
            this.offline_m = this.form.offline_model; // Remove this line
            if(that.is_uploadqueue_empty() && that.is_internet_connected())
            {
                console.log("FORMCONTROLLER: the uploadqueue is empty and internet connected");
                //TODO: SAve on server, 
                //TODO: get the online id  
                //TODO: save online_id in offline model
                //TODO: offline to online
                if(this.form.bulk)
                {
                    $.each(this.form.final_json.bulk, function(ind, obj){
                        // that.listenTo(OfflineToOnline, 'converted', that.json_converted);
                        // OfflineToOnline.convert(obj, that.form.bulk.foreign_fields);
                        OfflineToOnline.convert(obj, that.form.bulk.foreign_fields).then(that.json_converted);
                    });
                }
                else
                {
                    // that.offline_to_online(this.form.final_json); // If offline to online conversion succeds, then we save it to offline db. If this is succesful, then save it on server, then get online id from the server and set it on the offline object. If there is an error, then ?
                    // this.listenTo(OfflineToOnline, 'converted', this.json_converted);
                    // OfflineToOnline.convert(this.form.final_json,this.form.foreign_entities)
                    OfflineToOnline.convert(this.form.final_json,this.form.foreign_entities).then(this.json_converted);
                    
                }
                // Error callbacks???
            }
            else
            {
                //put into uploadqueue. save it in the offline db and upload Q.
                // Offline save
                if(this.form.bulk)
                {
                    console.log("FORMCONTROLLER: ITS A BULK");
                    this.bulk_jsons = this.form.final_json.bulk;
                    $.each(this.bulk_jsons,function(index, ijson){
                        console.log(ijson);
                        var generic_model_offline = Backbone.Model.extend({
                            database: indexeddb,
                            storeName: that.form.entity_name, // add attribute name
                            action: "A"    
                        });
                        var i_model = new generic_model_offline();
                        i_model.set(ijson);
                        i_model.save(null,{
                            success: function(in_model){
                                console.log("FORMCONTROLLER: bulk model saved offline - "+JSON.stringify(in_model.toJSON()));
                                upload_collection.create(
                                    {
                                        data: in_model.toJSON(),
                                        action: in_model.action,   
                                        entity_name: that.form.entity_name        
                                    },
                                    {
                                        success:function(u_model){
                                            console.log("FORMCNTROLLER: model added to uploadqueue - "+JSON.stringify(u_model.toJSON()));
                                            $(notifs_view.el)
                                                .append(that.error_notif_template({
                                                msg: "Success! Model saved offline and added to uploadqueue"
                                            }));
                                        },
                                        error: function(u_model){
                                            console.log("FORMCNTROLLER: Unexepected Error- error adding model to uploadqueue - "+JSON.stringify(u_model.toJSON()));
                
                                        }    
                                    }
                                );            
                            },
                            error: function(error){
                                console.log("FORMCONTROLLER: error saving inline model");
                                console.log(error);
                            }    
                        });
                    });
                    return;
                }
                this.offline_m.save(null,{ // already set the json upstairs
                    success: function(model){
                        console.log("FORMCONTROLLER:ON_SAVE: model saved in offline");
                        console.log(model);
                        console.log("FORMCONTROLLER: Can not save online. Putting in uploadqueue");
                        upload_collection.create(
                            {
                                data:model.toJSON(),
                                action: that.form.action,
                                entity_name: that.form.entity_name        
                            },
                            {
                                success: function(u_model){
                                    console.log("FORMCNTROLLER: model added to uploadqueue - "+JSON.stringify(u_model.toJSON()));
                                    
                                    // Save inlines
                                    if(that.form.inline)
                                    {
                                        console.log("FORMCONTROLLER: saving inlines");
                                        var for_attr = {};
                                        $.each(that.form.inline.foreign_attribute.host_attribute,function(index, obj){
                                           for_attr[obj] = model.get(obj);
                                           console.log(obj);
                                           console.log(model[obj]);
                                        });
                                        $.each(that.inline_models,function(index, ijson){
                                            console.log(ijson);
                                            var generic_model_offline = Backbone.Model.extend({
                                                database: indexeddb,
                                                storeName: that.form.inline.entity, // add attribute name
                                                action: "A"    
                                            });
                                            var i_model = new generic_model_offline();
                                            i_model.set(ijson);
                                            i_model.set(that.form.inline.foreign_attribute.inline_attribute, for_attr);
                                            var i_model_action = "A";
                                            if(i_model.id)
                                            {
                                                console.log("this inline has been edited");
                                                i_model_action = "E";
                                                i_model.action = "E";
                                            }
                                            i_model.save(null,{
                                                success: function(in_model){
                                                    console.log("FORMCONTROLLER: inline model saved - "+JSON.stringify(in_model.toJSON()));
                                                    upload_collection.create(
                                                        {
                                                            data: in_model.toJSON(),
                                                            action: in_model.action,   //TODO: what if grp was edited, some inlines were edited and some new created
                                                            entity_name: that.form.inline.entity        
                                                        },
                                                        {
                                                            success:function(u_model){
                                                                console.log("FORMCNTROLLER: model added to uploadqueue - "+JSON.stringify(u_model.toJSON()));
                                                            },
                                                            error: function(u_model){
                                                                console.log("FORMCNTROLLER: Unexepected Error- error adding model to uploadqueue - "+JSON.stringify(u_model.toJSON()));
                                    
                                                            }    
                                                        }
                                                    );            
                                                },
                                                error: function(error){
                                                    console.log("FORMCONTROLLER: error saving inline model");
                                                    console.log(error);
                                                }    
                                            });
                                            
                            
                                        });
                                        
                                    }
                                    ///////////////////////////////////////////////////////////////////////////////////////////////
                                    $(notifs_view.el)
                                        .append(that.error_notif_template({
                                        msg: "Success! Model saved offline and added to uploadqueue"
                                    }));
                                },
                                error: function(model){
                                    console.log("FORMCNTROLLER: Unexepected Error- error adding model to uploadqueue - "+JSON.stringify(model.toJSON()));
                                    // that.form.show_errors("Unexepected Error- error adding model to uploadqueue")
                                    alert("unepected error. check log");
                                    $(notifs_view.el)
                                        .append(that.error_notif_template({
                                        msg: "Error adding model to uploadqueue"
                                    }));
                                }    
                                    
                            }
                        );        
                    
                    },
                    error: function(){
                        console.log("FORMCONTROLLER:ON_SAVE: Unexpected Error - error saving the model offline.")
                        // that.form.show_errors("Unexepected Error- error saving the model offline")
                        alert("Unexpected error. Check log");
                        $(notifs_view.el)
                            .append(that.error_notif_template({
                            msg: "Error saving the model offline"
                        }));
                    }        
                });
                
                
            }
            
            
        },
            
        after_offline_to_online_success: function(o_json, off_json){ // call this send_to_server
            console.log("FORMCONTROLLER: Got this json to save online - "+JSON.stringify(o_json));
            var that = this;
            if(this.form.bulk)
            {
                var generic_model_offline = Backbone.Model.extend({
                    database: indexeddb,
                    storeName: that.form.entity_name, // add attribute name
                });
                var generic_model_online = Backbone.Model.extend({
                    sync: Backbone.ajaxSync,
                    url: function() {
                        return this.id ? that.params.initialize.view_configs.rest_api_url + this.id + "/" : that.params.initialize.view_configs.rest_api_url;
                    },
                });
                var b_model_offline = new generic_model_offline();
                var b_model_online = new generic_model_online();
            
                b_model_online.set(o_json);
                b_model_online.save(null, {
                    success: function(on_model){
                        console.log("FRMCONTROLLER: online model after save - " + JSON.stringify(on_model.toJSON()));
                        b_model_offline.set(off_json);
                        b_model_offline.set('online_id',parseInt(on_model.get("id")));
                        b_model_offline.save(null,{
                            success: function(off_model){
                                console.log("FRMCONTROLLER: offline model after evrthing-" + JSON.stringify(off_model.toJSON()));
                                console.log("FRMCONTROLLER: Successfuly saved on server and offline.");
                                $(notifs_view.el)
                                    .append(that.error_notif_template({
                                    msg: "Success! Saved on server and offline"
                                }));    
                            },
                            error: function(){
                                console.log("FORMCONTROLLER:ON_SAVE: Unexpected Error - error saving the model offline.");
                                // that.form.show_errors("Unexepected Error- error saving the model offline");
                                $(notifs_view.el)
                                    .append(that.error_notif_template({
                                    msg: "Error saving the model offline"
                                }));
                            }    
                        });
                        
                    },
                    error: function(model,xhr,options){
                        console.log("error saving a bulk model on server");
                        $(notifs_view.el)
                            .append(that.error_notif_template({
                            msg: "Error saving the model on server"
                        }));
                        that.form.show_errors(xhr.responseText);
                            
                       
                    }    
                });
                
                
                return;    
            }
            
            var that = this;
            var generic_model_online = Backbone.Model.extend({
                sync: Backbone.ajaxSync,
                url: function() {
                    return this.id ? that.params.initialize.view_configs.rest_api_url + this.id + "/" : that.params.initialize.view_configs.rest_api_url;
                },
            });
            var upload_online_model = new generic_model_online();
            
            this.offline_m.save(null,{
                success: function(model){ // please change this to offline_model
                    console.log("FORMCONTROLLER:ON_SAVE: model saved in offline - "+JSON.stringify(model.toJSON()));
                    upload_online_model.set(o_json);
                    if(that.form.action == "A")
                    {
                        upload_online_model.unset('id');
                    }
                    else
                    {
                        upload_online_model.set('id', parseInt(model.get('online_id')));
                        upload_online_model.unset('online_id');
                    
                    }
                    console.log("FRMCONTROLLER: upload online model set - " + JSON.stringify(upload_online_model.toJSON()));
                    console.log("FRMCONTROLLER: upload online model save called.");
                    upload_online_model.save(null, {
                        async: false,
                        success: function(online_model) {
                            console.log("FRMCONTROLLER: online model after save - " + JSON.stringify(upload_online_model.toJSON()));

                            // set online id in offline model
                            model.set('online_id', upload_online_model.get("id"));
                            model.save(null, {
                                success: function(model) {
                                    console.log("FRMCONTROLLER: offline model after evrthing-" + JSON.stringify(model.toJSON()));
                                    console.log("FRMCONTROLLER: Successfuly saved on server and offline.")
                                        
                                        
                                    ///saving inline models
                                    if(that.form.inline)
                                    {
                                        console.log("FORMCONTROLLER: saving inlines");
                                        ////////////////////creating foreign atrribute for inlines///////////////////
                                        var for_attr = {};
                                        $.each(that.form.inline.foreign_attribute.host_attribute,function(index, obj){
                                           for_attr[obj] = model.get(obj);
                                        });
                                        var for_attr_online = {};
                                        $.each(that.form.inline.foreign_attribute.host_attribute,function(index, obj){
                                           for_attr_online[obj] = online_model.get(obj);
                                        });
                                        /////////////////////////////////////////////////////////////////////////////
                                        $.each(that.inline_models,function(index, ijson){
                                            /////////////////creating offline model for inline/////////////////
                                            var generic_model_offline = Backbone.Model.extend({
                                                database: indexeddb,
                                                storeName: that.form.inline.entity, // add attribute name
                                            });
                                            var generic_model_online = Backbone.Model.extend({
                                                sync: Backbone.ajaxSync,
                                                url: function() {
                                                    return this.id ? configs[that.form.inline.entity].rest_api_url + this.id + "/" : configs[that.form.inline.entity].rest_api_url;
                                                },
                                            });
                                            var i_model = new generic_model_offline();
                                            var i_model_online = new generic_model_online();
                                            //////////////////////////////////////////////////////////////////
                                            
                                            if(ijson.id)
                                            {
                                                /////////setting the offline json on model and saving it/////////
                                                i_model.set("id",ijson.id);
                                                i_model.fetch({
                                                    success: function(off_in_model){
                                                        prev_json = off_in_model.toJSON();
                                                        ijson = $.extend(prev_json, ijson);
                                                        off_in_model.set(ijson);
                                                        off_in_model.set(that.form.inline.foreign_attribute.inline_attribute, for_attr);
                                                        //////////starts here
                                                        off_in_model.save(null,{
                                                            success: function(in_model){
                                                                console.log("FORMCONTROLLER: inline saved offline- "+JSON.stringify(in_model.toJSON()));
                                                                i_model_online.set(ijson);
                                                                i_model_online.set(that.form.inline.foreign_attribute.inline_attribute, for_attr_online);
                                                    
                                                            //replacing borrowed attributes with online-converted attributes from online model//
                                                                $.each(that.form.inline.borrow_attributes,function(index,b_attr){
                                                                    i_model_online.set(b_attr.inline_attribute, online_model.get(b_attr.host_attribute));    
                                                                });
                                                                i_model_online.set("id", parseInt(i_model_online.get("online_id")));
                                                                i_model_online.unset("online_id");
                                                            ////////////////////////////////////////////////////////////////////
                                                                i_model_online.save(null,{
                                                                    success: function(on_in_model){
                                                                        console.log("FORMCONTROLLER: inline saved online - "+JSON.stringify(on_in_model.toJSON()));
                                                                        i_model.set('online_id', on_in_model.get("id"));
                                                                        i_model.save(null, {
                                                                            success: function(model) {
                                                                                console.log("FRMCONTROLLER: inline offline model after evrthing-" + JSON.stringify(model.toJSON()));
                                                                                console.log("FRMCONTROLLER: Inline model Successfuly saved on server and offline.");
                                    
                                                                            },
                                                                            error: function(){
                                                                                console.log("ERROR:FRMCONTROLLER: Unexpected error.Couldn't save offline model.The offline model's online id could not be set.");
                                                                                // that.form.show_errors("Unexepected Error- error saving the model offline");
                                                                                $(notifs_view.el)
                                                                                    .append(that.error_notif_template({
                                                                                    msg: "Error setting onlineid of offline model"
                                                                                }));
                                                                    
                                                                            }        
                                                                        });    
                                                                    },
                                                                    error: function(){
                                                                        console.log("error saving inline online");
                                                                    }    
                                                                });    
                                                            },
                                                            error: function(error){
                                                                console.log("FORMCONTROLLER: error saving inline model");
                                                                console.log(error);
                                                            }    
                                                        });
                                                        
                                                        //////ends here
                                                    },
                                                    error: function(err){
                                                        console.log("ERROR:FORMCONTROLLER: Unexpected error. The inline model edited could not be fetched - "+err);
                                                                        
                                                    }        
                                                })
                                                
                                            }
                                            else{
                                                /////////setting the offline json on model and saving it/////////
                                                i_model.set(ijson);
                                                i_model.set(that.form.inline.foreign_attribute.inline_attribute, for_attr);
                                                i_model.save(null,{
                                                    success: function(in_model){
                                                        console.log("FORMCONTROLLER: inline model saved - "+JSON.stringify(in_model.toJSON()));
                                                        i_model_online.set(ijson);
                                                        i_model_online.set(that.form.inline.foreign_attribute.inline_attribute, for_attr_online);
                                                    
                                                    //replacing borrowed attributes with online-converted attributes from online model//
                                                        $.each(that.form.inline.borrow_attributes,function(index,b_attr){
                                                            i_model_online.set(b_attr.inline_attribute, online_model.get(b_attr.host_attribute));    
                                                        });
                                                    ////////////////////////////////////////////////////////////////////////////    
                                                        i_model_online.save(null,{
                                                            success: function(on_in_model){
                                                                console.log("inline saved online - "+JSON.stringify(on_in_model.toJSON()));
                                                                i_model.set('online_id', on_in_model.get("id"));
                                                                i_model.save(null, {
                                                                    success: function(model) {
                                                                        console.log("FRMCONTROLLER: inline offline model after evrthing-" + JSON.stringify(model.toJSON()));
                                                                        console.log("FRMCONTROLLER: Inline model Successfuly saved on server and offline.");
                                    
                                                                    },
                                                                    error: function(){
                                                                        console.log("ERROR:FRMCONTROLLER: Unexpected error.Couldn't save offline model.The offline model's online id could not be set.");
                                                                        // that.form.show_errors("Unexepected Error- error saving the model offline");
                                                                        $(notifs_view.el)
                                                                            .append(that.error_notif_template({
                                                                            msg: "Error setting onlineid of offline model"
                                                                        }));
                                                                    
                                                                    }        
                                                                });    
                                                            },
                                                            error: function(){
                                                                console.log("error saving inline online");
                                                            }    
                                                        });    
                                                    },
                                                    error: function(error){
                                                        console.log("FORMCONTROLLER: error saving inline model");
                                                        console.log(error);
                                                    }    
                                                });
                                            }
                                            ///////////////////////////////////////////////////////////////////////
                                        });
                                    }
                                    
                                    //////////////////////////////////////////////////////////////////////////////////////////////    
                                        
                                    $(notifs_view.el)
                                        .append(that.error_notif_template({
                                        msg: "Success! Saved on server and offline"
                                    }));    
                                },
                                error: function() {
                                    //ToDO: error handling
                                    console.log("ERROR:FRMCONTROLLER: Unexpected error.Couldn't save offline model.The offline model's online id could not be set.");
                                    // that.form.show_errors("Unexepected Error- error saving the model offline");
                                    $(notifs_view.el)
                                        .append(that.error_notif_template({
                                        msg: "Error setting onlineid of offline model"
                                    }));
                        
                                }
                            });
                        },
                        error: function(model, xhr, options){
                            console.log("FORMCONTROLLER:ADD: Error saving model on server ");
                            that.form.show_errors(xhr.responseText);
                            $(notifs_view.el)
                                .append(that.error_notif_template({
                                msg: "Error saving the model on server"
                            }));
                            
                            
                        }
                           
                    });
            
                    
                },
                error: function(){
                    console.log("FORMCONTROLLER:ON_SAVE: Unexpected Error - error saving the model offline.");
                    // that.form.show_errors("Unexepected Error- error saving the model offline");
                    $(notifs_view.el)
                        .append(that.error_notif_template({
                        msg: "Error saving the model offline"
                    }));
                    alert("Unexpected error. Check log");
                }        
            });
                       
                        
        },    
        
        is_uploadqueue_empty : function(){
            console.log("FORMCONTROLLER: length of upload_collection - "+upload_collection.length);
            console.log(upload_collection);
                
            return upload_collection.length<=0;    
        },
        
        is_internet_connected : function(){
            return navigator.onLine;
        },       
            

        on_button2: function(e) {
            e.stopPropagation();
            console.log("FORMCONTROLLER: Button 2 clicked on form");
        }




    });

    // Our module now returns our view
    return FormControllerView;
});

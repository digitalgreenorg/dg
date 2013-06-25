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

        },
        template: "<div><div id = 'form'></div></div>",
        
        beforeRender: function() {
            // #form is the id of the element inside in template where the new view will be inserted.
            var form_v = new Form(this.params);
            this.setView("#form", form_v);
            this.listenTo(form_v, 'save_clicked', this.on_save);
            this.listenTo(form_v, 'button2_clicked', this.on_button2);
        },
        
        /*Called when form view sends save_clicked event. 
        Identifies type of final_json and saves it
        After Save is finished calls an after_save function
        */
        //form.inline, bulk, final_json, foreign_fields, entity_name, 
        on_save: function(e) {
            this.form = e.context;  //event contains the form view object itself
            console.log("FORMCONTROLLER: cleaned, denormalised json from form.js-"+JSON.stringify(this.form.final_json));
            //separate inlines from final json
            if(this.form.inline)
            {
                console.log("FORMCONTROLLER: separating inlines from final json");
                this.inline_models = $.extend(null,this.form.final_json.inlines);
                delete this.form.final_json.inlines;
            }
            ////////////////////////////////////////////////////////////////////////////////////////////////////
            
            var that = this; 
            var save_complete_dfds = [];    //stores dfds of all objects bieng saved in this form
            if(this.form.bulk)
            {
                /*Save each object in bulk form individually*/
                $.each(this.form.final_json.bulk, function(ind, obj){
                    var save_object_dfd = that.save_object(obj, that.form.bulk.foreign_fields, that.form.entity_name);
                    save_object_dfd
                        .done(function(msg){
                            notifs_view.add_alert({
                                notif_type: "success",
                                message: msg
                            });
                        })
                        .fail(function(error){
                            notifs_view.add_alert({
                                notif_type: "error",
                                message: error
                            });    
                        });
                    save_complete_dfds.push(save_object_dfd);
                });
            }
            else
            {
                var save_object_dfd = this.save_object(this.form.final_json, this.form.foreign_entities, this.form.entity_name);
                save_object_dfd
                    .done(function(msg){
                        notifs_view.add_alert({
                            notif_type: "success",
                            message: msg
                        });
                    })
                    .fail(function(error){
                        notifs_view.add_alert({
                            notif_type: "error",
                            message: error
                        });    
                    });
                save_complete_dfds.push(save_object_dfd);                                
            }
            
            //When all objects in form are saved...
            $.when.apply($,save_complete_dfds)
                .done(function(){
                    that.after_save(that.form.entity_name);
                })
        },
        
        save_object: function(json, foreign_entities, entity_name){
            //TODO: check mode and call corresponding func
            var dfd = new $.Deferred();
            var that =  this;
            if(this.is_uploadqueue_empty() && this.is_internet_connected())
            {
                //Online mode
                ConvertNamespace.convert(json, foreign_entities, "offlinetoonline")
                    .done(function(on_off_jsons){
                        that.save_when_online(on_off_jsons)
                            .done(function(msg){
                                dfd.resolve(msg);
                            })
                            .fail(function(error){
                                dfd.reject(error);
                            });                            
                    })
                    .fail(function(){
                        return dfd.reject("Failed to save "+entity_name+". ConvertNamespace Failed.");
                    });
            }
            else
            {
                //Offline mode
                this.save_when_offline(entity_name, json)
                    .done(function(msg){
                        return dfd.resolve(msg);
                    })
                    .fail(function(err){
                        return dfd.reject(err);
                    });
            }
            return dfd.promise();
        },
        
        
        save_when_offline: function(entity_name, off_json){
            var dfd = new $.Deferred();
            var action = null;
            if(off_json.id)
                action = "E"
            else
                action = "A"
            var that = this;    
            
            Offline.save(null, entity_name, off_json)
                .done(function(off_m){
                    console.log("SAVED IN OFFLINE - "+JSON.stringify(off_m.toJSON()));
                    upload_collection.create(
                        {
                            data: off_m.toJSON(),
                            action: action,   
                            entity_name: entity_name        
                        },
                        {
                            success:function(u_model){
                                console.log("FORMCNTROLLER: model added to uploadqueue - "+JSON.stringify(u_model.toJSON()));
                                if(that.form.inline)
                                {
                                    console.log("FORMCONTROLLER: saving inlines");
                                    that.process_inlines_offline(that.form, off_m.toJSON(), that.inline_models);
                                }
                                return dfd.resolve("Saved "+entity_name+" (Local, Uploadqueue)");    
                            },
                            error: function(error){
                                console.log("FORMCNTROLLER: Unexepected Error- error adding model to uploadqueue - "+error);
                                //TODO: should delete the model from offline db as well?
                                return dfd.reject("Error saving the "+entity_name+" (Uploadqueue)");
                            }    
                    });
                })
                .fail(function(error){
                    that.form.show_errors(error);
                    return dfd.reject("Error saving the "+entity_name+" (Local)");
                });
                
            return dfd.promise();    
        },
        
        process_inlines_offline: function(form,parent_off_json,inlines){
            console.log("FORMCONTROLLER: saving inlines when offline");
            var for_attr_offline = {};
            $.each(form.inline.foreign_attribute.host_attribute,function(index, attr){
               for_attr_offline[attr] = parent_off_json[attr];
            });
            $.each(inlines,function(index, ijson){
                if(ijson.id)
                {
                    Offline.fetch_object(form.inline.entity, "id", ijson.id)  //just to preserve videos_seen
                        .done(function(off_in_model){
                            var prev_json = off_in_model.toJSON();
                            var off_ijson = $.extend(prev_json, ijson);
                            $.each(form.inline.borrow_attributes, function(index,b_attr){
                                off_ijson[b_attr.inline_attribute] = parent_off_json[b_attr.host_attribute];    
                            });
                            off_ijson[form.inline.foreign_attribute.inline_attribute] = for_attr_offline;
                            Offline.save(off_in_model,form.inline.entity,off_ijson)
                                .done(function(off_in_model){
                                    console.log("INLINE saved in offline - "+JSON.stringify(off_in_model.toJSON()));
                                    upload_collection.create(
                                        {
                                            data: off_in_model.toJSON(),
                                            action: "E",  
                                            entity_name: form.inline.entity        
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
                                })
                                .fail(function(error){
                                    console.log("FORMCONTROLLER:EDIT:SAVE:INLINE:SAVE:OFFLINE: "+error);
                                });
                        })
                        .fail(function(error){
                            console.log("FORMCONTROLLER:EDIT:SAVE:INLINE:FETCH: "+error);
                        });
                }
                else
                {
                    var off_ijson = $.extend(null, ijson);
                    $.each(form.inline.borrow_attributes, function(index,b_attr){
                        off_ijson[b_attr.inline_attribute] = parent_off_json[b_attr.host_attribute];    
                    });
                    off_ijson[form.inline.foreign_attribute.inline_attribute] = for_attr_offline;
                    Offline.save(null,form.inline.entity,off_ijson)
                        .done(function(off_in_model){
                            console.log("INLINE saved in offline - "+JSON.stringify(off_in_model.toJSON()));
                            upload_collection.create(
                                {
                                    data: off_in_model.toJSON(),
                                    action: "A",   
                                    entity_name: form.inline.entity        
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
                        })
                        .fail(function(error){
                            console.log("FORMCONTROLLER:EDIT:SAVE:INLINE:SAVE:OFFLINE: "+error);
                        });
                }
            });
        },
        
        //add_edit, entityname, inlines?_inline_models    
        save_when_online: function(on_off_jsons){ 
            var dfd = new $.Deferred();
            var on_json = on_off_jsons.on_json;
            var off_json = on_off_jsons.off_json
            console.log("FORMCONTROLLER: Got this json to save online - "+JSON.stringify(on_json));
            var that = this;
            if(that.form.action == "A")
                {
                    delete on_json.id;
                }
                else
                {
                    on_json.id = parseInt(off_json.online_id); 
                    delete on_json.online_id;
                }
            Online.save(null, that.form.entity_name, on_json)
                .done(function(on_m){
                    console.log("SAVED IN ONLINE - "+JSON.stringify(on_m.toJSON()));
                    off_json.online_id  = parseInt(on_m.get("id"));
                    Offline.save(null, that.form.entity_name, off_json)
                        .done(function(off_m){
                            console.log("SAVED IN OFFLINE - "+JSON.stringify(off_m.toJSON()));
                            if(that.form.inline)
                            {
                                console.log("FORMCONTROLLER: saving inlines");
                                that.process_inlines(that.form, off_m.toJSON(), on_m.toJSON(), that.inline_models);
                            }
                            return dfd.resolve("Saved "+that.form.entity_name + " (Server, Local)");    
                        })
                        .fail(function(error){
                            that.form.show_errors(error);
                            //TODO: what to do abt the model just saved on server? 
							return dfd.reject("Error saving the "+that.form.entity_name+" (Local)");
                        });
                })
                .fail(function(xhr){
                    that.form.show_errors(xhr.responseText);
                    return dfd.reject("Error saving the "+that.form.entity_name+" (Server)");
				});
			return dfd.promise();	 
        },        
        
        //form.inline obj, 
        process_inlines: function(form, parent_off_json, parent_on_json, inlines)
        {
            console.log("parent off json: "+JSON.stringify(parent_off_json));
            console.log("parent on json: "+JSON.stringify(parent_on_json));
            console.log("inlines: "+JSON.stringify(inlines));
            ////////////////////creating foreign atrribute for inlines///////////////////
            var for_attr_offline = {};
            $.each(form.inline.foreign_attribute.host_attribute,function(index, attr){
               for_attr_offline[attr] = parent_off_json[attr];
            });
            var for_attr_online = {};
            $.each(form.inline.foreign_attribute.host_attribute,function(index, attr){
               for_attr_online[attr] = parent_on_json[attr];
            });
            /////////////////////////////////////////////////////////////////////////////
            
            $.each(inlines,function(index, ijson){
                if(ijson.id)
                {
                    Offline.fetch_object(form.inline.entity, "id", ijson.id)  //just to get the online_id and preserve videos_seen
                        .done(function(off_in_model){
                            var prev_json = off_in_model.toJSON();
                            var off_ijson = $.extend(prev_json, ijson);
                            var on_ijson = $.extend(true,null,off_ijson);
                            $.each(form.inline.borrow_attributes, function(index,b_attr){
                                off_ijson[b_attr.inline_attribute] = parent_off_json[b_attr.host_attribute];    
                                on_ijson[b_attr.inline_attribute] = parent_on_json[b_attr.host_attribute];    
                            });
                            off_ijson[form.inline.foreign_attribute.inline_attribute] = for_attr_offline;
                            on_ijson[form.inline.foreign_attribute.inline_attribute] = for_attr_online;
                            on_ijson.id = parseInt(on_ijson.online_id);
                            delete on_ijson.online_id;
                            Online.save(null,form.inline.entity,on_ijson)
                                .done(function(on_in_model){
                                    console.log("INLINE saved in online - "+JSON.stringify(on_in_model.toJSON()));
                                    Offline.save(off_in_model,form.inline.entity,off_ijson)
                                        .done(function(off_in_model){
                                            console.log("INLINE saved in offline - "+JSON.stringify(off_in_model.toJSON()));
                                        })
                                        .fail(function(error){
                                            console.log("FORMCONTROLLER:EDIT:SAVE:INLINE:SAVE:OFFLINE: "+error);
                                        });
                                })
                                .fail(function(error){
                                    console.log("FORMCONTROLLER:EDIT:SAVE:INLINE:SAVE:ONLINE: "+error);
                                });
                        })
                        .fail(function(error){
                            console.log("FORMCONTROLLER:EDIT:SAVE:INLINE:FETCH: "+error);
                        });
                }
                else
                {
                    var off_ijson = $.extend(null, ijson);
                    var on_ijson = $.extend(true, null, ijson);
                    $.each(form.inline.borrow_attributes, function(index,b_attr){
                        off_ijson[b_attr.inline_attribute] = parent_off_json[b_attr.host_attribute];    
                        on_ijson[b_attr.inline_attribute] = parent_on_json[b_attr.host_attribute];    
                    });
                    off_ijson[form.inline.foreign_attribute.inline_attribute] = for_attr_offline;
                    on_ijson[form.inline.foreign_attribute.inline_attribute] = for_attr_online;
                    Online.save(null,form.inline.entity,on_ijson)
                        .done(function(on_in_model){
                            console.log("INLINE saved in online - "+JSON.stringify(on_in_model.toJSON()));
                            off_ijson.online_id = parseInt(on_in_model.get("id"));
                            Offline.save(null,form.inline.entity,off_ijson)
                                .done(function(off_in_model){
                                    console.log("INLINE saved in offline - "+JSON.stringify(off_in_model.toJSON()));
                                })
                                .fail(function(error){
                                    console.log("FORMCONTROLLER:EDIT:SAVE:INLINE:SAVE:OFFLINE: "+error);
                                });
                        })
                        .fail(function(error){
                            console.log("FORMCONTROLLER:EDIT:SAVE:INLINE:SAVE:ONLINE: "+error);
                        });
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
            console.log("FORMCONTROLLER: Button 2 clicked on form");
        },
        
        after_save: function(entity_name){
            window.Router.navigate(entity_name+'/add');
            window.Router.addPerson(entity_name); //since may be already on the add page, therefore have to call this explicitly
        }




    });

    // Our module now returns our view
    return FormControllerView;
});

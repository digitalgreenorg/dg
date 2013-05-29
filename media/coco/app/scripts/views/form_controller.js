define(['jquery', 'underscore', 'backbone', 'form_field_validator', 'syphon', 
    'views/notification', 'indexeddb_backbone_config', 'configs', 'views/form', 'collections/upload_collection', 'offline_to_online', 'offline_utils', 'online_utils'
// Using the Require.js text! plugin, we are loaded raw text
// which will be used as our views primary template
// 'text!templates/project/list.html'
], function($, pas, pass, pass, pass, notifs_view, indexeddb, configs, Form, upload_collection, OfflineToOnline, Offline, Online) {

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
        success_notif_template: _.template($('#' + 'success_notifcation_template').html()),
            
        json_converted: function(something){
            console.log("Gotcha B****: conv json");
            console.log(something);
            this.after_offline_to_online_success(something.on_json, something.off_json)
        },    

        on_save: function(e) {
            e.stopPropagation();
            console.log("ADD/EDIT: Save clicked on form - ");
            this.form = e.context; // form_view
            console.log("FORMCONTROLLER: cleaned, denormalised json from form.js-"+JSON.stringify(this.form.final_json));
            if(this.form.inline)
            {
                console.log("FORMCONTROLLER: separating inlines from final json");
                this.inline_models = $.extend(null,this.form.final_json.inlines);
                delete this.form.final_json.inlines;
            }
            
            this.form.offline_model.set(this.form.final_json);
            var that = this; // Please change to form_controller or something else which makes the content clear.
            this.offline_m = this.form.offline_model; // Remove this line
            if(that.is_uploadqueue_empty() && that.is_internet_connected())
            {
                console.log("FORMCONTROLLER: the uploadqueue is empty and internet connected");
                if(this.form.bulk)
                {
                    $.each(this.form.final_json.bulk, function(ind, obj){
                        OfflineToOnline.convert(obj, that.form.bulk.foreign_fields).then(that.json_converted);
                    });
                }
                else
                {
                    OfflineToOnline.convert(this.form.final_json,this.form.foreign_entities).then(this.json_converted);
                }
            }
            else
            {
                if(this.form.bulk)
                {
                    $.each(this.form.final_json.bulk, function(ind, obj){
                        that.save_when_offline(that.form.entity_name, obj);
                    });
                }
                else
                {
                    this.save_when_offline(this.form.entity_name, this.form.final_json);
                }
            }
        },
        
        save_when_offline: function(entity_name, off_json){
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
                                $(notifs_view.el)
                                    .append(that.success_notif_template({
                                    msg: "Success! Model saved offline and added to uploadqueue"
                                }));
                                if(that.form.inline)
                                    {
                                        console.log("FORMCONTROLLER: saving inlines");
                                        that.process_inlines_offline(that.form, off_m.toJSON(), that.inline_models);
                                    }
                            },
                            error: function(u_model){
                                console.log("FORMCNTROLLER: Unexepected Error- error adding model to uploadqueue - "+JSON.stringify(u_model.toJSON()));
                            }    
                        }
                    );
                    
                })
                .fail(function(error){
                    that.form.show_errors(error);
                    $(notifs_view.el)
                        .append(that.error_notif_template({
                        msg: "Error saving the model offline"
                    }));
                });
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
                    Offline.fetch_object(form.inline.entity, ijson.id)  //just to preserve videos_seen
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
        after_offline_to_online_success: function(o_json, off_json){ // call this send_to_server
            console.log("FORMCONTROLLER: Got this json to save online - "+JSON.stringify(o_json));
            var that = this;
            if(that.form.action == "A")
                {
                    delete o_json.id;
                }
                else
                {
                    o_json.id = parseInt(off_json.online_id); 
                    delete o_json.online_id;
                }
            Online.save(null, that.form.entity_name, o_json)
                .done(function(on_m){
                    console.log("SAVED IN ONLINE - "+JSON.stringify(on_m.toJSON()));
                    off_json.online_id  = parseInt(on_m.get("id"));
                    Offline.save(null, that.form.entity_name, off_json)
                        .done(function(off_m){
                            console.log("SAVED IN OFFLINE - "+JSON.stringify(off_m.toJSON()));
                            $(notifs_view.el)
                                .append(that.success_notif_template({
                                msg: "Successfully saved online and offline"
                            }));
                            if(that.form.inline)
                                {
                                    console.log("FORMCONTROLLER: saving inlines");
                                    that.process_inlines(that.form, off_m.toJSON(), on_m.toJSON(), that.inline_models);
                                }
                        })
                        .fail(function(error){
                            that.form.show_errors(error);
                            $(notifs_view.el)
                                .append(that.error_notif_template({
                                msg: "Error saving the model offline"
                            }));
                        });
                })
                .fail(function(xhr){
                    that.form.show_errors(xhr.responseText);
                    $(notifs_view.el)
                        .append(that.error_notif_template({
                        msg: "Error saving the model on server"
                    }));                           
                });
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
                    Offline.fetch_object(form.inline.entity, ijson.id)  //just to get the online_id and preserve videos_seen
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
                            off_ijson.online_id = on_in_model.get("id");
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
            e.stopPropagation();
            console.log("FORMCONTROLLER: Button 2 clicked on form");
        }




    });

    // Our module now returns our view
    return FormControllerView;
});

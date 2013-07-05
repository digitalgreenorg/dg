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
            console.log("FORMCONTROLLER: initializing a new FormControllerView");
            this.params = params;
            _.bindAll(this);
            // this.render();
        },
        template: "<div><div id = 'form'></div></div>",

        //setting up the form view
        beforeRender: function() {
            console.log(this.params);
            this.params = $.extend(this.params,{
                serialize: {
                    button1: "Save and Add Another",
                    button2: null
                }
            });
            // #form is the id of the element inside template where the new view will be inserted.
            var form_v = new Form(this.params);
            this.setView("#form", form_v);
            this.listenTo(form_v, 'save_clicked', this.on_save);
            this.listenTo(form_v, 'button2_clicked', this.on_button2);
        },
        
        /*
        Called when form view sends save_clicked event. 
        Identifies type of final_json and saves it
        After Save is finished calls an after_save function
        */
        //form.inline, bulk, final_json, foreign_fields, entity_name, 
        on_save: function(e) {
            this.form = e.context;  //event contains the form view object itself
            console.log("FORMCONTROLLER: cleaned, denormalised json from form.js-"+JSON.stringify(this.form.final_json));
            var that = this; 
            var save_complete_dfds = [];    //stores dfds of all objects bieng saved in this form
            
            if(this.form.bulk)
            {
                /*Save each object in bulk form individually*/
                $.each(this.form.final_json.bulk, function(ind, obj){
                    var bulk_index = obj.index;
                    delete obj.index;
                    var save_object_dfd = that.save_object(obj, that.form.bulk.foreign_fields, that.form.entity_name);
                    save_object_dfd
                        .fail(function(error){
                            that.form.show_errors(that.convert_to_row_error(error, that.form.entity_name, bulk_index));
                        });
                    save_complete_dfds.push(save_object_dfd);
                });
            }
            else    //normal or inlines
            {   
                //separate inlines from final json
                if(this.form.inline)
                {
                    console.log("FORMCONTROLLER: separating inlines from final json");
                    this.inline_models = $.extend(null,this.form.final_json.inlines);
                    delete this.form.final_json.inlines;
                    var inlines_dfd = new $.Deferred();
                    save_complete_dfds.push(inlines_dfd);
                }
                var save_object_dfd = this.save_object(this.form.final_json, this.form.foreign_entities, this.form.entity_name);
                save_object_dfd
                    .done(function(off_json){
                        if(that.form.inline)
                            that.save_inlines(that.inline_models, off_json, that.form.inline)
                                .done(function(){
                                    console.log("ALL INLINED SAVED");
                                    inlines_dfd.resolve();
                                })
                                .fail(function(){
                                    console.log("FAILED AT INLINES SAVE");
                                    show_inline_error();
                                    inlines_dfd.reject();
                                });
                    })
                    .fail(function(error){
                        that.form.show_errors(error);
                    });
                save_complete_dfds.push(save_object_dfd);                                
            }
            
            //When all objects in form are saved...
            $.when.apply(null, save_complete_dfds)
                .done(function(){
                    console.log("Everything saved");
                    that.after_save(that.form.entity_name);
                })
                .fail(function(){
                    if(that.form.bulk)
                        show_bulk_error();   
                });
            
            //shown if any inline could not be saved
            function show_inline_error(){
                var err = {};
                err[that.form.entity_name] = {
                    __all__: ["Some "+that.form.inline.entity+" (in red below) could not be saved. To correct errors and try saving them again - go to list page and edit this "+that.form.entity_name]
                };
                that.form.show_errors(err, true);
            }; 
            
            //shown if any bulk could not be saved
            function show_bulk_error(){
                var err = {};
                err[that.form.entity_name] = {
                    __all__: ["Some "+that.form.entity_name+" (in red below) could not be saved. To correct errors and try saving them again - open a new add form"]
                };
                that.form.show_errors(err, true);   
            };
        },
        
        //converts the error for an inline/bulk into a format which makes it show up at its own row
        convert_to_row_error: function(error, row_entity_name, row_index){
            error = $.parseJSON(error);
            error["row"+row_index] = error[row_entity_name];
            delete error[row_entity_name];
            return error;
        },
        
        save_inlines: function(inlines, parent_off_json, inline_config){
            var dfd = new $.Deferred();
            var that = this;
            console.log("Gotta save inlines now - ");
            console.log(JSON.stringify(inlines));
            console.log(JSON.stringify(parent_off_json));
            this.complete_inlines(inlines, parent_off_json, inline_config); 
            var inline_dfds = [];
            _.each(inlines, function(inl, index){
                var inl_index = inl.index;
                delete inl.index;
                var inl_save_dfd = this.save_object(inl, inline_config.foreign_entities, inline_config.entity); 
                inl_save_dfd
                    .fail(function(error){
                        that.form.show_errors(that.convert_to_row_error(error, inline_config.entity, inl_index));
                    });
                inline_dfds.push(inl_save_dfd);           
            }, this);
            $.when.apply($, inline_dfds)
                .done(function(){
                    dfd.resolve();
                })
                .fail(function(){
                    dfd.reject();
                })
            return dfd;
        },
        
        //put in the borrowed attributes and the joining attribute in inlines
        complete_inlines: function(inlines, parent_off_json, inline_config){
            var host_attr_json = {};
            host_attr_json[inline_config.joining_attribute.inline_attribute]={}
            _.each(inline_config.joining_attribute.host_attribute, function(attr, index){
               host_attr_json[inline_config.joining_attribute.inline_attribute][attr] = parent_off_json[attr];
            }, this);
            
            var borr_json = {}
            $.each(inline_config.borrow_attributes, function(index,b_attr){
                borr_json[b_attr.inline_attribute] = parent_off_json[b_attr.host_attribute];    
            });
            
            _.each(inlines, function(inl, index){
                console.log("inl before extension - "+JSON.stringify(inl));
                $.extend(true, inl, host_attr_json);
                $.extend(true, inl, borr_json);
                console.log("inl after extension - "+JSON.stringify(inl));
            });
        },
        
        save_object: function(json, foreign_entities, entity_name){
            var dfd = new $.Deferred();
            var that =  this;
            if(this.is_uploadqueue_empty() && this.is_internet_connected())
            {
                //Online mode
                ConvertNamespace.convert(json, foreign_entities, "offlinetoonline")
                    .done(function(on_off_jsons){
                        that.save_when_online(entity_name, on_off_jsons)
                            .done(function(off_json){
                                show_suc_notif();
                                dfd.resolve(off_json);
                            })
                            .fail(function(error){
                                show_err_notif();
                                dfd.reject(error);
                            });                            
                    })
                    .fail(function(error){
                        show_err_notif();
                        return dfd.reject(error);
                    });
            }
            else
            {
                //Offline mode
                this.save_when_offline(entity_name, json)
                    .done(function(off_json){
                        show_suc_notif();
                        return dfd.resolve(off_json);
                    })
                    .fail(function(error){
                        show_err_notif();
                        return dfd.reject(error);
                    });
            }
            
            function show_suc_notif(){
                notifs_view.add_alert({
                    notif_type: "success",
                    message: "Saved "+entity_name
                });
            };
            
            function show_err_notif(){
                notifs_view.add_alert({
                    notif_type: "error",
                    message: "Error saving "+entity_name
                });    
            };
            
            return dfd.promise();
        },
                
        save_when_offline: function(entity_name, off_json){
            var dfd = new $.Deferred();
            var action, that = this;
            if(off_json.id)
                action = "E"
            else
                action = "A"
            
            Offline.save(null, entity_name, off_json)
                .done(function(off_m){
                    console.log("SAVED IN OFFLINE - "+JSON.stringify(off_m.toJSON()));
                    upload_collection.create({
                            data: off_m.toJSON(),
                            action: action,   
                            entity_name: entity_name        
                        },
                        {
                            success:function(u_model){
                                console.log("FORMCNTROLLER: model added to uploadqueue - "+JSON.stringify(u_model.toJSON()));
                                return dfd.resolve(off_m.toJSON());    
                            },
                            error: function(error){
                                alert("Unexepected Error- error adding model to uploadqueue");
                                //TODO: should delete the model from offline db as well?
                                return dfd.reject(error);
                            }    
                    });
                })
                .fail(function(error){
                    return dfd.reject(error);
                });
                
            return dfd.promise();    
        },
        
        //save onlines then offline
        save_when_online: function(entity_name, on_off_jsons){ 
            var dfd = new $.Deferred();
            var on_json = on_off_jsons.on_json;
            var off_json = on_off_jsons.off_json
            console.log("FORMCONTROLLER: Got this json to save online - "+JSON.stringify(on_json));
            var that = this;
            //if edit case, substitute id with online id TODO: move it to convertnamespace?
            if(off_json.id)
            {
                on_json.id = parseInt(off_json.online_id); 
                delete on_json.online_id;
            }
            Online.save(null, entity_name, on_json)
                .done(function(on_m){
                    console.log("SAVED IN ONLINE - "+JSON.stringify(on_m.toJSON()));
                    off_json.online_id  = parseInt(on_m.get("id"));
                    Offline.save(null, entity_name, off_json)
                        .done(function(off_m){
                            console.log("SAVED IN OFFLINE - "+JSON.stringify(off_m.toJSON()));
                            return dfd.resolve(off_m.toJSON());    
                        })
                        .fail(function(error){
                            //TODO: what to do abt the model just saved on server? 
							return dfd.reject(error);
                        });
                })
                .fail(function(xhr){
                    return dfd.reject(xhr.responseText);
				});
			return dfd.promise();	 
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
            window.Router.add(entity_name); //since may be already on the add page, therefore have to call this explicitly
        }




    });

    // Our module now returns our view
    return FormControllerView;
});

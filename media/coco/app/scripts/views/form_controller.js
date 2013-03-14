define(['jquery', 'underscore', 'backbone', 'form_field_validator', 'syphon', 'views/notification', 'indexeddb_backbone_config', 'configs', 'views/form', 'collections/upload_collection'
// Using the Require.js text! plugin, we are loaded raw text
// which will be used as our views primary template
// 'text!templates/project/list.html'
], function($, pas, pass, pass, pass, notifs_view, indexeddb, configs, Form, upload_collection) {

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
                $.each(this.inline_models,function(index, imodel){
                    console.log(imodel);
                });
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
                that.offline_to_online(this.form.final_json); // If offline to online conversion succeds, then we save it to offline db. If this is succesful, then save it on server, then get online id from the server and set it on the offline object. If there is an error, then ?
                // Error callbacks???
            }
            else
            {
                //put into uploadqueue. save it in the offline db and upload Q.
                // Offline save
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
                                            });
                                            var i_model = new generic_model_offline();
                                            i_model.set(ijson);
                                            i_model.set(that.form.inline.foreign_attribute.inline_attribute, for_attr);
                                            i_model.save(null,{
                                                success: function(in_model){
                                                    console.log("FORMCONTROLLER: inline model saved - "+JSON.stringify(in_model.toJSON()));
                                                    upload_collection.create(
                                                        {
                                                            data: in_model.toJSON(),
                                                            action: "A",   //TODO: what if grp was edited, some inlines were edited and some new created
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
        
        
        offline_to_online: function(json) {
            console.log("FORMCONTROLLER:OFFLINE_TO_ONLINE: here am i");
            console.log(this.params);
            var f_entities = this.params.initialize.view_configs["foreign_entities"];
            console.log("FORMCONTROLLER:OFFLINE_TO_ONLINE: foreign entities for the model under consideration" + JSON.stringify(f_entities));
            var online_json = $.extend(null, json); // making a copy of object json
            console.log("FORMCONTROLLER:OFFLINE_TO_ONLINE: json before converting" + JSON.stringify(json));
            // var num_mem = Object.keys(f_entities).length; // Number of foreign entities referenced in this model.
            var num_mem = 0;
            for(member in f_entities)
            {
                num_mem += Object.keys(f_entities[member]).length;
            }
            console.log("FORMCONTROLLER:OFFLINE_TO_ONLINE: number of foreign elements - " + num_mem);
            if (!num_mem) {
                console.log("FORMCONTROLLER:OFFLINE_TO_ONLINE: no foreign entities to convert");
                this.after_offline_to_online_success(online_json);
            } else {
                for (member in f_entities) {
                    for(element in f_entities[member])
                    {
                        // If this foreign entity is not present in the current object, continue.
                        if (!(element in online_json)) {
                            num_mem--;
                            if (!num_mem) {
                                console.log("FORMCONTROLLER:OFFLINE_TO_ONLINE: all converted");
                                this.after_offline_to_online_success(online_json);
                                return;
                            }
                            else
                                continue;
                        }
                        console.log("FORMCONTROLLER:OFFLINE_TO_ONLINE: converting " + element + " offline to online.");
                        if(online_json[element] instanceof Array)
                        {
                            console.log("FORMCONTROLLER:OFFLINE_TO_ONLINE: This foreign element is multiselect. Fetching its collection.");
                            var generic_offline_collection = Backbone.Collection.extend({
                                database: indexeddb,
                                storeName: member,
                                attribute: element    
                            });
                            var f_collection = new generic_offline_collection();
                            var that = this;
                            f_collection.fetch({
                                success: function(collection){
                                    console.log("FORMCONTROLLER:OFFLINE_TO_ONLINE : foreign collection successfully fetched");
                                    $.each(online_json[collection.attribute],function(index,object){
                                        console.log("FORMCONTROLLER:OFFLINE_TO_ONLINE: converting this object inside multiselect" + JSON.stringify(object));
                                        var model = collection.get(object["id"]);
                                        console.log("FORMCONTROLLER:OFFLINE_TO_ONLINE: fetched same object from collection" + JSON.stringify(model.toJSON()));
                                        object["id"] =   model.get("online_id");
                                    });
                                    console.log("FORMCONTROLLER:OFFLINE_TO_ONLINE: json after converting" + JSON.stringify(online_json));
                                    num_mem--;
                                    if (!num_mem) {
                                        console.log("FORMCONTROLLER:OFFLINE_TO_ONLINE: all converted");
                                        that.after_offline_to_online_success(online_json);
                                    }            
                                },
                                error: function(){
                                    console.log("FORMCONTROLLER:OFFLINE_TO_ONLINE: Unexpected Error :foreign collection fetch failed");  
                                    alert("unexpected error. check console log");
                                    $(notifs_view.el)
                                        .append(that.error_notif_template({
                                        msg: "A foreign entity referenced does not exists in IDB."
                                    }));          
                                }        
                            });
    
                        }
                        else
                        {
                            console.log("FORMCONTROLLER:OFFLINE_TO_ONLINE: This foreign element is single select. Fetching its model.");
                            var generic_model_offline = Backbone.Model.extend({
                                database: indexeddb,
                                storeName: member, // add attribute name
                                attribute: element    
                            });
                            var f_model = new generic_model_offline();
                            f_model.set("id", online_json[element]["id"]);
                            var that = this;
                            f_model.fetch({
                                success: function(model) {
                                    console.log("FORMCONTROLLER:OFFLINE_TO_ONLINE: The foreign entity with the key mentioned fetched from IDB- " + JSON.stringify(model.toJSON()));
                                    online_json[model.attribute]["id"] =   model.get("online_id");
                                    // access the attribute name
                                    console.log("FORMCONTROLLER:OFFLINE_TO_ONLINE: json after converting" + JSON.stringify(online_json));
                                    num_mem--;
                                    if (!num_mem) {
                                        console.log("FORMCONTROLLER:OFFLINE_TO_ONLINE: all converted");
                                        that.after_offline_to_online_success(online_json);
                                    }
                                },
                                error: function() {
                                    console.log("FORMCONTROLLER:OFFLINE_TO_ONLINE: Unexpected Error : The foreign entity with the key mentioned does not exist anymore.");
                                    //TODO: this model should be deleted from IDB and server ????
                                    alert("unexpected error. check console log");
                                    // that.form.show_errors("A foreign entity referenced does not exists in IDB. ")
                                    $(notifs_view.el)
                                        .append(that.error_notif_template({
                                        msg: "A foreign entity referenced does not exists in IDB."
                                    }));
                                }
                            });
                        }
                    }
                }
            }
        },
        
        after_offline_to_online_success: function(o_json){ // call this send_to_server
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
                    console.log("FORMCONTROLLER:ON_SAVE: model saved in offline");
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
                                                ///////////////////////////////////////////////////////////////////////////////////    
                                                    i_model_online.save(null,{
                                                        success: function(on_in_model){
                                                            console.log("inline saved online - "+JSON.stringify(on_in_model.toJSON()));
                                                        },
                                                        error: function(){
                                                            console.log("error saving inline online");
                                                        }    
                                                    })    
                                                },
                                                error: function(error){
                                                    console.log("FORMCONTROLLER: error saving inline model");
                                                    console.log(error);
                                                }    
                                            });
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

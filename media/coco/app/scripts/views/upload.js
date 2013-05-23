define([
  'jquery',
  'underscore',
  'backbone',
  'indexeddb_backbone_config',
  'configs',
  'views/form',
  'collections/upload_collection',
  'offline_to_online',
  'offline_utils',
  'online_utils'                            
  // Using the Require.js text! plugin, we are loaded raw text
  // which will be used as our views primary template
  // 'text!templates/project/list.html'
], function($,pas,pass,indexeddb, configs, Form, upload_collection, OfflineToOnline, Offline, Online){
    
    var UploadView = Backbone.Layout.extend({
        
        template: "#upload_template",
        
        initialize: function(){
            console.log("UPLOAD: initializing new upload view");
            _(this).bindAll('stop_upload');
        },      
        
        events:{
            "click #stop_upload": "stop_upload"
        },
              
        stop_upload: function(){
            console.log("stopping upload");
            this.user_interrupt = true;
        },
              
        increment_pb: function() {
            w = parseFloat(document.getElementById('pbar').style.width);
            document.getElementById('pbar').style.width= (w + progress_bar_step) +'%';
        },
        
        update_status: function(status){
            $('#upl_status').html(status);
        },
        
        update_action: function(action){
            $('#upl_action').html(action);
        },
              
        initialize_upload: function(){
            this.user_interrupt = false;
            this.in_progress = true;
            this.$('#incremental_download_modal').modal({
                keyboard: false,
                backdrop: "static",
            });
            this.$('#upload_modal').modal('show');
            
        },
        
        tear_down: function(){
            $('#upload_modal').modal('hide'); 
            // this.remove();   
            this.in_progress = false; 
        },
              
        start_upload: function() {
            var dfd = new $.Deferred();
            console.log("UPLOAD: start the fuckin upload");
            var that = this;
            this.initialize_upload();
            this.get_uploadq()
                .done(function(collection){
                    that.iterate_uploadq(collection)
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
                    that.tear_down();
                    dfd.reject(error);
                });
            return dfd;
        },
        
        get_uploadq: function(){
            var dfd = new $.Deferred();
            upload_collection.fetch({
                success: function(collection){
                    dfd.resolve(collection);
                },
                error: function(error){
                    dfd.reject(error);
                }
            });
            return dfd;
        },

        // read each entry of the uploadqueue 
        iterate_uploadq: function(uploadq) {
            var dfd = new $.Deferred();
            this.upload_collection = uploadq;
            console.log("UPLOAD: inside upload queue: " + this.upload_collection.length + " entries");
            $('#num_upload').html(this.upload_collection.length);
            progress_bar_step = 100 / this.upload_collection.length;
            this.upload_status = {};
            this.upload_status["total"] = this.upload_collection.length;
            this.upload_status["uploaded"] = 0;
            this.pick_next(dfd);
            return dfd;
        },

        get_entity_name: function(upload_model){
            return upload_model.get('entity_name')
        },
        
        get_action: function(upload_model){
            return upload_model.get('action');
        },    
        
        get_json: function(upload_model){
            return upload_model.get('data');
        },
        
        get_foreign_field_desc: function(upload_model){
            var entity_name = this.get_entity_name(upload_model);    
            if(configs[entity_name].edit)
            {
                return configs[entity_name].edit.foreign_entities;
            }
            else
                return configs[entity_name].foreign_entities;
        },
        
        //returns the offline id of the object to be uploaded
        get_offline_id: function(upload_model){
            return parseInt(this.get_json(upload_model).id);
        },
        
        //returns the online id of the object to be uploaded
        get_online_id: function(upload_model){
            return parseInt(this.get_json(upload_model).online_id);
        },

        pick_next: function(whole_upload_dfd) {
            console.log("in pick_next");
            var that = this;
            this.update_status(this.upload_status["uploaded"]+"/"+this.upload_status["total"]);
            this.current_entry = this.upload_collection.shift();
            if (!this.current_entry) {
                return whole_upload_dfd.resolve();
            }
            else if (this.user_interrupt)
            {
                this.upload_collection.unshift(this.current_entry);
                return whole_upload_dfd.reject("User stopped Sync");
            }
            else{
                this.process_upload_entry(this.current_entry)
                    .fail(function(error){
                        console.log("FAILED TO UPLOAD AN OBJECT: ");
                        console.log(error);
                        //object to be uploaded doesn't exists in offline anymore
                        //offlineTOonline failed
                        //online_id couldn't be injected
                        //The object discarded in upload error form could not be deleted
                    })
                    .done(function(){
                        console.log("SUCESSFULLY UPLOADED AN OBJECT");
                    })
                    .always(function(){
                        that.current_entry.destroy();
                        that.increment_pb();
                        that.upload_status["uploaded"]++;
                        that.pick_next(whole_upload_dfd);
                    });
            }

        },
        
        process_upload_entry: function(up_entry) {
            var dfd = new $.Deferred();
            this.update_action("Uploading "+this.get_entity_name(up_entry));
            
            switch(this.get_action(up_entry))
                {
                    case 'A': 
                        this.upload_add_edit(up_entry, dfd);
                        break;
                    case 'E': 
                        this.upload_add_edit(up_entry, dfd);
                        break;
                    case 'D': 
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
            Offline.fetch_object(this.get_entity_name(up_model), this.get_offline_id(up_model))  
                .done(function(off_model){
                    console.log("Off model fetched - "+JSON.stringify(off_model.toJSON()));
                    OfflineToOnline.convert(that.get_json(up_model), that.get_foreign_field_desc(up_model))
                        .done(function(on_off_obj){
                            if(that.get_action(up_model) == "A")
                                {
                                    delete on_off_obj.on_json.id;
                                }
                                else
                                {
                                    on_off_obj.on_json.id = parseInt(off_model.get("online_id")); 
                                    delete on_off_obj.on_json.online_id;
                                }
                            Online.save(null, that.get_entity_name(up_model), on_off_obj.on_json)
                                .done(function(on_model){
                                    console.log("INCD:ADD: Successfully uploaded model. uploaded model - "+JSON.stringify(on_model.toJSON()));
                                    var off_json = off_model.toJSON();
                                    off_json.online_id = parseInt(on_model.get("id"));
                                    Offline.save(off_model, that.get_entity_name(up_model), off_json)
                                        .done(function(off_model){
                                            console.log("OFF model after all upload - "+JSON.stringify(off_model.toJSON()));
                                            dfd.resolve();    
                                        })
                                        .fail(function(error){
                                            dfd.reject("UPLOAD: Error saving online_id in offline obj: "+error);
                                        });
                                })
                                .fail(function(error){
                                    console.log("Error while saving oject on server");
                                    that.curr_entry_dfd = dfd;
                                    that.show_form(that.get_entity_name(up_model), on_off_obj.off_json, error.responseText);
                                });    
                        })
                        .fail(function(error){
                            console.log("UPLOAD: Not uploading object coz offlineTOonline failed");
                            dfd.reject(error);
                        });    
                })
                .fail(function(error){
                    if(error == "Not Found")
                    {
                        return dfd.reject("The object to be uploaded doesn't exists anymore.")    
                    }
                    else
                        dfd.reject(error);
                });    
        },
        
        show_form: function(entity_name, json, err_msg){
            console.log("UPLOAD:ERROR: need to show this json -" + JSON.stringify(json));
            p = new Form({
                serialize: {
                    button1: "Save again",
                    button2: "Discard"
                },
                initialize: {
                    view_configs: configs[entity_name],
                    router: null
                },
                model_id: null,
                model_json: json
            });
            p.render();
            this.listenTo(p, 'save_clicked', this.after_upload_error_save_again);
            this.listenTo(p, 'button2_clicked', this.after_upload_error_discard);
            p.show_errors(err_msg);
            this.$('#upload_form')
                .html(p.el);
        },
        
        after_upload_error_save_again: function(e){
            console.log("UPLOAD:ERROR: edit and retry");
            console.log("UPLOAD:ERROR: json from form - " + JSON.stringify(e.context.final_json));
            var after_upload_error_json = e.context.final_json;
            var that = this;
            Offline.save(null, this.get_entity_name(this.current_entry), after_upload_error_json)
                .done(function(off_model){
                    that.$('#upload_form')
                        .html("");
                    that.current_entry.set('data', after_upload_error_json);
                    that.upload_add_edit(that.current_entry, that.curr_entry_dfd);
                })
                .fail(function(error){
                    e.context.show_errors(error);
                });
        },
        
        after_upload_error_discard: function(e){
            console.log("DISCARD");
            var that = this;
            if (this.get_action(this.current_entry) == "A") 
            {
                Offline.delete_object(null, this.get_entity_name(this.current_entry), this.get_offline_id(this.current_entry))
                    .done(function(){
                        return that.curr_entry_dfd.resolve();
                    })
                    .fail(function(error){
                        return that.curr_entry_dfd.reject("The object discarded in upload error form could not be deleted - "+error);
                    });
            } 
            else 
            {
                this.curr_entry_dfd.resolve();
            }
            this.$('#upload_form')
                .html("");
        },
        
        upload_delete: function(up_model, dfd) {
            if(this.get_online_id(up_model))
            {
                Online.delete_object(null, this.get_entity_name(up_model), this.get_online_id(up_model))
                    .done(function(){
                        return dfd.resolve();
                    })
                    .fail(function(error){
                        return dfd.reject("The object discarded in upload error form could not be deleted - "+error);
                    });
            }
            else
            {
                // No online_id was found on the model when deleted. Therefore its not on server yet. Hence taking no action.
                return dfd.resolve();
            }
        },

              
    });
    
    
    
  // Our module now returns our view
  return UploadView;
});
define([
  'jquery',
  'underscore',
  'backbone',
  'indexeddb_backbone_config',
  'configs',
  'views/form',
  'collections/upload_collection',
  'offline_to_online'                            
  // Using the Require.js text! plugin, we are loaded raw text
  // which will be used as our views primary template
  // 'text!templates/project/list.html'
], function($,pas,pass,indexeddb, configs, Form, upload_collection, OfflineToOnline){
    
    var UploadView = Backbone.Layout.extend({
        
        template: "#upload_template",
        increment_pb: function() {
            w = parseInt(document.getElementById('pbar').style.width);
            document.getElementById('pbar').style.width= (w + progress_bar_step) +'%';
        },
        
        initialize: function(){
            console.log("UPLOAD: initializing new upload view");
            $(document)
                .on("read_next", this.next_upload);
            _(this)
                .bindAll('json_converted');
        },      
              
        start_upload: function() {
            this.$('#upload_modal').modal('show');
            console.log("UPLOAD: start the fuckin upload");
            // var generic_model_offline = Backbone.Model.extend({
//                 database: indexeddb,
//                 storeName: "uploadqueue",
//             });
//             var generic_offline_collection = Backbone.Collection.extend({
//                 model: generic_model_offline,
//                 database: indexeddb,
//                 storeName: "uploadqueue",
//             });

            // this.generic_upload_model = generic_model_offline;
            // this.upload_collection = new generic_offline_collection();
            this.upload_collection = upload_collection;
            this.upload_collection.bind('reset', this.process_upload_queue, this);
            this.upload_collection.fetch();
            ////////////////////////////////////////////////////////////////////////////////////////////////////////////
        },

        // read each entry of the uploadqueue 
        process_upload_queue: function() {
            console.log("UPLOAD: inside upload queue: " + this.upload_collection.length + " entries");
            $('#num_upload').html(this.upload_collection.length);
            progress_bar_step = 100 / this.upload_collection.length;
            console.log("UPLOAD: progress bar step: " + progress_bar_step);
            ev = {
                type: "read_next",
                context: this
            };
            $.event.trigger(ev);

        },
        ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

        next_upload: function(event) {
            event.stopPropagation();
            console.log("in next_upload");
            console.log(this);
            event.context.increment_pb();
            var model1 = event.context.upload_collection.shift();
            if (model1 == undefined) {
                $('#upload_modal').modal('hide'); 
                return;
            }
            console.log(model1);
            event.context.process_upload_entry(model1);
            $('#curr_status').html("Uploading "+model1.get("entity_name"));

        },

        process_upload_entry: function(entry) {
            this.current_entry = entry;
            console.log("UPLOAD: processing this uploadqueue entry - " + JSON.stringify(entry.toJSON()));
            if (entry.get("action") == "A" || entry.get("action") == "E") {
                console.log("UPLOAD: its add or edit action");
                // this.offline_to_online(entry);
                OfflineToOnline.convert(entry.get("data"), configs[entry.get('entity_name')]["foreign_entities"]).then(this.json_converted);
            } else if (entry.get("action") == "D") {
                console.log("UPLOAD: its delete action");
                this.upload_delete(entry);
            } else {
                console.log("ERROR:UPLOAD: its ambigous action in entry. None of A,E,D");
            }
        },
            
        json_converted: function(something){
            console.log("Gotcha B****: conv json");
            console.log(something);
            if (this.current_entry.get("action") == "A") {
                console.log("UPLOAD: its add action");
                this.upload_add(something.on_json);
            } else if (this.current_entry.get("action") == "E") {
                console.log("UPLOAD: its edit action");
                this.upload_edit(something.on_json);
            }
        },
        
        upload_add: function(conv_json) {
            //   this.setView("#upload_form", new PersonAddEditView({
            //     initialize: {view_configs:configs[entry.get("entity_name")],router:this},
            //     model_id: entry.get("data").id
            // }));

            // this.$('#upload_form').html('<form><input></input></form>');
            // var shit = new upload_view({            });
            // this.setView("#show_status",shit );

            // this.render();
            // shit.$('#upload_form').show();
            // create online,offline models for the entity of upload entry
            var that = this;

            var generic_model_online = Backbone.Model.extend({
                sync: Backbone.ajaxSync,
                url: function() {
                    return this.id ? configs[that.current_entry.get("entity_name")].rest_api_url + this.id + "/" : configs[that.current_entry.get("entity_name")].rest_api_url;
                },
            });
            var generic_model_offline = Backbone.Model.extend({
                database: indexeddb,
                storeName: that.current_entry.get("entity_name"),
            });

            var upload_online_model = new generic_model_online();
            var upload_offline_model = new generic_model_offline();
            ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////

            // set json from uploadqueue entry on online model, unset the id, save the model     
            var offline_id = this.current_entry.get("data")
                .id;

            upload_offline_model.set("id", offline_id);
            var that = this;
            var fetching = upload_offline_model.fetch({
                success: function(model) { // not deleted hence go forward

                    // var online_json = that.offline_to_online(entry);      
                    upload_online_model.set(conv_json); //setting what was recorded and not the exact model
                    upload_online_model.unset('id');
                    console.log("UPLOAD:ADD: upload online model set - " + JSON.stringify(upload_online_model.toJSON()));
                    console.log("UPLOAD:ADD: upload online model save called.");
                    upload_online_model.save(null, {
                        async: false,
                        success: function(online_model) {
                            console.log("UPLOAD:ADD: Dummy online person model after save - " + JSON.stringify(upload_online_model.toJSON()));

                            // set online id in offline model
                            model.set('online_id', upload_online_model.get("id"));
                            model.save(null, {
                                success: function(model) {
                                    console.log("UPLOAD:ADD: offline model after evrthing-" + JSON.stringify(model.toJSON()));
                                    that.current_entry.destroy();
                                    $.event.trigger(ev);
                                },
                                error: function() {
                                    //ToDO: error handling
                                    console.log("ERROR:UPLOAD:ADD: Unexpected error.Couldn't save offline model.The offline model's online id could not be set.");
                                    that.current_entry.destroy();
                                    $.event.trigger(ev);

                                }
                            });
                        },
                        error: function(model, xhr, options) {
                            console.log("UPLOAD:ADD: Error adding model on server ");
                            _(that).bindAll('after_upload_error');
                            $(document).on("upload_error_resolved", that.after_upload_error);
                            console.log("UPLOAD:ERROR: need to show this json -" + JSON.stringify(that.current_entry.get("data")));
                            p = new Form({
                                serialize: {
                                    button1: "Save again",
                                    button2: "Discard"
                                },
                                initialize: {
                                    view_configs: configs[that.current_entry.get("entity_name")],
                                    router: this
                                },
                                model_id: that.current_entry.get("data")
                                    .id,
                                model_json: that.current_entry.get("data")
                            });
                            p.render();
                            that.$('#error_msg')
                                .html(xhr.responseText);
                            console.log(xhr.statusText);
                            that.$('#upload_form')
                                .html(p.el);

                            // $.event.trigger(ev);

                        }

                    });

                    ///////////////////////////////////////////////////////////////////////////////////////////////////


                },


                error: function() {
                    console.log("ERROR:UPLOAD:ADD: The offline model does not exist in indexeddb anymore. Can't set its online id. Must be deleted. Ignoring. ");
                    //discard this and continue with next uploadqueue entry
                    that.current_entry.destroy();
                    $.event.trigger(ev);

                }
            });


        },

        after_upload_error: function(e) {
            console.log("UPLOAD:ERROR: in after error");
            this.$('#upload_form')
                .html("");
            this.$('#error_msg')
                .html("");

            e.stopPropagation();
            if (e.discard) {
                console.log("UPLOAD:ERROR: the entry was discraded");
                if (this.current_entry.get("action") == "A") {
                    var generic_model_offline = Backbone.Model.extend({
                        database: indexeddb,
                        storeName: this.current_entry.get("entity_name"),
                    });

                    var upload_offline_model = new generic_model_offline();
                    var offline_id = this.current_entry.get("data")
                        .id;

                    upload_offline_model.set("id", offline_id);
                    var that = this;
                    upload_offline_model.destroy({
                        success: function() {
                            console.log("UPLOAD:ADD:ERROR: Discarded and destroyed from IDB.");
                            that.current_entry.destroy();
                            $.event.trigger(ev);
                        },
                        error: function() {
                            console.log("ERROR:UPLOAD:ADD:ERROR: unexpected error. Coudn't delete an offline model");
                            alert("error");
                        }
                    });


                } else {
                    this.current_entry.destroy();
                    console.log("in after upload error");
                    $.event.trigger(ev);
                }

            } else {
                console.log("UPLOAD:ERROR: edit and retry");
                console.log("UPLOAD:ERROR: json from form - " + JSON.stringify(e.context.final_json));
                var after_upload_error_json = e.context.final_json;
                var generic_model_offline = Backbone.Model.extend({
                    database: indexeddb,
                    storeName: this.current_entry.get("entity_name"),
                });
                var upload_offline_model = new generic_model_offline();
                upload_offline_model.set(after_upload_error_json);
                var that = this;
                upload_offline_model.save(null, {
                    success: function(model) {

                        console.log("UPLOAD:ADD:ERROR:RETRY: edited to - " + JSON.stringify(model));
                        that.current_entry.set('data', after_upload_error_json);
                        var upload_model_edit = new that.generic_upload_model();
                        upload_model_edit.set({
                            data: after_upload_error_json,
                            action: "E",
                            entity_name: that.current_entry.get("entity_name")
                        });
                        that.upload_collection.unshift(that.current_entry);
                        that.upload_collection.push(upload_model_edit); // to maintain the consistency between online and offline data. bcoz there cud be an Edit on this model later in the uploadqueue.
                        $.event.trigger(ev);

                    },
                    error: function() {
                        console.log("ERROR:UPLOAD:ADD:ERROR:RETRY: Unexpected Error.Couldn't save the offline model ");
                    }
                });



                console.log(ev);
            }

        },


        upload_edit: function(conv_json) {
            // create online,offline models for the entity of upload entry
            var that = this;
            var generic_model_online = Backbone.Model.extend({
                sync: Backbone.ajaxSync,
                url: function() {
                    return this.id ? configs[that.current_entry.get("entity_name")].rest_api_url + this.id + "/" : configs[that.current_entry.get("entity_name")].rest_api_url;
                },
            });
            var generic_model_offline = Backbone.Model.extend({
                database: indexeddb,
                storeName: that.current_entry.get("entity_name"),
            });

            var upload_offline_model = new generic_model_offline();
            var upload_online_model = new generic_model_online();
            ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////

            // set json from uploadqueue entry on online model, unset the id, save the model     
            upload_offline_model.set(this.current_entry.get("data"));
            var that = this;
            var fetching = upload_offline_model.fetch({
                success: function(model) {
                    console.log("UPLOAD:EDIT: offline model fetched to get online id-" + JSON.stringify(model.toJSON()));
                    upload_online_model.set(conv_json);
                    console.log("UPLOAD:EDIT: upload online model from uploadqueue- " + JSON.stringify(upload_online_model.toJSON()));
                    upload_online_model.set('id', model.get('online_id'));
                    upload_online_model.unset('online_id');
                    console.log("UPLOAD:EDIT: upload online model set - " + JSON.stringify(upload_online_model.toJSON()));
                    upload_online_model.save(null, {
                        success: function(model) {
                            console.log("UPLOAD:EDIT: Dummy online person model after save - " + JSON.stringify(upload_online_model.toJSON()));
                            that.current_entry.destroy();
                            $.event.trigger(ev);
                        },
                        error: function(model, xhr, options) {
                            console.log("UPLOAD:EDIT: Error editing model on server ");

                            _(that)
                                .bindAll('after_upload_error');
                            $(document)
                                .on("upload_error_resolved", that.after_upload_error);
                            console.log("UPLOAD:ERROR: need to show this json -" + JSON.stringify(that.current_entry.get("data")));
                            p = new Form({
                                serialize: {
                                    button1: "Save again",
                                    button2: "Discard"
                                },
                                initialize: {
                                    view_configs: configs[that.current_entry.get("entity_name")],
                                    router: this
                                },
                                model_id: that.current_entry.get("data")
                                    .id,
                                model_json: that.current_entry.get("data")
                            });

                            p.render();
                            that.$('#error_msg')
                                .html(xhr.responseText);
                            console.log(xhr.statusText);
                            that.$('#upload_form')
                                .html(p.el);

                        }
                    });
                    console.log("UPLOAD:EDIT: upload online model save called.");

                },
                error: function() {
                    //ToDO: error handling
                    console.log("ERROR:UPLOAD:EDIT: The offline model does not exist in indexeddb. Can't get its online id. Ignoring. ");
                    that.current_entry.destroy();
                    $.event.trigger(ev);
                }
            });

            /////////////////////////////////////////////////////////////////////////////////////////////////////////////////

        },

        upload_delete: function(entry) {
            // create online,offline models for the entity of upload entry
            var generic_model_online = Backbone.Model.extend({
                sync: Backbone.ajaxSync,
                url: function() {
                    return this.id ? configs[entry.get("entity_name")].rest_api_url + this.id + "/" : configs[entry.get("entity_name")].rest_api_url;
                },
            });
            var generic_model_offline = Backbone.Model.extend({
                database: indexeddb,
                storeName: entry.get("entity_name"),
            });

            var upload_offline_model = new generic_model_offline();
            var upload_online_model = new generic_model_online();
            ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////

            // 
            if ('online_id' in entry.get("data")) {
                upload_online_model.set(entry.get("data"));
                console.log("UPLOAD:DELETE: upload online model from uploadqueue- " + JSON.stringify(upload_online_model.toJSON()));
                upload_online_model.set('id', upload_online_model.get('online_id'));
                upload_online_model.unset('online_id');
                console.log("UPLOAD:DELETE: upload online model set - " + JSON.stringify(upload_online_model.toJSON()));
                upload_online_model.delete(null, {
                    success: function(model) {
                        console.log("UPLOAD:DELETE: deleted ");
                        entry.destroy();
                        $.event.trigger(ev);
                    },
                    error: function() {
                        console.log("UPLOAD:DELETE: Error while deleting on server ");
                        entry.destroy();
                        $.event.trigger(ev);

                    }
                });
                console.log("UPLOAD:DELETE: upload online model delete called.");
            } else {
                console.log("UPLOAD:DELETE: No online_id was found on the model when deleted. Therefore its not on server yet. Hence taking no action.");
                entry.destroy();
                $.event.trigger(ev);

            }
            /////////////////////////////////////////////////////////////////////////////////////////////////////////////////




        },

              
    });
    
    
    
  // Our module now returns our view
  return UploadView;
});
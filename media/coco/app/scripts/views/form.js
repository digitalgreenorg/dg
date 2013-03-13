define(['jquery', 'underscore', 'backbone', 'form_field_validator', 'syphon', 'views/notification', 'indexeddb_backbone_config', 'configs', 'indexeddb-backbone'
// Using the Require.js text! plugin, we are loaded raw text
// which will be used as our views primary template
// 'text!templates/project/list.html'
], function($, pas, pass, pass, pass, notifs_view, indexeddb, all_configs) {


    var ShowAddEditFormView = Backbone.Layout.extend({

        events: {
            // 'click #button1': 'save', // jQuery Validate handles this event. Below, we link the 
            'click #button2': 'button2_clicked'
        },
        error_notif_template: _.template($('#' + 'error_notifcation_template')
            .html()),
        success_notif_template: _.template($('#' + 'success_notifcation_template')
            .html()),
        template : '#form_template',                
        serialize: function(){
            s_passed = this.options.serialize;
            s_passed["form_template"] = this.form_template;    
            return s_passed;
                
        },
        initialize: function(params) {
            console.log("ADD/EDIT: params to add/edit view: ");
            console.log(params);
            this.view_configs = params.initialize.view_configs;
            this.appRouter = params.initialize.router;
            this.form_template = $('#' + this.view_configs.add_edit_template_name).html();
            options_inner_template = _.template($('#options_template')
                .html());
            this.entity_name = this.view_configs.entity_name;
            this.final_json = null;
            
            // Creating the offline models for the entity in consideration 
            var generic_model_offline = Backbone.Model.extend({
                database: indexeddb,
                storeName: this.view_configs.entity_name,
            }); 
            
            this.offline_model = new generic_model_offline();
            ////////////////////////////////////////////////////////////////////////////////////////////////////////////////

            // Get foreign entities, create their offline collection to be fetched afterRender, bind them to render_foreign_entity
            this.f_colls = new Array();
            _(this)
                .bindAll('render_foreign_entity');

            for (f_entity in this.view_configs.foreign_entities) {
                var generic_collection_offline = Backbone.Collection.extend({
                    database: indexeddb,
                    storeName: all_configs[f_entity].entity_name,
                });

                this.f_colls.push(new generic_collection_offline());
                // Reset is called when a collection has finished fetching.
                // We are binding the reset of the last added collection to render_foreign_entity
                _.last(this.f_colls)
                    .bind('reset', this.render_foreign_entity);
                
                /*
                this.f_colls.push(new generic_collection_offline().bind);
                
                var f_collection = new generic_collection_offline();
                f_collection.bind
                f_colls.push(f_collection);
                */

            }
            ////////////////////////////////////////////////////////////////////////////////////////////////////////////////


            // Edit or Add? If Edit, set id on offline model, bind it to fill_form. 
            // There are two ways in which edit is true - when the ID is given, and the second is when an upload is edited on error.
            json = null;
            this.edit_case = false;
            // Edit case: we receive json from Upload
            if (params.model_json) {
                this.edit_case_json = true; // edit_case_upload
                this.model_json = params.model_json;
                this.edit_case = true;
            } else if (params.model_id) {

                this.offline_model.set({
                    id: params.model_id
                });
                this.edit_case_id = true;
                this.edit_case = true;

            }
            // No need for two variables. One is sufficient.
            if(this.edit_case)
                this.action = "E"
            else
                this.action = "A"            
            ////////////////////////////////////////////////////////////////////////////////////////////////////////////////
            
            _(this)
                .bindAll('save');

        },

        afterRender: function() {
            console.log("ADD/EDIT:foreign colls being fetched:");


            // fetching all foreign collections
            //TODO: handle error callback
            for (var i = 0; i < this.f_colls.length; i++) {
                console.log(this.f_colls[i]);
                this.f_colls[i].fetch({
                    success: function() {
                        console.log("ADD/EDIT: a foreign coll fetched");
                        // render foreign collection is called automatically on successful fetch
                    },
                    error: function() {
                        //ToDO: error handling
                        console.log("ERROR: ADD/EDIT: a foreign collection could not be fetched!");
                    }
                });
            }
            ////////////////////////////////////////////////////////////////////////////////////////////////////////////////


            // fetching offline model
            var that = this;
            if (this.edit_case_json) {
                this.fill_form();

            } else if (this.edit_case_id) {
                console.log("FORM: EDIT: fetching this model - "+JSON.stringify(this.offline_model.toJSON()));
                this.offline_model.fetch({
                    success: function(model) {
                        console.log("EDIT: edit model fetched");
                        that.model_json = model.toJSON();
                        that.normalize_json(that.model_json);
                        that.fill_form();
                    },
                    error: function() {
                        //ToDO: error handling
                        console.log("ERROR: EDIT: Edit model could not be fetched!");
                        alert("ERROR: EDIT: Edit model could not be fetched!");
                    }

                });
            }
            ////////////////////////////////////////////////////////////////////////////////////////////////////////////////


            // call validator on the form
            var context = this;
            var validate_obj = $.extend(this.view_configs.form_field_validation,{
                    "submitHandler" : function() {
                    context.save();
                }
                }
                );
            this.$('form')
                .validate(validate_obj);
            ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////

            return this;
        },

        render_foreign_entity: function(collection, options) {
            console.log("ADD/EDIT: rendering foreign entity");
            for(element in this.view_configs.foreign_entities[collection.__proto__.storeName])
            {
                f_entity_desc = this.view_configs.foreign_entities[collection.__proto__.storeName][element];
                $f_el = this.$('#' + f_entity_desc.placeholder);
                collection.each(function(f_model) {
                    $f_el.append(options_inner_template({
                        id: parseInt(f_model.get("id")),
                        name: f_model.get(f_entity_desc.name_field)
                    }));
                });
                console.log("ADD/EDIT: " + f_entity_desc.placeholder + " populated");
                    
            }
            if (this.model_json) Backbone.Syphon.deserialize(this, this.model_json);
        },

        normalize_json: function(d_json){
            console.log("FORM: Before Normalised json = "+JSON.stringify(d_json));      
            var f_entities = this.view_configs["foreign_entities"];
            for (member in f_entities) {
                for(element in f_entities[member])
                {
                    if (element in d_json) {
                        if (d_json[element] instanceof Array) {
                            var el_array = [];
                            $.each(d_json[element],function(index,object){
                                el_array.push(parseInt(object["id"]));
                            });
                            d_json[element] = el_array;
                        }
                        else {
                            d_json[element] = parseInt(d_json[element]["id"]); 
                        }
                    }
                }
            }
            console.log("FORM: Normalised json = "+JSON.stringify(d_json));      
            return d_json;
            
        },
            
        denormalize_json: function(n_json){
            console.log("FORM: Before DNormalising json - "+JSON.stringify(this.final_json))
            var f_entities = this.view_configs["foreign_entities"];
            var c=0;
            for (member in f_entities) {
                for(element in f_entities[member])
                {
                    if (element in n_json) {
                        name_field = f_entities[member][element]["name_field"];
                        
                        if (n_json[element] instanceof Array) {
                            var el_array = [];
                            var that = this;
                            $.each(n_json[element],function(index, id){
                                id = parseInt(id);
                                console.log(id);
                                if((id != "")&&(id!=null)&&(id!=undefined)){ 
                                    var entity = that.f_colls[c].where({
                                        id: id
                                    })[0];
                                    var el_dict = {};
                                    el_dict["id"] = id;
                                    el_dict[name_field] = entity.get(f_entities[member][element]["name_field"]);    
                                    el_array.push(el_dict);    
                                }
                            });
                            n_json[element] = el_array;
                        } else {
                            var id = parseInt(n_json[element]);
                            if((id != "")&&(id!=null)&&(id!=undefined)){ 
                                var entity = this.f_colls[c].where({
                                    id: id
                                })[0];
                                n_json[element] = {};
                                n_json[element]["id"] = id;
                                n_json[element][name_field] = entity.get(f_entities[member][element]["name_field"]);    
                            }
                            else{
                                n_json[element] = {};
                                n_json[element]["id"] = null;
                                n_json[element][name_field] = null;
                            }
                        }
                        
                        
                    }    
                }
                
                c++;
            }
            console.log("FORM: After DNormalising json - "+JSON.stringify(this.final_json))
            
        },
                
        fill_form: function() {
            console.log("FORM: filling form with the model - "+JSON.stringify(this.model_json));
            Backbone.Syphon.deserialize(this, this.model_json);
        },
        
            
        clean_json: function(object_json){
            console.log("FORM: Before cleaning json - "+JSON.stringify(object_json))
            
            for(member in object_json)
                {   
                    if(member == "")
                        delete object_json[member];
                    
                    else if(object_json[member]==""||object_json[member]==null||object_json[member]==undefined)
                    {
                        object_json[member] = null
                    }
                }    
            console.log("FORM: After cleaning json - "+JSON.stringify(object_json))
                
        },  
        show_errors: function(errors){
            console.log("FORM: in show errors");
            var error_str = "";
            console.log("FORM: SHOWERROR: ");
            // errors = eval(errors);
            // for(member in errors)
            // {
            //     if(member != "__all__"){
            //         error_str += member +" : <br>";
            //     }
            //     
            //     $.each(errors[member],function(err){
            //         error_str += err+"<br>";
            //     });
            //     
            // }
            // console.log(eval(errors));
            
            
            
            
            this.$('#form_errors').html(errors);
        },        
        save: function() {
            this.final_json = Backbone.Syphon.serialize(this);
            this.clean_json(this.final_json);
            this.denormalize_json(this.final_json);
            this.final_json = $.extend(this.model_json, this.final_json);
            ev_res = {
                type: "upload_error_resolved",
                context: this,
                discard: false
            };

            ev_save = {
                type: "save_clicked",
                context: this,
            };

            $.event.trigger(ev_res);
            $.event.trigger(ev_save);
        },

        button2_clicked: function() {
            ev_res = {
                type: "upload_error_resolved",
                context: this,
                discard: true
            };

            ev_button2 = {
                type: "button2_clicked",
                context: this,
                discard: true
            };

            $.event.trigger(ev_res);
            $.event.trigger(ev_button2);
        }


    });

    // Our module now returns our view
    return ShowAddEditFormView;
});

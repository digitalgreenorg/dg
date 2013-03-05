define(['jquery', 'underscore', 'backbone', 'form_field_validator', 'syphon', 'views/notification', 'indexeddb_backbone_config', 'configs', 'indexeddb-backbone'
// Using the Require.js text! plugin, we are loaded raw text
// which will be used as our views primary template
// 'text!templates/project/list.html'
], function($, pas, pass, pass, pass, notifs_view, indexeddb, all_configs) {


    var ShowAddEditFormView = Backbone.Layout.extend({

        events: {
            // 'click #button1': 'save',
            'click #button2': 'button2_clicked'
        },
        error_notif_template: _.template($('#' + 'error_notifcation_template')
            .html()),
        success_notif_template: _.template($('#' + 'success_notifcation_template')
            .html()),

        initialize: function(params) {
            console.log("ADD/EDIT: params to add/edit view: ");
            console.log(params);
            this.view_configs = params.initialize.view_configs;
            this.appRouter = params.initialize.router;
            this.template = '#' + this.view_configs.add_edit_template_name;
            options_inner_template = _.template($('#options_template')
                .html());

            this.final_json = null;
            // Creating the online,offline collections and models for the entity in consideration 
            var generic_model_offline = Backbone.Model.extend({
                database: indexeddb,
                storeName: this.view_configs.entity_name,
            });

            var generic_collection_offline = Backbone.Collection.extend({
                model: generic_model_offline,
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
                _.last(this.f_colls)
                    .bind('reset', this.render_foreign_entity);


            }
            ////////////////////////////////////////////////////////////////////////////////////////////////////////////////


            // Edit or Add? If Edit, set id on offline model, bind it to fill_form. 
            json = null;

            if (params.model_json) {
                this.edit_case_json = true;
                this.model_json = params.model_json;
            } else if (params.model_id) {

                this.offline_model.set({
                    id: params.model_id
                });
                this.edit_case_id = true;

            } else this.edit_case = false;
            ////////////////////////////////////////////////////////////////////////////////////////////////////////////////
            this.just_save = false;
            this.save_and_add_another = false;
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
            this.$('form')
                .validate({
                submitHandler: function() {
                    context.save();
                },
                highlight: function(element, errorClass, validClass) {
                    $(element)
                        .parent('div')
                        .parent('div')
                        .addClass("error");

                },
                unhighlight: function(element, errorClass, validClass) {
                    $(element)
                        .parent('div')
                        .parent('div')
                        .removeClass("error");

                },
                errorElement: "span",
                errorClass: "help-inline"
            });
            ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////

            return this;
        },

        render_foreign_entity: function(collection, options) {
            console.log("ADD/EDIT: rendering foreign entity");
            f_entity_desc = this.view_configs.foreign_entities[collection.__proto__.storeName];
            $f_el = this.$('#' + f_entity_desc.placeholder);
            collection.each(function(f_model) {
                $f_el.append(options_inner_template({
                    id: f_model.get("id"),
                    name: f_model.get(f_entity_desc.name_field)
                }));
            });
            console.log("ADD/EDIT: " + f_entity_desc.placeholder + " populated");
            if (this.model_json) Backbone.Syphon.deserialize(this, this.model_json);
        },

        normalize_json: function(d_json){
            console.log("FORM: Before Normalised json = "+JSON.stringify(this.model_json));      
            var f_entities = this.view_configs["foreign_entities"];
            for (member in f_entities) {
                if (member in d_json) {
                    d_json[member] = d_json[member]["id"]; 
                }
                
            }
            console.log("FORM: Normalised json = "+JSON.stringify(this.model_json));      
            return d_json;
            
        },
            
        denormalize_json: function(n_json){
            console.log("FORM: Before DNormalising json - "+JSON.stringify(this.final_json))
            var f_entities = this.view_configs["foreign_entities"];
            var c=0;
            for (member in f_entities) {
                if (member in n_json) {
                    name_field = f_entities[member]["name_field"];
                    var id = n_json[member];
                    if(id != ""){ 
                        var entity = this.f_colls[c].where({
                            id: id
                        })[0];
                        n_json[member] = {};
                        n_json[member]["id"] = id;
                        n_json[member][name_field] = entity.get(f_entities[member]["name_field"]);    
                    }
                    else
                        delete n_json[member]
                }
                c++;
            }
            console.log("FORM: After DNormalising json - "+JSON.stringify(this.final_json))
            
        },
                
        fill_form: function() {
            console.log("FORM: filling form with the model - "+JSON.stringify(this.model_json));
            Backbone.Syphon.deserialize(this, this.model_json);
        },

        save: function() {
            this.final_json = Backbone.Syphon.serialize(this);
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

define(['jquery', 'underscore', 'backbone', 'form_field_validator', 'syphon', 'views/notification', 'indexeddb_backbone_config', 'configs', 'indexeddb-backbone'
// Using the Require.js text! plugin, we are loaded raw text
// which will be used as our views primary template
// 'text!templates/project/list.html'
], function($, pas, pass, pass, pass, notifs_view, indexeddb, all_configs) {


    var ShowAddEditFormView = Backbone.Layout.extend({

        events: {
            'click #button1': 'save',
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
            Backbone.Syphon.deserialize(this, this.model_json);
        },


        fill_form: function(m_json) {
            Backbone.Syphon.deserialize(this, this.model_json);
        },

        save: function() {
            this.final_json = Backbone.Syphon.serialize(this);
            this.final_json = $.extend(this.model_json, this.final_json);
            ev_res = {
                type: "upload_error_resolved",
                context: this,
                discard: false
            };
            $.event.trigger(ev_res);
        },

        button2_clicked: function() {
            ev_res = {
                type: "upload_error_resolved",
                context: this,
                discard: true
            };
            $.event.trigger(ev_res);
        }


    });

    // Our module now returns our view
    return ShowAddEditFormView;
});

define([
  'jquery',
  'underscore',
  'backbone',
  'form_field_validator',
  'syphon',
  'views/notification',
  'indexeddb_backbone_config',
  'configs',
  // Using the Require.js text! plugin, we are loaded raw text
  // which will be used as our views primary template
  // 'text!templates/project/list.html'
], function($,pas,pass,pass,pass,notifs_view,indexeddb,all_configs){
    

    var PersonAddEditView = Backbone.Layout.extend({

        events: {
            'click #save': 'save',
            'click #save_add_another': 'set_save_add_another'
        },
        setjustsave: function() {
            console.log("ADD/EDIT: only save");
            this.just_save = true;
            this.save_and_add_another = false;
        },
        set_save_add_another: function() {
            console.log("ADD/EDIT: save and add another");
            this.save_and_add_another = true;
            this.just_save = false;
        },
        error_notif_template: _.template($('#' + 'error_notifcation_template')
            .html()),
        success_notif_template: _.template($('#' + 'success_notifcation_template')
            .html()),
        
        initialize: function(params) {
            console.log("ADD/EDIT: params to add/edit view:");
            console.log(params);
            this.view_configs = params.initialize.view_configs;
            this.appRouter = params.initialize.router;
            this.template = '#' + this.view_configs.add_edit_template_name;
            options_inner_template = _.template($('#options_template')
                .html());
            
          
            // Creating the online,offline collections and models for the entity in consideration 
            var generic_model_offline = Backbone.Model.extend({
                  database: indexeddb,
                  storeName: this.view_configs.entity_name,
            });
            
            var generic_model_online = Backbone.Model.extend({
                sync: Backbone.ajaxSync,
                
                url: function() {
                    return this.id ? this.view_configs.rest_api_url + this.id + "/" : this.view_configs.rest_api_url;
                },
                // save: function(attributes, options) {
//                     console.log("SAVE OVERRIDE: cleaning data");
//                     if(this.get("age")=="")
//                     this.set("age",null);
//         
//                     if(this.get("land_holdings")=="")
//                     this.set("land_holdings",null);
//         
//                     if(this.get("village"))
//                     this.set("village","/api/v1/village/" + this.get("village") + "/");
//                     else this.set("village",null);
//         
//                     if(this.get("group"))
//                     this.set("group","/api/v1/group/" + this.get("group") + "/");
//                     else this.set("group",null);
//                     console.log("ADD/EDIT: saving this on server" +JSON.stringify(this));
//                     return Backbone.Model.prototype.save.call(this, attributes, options);
//                 }
            });
          
            var generic_collection_offline = Backbone.Collection.extend({
                  model: generic_model_offline,
                  database: indexeddb,
                  storeName: this.view_configs.entity_name,
            });
          
            var generic_collection_online = Backbone.Collection.extend({
                  url: this.view_configs.rest_api_url,
                  sync: Backbone.ajaxSync,
                  parse: function(data) {
                      return data.objects;
                  }

            });
          
            this.offline_model = new generic_model_offline();
            this.online_model = new generic_model_online();
            ////////////////////////////////////////////////////////////////////////////////////////////////////////////////
            
            
            // Get foreign entities, create their offline collection to be fetched afterRender, bind them to render_foreign_entity
            this.f_colls = new Array();
            _(this)
                .bindAll('render_foreign_entity');
            
            for (f_entity in this.view_configs.foreign_entities)
            {  
                var generic_collection_offline = Backbone.Collection.extend({
                      database: indexeddb,
                      storeName: all_configs[f_entity].entity_name,
                });
                
                this.f_colls.push(new generic_collection_offline());
                _.last(this.f_colls).bind('reset', this.render_foreign_entity);
                
                
            }
            ////////////////////////////////////////////////////////////////////////////////////////////////////////////////
            
           
            // Edit or Add? If Edit, set id on offline model, bind it to fill_form. 
            json = null;
            if (params.model_id) {

                // model = new offline_model({
                //                 id: params.model_id
                //             });
                this.offline_model.set({
                    id: params.model_id
                });
                _(this)
                    .bindAll('fill_form');
                this.offline_model.bind('change', this.fill_form);
                this.edit_case = true;

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
            for(var i=0;i<this.f_colls.length;i++)
            {
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
            if (this.edit_case == true) {

                this.offline_model.fetch({
                    success: function() {
                        console.log("EDIT: edit model fetched");
                    },
                    error: function() {
                        //ToDO: error handling
                        console.log("ERROR: EDIT: Edit model could not be fetched!");
                        alert("ERROR: EDIT: Edit model could not be fetched!");
                    }
                    //ToDO: error handling
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
        
        render_foreign_entity: function(collection,options){
            console.log("ADD/EDIT: rendering foreign entity");
            f_entity_desc = this.view_configs.foreign_entities[collection.__proto__.storeName];
            $f_el = this.$('#'+f_entity_desc.placeholder);
            collection.each(function(f_model) {
                            $f_el.append(options_inner_template({
                                id: f_model.get("id"),
                                name: f_model.get(f_entity_desc.name_field)
                            }));
                        });
            console.log("ADD/EDIT: "+f_entity_desc.placeholder + " populated");
        },
        
       
        fill_form: function() {
            //render must be finished before this func
            console.log("EDIT: its edit case, model for edit:");
            console.log(this.offline_model);
            json = this.offline_model.toJSON();
            json.village = json.village.id;
            json.group = json.group.id;
            Backbone.Syphon.deserialize(this, json);
        },
            
        save: function() {
            // read data from form
            // check internet conn
            //if internect conn create on online coll/model(?) then create on offline coll/model        (server log ?)
            //else create on offline coll/model, add to local log
            var form_data = Backbone.Syphon.serialize(this);
            console.log("ADD/EDIT: form to json: ");
            console.log(form_data);
            if (form_data.hasOwnProperty('')) {
                delete form_data[''];
            }

            var village = this.villages.where({
                id: form_data['village']
            })[0];
            var persongroup = this.persongroups.where({
                id: form_data['group']
            })[0];
            // var offline_data = new Object();
            var offline_data = jQuery.extend(true, {}, form_data);
            var online_data = form_data;
            console.log(JSON.stringify(form_data));

            if (village) {
                offline_data['village'] = {
                    'id': village.get('id'),
                    'village_name': village.get('village_name')
                };
            } else offline_data['village'] = {
                'id': null,
                'village_name': null
            };

            if (persongroup) {
                offline_data['group'] = {
                    'id': persongroup.get('id'),
                    'group_name': persongroup.get('group_name')
                };
            } else offline_data['group'] = {
                'id': null,
                'group_name': null
            };

            var context = this;
            if (this.edit_case) {
                this.offline_model.set(offline_data);
                console.log("editing person to:");
                console.log(JSON.stringify(this.offline_model));
                this.offline_model.save(null, {
                    error: function() {
                        console.log("EDIT: error while saving edit of person in local db");
                        $(notifs_view.el)
                            .append(context.error_notif_template({
                            msg: "Failed to Edit the person"
                        }));


                    },
                    success: function() {
                        console.log("EDIT: successfully edited a person in local db");
                        $(notifs_view.el)
                            .append(context.success_notif_template({
                            msg: "Successfully Edited the person"
                        }));

                    }
                });

            } else {
                this.offline_model.set(offline_data);
                this.online_model.set(online_data);
                console.log("ADD: adding new person:");
                var context = this;

                this.online_model.save(null, {
                    error: function() {
                        console.log("ADD: error adding person online");
                        $(notifs_view.el)
                            .append(context.error_notif_template({
                            msg: "Failed to Add the person on server"
                        }));


                    },
                    success: function(model) {
                        console.log("ADD: successfully added a person on server");
                        $(notifs_view.el)
                            .append(context.success_notif_template({
                            msg: "Successfully Added the person on server"
                        }));
                        console.log(model.toJSON());
                        console.log(model.id);


                        context.offline_model.set({
                            id: model.id
                        });
                        console.log("ADD: saving this locally" + JSON.stringify(context.offline_model));

                        context.offline_model.save(null, {
                            error: function() {
                                console.log("ADD: error adding person locally");
                                $(notifs_view.el)
                                    .append(context.error_notif_template({
                                    msg: "Failed to Add the person locally"
                                }));


                            },
                            success: function(model) {
                                console.log("ADD: successfully added a person locally");
                                $(notifs_view.el)
                                    .append(context.success_notif_template({
                                    msg: "Successfully Added the person locally"
                                }));
                                console.log(model.toJSON());

                            }
                        });

                    }
                });

            }

            if (this.just_save) this.appRouter.navigate('person', true);
            else if (this.save_and_add_another) {
                this.appRouter.navigate('person/add');
                this.appRouter.addPerson(); //since may be already on the add page, therefore have to call this explicitly
            } else console.log("Bug: ADD/Edit after save option not set!");


        }

      
    });
    
  // Our module now returns our view
  return PersonAddEditView;
});
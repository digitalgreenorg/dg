define(['jquery', 'underscore', 'backbone', 'form_field_validator', 'syphon', 'views/notification', 'indexeddb_backbone_config', 'configs', 'indexeddb-backbone'
// Using the Require.js text! plugin, we are loaded raw text
// which will be used as our views primary template
// 'text!templates/project/list.html'
], function($, pas, pass, pass, pass, notifs_view, indexeddb, all_configs) {


    var ShowAddEditFormView = Backbone.Layout.extend({

        events: {
            'click #button1': 'save', // jQuery Validate handles this event. Below, we link the 
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
            s_passed["inline"] = (this.inline) ? true: false;
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
            this.inline = this.view_configs.inline;
            
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

            this.f_index = [];
            for (f_entity in this.view_configs.foreign_entities) {
                var generic_collection_offline = Backbone.Collection.extend({
                    database: indexeddb,
                    storeName: all_configs[f_entity].entity_name,
                });
                this.f_index.push(f_entity);    
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
            console.log(this.f_index);
            ////////////////////////////////////////////////////////////////////////////////////////////////////////////////


            // Edit or Add? If Edit, set id on offline model, bind it to fill_form. 
            // There are two ways in which edit is true - when the ID is given, and the second is when an upload is edited on error.
            json = null;
            this.edit_case = false;
            this.edit_id = null;
            // Edit case: we receive json from Upload
            if (params.model_json) {
                this.edit_case_json = true; // edit_case_upload
                this.model_json = params.model_json;
                this.edit_case = true;
                this.edit_id = this.model_json.id;
            } else if (params.model_id) {

                this.offline_model.set({
                    id: params.model_id
                });
                this.edit_case_id = true;
                this.edit_case = true;
                this.edit_id = params.model_id;
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

            //render inlines
            if(this.inline)
            {
                this.$('#inline_header').html($('#'+this.inline.header).html());
                var inline_t = $('#'+this.inline.template).html();
                for(var i=0;i<this.inline.num_rows;i++)
                {
                    this.$('#inline_body').append(inline_t);    
                }
                
            }
            ////////////////////////////////////////////////////////////////////////////////////////////////////////////////
            
            
            


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
            this.dependencies = {}; 
            this.element_entity_map={};
            ////////////////////////////////////////////////////////////////////////////////////////////////////////////////


            // fetching offline model and inlines
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
                
                if(this.inline)
                {
                    //TODO: fetching the whole collection. Can this be more effifcient by fetching just the relevant models? Done this way because the foreign field in model is a object and am not yet able to specify a condition on such fields using the I-B adapter.
                    console.log("FORM:EDIT: Fteching inline collection");
                    var generic_offline_collection = Backbone.Collection.extend({
                        database: indexeddb,
                        storeName: this.inline.entity,
                    });
                    this.inline_collection = new generic_offline_collection();
                    this.inline_collection.fetch({
                        success: function(collection){
                            console.log("FORM: EDIT: Inline collection fetched! - "+ collection.storeName);
                            // var inl_models =  collection.where({
//                                 that.inline.foreign_attribute.inline_attribute.id : that.edit_id
//                             });
                            var inl_models = collection.filter(function(model){
                               return model.get(that.inline.foreign_attribute.inline_attribute).id == that.edit_id;
                            });
                            console.log(inl_models);
                            that.fill_inlines(inl_models);
                        },
                        error: function(){
                            console.log("ERROR: EDIT: Inline collection could not be fetched!");
                        }        
                    });
                }
            }
            ////////////////////////////////////////////////////////////////////////////////////////////////////////////////


            // call validator on the form
            var context = this;
            var validate_obj = $.extend(this.view_configs.form_field_validation,{
                    "submitHandler" : function() {
                    context.save();
                }
            });
            this.$('form')
                .validate(validate_obj);
            ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////

            return this;
        },
        
        fill_inlines: function(model_array){
            console.log("Filling inlines");
            var count = 0;
            var trs = $('#inline_body tr');
            console.log(trs);
            var that = this;
            $.each(model_array,function(index, model){
                that.fill_form_elements(trs[count], model.toJSON());
                count++;
            });
        },    

        // takes a jquery object containgg form elements.Fills all input and select elements with the corrsponding value in json    
        fill_form_elements: function(container, o_json){
            var input_elms = $(container).find('input');
            $.each(input_elms,function(index,inp){
                $(inp).val(o_json[$(inp).attr('name')]);
            });
            var sel_elms = $(container).find('select');
            $.each(sel_elms,function(index,sel){
                $(sel).val(o_json[$(sel).attr('name')]);
            });
            $(container).attr("model_id", o_json.id);
        },
        
        fill_dep_entity: function(ev){
            var source = $(ev.target).attr("id");
            var curr_value = $(ev.target).val();
            for(var i=0; i<this.dependencies[source].length;i++)
            {
                var element = this.dependencies[source][i];
                var entity = this.element_entity_map[element];
                var index = this.f_index.indexOf(entity);
                var collection = this.f_colls[index];
                var dep_desc = this.view_configs.foreign_entities[entity][element].dependency;
                if(collection.length)
                {
                    console.log(collection.at(0).get(dep_desc.dep_attr));
                    if(collection.at(0).get(dep_desc.dep_attr) instanceof Array)
                    {
                        console.log("FORM: FILLDEPENTITY: The dep attribute is an array");
                        var filtered_models = collection.filter(function(model){
                           var exists = false;
                           $.each(model.get(dep_desc.dep_attr),function(index, object){
                                if(object.id == curr_value)
                                    exists = true;
                           });
                           return exists;
                        });
                        
                    }
                    else{
                        console.log("FORM: FILLDEPENTITY: The dep attribute is not an array");
                        var filtered_models = collection.filter(function(model){
                           return model.get(dep_desc.dep_attr).id == curr_value;
                        });
                    }
                    this.fill_foreign_entity(element, filtered_models);
                }
                
            }
            
        },    
          
        fill_foreign_entity: function(element, model_array){
            var f_entity_desc = this.view_configs.foreign_entities[this.element_entity_map[element]][element];
            if(f_entity_desc.expanded)
            {
                _.template($('#options_template')
                                .html());
                console.log(f_entity_desc.expanded.template);
                console.log($('#' + f_entity_desc.expanded.template));
                var expanded_template  = _.template($('#'+f_entity_desc.expanded.template).html());
                $f_el = this.$('#' + f_entity_desc.expanded.placeholder);
                $f_el.html('');
                $.each(model_array,function(index, f_model){
                    $f_el.append(expanded_template(f_model.toJSON()));    
                });
            }
            else{
                $f_el = this.$('#' + f_entity_desc.placeholder);
                $f_el.html('');
                $.each(model_array,function(index, f_model){
                    $f_el.append(options_inner_template({
                        id: parseInt(f_model.get("id")),
                        name: f_model.get(f_entity_desc.name_field)
                    }));    
                });
                console.log("ADD/EDIT: " + f_entity_desc.placeholder + " populated");
            }
        },
                        
        render_foreign_entity: function(collection, options) {
            console.log("ADD/EDIT: rendering foreign entity");
            _(this).bindAll('fill_dep_entity');
            for(element in this.view_configs.foreign_entities[collection.storeName])
            {
                this.element_entity_map[element] = collection.storeName;
                if(this.view_configs.foreign_entities[collection.storeName][element]["dependency"])
                {
                    console.log("FORM:render_for_entity: dependency exists ");
                    var f_ens = this.view_configs.foreign_entities;
                    var source_entity = f_ens[collection.storeName][element].dependency.source_entity;
                    var source_elm = f_ens[collection.storeName][element].dependency.source_form_element;
                    console.log(source_entity);
                    console.log(source_elm);
                    var source_elm_id = f_ens[source_entity][source_elm].placeholder;
                    console.log(source_elm_id);
                    var that = this;
                    if(source_elm_id in this.dependencies)
                        {
                            this.dependencies[source_elm_id].push(element);
                        }    
                    else{
                        this.dependencies[source_elm_id] = [];
                        this.dependencies[source_elm_id].push(element);
                        var that = this;
                        $('#'+source_elm_id).change(that.fill_dep_entity);
                    }
                    console.log("dependencies = "+JSON.stringify(this.dependencies));    
                    
                }
                else{
                    this.fill_foreign_entity(element, collection.toArray());
                }
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
        parse_inlines: function(raw_json){
            console.log("FORM: fetching inlines");
            var all_inlines = $('#inline_body tr');    
            raw_json["inlines"] = [];
            var that = this;
            var inline_attrs = [];
            $.each(all_inlines,function(index, inl){
                // console.log();
                var inl_obj = {};
                var inputs = $(inl).find("input");
                var ignore = true;
                if($(inl).attr("model_id"))
                    inl_obj.id = parseInt($(inl).attr("model_id"));
                $.each(inputs,function(index1, inp){
                    inl_obj[$(inp).attr("name")]= $(inp).val();
                    if($(inp).val()!="")
                        ignore = false;
                    if(index==0)
                        inline_attrs.push($(inp).attr("name"));
                });
                var selects = $(inl).find("select");
                $.each(selects,function(index2, sel){
                    inl_obj[$(sel).attr("name")]= $(sel).val();
                    if($(sel).val()!="")
                        ignore = false;
                    if(index==0)
                        inline_attrs.push($(sel).attr("name"));
                });
                $.each(that.inline.borrow_attributes,function(index,b_attr){
                    inl_obj[b_attr.inline_attribute] = raw_json[b_attr.host_attribute]    
                });
                if(!ignore)
                    raw_json["inlines"].push(inl_obj);
                // console.log($(inl).serializeArray());    
            });
            
            //remove inline attrs from raw_json...let them be inside raw_json.inlines only
            $.each(inline_attrs,function(index,attr){
                delete raw_json[attr];
            });
            console.log(inline_attrs);
            
            
        },
                    
        save: function() {
            this.final_json = Backbone.Syphon.serialize(this);
            this.clean_json(this.final_json);
            this.denormalize_json(this.final_json);
            if(this.inline)
                this.parse_inlines(this.final_json);
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

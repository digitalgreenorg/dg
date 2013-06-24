define([
    'jquery', 
    'underscore', 
    'layoutmanager', 
    'form_field_validator', 
    'syphon', 
    'views/notification', 
    'indexeddb_backbone_config', 
    'configs', 
    'offline_utils', 
    'indexeddb-backbone',
    'chosen',
    'date_picker',
    'time_picker'
], function(jquery, underscore, layoutmanager, pass, pass, notifs_view, indexeddb, all_configs, Offline) {


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
            s_passed["inline"] = (this.inline) ? true: false;
            return s_passed;
        },
        initialize: function(params) {
            console.log("ADD/EDIT: params to add/edit view: ");
            console.log(params);
            this.view_configs = params.initialize.view_configs;
            this.appRouter = params.initialize.router;
            options_inner_template = _.template($('#options_template')
                .html());
            this.entity_name = this.view_configs.entity_name;
            this.final_json = null;
            
            
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
            
            if(this.edit_case)
            {
                this.form_template = $('#' + this.view_configs.edit_template_name).html();
                if(this.view_configs.edit)
                {
                    this.foreign_entities = this.view_configs.edit.foreign_entities;
                    this.inline = this.view_configs.edit.inline;
                    this.bulk = this.view_configs.edit.bulk;
                }
                else
                {
                    this.foreign_entities = this.view_configs.foreign_entities;
                    this.inline = this.view_configs.inline;
                    this.bulk = this.view_configs.bulk;
                }
            }
            else
            {
                this.form_template = $('#' + this.view_configs.add_template_name).html();
                if(this.view_configs.add)
                {
                    this.foreign_entities = this.view_configs.add.foreign_entities;
                    this.inline = this.view_configs.add.inline;
                    this.bulk = this.view_configs.add.bulk;
                }
                else
                {
                    this.foreign_entities = this.view_configs.foreign_entities;
                    this.inline = this.view_configs.inline;
                    this.bulk = this.view_configs.bulk;
                }
            }

            // Get foreign entities, create their offline collection to be fetched afterRender, bind them to render_foreign_entity
            this.f_colls = new Array();
            _(this)
                .bindAll('render_foreign_entity');
            _(this).bindAll('fill_dep_entity');
            this.f_index = [];
            this.num_f_elems = 0;
            this.dependencies = {}; 
            this.element_entity_map={};
            this.foreign_elements_rendered = {};
            this.num_sources = {};
            for (f_entity in this.foreign_entities) {
                var generic_collection_offline = Backbone.Collection.extend({
                    database: indexeddb,
                    storeName: all_configs[f_entity].entity_name,
                    comparator: function(model){
                        return model.get(all_configs[this.storeName].sort_field)
                    }
                });
                this.f_index.push(f_entity);    
                this.f_colls.push(new generic_collection_offline());
                /*
                this.f_colls.push(new generic_collection_offline().bind);
                
                var f_collection = new generic_collection_offline();
                f_collection.bind
                f_colls.push(f_collection);
                */
                for(element in this.foreign_entities[f_entity])
                {
                    this.num_f_elems++; // total num of f elems
                    this.element_entity_map[element] = f_entity; //created mapping of element - entity
                    this.foreign_elements_rendered[element] = false;
                    // creating source - dependency mapping to be used for in-form events
                    var dependency = this.foreign_entities[f_entity][element]["dependency"];
                    if(dependency)
                        this.num_sources[element] = dependency.length;
                    else
                        this.num_sources[element] = 0;   
                    if(dependency)
                    {
                        var f_ens = this.foreign_entities;
                        var that = this;
                        $.each(dependency,function(index,dep){
                            var source_entity = dep.source_entity;
                            var source_elm = dep.source_form_element;
                            var source_elm_id = f_ens[source_entity][source_elm].placeholder;
                            if(source_elm_id in that.dependencies)
                                {
                                    that.dependencies[source_elm_id].push(element);
                                }    
                            else{
                                that.dependencies[source_elm_id] = [];
                                that.dependencies[source_elm_id].push(element);
                            }
                        });
                        // console.log("FORM: dependency exists ");
//                         var f_ens = this.foreign_entities;
//                         var source_entity = f_ens[f_entity][element].dependency.source_entity;
//                         var source_elm = f_ens[f_entity][element].dependency.source_form_element;
//                         var source_elm_id = f_ens[source_entity][source_elm].placeholder;
//                         var that = this;
//                         if(source_elm_id in this.dependencies)
//                             {
//                                 this.dependencies[source_elm_id].push(element);
//                             }    
//                         else{
//                             this.dependencies[source_elm_id] = [];
//                             this.dependencies[source_elm_id].push(element);
//                             // var that = this;
//                             // this.$el.$('#'+source_elm_id).change(that.fill_dep_entity);
//                         }
                        console.log("dependencies = "+JSON.stringify(this.dependencies));    
                    }
                    
                }
            }
            ////////////////////////////////////////////////////////////////////////////////////////////////////////////////


            
            
            _(this)
                .bindAll('save');

        },

        afterRender: function() {
            for (f_entity in this.foreign_entities) {
                for(element in this.foreign_entities[f_entity])
                {
                    if(!this.foreign_entities[f_entity][element].expanded)
                    {
                        this.$('[name='+element+']').prop("disabled", true);
                    }
                }
            }
            
            //render empty inlines - add case done
            if(this.inline)
            {
                this.$('#inline_header').html($('#'+this.inline.header).html());
                if(!this.edit_case)
                    this.append_new_inlines();    
            }
            ////////////////////////////////////////////////////////////////////////////////////////////////////////////////
            
            
            
            
            var that = this;
            // fetching all foreign collections
            //TODO: handle error callback
            for (var i = 0; i < this.f_colls.length; i++) {
                this.f_colls[i].fetch({
                    success: function(collection) {
                        console.log("ADD/EDIT: a foreign coll fetched - "+collection.storeName);
                        // render foreign collection is called automatically on successful fetch
                        that.render_foreign_entity(collection,null);
                    },
                    error: function() {
                        //ToDO: error handling
                        console.log("ERROR: ADD/EDIT: a foreign collection could not be fetched!");
                    }
                });
            }
            // this.dependencies = {}; 
//             this.element_entity_map={};
            this.num_initial_f_entities = 0;
            var that = this;
            for(el_id in this.dependencies)
            {
                console.log("creating changeevent for - "+el_id);
                this.$('#'+el_id).change(this.fill_dep_entity);
            }
            ////////////////////////////////////////////////////////////////////////////////////////////////////////////////


            // fetching offline model and inlines
            var that = this;
            if (this.edit_case_json) {
                that.normalize_json(this.model_json);
                this.fill_form();           //TODO: does it needs to be normalised first ?

            } else if (this.edit_case_id) {
                Offline.fetch_object(this.view_configs.entity_name, this.edit_id)
                    .done(function(model) {
                        console.log("EDIT: edit model fetched");
                        that.model_json = model.toJSON();
                        that.normalize_json(that.model_json);
                        that.fill_form();
                    })
                    .fail(function() {
                        //ToDO: error handling
                        console.log("ERROR: EDIT: Edit model could not be fetched!");
                        alert("ERROR: EDIT: Edit model could not be fetched!");
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
                            //TODO: error handling
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
            $(".chzn-select").chosen({'search_contains':true});
			
			var eDate = new Date();
			enddate = eDate.getFullYear() + "-" + (eDate.getMonth() + 1) + "-" + eDate.getDate();
			
            $(".date-picker")
                .datepicker({
                    format: 'yyyy-mm-dd',
					startDate: '2009-01-01',
					endDate: enddate,
                }).on('changeDate', function(ev){
                    $(this).datepicker('hide');
                });
            $(".time-picker")
                .timepicker({
                    minuteStep: 1,
                    defaultTime: false,
                    showMeridian: false
                });                
            return this;
        },
        
        append_new_inlines: function(){
            var inline_t  = _.template($('#'+this.inline.template).html());
            // var inline_t = $('#'+this.inline.template).html();
            for(var i=0;i<this.inline.num_rows;i++)
            {
                var tr = $(inline_t({index:i}));
                this.$('#inline_body').append(tr);    
                $(tr).on('change', this.switch_validation_for_inlines);
            }
        },
        
        switch_validation_for_inlines: function(){
            console.log("tr chenaged");
            var empty = true;
            $(this).find(':input').each(function() {
                console.log($(this).val());
                if($(this).val())
                    empty = false;
            });
            if(!empty)
            {
                $(this).find(':input').each(function() {
                    $(this).removeClass("donotvalidate")
                });
            }
            else
            {
                $(this).find(':input').each(function() {
                    $(this).addClass("donotvalidate")
                });
            }
        },
        
        fill_inlines: function(model_array){
            console.log("Filling inlines");
            var that = this;
            var inline_t  = _.template($('#'+this.inline.template).html());
            
            $.each(model_array,function(index, model){
                var tr = inline_t({index:index});
                var filled_tr = that.fill_form_elements($(tr), model.toJSON());
                $(filled_tr).find(':input').removeClass("donotvalidate");
                that.$('#inline_body').append(filled_tr);
                $(filled_tr).on('change', that.check_tr);
            });
        },    

        // takes a jquery object containgg form elements.Fills all input and select elements with the corrsponding value in json    
        fill_form_elements: function(container, o_json){
            container.attr("model_id", o_json.id);
            container.find(':input').each(function() {
                if(!$(this).attr('name'))
                    return;
                var attr_name = $(this).attr("name").replace(new RegExp("[0-9]", "g"), "");
    			switch(this.type) {
    				case 'password':
    				case 'select-multiple':
    				case 'select-one':
    				case 'text':
    				case 'textarea':
    					$(this).val(o_json[attr_name]);
    					break;
    				case 'checkbox':
    				case 'radio':
    					this.checked = o_json[attr_name];
                }
            });
            return container;
        },
        
        fill_dep_entity: function(ev){
            var source = $(ev.target).attr("id");
            console.log("FILLING DEP ENTITIES OF -"+source);
            for(var i=0; i<this.dependencies[source].length;i++)
            {
                //Fully Reset the dependent select element by looking at all its sources.
                var element = this.dependencies[source][i];
                var entity = this.element_entity_map[element];
                var index = this.f_index.indexOf(entity);
                var collection = this.f_colls[index];
                var dependencies = this.foreign_entities[entity][element].dependency;
                var final_models = [];
                // console.log("FORM:FILLDEPENTITY: F Collection length - "+collection.length+" "+element);
                var that = this;
                $.each(dependencies, function(index, dep_desc){
                    if(collection.length)
                    {
                        var dep_attr = dep_desc.dep_attr;
                        var source_form_element = dep_desc.source_form_element;
                        var source_entity = dep_desc.source_entity;
                        var source_placeholder = that.foreign_entities[source_entity][source_form_element].placeholder;
                        var curr_value = $('#'+source_placeholder).val();
                        var filtered_models = [];
                        if(!curr_value)
                        {
                            return;
                        }
                        if(!(curr_value instanceof Array))
                        {
                            v = curr_value;
                            curr_value = [];
                            curr_value.push(parseInt(v));
                        }
                        else{
                            $.each(curr_value, function(index,val){
                                curr_value[index] = parseInt(val);
                            });
                        }
                        if(collection.at(0).get(dep_desc.dep_attr) instanceof Array)
                        {
                            // console.log("FORM: FILLDEPENTITY: The dep attribute is an array");
                            filtered_models = collection.filter(function(model){
                               var exists = false;
                               $.each(model.get(dep_desc.dep_attr),function(index, object){
                                    if(!($.inArray( object.id, curr_value)==-1))
                                        exists = true;
                               });
                               return exists;
                            });
                        
                        }
                        else{
                            // console.log("FORM: FILLDEPENTITY: The dep attribute is not an array");
                            filtered_models = collection.filter(function(model){
                                var compare = null;
                                if(typeof model.get(dep_desc.dep_attr) == "object")
                                    compare = model.get(dep_desc.dep_attr).id; 
                                else
                                    compare = model.get(dep_desc.dep_attr)
                                if(dep_desc.rev_sub_attr)
                                    {
                                        var src_entity = dep_desc.source_entity;
                                        var index = that.f_index.indexOf(src_entity);
                                        var s_collection = that.f_colls[index];
                                        var s_model = s_collection.get(curr_value[0]);
                                        // console.log(s_model);
                                        var exists = false;
                                        if(s_model.get(dep_desc.rev_sub_attr) instanceof Array)
                                        {
                                            $.each(s_model.get(dep_desc.rev_sub_attr), function(index, src_compare){
                                                console.log(src_compare+ " "+ compare);
                                                if(typeof src_compare == "object")
                                                {
                                                    if(compare == src_compare.id)
                                                        exists = true;
                                                }
                                                else
                                                {
                                                    if(compare == src_compare)
                                                        exists = true;
                                                }
                                            });
                                        }
                                        return exists;
                                    }        
                                else
                                    {
                                        if(!($.inArray(compare, curr_value)==-1))
                                            exists = true;
                                        else
                                            exists = false;
                                        return exists;
                                    }            
                            });
                        }
                    }
                    final_models = final_models.concat(filtered_models);
                });
                that.fill_foreign_entity(element, final_models);
                
            }
            
        },    
          
        fill_foreign_entity: function(element, model_array){
            console.log("FILLING FOREIGN ENTITY - "+element);
            this.num_sources[element]--;
            var f_entity_desc = this.foreign_entities[this.element_entity_map[element]][element];
            // this.num_f_elems--; 
            var filter = f_entity_desc.filter;
            if(filter)
            {
                // console.log("FILTERING FOREIGN ENTITY!");
                var filter_attr = filter.attr;
                var filter_value = filter.value;
                filtered = [];
                $.each(model_array, function(index, obj){
                    if(obj.get(filter_attr).id == filter_value)
                    {
                        filtered.push(obj);
                    }
                });
                model_array = filtered;
            }
            if(this.edit_case && f_entity_desc.expanded && !this.foreign_elements_rendered[element])
            {
                console.log("EDIt CASE, EXPANDED, Not Yet RENDERED");
                var expanded_template  = _.template($('#'+f_entity_desc.expanded.template).html());
                $f_el = this.$('#' + f_entity_desc.expanded.placeholder);
                $f_el.html('');
                var id_field = "id"
                if(f_entity_desc.id_field)
                     id_field = f_entity_desc.id_field;
                var entity = this.element_entity_map[element];
                var index = this.f_index.indexOf(entity);
                var collection = this.f_colls[index];
                
                $.each(this.model_json[element], function(index, f_json){
                    // console.log(f_json[id_field]);
                    // console.log(collection);
                    model = collection.get(f_json[id_field]);
                    if(model)
                    {
                        var t_json = model.toJSON();
                        t_json["index"] = index; 
                        $.each(f_entity_desc.expanded.extra_fields, function(index,field){
                            t_json[field] = f_json[field];
                        });
                        console.log(t_json);
                        $f_el.append(expanded_template(t_json));    
                    }
                });
                $(".chzn-select").chosen();
                $(".date-picker")
                    .datepicker({
                        format: 'yyyy-mm-dd'
                    }).on('changeDate', function(ev){
                        $(this).datepicker('hide');
                    });
                this.expanded = element;
                if(this.num_sources[element]<=0)
                    this.foreign_elements_rendered[element] = true;
            }
            else if(f_entity_desc.expanded)
            {
                console.log("ADD CASE, EXPANDED, Not Yet RENDERED");
                var expanded_template  = _.template($('#'+f_entity_desc.expanded.template).html());
                $f_el = this.$('#' + f_entity_desc.expanded.placeholder);
                $f_el.html('');
                $.each(model_array,function(index, f_model){
                    var t_json = f_model.toJSON();
                    t_json["index"] = index; 
                    $f_el.append(expanded_template(t_json));    
                });
                this.expanded = element;
                $(".chzn-select").chosen();
                $(".date-picker")
                    .datepicker({
                        format: 'yyyy-mm-dd'
                    }).on('changeDate', function(ev){
                        $(this).datepicker('hide');
                    });
                // this.foreign_elements_rendered[element] = true;
            }
            else{
                console.log("NOT EXPANDED");
                $f_el = this.$('#' + f_entity_desc.placeholder);
                if($f_el.is('select[multiple]'))
                    $f_el.html('');    
                else
                    $f_el.html(options_inner_template({
                            id: "",
                            name: "------------"
                    }));
                $.each(model_array,function(index, f_model){
                    var f_json = f_model; 
                    if(f_model instanceof Backbone.Model)
                        f_json = f_model.toJSON();
                    $f_el.append(options_inner_template({
                        id: parseInt(f_json["id"]),
                        name: f_json[f_entity_desc.name_field]
                    }));    
                });
                // console.log("ADD/EDIT: " + f_entity_desc.placeholder + " populated");
                 $f_el.prop("disabled", false);
                 $f_el.trigger("liszt:updated");
            }
            // if(this.edit_case && this.num_f_elems>=0)
//             {
//                 console.log("SYPHONING");
//                 Backbone.Syphon.deserialize(this, this.model_json);
//             }
            if(this.edit_case && !this.foreign_elements_rendered[element] &&!f_entity_desc.expanded)
            {
                var t_json = {};
                t_json[element] = this.model_json[element]
                    
                // t_json = {t_json};
                // Backbone.Syphon.deserialize(this, t_json);
                // console.log("FORM: putting in value of -"+element);
                this.$('form [name='+element+']').val(this.model_json[element]).change();
                this.$('form [name='+element+']').trigger("liszt:updated");
                if(this.num_sources[element]<=0)
                    this.foreign_elements_rendered[element] = true;
            }
        },
                        
        render_foreign_entity: function(collection, options) {
            console.log(this.num_f_elems);
            // console.log("ADD/EDIT: rendering foreign entity");
            for(element in this.foreign_entities[collection.storeName])
            {
                this.num_f_elems--; 
                
            }
            
            if(this.num_f_elems==0)
            {
                for(element in this.foreign_elements_rendered)
                {
                    var entity = this.element_entity_map[element];
                    if(this.foreign_entities[entity][element]["dependency"])
                    {
                
                    }
                    else{
                        var index = this.f_index.indexOf(entity);
                        var collection1 = this.f_colls[index];
                        this.fill_foreign_entity(element, collection1.toArray());
                    }
                }
            }   
        },

        normalize_json: function(d_json){
            console.log("FORM: Before Normalised json = "+JSON.stringify(d_json));      
            var f_entities = this.foreign_entities;
            for (member in f_entities) {
                for(element in f_entities[member])
                {
                    if(this.foreign_entities[member][element].expanded)
                    {
                        
                    }
                    else if (element in d_json) {
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
            console.log("FORM: Before DNormalising json - "+JSON.stringify(n_json))
            var f_entities = {};    
            if(this.bulk)
                f_entities = this.bulk.foreign_fields;
            else            
                f_entities = this.foreign_entities;
            var c=0;
            console.log(f_entities);
            for (member in f_entities) {
                for(element in f_entities[member])
                {
                    if(f_entities[member][element].expanded)
                    {
                        for(el in f_entities[member][element].expanded.denormalize)
                        {
                            var d_obj = f_entities[member][element].expanded.denormalize;
                            if (n_json[element] instanceof Array) {
                                $.each(n_json[element], function(ind, obj){
                                    var id = obj[el];
                                    var index = obj["index"];
                                    var tr_el = $('tr[index='+index+']');
                                    var label = $(tr_el).find('select option:selected').text();
                                    // console.log((sel_el));
                                    // var label = $(sel_el)
                                    obj[el]={};
                                    obj[el]["id"] = id;
                                    obj[el][d_obj[el]["name_field"]] = label;
                                    // delete obj["index"];
                                });    
                            }
                        }
                    }
                    else if (this.bulk)
                    {
                        var name_field = f_entities[member][element]["name_field"];
                        var that = this;
                        $.each(n_json.bulk, function(ind, obj){
                            var id = obj[element];
                            var index = obj["index"];
                            console.log("index = "+index);
                            var tr_el = $('tr[index='+index+']');
                            var dom_el = $('tr[index='+index+']').find('[name='+element+index+']');
                            var label = null;
                            var el_dict = {};
                            if($(dom_el).is("select"))
                            {
                                label = $(tr_el).find('select[name='+element+index+'] option:selected').text();
                                el_dict["id"] = parseInt(id);
                                el_dict[name_field] = label;   
                                
                            }
                            else if($(dom_el).is("input"))
                            {
                                var index = that.f_index.indexOf(member);
                                console.log(index);
                                
                                var collection1 = that.f_colls[index];
                                console.log(element);
                                console.log(collection1);
                                var model = collection1.where({
                                    id: parseInt(id)
                                })[0];
                                el_dict["id"] = parseInt(id);
                                el_dict[name_field] = model.get(f_entities[member][element]["name_field"]);    
                            }
                            // console.log((sel_el));
                            // var label = $(sel_el)
                            console.log(el_dict);          
                            obj[element] = el_dict;
                            console.log(JSON.stringify(obj));
                            // delete obj["index"];
                            console.log(JSON.stringify(obj));
                            
                                
                        });
                        
                        
                        
                    }
                    else if (element in n_json) {
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
                                // var entity = this.f_colls[c].where({
//                                     id: id
//                                 })[0];
//                                 n_json[element] = {};
//                                 n_json[element]["id"] = id;
//                                 n_json[element][name_field] = entity.get(f_entities[member][element]["name_field"]);    
                                // var tr_el = $('tr[index='+index+']');
                                //var label = $(tr_el).find('select option:selected').text();
                                // var sel_el = $('select[name='+element+'] option:selected').text(); 
                                n_json[element] = {};
                                n_json[element]["id"] = id;
                                n_json[element][name_field] = $('select[name='+element+'] option:selected').text();     
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
            console.log("FORM: After DNormalising json - "+JSON.stringify(n_json))
            
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
                    
                    else if(object_json[member]===""||object_json[member]==null||object_json[member]==undefined)
                    {
                        object_json[member] = null
                    }
                    if(object_json[member]==null)
                    {
                        if(this.$('[name='+member+']').is('select[multiple]'))
                        {
                            object_json[member] = [];
                        }
                    }
                }    
            console.log("FORM: After cleaning json - "+JSON.stringify(object_json))
                
        },  
        
        show_errors: function(errors){
            console.log("FORM: in show errors");
            var error_str = "";
            console.log("FORM: SHOWERROR: ");
            this.$('#form_errors').html(errors);
        },        
        
        parse_inlines: function(raw_json){
            console.log("FORM: fetching inlines");
            var all_inlines = $('#inline_body tr');    
            raw_json["inlines"] = [];
            var that = this;
            var inline_attrs = [];
            $.each(all_inlines,function(index, inl){
                var inl_obj = {};
                var ignore = true;
                if($(inl).attr("model_id"))
                    inl_obj.id = parseInt($(inl).attr("model_id"));
                $(inl).find(':input').each(function() {
                    if(!$(this).attr('name'))
                        return;
                    else
                        inline_attrs.push($(this).attr("name"));    
                    var attr_name = $(this).attr("name").replace(new RegExp("[0-9]", "g"), "");
    				switch(this.type) {
    					case 'password':
    					case 'select-multiple':
    					case 'select-one':
    					case 'text':
    					case 'textarea':
    						inl_obj[attr_name] = $(this).val();
    						break;
    					case 'checkbox':
    					case 'radio':
    						inl_obj[attr_name] = this.checked;
    				}
                    if(inl_obj[attr_name]!="")
                        ignore = false;
                });
                if(!ignore)
                    raw_json["inlines"].push(inl_obj);
            });
            
            //remove inline attrs from raw_json...let them be inside raw_json.inlines only
            $.each(inline_attrs,function(index,attr){
                delete raw_json[attr];
            });
            console.log(inline_attrs);
            
            
        },
        
        parse_expanded: function(raw_json){
            console.log("FORM: fetching expandeds");
            var element = this.expanded;
            var entity = this.element_entity_map[element];
            var desc = this.foreign_entities[entity][element]
            console.log("FORM:expande desc -" +JSON.stringify(desc));   
            var placeholder = desc.expanded.placeholder; 
            var all_inlines = $('#'+placeholder+ ' tr');    
            raw_json[element] = [];
            var that = this;
            var inline_attrs = [];
            $.each(all_inlines,function(index, inl){
                var inl_obj = {};
                inl_obj["index"] = $(inl).attr("index");
                var inputs = $(inl).find("input");
                var ignore = true;
                // if($(inl).attr("model_id"))
                //     inl_obj.id = parseInt($(inl).attr("model_id"));
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
                if(!ignore)
                    raw_json[element].push(inl_obj);
                // console.log($(inl).serializeArray());    
            });
            
            //remove inline attrs from raw_json...let them be inside raw_json.inlines only
            $.each(inline_attrs,function(index,attr){
                delete raw_json[attr];
            });
            // console.log(inline_attrs);    
        },  
              
        
        parse_bulk: function(raw_json){
            console.log("FORM: fetching bulks");
            var all_inlines = $('#bulk tr');    
            raw_json["bulk"] = [];
            var that = this;
            $.each(all_inlines,function(index, inl){
                var inl_obj = {};
                inl_obj["index"] = $(inl).attr("index");
                $(inl).find(':input').each(function() {
                    if(!$(this).attr('name'))
                        return;
                    var attr_name = $(this).attr("name").replace(new RegExp("[0-9]", "g"), "");
    				switch(this.type) {
    					case 'password':
    					case 'select-multiple':
    					case 'select-one':
    					case 'text':
    					case 'textarea':
    						inl_obj[attr_name] = $(this).val();
    						break;
    					case 'checkbox':
    					case 'radio':
    						inl_obj[attr_name] = this.checked;
    				}
                    if(inl_obj[attr_name]!="")
                        ignore = false;
                });
                if(!ignore)
                    raw_json["bulk"].push(inl_obj);
            });
        },
        
        
        save: function() {
            if(this.bulk)
            {
                this.final_json= {};
                this.parse_bulk(this.final_json);
                console.log(JSON.stringify(this.final_json));
                var that = this;
                // $.each(this.final_json.bulk, function(index, obj){
                    that.clean_json(this.final_json);
                    that.denormalize_json(this.final_json);
                // });
            }
            else
            {
                this.final_json = Backbone.Syphon.serialize(this);
                this.clean_json(this.final_json);
                if(this.expanded)
                {
                    this.parse_expanded(this.final_json);
                }
                this.denormalize_json(this.final_json);
                if(this.inline)
                    this.parse_inlines(this.final_json);
                this.final_json = $.extend(this.model_json, this.final_json);
            }

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
            this.trigger("save_clicked",ev_res);
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
            this.trigger("button2_clicked",ev_res);
        }


    });

    // Our module now returns our view
    return ShowAddEditFormView;
});

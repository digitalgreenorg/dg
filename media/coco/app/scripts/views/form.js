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
        template : '#form_template',         
        options_inner_template : _.template($('#options_template')
            .html()),
        
        //would be called when render is called       
        serialize: function(){
            var s_passed = this.options.serialize;
            s_passed["form_template"] = this.form_template;    
            s_passed["inline"] = (this.inline) ? true: false;
            s_passed["entity_name"] = this.entity_name;
            return s_passed;
        },
        
        /* 
        Identifies the action of this form - add/ edit_id/ edit_json  
        Sets the result on the view object 
        this.edit_case_id, this.edit_case_json, this.edit_case
        */
        identify_form_action: function(params){
            // There are two ways in which edit is true - when the ID is given, and the second is when a json is given(LIMIT: can be add too if json is missing id?).
            this.edit_case = false;
            this.edit_id = null;
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
        },
        
        /*
        Refactor possible
        Reads entity_config and sets basic properties on view object for easy access
        */
        read_form_config: function(params){
            this.entity_name = params.entity_name;
            this.entity_config = all_configs[this.entity_name];
            //default locations - 
            this.foreign_entities = this.entity_config.foreign_entities;
            this.inline = this.entity_config.inline;
            this.bulk = this.entity_config.bulk;
            if(this.edit_case)
            {
                this.form_template = $('#' + this.entity_config.edit_template_name).html();
                if(this.entity_config.edit)
                {
                    this.foreign_entities = this.entity_config.edit.foreign_entities;
                    this.inline = this.entity_config.edit.inline;
                    this.bulk = this.entity_config.edit.bulk;
                }
            }
            else
            {
                this.form_template = $('#' + this.entity_config.add_template_name).html();
                if(this.entity_config.add)
                {
                    this.foreign_entities = this.entity_config.add.foreign_entities;
                    this.inline = this.entity_config.add.inline;
                    this.bulk = this.entity_config.add.bulk;
                }
            }
        },
        
        /*
        Relies on view object's context 
        Gets foreign entities, create their offline collection to be fetched in afterRender
        Sets up datastructures to setup in-form change events
        Shamelessly polluting the view object
        */
        setup_foreign_elements: function(){
            this.f_colls = []; //stores the foreign entities' collections
            //TODO: get rid of this
            this.f_index = []; //stores the index of an entity to access its collection in f_colls
            this.source_dependents_map = {}; //stores the dependency mapping between form elements
            this.element_entity_map={}; //stores the mapping between foreign element and their entity
            this.foreign_elements_rendered = {};  //stores whether a foreign element has been rendered
            this.num_sources = {};  //stores the number of sources for a dependent element
            //create a collection for each distinct entity, put them in this.f_colls, remem their index in f_colls using f_index
            for(f_entity in this.foreign_entities){
                var f_collection = Offline.create_b_collection(f_entity, {
                    comparator: function(model){
                        return model.get(all_configs[this.storeName].sort_field)
                    }
                });
                this.f_index.push(f_entity);
                this.f_colls.push(f_collection);
                //create entity_map, dependency map, foreign_elements_rendered, for each foreign element
                for(var element in this.foreign_entities[f_entity])
                {
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
                            var source_elm = dep.source_form_element;
                            if(source_elm in that.source_dependents_map)
                                that.source_dependents_map[source_elm].push(element);
                            else{
                                that.source_dependents_map[source_elm] = [];
                                that.source_dependents_map[source_elm].push(element);
                            }
                        });
                        console.log("source_dependents_map = "+JSON.stringify(this.source_dependents_map));    
                    }
                    
                }
            }
        },
        
        /*
        params = {
            serialiaze:{
                button1: "...",     //name of first button, not shown if ==""
                button2: "..."      //name of sec button, not shown if =="" 
            },
            entity_name:,           //name of entity to be added/edited
            model_id:,              //id of model if edit case
            model_json:,            //json of model to be shown in edit form - used when json!= json(model_id)
        }
        */
        initialize: function(params) {
            console.log("ADD/EDIT: params to add/edit view: ");
            console.log(params);
            this.final_json = null;
            _.bindAll(this);
            
            //read entity_config and sets main properties on view object for easy access
            this.read_form_config(params);

            //sets this.edit_case, and  this.edit_case_id, or this.edit_case_json
            this.identify_form_action(params);  

            //reads this.foreign_entities and setsup the collections, source_dependents_map
            this.setup_foreign_elements();
        },
        
        afterRender: function() {
            var that = this;
            
            //no foreign element has been rendered yet so disabling all - they get enabled as and when they get rendered
            this.disable_foreign_elements();

            //start in-form change events
            this.start_change_events();
            
            //fetch all foreign collections and render them when all are fetched
            this.fetch_and_render_foreign_entities();

            //if edit case - fill form with the model    
            if(this.edit_case)
                this.render_edit_model();

            //if inline case - render inlines
            if(this.inline)
                this.render_inlines();
            
            // call validator on the form
            this.initiate_form_field_validation();
            
            this.initiate_form_widgets();
        },
        
        //fetches all foreign collections and renders them when all are fetched
        fetch_and_render_foreign_entities: function(){
            var for_entities_fetch_dfds = [] 
            for (var i = 0; i < this.f_colls.length; i++) {
                console.log("fetching f coll");
                var f_dfd = this.f_colls[i].fetch();
                for_entities_fetch_dfds.push(f_dfd);    
            }
            $.when.apply($,for_entities_fetch_dfds)
                .done(this.render_non_dep_for_elements)
                .fail(function(){
                    //TODO: handle error callback
                    alert("Atleast one foreign entity could not be fetched!");
                })
        },
        
        //fill non-dependent foreign elements - dependent gets filled on change events
        render_non_dep_for_elements: function(){
            console.log("Rendering non dependent f elements");
            _.each(this.element_entity_map, function(entity,element){
                if(!this.foreign_entities[entity][element]["dependency"])
                    this.render_foreign_element(element, this.get_collection_of_element(element).toArray());    
            }, this);
        },
        
        // fetch offline model and inlines and render them into form
        render_edit_model: function(){
            var that = this;
            if (this.edit_case_json) {
                this.normalize_json(this.model_json);
                this.fill_form();           
            } 
            else if (this.edit_case_id) 
            {
                Offline.fetch_object(this.entity_config.entity_name, "id", this.edit_id)
                    .done(function(model) {
                        console.log("EDIT: edit model fetched");
                        that.model_json = model.toJSON();
                        that.normalize_json(that.model_json);
                        that.fill_form();
                    })
                    .fail(function() {
                        //TODO: error handling
                        console.log("ERROR: EDIT: Edit model could not be fetched!");
                        alert("ERROR: EDIT: Edit model could not be fetched!");
                    });
            }
        },
        
        //disable dropdowns of all foreign elements
        disable_foreign_elements: function(){
            for (f_entity in this.foreign_entities) {
                for(element in this.foreign_entities[f_entity])
                {
                    if(!this.foreign_entities[f_entity][element].expanded)
                    {
                        this.$('[name='+element+']').prop("disabled", true);
                    }
                }
            }
        },
        
        //render header, empty inlines if add case
        render_inlines: function(){
            var that = this;
            this.$('#inline_header').html($('#'+this.inline.header).html());
            //if add case put in empty inlines, edit case would get handled when model is being put it
            if(!this.edit_case)
                this.append_new_inlines(this.inline.default_num_rows);
            else if(this.edit_case_id)
            {
                console.log("FORM:EDIT: Fteching inline collection");
                Offline.fetch_collection(this.inline.entity)
                    .done(function(collection){
                        // id-json dictionary of inline models - later used to extend the modified inlines
                        that.inl_models_dict = {};
                        var inl_models = collection.filter(function(model){
                            if(model.get(that.inline.joining_attribute.inline_attribute).id == that.edit_id)
                            {
                                that.inl_models_dict[model.get("id")] = model.toJSON();
                                return true 
                            }
                            return false;    
                        });
                        console.log(inl_models);
                        that.fill_inlines(inl_models);
                    })
                    .fail(function(){
                        console.log("ERROR: EDIT: Inline collection could not be fetched!");
                    });
            }
            //not showing the inlines in case of edit_case_json            
        },
        
        append_new_inlines: function(num_rows){
            var inline_t  = _.template($('#'+this.inline.template).html());
            //TODO: gotta start index from the last index already in dom for 'add more rows feature' 
            for(var i=0;i<num_rows;i++)
            {
                var tr = $(inline_t({index:i}));
                this.$('#inline_body').append(tr);
                tr.on('change', this.switch_validation_for_inlines);
            }
        },
        
        // to prevent validation of empty inline rows
        switch_validation_for_inlines: function(ev){
            var elem = ev.delegateTarget;   //get the changed row
            var empty = true;
            $(elem).find(':input').each(function() {
                if($(this).val())
                    empty = false;
            });
            if(!empty)
            {
                $(elem).find(':input').each(function() {
                    $(this).removeClass("donotvalidate");
                });
            }
            else
            {
                $(elem).find(':input').each(function() {
                    $(this).addClass("donotvalidate");
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
                $(filled_tr).on('change', that.switch_validation_for_inlines);
            });
        },    
        
        //takes a jquery object containgg form elements and a json. Fills all elements with the corrsponding value in json  
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

        start_change_events: function(){
            for(element in this.source_dependents_map)
            {
                console.log("creating changeevent for - "+element);
                this.$('[name='+element+']').change(this.render_dep_for_elements);
            }
        },
        
        initiate_form_field_validation: function(){
            var that = this;
            var validate_obj = $.extend(this.entity_config.form_field_validation,{
                "submitHandler" : function() {
                     that.save();
                 }
            });
            this.$('form')
                .validate(validate_obj);
        },
        
        initiate_form_widgets: function(){
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
        },
        
        get_collection_of_element : function(element){
            var entity = this.element_entity_map[element];  
            var index = this.f_index.indexOf(entity);   
            return this.f_colls[index];   
        },
        
        get_sources_of_element: function(element){
            var entity = this.element_entity_map[element];  
            return this.foreign_entities[entity][element].dependency;
        },
        
        get_curr_value_of_element: function(element){
            return $('[name='+element+']').val();
        },
        
        render_dep_for_elements: function(ev){
            var source = $(ev.target).attr("name"); //source changed
            console.log("FILLING DEP ENTITIES OF -"+source);
            // Iterate over its dependents
            _.each(this.source_dependents_map[source], function(dep_el){
                var filtered_models = this.filter_dep_for_element(dep_el);
                this.render_foreign_element(dep_el, filtered_models);
            }, this);
        },    
        
        // Fully Reset the dependent foreign element by looking at all its sources.  
        filter_dep_for_element: function(element){
            //get dependent element's entity's collection - to be filtered
            var dep_collection = this.get_collection_of_element(element);   
            var all_sources = this.get_sources_of_element(element);   // get all sources of this element - to filter by
            var final_models = [];  //model array to be finally inserted into dom
            var that = this;
            
            if(!dep_collection.length)
                return [];
                
            $.each(all_sources, function(index, dep_desc){
                var dep_attr = dep_desc.dep_attr;
                var source_form_element = dep_desc.source_form_element;
                var filtered_models = [];
                
                //LIMITS: source can't be an expanded right now, bcoz won't get its value
                var source_curr_value = that.get_curr_value_of_element(source_form_element);   
                if(!source_curr_value)
                    return;
                else if(!(source_curr_value instanceof Array))  
                {
                    //if source is single select - convert its value to array - like a multiselect
                    var temp = source_curr_value;
                    source_curr_value = [];    
                    source_curr_value.push((temp));
                }
                
                // many-to-many relation between source and dependent
                if(dep_collection.at(0).get(dep_desc.dep_attr) instanceof Array)
                {
                    filtered_models = dep_collection.filter(function(model){
                       var exists = false;
                       //LIMITS: array assumed to contain objects - its an array so possibly other case not possible
                       $.each(model.get(dep_desc.dep_attr),function(index, object){
                            if($.inArray(String(object.id), source_curr_value)>-1)
                                exists = true;
                       });
                       return exists;
                    });
                }
                else
                {
                    filtered_models = dep_collection.filter(function(model){
                        var exists = false;
                        var compare = null;
                        if(typeof model.get(dep_desc.dep_attr) == "object")
                            compare = model.get(dep_desc.dep_attr).id; 
                        else
                            compare = model.get(dep_desc.dep_attr)
                            
                        if(dep_desc.src_attr&&dep_desc.src_attr!="id")
                        {
                            var s_collection = that.get_collection_of_element(source_form_element);
                            var s_model = s_collection.get(parseInt(source_curr_value[0]));
                            if(s_model.get(dep_desc.src_attr) instanceof Array)
                            {
                                //LIMITS: array assumed to contain objects - its an array so possibly other case not possible
                                $.each(s_model.get(dep_desc.src_attr), function(index, src_compare){
                                    if(compare == src_compare.id)
                                        exists = true;
                                });
                            }
                            return exists;
                        }        
                        else
                        {
                            if(!($.inArray(String(compare), source_curr_value)==-1))
                                exists = true;
                            return exists;
                        }            
                    });
                }
                final_models = final_models.concat(filtered_models);
            });
            return final_models;
        },
          
        filter_model_array: function(model_array, filter){
            var filter_attr = filter.attr;
            var filter_value = filter.value;
            filtered = [];
            $.each(model_array, function(index, obj){
                //TODO: assumed to be an object
                if(obj.get(filter_attr).id == filter_value)
                {
                    filtered.push(obj);
                }
            });
            return filtered;
        },
          
        render_foreign_element: function(element, model_array){
            console.log("FILLING FOREIGN ENTITY - "+element);
            var that = this;
            this.num_sources[element]--;
            var f_entity_desc = this.foreign_entities[this.element_entity_map[element]][element];
            
            //if any defined, filter the model array before putting into dom 
            if(f_entity_desc.filter)
                model_array = this.filter_model_array(model_array, f_entity_desc.filter);
            
            if(f_entity_desc.expanded)
            {
                var expanded_template  = _.template($('#'+f_entity_desc.expanded.template).html());
                $f_el = this.$('#' + f_entity_desc.expanded.placeholder);
                $f_el.html('');
                this.expanded = element; //LIMIT: there can be only one expanded f element!
                
                //Its edit case and edit model is not yet rendered - so render it
                if(this.edit_case && !this.foreign_elements_rendered[element])
                {
                    var id_field = "id"
                    if(f_entity_desc.id_field)
                        id_field = f_entity_desc.id_field;
                        var collection = this.get_collection_of_element(element);                
                    $.each(this.model_json[element], function(index, f_json){
                        model = collection.get(f_json[id_field]);
                        if(!model)
                            return;
                        var t_json = model.toJSON();
                        t_json["index"] = index; 
                        $.each(f_entity_desc.expanded.extra_fields, function(index,field){
                            t_json[field] = f_json[field];
                        });
                        console.log(t_json);
                        $f_el.append(expanded_template(t_json));    
                    });
                    if(this.num_sources[element]<=0)
                        this.foreign_elements_rendered[element] = true;
                }
                else
                {
                    $.each(model_array,function(index, f_model){
                        var t_json = f_model.toJSON();
                        t_json["index"] = index; 
                        $f_el.append(expanded_template(t_json));    
                    });
                }    
                this.initiate_form_widgets();
            }
            else
            {
                console.log("NOT EXPANDED");
                $f_el = this.$('#' + f_entity_desc.placeholder);
                if($f_el.is('select[multiple]'))
                    $f_el.html('');    
                else
                    $f_el.html(this.options_inner_template({
                        id: "",
                        name: "------------"
                    }));
                $.each(model_array,function(index, f_model){
                    var f_json = f_model; 
                    if(f_model instanceof Backbone.Model)
                        f_json = f_model.toJSON();
                    $f_el.append(that.options_inner_template({
                        id: parseInt(f_json["id"]),
                        name: f_json[f_entity_desc.name_field]
                    }));    
                });
                $f_el.prop("disabled", false);
                $f_el.trigger("liszt:updated");

                //select the options selected in edit model
                if(this.edit_case && !this.foreign_elements_rendered[element])
                {
                    this.$('form [name='+element+']').val(this.model_json[element]).change();
                    this.$('form [name='+element+']').trigger("liszt:updated");
                    if(this.num_sources[element]<=0)
                        this.foreign_elements_rendered[element] = true;
                }
            }
        },
                        
        normalize_json: function(d_json){
            console.log("FORM: Before Normalised json = "+JSON.stringify(d_json));      
            var f_entities = this.foreign_entities;
            for (member in f_entities) {
                for(element in f_entities[member])
                {
                    if((element in d_json)&&!(f_entities[member][element].expanded)) 
                    {
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
                else if(!object_json[member])
                {
                    object_json[member] = null
                    if(this.$('[name='+member+']').is('select[multiple]'))
                    {
                        object_json[member] = [];
                    }
                }
            }    
            console.log("FORM: After cleaning json - "+JSON.stringify(object_json))
                
        },  
        
        
        set_submit_button_state: function(state){
            if(state=="disabled")
                this.$(".action_button").attr("disabled",true);    
            else
                this.$(".action_button").button(state);    
        },
        //server err eg. - {"mediator": {"__all__": ["Animator with this Name, Gender and Partner already exists."]}}
        show_errors: function(errors, disable_submit){
            // used to clear form errors 
            if(errors==null)
            {
                $('.form_error').remove();
                $('.error').removeClass("error");
                return;
            }
            
            this.set_submit_button_state('reset');
            if(disable_submit)
                this.set_submit_button_state('disabled');
            
            
            if(typeof(errors)!=="object")
                errors = $.parseJSON(errors);
            console.log("Showing this error");
            console.log(errors);
            _.each(errors, function(errors_obj, parent){
                var parent_el = this.$('[name='+parent+']');
                $.each(errors_obj, function(error_el_name, error_list){
                    var error_ul = null;
                    all_li = "<li>"+error_list.join("</li><li>")+"</li>";
                    error_ul = "<tr class='form_error'><td colspan='100%'><ul>" + all_li + "</ul></td></tr>";
                    if(error_el_name=="__all__")
                    {
                        parent_el.before(error_ul);     //insert error message
                        parent_el.addClass("error");    //highlight
                    }
                    else
                    {
                        //NOt Done
                        var error_el = parent_el.find('[name='+error_el_name+']');
                        error_el.after(error_ul);    //insert error message
                        error_el
                            .parent('div')
                            .parent('div')
                            .addClass("error");     //highlight
                    }
                });
            }, this);
            
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
                inl_obj.index = $(inl).attr("index");
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
            var all_inlines = $('#bulk tr').not(".form_error");    
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
        
        //preserve the background fields - not entered through form
        extend_edit_json: function(o_json){
            o_json = $.extend(true, this.model_json, o_json);
            if(this.inline)
            {
                _.each(o_json.inlines, function(inl, index){
                    var old_json = this.inl_models_dict[inl.id];
                    o_json.inlines[index] = $.extend(true, old_json, inl);
                }, this);
            }
            return o_json;
        },
        
        save: function() {
            this.show_errors(null);    //clear old errors
            this.set_submit_button_state('loading'); //set state to loading
            
            if(this.bulk)
            {
                this.final_json= {};
                this.parse_bulk(this.final_json);
                // $.each(this.final_json.bulk, function(index, obj){
                // });
            }
            else
            {
                this.final_json = Backbone.Syphon.serialize(this);
                if(this.expanded)
                    this.parse_expanded(this.final_json);
                if(this.inline)
                    this.parse_inlines(this.final_json);
            }

            this.clean_json(this.final_json);
            this.denormalize_json(this.final_json);
            if(this.edit_case)
                this.final_json = this.extend_edit_json(this.final_json);
            var ev_data = {
                context: this,
            };
            this.trigger("save_clicked",ev_data);
        },

        button2_clicked: function() {
            var ev_data = {
                context: this,
            };
            this.trigger("button2_clicked",ev_data);
        }


    });

    // Our module now returns our view
    return ShowAddEditFormView;
});

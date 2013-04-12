define(['jquery', 'configs', 'backbone', 'indexeddb_backbone_config'

], function($, configs, pa, indexeddb) {
    var offline_to_online = {
        
        convert : function(json, f_entities) {
        var dfd = new $.Deferred();
    
        console.log("FORMCONTROLLER:OFFLINE_TO_ONLINE: here am i");
        // var f_entities = this.params.initialize.view_configs["foreign_entities"];
        // var f_entities = f_entity_desc;
        // if(this.form.bulk)
        // {
        //     f_entities = this.form.bulk.foreign_fields;
        // }
        console.log("FORMCONTROLLER:OFFLINE_TO_ONLINE: foreign entities for the model under consideration" + JSON.stringify(f_entities));
        var online_json = $.extend(null, json); // making a copy of object json
        console.log("FORMCONTROLLER:OFFLINE_TO_ONLINE: json before converting" + JSON.stringify(json));
        // var num_mem = Object.keys(f_entities).length; // Number of foreign entities referenced in this model.
        var num_mem = 0;
        var convert_fields = [];
        for(member in f_entities)
        {
            for(element in f_entities[member])
            {
                convert_fields.push(element);
                num_mem++;
                if(f_entities[member][element].expanded&&!f_entities[member][element].only_render)
                {
                    if(f_entities[member][element].expanded.foreign_fields)
                    {
                        for(field in f_entities[member][element].expanded.foreign_fields)
                        {
                            num_mem++;
                            convert_fields.push(field);
                        }
                    }
                }
            }
        }
        
        console.log("FORMCONTROLLER:OFFLINE_TO_ONLINE: The convert fields = "+ convert_fields);
        console.log("FORMCONTROLLER:OFFLINE_TO_ONLINE: number of foreign elements - " + num_mem);
        if (!num_mem) {
            console.log("FORMCONTROLLER:OFFLINE_TO_ONLINE: no foreign entities to convert");
            // this.after_offline_to_online_success(online_json,json);
            // that.trigger("converted", {on_json:online_json, off_json:json});
            return dfd.resolve( {on_json:online_json, off_json:json} );
        } else {
            for (member in f_entities) {
                for(element in f_entities[member])
                {
                    // If this foreign entity is not present in the current object, continue.
                    if (!(element in online_json)) {
                        num_mem--;
                        if (!num_mem) {
                            console.log("FORMCONTROLLER:OFFLINE_TO_ONLINE: all converted");
                            // this.after_offline_to_online_success(online_json,json);
                            // that.trigger("converted", {on_json:online_json, off_json:json});
                            return dfd.resolve( {on_json:online_json, off_json:json} );
                        }
                        else
                            continue;
                    }
                    console.log("FORMCONTROLLER:OFFLINE_TO_ONLINE: converting " + element + " offline to online.");
                    if(online_json[element] instanceof Array)
                    {
                        console.log("FORMCONTROLLER:OFFLINE_TO_ONLINE: This foreign element is multiselect. Fetching its collection.");
                        var id_field = "id";
                        if(f_entities[member][element].id_field)
                        {
                            id_field  = f_entities[member][element].id_field;
                        }
                        var generic_offline_collection = Backbone.Collection.extend({
                            database: indexeddb,
                            storeName: member,
                            attribute: element,
                            id_field: id_field    
                        });
                        var f_collection = new generic_offline_collection();
                        var that = this;
                        f_collection.fetch({
                            success: function(collection){
                                console.log("FORMCONTROLLER:OFFLINE_TO_ONLINE : foreign collection successfully fetched");
                                var conv_array = [];
                                $.each(online_json[collection.attribute],function(index,object){
                                    console.log("FORMCONTROLLER:OFFLINE_TO_ONLINE: converting this object inside multiselect" + JSON.stringify(object));
                                    var model = collection.get(object[collection.id_field]);
                                    console.log("FORMCONTROLLER:OFFLINE_TO_ONLINE: fetched same object from collection" + JSON.stringify(model.toJSON()));
                                    var con_obj = $.extend(null,object);
                                    con_obj[collection.id_field] =   model.get("online_id"); 
                                    conv_array.push(con_obj);
                                    // object["id"] =   model.get("online_id");
                                });
                                online_json[collection.attribute] = conv_array;
                                console.log("FORMCONTROLLER:OFFLINE_TO_ONLINE: json after converting" + JSON.stringify(online_json));
                                num_mem--;
                                if (!num_mem) {
                                    console.log("FORMCONTROLLER:OFFLINE_TO_ONLINE: all converted");
                                    // that.after_offline_to_online_success(online_json,json);
                                    // that.trigger("converted", {on_json:online_json, off_json:json});
                                    return dfd.resolve( {on_json:online_json, off_json:json} );
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
                        f_model.set("id", parseInt(online_json[element]["id"]));
                        var that = this;
                        console.log(online_json[element]["id"]);
                        console.log(parseInt(online_json[element]["id"]));
                        
                        console.log("Fetching ths model - ");
                        console.log((f_model));
                        f_model.fetch({
                            success: function(model) {
                                console.log("FORMCONTROLLER:OFFLINE_TO_ONLINE: The foreign entity with the key mentioned fetched from IDB- " + JSON.stringify(model.toJSON()));
                                // online_json[model.attribute]["id"] =   model.get("online_id");
                                var con_obj = $.extend(null,online_json[model.attribute]);
                                con_obj["id"] =   model.get("online_id"); 
                                online_json[model.attribute] = con_obj;
                                // access the attribute name
                                console.log("FORMCONTROLLER:OFFLINE_TO_ONLINE: json after converting" + JSON.stringify(online_json));
                                num_mem--;
                                if (!num_mem) {
                                    console.log("FORMCONTROLLER:OFFLINE_TO_ONLINE: all converted");
                                    console.log("FORMCONTROLLER:OFFLINE_TO_ONLINE: original json - "+ JSON.stringify(json));
                                    console.log("FORMCONTROLLER:OFFLINE_TO_ONLINE: fully converted json - "+JSON.stringify(online_json))
                                    // that.after_offline_to_online_success(online_json,json);
                                    // that.trigger("converted", {on_json:online_json, off_json:json});
                                    return dfd.resolve( {on_json:online_json, off_json:json} );
                                }
                            },
                            error: function(error) {
                                console.log("FORMCONTROLLER:OFFLINE_TO_ONLINE: Unexpected Error : The foreign entity with the key mentioned does not exist anymore.");
                                //TODO: this model should be deleted from IDB and server ????
                                console.log(error);
                                alert("unexpected error. check console log "+error);
                                // that.form.show_errors("A foreign entity referenced does not exists in IDB. ")
                                $(notifs_view.el)
                                    .append(that.error_notif_template({
                                    msg: "A foreign entity referenced does not exists in IDB."
                                }));
                            }
                        });
                    }
                    
                    if(f_entities[member][element].expanded&&!f_entities[member][element].only_render)
                    {
                        if(f_entities[member][element].expanded.foreign_fields)
                        {
                            // TODO: proces these foreign fields
                            for(field in f_entities[member][element].expanded.foreign_fields)
                            {
                                var entity = f_entities[member][element].expanded.foreign_fields[field].entity_name;
                                // if(online_json[element][field] instanceof Array)
                                {
                                    var generic_offline_collection = Backbone.Collection.extend({
                                        database: indexeddb,
                                        storeName: entity,
                                        attribute: element,
                                        sub_attribute: field        
                                    });
                                    var f_collection = new generic_offline_collection();
                                    var that = this;
                                    console.log(entity);
                                    f_collection.fetch({
                                        success: function(collection){
                                            console.log("FORMCONTROLLER:OFFLINE_TO_ONLINE : foreign collection successfully fetched");
                                            var conv_array = [];
                                            var id_field = "id";
                                            $.each(online_json[collection.attribute],function(index,object){
                                                var field_object = object[field];
                                                console.log("FORMCONTROLLER:OFFLINE_TO_ONLINE: converting this object inside multiselect" + JSON.stringify(field_object));
                                                if(field_object[id_field])
                                                {
                                                    var model = collection.get(field_object[id_field]);
                                                    console.log("FORMCONTROLLER:OFFLINE_TO_ONLINE: fetched same object from collection" + JSON.stringify(model.toJSON()));
                                                    var con_obj = $.extend(null,field_object);
                                                    con_obj[id_field] =   model.get("online_id"); 
                                                    object[field] = con_obj;
                                                }
                                                // conv_array.push(con_obj);
                                                // object["id"] =   model.get("online_id");
                                            });
                                            console.log("FORMCONTROLLER:OFFLINE_TO_ONLINE: json after converting" + JSON.stringify(online_json));
                                            num_mem--;
                                            if (!num_mem) {
                                                console.log("FORMCONTROLLER:OFFLINE_TO_ONLINE: all converted");
                                                // that.after_offline_to_online_success(online_json,json);
                                                // that.trigger("converted", {on_json:online_json, off_json:json});
                                                return dfd.resolve( {on_json:online_json, off_json:json} );
                                            }            
                                        }
                                        
                                        //TODO: error callback
                                    });        
                                }
                            }
                        }
                    }
                }
            }
        }
    return dfd.promise();
    }
    
    }   
    
    
    return offline_to_online;

});

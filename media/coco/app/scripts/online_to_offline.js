define(['jquery', 'configs', 'backbone', 'indexeddb_backbone_config'

], function($, configs, pa, indexeddb) {
    var online_to_offline = {
        
        convert : function(json, f_entities) {
            var dfd = new $.Deferred();
            var that = this;
            console.log("FORMCONTROLLER:ONLINE_TO_OFFLINE: foreign entities for the model under consideration" + JSON.stringify(f_entities));
            var online_json = $.extend(true, null, json); // making a deep copy of object json
            console.log("FORMCONTROLLER:ONLINE_TO_OFFLINE: json before converting" + JSON.stringify(json));
            var field_dfds = [];
            for (member in f_entities) {
                for(element in f_entities[member])
                {
                    // If this foreign entity is not present in the current object, continue.
                    if (!(element in online_json)) {
                        continue;
                    }
                    console.log("FORMCONTROLLER:ONLINE_TO_OFFLINE: converting " + element + " offline to online.");
                    var id_field = "id";
                    if(f_entities[member][element].id_field)
                    {
                        id_field  = f_entities[member][element].id_field;
                    }
                    var field_desc = {entity_name:member, id_attribute:id_field};
                    
                    if(online_json[element] instanceof Array)   //multi-select dropdown
                    {
                        console.log("FORMCONTROLLER:ONLINE_TO_OFFLINE: This foreign element is multiselect.");
                        $.each(online_json[element],function(index,object){
                            field_dfds.push(that.convert_object(object,field_desc));
                        });
                    }
                    else   //single-select dropdown
                    {
                        console.log("FORMCONTROLLER:ONLINE_TO_OFFLINE: This foreign element is single select.");
                        field_dfds.push(that.convert_object(online_json[element],field_desc));
                    }
                
                    if(f_entities[member][element].expanded&&!f_entities[member][element].only_render) //expandeds
                    {
                        if(f_entities[member][element].expanded.foreign_fields) //contains foreign fields
                        {
                            // TODO: proces these foreign fields
                            for(field in f_entities[member][element].expanded.foreign_fields) //convert each field
                            {
                                var entity = f_entities[member][element].expanded.foreign_fields[field].entity_name;
                                field_desc = {entity_name: entity, id_attribute:"id"};
                                console.log("FORMCONTROLLER:ONLINE_TO_OFFLINE: This foreign element is expanded");
                                $.each(online_json[element],function(index,object){
                                    var field_object = object[field];
                                    if(field_object[id_field])
                                    {
                                        field_dfds.push(that.convert_object(field_object,field_desc));
                                    }
                                });
                            }
                        }
                    }
                }
            }
            
            if(field_dfds.length)
            {
                $.when.apply($,field_dfds)
                    .done(function(){
                        console.log("FORMCONTROLLER:ONLINE_TO_OFFLINE: Converted to this: "+JSON.stringify(online_json));
                        return dfd.resolve( {on_json:json, off_json:online_json} );
                    })
                    .fail(function(){
                        console.log("Atleast one of the foreign objects could not be resolved! Rejecting the dfd.");
                        return dfd.reject();
                    });
            }
            else
            {
                console.log("FORMCONTROLLER:ONLINE_TO_OFFLINE: Nothing to convert.");
                return dfd.resolve( {on_json:json, off_json:online_json} );
            }
            return dfd.promise();
        },
        
        convert_object: function(obj, field_desc){
            var dfd = new $.Deferred();
            var generic_model_offline = Backbone.Model.extend({
                database: indexeddb,
                storeName: field_desc.entity_name,
                // attribute: element    
            });
            var f_model = new generic_model_offline();
            f_model.set("online_id", parseInt(obj[field_desc.id_attribute]));
            var that = this;
            console.log("Fetching ths model - ");
            console.log(f_model);
            f_model.fetch({
                success: function(model) {
                    console.log("FORMCONTROLLER:ONLINE_TO_OFFLINE: The foreign entity with the key mentioned fetched from IDB- " + JSON.stringify(model.toJSON()));
                    obj[field_desc.id_attribute] = model.get("id"); 
                    // console.log("FORMCONTROLLER:ONLINE_TO_OFFLINE: object after converting" + JSON.stringify(obj));
                    return dfd.resolve();
                },
                error: function(error) {
                    console.log("FORMCONTROLLER:ONLINE_TO_OFFLINE: Unexpected Error : The foreign entity with the key mentioned does not exist anymore.");
                    //TODO: OOPS! What should be done now????
                    console.log(error);
                    alert("unexpected error. check console log "+error);
                    return dfd.reject();
                    // that.form.show_errors("A foreign entity referenced does not exists in IDB. ")
                    // $(notifs_view.el)
//                         .append(that.error_notif_template({
//                         msg: "A foreign entity referenced does not exists in IDB."
//                     }));
                }
            });
            return dfd.promise();
        }    
    
    }   
    
    
    return online_to_offline;

});

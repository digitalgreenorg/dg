define(['jquery', 'configs', 'backbone', 'indexeddb_backbone_config'

], function($, configs, pa, indexeddb) {
    var convert_namespace = {
        which_to_which: "offlinetoonline",
        conv_dict : {
            "onlinetooffline" : {
                replace_this : "online_id",
                replace_with : "id"
            },
            "offlinetoonline" : {
                replace_this : "id",
                replace_with : "online_id"
            }
        },

        get_id_field : function(entity, element, f_entities){
            return f_entities[entity][element].id_field||"id";
        },
        
        convert : function(json, f_entities, which_to_which) {
            var dfd = new $.Deferred();
            if(which_to_which)
                this.which_to_which = which_to_which;
            var that = this;
            var conv_json = $.extend(true, null, json); // making a deep copy of received json...this copy would be altered
            console.log("FORMCONTROLLER:convert_namespace: json before converting" + JSON.stringify(json));
            this.field_dfds = [];
            this.iterate_foreign_fields(conv_json, f_entities);
            
            var object_jsons = null;
            switch(this.which_to_which){
                case "onlinetooffline": 
                    object_jsons = {
                        off_json : conv_json,
                        on_json : json
                    }
                    break;
                default:
                    object_jsons = {
                        off_json : json,
                        on_json : conv_json
                    }
            }
            if(this.field_dfds.length)
            {
                $.when.apply($, this.field_dfds)
                    .done(function(){
                        return dfd.resolve(object_jsons);
                    })
                    .fail(function(){
                        return dfd.reject();
                    });
            }
            else
            {
                console.log("FORMCONTROLLER:convert_namespace: Nothing to convert.");
                return dfd.resolve(object_jsons);
            }
            
            return dfd.promise();
        },
        
        iterate_foreign_fields: function(json, f_entities){
            for (var entity in f_entities) {
                for(var element in f_entities[entity])
                {
                    if (!(json[element]))
                        continue;
                    var id_field = this.get_id_field(entity, element, f_entities);
                    var field_desc = {
                        entity_name : entity, 
                        id_attribute : id_field
                    };
                    
                    if(json[element] instanceof Array)   //multi-select dropdown
                        _.each(json[element],function(object, index){
                            this.field_dfds.push(this.convert_object(object, field_desc));
                        }, this);
                    else   //single-select dropdown
                        this.field_dfds.push(this.convert_object(json[element],field_desc));
                
                    if(f_entities[entity][element].expanded) //expandeds
                        if(f_entities[entity][element].expanded.foreign_entities) //contains foreign fields
                            _.each(json[element], function(object, index){
                                this.iterate_foreign_fields(object, f_entities[entity][element].expanded.foreign_entities);
                            }, this);
                }
            }
        },
        
        convert_object: function(obj, field_desc){
            console.log("ConvertNamespace: converting object",JSON.stringify(obj), JSON.stringify(field_desc));
            var dfd = new $.Deferred();
            if(!obj[field_desc.id_attribute])
                return dfd.resolve();
            var generic_model_offline = Backbone.Model.extend({
                database: indexeddb,
                storeName: field_desc.entity_name,
            });
            var f_model = new generic_model_offline();
            f_model.set(this.conv_dict[this.which_to_which].replace_this, parseInt(obj[field_desc.id_attribute]));
            var that = this;
            f_model.fetch({
                success: function(model) {
                    obj[field_desc.id_attribute] = model.get(that.conv_dict[that.which_to_which].replace_with); 
                    return dfd.resolve();
                },
                error: function(model, error) {
                    //TODO: OOPS! What should be done now????
                    alert("unexpected error. check console log "+error);
                    return dfd.reject(error);
                }
            });
            return dfd.promise();
        }    
    
    }   
    
    
    return convert_namespace;

});

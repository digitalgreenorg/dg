/*takes an object and the foreign entities description for the object. Using the descrip iterates over json,
identifies the foreign values and denormalizes them. Same object passed is denormalised. New object is not created.*/

define(['jquery', 'configs', 'backbone', 'indexeddb_backbone_config'],

function($, configs, pa, indexeddb) {
    var denormalize = {
        _get_id_field: function(entity, element, f_entities) {
            return f_entities[entity][element].id_field || "id";
        },

        _get_name_field: function(entity, element, f_entities) {
            return f_entities[entity][element].name_field;
        },

        denormalize: function(json, f_entities) {
            console.log("FORMCONTROLLER:denormalize: json before denormalizing" + JSON.stringify(json));
            var that = this;
            this.field_dfds = [];
            this._iterate_foreign_fields(json, f_entities);
            return $.when.apply($,this.field_dfds);
        },

        _iterate_foreign_fields: function(json, f_entities) {
            for (var entity in f_entities) {
                for (var element in f_entities[entity]) {
                    if (!(json[element])) 
                    {
                        json[element] = {};
                        continue;
                    }
                    
                    if(f_entities[entity][element].expanded)
                    {
                        if (f_entities[entity][element].expanded.foreign_entities){
                            //expanded contains foreign fields
                            _.each(json[element], function(object, index) {
                                this._iterate_foreign_fields(object, f_entities[entity][element].expanded.foreign_entities);
                            }, this);
                        }
                        return;
                    }
                        
                    var id_field = this._get_id_field(entity, element, f_entities);
                    var name_field = this._get_name_field(entity, element, f_entities);
                    var field_desc = {
                        entity_name: entity,
                        id_attribute: id_field,
                        name_attribute: name_field
                    };

                    if (json[element] instanceof Array) //multi-select dropdown
                    {
                        _.each(json[element], function(val, index) {
                            json[element][index] = {};
                            json[element][index][id_field] = parseInt(val);
                            this.field_dfds.push(this._denormalize_object(json[element][index], field_desc));
                        }, this);
                    }
                    else //single-select dropdown
                    {
                        var temp = {};
                        temp[id_field] = parseInt(json[element]);
                        json[element] = temp;
                        this.field_dfds.push(this._denormalize_object(json[element], field_desc));
                    }

                }
            }
        },

        _denormalize_object: function(obj, field_desc) {
            console.log("Denormalize: dnormalizing object", JSON.stringify(obj), JSON.stringify(field_desc));
            var dfd = new $.Deferred();
            if (!obj[field_desc.id_attribute]) return dfd.resolve();
            var generic_model_offline = Backbone.Model.extend({
                database: indexeddb,
                storeName: field_desc.entity_name,
            });
            var f_model = new generic_model_offline();
            f_model.set("id", parseInt(obj[field_desc.id_attribute]));
            var that = this;
            f_model.fetch({
                success: function(model) {
                    obj[field_desc.name_attribute] = model.get(field_desc.name_attribute);
                    return dfd.resolve();
                },
                error: function(model, error) {
                    //TODO: OOPS! What should be done now????
                    alert("Denormalize: unexpected error. check console log " + error);
                    return dfd.reject(error);
                }
            });
            return dfd.promise();
        }

    }


    return denormalize;

});

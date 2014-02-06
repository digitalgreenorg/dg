// takes an object and the foreign entities description for the object. Using the descrip iterates over json,identifies the foreign values and denormalizes them. Same object passed is denormalised. New object is not created.
// converts a foreign element like person:23131 to person:{id:23131, name:"Shrey Jairath"}
// To use - call the denormalize method
define(['jquery', 'configs', 'backbone', 'indexeddb_backbone_config'],

    function($, configs, pa, indexeddb) {
        var denormalize = {

            // get the name of the id field of foreign element in object's json - for eg - id or person_id
            _get_id_field: function(entity, element, f_entities) {
                return f_entities[entity][element].id_field || "id";
            },

            // get name of the name_field of the foreign element in object's json - for eg - name or person_name
            _get_name_field: function(entity, element, f_entities) {
                return f_entities[entity][element].name_field;
            },

            denormalize: function(json, f_entities) {
                console.log("FORMCONTROLLER:denormalize: json before denormalizing" + JSON.stringify(json));
                var that = this;
                // is filled with a dfd for each foreign element to be denormalised - when all dfds resolve - denormalisation is complete
                this.field_dfds = [];
                // iterate over the foreign elements of the object and denpormalise them asynchronously - fills the field_dfds with a dfd for each conversion
                this._iterate_foreign_fields(json, f_entities);
                return $.when.apply($, this.field_dfds);
            },

            // iterates over the foreign elements of the object and denormalises them asynchronously - fills the field_dfds with a dfd for each conversion
            _iterate_foreign_fields: function(json, f_entities) {
                // use the foreign entities definition of this object's entity to iterate over the foreign elements in the object 
                for (var entity in f_entities) {
                    for (var element in f_entities[entity]) {
                        // get details of the foreign element bieng denormalised
                        var id_field = this._get_id_field(entity, element, f_entities);
                        var name_field = this._get_name_field(entity, element, f_entities);
                        var field_desc = {
                            entity_name: entity,
                            id_attribute: id_field,
                            name_attribute: name_field
                        };

                        //  if the foreign element doesn't exist, put an empty object and return
                        if (!(json[element])) {
                            json[element] = {};
                            json[element][field_desc.id_attribute] = null;
                            json[element][field_desc.name_attribute] = null;
                            continue;
                        }

                        // the foreign element is an expanded
                        if (f_entities[entity][element].expanded) {
                            // and has its own foreign elements
                            if (f_entities[entity][element].expanded.foreign_entities) {
                                // recursively denormalise the foreign elements of expanded objects
                                _.each(json[element], function(object, index) {
                                    this._iterate_foreign_fields(object, f_entities[entity][element].expanded.foreign_entities);
                                }, this);
                            }
                            return;
                        }

                        //foreign element is a multi-select dropdown
                        if (json[element] instanceof Array) {
                            // denormalise each object of the multi-select
                            _.each(json[element], function(val, index) {
                                json[element][index] = {};
                                json[element][index][id_field] = parseInt(val);
                                // denormalise the element and put its dfd in field_dfds list 
                                this.field_dfds.push(this._denormalize_object(json[element][index], field_desc));
                            }, this);
                        }
                        //foreign element is a single-select dropdown
                        else {
                            var temp = {};
                            temp[id_field] = parseInt(json[element]);
                            json[element] = temp;
                            // denormalise the element and put its dfd in field_dfds list 
                            this.field_dfds.push(this._denormalize_object(json[element], field_desc));
                        }

                    }
                }
            },

            // denormalises a single foreign element asynchronously and returns a dfd to wait upon
            _denormalize_object: function(obj, field_desc) {
                console.log("Denormalize: dnormalizing object", JSON.stringify(obj), JSON.stringify(field_desc));
                var dfd = new $.Deferred();
                // foreign element is empty - convert to {id:null, name:null} 
                if (!obj[field_desc.id_attribute]) {
                    obj[field_desc.id_attribute] = null;
                    obj[field_desc.name_attribute] = null;
                    return dfd.resolve();
                }
                //  fetch the foreign element from offline db  
                // TODO:remove this and use the offline_utils module instead
                var generic_model_offline = Backbone.Model.extend({
                    database: indexeddb,
                    storeName: field_desc.entity_name,
                });
                var f_model = new generic_model_offline();
                f_model.set("id", parseInt(obj[field_desc.id_attribute]));
                var that = this;
                f_model.fetch({
                    success: function(model) {
                        // put in the name attribute - denormalization completed for this element
                        obj[field_desc.name_attribute] = model.get(field_desc.name_attribute);
                        return dfd.resolve();
                    },
                    error: function(model, error) {
                        // the foreign element doesn't exists in offline db
                        console.log("Denormalize: unexpected error.fetch failed", error);
                        return dfd.reject(error);
                    }
                });
                return dfd.promise();
            }

        }


        return denormalize;

    });

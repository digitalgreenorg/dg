// This module converts an object of an entity from one namespace to another.
// takes a denormalised object and the foreign entities description for the object. Using the descrip iterates over json,identifies the foreign values and substitute their online ids with offline ids or the opposite. 
// Used by incremental_download, upload, form_controller.
// To use - call the convert method
define(['jquery', 'configs', 'backbone', 'indexeddb_backbone_config'

], function($, configs, pa, indexeddb) {
    var convert_namespace = {
        // converts from offline to online by default
        which_to_which: "offlinetoonline",
        // declared to make conversion code generic
        conv_dict: {
            "onlinetooffline": {
                replace_this: "online_id",
                replace_with: "id"
            },
            "offlinetoonline": {
                replace_this: "id",
                replace_with: "online_id"
            }
        },

        // returns the id_field declared in the foreign entity definition of this 'element' in configs of 'entity'
        get_id_field: function(entity, element, f_entities) {
            return f_entities[entity][element].id_field || "id";
        },

        // recieves the object to be converted, conversion-way and the foreign entity definition of the object
        convert: function(json, f_entities, which_to_which) {
            var dfd = new $.Deferred();
            if (which_to_which)
                this.which_to_which = which_to_which;
            var that = this;
            // making a deep copy of received object...this copy would be altered
            var conv_json = $.extend(true, null, json);
            console.log("FORMCONTROLLER:convert_namespace: json before converting" + JSON.stringify(json));
            // is filled with a dfd for each foreign element to be converted - when all dfds resolve - conversion is complete
            this.field_dfds = [];
            // iterate over the foreign elements of the object and converts them asynchronously - fills the field_dfds with a dfd for each conversion
            this.iterate_foreign_fields(conv_json, f_entities);

            var object_jsons = null;
            // set the return object based on conversion-way
            switch (this.which_to_which) {
                case "onlinetooffline":
                    object_jsons = {
                        off_json: conv_json,
                        on_json: json
                    }
                    break;
                default:
                    object_jsons = {
                        off_json: json,
                        on_json: conv_json
                    }
            }
            if (this.field_dfds.length) {
                // wait till all foreign elements resolve(all dfds in field_dfds resolve)
                $.when.apply($, this.field_dfds)
                    .done(function() {
                        // object successfully converted - return
                        return dfd.resolve(object_jsons);
                    })
                    .fail(function() {
                        // atleast one foreign element failed to be converted - abort and return
                        return dfd.reject();
                    });
            } else {
                // no conversion taking place - return immediately
                console.log("FORMCONTROLLER:convert_namespace: Nothing to convert.");
                return dfd.resolve(object_jsons);
            }

            return dfd.promise();
        },

        // iterates over the foreign elements of the object and converts them asynchronously - fills the field_dfds with a dfd for each conversion
        iterate_foreign_fields: function(json, f_entities) {
            // use the foreign entities definition of this object's entity to iterate over the foreign elements in the object
            for (var entity in f_entities) {
                for (var element in f_entities[entity]) {
                    // the foreign element doesn't exists in the object 
                    if (!(json[element]))
                        continue;

                    //  get the name of the id_field of the foreign element - for eg - id or person_id 
                    var id_field = this.get_id_field(entity, element, f_entities);
                    var field_desc = {
                        entity_name: entity,
                        id_attribute: id_field
                    };

                    //foreign elements is a multi-select (dropdown or expanded)
                    if (json[element] instanceof Array)
                        _.each(json[element], function(object, index) {
                            // convert each value of this multi-select 
                            this.field_dfds.push(this.convert_object(object, field_desc));
                        }, this);
                    else //foreign elements is a single-select (dropdown)
                        this.field_dfds.push(this.convert_object(json[element], field_desc));
                    //if foreign element is an expanded and contains its own foreign elements - recursively iterate the expanded objects to convert their foreign elements
                    if (f_entities[entity][element].expanded)
                        if (f_entities[entity][element].expanded.foreign_entities)
                            _.each(json[element], function(object, index) {

                                this.iterate_foreign_fields(object, f_entities[entity][element].expanded.foreign_entities);
                            }, this);
                }
            }
        },

        // converts a single foreign element asynchronously and returns a dfd to wait upon
        convert_object: function(obj, field_desc) {
            console.log("ConvertNamespace: converting object", JSON.stringify(obj), JSON.stringify(field_desc));
            var dfd = new $.Deferred();
            // the forein element is empty - return
            if (!obj[field_desc.id_attribute])
                return dfd.resolve();
            //  fetch the foreign element from offline db  
            // TODO:remove this and use the offline_utils module instead
            var generic_model_offline = Backbone.Model.extend({
                database: indexeddb,
                storeName: field_desc.entity_name,
            });
            var f_model = new generic_model_offline();
            // the object is to be fetched based on "id" or "online_id" depending upon the conversion-way(on-to-off or off-to-on)
            f_model.set(this.conv_dict[this.which_to_which].replace_this, parseInt(obj[field_desc.id_attribute]));
            var that = this;
            f_model.fetch({
                success: function(model) {
                    // replace id with online_id or the opposite depending upon the conversion-way
                    obj[field_desc.id_attribute] = model.get(that.conv_dict[that.which_to_which].replace_with);
                    return dfd.resolve();
                },
                error: function(model, error) {
                    //TODO: OOPS! What should be done now????
                    // alert("unexpected error. check console log "+error);
                    console.log("CONVERTNAMESPACE: unexpected error.",error);
                    // the foreign element object doesn't exists
                    return dfd.reject(error);
                }
            });
            return dfd.promise();
        }

    }


    return convert_namespace;

});

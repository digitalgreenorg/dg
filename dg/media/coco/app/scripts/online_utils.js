//A module of data layer to communicate with server. Since there are no fixed entities in COCO v2(as they are defined by user in config.js), there are no predefined models. This module creates backbone models/collection on the fly and enable communication with the server thru the models.
define(['jquery', 'configs', 'backbone', 'indexeddb_backbone_config'], 

function($, all_configs, pa, indexeddb) {
    
    var online = {
        
        //Creates and return a new online backbone model object for the given entity
        create_b_model: function(entity_name)
        {
            var generic_model_online = Backbone.Model.extend({
                //configure the model to with the server
                sync: Backbone.ajaxSync,
                //read rest api endpoint for this entity from config.js and set it on model
                url: function() {
                    return this.id ? all_configs[entity_name].rest_api_url + this.id + "/" : all_configs[entity_name].rest_api_url;
                },
            });
            return new generic_model_online();
        },
    
        //Saves object on Server
        save: function(on_model, entity_name, json){
            var dfd = new $.Deferred();
            console.log("SAVING THIS IN ONLINE DB - "+JSON.stringify(json));
            if(!on_model)
            {
                //create a backbone model of entity type if one is not passed 
                on_model = this.create_b_model(entity_name);
            }
            //save model with the given json - backbone sends the request to save it on the server
            on_model.save(json,{
                success: function(model){
                    return dfd.resolve(model);
                },
                error: function(error, xhr, options){
                    return dfd.reject(xhr);
                }
            });
            return dfd;
        },
        
        //deletes an object referenced by off_model or by (entity_name, id) from server
        delete_object: function(on_model, entity_name, id){
            var dfd = new $.Deferred();
            if(!on_model)
            {
                //create a backbone model of entity type if one is not passed
                on_model = this.create_b_model(entity_name);
            }
            if(id)
            {
                //set the id on the model
                on_model.set("id",id);
            }
            //call model's destroy method - this sends delete request to server
            on_model.destroy({
                success: function(model){
                    return dfd.resolve(model);
                },
                error: function(error){
                    console.log(error);
                    return dfd.reject("Error destroying object in offline - "+xhr.responseText);
                }
            });
            return dfd;
        },
        
        
    }
    
    return online;

});

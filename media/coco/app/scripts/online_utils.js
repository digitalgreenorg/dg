define(['jquery', 'configs', 'backbone', 'indexeddb_backbone_config',

], function($, all_configs, pa, indexeddb) {
    
    var online = {
        
        //Creates and return a new offline backbone model object for the given entity
        create_b_model: function(entity_name)
        {
            var generic_model_online = Backbone.Model.extend({
                sync: Backbone.ajaxSync,
                url: function() {
                    return this.id ? all_configs[entity_name].rest_api_url + this.id + "/" : all_configs[entity_name].rest_api_url;
                },
            });
            return new generic_model_online();
            
        },
    
        //Saves object to online object store. 
        save: function(on_model, entity_name, json){
            var dfd = new $.Deferred();
            console.log("SAVING THIS IN ONLINE DB - "+JSON.stringify(json));
            //TODO: Do Unique validation here?
            if(!on_model)
            {
                on_model = this.create_b_model(entity_name);
            }
            on_model.save(json,{
                success: function(model){
                    //TODO: If edit case, do label changes here?
                    return dfd.resolve(model);
                },
                error: function(error, xhr, options){
                    return dfd.reject(xhr);
                }
            });
            return dfd;
        }
        
    }
    
    return online;

});

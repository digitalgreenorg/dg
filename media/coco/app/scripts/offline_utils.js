define(['jquery', 'configs', 'backbone', 'indexeddb_backbone_config',

], function($, all_configs, pa, indexeddb) {
    
    var offline = {
        
        //Creates and return a new offline backbone model object for the given entity
        create_b_model: function(entity_name)
        {
            var generic_model_offline = Backbone.Model.extend({
                database: indexeddb,
                storeName: entity_name,
            });
            return new generic_model_offline();
        },
    
        //Saves object to offline object store. 
        save: function(off_model, entity_name, json){
            var dfd = new $.Deferred();
            console.log("SAVING THIS IN OFFLINE DB - "+JSON.stringify(json));
            //TODO: Do Unique validation here?
            if(!off_model)
            {
                off_model = this.create_b_model(entity_name);
            }
            off_model.save(json,{
                success: function(model){
                    //TODO: If edit case, do label changes here?
                    return dfd.resolve(model);
                },
                error: function(error){
                    return dfd.reject("Error saving object in offline - "+error);
                }
            });
            return dfd;
        },
        
        fetch_object: function(entity_name, id){
            var dfd = new $.Deferred();
            var off_model = this.create_b_model(entity_name);
            off_model.set("id",id);
            off_model.fetch({
                success: function(off_model){
                    dfd.resolve(off_model);
                },
                error: function(error){
                    dfd.reject("Error fetching object from offline - "+error);
                }
            })
            return dfd;
        }
        
    }
    
    return offline;

});

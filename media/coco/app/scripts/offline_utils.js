define(['jquery', 'configs', 'backbone', 'indexeddb_backbone_config', 'auth_offline_backend'

], function($, all_configs, pa, indexeddb, OfflineAuthBackend) {
    
    var offline = {
        
        //Creates and return a new offline backbone model object for the given entity
        create_b_model: function(entity_name)
        {
            var model_offline = Backbone.Model.extend({
                database: indexeddb,
                storeName: entity_name,
            });
            return new model_offline();
        },
        
        create_b_collection: function(entity_name){
            var model_offline = Backbone.Model.extend({
                database: indexeddb,
                storeName: entity_name,
            });

            var collection_offline = Backbone.Collection.extend({
                model: model_offline,
                database: indexeddb,
                storeName: entity_name,
            });
            return new collection_offline();
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
            
            this.check_login_wrapper()
                .done(function(){
                    off_model.save(json,{
                        success: function(model){
                            //TODO: If edit case, do label changes here?
                            return dfd.resolve(model);
                        },
                        error: function(error){
                            console.log(error);
                            return dfd.reject("Error saving object in offline - "+error.srcElement.error.name);
                        }
                    });
                })
            return dfd;
        },
        
        /*
        creates a offline model
        sets the id
        fetches it
        returns fetched model
        */
        fetch_object: function(entity_name, id){
            var dfd = new $.Deferred();
            var off_model = this.create_b_model(entity_name);
            off_model.set("id",id);
            this.check_login_wrapper()
                .done(function(){
                    off_model.fetch({
                        success: function(off_model){
                            dfd.resolve(off_model);
                        },
                        error: function(error){
                            dfd.reject("Error fetching object from offline - "+error);
                        }
                    });
                })
            return dfd;
        },
        
        fetch_collection: function(entity_name){
            var dfd = new $.Deferred();
            var off_coll = this.create_b_collection(entity_name);
            this.check_login_wrapper()
                .done(function(){
                    off_coll.fetch({
                        success: function(off_coll){
                            dfd.resolve(off_coll);
                        },
                        error: function(error){
                            dfd.reject("Error fetching collection -"+entity_name+"- from offline - "+error);
                        }
                    });
                })
            return dfd;
        },
        
        delete_object: function(off_model, entity_name, id){
            var dfd = new $.Deferred();
            if(!off_model)
            {
                off_model = this.create_b_model(entity_name);
            }
            if(id)
            {
                off_model.set("id",id);
            }
            this.check_login_wrapper()
                .done(function(){
                    off_model.destroy({
                        success: function(model){
                            return dfd.resolve(model);
                        },
                        error: function(error){
                            console.log(error);
                            return dfd.reject("Error destroying object in offline - "+error.srcElement.error.name);
                        }
                    });
                })
            return dfd;
        },
        
        check_login_wrapper: function(){
            var dfd = new $.Deferred();
            console.log("Offline Backend : Authenticating Request");
            OfflineAuthBackend.check_login()
                .done(function(){
                    dfd.resolve();
                })
                .fail(function(){
                    dfd.reject();
                    window.Router.navigate("login",{trigger:true});
                });  
            return dfd;    
        }
        
    }
    
    return offline;

});

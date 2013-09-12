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
        
        create_b_collection: function(entity_name, options){
            var model_offline = Backbone.Model.extend({
                database: indexeddb,
                storeName: entity_name,
            });
            options = $.extend({
                model: model_offline,
                database: indexeddb,
                storeName: entity_name,
            },options);
            var collection_offline = Backbone.Collection.extend(options);
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
            var that = this;
            this.check_login_wrapper()
                .done(function(){
                    off_model.save(json,{
                        success: function(model){
                            //TODO: If edit case, do label changes here?
                            return dfd.resolve(off_model);
                        },
                        error: function(model,error){
                            console.log(error);
                            //format error object to match the format of error sent by online save
                            var err_json = {};
							//get unique together fields
							var ut = eval("all_configs." + entity_name +".unique_together_fields").slice(0); //to copy by value
							var utStr = that.beautify(ut);
							cap_entity_name = entity_name.charAt(0).toUpperCase() + entity_name.slice(1);
							var newerr = cap_entity_name + " with this " + utStr + " already exists";
                            err_json[entity_name] = {
                                __all__: [newerr]
                            }
                            return dfd.reject(JSON.stringify(err_json));
                        }
                    });
                })
            return dfd;
        },
		
		beautify: function(ut){
			for (var i=0; i< ut.length; i++){
				ut[i] = ut[i].charAt(0).toUpperCase() + ut[i].slice(1)
				ut[i] = ut[i].replace("_"," ");
				ut[i] = ut[i].replace(".id","");
			}
			return ut.join(", ");
		},
        
        /*
        creates a offline model
        sets the key, value
        fetches it
        returns fetched model
        Must have an index on key in IDB
        */
        fetch_object: function(entity_name, key, value){
            var dfd = new $.Deferred();
            var off_model = this.create_b_model(entity_name);
            off_model.set(key, value);
            this.check_login_wrapper()
                .done(function(){
                    off_model.fetch({
                        success: function(off_model){
                            dfd.resolve(off_model);
                        },
                        error: function(model, error){
                            dfd.reject(model, error);
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
        },
        
        reset_database: function(){
            var request = indexedDB.deleteDatabase("offline-database");
            request.onerror = function(event) {
                console.log(event);
                console.log("RESET DATABASE:Error!");
                alert("Error while resetting database! Refresh the page and try again.");
            };
            request.onsuccess = function(event) {
                console.log("RESET DATABASE:Success!");
                location.reload();
            }
            request.onblocked = function(event) {
                console.log("RESET DATABASE:Blocked!");
                location.reload();
            };
        }    
        
        
    }
    
    return offline;

});

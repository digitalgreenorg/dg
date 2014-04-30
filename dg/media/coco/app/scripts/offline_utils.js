//A module of data layer to communicate with offline DB. Since there are no fixed entities in COCO v2(as they are defined by user in config.js), there are no predefined models. This module creates backbone models/collection on the fly and enable communication with the offline DB thru the models/collections.
define(['jquery', 'configs', 'backbone', 'indexeddb_backbone_config', 'auth_offline_backend'], 
function($, all_configs, pa, indexeddb, OfflineAuthBackend) {
    
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
        
        //Creates and return a new offline backbone collection object for the given entity
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
    
        //Saves object in offline DB
        save: function(off_model, entity_name, json){
            var dfd = new $.Deferred();
            console.log("SAVING THIS IN OFFLINE DB - "+JSON.stringify(json));
            if(!off_model)
            {
                //create offline model
                off_model = this.create_b_model(entity_name);
            }
            var that = this;
            //check whether user is logged in
            this.check_login_wrapper()
                .done(function(){
                    //save model with the given json
                    off_model.save(json,{
                        success: function(model){
                            return dfd.resolve(off_model);
                        },
                        error: function(model,error){
                            console.log(error);
                            //format error object to match the format of error sent by online save
                            var err_json = {};
							//get unique together fields
							var ut = eval("all_configs." + entity_name +".unique_together_fields").slice(0); 
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
        
        //fetches an object from Offline DB from "entity_name" table having "value" value for "key" attribute 
        fetch_object: function(entity_name, key, value){
            var dfd = new $.Deferred();
            //create a offline model
            var off_model = this.create_b_model(entity_name);
            // set the key, value - Must have an index on key in IDB
            off_model.set(key, value);
            //check whether user is logged in
            this.check_login_wrapper()
                .done(function(){
                    // fetch the model - from offline DB
                    off_model.fetch({
                        success: function(off_model){
                            // return fetched model
                            dfd.resolve(off_model);
                        },
                        error: function(model, error){
                            dfd.reject(model, error);
                        }
                    });
                })
            return dfd;
        },
        
        //fetches whole "entity_name" table from offline DB as backbone collection 
        fetch_collection: function(entity_name){
            var dfd = new $.Deferred();
            //create backbone collection of type entity_name
            var off_coll = this.create_b_collection(entity_name);
            //check whether user is logged in 
            this.check_login_wrapper()
                .done(function(){
                    //fetch collection
                    off_coll.fetch({
                        success: function(off_coll){
                            //return fetched collection
                            dfd.resolve(off_coll);
                        },
                        error: function(error){
                            dfd.reject("Error fetching collection -"+entity_name+"- from offline - "+error);
                        }
                    });
                })
            return dfd;
        },
        
        //deletes an object from offline db - specified in either off_model or as (entity_name,id)
        delete_object: function(off_model, entity_name, id){
            var dfd = new $.Deferred();
            if(!off_model)
            {   
                //if backbone model for the object to be deleted was not provided - create one
                off_model = this.create_b_model(entity_name);
            }
            if(id)
            {
                //set id on model to delete
                off_model.set("id",id);
            }
            
            //check whether user is logged in
            this.check_login_wrapper()
                .done(function(){
                    //delete the model 
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
        
        //wrapper to wrap db requests with - to check whether user is logged in or not before accessing DB
        check_login_wrapper: function(){
            var dfd = new $.Deferred();
            console.log("Offline Backend : Authenticating Request");
            OfflineAuthBackend.check_login()
                .done(function(){
                    dfd.resolve();
                })
                .fail(function(){
                    dfd.reject();
                    //navigate to login url if not logged in
                    window.Router.navigate("login",{trigger:true});
                });  
            return dfd;    
        },
        
        //completely deletes the offline database and refreshes the page 
        reset_database: function(){
            var request = indexedDB.deleteDatabase("offline-database-v2");
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
                //reloading when blocked might be causing the unproper deletion of db 
                location.reload();
            };
        }    
        
        
    }
    
    return offline;

});

define([
  'jquery',
  'configs',
  
], function($, configs){
  
  
  
var idb = {
    id: "offline-database",
    description: "The offline database for COCO",
    migrations: [{
        version: 1,
        migrate: function(transaction, next) {

            for (var member in configs) {
                var entity_store = transaction.db.createObjectStore(configs[member].entity_name, {
                    autoIncrement: true,keyPath: "id"
                });    
                entity_store.createIndex("onlineIndex", "online_id", { unique: true })
                    
            }

            transaction.db.createObjectStore("uploadqueue", {
              autoIncrement: true,keyPath: "id"
            });
        
            var meta_store = transaction.db.createObjectStore("meta_data", {
              autoIncrement: true,keyPath: "id"
            });      
            meta_store.createIndex("metaIndex", "key", { unique: true })

            console.log("indexeddb database created")
            next();
        }
    }]
};

return idb;

});

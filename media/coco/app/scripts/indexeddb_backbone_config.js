define([
  'jquery',
  'configs',
  
], function(pass, configs){
  
  
  
var idb = {
    nolog: true,
    id: "offline-database",
    description: "The offline database for COCO",
    migrations: [{
        version: 1,
        migrate: function(transaction, next) {

            for (var member in configs) {
                var entity_store = transaction.db.createObjectStore(configs[member].entity_name, {
                    autoIncrement: true,keyPath: "id"
                });    
                entity_store.createIndex("onlineIndex", "online_id", { unique: true });
                var uniques = configs[member].unique_together_fields;
                if(uniques&&uniques.length)
                {
                    entity_store.createIndex("uniquesindex", uniques, { unique: true });    
                }
            }

            transaction.db.createObjectStore("uploadqueue", {
              autoIncrement: true,keyPath: "id"
            });
        
            var meta_store = transaction.db.createObjectStore("meta_data", {
              autoIncrement: true,keyPath: "id"
            });      
            meta_store.createIndex("metaIndex", "key", { unique: true })

            var full_download_info_store = transaction.db.createObjectStore("full_download_info", {
              autoIncrement: true,keyPath: "id"
            });      
            full_download_info_store.createIndex("downloadedIndex", ["entity_name", "offset", "limit"], { unique: true });

            var user_store = transaction.db.createObjectStore("user", {
              autoIncrement: true,keyPath: "id"
            });   
            user_store.createIndex("userIndex", "key", { unique: true })
               
            
            console.log("indexeddb database created");
            next();
        }
    }]
};

return idb;

});

define([
  'jquery',
  'configs',
  
], function($, configs){
  
  
  
var idb = {
    id: "coco-database",
    description: "The offline database for COCO",
    migrations: [{
        version: 1,
        migrate: function(transaction, next) {

            for (var member in configs) {
                transaction.db.createObjectStore(configs[member].entity_name, {
                    autoIncrement: true
                });    
                
              }
            
            console.log("indexeddb database created")
            //store.createIndex("nameIndex", "country_name", { unique: false })
            next();
        }
    }]
};

return idb;

});

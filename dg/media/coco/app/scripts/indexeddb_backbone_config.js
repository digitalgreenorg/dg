//Defines the config object used by backbone-indexeddb adapter - contains the offline db schema
define(['jquery', 'configs'],

function(pass, configs) {
    var idb = {
        nolog: true,
        id: "offline-database",
        description: "The offline database for COCO",
        migrations: [{
            version: 1,
            migrate: function(transaction, next) {
                for (var member in configs) {
                    //creating an objectstore for each entity defined in config file
                    var entity_store = transaction.db.createObjectStore(configs[member].entity_name, {
                        autoIncrement: true,
                        keyPath: "id"
                    });
                    //creating index on online_id field in each objectstore
                    entity_store.createIndex("onlineIndex", "online_id", {
                        unique: true
                    });
                    //creating a unique index on the unique together fields of this entity to enforce uniqueness
                    var uniques = configs[member].unique_together_fields;
                    if (uniques && uniques.length) {
                        entity_store.createIndex("uniquesindex", uniques, {
                            unique: true
                        });
                    }
                }
                
                //creating uploadQ objectstore - stores objects yet to be synced with server
                transaction.db.createObjectStore("uploadqueue", {
                    autoIncrement: true,
                    keyPath: "id"
                });
                
                //creating meta_data objectstore - stores timestamps of last full download, last inc download
                var meta_store = transaction.db.createObjectStore("meta_data", {
                    autoIncrement: true,
                    keyPath: "id"
                });
                meta_store.createIndex("metaIndex", "key", {
                    unique: true
                })
                
                //creating full_download_info objectstore - stores info abt which chunks have been downloaded - used for resumable full download
                var full_download_info_store = transaction.db.createObjectStore("full_download_info", {
                    autoIncrement: true,
                    keyPath: "id"
                });
                full_download_info_store.createIndex("downloadedIndex", ["entity_name", "offset", "limit"], {
                    unique: true
                });
                
                //creating user objectstore - stores the username, password and login-status of user
                var user_store = transaction.db.createObjectStore("user", {
                    autoIncrement: true,
                    keyPath: "id"
                });
                user_store.createIndex("userIndex", "key", {
                    unique: true
                })
                console.log("indexeddb database created");
                next();
            }
        }]
    };

    return idb;

});

var databasev1 = {
    id: "coco-database",
    description: "The offline database for COCO",
    migrations: [{
        version: 1,
        migrate: function(transaction, next) {
            transaction.db.createObjectStore("country", {
                autoIncrement: true
            });
            transaction.db.createObjectStore("village", {
                autoIncrement: true
            });
            transaction.db.createObjectStore("video", {
                autoIncrement: true
            });
            transaction.db.createObjectStore("persongroup", {
                autoIncrement: true
            });
            transaction.db.createObjectStore("screening", {
                autoIncrement: true
            });
            transaction.db.createObjectStore("person", {
                autoIncrement: true
            });
            transaction.db.createObjectStore("personadoptvideo", {
                autoIncrement: true
            });
            transaction.db.createObjectStore("animator", {
                autoIncrement: true
            });
            console.log("indexeddb database created")
            //store.createIndex("nameIndex", "country_name", { unique: false })
            next();
        }
    }]
};

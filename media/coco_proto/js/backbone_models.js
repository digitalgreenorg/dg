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




var village_offline_model = Backbone.Model.extend({
    // Common functions
    remove: function() {
        this.destroy();
    },
    database: databasev1,
    storeName: "village"
});


var village_online_model = Backbone.Model.extend({
    remove: function() {
        this.destroy();
    },
    sync: Backbone.ajaxSync,
    url: function() {
        return this.id ? '/api/v1/village/' + this.id + "/" : '/api/v1/village/?limit=0';
    }

});
var village_online_collection = Backbone.Collection.extend({
    model: village_online_model,
    url: '/api/v1/village/?limit=0',
    sync: Backbone.ajaxSync,
    parse: function(data) {
        return data.objects;
    }

});

// define the collection of countries
var village_offline_collection = Backbone.Collection.extend({
    model: village_offline_model,
    database: databasev1,
    storeName: "village",
});



var video_offline_model = Backbone.Model.extend({
    remove: function() {
        this.destroy();
    },
    database: databasev1,
    storeName: "video",

});

var video_online_model = Backbone.Model.extend({
    remove: function() {
        this.destroy();
    },
    sync: Backbone.ajaxSync,
    url: function() {
        return this.id ? '/api/v1/video/' + this.id + "/" : '/api/v1/video/?limit=0';
    }

});
var video_online_collection = Backbone.Collection.extend({
    model: video_online_model,
    url: '/api/v1/video/?limit=0',
    sync: Backbone.ajaxSync,
    parse: function(data) {
        return data.objects;
    }

});

var video_offline_collection = Backbone.Collection.extend({
    model: video_offline_model,
    database: databasev1,
    storeName: "video",
});

var persongroup_offline_model = Backbone.Model.extend({
    remove: function() {
        this.destroy();
    },
    database: databasev1,
    storeName: "persongroup"

});

var persongroup_online_model = Backbone.Model.extend({
    remove: function() {
        this.destroy();
    },
    sync: Backbone.ajaxSync,
    url: function() {
        return this.id ? '/api/v1/group/' + this.id + "/" : '/api/v1/group/?limit=0';
    }

});
var persongroup_online_collection = Backbone.Collection.extend({
    model: persongroup_online_model,
    url: '/api/v1/group/?limit=0',
    sync: Backbone.ajaxSync,
    parse: function(data) {
        return data.objects;
    }

});

var persongroup_offline_collection = Backbone.Collection.extend({
    model: persongroup_offline_model,
    database: databasev1,
    storeName: "persongroup",


    by_village: function(vill_id) {
        return this.filter(function(pg) {
            return pg.get("village")
                .id == vill_id;
        });
    }
});

var screening_offline_model = Backbone.Model.extend({
    remove: function() {
        this.destroy();
    },
    database: databasev1,
    storeName: "screening",

});

var screening_online_model = Backbone.Model.extend({
    remove: function() {
        this.destroy();
    },
    sync: Backbone.ajaxSync,
    url: function() {
        return this.id ? '/api/v1/screening/' + this.id + "/" : '/api/v1/screening/?limit=0';
    }

});
var screening_online_collection = Backbone.Collection.extend({
    model: screening_online_model,
    url: '/api/v1/screening/?limit=0',
    sync: Backbone.ajaxSync,
    parse: function(data) {
        return data.objects;
    }

});

var screening_offline_collection = Backbone.Collection.extend({
    model: screening_offline_model,
    database: databasev1,
    storeName: "screening",
});


var person_offline_model = Backbone.Model.extend({
    remove: function() {
        this.destroy();
    },
    database: databasev1,
    storeName: "person",

});

var person_online_model = Backbone.Model.extend({
    remove: function() {
        this.destroy();
    },
    sync: Backbone.ajaxSync,
    url: function() {
        return this.id ? '/api/v1/person/' + this.id + "/" : '/api/v1/person/';
    },
    save: function(attributes, options) {
        console.log("SAVE OVERRIDE: cleaning data");
        if(this.get("age")=="")
        this.set("age",null);
        
        if(this.get("land_holdings")=="")
        this.set("land_holdings",null);
        
        if(this.get("village"))
        this.set("village","/api/v1/village/" + this.get("village") + "/");
        else this.set("village",null);
        
        if(this.get("group"))
        this.set("group","/api/v1/group/" + this.get("group") + "/");
        else this.set("group",null);
        console.log("ADD/EDIT: saving this on server" +JSON.stringify(this));
        return Backbone.Model.prototype.save.call(this, attributes, options);
    }
});
var person_online_collection = Backbone.Collection.extend({
    model: person_online_model,
    url: '/api/v1/person/',
    sync: Backbone.ajaxSync,
    parse: function(data) {
        return data.objects;
    }

});

var person_offline_collection = Backbone.Collection.extend({
    model: person_offline_model,
    database: databasev1,
    storeName: "person",
});

var personadoptvideo_offline_model = Backbone.Model.extend({
    remove: function() {
        this.destroy();
    },
    database: databasev1,
    storeName: "personadoptvideo",

});

var personadoptvideo_online_model = Backbone.Model.extend({
    remove: function() {
        this.destroy();
    },
    sync: Backbone.ajaxSync,
    url: function() {
        return this.id ? '/api/v1/personadoptvideo/' + this.id + "/" : '/api/v1/personadoptvideo/?limit=0';
    }

});
var personadoptvideo_online_collection = Backbone.Collection.extend({
    model: personadoptvideo_online_model,
    url: '/api/v1/personadoptvideo/?limit=0',
    sync: Backbone.ajaxSync,
    parse: function(data) {
        return data.objects;
    }

});

var personadoptvideo_offline_collection = Backbone.Collection.extend({
    model: personadoptvideo_offline_model,
    database: databasev1,
    storeName: "personadoptvideo",
});

var animator_offline_model = Backbone.Model.extend({
    remove: function() {
        this.destroy();
    },
    database: databasev1,
    storeName: "animator",

});

var animator_online_model = Backbone.Model.extend({
    remove: function() {
        this.destroy();
    },
    sync: Backbone.ajaxSync,
    url: function() {
        return this.id ? '/api/v1/animator/' + this.id + "/" : '/api/v1/animator/?limit=0';
    }

});
var animator_online_collection = Backbone.Collection.extend({
    model: animator_online_model,
    url: '/api/v1/animator/?limit=0',
    sync: Backbone.ajaxSync,
    parse: function(data) {
        return data.objects;
    }

});

var animator_offline_collection = Backbone.Collection.extend({
    model: animator_offline_model,
    database: databasev1,
    storeName: "animator",
});

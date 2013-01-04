define([
  'backbone',
  'indexeddb-backbone',
  'indexeddb_backbone_config'
  
], function(_){
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
    
  // Return the model for the module
  return{
       person_offline_model : person_offline_model,
       person_online_model : person_online_model
   }
});
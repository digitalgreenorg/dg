define([
  'jquery',
  'underscore',
  'backbone',
  'configs',
  'indexeddb_backbone_config'
  
], function($,pass, pass, configs, indexeddb){
    
    var DashboardView = Backbone.Layout.extend({
      template: "#dashboard",
      events: {
          "click button#download": "Download",
      },
      item_template: _.template($("#dashboard_item_template").html()),
      
      afterRender: function() {
          /* Work with the View after render. */
          // this.collection.fetch();
          for (var member in configs) {
              // console.log(configs[member]);
              $('tbody').append(this.item_template({name: member,title: configs[member]["page_header"]}));
              
            }
      },
      
      fetch_save: function(config) {
          var prevTime, curTime;
          curTime = (new Date())
              .getTime();
          prevTime = curTime;
          console.log("DASHBOARD:DOWNLOAD: downloading  " + config.page_header);
          var generic_model_offline = Backbone.Model.extend({
                database: indexeddb,
                storeName: config.entity_name,
          });
          
          var generic_collection_offline = Backbone.Collection.extend({
                model: generic_model_offline,
                database: indexeddb,
                storeName: config.entity_name,
          });
          
          var generic_collection_online = Backbone.Collection.extend({
                url: config.rest_api_url,
                sync: Backbone.ajaxSync,
                parse: function(data) {
                    return data.objects;
                }

          });
            
          var collection_offline = new generic_collection_offline();
          var collection_online = new generic_collection_online(); 
          console.log(collection_offline);
          console.log(collection_online);
          
          collection_online.fetch({
              success: function() {
                  data = (collection_online.toJSON());
                  console.log("DASHBOARD:DOWNLOAD: "+config.entity_name + " collection fetched ");
                  curTime = (new Date())
                      .getTime();
                  deltaTime = curTime - prevTime;
                  var download_time = deltaTime;
                  prevTime = curTime;
                  var db;
                  var request = indexedDB.open("coco-database");
                  request.onerror = function(event) {
                      console.log("DASHBOARD:DOWNLOAD: "+"Why didn't you allow my web app to use IndexedDB?!");
                  };
                  request.onsuccess = function(event) {
                      db = request.result;
                      var clearTransaction = db.transaction([config.entity_name], "readwrite");
                      var clearRequest = clearTransaction.objectStore(config.entity_name)
                          .clear();
                      clearRequest.onsuccess = function(event) {
                          console.log("DASHBOARD:DOWNLOAD: "+config.entity_name + ' objectstore cleared');
                          console.log(collection_offline);
          
                          for (var i = 0; i < data.length; i++) {
                              // console.log(data[i]);
                              collection_offline.create(data[i]);
                          }
    
                          curTime = (new Date())
                              .getTime();
    
                          deltaTime = curTime - prevTime;
                          var writing_time = deltaTime;
                          console.log("DASHBOARD:DOWNLOAD: "+config.entity_name + " downloaded");
                          console.log("DASHBOARD:DOWNLOAD: "+config.entity_name + " downlaod time = " + download_time);
                          console.log("DASHBOARD:DOWNLOAD: "+config.entity_name + " writing time = " + writing_time);
    
                      };
    
    
    
                  }
              }
          });
      },
      Download: function() {
          console.log("starting download");
          //Download:fetch each model from server and save it to the indexeddb
    
    
          for (var member in configs) {
              // console.log(configs[member]);
              this.fetch_save(configs[member]);
         
            }
            
      },
        
    });
    
    
  // Our module now returns our view
  return DashboardView;
});
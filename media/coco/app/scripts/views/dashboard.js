define([
  'jquery',
  'underscore',
  'backbone',
  'collections/person_collection',
  'collections/village_collection',
  'collections/persongroup_collection',
  'configs',
  
], function($,pass, pass,person_collection,village_collection,persongroup_collection,configs){
    
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
      
      fetch_save: function(collection_online, collection_offline, storeName) {
          var prevTime, curTime;
          curTime = (new Date())
              .getTime();
          prevTime = curTime;
          console.log("downloading  " + storeName);
          collection_online.fetch({
              success: function() {
                  data = (collection_online.toJSON());
                  console.log(storeName + " collection fetched ");
                  curTime = (new Date())
                      .getTime();
                  deltaTime = curTime - prevTime;
                  var download_time = deltaTime;
                  prevTime = curTime;
                  var db;
                  var request = indexedDB.open("coco-database");
                  request.onerror = function(event) {
                      console.log("Why didn't you allow my web app to use IndexedDB?!");
                  };
                  request.onsuccess = function(event) {
                      db = request.result;
                      var clearTransaction = db.transaction([storeName], "readwrite");
                      var clearRequest = clearTransaction.objectStore(storeName)
                          .clear();
                      clearRequest.onsuccess = function(event) {
                          console.log(storeName + ' objectstore cleared');
                          for (var i = 0; i < data.length; i++) {
                              // console.log(data[i]);
                              collection_offline.create(data[i]);
                          }
    
                          curTime = (new Date())
                              .getTime();
    
                          deltaTime = curTime - prevTime;
                          var writing_time = deltaTime;
                          console.log(storeName + " downloaded");
                          console.log(storeName + " downlaod time = " + download_time);
                          console.log(storeName + " writing time = " + writing_time);
    
                      };
    
    
    
                  }
              }
          });
      },
      Download: function() {
          console.log("starting download");
          //Download:fetch each model from server and save it to the indexeddb
    
         villages_online = new village_collection.village_online_collection();
         villages_offline = new village_collection.village_offline_collection();
         // this.fetch_save(villages_online, villages_offline, "village");
                    //                      
          //          videos_online = new video_online_collection();
          //          videos_offline = new video_offline_collection();
          //          this.fetch_save(videos_online, videos_offline, "video");
          //                      
          persongroups_online = new persongroup_collection.persongroup_online_collection();
          persongroups_offline = new persongroup_collection.persongroup_offline_collection();
          // this.fetch_save(persongroups_online, persongroups_offline, "persongroup");
                                         
          //          screenings_online = new screening_online_collection();
          //          screenings_offline = new screening_offline_collection();
          //          this.fetch_save(screenings_online, screenings_offline, "screening");
          //          
          persons_online = new person_collection.person_online_collection();
          persons_offline = new person_collection.person_offline_collection();
          // this.fetch_save(persons_online, persons_offline, "person");
          
          // personadoptvideos_online = new personadoptvideo_online_collection();
          //  personadoptvideos_offline = new personadoptvideo_offline_collection();
          //  this.fetch_save(personadoptvideos_online, personadoptvideos_offline, "personadoptvideo");
          //  
          //  animators_online = new animator_online_collection();
          //  animators_offline = new animator_offline_collection();
          //  this.fetch_save(animators_online, animators_offline, "animator");
      },
        
    });
    
    
  // Our module now returns our view
  return DashboardView;
});
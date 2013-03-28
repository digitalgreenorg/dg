define([
  'jquery',
  'underscore',
  'backbone',
  'indexeddb_backbone_config',
      'configs'
  // Using the Require.js text! plugin, we are loaded raw text
  // which will be used as our views primary template
  // 'text!templates/project/list.html'
], function($,_,pass,indexeddb, configs){
    
    var FullDownloadView = Backbone.Layout.extend({
        template: "#download_template",

        initialize: function(){
            // this.$('#full_download_modal').show();
            
        },

        afterRender: function(){
            this.$('#full_download_modal').modal('show');
            this.Download();
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
            var that = this;
            collection_online.fetch({
                data: {
                    limit: 100
                },
                success: function() {
                    data = (collection_online.toJSON());
                    console.log("DASHBOARD:DOWNLOAD: " + config.entity_name + " collection fetched ");
                    curTime = (new Date())
                        .getTime();
                    deltaTime = curTime - prevTime;
                    var download_time = deltaTime;
                    prevTime = curTime;
                    var db;
                    var request = indexedDB.open("offline-database");
                    request.onerror = function(event) {
                        console.log("DASHBOARD:DOWNLOAD: " + "Why didn't you allow my web app to use IndexedDB?!");
                    };
                    request.onsuccess = function(event) {
                        db = request.result;
                        var clearTransaction = db.transaction([config.entity_name], "readwrite");
                        var clearRequest = clearTransaction.objectStore(config.entity_name)
                            .clear();
                        clearRequest.onsuccess = function(event) {
                            console.log("DASHBOARD:DOWNLOAD: " + config.entity_name + ' objectstore cleared');
                            console.log(collection_offline);

                            for (var i = 0; i < data.length; i++) {
                                // console.log(data[i]);
                                // adding online_id field to support offline functionality
                                data[i]['id'] = parseInt(data[i]['id']);
                                data[i]['online_id'] = data[i]['id'];
                                collection_offline.create(data[i]);
                            }

                            curTime = (new Date())
                                .getTime();

                            deltaTime = curTime - prevTime;
                            var writing_time = deltaTime;
                            console.log("DASHBOARD:DOWNLOAD: " + config.entity_name + " downloaded");
                            console.log("DASHBOARD:DOWNLOAD: " + config.entity_name + " downlaod time = " + download_time);
                            console.log("DASHBOARD:DOWNLOAD: " + config.entity_name + " writing time = " + writing_time);
                            that.num_of_entities--;
                            if(!that.num_of_entities)
                            {
                                that.finish_download();
                            }
                        };



                    }
                }
            });
        },
            
        Download: function() {
            console.log("DASHBOARD:DOWNLOAD: starting download");
            //Download:fetch each model from server and save it to the indexeddb

            this.num_of_entities = Object.keys(configs).length; // Number of foreign entities referenced in this model.
            
            for (var member in configs) {
                // console.log(configs[member]);
                this.fetch_save(configs[member]);

            }
            
         
        },
                
        finish_download: function(){
            console.log("DASHBOARD:DOWNLOAD: In finish downlaod");
            var generic_model_offline = Backbone.Model.extend({
                database: indexeddb,
                storeName: "meta_data",
            });
            var meta_model = new generic_model_offline();
            meta_model.set({key: "last_downloaded"});
            meta_model.fetch({
                success: function(model){
                    console.log("lDASHBOARD:DOWNLOAD: ast_downloaded fetched from meta_data objectStore:");
                    console.log(JSON.stringify(model.toJSON()));
                    model.set('timestamp',new Date());
                    model.save(null,{
                        success: function(){
                            console.log("DASHBOARD:DOWNLOAD: last_downloaded updated in meta_data objectStore:");    
                            console.log(JSON.stringify(model.toJSON()));
                            
                        },
                        error: function(one,two,three){
                            console.log("DASHBOARD:DOWNLOAD: error updating last_downloaded in meta_data objectStore");    
                            console.log(one);
                            console.log(two);
                            console.log(three);
                        }
                    });
                },
                error: function(error){
                    console.log("DASHBOARD:DOWNLOAD: error while fetching last_downloaded from meta_data objectStore");
                    if(error == "Not Found")
                        {
                            meta_model.set('timestamp',new Date());
                            meta_model.save(null,{
                                success: function(model){
                                    console.log("DASHBOARD:DOWNLOAD: last_downloaded created in meta_data objectStore:");    
                                    console.log(JSON.stringify(model.toJSON()));
                                    this.$('#full_download_modal').modal('hide');
                            
                                },
                                error: function(one,two,three){
                                    console.log("DASHBOARD:DOWNLOAD: error creating last_downloaded in meta_data objectStore");    
                                    console.log(one);
                                    console.log(two);
                                    console.log(three);
                                    
                                }
                            });
                            
                        }    
                }        
            });
        }        
        
                
    
          
    });
    
  // Our module now returns our view
  return FullDownloadView;
});
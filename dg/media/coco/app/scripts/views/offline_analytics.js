/*define([
    'jquery',
    'underscore',
    'backbone',
    'indexeddb_backbone_config',
    'configs',
    'indexeddb-backbone',
    'layoutmanager',
  	'offline_utils'],
  	function(jquery, underscore, backbone, layoutmanager, indexeddb,all_configs, Offline){
  		var ListView = Backbone.Layout.extend({

        template: "#graph_view_template",
        initialize: function(){
          this.entity_config = all_configs['village'];
          console.log("Initializing graph view");
          _.bindAll(this);
          this.render();
         },

      	serialize: function () {
            //send these to the list page template
            return {
                page_header: "Analytics",
            };
        },

        afterRender: function () {
            //Fetch entity's full data from offline DB and call render_data when fetched
            Offline.fetch_collection(this.entity_config.entity_name)
                .done(this.render_data)
                .fail(function () {
                    notifs_view.add_alert({
                        notif_type: "error",
                        message: "Error reading data for graphs."
                    });
                });
        },

        get_row: function (model_object) {
            var list_elements = this.entity_config.list_elements;
            var row = $.map(list_elements, function (column_definition) {
                var cell = '';
                if ('element' in column_definition) {
                    if ('subelement' in column_definition) {
                        var subelement_definition = column_definition['subelement'];
                        cell = $.map(model_object[column_definition['element']],function (val) {
                            return val[subelement_definition];
                        }).join("; ");
                    }
                    else {
                        var element_definition = column_definition['element'];
                        var element_parts = element_definition.split(".");
                        var object = model_object;
                        for (var i = 0; i < element_parts.length; i++) {
                            // To check if the entry is made online or offline. Display "Not uploaded in place of id in case of offline entry"
                            if(element_parts.length == 1 && element_parts[i] == "id" && object.online_id == undefined){
                                object = "Not Uploaded"
                            }
                            else{
                                object = object[element_parts[i]];
                            }
                        }
                        if (object != null) {
                            cell = object;
                        }
                    }
                }
                else {
                    // Developer needs to be told that 'element' is compulsory.
                    alert('Error: Add element in list_elements parameter in configs.js');
                }
                return cell;
            });
            return row;
        },

        render_data: function (entity_collection) {
        	var self = this;
            var array_table_values = $.map(entity_collection.toJSON(), function (model) {
                return [self.get_row(model)];
            });


console.log("*********************************");
            var dict = [];
            for(var i=0; i<array_table_values.length; i++)
            {
                var village = array_table_values[i][1];
                var block = array_table_values[i][2];
                var count = 1;
                
                for (var j=0; j<array_table_values.length; j++)
                {
                    
                    if(block == array_table_values[j][2]){  
                        count++;
                    }

                }
                if(block in Object.keys(dict)){
                    console.log("hi");
                }
                for(var key in dict){
                    for (var k in dict[key]){
                        console.log(dict[key][k]);                
                    }
                }
            
                   dict.push({
                    key:   block,
                    value: count
                    
                    });
                
            }    
            
            
            //console.log(typeof dict);
            //console.log(Object.keys(dict));
            //console.log(dict);
            

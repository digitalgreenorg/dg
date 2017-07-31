define([
    'jquery',
    'underscore',
    'backbone',
    'indexeddb_backbone_config',
    'configs',
    'models/user_model',
    'indexeddb-backbone',
    'layoutmanager',
    'libs/highstocks',
    'offline_utils'
    ],
    function($, underscore, backbone, idb, all_configs, User, indexeddb, layoutmanager,highcharts, Offline){
        
        var AnalyticsView = Backbone.Layout.extend({

        
        template: "#analytics_template",
        
        initialize: function(para){
          this.ent = para.entities;
          this.entity_config = all_configs[para.entities];
          this.container = para.container;
          this.xaxis = para.xaxis;//all_configs[para.entities]['xaxis'];
          this.k = para.j;
          this.yaxis = all_configs[para.entities]['yaxis'];
          if(para.key==undefined)
          this.key = all_configs[para.entities]['key'];
          else
            this.key = para.key;
          this.graph_type = all_configs[para.entities]['graph_type'];
          this.tabId = para.tabId;
          console.log("Initializing graph view");
          _.bindAll(this);
          this.render();
         },

        serialize: function () {
            return {
                page_header: "Analytics",
            };
        },

        afterRender: function () {
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
            var language = User.get('language');
            var list_elements = this.entity_config['list_elements_'+language];
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
            var category_id = [];
            var temp_Dict ={}
            var array_table_values = $.map(entity_collection.toJSON(), function (model) {
                if (model.hasOwnProperty('videoes_screened')){
                    _.each(model.videoes_screened, function(element, index) {
                        // console.log(element.id, index)
                        Offline.fetch_object("video", "id", element.id)
                            .fail(function(obj, error) {
                                // console.log(model);
                            })
                            .done(function(obj) {
                                // console.log(model);
                                if(temp_Dict.hasOwnProperty(obj.attributes.category.category_name)){
                                    temp_Dict[obj.attributes.category.category_name]++
                                    // console.log(temp_Dict)

                                }else{
                                    temp_Dict[obj.attributes.category.category_name]=1
                                }
                                window.temp_dict = temp_Dict
                                // category_id.push(obj.attributes.category.category_name);
                                
                            });
                    })
                }
                
                return [self.get_row(model)];
            });
            console.log("*****************************");
            var dict = {};
            
            if(!this.key[this.k]==0){
            for(var i=0; i<array_table_values.length; i++)
            {
                var count = 0;
                if(this.key[this.k]==1){
                    var arr = array_table_values[i][this.key[this.k]].split('-');
                    var year = arr[0];
                    var month = arr[1];
                    var date = arr[2];
                    var block = Date.UTC(year,month,date);
                    
                }
                else block = array_table_values[i][this.key[this.k]];
                if(!dict.hasOwnProperty(block))
                    dict[block] = 1;
                else 
                    dict[block]++;
            }
            }
            var sorted = [];
                for(var key in dict) {
                    sorted[sorted.length] = key;
                }
                sorted.sort();

            var tempDict = {};
            for(var i = 0; i < sorted.length; i++) {
            tempDict[sorted[i]] = dict[sorted[i]];
            }
            dict = tempDict
            if (this.xaxis == "Category"){
                dict = window.temp_dict
            }
            if(this.key[this.k]>1){
            var options = {
                title: {
                    text: ''
                },
                chart: {
                    renderTo: this.container,
                    type: this.graph_type,
                },

                xAxis: {
                    categories: [],
                    title: {
                        text: this.xaxis,
                    },
                },
                navigator:{
                    enabled:true,
                    width:'20%'
                },
                yAxis: {
                    title: {
                        text: this.yaxis,
                    },
                    tickInterval: 1,
                    minRange: 1,
                    allowDecimals: false
                },
                series: [{
                    data: []
                }]
            };
            for (var key in dict) 
            {
                if (dict.hasOwnProperty(key)) 
                {            
                    options.xAxis.categories.push(key);
                    options.series[0].data.push(dict[key]);    
                }
            }
            var chart = new Highcharts.Chart(options);            
            console.log("*****************************");
        }
        else if(this.key[this.k]==1){
            var groupingUnits = [[
                'week',                         // unit name
                    [1]                             // allowed multiples
                ],[
                    'month',
                [1, 2, 3, 4, 6]
            ]];
            var i=0,dataTime=[];
            for (var key in dict) 
            {
                if (dict.hasOwnProperty(key)) 
                {            

                    dataTime.push([key*1,dict[key]]);
                }
            }
            var options2 = {
                title: {
                    text: ''
                },
                chart: {
                    renderTo: this.container,
                    type: this.graph_type,
                },
                xAxis: {
                    categories: [],
                    title: {
                        text: this.xaxis,
                    },
                },  
                yAxis: {
                    title: {
                        text: this.yaxis,
                    },
                    opposite:false,
                    allowDecimals: true
                },
                series: [{
                data : dataTime,
                tooltip: {
                    valueDecimals: 2
                },
                dataGrouping: {
                        approximation: "sum",
                        enabled: true,
                        forced: true,
                        units: groupingUnits,
                        
                    }
            }]
            };
            /*for (var key in dict) 
            {
                if (dict.hasOwnProperty(key)) 
                {            
                    //options2.xAxis.categories.push(key);
                    options2.series[0].data.push(dict[key]);    
                }
            }*/
            var chart = new Highcharts.stockChart(options2);            
        }
        else{
            if(this.ent=='village')
                window.village = array_table_values.length
            if(this.ent=='group')
                window.group = array_table_values.length
            if(this.ent=='video')
                window.video = array_table_values.length
            if(this.ent=='screening')
                window.screening = array_table_values.length
            if(this.ent=='mediator')
                window.mediator = array_table_values.length
            if(this.ent=='adoption')
                window.adoption = array_table_values.length
            if(this.ent=='person')
                window.person = array_table_values.length
            if(window.village!=undefined&&window.group!=undefined&&window.video!=undefined&&window.screening!=undefined&&window.mediator!=undefined&&window.adoption!=undefined&&window.person!=undefined){

            $('#container11').html('Number of Village'+' : '+window.village);
            $('#container12').html('Number of Group'+' : '+window.group);
            $('#container13').html('Number of Video'+' : '+window.video);
            $('#container14').html('Number of Screening'+' : '+window.screening);
            $('#container15').html('Number of Mediator'+' : '+window.mediator);
            $('#container16').html('Number of Adoption'+' : '+window.adoption);
            $('#container17').html('Number of Person'+' : '+window.person);
            }
        }
       
    }
    
    });
  // Our module now returns our view
  return AnalyticsView;
});
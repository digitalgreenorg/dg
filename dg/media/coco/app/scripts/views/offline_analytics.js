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
            console.log('hhhhh', this.entity_config.entity_name)
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
            var list_elements = this.entity_config['list_elements_for_analytics'];
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
        render_chart: function(dict){
            var self=this;
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
        },

        // get_category_data: function(video_array){
        //     temp_dict = {}
        //         _.each(video_array, function(element, index) {
        //             Offline.fetch_object("video", "title", element[5])
        //                 .fail(function(obj, error) {
        //                     console.log(error)
        //                 })
        //                 .done(function(obj) {
        //                     (function(obj, index){
        //                         if(temp_Dict.hasOwnProperty(obj.attributes.category.category_name)){
        //                             temp_Dict[obj.attributes.category.category_name]++

        //                         }else{
        //                             temp_Dict[obj.attributes.category.category_name]=1
        //                         }
                              
        //                     })(obj, index);
        //                     temp_dict = temp_Dict
        //                     // dfd.resolve();
                            
        //                 });
        //         })
        //     return temp_dict
        // },

        render_data: function (entity_collection) {

            var self = this;
            var village_reached = [];
            temp_Dict ={}
            var array_table_values = $.map(entity_collection.toJSON(), function (model) {
                return [self.get_row(model)];
            });
            var dict = {};
            
            if(!this.key[this.k]==0){
            for(var i=0; i<array_table_values.length; i++)
            {
                var count = 0;
                if(this.key[this.k]==1){
                    var arr = array_table_values[i][this.key[this.k]].split('-');
                    var year = arr[0];
                    var month = arr[1]-1;
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
            if(this.key[this.k]>1){
                self.render_chart(dict);
                // console.log("*****************************");
            }
            // if (this.xaxis == "Category"){
            //     temp_dict = {'Agriculture': 21}
            //     console.log(temp_dict)
            //     // setTimeout(function(){
            //     //     self.chacha(temp_dict);
            //     // }, 1000);
            //     self.chacha(temp_dict);
            //     // self.get_category_data(array_table_values)
                
            // }
            
        else if(this.key[this.k]==1){dict=tempDict
            console.log('final', dict)
            var groupingUnits = [['day',[1]],[
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
            console.log(this.ent)
            villagee = 0
            var unique_village_reached = [];
            if(this.ent=='village')
                window.village = array_table_values.length
            else if(this.ent=='group')
                window.group = array_table_values.length
            else if(this.ent=='video')
                window.video = array_table_values.length
            else if(this.ent=='screening'){
                window.screening = array_table_values.length
                village_reached = [];
                videos_screened_reached = [];
                category_reached = [];
                group_reached = [];
                _.each(entity_collection.models, function(element, index){
                    if (element.attributes.village){
                        village_reached.push(element.attributes.village.id)
                        if (village_reached.length){
                            var unique_village_reached = _.uniq(village_reached).length;
                            window.villagee = unique_village_reached
                        }   
                    }
                    if (element.attributes.videoes_screened){
                        _.each(element.attributes.videoes_screened, function(ele, index){
                            videos_screened_reached.push(ele.id) 
                        })
                        if (videos_screened_reached.length){
                            var unique_videos_reached = _.uniq(videos_screened_reached).length;
                            window.videoss = unique_videos_reached
                        }
                    }
                    if (element.attributes.farmers_attendance){
                        _.each(element.attributes.farmers_attendance, function(elem, index){
                            category_reached.push(elem.person_id)
                             
                        })
                        if (category_reached.length){
                            // var unique_category_reached = _.uniq(category_reached).length;
                            // window.category_reacheddd = unique_category_reached
                            window.category_reacheddd = category_reached.length
                        }
                    }
                    if (element.attributes.farmer_groups_targeted){
                        _.each(element.attributes.farmer_groups_targeted, function(elem, index){
                            group_reached.push(elem.id)
                             
                        })
                        if (group_reached.length){
                            var unique_group_reached = _.uniq(group_reached).length;
                            window.group_reacheddd = unique_group_reached
                            // window.category_reacheddd = category_reached.length
                        }
                    }
                    
                })
                $('#container17').html(window.screening);
                $('#container13').html(window.villagee);
                $('#container16').html(window.videoss);
                $('#container15').html(window.category_reacheddd);
                $('#container14').html(window.group_reacheddd);
            }    
                
                
                
            // else if(this.ent=='mediator')
            //     window.mediator = array_table_values.length
            else if(this.ent=='adoption')
                window.adoption = array_table_values.length
                $('#container18').html(window.adoption);
            // else if(this.ent=='person')
            //     window.person = array_table_values.length
            
            // if(this.ent=='adoption'||this.ent=='screening'){
                
            //     $('#container14').html(window.group);
            //     $('#container15').html(window.person);
            //     $('#container16').html(window.video);
                
            //     $('#container18').html(window.adoption);
            // }
                

            // if(window.village!=undefined&&window.group!=undefined&&window.video!=undefined&&window.screening!=undefined&&window.mediator!=undefined&&window.adoption!=undefined&&window.person!=undefined){
            // $('#container13').html(villagee);
            // $('#container14').html(window.group);
            // $('#container15').html(window.person);
            // $('#container16').html(window.video);
            // $('#container17').html(window.screening);
            // $('#container18').html(window.adoption);
            // }
            
        }
       
    }
    
    });
  // Our module now returns our view
  return AnalyticsView;
});
window.onload = initialize;

function initialize() {
    // initialize any library here
    $('select').material_select();
    set_eventlistener();
    $(".button-collapse").sideNav()
    total_static_data();
    recent_graphs_data();
    days_to_average = 15;
}

function set_eventlistener() {
    $("#mFrequency").change(function(){
        days_to_average = $('#mFrequency :selected').val()
        plot_cards_data();
    });
}

bullet_options = {
    type: "bullet",
    width: "100",
    height: "30",
    performanceColor: '#00bfbf',
    rangeColors: ['#a2d6d6']
}

sparkline_option = {
    type: 'line',
    width: '100',
    height: '40',
    lineColor: '#00bfbf',
    fillColor: '#dde1df',
    lineWidth: 2
}

function total_static_data() {
    $.get("/loop/total_static_data/", {}).done(function(data) {
        var json_data = JSON.parse(data);

        var total_volume = json_data['total_volume']['quantity__sum'];
        
        var total_amount = json_data['total_volume']['amount__sum'];
        
        var total_farmers_reached = json_data['total_farmers_reached'];
        var total_repeat_farmers = json_data['total_repeat_farmers']
        
        var total_transportation_cost = json_data['total_transportation_cost']['transportation_cost__sum'];
        var total_farmer_share = json_data['total_transportation_cost']['farmer_share__sum'];
        var total_expenditure = total_transportation_cost - total_farmer_share;
        var total_volume_for_transport = json_data['total_volume_for_transport']['quantity__sum'];
        
        var sustainability = total_farmer_share / total_transportation_cost * 100;
        
        var clusters = json_data['total_cluster_reached'];
        
        var total_cpk = total_transportation_cost/total_volume_for_transport;
        
        var kg = "Kg";
        var rs = "₹";

        document.getElementById('cluster_card').innerHTML = clusters;
        $('#cluster_bullet').sparkline([30, clusters, 50], bullet_options);
        
        document.getElementById('total_farmers_card').innerHTML = total_farmers_reached +" <sub style='font-size: 12px'>"+parseFloat((total_repeat_farmers/total_farmers_reached)*100).toFixed(2)+"%"+"</sub>";
        $('#total_farmers_bullet').sparkline([1500, total_farmers_reached, 5000], bullet_options);

        document.getElementById('total_volume_card').innerHTML = parseFloat(total_volume).toFixed(0).concat(kg);
        $('#total_volume_bullet').sparkline([1000000, total_volume, 1500000], bullet_options);   
        
        document.getElementById('revenue_card').innerHTML =rs.concat(parseFloat(total_amount).toFixed(0));
        $('#revenue_bullet').sparkline([10000000, total_amount, 15000000], bullet_options);

        document.getElementById('total_expenditure_card').innerHTML =  parseFloat(total_cpk).toFixed(2); //rs.concat(parseFloat(total_transportation_cost).toFixed(2) - parseFloat(total_farmer_share).toFixed(2));
        $('#total_expenditure_bullet').sparkline([0.4, total_cpk, 0.5], bullet_options);

        document.getElementById('sustainability_card').innerHTML = parseFloat(sustainability).toFixed(2).concat(" %");
        $('#sustainability_bullet').sparkline([60, sustainability, 100], bullet_options);     
    })
}

function recent_graphs_data() {
    $.get("/loop/recent_graphs_data/", {
        "start_date": "",
        "end_date": ""
    }).done(function(data) {
            json_data = JSON.parse(data);

            dates = json_data['dates'];
            aggregators_details = json_data.aggregators;
            mandis = json_data['mandis'];
            stats = json_data['stats'];
            transportation = json_data['transportation_cost'];
            crops = json_data['crops'];

            plot_cards_data();

            cummulative();
    });
}



function plot_cards_data() {
    var avg = get_average(); // Retunts [avg_volume, active_farmers, avg_amount]
    var avg_vol = avg[0];
    var kg = "Kg";
    var rs = "₹";
    document.getElementById('recent_volume_card').innerHTML = parseFloat(avg_vol[0]).toFixed(2).concat(kg);
    $('#recent_volume_sparkline').sparkline(avg_vol.reverse(), sparkline_option);

    var active_farmers = avg[1];
    document.getElementById('recent_active_farmers_card').innerHTML = active_farmers[0];
    $('#recent_active_farmers_sparkline').sparkline(active_farmers.reverse(), sparkline_option);
    
    var avg_amt = avg[2];
    document.getElementById('recent_revenue_card').innerHTML = parseFloat(avg_amt[0]).toFixed(2);
    $('#recent_revenue_sparkline').sparkline(avg_amt.reverse(), sparkline_option);

    var data = get_cpk(avg_vol.reverse());
    var cpk = data[0];
    document.getElementById('cpk_card').innerHTML = rs.concat(parseFloat(cpk[0]).toFixed(2));
    $('#cpk_sparkline').sparkline(cpk.reverse(), sparkline_option);

    var sustainability = data[1];
    document.getElementById('recent_sustainability_card').innerHTML = parseFloat(sustainability[0]).toFixed(2) + "%";
    $('#recent_sustainability_sparkline').sparkline(sustainability.reverse(), sparkline_option);
}



function get_average() {

    var today = new Date();

    today.setDate(today.getDate() - days_to_average);

    var avg_vol = [];

    var avg_amt =[];

    var active_farmers = [];
    var active_farmers_id = [];

    var j = 0,
        temp_vol = 0,
        temp_amt=0;
    //If no data is present for a period of days_to_average initially
    while (today >= new Date(stats[j]['date'])) {
        avg_vol.push(0);
        avg_amt.push(0);
        active_farmers.push(0);
        today.setDate(today.getDate() - days_to_average);
    }

    while (j < stats.length && today < new Date(stats[j]['date'])) {
        temp_vol += stats[j]['quantity__sum'];
        temp_amt += stats[j]['amount__sum'];

        var farmer_id = stats[j]['farmer__id'];
        if (active_farmers_id.indexOf(farmer_id) == -1) {
            active_farmers_id.push(farmer_id);
        }
        j++;
        if (j < stats.length && today >= new Date(stats[j]['date'])) {
            avg_vol.push(temp_vol);
            avg_amt.push(temp_amt);
            temp_vol = 0;
            temp_amt=0;
            
            active_farmers.push(active_farmers_id.length);
            active_farmers_id = [];

            today.setDate(today.getDate() - days_to_average);

            //If no data is present for a period of days_to_average
            while (today >= new Date(stats[j]['date'])) {
                avg_vol.push(0);
                avg_amt.push(0);
                active_farmers.push(0);
                today.setDate(today.getDate() - days_to_average);
            }
        }
    }

    avg_vol.push(temp_vol);
    avg_amt.push(temp_amt);
    active_farmers.push(active_farmers_id.length);

    return [avg_vol, active_farmers, avg_amt];
}

function get_cpk(avg_vol) {

    var today = new Date();
    today.setDate(today.getDate() - days_to_average);

    var cpk = [];
    var sustainability_per_kg = [];

    var j = 0, // To loop through transportation details
        temp = 0,
        k = 0, // keeping note of position in avg_vol
        f_share = 0;

    //If no data is present for a period of days_to_average initially
    while (today >= new Date(transportation[j]['date'])) {
        cpk.push(0);
        sustainability_per_kg.push(0);
        today.setDate(today.getDate() - days_to_average);
        k++;
    }
    while (j < transportation.length && today < new Date(transportation[j]['date'])) {
        temp += transportation[j]['transportation_cost__sum']; // - transportation[j]['farmer_share__sum'];
        f_share += transportation[j]['farmer_share__sum'];
        j++;
        if (j < transportation.length && today >= new Date(transportation[j]['date'])) {
            if (avg_vol[k]==0){
                cpk.push(0);
                sustainability_per_kg.push(0);
            }else{
                cpk.push(temp / avg_vol[k]);
                sustainability_per_kg.push(f_share/temp*100);
            }
            
            k++;
            today.setDate(today.getDate() - days_to_average);
            temp = 0;
            f_share = 0;
            //If no data is present for a period of days_to_average
            while (today >= new Date(transportation[j]['date'])) {
                cpk.push(0);
                sustainability_per_kg.push(0);
                today.setDate(today.getDate() - days_to_average);
                k++;
            }
        }
    }

    if (avg_vol[k]==0){
        cpk.push(0);
        sustainability_per_kg.push(0);
    }else{
        cpk.push(temp / avg_vol[k]);
        sustainability_per_kg.push(f_share/temp*100);
    }

    //Adding 0 cost for previous data making length of both arrays same
    for (var i = cpk.length; i < avg_vol.length; i++) {
        cpk.push(0);
        sustainability_per_kg.push(0);
    }
    return [cpk, sustainability_per_kg];
}


function cummulative(){

    var all_dates = [];
    var farmer_ids = []

    var first_date = new Date(dates[dates.length-1]);
    while (first_date <= new Date(dates[0])){
        all_dates.push(first_date.getTime());
        first_date.setDate(first_date.getDate()+1)
    }

    var cumm = new Array(all_dates.length).fill(0.0);
    var cumm_farmers = new Array(all_dates.length).fill(0.0);
    var temp ={}
    temp['name'] = "volume";
    temp['data'] = [];
    temp['type'] = 'spline';
    temp['pointInterval'] = 24 * 3600 * 1000;
    temp['pointStart'] = all_dates[all_dates.length-1]; // Pointing to the starting date
    temp['showInLegend'] = true;
    var temp_farmers ={}
    temp_farmers['name'] = "farmers";
    temp_farmers['data'] = [];
    temp_farmers['type'] = 'spline';
    temp_farmers['pointInterval'] = 24 * 3600 * 1000;
    temp_farmers['pointStart'] = all_dates[all_dates.length-1]; // Pointing to the starting date
    temp_farmers['showInLegend'] = true;

    for (var i=0; i<stats.length;i++){
        var index = all_dates.indexOf(new Date(stats[i]['date']).getTime());
        if (farmer_ids.indexOf(stats[i]['farmer__id'])== -1){
            farmer_ids.push(stats[i]['farmer__id']);
            cumm_farmers[index]+=1;

        }
        cumm[index]+=stats[i]['quantity__sum'];
    }

    temp['data'].push([all_dates[0],cumm[0]]);
    temp_farmers['data'].push([all_dates[0],cumm_farmers[0]]);

    for (var i=1; i<cumm.length;i++){        
        cumm[i]+=cumm[i-1];
        cumm_farmers[i]+=cumm_farmers[i-1];
        temp['data'].push([all_dates[i], cumm[i]]);
        temp_farmers['data'].push([all_dates[i], cumm_farmers[i]]);
    }

    var series =[];
    series.push(temp);
    series.push(temp_farmers);
     var $container = $('#container2')
                .css('position', 'relative');

            $('<div id="detail-container">')
                .appendTo($container);

            $('<div id="master-container">')
                .css({
                    position: 'absolute',
                    top: 300,
                    height: 100,
                    width: '100%'
                })
                    .appendTo($container);
    createMaster(series);   
}





function createDetail(masterChart, dict) {

                // prepare the detail chart
                var myDict=[]
                var detailData = [],
                    detailStart = dict[0]['data'][0][0];

                $.each(masterChart.series, function () {
                    var temp ={};
                    temp['name'] = this.name;
                    temp['type'] = "spline"
                    temp['data'] = new Array();
                    temp['pointStart']= detailStart;
                    temp['pointInterval']= 24 * 3600 * 1000;
                    temp['showInLegend'] = true;
                    $.each(this.data, function () {
                        if (this.x >= detailStart) {
                            temp['data'].push(this.y);
                        }

                    });
                    myDict.push(temp)});

                // create a detail chart referenced by a global variable
                detailChart = $('#detail-container').highcharts({
                    chart: {
                        marginBottom: 120,
                        reflow: false,
                        marginLeft: 50,
                        marginRight: 20,
                        style: {
                            position: 'absolute'
                        }
                    },
                    credits: {
                        enabled: false
                    },
                    
                    xAxis: {
                        type: 'datetime'
                    },
                    yAxis: {
                        title: {
                            text: null
                        },
                        maxZoom: 0.1
                    },
                    tooltip: {
                        // formatter: function () {
                        //     var point = this.points[0];
                        //     return '<b>' + point.series.name + '</b><br/>' + Highcharts.dateFormat('%A %B %e %Y', this.x) + ':<br/>' +
                        //         'Volume= ' + Highcharts.numberFormat(point.y, 2);
                        // },
                        shared: true
                    },
                    legend: {
                        enabled: false
                    },
                    plotOptions: {
                        series: {
                            marker: {
                                enabled: false,
                                states: {
                                    hover: {
                                        enabled: true,
                                        radius: 3
                                    }
                                }
                            }
                        }
                    },
                    legend: {
                        align: 'right',
                        x: 0,
                        verticalAlign: 'top',
                        y: 0,
                        floating: true,
                        backgroundColor: (Highcharts.theme && Highcharts.theme.background2) || 'white',
                        borderColor: '#CCC',
                        borderWidth: 1,
                        shadow: false
                    },
                    series: myDict,

                    exporting: {
                        enabled: false
                    }

                }).highcharts(); // return chart
            }

            // create the master chart
            function createMaster(dict) {
                $('#master-container').highcharts({
                    chart: {
                        reflow: false,
                        borderWidth: 0,
                        backgroundColor: null,
                        marginLeft: 50,
                        marginRight: 20,
                        zoomType: 'x',
                        events: {

                            // listen to the selection event on the master chart to update the
                            // extremes of the detail chart
                            selection: function (event) {
                                var extremesObject = event.xAxis[0],
                                    min = extremesObject.min,
                                    max = extremesObject.max,
                                    detailData = [],
                                    xAxis = this.xAxis[0],
                                    myDict = [];

                                $.each(this.series, function(){
                                    var temp ={};
                                    temp['name']= this.name;
                                    temp['data'] = new Array();
                                    temp['pointStart']= dict[0]['data'][0][0];
                                    temp['pointInterval']= 24 * 3600 * 1000;
                                    $.each(this.data, function(){
                                       if (this.x > min && this.x < max) {
                                            temp['data'].push([this.x, this.y]);
                                        } 
                                    });
                                    myDict.push(temp);
                                });
                                console.log(myDict);
                                // reverse engineer the last part of the data
                              
                                // move the plot bands to reflect the new detail span
                                xAxis.removePlotBand('mask-before');
                                xAxis.addPlotBand({
                                    id: 'mask-before',
                                    from: dict[0]['data'][0][0],    //data[0][0],
                                    to: min,
                                    color: 'rgba(0, 0, 0, 0.2)'
                                });

                                xAxis.removePlotBand('mask-after');
                                xAxis.addPlotBand({
                                    id: 'mask-after',
                                    from: max,
                                    to: dict[0]['data'][dict[0]['data'].length - 1][0],
                                    color: 'rgba(0, 0, 0, 0.2)'
                                });
                                var pos=0;
                                $.each(this.series, function(){
                                    detailChart.series[pos].setData(myDict[pos].data);
                                    pos++;
                                });
                                
                                
                                

                                return false;
                            }
                        }
                    },
                    title: {
                        text: null
                    },
                    xAxis: {
                        type: 'datetime',
                        showLastTickLabel: true,
                        maxZoom: 14 * 24 * 3600000, // fourteen days
                        plotBands: [{
                            id: 'mask-before',
                            from: dict[0]['data'][0][0],
                            to: dict[0]['data'][dict[0]['data'].length - 1][0],
                            color: 'rgba(0, 0, 0, 0.2)'
                        }],
                        title: {
                            text: null
                        }
                    },
                    yAxis: {
                        gridLineWidth: 0,
                        labels: {
                            enabled: false
                        },
                        title: {
                            text: null
                        },
                        min: 0.6,
                        showFirstLabel: false
                    },
                    tooltip: {
                        formatter: function () {
                            return false;
                        }
                    },
                    legend: {
                        enabled: false
                    },
                    credits: {
                        enabled: false
                    },
                    plotOptions: {
                        series: {
                            fillColor: {
                                linearGradient: [0, 0, 0, 70],
                                stops: [
                                    [0, Highcharts.getOptions().colors[0]],
                                    [1, 'rgba(255,255,255,0)']
                                ]
                            },
                            lineWidth: 1,
                            marker: {
                                enabled: false
                            },
                            shadow: false,
                            states: {
                                hover: {
                                    lineWidth: 1
                                }
                            },
                            enableMouseTracking: false
                        }
                    },

                    series: dict,

                    exporting: {
                        enabled: false
                    }

                }, function (masterChart) {
                    createDetail(masterChart, dict);
                })
                    .highcharts(); // return chart instance
            }
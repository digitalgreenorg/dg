/* This file should contain all the JS for Training dashboard */
window.onload = initialize;

function initialize() {
  // initialize any library here

  // to initialize material select
  $('select').material_select();
  get_data();
  set_eventlistener();
  update_tables();
  update_charts();
}

function get_data(){
  var start_date = $('#from_date').val();
	var end_date = $('#to_date').val();
	if(Date.parse(start_date) > Date.parse(end_date)){
		//$('.modal-trigger').leanModal();
		$('#modal1').openModal();
  }
  else{
    gettrainingdata(start_date, end_date);
    gettrainerdata(start_date, end_date);
    getquestiondata(start_date, end_date);
    getmediatordata(start_date, end_date);
  }
}

/* Progress Bar functions */
function hide_progress_bar() {
  $('#progress_bar').hide()
}

function show_progress_bar() {
	$('#progress_bar').show();
}

// event listeners
function set_eventlistener(){

  // to change the visibility of tables , charts on change in select
  $( "#table_option" ).change(function() {
    update_tables();
  });

  $( "#chart_option" ).change(function() {
    update_charts();
  });

  //datepicker
  $('.datepicker').pickadate({
  	selectMonths: true, // Creates a dropdown to control month
  	selectYears: 15, // Creates a dropdown of 15 years to control year
  	format: 'yyyy-mm-dd'
  });

  //get data button click
  $( "#get_data" ).click(function() {
    get_data();
  });
}

/* show charts */

function show_charts() {
  $("#crop_chart_div").show();
  $("#agg_crop_chart_div").show();
}

/*to change the visibility of tables , charts on change in select*/

function update_tables() {
	var opt = $('#table_option :selected').val();
	if(opt ==1 ){
		$("#village_table").show();
		$("#mediator_table").hide();
	}
	else{
		$("#mediator_table").show();
		$("#village_table").hide();
	}
}

function update_charts() {
  var opt = $('#chart_option :selected').val();
  if(opt ==1 ){
    $("#crop_chart_div").show();
    $("#agg_crop_chart_div").hide();
  }
  else{
    $("#agg_crop_chart_div").show();
    $("#crop_chart_div").hide();
  }
}

/* ajax to get json */

function gettrainingdata(start_date, end_date) {
  show_progress_bar();
  $.get( "/training/training_wise_data/", {'start_date':start_date, 'end_date':end_date})
           .done(function( data ) {
               data_json = JSON.parse(data);
               hide_progress_bar();
               filltrainingtable(data_json);
           });  
}

function gettrainerdata(start_date, end_date) {
  show_progress_bar();
  $.get( "/training/trainer_wise_data/", {'start_date':start_date, 'end_date':end_date})
           .done(function( data ) {
               data_json = JSON.parse(data);
               hide_progress_bar();
               plot_trainerwise_data(data_json);
           });
}

function getquestiondata(start_date, end_date) {
  show_progress_bar();
  $.get( "/training/question_wise_data/", {'start_date':start_date, 'end_date':end_date})
           .done(function( data ) {
               data_json = JSON.parse(data);
               hide_progress_bar();
               plot_questionwise_data(data_json);
           });
}

function getmediatordata(start_date, end_date) {
  show_progress_bar();
  $.get( "/training/mediator_wise_data/", {'start_date':start_date, 'end_date':end_date})
           .done(function( data ) {
               data_json = JSON.parse(data);
               hide_progress_bar();
               plot_mediator_wise_data(data_json);
           });  
}

/* Table Generating UI Functions - Fill data in table */

function filltrainingtable(data_json) {
  $('#table1 tr:gt(0)').remove();
  var row = $('#table1_tbody');
  var tr_name = $('<tr>');
  var table_ref = document.getElementById('table1');
  for ( i =0; i< data_json.length; i++){
     var row = table_ref.insertRow(-1);
     var cell1 = row.insertCell(0);
     var cell2 = row.insertCell(1);
     var cell3 = row.insertCell(2);
     var cell4 = row.insertCell(3);
     var cell5 = row.insertCell(4);
     cell1.innerHTML = data_json[i]['place'];
     cell1.setAttribute('style','text-align:center;');
     cell2.innerHTML = data_json[i]['trainer__name'];
     cell2.setAttribute('style','text-align:center;');
     cell3.innerHTML = data_json[i]['language__language_name'].toString();
     cell3.setAttribute('style','text-align:center;');
     cell4.innerHTML = data_json[i]['participants__count'].toString();
     cell4.setAttribute('style','text-align:center;');
  }
}

/* Fill data for highcharts */
function plot_trainerwise_data(data_json) {
	var vol_data = [];
	var amt_data = [];
	for(var i=0 ; i<data_json.length; i++){
		vol_data.push([data_json[i]['farmer__village__village_name'],  (data_json[i]['quantity__sum']*100.0)/total_volume ])
	}
	for(var i=0 ; i<data_json.length; i++){
		amt_data.push([data_json[i]['farmer__village__village_name'],  (data_json[i]['amount__sum']*100.0)/total_amount ])
	}
	plot_piechart($('#pie_vol'),vol_data,'Villages');
	plot_piechart($('#pie_amount'),amt_data,'Villages');
}

function plot_questionwise_data(data_json){
  var vol_data =[];
  var amt_data = [];
  for(var i=0 ; i<data_json.length; i++){
    vol_data.push([data_json[i]['user_name'],  (data_json[i]['quantity__sum']*100.0)/total_volume ])
  }
  for(var i=0 ; i<data_json.length; i++){
    amt_data.push([data_json[i]['user_name'],  (data_json[i]['amount__sum']*100.0)/total_amount ])
  }
  plot_piechart($('#pie_vol2'),vol_data,'VRP');
  plot_piechart($('#pie_amount2'),amt_data,'VRP');

}

function plot_mediatorwise_data(data_json) {
  var x_axis = data_json['dates'];
  var total_crop_price = [];
  var total_crop_volume = [];
  var total_crop_income = [];
  // crop wise data calculation - amount , volume and price
  for(i=0; i<data_json['crops'].length; i++) {
    var temp_price_dict = {};
    var temp_vol_dict = {};
    var temp_amt_dict = {};
    temp_price_dict['name'] = data_json['crops'][i];
    temp_price_dict['data'] = new Array(x_axis.length).fill(0.0);
    temp_vol_dict['name'] = data_json['crops'][i];
    temp_vol_dict['type'] = "column";
    temp_vol_dict['data'] = new Array(x_axis.length).fill(0.0);
    temp_amt_dict['name'] = data_json['crops'][i];
    temp_amt_dict['type'] = "column";
    temp_amt_dict['data'] = new Array(x_axis.length).fill(0.0);
    for (j=0; j<data_json['transactions'].length; j++) {
      if (data_json['transactions'][j]['crop__crop_name'] == temp_price_dict['name']) {
          var index_date = x_axis.indexOf(data_json['transactions'][j]['date']);
          temp_amt_dict['data'][index_date] = data_json['transactions'][j]['amount__sum'];
          temp_vol_dict['data'][index_date] = data_json['transactions'][j]['quantity__sum'];
          if(temp_vol_dict['data'][index_date] != 0){
            temp_price_dict['data'][index_date] = temp_amt_dict['data'][index_date]/temp_vol_dict['data'][index_date];}
      }
    }
    total_crop_price.push(temp_price_dict);
    total_crop_volume.push(temp_vol_dict);
    total_crop_income.push(temp_amt_dict);
  }

  // assigning farmer counts to volume stacked chart
  var data_dict = {};
  data_dict["name"] = "Farmer Count";
  data_dict["type"] = "line";
  data_dict["yAxis"] = 1;
  data_dict["data"] = new Array(x_axis.length).fill(0);
  for (k=0; k<data_json['farmer_count'].length; k++){
    data_dict["data"][k] = data_json['farmer_count'][k]['farmer__count'];
  }
  total_crop_volume.push(data_dict);

  // crop and mediator wise price calculation
  var total_crop_mediator_price = [];
  for(l=0; l<data_json['crops_mediators'].length; l++){
    var temp_price_dict = {};
    var temp_crop = data_json['crops_mediators'][l]['crop__crop_name'];
    var temp_mediator =  data_json['crops_mediators'][l]['user_name'];
    var temp_mediator_id = data_json['crops_mediators'][l]['user_created__id']
    temp_price_dict['name'] = temp_crop +'-'+ temp_mediator;
    temp_price_dict['data'] = new Array(x_axis.length).fill(0.0);
      for (j=0; j<data_json['crops_mediators_transactions'].length; j++) {
        if (data_json['crops_mediators_transactions'][j]['crop__crop_name'] == temp_crop && data_json['crops_mediators_transactions'][j]['user_created__id'] == temp_mediator_id ){
           var index_date = x_axis.indexOf(data_json['crops_mediators_transactions'][j]['date']);
           var temp_amt_dict = data_json['crops_mediators_transactions'][j]['amount'];
           var temp_vol_dict = data_json['crops_mediators_transactions'][j]['quantity'];
           if(temp_vol_dict != 0){
             temp_price_dict['data'][index_date] = temp_amt_dict/temp_vol_dict;
           }
        }
      }
   total_crop_mediator_price.push(temp_price_dict);
  }
  show_charts();
  // Plot charts
  plot_stacked_chart($("#crops_price"), x_axis, total_crop_income, "Total Amount Earned(₹)", "₹", true);
  plot_multiline_chart($("#crops_price2"), x_axis, total_crop_price, "Crop Price Per Day(₹)", "₹");
  plot_multiline_chart($("#crop_aggregator_price"), x_axis, total_crop_mediator_price, "Crop Price Per Day(₹)");
  plot_stacked_chart($("#crops_volume"), x_axis, total_crop_volume, "Total Volume Dispatched(kg)", "kg", false, /*dashboard.farmers_count*/null);
  update_charts();
}

/* plot highcharts data */

function plot_piechart(container_obj, _data, arg) {
	var chart = {
		plotBackgroundColor: null,
		plotBorderWidth: null,
		plotShadow: false
	};

	var tooltip = {
		pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
	};
	var plotOptions = {
		pie:{
			allowPointSelect: true,
			cursor: 'pointer',
			dataLabels: {
				enabled: true,
				format: '<b>{point.name}%</b>: {point.percentage:.1f} %',
				style: {
				color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
				}
			}
		}
	};

	series= [{
		type: 'pie',
		name: arg,
		data: _data
	}];

	var json = {};
	json.chart = chart;
	json.title = null;
	json.tooltip = tooltip;
	json.series = series;
	json.plotOptions = plotOptions;
	container_obj.highcharts(json);
}

function plot_multiline_chart(container_obj, x_axis, dict, y_axis_text) {
    container_obj.highcharts({
      title: {
        text: ''
      },
      subtitle: {
        text: '',
        x: -20
      },
      xAxis: {
        categories: x_axis,
        labels: {
          rotation: -90
        }
      },
      yAxis: {
        title: {
          text: y_axis_text
        },
        plotLines: [{
          value: 0,
          width: 1,
          color: '#808080'
        }]
      },
      tooltip: {
        valuePrefix: '₹ '
      },
      legend: {
        layout: 'vertical',
        align: 'right',
        verticalAlign: 'middle',
        borderWidth: 0
      },
      series: dict
    });
}

function plot_stacked_chart(container_obj, x_axis, dict, y_axis_text, unit, prefix_or_suffix, farmer_counts) {

  if (farmer_counts) {
    var data_dict = {};
    data_dict["name"] = "Farmer Count";
    data_dict["type"] = "line";
    data_dict["yAxis"] = 1;
    data_dict["data"] = farmer_counts;
    dict.push(data_dict);
  }

  container_obj.highcharts({
    chart: {
      type: 'column'
    },
    xAxis: {
      categories: x_axis,
      labels: {
        rotation: -90
      }
    },
    yAxis: [{
      min: 0,
      title: {
        text: y_axis_text
      },
      stackLabels: {
        enabled: true,
        format: '<b>' + ((prefix_or_suffix)?unit + ' ':'') + '{total:.0f}'+ ((prefix_or_suffix)?'':' ' + unit) + '</b>',
        style: {
          fontWeight: 'bold',
          color: (Highcharts.theme && Highcharts.theme.textColor) || 'gray'
        }
      }
    }, {
      title: {
        text: "Farmer Count",
        style: {
          color: Highcharts.getOptions().colors[0]
        }
      },
      labels: {
        format: '{value}',
        style: {
          color: Highcharts.getOptions().colors[0]
        }
      },
      opposite: true
    }],
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
    tooltip: {
      headerFormat: '<b>{point.x}</b><br/>',
      /*pointFormat: '{series.name}: ' + ((prefix_or_suffix)?unit + ' ':'') + '{point.y:.1f}'+ ((prefix_or_suffix)?'':' ' + unit) + '<br/>Total: ' + ((prefix_or_suffix)?unit + ' ':'') + '{point.stackTotal:.1f}'+ ((prefix_or_suffix)?'':' ' + unit)*/
      shared: true
    },
    plotOptions: {
      column: {
        showCheckbox: true,
        stacking: 'normal',
        dataLabels: {
          enabled: true,
          format: ' ',
          color: (Highcharts.theme && Highcharts.theme.dataLabelsColor) || 'white',
          style: {
            textShadow: '0 0 3px black'
          }
        }
      }
    },
    series: dict
  });
}

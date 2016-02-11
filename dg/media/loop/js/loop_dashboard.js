// This file should contain all the JS for Loop dashboard
window.onload = initialize;
function initialize() {
  // initialize any library here
  $('select').material_select();
  show_charts();
  getvillagedata();
}
function hide_progress_bar() {
  $('#progress_bar').hide()
}
function show_progress_bar() {
	$('#progress_bar').show();
}
// ajax to get json
function getvillagedata() {
  show_progress_bar();
  $.get( "/loop/village_wise_data/", {})
           .done(function( data ) {
               data_json = JSON.parse(data);
               hide_progress_bar();
               fillvillagetable(data_json);
           });
}
function getmediatordata() {
  show_progress_bar();
  $.get( "/loop/mediator_wise_data/", {})
           .done(function( data ) {
               data_json = JSON.parse(data);
               hide_progress_bar();
               fillmediatortable(data_json);
           });
}
function getcropdata() {
  show_progress_bar();
  $.get( "/loop/crop_wise_data/", {})
           .done(function( data ) {
               data_json = JSON.parse(data);
               hide_progress_bar();
               plot_cropwise_data(data_json);
           });
}
//fill data in tables
function fillvillagetable(data_json) {
  $('#table1 tr:gt(0)').remove();
  var row = $('#table1_tbody');
  var tr_name = $('<tr>');
  var table_ref = document.getElementById('table1');
  var total_volume = 0;
  var total_amount = 0;
  var total_farmers = 0;
  var total_avg = 0;
  var str1 = "₹ "
  for ( i =0; i< data_json.length; i++)
  {
     var row = table_ref.insertRow(-1);
     var cell1 = row.insertCell(0);
     var cell2 = row.insertCell(1);
     var cell3 = row.insertCell(2);
     var cell4 = row.insertCell(3);
     var cell5 = row.insertCell(4);

     cell1.innerHTML = data_json[i]['farmer__village__village_name'];
     cell2.innerHTML = data_json[i]['quantity__sum'].toString().concat(" Kg");
     cell3.innerHTML = data_json[i]['amount__sum'].toString();
     cell4.innerHTML = data_json[i]['farmer__count'].toString();
     var avg = (data_json[i]['farmer__count'])/(data_json[i]['date__count']).toFixed(1);
     cell5.innerHTML = avg;

     total_volume += data_json[i]['quantity__sum'];
     total_amount += data_json[i]['amount__sum'];
     total_farmers+= data_json[i]['farmer__count'];
     total_avg+= avg;
  }
 /*if there are entries in the table*/
 if(data_json.length){
   var row = table_ref.insertRow(-1);
   var cell1 = row.insertCell(0);
   var cell2 = row.insertCell(1);
   var cell3 = row.insertCell(2);
   var cell4 = row.insertCell(3);
   var cell5 = row.insertCell(4);
   cell1.innerHTML = "TOTAL";
   cell1.style.fontWeight = "bold";
   cell2.innerHTML = total_volume.toString().concat(" Kg");
   cell2.style.fontWeight = "bold";
   cell3.innerHTML = str1.concat(total_amount).toString();
   cell3.style.fontWeight = "bold";
   cell4.innerHTML = total_farmers;
   cell4.style.fontWeight = "bold";
   cell5.innerHTML = total_avg/data_json.length;
   cell5.style.fontWeight = "bold";
   /*function call to make mediator pie chart*/
   plot_village_data(data_json,total_volume,total_amount);
 }
}
function fillmediatortable(data_json) {
  var table_ref = document.getElementById("table2");
  $('#table2 tr:gt(0)').remove();
  row = $('#table2_tbody');
  tr_name = $('<tr>');
  row.append(tr_name);

  var mediator_info = dashboard.mediator_info; // mediator info from dashboard to populate table2
  var mediators = dashboard.active_mediators; //unique active mediators
  var Total_Volume = 0;
  var Total_Amount = 0;
  var Total_Farmers = 0;
  var Total_avg = 0;
  var str1 = "₹ "
  for (var i = 0; i < mediators.length; i++) {
    var row = table_ref.insertRow(-1);
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);
    var cell4 = row.insertCell(3);
    var cell5 = row.insertCell(4);

    cell1.innerHTML = mediators[i];
    cell2.innerHTML = print_number(mediator_info[i].total_volume).toString().concat(" Kg");
    cell3.innerHTML =str1.concat(print_number(mediator_info[i].pay_amount).toString());
    cell4.innerHTML =  Object.keys(mediator_info[i].active_farmers).length;
    var avg = (Object.size(mediator_info[i].active_farmers)*1.0)/diffDays;
    cell5.innerHTML = print_number(avg);

    Total_Volume += mediator_info[i].total_volume;
    Total_Amount += mediator_info[i].pay_amount;
    Total_Farmers+=Object.keys(mediator_info[i].active_farmers).length;
    Total_avg+=(Object.size(mediator_info[i].active_farmers)*1.0)/diffDays;
  };
  if(mediators.length){
    var row = table_ref.insertRow(-1);
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);
    var cell4 = row.insertCell(3);
    var cell5 = row.insertCell(4);
    cell1.innerHTML = "TOTAL";
    cell1.style.fontWeight = "bold";
    cell2.innerHTML = print_number(Total_Volume).toString().concat(" Kg");
    cell2.style.fontWeight = "bold";
    cell3.innerHTML = str1.concat(print_number(Total_Amount).toString());
    cell3.style.fontWeight = "bold";
    cell4.innerHTML = print_number(Total_Farmers);
    cell4.style.fontWeight = "bold";
    cell5.innerHTML = print_number(Total_avg);
    cell5.style.fontWeight = "bold";
  }
  /*function call to make mediator pie chart*/
  plot_mediator_data(dashboard.mediator_info,dashboard.total_volume,dashboard.total_amount);
}
// fill data for highcharts
function plot_village_data(data_json,total_volume,total_amount) {
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
function plot_mediator_data(mediator_info,Total_Volume,Total_Amount){
  var vol_data =[];
  var amt_data = [];
  for(var i=0 ; i<mediator_info.length; i++){
    vol_data.push([mediator_info[i].name,  (mediator_info[i].total_volume*100.0)/Total_Volume ])
  }
  for(var i=0 ; i<mediator_info.length; i++){
    amt_data.push([mediator_info[i].name,  (mediator_info[i].pay_amount*100.0)/Total_Amount ])
  }
  plot_piechart($('#pie_vol2'),vol_data,'VRP');
  plot_piechart($('#pie_amount2'),amt_data,'VRP');

}
function plot_cropwise_data(data_json) {
  //show_charts();
  /* First plot cropwise prices stacked chart */
  plot_stacked_chart($("#crops_price"), data_json.length, dashboard.crops_purchase, "Total Amount Earned(₹)", "₹", true);
  plot_multiline_chart($("#crops_price2"), data_json.length, dashboard.crops_price, "Crop Price Per Day(₹)");
  plot_multiline_chart($("#crop_aggregator_price"), data_json.length, dashboard.crop_aggregator_price, "Crop Price Per Day(₹)");
  plot_stacked_chart($("#crops_volume"), data_json.length, dashboard.crops_volume, "Total Volume Dispatched(kg)", "kg", false, dashboard.farmers_count);
  //update_charts();
}
// show charts
function show_charts() {
  $("#crop_chart_div").show();
  $("#agg_crop_chart_div").show();
}
// plot highcharts data
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
  /* from the given dict we need to create a list suitable for highcharts api */
  multiline_data_list = [];
  $.each(dict, function(key, value) {
    var data_dict = {};
    data_dict["name"] = key;
    data_dict["data"] = value;
    multiline_data_list.push(data_dict);
  });
  $(function () {
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
      series: multiline_data_list
    });
  });
}
function plot_stacked_chart(container_obj, x_axis, dict, y_axis_text, unit, prefix_or_suffix, farmer_counts) {
  /* from the given dict we need to create a list suitable for highcharts api */
  stack_data_list = [];
  $.each(dict, function(key, value) {
    var data_dict = {};
    data_dict["name"] = key;
    data_dict["type"] = "column";
    /*data_dict["yAxis"] = 1;*/
    data_dict["data"] = value;
    data_dict["tooltip"] = {
      valueSuffix: ((prefix_or_suffix)?'':unit),
      valuePrefix: ((prefix_or_suffix)?unit:'')};
    stack_data_list.push(data_dict);
  });
  if (farmer_counts) {
    var data_dict = {};
    data_dict["name"] = "Farmer Count";
    data_dict["type"] = "line";
    data_dict["yAxis"] = 1;
    data_dict["data"] = farmer_counts;
    stack_data_list.push(data_dict);
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
    series: stack_data_list
  });
}

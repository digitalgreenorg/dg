// This file should contain all the JS for Loop dashboard
window.onload = initialize;
function initialize() {
  // initialize any library here
  // First ajax to get json
  // Init highcharts
  // fill data in highcharts
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

function getvillagedata()
{
  show_progress_bar();
  $.get( "/loop/village_wise_data/", {})
           .done(function( data ) {
               data_json = JSON.parse(data);
               hide_progress_bar();
               fillvillagetable(data_json);

           });
}
function fillvillagetable(data_json)
{
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
   plot_village_data(data_json,total_volume,total_amount);
 }
}
function plot_village_data(data_json,total_volume,total_amount){
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
function show_charts() {
	$("#crop_chart_div").show();
	$("#agg_crop_chart_div").show();
}

google.load("visualization", "1", {packages:["controls"]});
google.setOnLoadCallback(drawCharts);

var geog_pie_chart;
var geog_pie_chart_data;
var exp_geog_pie_chart;
var exp_monthwise_column_chart;
var exp_total_line_chart;
var exp_percent_line_chart;
var exp_practice_bubble_chart;
var exp_gender_pie_chart;
var exp_day_line_chart;

var pie_options= {colors: ['#7edc32','#ced916','#26d52f','#05f866','#d6cc57','#909504','#f9c423','#3bfaab','#51be72','#f5f772','#86ec5e','#f2b030','#96267d']};
var line_options={colors: ['#FFCC00','#999999','#3366FF','#FF0000','#996633','#FF9900','#333333,#000066','#CC0033','#663300'],
		lineWidth: 1,
		hAxis: {slantedText: false, maxAlternation: 1}
};
var column_options={colors: ['#ced916','#7edc32','#26d52f','#05f866','#f9c423','#3bfaab'],
		bar : {groupWidth: '80%'}};
var bubble_options={colors: ['00CC33','#7edc32','#26d52f','#909504','#f9c423','#3bfaab'],
		legend: {position: 'none'},
		sizeAxis: {maxSize: 20}, 
		bubble: {textStyle: {color: 'none'}}
};
function drawCharts() {
	$.getJSON('/analytics/screening_geog_pie_data/'+search_params, function(json){geog_pie(json);});
	$.getJSON('/analytics/screening_monthwise_bar_data/'+search_params, function(json){monthwise_column(json);});
	$.getJSON('/analytics/screening_practice_wise_scatter_data/'+search_params, function(json){practice_bubble(json);});
	$.getJSON('/analytics/screening_mf_ratio/'+search_params, function(json){gender_pie(json);});
	$.getJSON('/analytics/screening_per_day_line/'+search_params, function(json){day_line(json);});
	$.getJSON('/analytics/screening_tot_lines/'+search_params, function(json){total_line(json);});
	$.getJSON('/analytics/screening_percent_lines/'+search_params, function(json){percent_line(json);});
}

function remove_loader(div_id){
	document.getElementById(div_id).style.backgroundImage = "none";
}

function geog_pie(json) {

	geog_pie_chart_data = google.visualization.arrayToDataTable(json,false);
	var options = jQuery.extend(true, {}, pie_options);
	options['sliceVisibilityThreshold']=1.0/10000;
	geog_pie_chart = new google.visualization.ChartWrapper({
		'chartType':'PieChart',
		'containerId':'javascript_geogwise_pie',
		'options':options,
		'dataTable':geog_pie_chart_data
	});
	geog_pie_chart.draw();
	google.visualization.events.addListener(geog_pie_chart, 'select', geog_pie_click);
	exp_geog_pie_chart=new google.visualization.ChartWrapper({
		'chartType':'PieChart',
		'options':options,
		'dataTable':geog_pie_chart_data
	});
}

function geog_pie_click(e) {
	if(geog_pie_chart.getChart().getSelection()[0])
	{
		url=geog_pie_chart_data.getValue(geog_pie_chart.getChart().getSelection()[0].row, 2);
		if(url!='')
		{
			top.location.href=url;			   
		}
	}
}

function monthwise_column(json) {

	var monthwise_column_chart_data = google.visualization.arrayToDataTable(json,false);
	var options = jQuery.extend(true, {}, column_options);
	options['chartArea']={left:70,top:20,width:"80%",height:"80%"};
	options['vAxis']= {title: 'Number of Disseminations'};
	options['legend']= {position: 'bottom'};

	var monthwise_column_chart = new google.visualization.ChartWrapper({
		'chartType':'ColumnChart',
		'containerId':'javascript_monthwise_column',
		'options':options,
		'dataTable':monthwise_column_chart_data
	});
	remove_loader(monthwise_column_chart.getContainerId());
	monthwise_column_chart.draw();
	exp_monthwise_column_chart=new google.visualization.ChartWrapper({
		'chartType':'ColumnChart',
		'options':options,
		'dataTable':monthwise_column_chart_data
	});
}

function total_line(json) {

	var total_line_chart_data = google.visualization.arrayToDataTable(json,false);
	var options = jQuery.extend(true, {}, line_options);
	options['vAxis']= {title: 'No. of Persons'};
	options['legend']= {position: 'top', alignment: 'start', textStyle: {fontSize: 9}};
	options['chartArea']={left:60,top:40,width:"85%",height:"75%"};


	var total_line_chart = new google.visualization.ChartWrapper({
		'chartType':'LineChart',
		'containerId':'javascript_total_line',
		'options':options,
		'dataTable':total_line_chart_data
	});
	remove_loader(total_line_chart.getContainerId());
	total_line_chart.draw();
	exp_total_line_chart=new google.visualization.ChartWrapper({
		'chartType':'LineChart',
		'options':options,
		'dataTable':total_line_chart_data
	});
	$("span").remove();
}

function percent_line(json) {

	var percent_line_chart_data = google.visualization.arrayToDataTable(json,false);
	var options = jQuery.extend(true, {}, line_options);
	options['legend']= {position: 'top', alignment: 'start', textStyle: {fontSize: 9}};
	options['chartArea']={left:60,top:40,width:"85%",height:"70%"};

	var percent_line_chart = new google.visualization.ChartWrapper({
		'chartType':'LineChart',
		'containerId':'javascript_percent_line',
		'options':options,
		'dataTable':percent_line_chart_data
	});
	remove_loader(percent_line_chart.getContainerId());
	percent_line_chart.draw();
	$("span").remove();
	exp_percent_line_chart=new google.visualization.ChartWrapper({
		'chartType':'LineChart',
		'options':options,
		'dataTable':percent_line_chart_data
	});
}

function practice_bubble(json) {

	var practice_bubble_chart_data = google.visualization.arrayToDataTable(json,false);
	if(json.length>1)
	{
		var xrange=practice_bubble_chart_data.getColumnRange(1);
		var yrange=practice_bubble_chart_data.getColumnRange(2);
		var options = jQuery.extend(true, {}, bubble_options);
		options['hAxis']= {title: 'Practices',  maxValue: xrange.max, minValue: xrange.min, gridlines:{count:10},textColor: '#ffffff'};
		options['vAxis']= {title: 'Number of Disseminations',gridlines:{count:10}, maxValue: yrange.max };
		options['sizeAxis']={maxSize: 20};
		options['chartArea']={left:60,top:40,width:"85%",height:"75%"};

	}
	var practice_bubble_chart = new google.visualization.ChartWrapper({
		'chartType':'BubbleChart',
		'containerId':'javascript_practice_type_bubble',
		'options':options,
		'dataTable':practice_bubble_chart_data
	});
	remove_loader(practice_bubble_chart.getContainerId());
	practice_bubble_chart.draw();
	exp_practice_bubble_chart=new google.visualization.ChartWrapper({
		'chartType':'BubbleChart',
		'options':options,
		'dataTable':practice_bubble_chart_data
	});
	$("span").remove();
}

function gender_pie(json) {

	var gender_pie_chart_data = google.visualization.arrayToDataTable(json,false);
	var options = jQuery.extend(true, {}, pie_options);
	options['legend']={position: 'bottom' };
	var gender_pie_chart = new google.visualization.ChartWrapper({
		'chartType':'PieChart',
		'containerId':'javascript_gender_pie',
		'options':options,
		'dataTable':gender_pie_chart_data
	});
	gender_pie_chart.draw();
	exp_gender_pie_chart=new google.visualization.ChartWrapper({
		'chartType':'PieChart',
		'options':options,
		'dataTable':gender_pie_chart_data
	});
	$("span").remove();
}

function day_line(json) {
	var day_line_chart_data = google.visualization.arrayToDataTable(json,false);
	var options = jQuery.extend(true, {}, line_options);
	options['legend']={position: 'in'};
	options['chartArea']={left: 70,top:20,width:"90%",height:"85%"};
	var day_line_chart = new google.visualization.ChartWrapper({
		'chartType':'LineChart',
		'containerId':'javascript_day_line',
		'options':options,
		'dataTable':day_line_chart_data
	});
	remove_loader(day_line_chart.getContainerId());
	day_line_chart.draw();
	exp_day_line_chart=new google.visualization.ChartWrapper({
		'chartType':'LineChart',
		'options':options,
		'dataTable':day_line_chart_data
	});
	$("span").remove();
}


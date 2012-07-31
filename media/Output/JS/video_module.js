google.load("visualization", "1", {packages:["controls"]});
google.setOnLoadCallback(drawCharts);

var geog_pie_chart;
var geog_pie_chart_data;

var exp_geog_pie_chart;
var exp_gender_pie_chart;
var actor_pie_chart;
var exp_type_pie_chart;
var exp_total_line_chart;
var exp_practice_bubble_chart;
var exp_language_bubble_chart;
var exp_monthwise_column_chart;
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
	$.getJSON('/analytics/video_geog_pie_data/?'+search_params, function(json){geog_pie(json)});
	$.getJSON('/analytics/video_actor_wise_pie/?'+search_params, function(json){actor_pie(json)});
	$.getJSON('/analytics/video_pie_graph_mf_ratio/?'+search_params, function(json){gender_pie(json)});
	$.getJSON('/analytics/video_monthwise_bar_data/?'+search_params, function(json){monthwise_column(json);});
	$.getJSON('/analytics/video_type_wise_pie/?'+search_params, function(json){type_pie(json)});
	$.getJSON('/analytics/video_language_wise_scatter_data/?'+search_params, function(json){language_bubble(json)});
	$.getJSON('/analytics/video_practice_wise_scatter/?'+search_params, function(json){practice_bubble(json)});
	$.getJSON('/analytics/overview_line_graph/?'+search_params,{type:['prod', 'prod_tar']}, function(json){total_line(json)});
}
function monthwise_column(json) {

	var monthwise_column_chart_data = google.visualization.arrayToDataTable(json,false);
	var options = jQuery.extend(true, {}, column_options);
	options['chartArea']={left:70,top:20,width:"80%",height:"80%"};
	options['vAxis']= {title: 'Number of Videos'};
	options['legend']= {position: 'bottom'};

	var monthwise_column_chart = new google.visualization.ChartWrapper({
		'chartType':'ColumnChart',
		'containerId':'javascript_monthwise_column',
		'options':options,
		'dataTable':monthwise_column_chart_data
	});

	monthwise_column_chart.draw();
	exp_monthwise_column_chart=new google.visualization.ChartWrapper({
		'chartType':'ColumnChart',
		'options':options,
		'dataTable':monthwise_column_chart_data
	});
}

function language_bubble(json) {

	var language_bubble_chart_data = google.visualization.arrayToDataTable(json,false);
	var xrange=language_bubble_chart_data.getColumnRange(1);
	var yrange=language_bubble_chart_data.getColumnRange(2);
	var options = jQuery.extend(true, {}, bubble_options);
	options['hAxis']= {title: 'Languages',  maxValue: xrange.max, minValue: xrange.min, gridlines:{count:10}};
	options['vAxis']= {title: 'Number of Videos',gridlines:{count:10}, maxValue: yrange.max };
	options['sizeAxis']={maxSize: 20};

	var language_bubble_chart = new google.visualization.ChartWrapper({
		'chartType':'BubbleChart',
		'containerId':'javascript_language_bubble',
		'options':options,
		'dataTable':language_bubble_chart_data
	});
	language_bubble_chart.draw(json);
	exp_language_bubble_chart=new google.visualization.ChartWrapper({
		'chartType':'BubbleChart',
		'options':options,
		'dataTable':language_bubble_chart_data
	});
}

function geog_pie(json) {
	geog_pie_chart_data = google.visualization.arrayToDataTable(json,false);
	var options = jQuery.extend(true, {}, pie_options);
	options['sliceVisibilityThreshold']=1.0/10000;
	options['legend'] = { position: 'right', textStyle: {fontSize: 14},alignment: 'center' };
	options['chartArea']={left:100,top:30,width:"70%",height:"70%"};
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

function type_pie(json) {

	var type_pie_chart_data = google.visualization.arrayToDataTable(json,false);
	var options = jQuery.extend(true, {}, pie_options);
	options['chartArea']={left:100,top:30,width:"80%",height:"70%"};
	options['legend'] = { position: 'right', textStyle: {fontSize: 14},alignment: 'center' };

	var type_pie_chart = new google.visualization.ChartWrapper({
		'chartType':'PieChart',
		'containerId':'javascript_type_pie',
		'options':options,
		'dataTable':type_pie_chart_data
	});
	type_pie_chart.draw(json);
	exp_type_pie_chart=new google.visualization.ChartWrapper({
		'chartType':'PieChart',
		'options':options,
		'dataTable':type_pie_chart_data
	});
}
function practice_bubble(json) {

	var practice_bubble_chart_data = google.visualization.arrayToDataTable(json,false);
	var xrange=practice_bubble_chart_data.getColumnRange(1);
	var yrange=practice_bubble_chart_data.getColumnRange(2);
	var options = jQuery.extend(true, {}, bubble_options);
	options['hAxis']= {title: 'Practices',  maxValue: xrange.max, minValue: xrange.min, gridlines:{count:12},textColor: '#ffffff'};
	options['vAxis']= {title: 'Number of Videos',gridlines:{count:10} };
	options['chartArea']={left:60,top:40,width:"85%",height:"75%"};
	options['sizeAxis']={maxSize: 20};

	var practice_bubble_chart = new google.visualization.ChartWrapper({
		'chartType':'BubbleChart',
		'containerId':'javascript_practice_bubble',
		'options':options,
		'dataTable':practice_bubble_chart_data
	});
	practice_bubble_chart.draw();
	exp_practice_bubble_chart=new google.visualization.ChartWrapper({
		'chartType':'BubbleChart',
		'options':options,
		'dataTable':practice_bubble_chart_data
	});
}
function total_line(json) {

	var total_line_chart_data = google.visualization.arrayToDataTable(json,false);
	var options = jQuery.extend(true, {}, line_options);
	options['vAxis']= {title: 'No. of Persons'};
	options['legend']= {position: 'top', alignment: 'center', textStyle: {fontSize: 12}};
	options['chartArea']={left:60,top:40,width:"85%",height:"75%"};


	var total_line_chart = new google.visualization.ChartWrapper({
		'chartType':'LineChart',
		'containerId':'javascript_total_line',
		'options':options,
		'dataTable':total_line_chart_data
	});

	total_line_chart.draw();
	exp_total_line_chart=new google.visualization.ChartWrapper({
		'chartType':'LineChart',
		'options':options,
		'dataTable':total_line_chart_data
	});
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
}

function actor_pie(json) {

	var actor_pie_chart_data = google.visualization.arrayToDataTable(json,false);
	var options = jQuery.extend(true, {}, pie_options);
	options['legend']={position: 'bottom' };
	var actor_pie_chart = new google.visualization.ChartWrapper({
		'chartType':'PieChart',
		'containerId':'javascript_actor_pie',
		'options':options,
		'dataTable':actor_pie_chart_data
	});
	actor_pie_chart.draw();
	exp_actor_pie_chart=new google.visualization.ChartWrapper({
		'chartType':'PieChart',
		'options':options,
		'dataTable':actor_pie_chart_data
	});
}	

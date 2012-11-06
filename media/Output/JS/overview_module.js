google.load("visualization", "1", {packages:["controls"]});
google.setOnLoadCallback(drawCharts);

var exp_total_line_chart;
var line_options={colors: ['#FFCC00','#999999','#3366FF','#FF0000','#996633','#FF9900','#333333','#000066','#CC0033','#663300'],
		lineWidth: 1,
		hAxis: {slantedText: false, maxAlternation: 1}
};

function drawCharts() {

	$.getJSON('/analytics/overview_line_graph/'+search_params,{type:['prod', 'screen', 'prac', 'person', 'adopt']}, function(json){overview_line(json);});
}
function overview_line(json){
	var total_line_chart_data = google.visualization.arrayToDataTable(json,false);
	var options = jQuery.extend(true, {}, line_options);
	options['legend']= {position: 'bottom', alignment: 'start', textStyle: {fontSize: 12}};
	options['chartArea']={left:100,top:40,width:"90%",height:"70%"};


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

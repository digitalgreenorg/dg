google.load("visualization", "1", {packages:["controls"]});
google.setOnLoadCallback(drawCharts);

var geog_pie_chart;
var geog_pie_chart_data;
var practice_bubble_chart;
var practice_bubble_chart_data;
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
	if(json.length>1)
	{
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
	remove_loader('javascript_monthwise_column');
}

function total_line(json) {

	var total_line_chart_data = google.visualization.arrayToDataTable(json,false);
	if (json.length>1)
	{
		var options = jQuery.extend(true, {}, line_options);
		options['vAxis']= {title: 'Number of Persons'};
		options['legend']= {position: 'top', alignment: 'start', textStyle: {fontSize: 9}};
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
	remove_loader('javascript_total_line');
}

function percent_line(json) {

	var percent_line_chart_data = google.visualization.arrayToDataTable(json,false);
	if (json.length>1)
	{
		var options = jQuery.extend(true, {}, line_options);
		options['legend']= {position: 'top', alignment: 'start', textStyle: {fontSize: 9}};
		options['chartArea']={left:60,top:40,width:"85%",height:"70%"};

		var percent_line_chart = new google.visualization.ChartWrapper({
			'chartType':'LineChart',
			'containerId':'javascript_percent_line',
			'options':options,
			'dataTable':percent_line_chart_data
		});

		percent_line_chart.draw();
		exp_percent_line_chart=new google.visualization.ChartWrapper({
			'chartType':'LineChart',
			'options':options,
			'dataTable':percent_line_chart_data
		});
	}
	remove_loader('javascript_percent_line');
}

function practice_bubble(json) {
	practice_bubble_chart_data = google.visualization.arrayToDataTable(json,false);
	var options = jQuery.extend(true, {}, bubble_options);
	options['hAxis']= {title: 'Practice level', gridlines:{count:12},textColor: '#ffffff',logScale:true};
	options['vAxis']= {title: 'Number of disseminations',gridlines:{count:10},logScale:true};
	options['chartArea']={left:60,top:50,width:"85%",height:"75%"};
	options['sizeAxis']={maxSize: 20,minSize:10};
	options['title']='Number of disseminations per practice';
	if(json.length>1)
	{
		practice_bubble_chart = new google.visualization.ChartWrapper({
			'chartType':'BubbleChart',
			'containerId':'javascript_practice_type_bubble',
			'options':options,
			'dataTable':google.visualization.data.group(practice_bubble_chart_data,[5],[{'column': 6, 'aggregation': custom_rand, 'type': 'number'},
			                                                                            {'column': 7, 'aggregation': google.visualization.data.sum, 'type': 'number'},
			                                                                            {'column': 8, 'aggregation': google.visualization.data.min, 'type': 'string'},
			                                                                            {'column': 9, 'aggregation': google.visualization.data.sum, 'type': 'number'}])
		});

		fillSelect(practice_bubble_chart_data.getDistinctValues(1),"sec","Any");
		fillSelect(practice_bubble_chart_data.getDistinctValues(2),"subsec","Any");
		fillSelect(practice_bubble_chart_data.getDistinctValues(3),"top","Any");
		fillSelect(practice_bubble_chart_data.getDistinctValues(4),"subtop","Any");
		fillSelect(practice_bubble_chart_data.getDistinctValues(5),"sub","Any");
		exp_practice_bubble_chart=new google.visualization.ChartWrapper({
			'chartType':'BubbleChart',
			'options':options,
			'dataTable':google.visualization.data.group(practice_bubble_chart_data,[5],[{'column': 6, 'aggregation': custom_rand, 'type': 'number'},
			                                                                            {'column': 7, 'aggregation': google.visualization.data.sum, 'type': 'number'},
			                                                                            {'column': 8, 'aggregation': google.visualization.data.min, 'type': 'string'},
			                                                                            {'column': 9, 'aggregation': google.visualization.data.sum, 'type': 'number'}])
		});
		init();
		practice_bubble_chart.draw();
	}
	else
	{
		draw_radio();
	}
	remove_loader("javascript_practice_type_bubble");
}


function chartDraw(sec,subsec,top,subtop,sub,number) {
	var plot_view=new google.visualization.DataView(practice_bubble_chart_data);
	var params=new Array;
	if (sec!="Any")
	{
		params.push({column: 1, value: sec });
	}
	if (subsec!="Any")
	{
		params.push({column: 2, value: subsec });
	}
	if (top!="Any")
	{
		params.push({column: 3, value: top });
	}
	if (subtop!="Any")
	{
		params.push({column: 4, value: subtop });
	}
	if (sub!="Any")
	{
		params.push({column: 5, value: sub });
	}
	if(params.length>0)
	{
		plot_view.setRows(plot_view.getFilteredRows(params));  
	}

	var filtered_data=  google.visualization.data.group(plot_view,[parseInt(number)+1],[{'column': 6, 'aggregation': custom_rand, 'type': 'number'},
	                                                                                    {'column': 7, 'aggregation': google.visualization.data.sum, 'type': 'number'},
	                                                                                    {'column': 8, 'aggregation': google.visualization.data.min, 'type': 'string'},
	                                                                                    {'column': 9, 'aggregation': google.visualization.data.sum, 'type': 'number'}]);
	var null_filtered_data=new google.visualization.DataView(filtered_data);
	null_filtered_data.hideRows(null_filtered_data.getFilteredRows([{column: 0, value: null}]));
	practice_bubble_chart.setDataTable(null_filtered_data);
	exp_practice_bubble_chart.setDataTable(null_filtered_data);
	practice_bubble_chart.draw();
}

function custom_rand(values) {
	return values[Math.floor((Math.random()*values.length))];
}

function fillSelect(values,sel_id,sel) {
	var null_ind=values.indexOf(null);
	if(null_ind!=-1)
	{
		values.splice(null_ind,1);
	}

	var html_values="";
	i=0;
	html_values=html_values+"<option selected='selected'>Any</option>"
	for (item in values){
		if(values[item]==sel)
		{
			html_values=html_values+"<option selected='selected'>"+values[item]+"</option>"
		}
		else
		{
			html_values=html_values+"<option>"+values[item]+"</option>"
		}
		i=i+1;
	}
	$("#"+sel_id).html(html_values);
}

function ValChange(sec,subsec,top,subtop,sub,number) {
	var data_view=new google.visualization.DataView(practice_bubble_chart_data);
	var params=new Array;
	if (sec!="Any")
	{
		params.push({column: 1, value: sec });
	}
	if (subsec!="Any")
	{
		params.push({column: 2, value: subsec });
	}
	if (top!="Any")
	{
		params.push({column: 3, value: top });
	}
	if (subtop!="Any")
	{
		params.push({column: 4, value: subtop });
	}
	if (sub!="Any")
	{
		params.push({column: 5, value: sub });
	}
	if(params.length>0)
	{
		data_view.setRows(data_view.getFilteredRows(params));
	}
	fillSelect(data_view.getDistinctValues(1),"sec",sec);
	fillSelect(data_view.getDistinctValues(2),"subsec",subsec);
	fillSelect(data_view.getDistinctValues(3),"top",top);
	fillSelect(data_view.getDistinctValues(4),"subtop",subtop);
	fillSelect(data_view.getDistinctValues(5),"sub",sub);
	chartDraw(sec,subsec,top,subtop,sub,number);

}
function init()
{
	fillSelect(practice_bubble_chart_data.getDistinctValues(1),"sec","Any");
	fillSelect(practice_bubble_chart_data.getDistinctValues(2),"subsec","Any");
	fillSelect(practice_bubble_chart_data.getDistinctValues(3),"top","Any");
	fillSelect(practice_bubble_chart_data.getDistinctValues(4),"subtop","Any");
	fillSelect(practice_bubble_chart_data.getDistinctValues(5),"sub","Any");
	draw_radio();
	radio_value();
	chartDraw("Any","Any","Any","Any","Any",radio_value());

}

function draw_radio()
{
	html="<input type='radio' name ='prac_n' value=0 style='margin-left:10px;' onClick='onClickRadio();'/>Sector" +
	"<input type='radio' name ='prac_n' value=1 style='margin-left:34px;' onClick='onClickRadio();'/>Subsector" +
	"<input type='radio' name ='prac_n' value=2 style='margin-left:23px;' onClick='onClickRadio();'/>Topic" +
	"<input type='radio' name ='prac_n' value=3 style='margin-left:43px;' onClick='onClickRadio();'/>Subtopic" +
	"<input type='radio' name ='prac_n' value=4 CHECKED style='margin-left:28px;' onClick='onClickRadio();'/>Subject";
	$("#practice").html(html);
}

function onClickRadio() {
	var sec = document.getElementById('sec').value;
	var subsec = document.getElementById('subsec').value;
	var top = document.getElementById('top').value;
	var subtop = document.getElementById('subtop').value;
	var sub = document.getElementById('sub').value;
	chartDraw(sec, subsec, top, subtop, sub, radio_value());

}

function radio_value()
{
	var radios = document.getElementsByName('prac_n');
	for ( var i = 0; i < radios.length; i++) {
		if(radios[i].checked) {
			return radios[i].value
		}
	}
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

function day_line(json) {
	var day_line_chart_data = google.visualization.arrayToDataTable(json,false);
	if(json.length>1)
	{
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
	}
	remove_loader('javascript_day_line');
}


/* This file should contain all the JS for Training dashboard */
window.onload = initialize;

function initialize() {
  // initialize any library here

  // to initialize material select
  $('select').material_select();
  get_filter_data();
  set_eventlistener();
  // update_tables();
  // update_charts();
  $(".button-collapse").sideNav();
}

/* Progress Bar functions */

function hide_progress_bar() {
  $('#progress_bar').hide()
}

function show_progress_bar() {
  $('#progress_bar').show();
}

/* set event listeners here */

function set_eventlistener(){

  // to change the visibility of tables, charts on change in select
  $("#table_option").change(function() {
    update_tables();
  });

  $("#chart_option").change(function() {
    update_charts();
  });

  //datepicker
  $('.datepicker').pickadate({
    selectMonths: true, // Creates a dropdown to control month
    selectYears: 15, // Creates a dropdown of 15 years to control year
    format: 'yyyy-mm-dd'
  });

  set_filterlistener();

  //get data button click
  $("#get_data").click(function() {
    get_data();
  });

    // apply filter button click
  $('#apply_filter').click(function() {
    get_data();
  });
}

/* event listeners for filters */

function set_filterlistener() {
  $('#trainer_all').on('change', function(e) {
    if (this.checked) {
      $('#trainers').children().each(function() {
          var trainers_all = $(this).children()[1].firstChild;
          trainers_all.checked = true;
         });
    }
    else {
      $('#trainers').children().each(function() {
          var trainers_all = $(this).children()[1].firstChild;
          trainers_all.checked = false;
         });
    }
  });

  $('#question_all').on('change', function(e) {
    if (this.checked) {
      $('#questions').children().each(function() {
          var questions_all = $(this).children()[1].firstChild;
          questions_all.checked = true;
         });
    }
    else {
      $('#questions').children().each(function() {
          var questions_all = $(this).children()[1].firstChild;
          questions_all.checked = false;
         });
    }
  });
}

/* show charts */

function show_charts() {
  $("#crop_chart_div").show();
  $("#agg_crop_chart_div").show();
}

/* to change the visibility of tables, charts on change in select */

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

/* get data according to filters */

function get_data(){
  var start_date = $('#from_date').val();
	var end_date = $('#to_date').val();

  var trainer_ids = [];
  var question_ids = [];

  $('#trainers').children().each(function(){
    var trainer_div = $(this).children()[1].firstChild;
    if(trainer_div.checked)
      trainer_ids.push(trainer_div.getAttribute('data'));
  });

  $('#questions').children().each(function(){
    var question_div = $(this).children()[1].firstChild;
    if(question_div.checked)
      question_ids.push(question_div.getAttribute('data'));
  });

	if(Date.parse(start_date) > Date.parse(end_date)){
		//$('.modal-trigger').leanModal();
		$('#modal1').openModal();
  }
  else{
    gettrainingdata(start_date, end_date, trainer_ids, question_ids);
    gettrainerdata(start_date, end_date, trainer_ids, question_ids);
    getquestiondata(start_date, end_date, trainer_ids, question_ids);
    //getmediatordata(start_date, end_date, trainer_ids, question_ids);
  }
}

/* Initializing filters */

function get_filter_data() {
  $.get( "/training/filter_data/", {})
       .done(function( data ) {
           data_json = JSON.parse(data);
           fill_trainer_filter(data_json.trainers);
           fill_question_filter(data_json.questions);
           get_data();
       });
}

function fill_trainer_filter(data_json) {
  $.each(data_json, function (index, data) {
    create_filter($('#trainers'), data.id, data.name , true);
  });
}

function fill_question_filter(data_json) {
  $.each(data_json, function (index, data) {
    create_filter($('#questions'), data.id, data.text, true);
  });
}

function create_filter(tbody_obj, id, name, checked) {
  var row = $('<tr>');
  var td_name = $('<td>').html(name);
  row.append(td_name);
  var checkbox_html = '<input type="checkbox" class="black" data=' + id + ' id="' + name + id + '" checked="checked" /><label for="' + name + id + '"></label>';
  var td_checkbox = $('<td>').html(checkbox_html);
  row.append(td_checkbox);
  tbody_obj.append(row);
}

/* ajax to get json */

function gettrainingdata(start_date, end_date, trainer_ids, question_ids) {
  show_progress_bar();
  $.get( "/training/training_wise_data/", {'start_date': start_date, 'end_date': end_date, 'trainer_ids[]': trainer_ids, 'question_ids[]': question_ids})
           .done(function( data ) {
               data_json = JSON.parse(data);
               hide_progress_bar();
               filltrainingtable(data_json);
           });  
}

function gettrainerdata(start_date, end_date, trainer_ids, question_ids) {
  show_progress_bar();
  $.get( "/training/trainer_wise_data/", {'start_date': start_date, 'end_date': end_date, 'trainer_ids[]': trainer_ids, 'question_ids[]': question_ids})
           .done(function( data ) {
               data_json = JSON.parse(data);
               hide_progress_bar();
               plot_trainerwise_data(data_json);
           });
}

function getquestiondata(start_date, end_date, trainer_ids, question_ids) {
  show_progress_bar();
  $.get( "/training/question_wise_data/", {'start_date': start_date, 'end_date': end_date, 'trainer_ids[]': trainer_ids, 'question_ids[]': question_ids})
           .done(function( data ) {
               data_json = JSON.parse(data);
               hide_progress_bar();
               plot_questionwise_data(data_json);
           });
}

function getmediatordata(start_date, end_date, trainer_ids, question_ids) {
  show_progress_bar();
  $.get( "/training/mediator_wise_data/", {'start_date': start_date, 'end_date': end_date, 'trainer_ids[]': trainer_ids, 'question_ids[]': question_ids})
           .done(function( data ) {
               data_json = JSON.parse(data);
               hide_progress_bar();
               plot_mediatorwise_data(data_json);
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
  var x_axis = [];
  trainer_scores_dict = [];
  var total_score_dict = {};
  var avg_score_dict = {};
  var perc_score_dict = {};
  total_score_dict['name'] = 'Total Scores';
  avg_score_dict['name'] = 'Scores per Participant';
  perc_score_dict['name'] = 'Percent Answered Correctly';
  total_score_dict['data'] = new Array(data_json.length).fill(0.0);
  avg_score_dict['data'] = new Array(data_json.length).fill(0.0);
  perc_score_dict['data'] = new Array(data_json.length).fill(0.0);
  for (i=0; i<data_json.length; i++) {
    x_axis.push(data_json[i]['training__trainer__name']);
    total_score_dict['data'][i] = data_json[i]['score__sum'];
    var avg = (data_json[i]['score__sum']/data_json[i]['participant__count']);
    var perc = (data_json[i]['score__sum']/data_json[i]['score__count'])*100;
    avg_score_dict['data'][i] = parseFloat(avg.toFixed(2));
    perc_score_dict['data'][i] = parseFloat(perc.toFixed(2));
  }    
  //question_scores_dict.push(total_score_dict);
  trainer_scores_dict.push(avg_score_dict);
  trainer_scores_dict.push(perc_score_dict);
  plot_multiline_chart($("#trainer_mediator_score"), x_axis, trainer_scores_dict, "Score", "%");
}

function plot_questionwise_data(data_json){
  var x_axis = [];
  question_scores_dict = [];
  var total_score_dict = {};
  var avg_score_dict = {};
  var perc_score_dict = {};
  total_score_dict['name'] = 'Total Scores';
  avg_score_dict['name'] = 'Percentage Scores per Participant';
  perc_score_dict['name'] = 'Percent Answered Correctly';
  total_score_dict['data'] = new Array(data_json.length).fill(0.0);
  avg_score_dict['data'] = new Array(data_json.length).fill(0.0);
  perc_score_dict['data'] = new Array(data_json.length).fill(0.0);
  for (i=0; i<data_json.length; i++) {
    x_axis.push(data_json[i]['question__text']);
    total_score_dict['data'][i] = data_json[i]['score__sum'];
    var avg = (data_json[i]['score__sum']/data_json[i]['participant__count'])*100;
    var perc = (data_json[i]['score__sum']/data_json[i]['score__count'])*100;
    avg_score_dict['data'][i] = parseFloat(avg.toFixed(2));
    perc_score_dict['data'][i] = parseFloat(perc.toFixed(2));
  }    
  //question_scores_dict.push(total_score_dict);
  question_scores_dict.push(avg_score_dict);
  question_scores_dict.push(perc_score_dict);
  plot_multiline_chart($("#question_mediator_score"), x_axis, question_scores_dict, "Score", "%");
}

function plot_mediatorwise_data(data_json) {
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

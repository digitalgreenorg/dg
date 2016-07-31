/* This file should contain all the JS for Training dashboard */
window.onload = initialize;

function initialize() {
    // initialize any library here

    // to initialize material select
    $('select').material_select();
    get_filter_data();
    set_eventlistener();
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

function set_eventlistener() {

    // to change the visibility of tables, charts on change in select
    $("#table_option").change(function() {
        update_tables();
    });

    $("#chart_option").change(function() {
        update_charts();
    });

    // //datepicker
    // $('.datepicker').pickadate({
    //     selectMonths: true, // Creates a dropdown to control month
    //     selectYears: 15, // Creates a dropdown of 15 years to control year
    //     format: 'yyyy-mm-dd'
    // });

    $('#from_date').pickadate({
        selectMonths: true,
        selectYears: 15,
        format: "yyyy-mm-dd",
        max: -1,
        onSet: function(element) {
            if (element.select) {
                this.close();
            }
        }
    });
    $('#to_date').pickadate({
        selectMonths: true,
        selectYears: 15,
        format: "yyyy-mm-dd",
        max: true,
        onSet: function(element) {
            if (element.select) {
                this.close();
            }
        }
    });

    var today = new Date();
    $("#to_date").val(today.getFullYear() + "-" + (today.getMonth() + 1) + "-" + today.getDate());
    $("#from_date").val(2015 + "-" + 01 + "-" + 01);

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
    // only one should be selected
    $('#assessments').on('change', function(e) {
        if (this.checked) {
            var assessment = $(this).children()[1].firstChild;
            assessments.checked = true;
        }
    });

    $('#trainer_all').on('change', function(e) {
        if (this.checked) {
            $('#trainers').children().each(function() {
                var trainers_all = $(this).children()[1].firstChild;
                trainers_all.checked = true;
            });
        } else {
            $('#trainers').children().each(function() {
                var trainers_all = $(this).children()[1].firstChild;
                trainers_all.checked = false;
            });
        }
    });

    $('#state_all').on('change', function(e) {
        if (this.checked) {
            $('#states').children().each(function() {
                var states_all = $(this).children()[1].firstChild;
                states_all.checked = true;
            });
        } else {
            $('#states').children().each(function() {
                var states_all = $(this).children()[1].firstChild;
                states_all.checked = false;
            });
        }
    });
}

/* to change the visibility of tables, charts on change in select */

// function update_charts() {
//     var opt = $('#assessment_option :selected').val();
//     if(opt == 1){
//       $("#pico_assessment").show();
//       $("#documentation_assessment").hide();
//     }
//     else{
//       $("#documentation_assessment").show();
//       $("#pico_assessment").hide();
//     }
// }

/* get data according to filters */

function get_data() {
    var start_date = $('#from_date').val();
    var end_date = $('#to_date').val();

    var assessment_ids = [];
    var trainer_ids = [];
    var state_ids = [];

    $('#assessments').children().each(function() {
        var assessment_div = $(this).children()[1].firstChild;
        if (assessment_div.checked)
            assessment_ids.push(assessment_div.getAttribute('data'));
    });

    $('#trainers').children().each(function() {
        var trainer_div = $(this).children()[1].firstChild;
        if (trainer_div.checked)
            trainer_ids.push(trainer_div.getAttribute('data'));
    });

    $('#states').children().each(function() {
        var state_div = $(this).children()[1].firstChild;
        if (state_div.checked)
            state_ids.push(state_div.getAttribute('data'));
    });

    if (Date.parse(start_date) > Date.parse(end_date)) {
        //$('.modal-trigger').leanModal();
        $('#modal1').openModal();
    } else {
        gettrainerdata(start_date, end_date, assessment_ids, trainer_ids, state_ids);
        getquestiondata(start_date, end_date, assessment_ids, trainer_ids, state_ids);
        getstatedata(start_date, end_date, assessment_ids, trainer_ids, state_ids);
    }
}

/* Initializing filters */

function get_filter_data() {
    $.get("/training/filter_data/", {})
        .done(function(data) {
            data_json = JSON.parse(data);
            fill_assessment_filter(data_json.assessments);
            fill_trainer_filter(data_json.trainers);
            fill_state_filter(data_json.states);
            fill_top_boxes(data_json.num_trainings, data_json.num_participants, data_json.num_pass, data_json.num_farmers);
            get_data();
        });
}

function fill_assessment_filter(data_json) {
    $.each(data_json, function(index, data) {
        create_filter($('#assessments'), data.id, data.name, true);
    });
}

function fill_trainer_filter(data_json) {
    $.each(data_json, function(index, data) {
        create_filter($('#trainers'), data.id, data.name, true);
    });
}

function fill_state_filter(data_json) {
    $.each(data_json, function(index, data) {
        create_filter($('#states'), data.id, data.state_name, true)
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

function gettrainerdata(start_date, end_date, assessment_ids, trainer_ids, state_ids) {
    show_progress_bar();
    $.get("/training/trainer_wise_data/", {
            'start_date': start_date,
            'end_date': end_date,
            'assessment_ids[]': assessment_ids,
            'trainer_ids[]': trainer_ids,
            'state_ids[]': state_ids
        })
        .done(function(data) {
            data_json = JSON.parse(data);
            hide_progress_bar();
            plot_trainerwise_data(data_json);
        });
}

function getquestiondata(start_date, end_date, assessment_ids, trainer_ids, state_ids) {
    show_progress_bar();
    $.get("/training/question_wise_data/", {
            'start_date': start_date,
            'end_date': end_date,
            'assessment_ids[]': assessment_ids,
            'trainer_ids[]': trainer_ids,
            'state_ids[]': state_ids
        })
        .done(function(data) {
            data_json = JSON.parse(data);
            hide_progress_bar();
            plot_questionwise_data(data_json, assessment_ids);
        });
}

function getstatedata(start_date, end_date, assessment_ids, trainer_ids, state_ids) {
    show_progress_bar();
    $.get("/training/state_wise_data/", {
            'start_date': start_date,
            'end_date': end_date,
            'assessment_ids[]': assessment_ids,
            'trainer_ids[]': trainer_ids,
            'state_ids[]': state_ids
        })
        .done(function(data) {
            data_json = JSON.parse(data);
            hide_progress_bar();
            plot_statewise_data(data_json);
        });
}

/* Table Generating UI Functions - Fill data in table */

function fill_top_boxes(num_trainings, num_participants, num_pass) {
    var num_passed = 0;
    var num_failed = 0;
    var total_score = 0;
    for (i = 0; i < num_pass.length; i++) {
        total_score = total_score + num_pass[i]['score__sum'];
        if (num_pass[i]['score__count'] != 0) {
            if (num_pass[i]['score__sum'] / num_pass[i]['score__count'] >= 0.7) {
                num_passed += 1;
            } else {
                num_failed += 1;
            }
        }
    }
    var num_pass_percent = num_passed / (num_passed + num_failed) * 100;
    var avg_score = total_score / num_pass.length;

    document.getElementById('num_trainings').innerHTML = num_trainings;
    document.getElementById("mediators_trained").innerHTML = num_participants;
    document.getElementById("average_score").innerHTML = parseFloat(avg_score.toFixed(2));
    document.getElementById("pass_percent").innerHTML = parseFloat(num_pass_percent.toFixed(2));
}

/* Fill data for highcharts */

function plot_trainerwise_data(data_json) {
    var x_axis = [];
    var trainer_scores_dict = [];
    var trainer_trainings_mediators_dict = [];

    var avg_score_dict = {};
    var perc_score_dict = {};
    var trainer_trainings_dict = {};
    var trainer_mediators_dict = {};

    avg_score_dict['name'] = 'Average Scores per Participant';
    perc_score_dict['name'] = 'Percent Answered Correctly';
    trainer_trainings_dict['name'] = 'Total Trainings';
    trainer_mediators_dict['name'] = 'Mediators Trained';

    avg_score_dict['type'] = 'column';
    perc_score_dict['type'] = 'spline';
    trainer_trainings_dict['type'] = 'column';
    trainer_mediators_dict['type'] = 'column';

    perc_score_dict['yAxis'] = 1;
    trainer_trainings_dict['yAxis'] = 1;

    avg_score_dict['data'] = new Array(data_json.length).fill(0.0);
    perc_score_dict['data'] = new Array(data_json.length).fill(0.0);
    trainer_trainings_dict['data'] = new Array(data_json.length).fill(0.0);
    trainer_mediators_dict['data'] = new Array(data_json.length).fill(0.0);

    for (i = 0; i < data_json.length; i++) {
        x_axis.push(data_json[i]['training__trainer__name']);

        var avg = (data_json[i]['score__sum'] / data_json[i]['participant__count']);
        var perc = (data_json[i]['score__sum'] / data_json[i]['score__count']) * 100;

        avg_score_dict['data'][i] = parseFloat(avg.toFixed(2));
        perc_score_dict['data'][i] = parseFloat(perc.toFixed(2));
        trainer_trainings_dict['data'][i] = data_json[i]['training__id__count'];
        trainer_mediators_dict['data'][i] = data_json[i]['participant__count'];

        //TODO: 70% above is not feasible. Per Trainer, per mediator, score summary required for this. -> Precalulation tables need to be created for better execution.
        //TODO: Avg score per participant per trainer instead of how it is now
        //TODO: Make second graph line and stacked as per data instead of current graph
    }

    trainer_scores_dict.push(perc_score_dict);
    trainer_scores_dict.push(avg_score_dict);
    trainer_trainings_mediators_dict.push(trainer_trainings_dict);
    trainer_trainings_mediators_dict.push(trainer_mediators_dict);

    plot_dual_axis_chart($("#trainer_mediator_data"), x_axis, trainer_scores_dict, "Average Scores per Participant", "Percent Answered Correctly", "", "%");
    plot_dual_axis_chart($("#trainer_training_data"), x_axis, trainer_trainings_mediators_dict, "Mediators Trained", "Total Trainings", "", "");
}

function plot_questionwise_data(data_json, assessment_ids) {
    var x_axis = [];
    var question_dict = [];

    if (assessment_ids[0] == 1) {
        var question_mediators_dict = {};
        var question_mediators_passed_dict = {};
        var question_percent_dict = {};

        question_mediators_dict['name'] = 'Total Mediators';
        question_mediators_passed_dict['name'] = "Mediators Answered Correctly"
        question_percent_dict['name'] = 'Percentage Answered Correctly';

        question_mediators_dict['type'] = 'column';
        question_mediators_passed_dict['type'] = 'column';
        question_percent_dict['type'] = 'spline';

        question_percent_dict['yAxis'] = 1;

        // question_mediators_dict['stacking'] = 'normal'
        // question_mediators_passed_dict['stacking'] = 'normal'

        question_mediators_dict['data'] = new Array(data_json.length / 2).fill(0.0);
        question_mediators_passed_dict['data'] = new Array(data_json.length / 2).fill(0.0);
        question_percent_dict['data'] = new Array(data_json.length / 2).fill(0.0);

        for (i = 0; i < data_json.length / 2; i++) {
            if (data_json[i]['question__language__id'] == 2) {
                x_axis.push(data_json[i]['question__text']);
                var total_score = data_json[i]['score__sum'] + data_json[i + 15]['score__sum'];
                var total_count = data_json[i]['score__count'] + data_json[i + 15]['score__count'];
                var perc = total_score / total_count * 100;
                question_percent_dict['data'][i] = parseFloat(perc.toFixed(2));
                question_mediators_dict['data'][i] = data_json[i]['participant__count'] + data_json[i + 15]['participant__count'];
                var eng_pass = data_json[i]['participant__count'] * data_json[i]['score__sum'] / data_json[i]['score__count'];
                var hin_pass = data_json[i + 15]['participant__count'] * data_json[i + 15]['score__sum'] / data_json[i + 15]['score__count'];
                question_mediators_passed_dict['data'][i] = parseInt(eng_pass + hin_pass);

            }
        }

        question_dict.push(question_mediators_dict);
        question_dict.push(question_mediators_passed_dict);
        question_dict.push(question_percent_dict);
    
    } else {
    // Documentation Module 
    }

    plot_dual_axis_chart($("#question_mediator_data"), x_axis, question_dict, "Mediators Answered Correctly", "Percentage Answered Correctly", "", "%");
}

function plot_statewise_data(data_json) {

    //TODO: 70% above is not feasible. Per Trainer, per mediator, score summary required for this. -> Precalulation tables need to be created for better execution.
    //TODO: Avg score per participant per trainer instead of how it is now
    //TODO: Make second graph line and stacked 3 axis as per data instead of current graph

    var x_axis = [];
    var state_scores_dict = [];
    var state_trainings_mediators_dict = [];

    var avg_score_dict = {};
    var perc_score_dict = {};
    var state_trainings_dict = {};
    var state_mediators_dict = {};

    avg_score_dict['name'] = 'Average Scores per Mediator';
    perc_score_dict['name'] = 'Percent Answered Correctly';
    state_trainings_dict['name'] = 'Total Trainings';
    state_mediators_dict['name'] = 'Mediators Trained';

    avg_score_dict['type'] = 'column';
    perc_score_dict['type'] = 'spline';
    state_trainings_dict['type'] = 'column';
    state_mediators_dict['type'] = 'column';

    perc_score_dict['yAxis'] = 1;
    state_trainings_dict['yAxis'] = 1;

    avg_score_dict['data'] = new Array(data_json.length).fill(0.0);
    perc_score_dict['data'] = new Array(data_json.length).fill(0.0);
    state_trainings_dict['data'] = new Array(data_json.length).fill(0.0);
    state_mediators_dict['data'] = new Array(data_json.length).fill(0.0);

    for (i = 0; i < data_json.length; i++) {
        x_axis.push(data_json[i]['participant__district__state__state_name']);

        var avg = (data_json[i]['score__sum'] / data_json[i]['participant__count']);
        var perc = (data_json[i]['score__sum'] / data_json[i]['score__count']) * 100;

        avg_score_dict['data'][i] = parseFloat(avg.toFixed(2));
        perc_score_dict['data'][i] = parseFloat(perc.toFixed(2));
        state_trainings_dict['data'][i] = data_json[i]['training__id__count'];
        state_mediators_dict['data'][i] = data_json[i]['participant__count'];

        //TODO: 70% above is not feasible. Per Trainer, per mediator, score summary required for this. -> Precalulation tables need to be created for better execution.
        //TODO: Avg score per participant per trainer instead of how it is nows
        //TODO: Make second graph line and stacked as per data instead of current graph
    }

    state_scores_dict.push(perc_score_dict);
    state_scores_dict.push(avg_score_dict);
    state_trainings_mediators_dict.push(state_trainings_dict);
    state_trainings_mediators_dict.push(state_mediators_dict);

    plot_dual_axis_chart($("#state_mediator_data"), x_axis, state_scores_dict, "Average Scores per Mediator", "Percent Answered Correctly", "", "%");
    plot_dual_axis_chart($("#state_training_data"), x_axis, state_trainings_mediators_dict, "Mediators Trained", "Total Trainings", "", "");
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
        pie: {
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

    series = [{
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
                format: '<b>' + ((prefix_or_suffix) ? unit + ' ' : '') + '{total:.0f}' + ((prefix_or_suffix) ? '' : ' ' + unit) + '</b>',
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

function plot_single_axis_chart(container_obj, x_axis, data_dict, y_axis_text, unit) {
    container_obj.highcharts({
        chart: {
            zoomType: 'xy'
        },
        title: '',
        xAxis: [{
            categories: x_axis,
            crosshair: true
        }],
        yAxis: [{ // Primary yAxis
            labels: {
                format: '{value} ' + unit,
                style: {
                    color: Highcharts.getOptions().colors[0]
                }
            },
            title: {
                text: y_axis_text,
                style: {
                    color: Highcharts.getOptions().colors[0]
                }
            }
        }],
        tooltip: {
            shared: true
        },
        legend: {
            layout: 'vertical',
            align: 'left',
            x: 120,
            verticalAlign: 'top',
            y: 100,
            floating: true,
            backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'
        },
        series: data_dict
    });
}

function plot_dual_axis_chart(container_obj, x_axis, data_dict, y_axis_1_text, y_axis_2_text, unit_1, unit_2) {
    container_obj.highcharts({
        chart: {
            zoomType: 'xy'
        },
        title: '',
        xAxis: [{
            categories: x_axis,
            crosshair: true
        }],
        yAxis: [{ // Primary yAxis
            labels: {
                format: '{value} ' + unit_1,
                style: {
                    color: Highcharts.getOptions().colors[1]
                }
            },
            title: {
                text: y_axis_1_text,
                style: {
                    color: Highcharts.getOptions().colors[1]
                }
            }
        }, { // Secondary yAxis
            title: {
                text: y_axis_2_text,
                style: {
                    color: Highcharts.getOptions().colors[0]
                }
            },
            labels: {
                format: '{value} ' + unit_2,
                style: {
                    color: Highcharts.getOptions().colors[0]
                }
            },
            opposite: true
        }],
        tooltip: {
            shared: true
        },
        legend: {
            layout: 'vertical',
            align: 'left',
            x: 120,
            verticalAlign: 'top',
            y: 100,
            floating: true,
            backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'
        },
        series: data_dict
    });
}

function plot_multiple_axis_chart(container_obj, x_axis, data_dict, y_axis_1_text, y_axis_2_text, y_axis_3_text, unit_1, unit_2, unit_3) {
    container_obj.highcharts({
        chart: {
            zoomType: 'xy'
        },
        title: '',
        xAxis: [{
            categories: x_axis,
            crosshair: true
        }],
        yAxis: [{ // Primary yAxis
            labels: {
                format: '{value} ' + unit_1,
                style: {
                    color: Highcharts.getOptions().colors[1]
                }
            },
            title: {
                text: y_axis_1_text,
                style: {
                    color: Highcharts.getOptions().colors[1]
                }
            }
        }, { // Secondary yAxis
            title: {
                text: y_axis_2_text,
                style: {
                    color: Highcharts.getOptions().colors[0]
                }
            },
            labels: {
                format: '{value} ' + unit_2,
                style: {
                    color: Highcharts.getOptions().colors[0]
                }
            },
            opposite: true
        }, { // Secondary yAxis
            title: {
                text: y_axis_3_text,
                style: {
                    color: Highcharts.getOptions().colors[2]
                }
            },
            labels: {
                format: '{value} ' + unit_3,
                style: {
                    color: Highcharts.getOptions().colors[2]
                }
            },
            opposite: true
        }],
        tooltip: {
            shared: true
        },
        legend: {
            layout: 'vertical',
            align: 'left',
            x: 120,
            verticalAlign: 'top',
            y: 100,
            floating: true,
            backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'
        },
        series: data_dict
    });
}

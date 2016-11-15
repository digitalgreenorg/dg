/* This file should contain all the JS for Training dashboard */
window.onload = initialize;

function initialize() {
    // initialize any library here

    // to initialize material select
    $('select').material_select();
    get_filter_data();
    set_eventlistener();
    // update_charts();
    $(".button-collapse").sideNav({
          // Default is 240
          edge: 'left', // Choose the horizontal origin
          closeOnClick: true  // Closes side-nav on <a> clicks, useful for Angular/Meteor
        }
      );

}

$('#nav_menu').on('click', function() {
    reset_filter_form();
});

// Set Reflow the highcharts to make it responsive while resizing the windows.
$('#month_tab_link').on('click', function () {
    setTimeout(function () {
        $('#month_training_data').highcharts().reflow();
    }, 1);
});

$('#question_tab_link').on('click', function () {
    setTimeout(function () {
        $('#question_mediator_data').highcharts().reflow();
    }, 1);
});
$('#trainer_tab_link').on('click', function () {
    setTimeout(function () {
        $('#trainer_training_data').highcharts().reflow();
        $('#trainer_mediator_data').highcharts().reflow();
    }, 1);
});
$('#state_tab_link').on('click', function () {
    setTimeout(function () {
        $('#state_training_data').highcharts().reflow();
        $('#state_mediator_data').highcharts().reflow();
    }, 1);
});

//Search Trainers in SideNav

$("#search_trainers").keyup(function() {

    var index_map = {};

    //$("#trainer_all").prop("disabled",true);    
    var value = this.value.trim();
    if(value.length != 0)
        $("#trainer_all").prop("disabled",true);
    else
        $("#trainer_all").prop("disabled",false);

        $("#trainers_table").find("tr").each(function(index) {
            if (index === -1) return;

            trainer_name_array = $(this).text().toLowerCase().split(" ");
            var if_td_has = false; //boolean value to track if td had the entered key
            $(this).find('td').each(function () {
                for(var i = 0; i < trainer_name_array.length; i++){
                    if(trainer_name_array[i].indexOf(value.toLowerCase()) == 0) {
                            if_td_has = true; 
                            break;
                    }
                }//Check if td's text matches key and then use OR to check it for all td's
            });

            $(this).toggle(if_td_has);

        });
});


//Search States in Side Nav
$("#search_states").keyup(function() {
    var value = this.value;

    if(value.length != 0)
        $("#state_all").prop("disabled",true);
    else
        $("#state_all").prop("disabled",false);
        $("#states_table").find("tr").each(function(index) {
            if (index === -1) return;

            state_name_array = $(this).text().toLowerCase().split(" ");
            var if_td_has = false; //boolean value to track if td had the entered key
            $(this).find('td').each(function () {
                for(var i = 0; i < state_name_array.length; i++){
                    if(state_name_array[i].indexOf(value.toLowerCase()) == 0) {
                            if_td_has = true;
                            break;
                    }
                }//Check if td's text matches key and then use OR to check it for all td's
            });


            $(this).toggle(if_td_has);

        });
});


// reset
function reset_filter_form() {
    $('#search_trainers').val('');
    $('#search_trainers').keyup();
    $('#search_states').val('');
    $('#search_states').keyup();
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

    $('#from_date').pickadate({
        selectMonths: true,
        selectYears: 15,
        format: "yyyy-mm-dd",
        onClose: function() {
            $(document.activeElement).blur()
        },
        min: new Date(2015,0,1),
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
        onClose: function() {
            $(document.activeElement).blur()
        },
        min: new Date(2015,0,1),
        max: true,
        onSet: function(element) {
            if (element.select) {
                this.close();
            }
        }
    });

    var today = new Date();
    var month_ = (( (today.getMonth() + 1) > 9 ) ? (today.getMonth() + 1).toString(): "0" + (today.getMonth() + 1).toString());
    var date_ = (( (today.getDate() + 1) > 9 ) ? (today.getDate() + 1).toString(): "0" + (today.getDate() + 1).toString());
    $("#to_date").val(today.getFullYear() + "-" + month_ + "-" + date_);
    $("#from_date").val("2015-01-01");

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

/* get data according to filters */

function get_data() {
    var start_date = $('#from_date').val();
    var end_date = $('#to_date').val();
    if(start_date === '' || end_date === '')
    {
        $('#invalid_date_modal').openModal();
    }
    else
    {
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
            $('#invalid_date_modal').openModal();
        } else {
            gettrainerdata(start_date, end_date, assessment_ids, trainer_ids, state_ids);
            getquestiondata(start_date, end_date, assessment_ids, trainer_ids, state_ids);
            getstatedata(start_date, end_date, assessment_ids, trainer_ids, state_ids);
            getmonthdata(start_date,end_date,assessment_ids,trainer_ids,state_ids);
            get_bottom_boxes();
        }
    }
}

function get_bottom_boxes(){

    var start_date = $('#from_date').val();
    var end_date = $('#to_date').val();
    $.get("/training/date_filter_data/", {
        'start_date': start_date,
        'end_date': end_date
    })
    .done(function(data) {
        data_json = JSON.parse(data);
        fill_bottom_boxes(data_json.num_trainings, data_json.num_participants, data_json.num_pass, data_json.num_villages, data_json.num_beneficiaries);
    });
}


/* Initializing filters */

function get_filter_data() {
    $.get("/training/filter_data/", {})
        .done(function(data) {
            data_json = JSON.parse(data);
            fill_assessment_filter(data_json.assessments);
            fill_trainer_filter(data_json.trainers);
            fill_state_filter(data_json.states);
            fill_top_boxes(data_json.num_trainings, data_json.num_participants, data_json.num_pass, data_json.num_villages,data_json.num_beneficiaries);

            get_data();
        });
}

function fill_assessment_filter(data_json) {
    $.each(data_json, function(index, data) {
        create_filter($('#assessments'), data.id, data.name, 'radio');
    });

    $('#assessments tr:eq(0)').children()[1].firstChild.checked = true;
}

function fill_trainer_filter(data_json) {
    $.each(data_json, function(index, data) {
        create_filter($('#trainers'), data.id, data.name, 'checkbox');
    });
}

function fill_state_filter(data_json) {
    $.each(data_json, function(index, data) {
        create_filter($('#states'), data.id, data.state_name, 'checkbox')
    });
}

function create_filter(tbody_obj, id, name, type) {
    var row = $('<tr>');
    var td_name = $('<td>').html(name);
    row.append(td_name);
    if (type == 'checkbox') {
        var checkbox_html = '<input type="checkbox" class="black" data=' + id + ' id="' + name + id + '" checked="checked" /><label for="' + name + id + '"></label>';
    } else if (type == 'radio') {
        var checkbox_html = '<input type="radio" class="with-gap" name="assessment" data=' + id + ' id="' + name + id + '"/><label for="' + name + id + '"></label>';
    }
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
            plot_trainerwise_data(data_json.trainer_list, data_json.mediator_list, data_json.test);
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
            plot_statewise_data(data_json.state_list, data_json.mediator_list, data_json.state_test);
        });
}

function getmonthdata(start_date, end_date, assessment_ids, trainer_ids, state_ids) {
    show_progress_bar();
    $.get("/training/month_wise_data/", {
            'start_date': start_date,
            'end_date': end_date,
            'assessment_ids[]': assessment_ids,
            'trainer_ids[]': trainer_ids,
            'state_ids[]': state_ids
        })
        .done(function(data) {
            data_json = JSON.parse(data);
            hide_progress_bar();
            plot_monthwise_data(data_json.trainings, data_json.data_list);
        });
}



/* Table Generating UI Functions - Fill data in table */

function fill_top_boxes(num_trainings, num_participants, num_pass, num_villages, num_beneficiaries) {
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

    document.getElementById('num_trainings').innerHTML = numberWithCommas(num_trainings);
    document.getElementById('mediators_trained').innerHTML = numberWithCommas(num_participants);
    document.getElementById('average_score').innerHTML = parseFloat(avg_score.toFixed(2));
    document.getElementById('pass_percent').innerHTML = parseFloat(num_pass_percent.toFixed(2));
}

function fill_bottom_boxes(num_trainings, num_participants, num_pass, num_villages, num_beneficiaries) {
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

    if(isNaN(avg_score))
    {
        avg_score = 0;
    }

    if(isNaN(num_pass_percent))
    {
        num_pass_percent = 0;
    }

    document.getElementById('filtered_num_trainings').innerHTML = numberWithCommas(num_trainings);
    document.getElementById('filtered_mediators_trained').innerHTML = numberWithCommas(num_participants);
    document.getElementById('filtered_average_score').innerHTML = parseFloat(avg_score.toFixed(2));
    document.getElementById('filtered_pass_percent').innerHTML = parseFloat(num_pass_percent.toFixed(2));
}

function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

/* Fill data for highcharts */

function plot_trainerwise_data(trainer_list, mediator_list, test) {

    if (trainer_list.length == 0) {

        plot_dual_axis_chart($("#trainer_mediator_data"), [], {}, "Average Scores per Participant", "", "", "%","");
        plot_multiple_axis_chart($("#trainer_training_data"), [], {}, "Mediators Trained", "", "", "", "", "%", {}, "", "","No data for this assessment");
    } else {
        var x_axis = [];
        var trainer_scores_dict = [];
        var trainer_trainings_mediators_dict = [];
      
        var avg_score_dict = {};
        var perc_score_dict = {};
        var trainer_trainings_dict = {};
        var trainer_mediators_dict = {};
        var trainer_mediators_pass_dict = {};
        var trainer_pass_perc_dict = {};

        avg_score_dict['name'] = 'Average Scores per Participant (out of 15)';
        perc_score_dict['name'] = 'Percent Answered Correctly';
        trainer_trainings_dict['name'] = 'Total Trainings';
        trainer_mediators_dict['name'] = 'Mediators Trained';
        trainer_mediators_pass_dict['name'] = 'Mediator scores above 70%';

        trainer_mediators_dict['pointPadding'] = -0.2;
        trainer_mediators_dict['pointPlacement'] = 0.125;

        trainer_mediators_pass_dict['pointPadding'] = 0.2;
        trainer_mediators_pass_dict['pointPlacement'] = -0.168;

        trainer_mediators_dict['color'] = 'rgba(248,161,63,1)';
        trainer_trainings_dict['color'] = '#000000';
        trainer_mediators_pass_dict['color'] = 'rgba(186,60,61,.9)';

        avg_score_dict['type'] = 'column';
        perc_score_dict['type'] = 'spline';
        trainer_trainings_dict['type'] = 'spline';
        trainer_mediators_dict['type'] = 'column';
        trainer_mediators_pass_dict['type'] = 'column';

        perc_score_dict['yAxis'] = 1;
        trainer_mediators_dict['yAxis'] = 0;
         
        avg_score_dict['data'] = new Array(trainer_list.length).fill(0.0);
        perc_score_dict['data'] = new Array(trainer_list.length).fill(0.0);
        trainer_trainings_dict['data'] = new Array(trainer_list.length).fill(0.0);
        trainer_mediators_dict['data'] = new Array(trainer_list.length).fill(0.0);
        trainer_mediators_pass_dict['data'] = new Array(trainer_list.length).fill(0.0);
        trainer_pass_perc_dict['data'] = new Array(trainer_list.length).fill(0.0);
        for (i = 0; i < trainer_list.length; i++) {
            var trainer_name = trainer_list[i]['training__trainer__name'];
            x_axis.push(trainer_name);
            var avg = (test[i][trainer_name]['score_sum'] / test[i][trainer_name]['participant_count']);
            var perc = (trainer_list[i]['score__sum'] / trainer_list[i]['score__count']) * 100;

            avg_score_dict['data'][i] = parseFloat(avg.toFixed(2));
            perc_score_dict['data'][i] = parseFloat(perc.toFixed(2));
            trainer_trainings_dict['data'][i] = trainer_list[i]['training__id__count'];
            trainer_mediators_dict['data'][i] = trainer_list[i]['participant__count'];
            trainer_mediators_pass_dict['data'][i] = 0;

            for (j = 0; j < mediator_list.length; j++) {
                if (trainer_list[i]['training__trainer__name'] == mediator_list[j]['training__trainer__name']) {
                    if (mediator_list[j]['score__sum']/mediator_list[j]['score__count'] >= 0.7) {
                        trainer_mediators_pass_dict['data'][i] += 1;
                    }
                }
            }

            var pass_perc = trainer_mediators_pass_dict['data'][i]/trainer_mediators_dict['data'][i]*100; //todo
            trainer_pass_perc_dict['data'][i] = parseFloat(perc.toFixed(2));
        }

        trainer_scores_dict.push(avg_score_dict);
        
        trainer_trainings_mediators_dict.push(trainer_mediators_dict);
        trainer_trainings_mediators_dict.push(trainer_mediators_pass_dict);

        plot_dual_axis_chart($("#trainer_mediator_data"), x_axis, trainer_scores_dict, "Average Scores per Participant", "", "", "%","");
        plot_multiple_axis_chart($("#trainer_training_data"), x_axis, trainer_trainings_mediators_dict, "Mediators Trained", "", "", "", "", "%", trainer_trainings_dict, "", "Labels represent : Total Trainings","");
    }
}

function plot_questionwise_data(data_json, assessment_ids) {
    question_data_length = data_json.length;
    //Question Array length to store Distinct question : whether it is available in different languages.
    question_array_length = 0;
    // offset represent for same Questions in different Languages : 15, if data available in both english and hindi.
    question_offset = 0;
    if (question_data_length == 0) {
        plot_multiple_axis_chart($("#question_mediator_data"), [], {}, "No. of Mediators", "", "","","", "%", {}, "%", "","No data for this assessment");
    } else {
        var x_axis = [];
        var question_dict = [];
        var question_mediators_dict = {};
        var question_mediators_passed_dict = {};
        var question_percent_dict = {};

        question_mediators_dict['pointPadding'] = -0.2;
        question_mediators_dict['pointPlacement'] = 0.125;

        question_mediators_passed_dict['pointPadding'] = 0.2;
        question_mediators_passed_dict['pointPlacement'] = -0.168;

        question_mediators_dict['color'] = 'rgba(248,161,63,1)';
        question_percent_dict['color'] = '#000000';
        question_mediators_passed_dict['color'] = 'rgba(186,60,61,.9)';

        // For Peeco Seekho, Assessment Id = 1
        if (assessment_ids[0] == 1) {

            // For Peeco Seekho, total distinct questions = 15

            question_array_length = 15;
            language_count = question_data_length / question_array_length;
            if(language_count == 2) {
                question_offset = 15;
            }
            question_mediators_dict['name'] = 'Total Mediators';
            question_mediators_passed_dict['name'] = "Mediators Answered Correctly"
            question_percent_dict['name'] = 'Percentage Answered Correctly';

            question_mediators_dict['type'] = 'column';
            question_mediators_passed_dict['type'] = 'column';
            question_percent_dict['type'] = 'spline';

            question_mediators_passed_dict['yAxis'] = 0;

            question_mediators_dict['data'] = new Array(question_array_length).fill(0.0);
            question_mediators_passed_dict['data'] = new Array(question_array_length).fill(0.0);
            question_percent_dict['data'] = new Array(question_array_length).fill(0.0);

            for (i = 0; i < question_array_length; i++) {
                if (data_json[i]['question__language__id'] == 2) {
                    x_axis.push(data_json[i]['question__text']);
                    var total_score = data_json[i]['score__sum'] + (question_offset == 0 ? 0 : data_json[i + question_offset]['score__sum']);
                    var total_count = data_json[i]['score__count'] + (question_offset == 0 ? 0 : data_json[i + question_offset]['score__count']);
                    var perc = total_score / total_count * 100;
                    question_percent_dict['data'][i] = parseFloat(perc.toFixed(2));
                    question_mediators_dict['data'][i] = data_json[i]['participant__count'] + (question_offset == 0 ? 0 : data_json[i + question_offset]['participant__count']);
                    var eng_pass = data_json[i]['participant__count'] * data_json[i]['score__sum'] / data_json[i]['score__count'];
                    var hin_pass = (question_offset == 0 ? 0 : data_json[i + question_offset]['participant__count'] * data_json[i + question_offset]['score__sum'] / data_json[i + question_offset]['score__count']);
                    question_mediators_passed_dict['data'][i] = parseInt(eng_pass + hin_pass);
                }
            }
            question_dict.push(question_mediators_passed_dict);

        } else {
            console.log("length2 = " + data_json.length);
            question_mediators_dict['name'] = 'Total Mediators';
            question_mediators_passed_dict['name'] = "Mediators Answered Correctly"
            question_percent_dict['name'] = 'Percentage Answered Correctly';

            question_mediators_dict['type'] = 'column';
            question_mediators_passed_dict['type'] = 'column';
            question_percent_dict['type'] = 'spline';

            question_mediators_passed_dict['yAxis'] = 0;
            question_mediators_dict['data'] = new Array(data_json.length).fill(0.0);
            question_mediators_passed_dict['data'] = new Array(data_json.length).fill(0.0);
            question_percent_dict['data'] = new Array(data_json.length).fill(0.0);

            for (i = 0; i < data_json.length; i++) {
                x_axis.push(data_json[i]['question__text']);
                var total_score = data_json[i]['score__sum'];
                var total_count = data_json[i]['score__count'];
                var perc = total_score / total_count * 100;
                question_percent_dict['data'][i] = parseFloat(perc.toFixed(2));
                question_mediators_dict['data'][i] = data_json[i]['participant__count'];
                var med_pass = data_json[i]['participant__count'] * data_json[i]['score__sum'] / data_json[i]['score__count'];
                question_mediators_passed_dict['data'][i] = parseInt(med_pass);
            }

            question_dict.push(question_mediators_passed_dict);
        }

        plot_multiple_axis_chart($("#question_mediator_data"), x_axis, question_dict, "No. of Mediators", "", "","","", "%", question_percent_dict, "%", "Labels represent : % of mediators scoring above 70%","");

    }
}

function plot_statewise_data(state_list, mediator_list, state_test) {
    if (state_list.length == 0) {
        plot_dual_axis_chart($("#state_mediator_data"), [], {}, "Average Scores per Mediator", "", "", "%","");
        plot_multiple_axis_chart($("#state_training_data"), [], {}, "No. of Mediators", "", "", "", "", "%", {}, "", "","No data for this assessment");
    }
    else {
        var x_axis = [];
        var state_scores_dict = [];
        var state_trainings_mediators_dict = [];

        var avg_score_dict = {};
        var perc_score_dict = {};
        var state_trainings_dict = {};
        var state_mediators_dict = {};
        var state_mediators_pass_dict = {};
        var state_pass_perc_dict = {};

        avg_score_dict['name'] = 'Average Scores per Mediator  (out of 15)';
        perc_score_dict['name'] = 'Percent Answered Correctly';
        state_trainings_dict['name'] = 'Total Trainings';
        state_mediators_dict['name'] = 'Mediators Trained';
        state_mediators_pass_dict['name'] = 'Mediator scores above 70%';
        state_pass_perc_dict['name'] = 'Percentage scores above 70%';

        avg_score_dict['type'] = 'column';
        perc_score_dict['type'] = 'spline';
        state_trainings_dict['type'] = 'column';
        state_mediators_dict['type'] = 'column';
        state_mediators_pass_dict['type'] = 'column';
        state_pass_perc_dict['type'] = 'spline';


        state_mediators_dict['pointPadding'] = -0.2;
        state_mediators_dict['pointPlacement'] = 0.125;

        state_mediators_pass_dict['pointPadding'] = 0.2;
        state_mediators_pass_dict['pointPlacement'] = -0.168;

        state_mediators_dict['color'] = 'rgba(248,161,63,1)';
        state_trainings_dict['color'] = '#000000';
        state_mediators_pass_dict['color'] = 'rgba(186,60,61,.9)';

        state_mediators_dict['yAxis'] = 0;

        avg_score_dict['data'] = new Array(state_list.length).fill(0.0);
        perc_score_dict['data'] = new Array(state_list.length).fill(0.0);
        state_trainings_dict['data'] = new Array(state_list.length).fill(0.0);
        state_mediators_dict['data'] = new Array(state_list.length).fill(0.0);
        state_mediators_pass_dict['data'] = new Array(state_list.length).fill(0.0);
        state_pass_perc_dict['data'] = new Array(state_list.length).fill(0.0);

        for (i = 0; i < state_list.length; i++) {
            state_name = state_list[i]['participant__district__state__state_name']; 
            x_axis.push(state_name);

            var avg = (state_test[i][state_name]['score_sum'] / state_test[i][state_name]['participant_count']);
            var perc = (state_list[i]['score__sum'] / state_list[i]['score__count']) * 100;

            avg_score_dict['data'][i] = parseFloat(avg.toFixed(2));
            perc_score_dict['data'][i] = parseFloat(perc.toFixed(2));
            state_trainings_dict['data'][i] = state_list[i]['training__id__count'];
            state_mediators_dict['data'][i] = state_list[i]['participant__count'];
            state_mediators_pass_dict['data'][i] = 0;

            for (j = 0; j < mediator_list.length; j++) {
                if (state_list[i]['participant__district__state__state_name'] == mediator_list[j]['participant__district__state__state_name']) {
                    if (mediator_list[j]['score__sum']/mediator_list[j]['score__count'] >= 0.7) {
                        state_mediators_pass_dict['data'][i] += 1;
                    }
                }
            }

            var pass_perc = state_mediators_pass_dict['data'][i]/state_mediators_dict['data'][i]*100;
            state_pass_perc_dict['data'][i] = parseFloat(perc.toFixed(2));
        }

        state_scores_dict.push(avg_score_dict);
        state_trainings_mediators_dict.push(state_mediators_dict);
        state_trainings_mediators_dict.push(state_mediators_pass_dict);

        plot_dual_axis_chart($("#state_mediator_data"), x_axis, state_scores_dict, "Average Scores per Mediator", "", "", "%","");
        plot_multiple_axis_chart($("#state_training_data"), x_axis, state_trainings_mediators_dict, "No. of Mediators", "", "", "", "", "%", state_trainings_dict, "", "Labels represent : No. of total trainings","");
    }
}

function plot_monthwise_data(series_name, series_data_list) {

        $('#month_training_data').highcharts({
        chart: {
            type: 'column'
        },
        credits:{enabled :false},
        title: {
            text: 'No. Of Trainings Per Month'
        },
        xAxis: {
            categories: [
                'Jan',
                'Feb',
                'Mar',
                'Apr',
                'May',
                'Jun',
                'Jul',
                'Aug',
                'Sep',
                'Oct',
                'Nov',
                'Dec'
            ],
            crosshair: true
        },
        yAxis: {
            min: 0,
            title: {
                text: 'No. of trainings'
            }
        },
        tooltip: {
            shared: true,
        },

        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0,
                dataLabels: {
                enabled: true,
                format:'{point.y}'
            }
            }
        },
        series: [{
            name: series_name,
            data: series_data_list
       
            }]
    });
}

/* plot highcharts data */

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
            align: 'center',
            verticalAlign: 'top',
            layout: 'horizontal',
            x: 0,
            y: 0,
            backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'
        },
        series: data_dict
    });
}

function plot_dual_axis_chart(container_obj, x_axis, data_dict, y_axis_1_text, y_axis_2_text, unit_1, unit_2, title_) {

    var width_ = $('.container').width();
    var dataLabels = {
        enabled:true,
        formatter:function (){return this.y;}
    };

    var len = Object.keys(data_dict).length
    if(len != 0)
        data_dict[0]['dataLabels'] = dataLabels;

    container_obj.highcharts({
        chart: {
            zoomType: '',
            /*width:width_*/
        },

        credits:{enabled : false},
        title:{text: title_},
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

            align: 'center',
            layout: 'horizontal',
        
            x: 0,
            y: 0,
            backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'
        },
        series: data_dict
    });
}
function plot_multiple_axis_chart(container_obj, x_axis, data_dict, y_axis_1_text, y_axis_2_text, y_axis_3_text, unit_1, unit_2, unit_3, datalablels_dict, label_type, custom_subtitle, title_) {

    var i = 0;
    var len = Object.keys(datalablels_dict).length
    var width_ = $('.container').width();
    if(len > 0) {
        len =Object.keys(datalablels_dict['data']).length;
        var dataLabels = {
            enabled :true,
            formatter: function() {
                if(i >= len) {
                    i = 0;
                }
                while(i < len){
                    i++;
                    return (datalablels_dict['data'][i-1] + label_type);
                }
            },
            allowOverlap : true
        }; 
        data_dict[0]['dataLabels'] = dataLabels;  
    }
    

    
    container_obj.highcharts({
        chart: {
            zoomType: '',
            spacingRight : 30,
            /*width: width_*/
        },
        credits:{enabled :false},
        title:{ text: title_
        },
        subtitle: {
            text: custom_subtitle
        },
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
          align: 'center',
          layout: 'horizontal',

          x: 0,
          y: 0,
            backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'
        },
        series:  data_dict
    });

}

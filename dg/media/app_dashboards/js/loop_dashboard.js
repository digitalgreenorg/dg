/* This file should contain all the JS for Loop dashboard */
window.onload = initialize;

function initialize() {
    // initialize any library here
    $('select').material_select();
    set_eventlistener();
    $(".button-collapse").sideNav()
    // to initialize material select
    if (document.title == "Home") {
        set_date_pickers();
        total_static_data();
        // recent_graphs_data();
        get_data_main();
        days_to_average = 30;
        days_to_go_back = 5;
        counter_volume = 0;
    } else if (document.title == "Second Page") {
        ;
        
        get_filter_data();
        update_tables();
        update_charts();


    }

}

function set_date_pickers() {
    $('#start_date_main').pickadate({
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
    $('#end_date_main').pickadate({
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

    $('#get_data_main').click(function() {
        get_data_main();
    });
}

function get_data_main() {
    start_date_main = $('#start_date_main').val();
    end_date_main = $('#end_date_main').val();
    if (Date.parse(start_date_main) > Date.parse(end_date_main)) {
        //$('.modal-trigger').leanModal();
        $('#modal1').openModal();
    } else {
        recent_graphs_data();
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
function set_eventlistener() {

    // to change the visibility of tables , charts on change in select
    $("#table_option").change(function() {
        update_tables();
    });

    $("#chart_option").change(function() {
        update_charts();
    });

    $("#mFrequency").change(function(){
        days_to_average = $('#mFrequency :selected').val()
        plot_cards_data();
    });


    //datepicker
    $('.datepicker').pickadate({
        selectMonths: true, // Creates a dropdown to control month
        selectYears: 15, // Creates a dropdown of 15 years to control year
        format: 'yyyy-mm-dd'
    });

    set_filterlistener();

    //get data button click
    $('#get_data').click(function() {
        get_data();
    });

    // apply filter button click
    $('#apply_filter').click(function() {
        get_data();
    });

    $('#v_a').change(function() {
        update_graphs_aggregator_wise();
    });
}

/* event listeners for filters */

function set_filterlistener() {
    $('#aggregator_all').on('change', function(e) {
        if (this.checked) {
            $('#aggregators').children().each(function() {
                var aggregators_all = $(this).children()[1].firstChild;
                aggregators_all.checked = true;
            });
        } else {
            $('#aggregators').children().each(function() {
                var aggregators_all = $(this).children()[1].firstChild;
                aggregators_all.checked = false;
            });
        }
    });

    $('#village_all').on('change', function(e) {
        if (this.checked) {
            $('#villages').children().each(function() {
                var villages_all = $(this).children()[1].firstChild;
                villages_all.checked = true;
            });
        } else {
            $('#villages').children().each(function() {
                var villages_all = $(this).children()[1].firstChild;
                villages_all.checked = false;
            });
        }
    });

    $('#crop_all').on('change', function(e) {
        if (this.checked) {
            $('#crops').children().each(function() {
                var crops_all = $(this).children()[1].firstChild;
                crops_all.checked = true;
            });
        } else {
            $('#crops').children().each(function() {
                var crops_all = $(this).children()[1].firstChild;
                crops_all.checked = false;
            });
        }
    });

    $('#mandi_all').on('change', function(e) {
        if (this.checked) {
            $('#mandis').children().each(function() {
                var mandis_all = $(this).children()[1].firstChild;
                mandis_all.checked = true;
            });
        } else {
            $('#mandis').children().each(function() {
                var mandis_all = $(this).children()[1].firstChild;
                mandis_all.checked = false;
            });
        }
    });
    $('#gaddidar_all').on('change', function(e) {
        if (this.checked) {
            $('#gaddidars').children().each(function() {
                var gaddidar_all = $(this).children()[1].firstChild;
                gaddidar_all.checked = true;
            });
        } else {
            $('#gaddidars').children().each(function() {
                var gaddidar_all = $(this).children()[1].firstChild;
                gaddidar_all.checked = false;
            });
        }
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
    if (opt == 1) {
        $("#village_table").show();
        $("#aggregator_table").hide();
    } else {
        $("#aggregator_table").show();
        $("#village_table").hide();
    }
}

function update_charts() {
    var opt = $('#chart_option :selected').val();
    if (opt == 1) {
        $("#crop_chart_div").show();
        $("#agg_crop_chart_div").hide();
    } else {
        $("#agg_crop_chart_div").show();
        $("#crop_chart_div").hide();
    }
}

function update_graphs_aggregator_wise() {

    var option = $('#v_a :selected').val();
    if (option == 1) {
        var parameter = "quantity__sum";

    } else if (option == 2) {
        var parameter = "amount__sum";
    }
    aggregator_graph($('#aggregator_mandi'), mandi_ids, mandi_names, 'mandi__id', aggregator_ids, aggregator_names, 'user_created__id', aggregator_graphs_json_data.aggregator_mandi, parameter);
    aggregator_graph($('#aggregator_gaddidar'), gaddidar_ids, gaddidar_names, 'gaddidar__id', aggregator_ids, aggregator_names, 'user_created__id', aggregator_graphs_json_data.aggregator_gaddidar, parameter);
    aggregator_graph($('#aggregator_crop'), crop_ids, crop_names, 'crop__id', aggregator_ids, aggregator_names, 'user_created__id', aggregator_graphs_json_data.aggregator_crop, parameter);
    transport_cost_graph($('#mandi_cost'), mandi_ids, mandi_names, 'mandi__id', aggregator_ids, aggregator_names, 'user_created__id', aggregator_graphs_json_data.transportation_cost_mandi);
    cpk_spk_graph(mandi_ids, mandi_names, 'mandi__id', aggregator_ids, aggregator_names, 'user_created__id', aggregator_graphs_json_data);

}

function update_graphs_mandi_wise() {

    var option = $('#v_a :selected').val();
    if (option == 1) {
        aggregator_graph($('#aggregator_mandi'), aggregator_ids, aggregator_names, 'user_created__id', mandi_ids, mandi_names, 'mandi__id', aggregator_graphs_json_data.aggregator_mandi, "quantity__sum");
        aggregator_graph($('#aggregator_gaddidar'), gaddidar_ids, gaddidar_names, 'gaddidar__id', mandi_ids, mandi_names, 'mandi__id', aggregator_graphs_json_data.mandi_gaddidar, "quantity__sum");
        aggregator_graph($('#aggregator_crop'), crop_ids, crop_names, 'crop__id', mandi_ids, mandi_names, 'mandi__id', aggregator_graphs_json_data.mandi_crop, "quantity__sum");
    } else if (option == 2) {
        aggregator_graph($('#aggregator_mandi'), aggregator_ids, aggregator_names, 'user_created__id', mandi_ids, mandi_names, 'mandi__id', aggregator_graphs_json_data.aggregator_mandi, "amount__sum");
        aggregator_graph($('#aggregator_gaddidar'), gaddidar_ids, gaddidar_names, 'gaddidar__id', mandi_ids, mandi_names, 'mandi__id', aggregator_graphs_json_data.mandi_gaddidar, "amount__sum");
        aggregator_graph($('#aggregator_crop'), crop_ids, crop_names, 'crop__id', mandi_ids, mandi_names, 'mandi__id', aggregator_graphs_json_data.mandi_crop, "amount__sum");
    }
    transport_cost_graph($('#mandi_cost'), aggregator_ids, aggregator_names, 'user_created__id', mandi_ids, mandi_names, 'mandi__id', aggregator_graphs_json_data.transportation_cost_mandi);
    cpk_spk_graph(aggregator_ids, aggregator_names, 'user_created__id', mandi_ids, mandi_names, 'mandi__id', aggregator_graphs_json_data);

}

function update_graphs_crop_wise() {

    var option = $('#v_a :selected').val();
    if (option == 1) {
        aggregator_graph($('#aggregator_mandi'), aggregator_ids, aggregator_names, 'user_created__id', crop_ids, crop_names, 'crop__id', aggregator_graphs_json_data.aggregator_crop, "quantity__sum");
        aggregator_graph($('#aggregator_gaddidar'), mandi_ids, mandi_names, 'mandi__id', crop_ids, crop_names, 'crop__id', aggregator_graphs_json_data.mandi_crop, "quantity__sum");
        aggregator_graph($('#aggregator_crop'), gaddidar_ids, gaddidar_names, 'gaddidar__id', crop_ids, crop_names, 'crop__id', aggregator_graphs_json_data.gaddidar_crop, "quantity__sum");
    } else if (option == 2) {
        aggregator_graph($('#aggregator_mandi'), aggregator_ids, aggregator_names, 'user_created__id', crop_ids, crop_names, 'crop__id', aggregator_graphs_json_data.aggregator_crop, "amount__sum");
        aggregator_graph($('#aggregator_gaddidar'), mandi_ids, mandi_names, 'mandi__id', crop_ids, crop_names, 'crop__id', aggregator_graphs_json_data.mandi_crop, "amount__sum");
        aggregator_graph($('#aggregator_crop'), gaddidar_ids, gaddidar_names, 'gaddidar__id', crop_ids, crop_names, 'crop__id', aggregator_graphs_json_data.gaddidar_crop, "amount__sum");
    }
    // transport_cost_graph($('#mandi_cost'),aggregator_ids, aggregator_names, 'user_created__id', mandi_ids, mandi_names, 'mandi__id', aggregator_graphs_json_data.transportation_cost_mandi);
    // cpk_spk_graph(aggregator_ids, aggregator_names, 'user_created__id', mandi_ids, mandi_names, 'mandi__id', aggregator_graphs_json_data);

}

function update_graphs_gaddidar_wise() {

    var option = $('#v_a :selected').val();
    if (option == 1) {
        aggregator_graph($('#aggregator_mandi'), aggregator_ids, aggregator_names, 'user_created__id', gaddidar_ids, gaddidar_names, 'gaddidar__id', aggregator_graphs_json_data.aggregator_gaddidar, "quantity__sum");
        aggregator_graph($('#aggregator_gaddidar'), mandi_ids, mandi_names, 'mandi__id', gaddidar_ids, gaddidar_names, 'gaddidar__id', aggregator_graphs_json_data.mandi_gaddidar, "quantity__sum");
        aggregator_graph($('#aggregator_crop'), crop_ids, crop_names, 'crop__id', gaddidar_ids, gaddidar_names, 'gaddidar__id', aggregator_graphs_json_data.gaddidar_crop, "quantity__sum");
    } else if (option == 2) {
        aggregator_graph($('#aggregator_mandi'), aggregator_ids, aggregator_names, 'user_created__id', gaddidar_ids, gaddidar_names, 'gaddidar__id', aggregator_graphs_json_data.aggregator_gaddidar, "amount__sum");
        aggregator_graph($('#aggregator_gaddidar'), mandi_ids, mandi_names, 'mandi__id', gaddidar_ids, gaddidar_names, 'gaddidar__id', aggregator_graphs_json_data.mandi_gaddidar, "amount__sum");
        aggregator_graph($('#aggregator_crop'), crop_ids, crop_names, 'crop__id', gaddidar_ids, gaddidar_names, 'gaddidar__id', aggregator_graphs_json_data.gaddidar_crop, "amount__sum");
    }
    // transport_cost_graph($('#mandi_cost'),aggregator_ids, aggregator_names, 'user_created__id', mandi_ids, mandi_names, 'mandi__id', aggregator_graphs_json_data.transportation_cost_mandi);
    // cpk_spk_graph(aggregator_ids, aggregator_names, 'user_created__id', mandi_ids, mandi_names, 'mandi__id', aggregator_graphs_json_data);

}

function get_data() {
    var start_date = $('#from_date').val();
    var end_date = $('#to_date').val();
    // Get rest of the filters
    aggregator_ids = [];
    aggregator_names = [];
    var village_ids = [];
    crop_ids = [];
    crop_names = [];
    mandi_ids = [];
    mandi_names = [];
    gaddidar_ids = [];
    gaddidar_names = [];

    $('#aggregators').children().each(function() {
        var aggregator_div = $(this).children()[1].firstChild;
        if (aggregator_div.checked) {
            aggregator_ids.push(aggregator_div.getAttribute('data'));
            aggregator_names.push(aggregator_div.getAttribute('value'));
        }
    });

    $('#villages').children().each(function() {
        var village_div = $(this).children()[1].firstChild;
        if (village_div.checked)
            village_ids.push(village_div.getAttribute('data'));
    });

    $('#crops').children().each(function() {
        var crop_div = $(this).children()[1].firstChild;
        if (crop_div.checked) {
            crop_ids.push(crop_div.getAttribute('data'));
            crop_names.push(crop_div.getAttribute('value'));
        }
    });

    $('#mandis').children().each(function() {
        var mandi_div = $(this).children()[1].firstChild;
        if (mandi_div.checked) {
            mandi_ids.push(mandi_div.getAttribute('data'));
            mandi_names.push(mandi_div.getAttribute('value'));
        }
    });
    $('#gaddidars').children().each(function() {
        var gaddidar_div = $(this).children()[1].firstChild;
        if (gaddidar_div.checked) {
            gaddidar_ids.push(gaddidar_div.getAttribute('data'));
            gaddidar_names.push(gaddidar_div.getAttribute('value'));
        }
    });

    if (Date.parse(start_date) > Date.parse(end_date)) {
        //$('.modal-trigger').leanModal();
        $('#modal1').openModal();
    } else {
        getvillagedata(start_date, end_date, aggregator_ids, village_ids, crop_ids, mandi_ids);
        getaggregatordata(start_date, end_date, aggregator_ids, village_ids, crop_ids, mandi_ids);
        // getcropdata(start_date, end_date, aggregator_ids, village_ids, crop_ids, mandi_ids);
        get_aggregator_wise_data(start_date, end_date, aggregator_ids, village_ids, crop_ids, mandi_ids, gaddidar_ids);
        fillaggregatormanditable(start_date, end_date, aggregator_ids, village_ids, crop_ids, mandi_ids, gaddidar_ids);
    }
}

/* Initializing filters */

function get_filter_data() {
    $.get("/loop/filter_data/", {})
        .done(function(data) {
            data_json = JSON.parse(data);
            aggregators_for_filter = data_json.aggregators;
            mandis_for_filter = data_json.mandis;
            gaddidars_for_filter = data_json.gaddidars;
            fill_aggregator_filter(aggregators_for_filter);
            fill_village_filter(data_json.villages);
            fill_crop_filter(data_json.crops);
            fill_mandi_filter(mandis_for_filter);
            fill_gaddidar_filter(gaddidars_for_filter);
            get_data();
        });
}

function fill_aggregator_filter(data_json) {
    $.each(data_json, function(index, data) {
        create_filter($('#aggregators'), data.user__id, data.name, true);
    });
}

function fill_village_filter(data_json) {
    $.each(data_json, function(index, data) {
        create_filter($('#villages'), data.id, data.village_name, true);
    });
}

function fill_crop_filter(data_json) {
    $.each(data_json, function(index, data) {
        create_filter($('#crops'), data.id, data.crop_name, true);
    });
}

function fill_mandi_filter(data_json) {
    $.each(data_json, function(index, data) {
        create_filter($('#mandis'), data.id, data.mandi_name, true);
    });
}

function fill_gaddidar_filter(data_json) {
    $.each(data_json, function(index, data) {
        create_filter($('#gaddidars'), data.id, data.gaddidar_name, true);
    });
}

function create_filter(tbody_obj, id, name, checked) {
    var row = $('<tr>');
    var td_name = $('<td>').html(name);
    row.append(td_name);
    var checkbox_html = '<input type="checkbox" class="black" data=' + id + ' id="' + name + id + '" checked="checked" value = ' + name + ' /><label for="' + name + id + '"></label>';
    var td_checkbox = $('<td>').html(checkbox_html);
    row.append(td_checkbox);
    tbody_obj.append(row);
}

/* ajax to get json */

function getvillagedata(start_date, end_date, aggregator_ids, village_ids, crop_ids, mandi_ids) {
    show_progress_bar();
    $.get("/loop/village_wise_data/", {
            'start_date': start_date,
            'end_date': end_date,
            'aggregator_ids[]': aggregator_ids,
            'village_ids[]': village_ids,
            'crop_ids[]': crop_ids,
            'mandi_ids[]': mandi_ids
        })
        .done(function(data) {
            data_json = JSON.parse(data);
            hide_progress_bar();
            fillvillagetable(data_json);
        });
}

function getaggregatordata(start_date, end_date, aggregator_ids, village_ids, crop_ids, mandi_ids) {
    show_progress_bar();
    $.get("/loop/aggregator_wise_data/", {
            'start_date': start_date,
            'end_date': end_date,
            'aggregator_ids[]': aggregator_ids,
            'village_ids[]': village_ids,
            'crop_ids[]': crop_ids,
            'mandi_ids[]': mandi_ids
        })
        .done(function(data) {
            data_json = JSON.parse(data);
            hide_progress_bar();
            fillaggregatortable(data_json);
        });
}

function getcropdata(start_date, end_date, aggregator_ids, village_ids, crop_ids, mandi_ids) {
    show_progress_bar();
    $.get("/loop/crop_wise_data/", {
            'start_date': start_date,
            'end_date': end_date,
            'aggregator_ids[]': aggregator_ids,
            'village_ids[]': village_ids,
            'crop_ids[]': crop_ids,
            'mandi_ids[]': mandi_ids
        })
        .done(function(data) {
            data_json = JSON.parse(data);
            hide_progress_bar();
            plot_cropwise_data(data_json);
        });
}

/* Table Generating UI Functions - Fill data in tables */

function fillvillagetable(data_json) {
    $('#table1 tr:gt(0)').remove();
    var row = $('#table1_tbody');
    var tr_name = $('<tr>');
    var table_ref = document.getElementById('table1');
    var total_volume = 0;
    var total_amount = 0;
    var total_farmers = 0;
    var total_avg = 0;
    var str1 = 'Rs. ';
    for (i = 0; i < data_json.length; i++) {
        var row = table_ref.insertRow(-1);
        var cell1 = row.insertCell(0);
        var cell2 = row.insertCell(1);
        var cell3 = row.insertCell(2);
        var cell4 = row.insertCell(3);
        var cell5 = row.insertCell(4);

        cell1.innerHTML = data_json[i]['farmer__village__village_name'];
        cell1.setAttribute('style', 'text-align:center;');
        cell2.innerHTML = data_json[i]['quantity__sum'].toString().concat(" Kg");
        cell2.setAttribute('style', 'text-align:center;');
        cell3.innerHTML = data_json[i]['amount__sum'].toFixed(2);
        cell3.setAttribute('style', 'text-align:center;');
        cell4.innerHTML = data_json[i]['farmer__count'].toString();
        cell4.setAttribute('style', 'text-align:center;');
        var avg = (data_json[i]['total_farmers']) / (data_json[i]['date__count'])
        cell5.innerHTML = avg.toFixed(2);
        cell5.setAttribute('style', 'text-align:center;');

        total_volume += data_json[i]['quantity__sum'];
        total_amount += data_json[i]['amount__sum'];
        total_farmers += data_json[i]['farmer__count'];
        total_avg += avg;
    }
    // if there are entries in the table
    if (data_json.length) {
        var row = table_ref.insertRow(-1);
        var cell1 = row.insertCell(0);
        var cell2 = row.insertCell(1);
        var cell3 = row.insertCell(2);
        var cell4 = row.insertCell(3);
        var cell5 = row.insertCell(4);
        cell1.innerHTML = "TOTAL";
        cell1.setAttribute('style', 'text-align:center; font-weight:bold;');
        cell2.innerHTML = total_volume.toFixed(1).toString().concat(" Kg");
        cell2.setAttribute('style', 'text-align:center; font-weight:bold;');
        cell3.innerHTML = str1.concat((total_amount).toFixed(2));
        cell3.setAttribute('style', 'text-align:center; font-weight:bold;');
        cell4.innerHTML = total_farmers;
        cell4.setAttribute('style', 'text-align:center; font-weight:bold;');
        cell5.innerHTML = (total_avg / data_json.length).toFixed(2);
        cell5.setAttribute('style', 'text-align:center; font-weight:bold;');
        // function call to make village pie chart
    }
    plot_village_data(data_json, total_volume, total_amount);

}

function fillaggregatortable(data_json) {
    var table_ref = document.getElementById("table2");
    $('#table2 tr:gt(0)').remove();
    row = $('#table2_tbody');
    tr_name = $('<tr>');
    row.append(tr_name);

    var total_volume = 0;
    var total_amount = 0;
    var total_farmers = 0;
    var total_avg = 0;
    var str1 = "Rs. "
    for (var i = 0; i < data_json.length; i++) {
        var row = table_ref.insertRow(-1);
        var cell1 = row.insertCell(0);
        var cell2 = row.insertCell(1);
        var cell3 = row.insertCell(2);
        var cell4 = row.insertCell(3);
        var cell5 = row.insertCell(4);

        cell1.innerHTML = data_json[i]['user_name'];
        cell2.innerHTML = data_json[i]['quantity__sum'].toString().concat(" Kg");
        cell3.innerHTML = data_json[i]['amount__sum'].toFixed(2);
        cell4.innerHTML = data_json[i]['farmer__count'].toString();
        var avg = (data_json[i]['total_farmers']) / (data_json[i]['date__count']);
        cell5.innerHTML = avg.toFixed(2);

        total_volume += data_json[i]['quantity__sum'];
        total_amount += data_json[i]['amount__sum'];
        total_farmers += data_json[i]['farmer__count'];
        total_avg += avg;
    };
    if (data_json.length) {
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
        cell3.innerHTML = str1.concat((total_amount).toFixed(2));
        cell3.style.fontWeight = "bold";
        cell4.innerHTML = total_farmers;
        cell4.style.fontWeight = "bold";
        cell5.innerHTML = (total_avg / data_json.length).toFixed(2);
        cell5.style.fontWeight = "bold";
        // call to make aggregator pie chart
    }
    plot_aggregator_data(data_json, total_volume, total_amount);
}

/* Fill data for highcharts */
function plot_village_data(data_json, total_volume, total_amount) {
    var vol_data = [];
    var amt_data = [];
    for (var i = 0; i < data_json.length; i++) {
        vol_data.push([data_json[i]['farmer__village__village_name'], (data_json[i]['quantity__sum'] * 100.0) / total_volume])
    }
    for (var i = 0; i < data_json.length; i++) {
        amt_data.push([data_json[i]['farmer__village__village_name'], (data_json[i]['amount__sum'] * 100.0) / total_amount])
    }
    plot_piechart($('#pie_vol'), vol_data, 'Villages');
    plot_piechart($('#pie_amount'), amt_data, 'Villages');
}

function plot_aggregator_data(data_json, total_volume, total_amount) {
    var vol_data = [];
    var amt_data = [];
    for (var i = 0; i < data_json.length; i++) {
        vol_data.push([data_json[i]['user_name'], (data_json[i]['quantity__sum'] * 100.0) / total_volume])
    }
    for (var i = 0; i < data_json.length; i++) {
        amt_data.push([data_json[i]['user_name'], (data_json[i]['amount__sum'] * 100.0) / total_amount])
    }
    plot_piechart($('#pie_vol2'), vol_data, 'VRP');
    plot_piechart($('#pie_amount2'), amt_data, 'VRP');

}

function plot_cropwise_data(data_json) {
    var x_axis = data_json['dates'];
    var total_crop_price = [];
    var total_crop_volume = [];
    var total_crop_income = [];
    // crop wise data calculation - amount , volume and price
    for (i = 0; i < data_json['crops'].length; i++) {
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
        for (j = 0; j < data_json['transactions'].length; j++) {
            if (data_json['transactions'][j]['crop__crop_name'] == temp_price_dict['name']) {
                var index_date = x_axis.indexOf(data_json['transactions'][j]['date']);
                temp_amt_dict['data'][index_date] = data_json['transactions'][j]['amount__sum'];
                temp_vol_dict['data'][index_date] = data_json['transactions'][j]['quantity__sum'];
                if (temp_vol_dict['data'][index_date] != 0) {
                    temp_price_dict['data'][index_date] = temp_amt_dict['data'][index_date] / temp_vol_dict['data'][index_date];
                }
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
    for (k = 0; k < data_json['farmer_count'].length; k++) {
        data_dict["data"][k] = data_json['farmer_count'][k]['farmer__count'];
    }
    total_crop_volume.push(data_dict);

    // crop and aggregator wise price calculation
    var total_crop_aggregator_price = [];
    for (l = 0; l < data_json['crops_aggregators'].length; l++) {
        var temp_price_dict = {};
        var temp_crop = data_json['crops_aggregators'][l]['crop__crop_name'];
        var temp_aggregator = data_json['crops_aggregators'][l]['user_name'];
        var temp_aggregator_id = data_json['crops_aggregators'][l]['user_created__id']
        temp_price_dict['name'] = temp_crop + '-' + temp_aggregator;
        temp_price_dict['data'] = new Array(x_axis.length).fill(0.0);
        for (j = 0; j < data_json['crops_aggregators_transactions'].length; j++) {
            if (data_json['crops_aggregators_transactions'][j]['crop__crop_name'] == temp_crop && data_json['crops_aggregators_transactions'][j]['user_created__id'] == temp_aggregator_id) {
                var index_date = x_axis.indexOf(data_json['crops_aggregators_transactions'][j]['date']);
                var temp_amt_dict = data_json['crops_aggregators_transactions'][j]['amount'];
                var temp_vol_dict = data_json['crops_aggregators_transactions'][j]['quantity'];
                if (temp_vol_dict != 0) {
                    temp_price_dict['data'][index_date] = temp_amt_dict / temp_vol_dict;
                }
            }
        }
        total_crop_aggregator_price.push(temp_price_dict);
    }
    show_charts();
    // Plot charts
    plot_stacked_chart($("#crops_price"), x_axis, total_crop_income, "Total Amount Earned(₹)", "₹", true);
    plot_multiline_chart($("#crops_price2"), x_axis, total_crop_price, "Crop Price Per Day(₹)", "₹");
    plot_multiline_chart($("#crop_aggregator_price"), x_axis, total_crop_aggregator_price, "Crop Price Per Day(₹)");
    plot_stacked_chart($("#crops_volume"), x_axis, total_crop_volume, "Total Volume Dispatched(kg)", "kg", false, /*dashboard.farmers_count*/ null);
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
        tooltip: {
            valuePrefix: 'Rs. '
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

    // if (farmer_counts) {
    //   var data_dict = {};
    //   data_dict["name"] = "Farmer Count";
    //   data_dict["type"] = "line";
    //   data_dict["yAxis"] = 1;
    //   data_dict["data"] = farmer_counts;
    //   dict.push(data_dict);
    // }

    container_obj.highcharts({
        chart: {
            type: 'column',
            // height: 500,
        },
        xAxis: {
            categories: x_axis,
            labels: {
                rotation: 0
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
                text: null,
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
        title: {
            text: null
        },
       legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            borderWidth: 0
        },
        tooltip: {
            headerFormat: '<b>{point.x}</b><br/>',
            /*pointFormat: '{series.name}: ' + ((prefix_or_suffix)?unit + ' ':'') + '{point.y:.1f}'+ ((prefix_or_suffix)?'':' ' + unit) + '<br/>Total: ' + ((prefix_or_suffix)?unit + ' ':'') + '{point.stackTotal:.1f}'+ ((prefix_or_suffix)?'':' ' + unit)*/
            shared: false
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
bullet_options = {
    type: "bullet",
    width: "100",
    height: "30",
    performanceColor: '#00bfbf',
    rangeColors: ['#a2d6d6']
}

function total_static_data() {
    $.get("/loop/total_static_data/", {}).done(function(data) {
        var json_data = JSON.parse(data);
        var total_volume = json_data['total_volume']['quantity__sum'];
        var total_amount = json_data['total_volume']['amount__sum'];
        var total_farmers_reached = json_data['total_farmers_reached'];
        var total_repeat_farmers = json_data['total_repeat_farmers']
        var total_transportation_cost = json_data['total_transportation_cost']['transportation_cost__sum'];
        var total_farmer_share = json_data['total_transportation_cost']['farmer_share__sum'];
        var total_expenditure = total_transportation_cost - total_farmer_share;
        var sustainability = total_farmer_share / total_transportation_cost * 100;
        var clusters = json_data['total_cluster_reached'];
        var total_volume_for_transport = json_data['total_volume_for_transport']['quantity__sum'];
        console.log("avinash"+total_volume_for_transport);
        var total_cpk = total_transportation_cost/total_volume_for_transport;
        var kg = "Kg";
        var rs = "₹";
        document.getElementById('total_volume_card').innerHTML = parseFloat(total_volume).toFixed(2).concat(kg);
        document.getElementById('total_farmers_card').innerHTML = total_farmers_reached +" <sub style='font-size: 12px'>"+parseFloat((total_repeat_farmers/total_farmers_reached)*100).toFixed(2)+"%"+"</sub>";   
        document.getElementById('total_expenditure_card').innerHTML =  parseFloat(total_cpk).toFixed(2); //rs.concat(parseFloat(total_transportation_cost).toFixed(2) - parseFloat(total_farmer_share).toFixed(2));
        document.getElementById('sustainability_card').innerHTML = parseFloat(sustainability).toFixed(2).concat(" %");
        document.getElementById('revenue_card').innerHTML =rs.concat(parseFloat(total_amount).toFixed(2));
        document.getElementById('cluster_card').innerHTML = clusters;

        $('#total_volume_bullet').sparkline([1000000, total_volume, 1500000], bullet_options);

        $('#total_farmers_bullet').sparkline([1500, total_farmers_reached, 5000], bullet_options);

        $('#total_expenditure_bullet').sparkline([0.4, total_cpk, 0.5], bullet_options);

        $('#sustainability_bullet').sparkline([60, sustainability, 100], bullet_options);
        $('#revenue_bullet').sparkline([10000000, total_amount, 15000000], bullet_options);
        $('#cluster_bullet').sparkline([30, clusters, 50], bullet_options);
    })
}

function recent_graphs_data() {
    $.get("/loop/recent_graphs_data/", {
        'start_date': start_date_main,
        'end_date': end_date_main
    }).done(function(data) {
        json_data = JSON.parse(data);
        dates = json_data['dates'];
        aggregators_details = json_data.aggregators;
        mandis = json_data['mandis'];
        stats = json_data['stats'];
        transportation = json_data['transportation_cost'];
        crops = json_data['crops'];

        plot_main_graphs();
        plot_cards_data();

    });
}

sparkline_option = {
    type: 'line',
    width: '100',
    height: '40',
    lineColor: '#00bfbf',
    fillColor: '#dde1df',
    lineWidth: 2
}

function plot_cards_data() {
    var avg = get_average(); // Retunts [avg_volume, active_farmers, avg_amount]
    var cumm = cummulative();
    var avg_vol = avg[0];
    var kg = "Kg";
    var rs = "₹";
    document.getElementById('recent_volume_card').innerHTML = parseFloat(avg_vol[0]).toFixed(2).concat(kg);
    $('#recent_volume_sparkline').sparkline(avg_vol.reverse(), sparkline_option);

    var active_farmers = avg[1];
    document.getElementById('recent_active_farmers_card').innerHTML = active_farmers[0];
    $('#recent_active_farmers_sparkline').sparkline(active_farmers.reverse(), sparkline_option);
    
    var avg_amt = avg[2];
    document.getElementById('recent_revenue_card').innerHTML = parseFloat(avg_amt[0]).toFixed(2);
    $('#recent_revenue_sparkline').sparkline(avg_amt.reverse(), sparkline_option);

    var data = get_cpk(avg_vol.reverse());
    console.log(avg_vol);
    var cpk = data[0];
    document.getElementById('cpk_card').innerHTML = rs.concat(parseFloat(cpk[0]).toFixed(2));
    $('#cpk_sparkline').sparkline(cpk.reverse(), sparkline_option);

    var sustainability = data[1];
    document.getElementById('recent_sustainability_card').innerHTML = rs.concat(parseFloat(sustainability[0]).toFixed(2));
    $('#recent_sustainability_sparkline').sparkline(sustainability.reverse(), sparkline_option);
}

function cummulative(){
    var all_dates = [];
    var first_date = new Date(dates[dates.length-1]);
    while (first_date < new Date(dates[0])){
        all_dates.push(first_date.getTime());
        first_date.setDate(first_date.getDate()+1)
    }
    var cumm = new Array(all_dates.length).fill(0.0);
    for (var i=0; i<stats.length;i++){
        var index = all_dates.indexOf(new Date(stats[i]['date']).getTime());
        cumm[index]+=stats[i]['quantity__sum'];
    }
    for (var i=cumm.length-2; i>=0;i--){
        cumm[i]+=cumm[i+1];
    }
    console.log(cumm);
    return cumm;
}

function get_average() {

    if (end_date_main.length > 0) {
        var today = new Date(end_date_main);
    } else {
        var today = new Date();
    }

    today.setDate(today.getDate() - days_to_average);
    var avg_vol = [];
    var avg_amt =[];
    var active_farmers = [];
    var active_farmers_id = [];
    var j = 0,
        temp = 0,
        temp_amt=0;
    //If no data is present for a period of days_to_average initially
    while (today >= new Date(stats[j]['date'])) {
        avg_vol.push(0);
        avg_amt.push(0);
        active_farmers.push(0);
        today.setDate(today.getDate() - days_to_average);
    }
    while (j < stats.length && today < new Date(stats[j]['date'])) {
        temp += stats[j]['quantity__sum'];
        temp_amt += stats[j]['amount__sum'];

        var farmer_id = stats[j]['farmer__id'];
        if (active_farmers_id.indexOf(farmer_id) == -1) {
            active_farmers_id.push(farmer_id);
        }
        j++;
        if (j < stats.length && today >= new Date(stats[j]['date'])) {
            avg_vol.push(temp / days_to_average);
            avg_amt.push(temp_amt / days_to_average);
            temp = 0;
            temp_amt=0;
            today.setDate(today.getDate() - days_to_average);
            active_farmers.push(active_farmers_id.length);
            active_farmers_id = [];
            //If no data is present for a period of days_to_average
            while (today >= new Date(stats[j]['date'])) {
                avg_vol.push(0);
                avg_amt.push(0);
                active_farmers.push(0);
                today.setDate(today.getDate() - days_to_average);
            }
        }
    }
    avg_vol.push(temp / days_to_average);
    avg_amt.push(temp_amt / days_to_average);
    active_farmers.push(active_farmers_id.length);

    return [avg_vol, active_farmers, avg_amt];
}

function get_cpk(avg_vol) {
    var today = new Date();
    today.setDate(today.getDate() - days_to_average);
    var cpk = [];
    var sustainability_per_kg = [];
    var j = 0,
        temp = 0,
        k = 0,
        f_share = 0;
    //If no data is present for a period of days_to_average initially
    while (today >= new Date(transportation[j]['date'])) {
        cpk.push(0);
        sustainability_per_kg.push(0);
        today.setDate(today.getDate() - days_to_average);
        k++;
    }
    while (j < transportation.length && today < new Date(transportation[j]['date'])) {
        temp += transportation[j]['transportation_cost__sum']; // - transportation[j]['farmer_share__sum'];
        f_share += transportation[j]['farmer_share__sum'];
        j++;
        if (j < transportation.length && today >= new Date(transportation[j]['date'])) {
            if (avg_vol[k]==0){
                cpk.push(0);
                sustainability_per_kg.push(0);
            }else{
                cpk.push((temp / days_to_average) / avg_vol[k]);
                sustainability_per_kg.push(f_share/temp);
            }
            
            k++;
            today.setDate(today.getDate() - days_to_average);
            temp = 0;
            f_share = 0;
            //If no data is present for a period of days_to_average
            while (today >= new Date(transportation[j]['date'])) {
                cpk.push(0);
                sustainability_per_kg.push(0);
                today.setDate(today.getDate() - days_to_average);
                k++;
            }
        }
    }

    if (avg_vol[k]==0){
        cpk.push(0);
        sustainability_per_kg.push(0);
    }else{
        cpk.push((temp / days_to_average) / avg_vol[k]);
        sustainability_per_kg.push(f_share/temp);
    }

    //Adding 0 cost for previous data making length of both arrays same
    for (var i = cpk.length; i < avg_vol.length; i++) {
        cpk.push(0);
        sustainability_per_kg.push(0);
    }
    return [cpk, sustainability_per_kg];
}

function plot_main_graphs() {
    temp_aggregator_volume = new Array(aggregators_details.length).fill(0.0);
    temp_mandi_volume = new Array(mandis.length).fill(0.0);
    temp_crop_volume = new Array(crops.length).fill(0.0);
    temp_crop_amount = new Array(crops.length).fill(0.0);

    // var temp_aggregator_farmer = new Array(aggregators.length);
    //
    // for(var i=0;i<temp_aggregator_farmer.length;i++){
    //   temp_aggregator_farmer[i]=[];
    // }
    // console.log(temp_aggregator_farmer.length);
    // aggregator_farmers = [];

    var stats_length = stats.length;
    for (var i = 0; i < stats_length; i++) {
        agg_index = aggregators_details.map(function(e) {
            return e.user_id
        }).indexOf(stats[i]['user_created__id']);
        mandi_index = mandis.map(function(e) {
            return e.id
        }).indexOf(stats[i]['mandi__id']);
        crop_index = crops.map(function(e) {
            return e.crop_name
        }).indexOf(stats[i]['crop__crop_name']);

        var quantity = stats[i]['quantity__sum'];
        temp_aggregator_volume[agg_index] += quantity;
        temp_mandi_volume[mandi_index] += quantity;
        temp_crop_volume[crop_index] += quantity;

        temp_crop_amount[crop_index] += stats[i]['amount__sum'];

        // var farmer_id = stats[i]['farmer__id'];
        // if (temp_aggregator_farmer[agg_index].indexOf(farmer_id) == -1) {
        //     temp_aggregator_farmer[agg_index].push(farmer_id);
        //   }
    }
    // for (var i = 0; i < temp_aggregator_farmer.length; i++) {
    //     aggregator_farmers.push(temp_aggregator_farmer[i].length);
    // }
    // aggregator_wise_total_data();

    temp_aggregator_cost = new Array(aggregators_details.length).fill(0.0);
    temp_mandi_cost = new Array(mandis.length).fill(0.0);
    var transportation_length = transportation.length;
    for (var i = 0; i < transportation_length; i++) {
        var agg_index = aggregators_details.map(function(e) {
            return e.user_id
        }).indexOf(transportation[i]['user_created__id']);
        var mandi_index = mandis.map(function(e) {
            return e.id
        }).indexOf(transportation[i]['mandi__id']);
        temp_aggregator_cost[agg_index] += (transportation[i]['transportation_cost__sum'] - transportation[i]['farmer_share__sum']);
        temp_mandi_cost[mandi_index] += (transportation[i]['transportation_cost__sum'] - transportation[i]['farmer_share__sum']);
    }

    var temp_aggregator_cost_length = temp_aggregator_cost.length;
    for (var i = 0; i < temp_aggregator_cost_length; i++) {
        if (temp_aggregator_volume[i] != 0)
            temp_aggregator_cost[i] /= temp_aggregator_volume[i];
    }
    var temp_mandi_cost_length = temp_mandi_cost.length;
    for (var i = 0; i < temp_mandi_cost_length; i++) {
        if (temp_mandi_volume[i] != 0)
            temp_mandi_cost[i] /= temp_mandi_volume[i];
    }

    farmer_count_aggregator_wise();

}

function aggregator_wise_total_data() {
    counter_check_length = aggregators_details.length;
    counter_volume = 0;
    counter_farmer = 0;
    counter_cost = 0;
    sorted_vol = sort_data(aggregators_details, temp_aggregator_volume, "name");
    sorted_farmer = sort_data(aggregators_details, aggregator_farmers, "name");
    sorted_cpk = sort_data(aggregators_details, temp_aggregator_cost, 'name');

    $('#cpk_title').text("Cost/kg (INR)");
    plot($('#total_volume_graph'), sorted_vol[0], sorted_vol[1], counter_volume, "Volume");
    plot($('#total_farmers_graph'), sorted_farmer[0], sorted_farmer[1], counter_farmer, "Number Of Farmers");
    plot($('#cpk_graph'), sorted_cpk[0], sorted_cpk[1], counter_cost, "Cost per Kg");

    $('#farmer_div').show();
    $('#sustainability_div').hide();
}

function mandi_wise_total_data() {
    counter_check_length = mandis.length;
    counter_volume = 0;
    counter_farmer = 0;
    counter_cost = 0;

    sorted_vol = sort_data(mandis, temp_mandi_volume, "mandi_name");
    sorted_cpk = sort_data(mandis, temp_mandi_cost, "mandi_name");

    $('#cpk_title').text("Cost/kg (INR)");
    plot($('#total_volume_graph'), sorted_vol[0], sorted_vol[1], counter_volume, "Volume");
    plot($('#cpk_graph'), sorted_cpk[0], sorted_cpk[1], counter_cost, "Cost per Kg");

    $('#farmer_div').hide();
    $('#sustainability_div').hide();
}

function crop_wise_total_data() {
    counter_check_length = crops.length;
    counter_volume = 0;
    counter_farmer = 0;
    counter_cost = 0;
    sorted_vol = sort_data(crops, temp_crop_volume, "crop_name");
    sorted_cpk = sort_data(crops, temp_crop_amount, "crop_name");

    $('#cpk_title').text("Total Amount");
    plot($('#total_volume_graph'), sorted_vol[0], sorted_vol[1], counter_volume, "Volume");
    plot($('#cpk_graph'), sorted_cpk[0], sorted_cpk[1], counter_cost, "Amount");

    $('#farmer_div').hide();
    $('#sustainability_div').hide();
}


function sort_data(axis, data, name) {
    var sorted_axis_data = [];
    for (var i = 0; i < data.length; i++) {
        sorted_axis_data.push({
            'name': axis[i][name],
            'sort_by': data[i]
        });
    }
    sorted_axis_data.sort(function(a, b) {
        return b['sort_by'] - a['sort_by'];
    });

    var sorted_data = [];
    var sorted_axis = [];
    for (var i = 0; i < sorted_axis_data.length; i++) {
        sorted_axis.push(sorted_axis_data[i]['name']);
        sorted_data.push(sorted_axis_data[i]['sort_by']);
    }
    // plot(container, sorted_axis, sorted_data, counter);

    return [sorted_axis, sorted_data];
}

function plot(id, x_axis, data, counter, legendName) {
    var series = [];
    var temp_series = {};
    temp_series['name'] = legendName;
    temp_series['type'] = "bar";
    temp_series['showInLegend'] = false;
    temp_series['data'] = data.slice(counter, counter + 5);
    // temp_series['pointPadding']=0;
    // temp_series['groupPadding']=0.1;

    series.push(temp_series);
    plot_stacked_chart(id, x_axis.slice(counter, counter + 5), series);
}

function farmer_count_aggregator_wise() {
    $.get("/loop/farmer_count_aggregator_wise/", {
        'start_date': start_date_main,
        'end_date': end_date_main
    }).done(function(data) {
        var json_data = JSON.parse(data);

        aggregator_farmers = new Array(aggregators_details.length).fill(0);

        var farmers_count_length = json_data['farmers_count'].length;
        for (var i = 0; i < farmers_count_length; i++) {
            var agg_index = aggregators_details.map(function(e) {
                return e.user_id
            }).indexOf(json_data['farmers_count'][i]['user_created__id']);
            aggregator_farmers[agg_index] = json_data['farmers_count'][i]['farmer__count'];
        }
        aggregator_wise_total_data();
    });
}

function add_counter(chart) {
    if (chart == "volume") {
        counter_volume += 5;
        if (counter_volume >= counter_check_length) {
            counter_volume = 0;
        }
        plot($('#total_volume_graph'), sorted_vol[0], sorted_vol[1], counter_volume);
    }
    if (chart == "farmer") {
        counter_farmer += 5;
        if (counter_farmer >= counter_check_length) {
            counter_farmer = 0;
        }
        plot($('#total_farmers_graph'), sorted_farmer[0], sorted_farmer[1], counter_farmer);
    }
    if (chart == "cpk") {
        counter_cost += 5;
        if (counter_cost >= counter_check_length) {
            counter_cost = 0;
        }
        plot($('#cpk_graph'), sorted_cpk[0], sorted_cpk[1], counter_cost);
    }
}

function subtract_counter(chart) {
    if (chart == "volume") {
        counter_volume -= 5;
        if (counter_volume <= 0) {
            counter_volume = 0;
        }
        // $('#up_volume').addClass('show');

        plot($('#total_volume_graph'), sorted_vol[0], sorted_vol[1], counter_volume);
    }

    if (chart == "farmer") {
        counter_farmer -= 5;
        if (counter_farmer <= 0) {
            counter_farmer = 0;
        }
        plot($('#total_farmers_graph'), sorted_farmer[0], sorted_farmer[1], counter_farmer);
    }
    if (chart == "cpk") {
        counter_cost -= 5;
        if (counter_cost <= 0) {
            counter_cost = 0;
        }
        plot($('#cpk_graph'), sorted_cpk[0], sorted_cpk[1], counter_cost);
    }
}

function get_aggregator_wise_data(start_date, end_date, aggregator_ids, village_ids, crop_ids, mandi_ids, gaddidar_ids) {
    $.get("/loop/new_aggregator_wise_data/", {
            'start_date': start_date,
            'end_date': end_date,
            'aggregator_ids[]': aggregator_ids,
            'village_ids[]': village_ids,
            'crop_ids[]': crop_ids,
            'mandi_ids[]': mandi_ids,
            'gaddidar_ids[]': gaddidar_ids
        })
        .done(function(data) {
            aggregator_graphs_json_data = JSON.parse(data);
            update_graphs_aggregator_wise();
            line_graphs(start_date, end_date, aggregator_ids, village_ids, crop_ids, mandi_ids, gaddidar_ids);
        });
}

function aggregator_graph(container, axis, axis_names, axis_parameter, values, values_names, values_parameter, json_data, parameter) {
    var series = [];
    var x_axis = new Array(axis.length);

    var axis_length = axis.length;
    for (var i = 0; i < axis_length; i++) {
        x_axis[i] = axis_names[i];
    }

    var values_length = values.length;
    for (var i = 0; i < values_length; i++) {
        var temp_vol = {};
        temp_vol['name'] = values_names[i];
        temp_vol['type'] = "bar";
        temp_vol['stacking'] = "normal";
        temp_vol['data'] = new Array(axis.length).fill(0.0);
        temp_vol['showInLegend'] = false;

        series.push(temp_vol);
    }
    for (var i = 0; i < json_data.length; i++) {
        var agg_index = values.indexOf(json_data[i][values_parameter].toString());
        var index = axis.indexOf(json_data[i][axis_parameter].toString());

        series[agg_index]['data'][index] = json_data[i][parameter];
    }

    plot_stacked_chart(container, x_axis, series, '', 'kg');
}

function transport_cost_graph(container, axis, axis_names, axis_parameter, values, values_names, values_parameter, json_data) {
    var series = [];
    var x_axis = new Array(axis.length);
    for (var i = 0; i < axis.length; i++) {
        x_axis[i] = axis_names[i];
    }

    var values_names_length = values_names.length;
    for (var i = 0; i < values_names_length; i++) {
        var temp_cost = {};
        temp_cost['name'] = values_names[i];
        temp_cost['type'] = "bar";
        temp_cost['stacking'] = "normal";
        temp_cost['showInLegend'] = false;
        temp_cost['data'] = new Array(axis.length).fill(0);
        series.push(temp_cost);
    }

    var json_data_length = json_data.length;
    for (var i = 0; i < json_data_length; i++) {
        var agg_index = values.indexOf(json_data[i][values_parameter].toString());
        var index = axis.indexOf(json_data[i][axis_parameter].toString());

        series[agg_index]['data'][index] = json_data[i]['transportation_cost__sum'] - json_data[i]['farmer_share__sum'];
    }
    plot_stacked_chart(container, x_axis, series, '', 'Rs');
}

function cpk_spk_graph(axis, axis_names, axis_parameter, values, values_names, values_parameter, json_data) {
    var vol_stats = json_data.aggregator_mandi;
    var cost_stats = json_data.transportation_cost_mandi;
    var series_cpk = [];
    var series_spk = [];
    var x_axis = new Array(axis.length);
    for (var i = 0; i < axis.length; i++) {
        x_axis[i] = axis_names[i];
    }
    values_vol = [];
    values_cost_cpk = [];
    values_cost_spk = [];

    var values_names_length = values_names.length;
    for (var i = 0; i < values_names_length; i++) {
        var temp = {};
        var temp_spk = {};
        temp['name'] = values_names[i];
        temp['type'] = "bar";
        temp['stacking'] = "normal";
        temp['showInLegend'] = false;
        temp['data'] = new Array(axis.length).fill(0.0);


        temp_spk['name'] = values_names[i];
        temp_spk['type'] = "bar";
        temp_spk['stacking'] = "normal";
        temp_spk['showInLegend'] = false;
        temp_spk['data'] = new Array(axis.length).fill(0.0);

        series_cpk.push(temp);
        series_spk.push(temp_spk);
        values_vol.push(new Array(axis.length).fill(0.0));
        values_cost_cpk.push(new Array(axis.length).fill(0.0));
        values_cost_spk.push(new Array(axis.length).fill(0.0));
    }

    for (var i = 0; i < vol_stats.length; i++) {
        var agg_index = values.indexOf(vol_stats[i][values_parameter].toString());
        var index = axis.indexOf(vol_stats[i][axis_parameter].toString());
        values_vol[agg_index][index] = vol_stats[i]['quantity__sum'];
    }
    for (var i = 0; i < cost_stats.length; i++) {
        var agg_index = values.indexOf(cost_stats[i][values_parameter].toString());
        var index = axis.indexOf(cost_stats[i][axis_parameter].toString());
        values_cost_cpk[agg_index][index] = cost_stats[i]['transportation_cost__sum'] - cost_stats[i]['farmer_share__sum'];
        values_cost_spk[agg_index][index] = cost_stats[i]['farmer_share__sum'];
    }


    var values_names_length = values_names.length;
    for (var i = 0; i < values_names_length; i++) {
        for (var j = 0; j < axis_names.length; j++) {
            series_cpk[i]['data'][j] = values_vol[i][j] > 0 ? values_cost_cpk[i][j] / values_vol[i][j] : 0.0;
            series_spk[i]['data'][j] = values_vol[i][j] > 0 ? values_cost_spk[i][j] / values_vol[i][j] : 0.0;
        }
    }
    // console.log(series_cpk);
    plot_stacked_chart($('#cpk'), x_axis, series_cpk, '', 'Rs');
    plot_stacked_chart($('#spk'), x_axis, series_spk, '', 'Rs');
}

// function line_graphs(start_date, end_date, aggregator_ids, village_ids, crop_ids, mandi_ids, gaddidar_ids) {
//     $.get("/loop/data_for_line_graph", {
//         'start_date': start_date,
//         'end_date': end_date,
//         'aggregator_ids[]': aggregator_ids,
//         'village_ids[]': village_ids,
//         'crop_ids[]': crop_ids,
//         'mandi_ids[]': mandi_ids,
//         'gaddidar_ids[]': gaddidar_ids
//     }).done(function(data) {

//             data_for_line_graph = JSON.parse(data);
//             dates = data_for_line_graph['dates']
//             // plot_line_graph($('#container2'),dates, mandi_ids, mandi_names, 'mandi__id', data_for_line_graph['mandi_data']);
//             // plot_line_graph($('#container3'),dates, aggregator_ids, aggregator_names, 'user_created__id', data_for_line_graph['aggregator_data']);
//             plot_line_graph($('#container4'),dates, crop_ids, crop_names, 'crop__id', data_for_line_graph['crop_data']);
//             // plot_line_graph($('#container5'),dates, gaddidar_ids, gaddidar_names, 'gaddidar__id', data_for_line_graph['gaddidar_data']);
            
//         });
// }

function line_graphs(start_date, end_date, aggregator_ids, village_ids, crop_ids, mandi_ids, gaddidar_ids) {
    $.get("/loop/data_for_time_chart", {
        'start_date': start_date,
        'end_date': end_date,
        'aggregator_ids[]': aggregator_ids,
        'village_ids[]': village_ids,
        'crop_ids[]': crop_ids,
        'mandi_ids[]': mandi_ids,
        'gaddidar_ids[]': gaddidar_ids
    }).done(function(data) {

            data_for_time_chart = JSON.parse(data);
            var dates = data_for_time_chart['dates'];
            // plot_line_graph($('#container2'),dates, mandi_ids, mandi_names, 'mandi__id', data_for_line_graph['mandi_data']);
            // plot_line_graph($('#container3'),dates, aggregator_ids, aggregator_names, 'user_created__id', data_for_line_graph['aggregator_data']);
            plot_time_graph(data_for_time_chart['total_data']);
            // plot_line_graph($('#container5'),dates, gaddidar_ids, gaddidar_names, 'gaddidar__id', data_for_line_graph['gaddidar_data']);
            
        });
}
function plot_time_graph(json_data){

    var dates = [];
    var date = new Date(json_data[0]['date']);
    while(date<= new Date(json_data[json_data.length-1]['date'])){
        dates.push(date.getTime());
        date.setDate(date.getDate()+1);
    }

    var series = [];
    var temp_vol = {};
    temp_vol['name'] = "volume";
    temp_vol['data'] = new Array(dates.length);
    for (var j=0;j<dates.length;j++){
        temp_vol['data'][j] = [dates[j],0];
    };
    temp_vol['type'] = 'spline';
    temp_vol['pointInterval'] = 24 * 3600 * 1000;
    temp_vol['pointStart'] = dates[dates.length-1];
    temp_vol['showInLegend'] = true;

    var temp_amt = {};
    temp_amt['name'] = "amount";
    temp_amt['data'] = new Array(dates.length);
    for (var j=0;j<dates.length;j++){
        temp_amt['data'][j] = [dates[j],0];
    };
    temp_amt['type'] = 'spline';
    temp_amt['pointInterval'] = 24 * 3600 * 1000;
    temp_amt['pointStart'] = dates[dates.length-1];
    temp_amt['showInLegend'] = true;
    series.push(temp_vol);
    series.push(temp_amt);

    for (var i = 0; i < json_data.length; i++) {
        var date_index = dates.indexOf((new Date(json_data[i]['date'])).getTime());

        series[0]['data'][date_index][1] = json_data[i]['quantity__sum'];
        series[1]['data'][date_index][1] = json_data[i]['amount__sum'];
    }
    var $container = $('#container6')
                .css('position', 'relative');

            $('<div id="detail-container">')
                .appendTo($container);

            $('<div id="master-container">')
                .css({
                    position: 'absolute',
                    top: 300,
                    height: 100,
                    width: '100%'
                })
                    .appendTo($container);
    console.log(series);
    console.log(get_frequency_data(dates,series,3,false));
    createMaster(series);
}
// function plot_line_graph(container, axis, values, values_names, values_parameter, json_data) {

//     var x_axis = axis;
//     var series = [];
//     var values_names_length = values_names.length;
//     for (var i = 0; i < values_names_length; i++) {
//         var temp = {};
//         temp['name'] = values_names[i];
//         temp['data'] = new Array(x_axis.length);
//         for (var j=0;j<x_axis.length;j++){
//             temp['data'][j] = ([new Date(x_axis[j]).getTime(),0]);
//         };
//         temp['type'] = 'line';
//         temp['pointInterval'] = 24 * 3600 * 1000;
//         temp['pointStart'] = x_axis[x_axis.length-1];
//         // temp['stacking'] = 'normal';
//         temp['showInLegend'] = false;
//         series.push(temp);

//     }

//     var json_data_length = json_data.length;
//     for (var i = 0; i < json_data_length; i++) {
//         var index = values.indexOf(json_data[i][values_parameter].toString());
//         var date_index = x_axis.indexOf(json_data[i]['date']);

//         series[index]['data'][date_index][1] = json_data[i]['quantity__sum'];
//     }
//     // plot_time_chart(container, x_axis, series,"","")
//     var $container = $('#container6')
//                 .css('position', 'relative');

//             $('<div id="detail-container">')
//                 .appendTo($container);

//             $('<div id="master-container">')
//                 .css({
//                     position: 'absolute',
//                     top: 300,
//                     height: 100,
//                     width: '100%'
//                 })
//                     .appendTo($container);
    
//     createMaster(series);
// }


function createDetail(masterChart, dict) {

                // prepare the detail chart
                var myDict=[]
                var detailData = [],
                    detailStart = dict[0]['data'][0][0];

                $.each(masterChart.series, function () {
                    var temp ={};
                    temp['name'] = this.name;
                    temp['type'] = "spline"
                    temp['data'] = new Array();
                    temp['pointStart']= detailStart;
                    temp['pointInterval']= 24 * 3600 * 1000;
                    temp['showInLegend'] = true;
                    $.each(this.data, function () {
                        if (this.x >= detailStart) {
                            temp['data'].push(this.y);
                        }

                    });
                    myDict.push(temp)});

                // create a detail chart referenced by a global variable
                detailChart = $('#detail-container').highcharts({
                    chart: {
                        marginBottom: 120,
                        reflow: false,
                        marginLeft: 50,
                        marginRight: 20,
                        style: {
                            position: 'absolute'
                        }
                    },
                    credits: {
                        enabled: false
                    },
                    
                    xAxis: {
                        type: 'datetime'
                    },
                    yAxis: {
                        title: {
                            text: null
                        },
                        maxZoom: 0.1
                    },
                    tooltip: {
                        // formatter: function () {
                        //     var point = this.points[0];
                        //     return '<b>' + point.series.name + '</b><br/>' + Highcharts.dateFormat('%A %B %e %Y', this.x) + ':<br/>' +
                        //         'Volume= ' + Highcharts.numberFormat(point.y, 2);
                        // },
                        shared: true
                    },
                    legend: {
                        enabled: false
                    },
                    plotOptions: {
                        series: {
                            marker: {
                                enabled: false,
                                states: {
                                    hover: {
                                        enabled: true,
                                        radius: 3
                                    }
                                }
                            }
                        }
                    },
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
                    series: myDict,

                    exporting: {
                        enabled: false
                    }

                }).highcharts(); // return chart
            }

            // create the master chart
            function createMaster(dict) {
                $('#master-container').highcharts({
                    chart: {
                        reflow: false,
                        borderWidth: 0,
                        backgroundColor: null,
                        marginLeft: 50,
                        marginRight: 20,
                        zoomType: 'x',
                        events: {

                            // listen to the selection event on the master chart to update the
                            // extremes of the detail chart
                            selection: function (event) {
                                var extremesObject = event.xAxis[0],
                                    min = extremesObject.min,
                                    max = extremesObject.max,
                                    detailData = [],
                                    xAxis = this.xAxis[0],
                                    myDict = [];

                                $.each(this.series, function(){
                                    var temp ={};
                                    temp['name']= this.name;
                                    temp['data'] = new Array();
                                    temp['pointStart']= dict[0]['data'][0][0];
                                    temp['pointInterval']= 24 * 3600 * 1000;
                                    $.each(this.data, function(){
                                       if (this.x > min && this.x < max) {
                                            temp['data'].push([this.x, this.y]);
                                        } 
                                    });
                                    myDict.push(temp);
                                });
                                console.log(myDict);
                                // reverse engineer the last part of the data
                              
                                // move the plot bands to reflect the new detail span
                                xAxis.removePlotBand('mask-before');
                                xAxis.addPlotBand({
                                    id: 'mask-before',
                                    from: dict[0]['data'][0][0],    //data[0][0],
                                    to: min,
                                    color: 'rgba(0, 0, 0, 0.2)'
                                });

                                xAxis.removePlotBand('mask-after');
                                xAxis.addPlotBand({
                                    id: 'mask-after',
                                    from: max,
                                    to: dict[0]['data'][dict[0]['data'].length - 1][0],
                                    color: 'rgba(0, 0, 0, 0.2)'
                                });
                                var pos=0;
                                $.each(this.series, function(){
                                    detailChart.series[pos].setData(myDict[pos].data);
                                    pos++;
                                });
                                
                                
                                

                                return false;
                            }
                        }
                    },
                    title: {
                        text: null
                    },
                    xAxis: {
                        type: 'datetime',
                        showLastTickLabel: true,
                        maxZoom: 14 * 24 * 3600000, // fourteen days
                        plotBands: [{
                            id: 'mask-before',
                            from: dict[0]['data'][0][0],
                            to: dict[0]['data'][dict[0]['data'].length - 1][0],
                            color: 'rgba(0, 0, 0, 0.2)'
                        }],
                        title: {
                            text: null
                        }
                    },
                    yAxis: {
                        gridLineWidth: 0,
                        labels: {
                            enabled: false
                        },
                        title: {
                            text: null
                        },
                        min: 0.6,
                        showFirstLabel: false
                    },
                    tooltip: {
                        formatter: function () {
                            return false;
                        }
                    },
                    legend: {
                        enabled: false
                    },
                    credits: {
                        enabled: false
                    },
                    plotOptions: {
                        series: {
                            fillColor: {
                                linearGradient: [0, 0, 0, 70],
                                stops: [
                                    [0, Highcharts.getOptions().colors[0]],
                                    [1, 'rgba(255,255,255,0)']
                                ]
                            },
                            lineWidth: 1,
                            marker: {
                                enabled: false
                            },
                            shadow: false,
                            states: {
                                hover: {
                                    lineWidth: 1
                                }
                            },
                            enableMouseTracking: false
                        }
                    },

                    series: dict,

                    exporting: {
                        enabled: false
                    }

                }, function (masterChart) {
                    createDetail(masterChart, dict);
                })
                    .highcharts(); // return chart instance
            }

            // make the container smaller and add a second container for the master chart

            
function fillaggregatormanditable(start_date, end_date, aggregator_ids, village_ids, crop_ids, mandi_ids, gaddidar_ids) {
  $.get("/loop/visits_data/",
            {'start_date': start_date,
            'end_date': end_date,
            'aggregator_ids[]': aggregator_ids,
            'village_ids[]': village_ids,
            'crop_ids[]': crop_ids,
            'mandi_ids[]': mandi_ids,
            'gaddidar_ids[]': gaddidar_ids
        })
        .done(function(data) {
              var data_json = JSON.parse(data)  
              var x_axis = [];
              var x_axis_agg = [];
              var total_visits = [];
              var total_volume = [];
              var total_visits_mandi = [];
              var total_volume_mandi = [];

              for (i=0; i< data_json['aggregators'].length; i++){
                x_axis_agg.push(data_json['aggregators'][i]['name']);
                // Making a dict for graph
                total_visits[i] = {};
                total_visits[i]["name"] = data_json['aggregators'][i]['name'];
                total_visits[i]["data"] = new Array(data_json["mandis"].length).fill(0.0);
                total_visits[i]["type"] = "bar";
                total_visits[i]["stacking"] = "normal"; 
                total_volume[i] = {};
                total_volume[i]["name"] = data_json['aggregators'][i]['name'];
                total_volume[i]["data"] = new Array(data_json["mandis"].length).fill(0.0);
                total_volume[i]["type"] = "bar";
                total_volume[i]["stacking"] = "normal";

              }

              for (var i = 0; i < data_json['mandis'].length; i++) {

                x_axis.push(data_json['mandis'][i]['mandi_name']);
                total_visits_mandi[i] = {};
                total_visits_mandi[i]["name"] = data_json['mandis'][i]['mandi_name'];
                total_visits_mandi[i]["data"] = new Array(data_json["aggregators"].length).fill(0.0);
                total_visits_mandi[i]["type"] = "bar";
                total_visits_mandi[i]["stacking"] = "normal";
                total_volume_mandi[i] = {}
                total_volume_mandi[i]["name"] = data_json['mandis'][i]['mandi_name'];
                total_volume_mandi[i]["data"] = new Array(data_json["aggregators"].length).fill(0.0);
                total_volume_mandi[i]["type"] = "bar";
                total_volume_mandi[i]["stacking"] = "normal";


                for (j=0; j< data_json['aggregators'].length; j++){



                  for (k=0; k<data_json['aggregators_mandis'].length; k++){
                    if (data_json['aggregators_mandis'][k]['user_created__id'] == data_json['aggregators'][j]['user__id'] && data_json['aggregators_mandis'][k]['mandi__id'] == data_json['mandis'][i]['id']){

                      total_visits[j]["data"][i] = data_json['aggregators_mandis'][k]["mandi__id__count"];
                      total_volume[j]["data"][i] = data_json['aggregators_mandis'][k]["quantity__sum"];
                      total_visits_mandi[i]["data"][j] = data_json['aggregators_mandis'][k]["mandi__id__count"];
                      total_volume_mandi[i]["data"][j] = data_json['aggregators_mandis'][k]["quantity__sum"];

                    }
                  }

                }
              }
              plot_stacked_chart($("#visits"), x_axis, total_visits, "", "");
              plot_stacked_chart($("#mandi_visits"), x_axis_agg, total_visits_mandi, "", "");
              plot_stacked_chart($("#mvolume"), x_axis, total_volume, "", "");
              plot_stacked_chart($("#mmandi_volume"), x_axis_agg, total_volume_mandi, "", "");
          });
    
}




function get_frequency_data(x_axis, series, frequency, averaged){
  var first_date = new Date(x_axis[0]);
  var final_date = new Date(x_axis[x_axis.length - 1]);
  new_series=[];

  if (frequency==2){
    var new_x_axis = [];    
    while(first_date < final_date){
      new_x_axis.push(first_date.getTime());
      first_date.setDate(first_date.getDate()+7);
    }
  }

  else if (frequency==3){
    var new_x_axis = [];
    while (first_date < final_date) {
      if (first_date.getDate() <= 15){
        new_x_axis.push(new Date(first_date.getFullYear()+"-"+(first_date.getMonth()+1)+"-"+"01").getTime());
      }
      else{
        new_x_axis.push(new Date(first_date.getFullYear()+"-"+(first_date.getMonth()+1)+"-"+"16").getTime()); 
      }
      first_date.setDate(first_date.getDate()+15);
      if (first_date.getDate() == 31){
        first_date.setDate(first_date.getDate()+1);
      }
    };
  }
  else if (frequency==4){
    var new_x_axis = [];
    first_date.setDate(1)
    while (first_date <= final_date) {
      new_x_axis.push(new Date(first_date.getFullYear()+"-"+(first_date.getMonth()+1)+"-"+"01").getTime());
      first_date.setMonth(first_date.getMonth()+1);
    } 
  }

  for(i=0; i< series.length; i++){
    var temp_series = {};
    temp_series['name'] = series[i]['name'];
    temp_series['data'] = new Array(new_x_axis.length);
    for (var j=0;j<new_x_axis.length;j++){
        temp_series['data'][j]=[new_x_axis[j],0]
    }
    var count = 0;
    var temp = 0;
    var index = 0;
    for (k=0; k<series[i]['data'].length; k++){

      var temp_date = new Date(x_axis[k]); 
      if (new Date(new_x_axis[index+1]) <= new Date(x_axis[k])){
          index+=1;
      }
      if (averaged){
        if (temp != index){
          temp_series['data'][temp][1]=temp_series['data'][temp][1]/count;
          count = 0;
        }
      }
      temp_series['data'][index][1]+=series[i]['data'][k][1];
      count+=1;
      var temp = index;
    }
    if (averaged){
      temp_series['data'][temp][1]/=count;
    }
    new_series.push(temp_series);
  }
  return new_series;
}
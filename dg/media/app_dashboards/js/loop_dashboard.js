/* This file should contain all the JS for Loop dashboard */
window.onload = initialize;

function initialize() {
    // initialize any library here
    $('select').material_select();
    // to initialize material select
    if (document.title == "Home") {
        total_static_data();
        show_side_bar();
        recent_graphs_data();
        days_to_average = 15;
        days_to_go_back = 5;
        counter_volume = 0;
    } else if (document.title == "Second Page") {
        $(".button-collapse").sideNav();
        set_eventlistener();
        get_filter_data();
        update_tables();
        update_charts();
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
        update_graphs();
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

function update_graphs() {

    var option = $('#v_a :selected').val();
    if (option == 1) {
        aggregator_graph($('#aggregator_mandi'), mandi_ids, mandi_names, 'mandi__id', aggregator_ids, aggregator_names, aggregator_graphs_json_data.aggregator_mandi, "quantity__sum");
        aggregator_graph($('#aggregator_gaddidar'), gaddidar_ids, gaddidar_names, 'gaddidar__id', aggregator_ids, aggregator_names, aggregator_graphs_json_data.aggregator_gaddidar, "quantity__sum");
        aggregator_graph($('#aggregator_crop'), crop_ids, crop_names, 'crop__id', aggregator_ids, aggregator_names, aggregator_graphs_json_data.aggregator_crop, "quantity__sum");
    } else if (option == 2) {
        aggregator_graph($('#aggregator_mandi'), mandi_ids, mandi_names, 'mandi__id', aggregator_ids, aggregator_names, aggregator_graphs_json_data.aggregator_mandi, "amount__sum");
        aggregator_graph($('#aggregator_gaddidar'), gaddidar_ids, gaddidar_names, 'gaddidar__id', aggregator_ids, aggregator_names, aggregator_graphs_json_data.aggregator_gaddidar, "amount__sum");
        aggregator_graph($('#aggregator_crop'), crop_ids, crop_names, 'crop__id', aggregator_ids, aggregator_names, aggregator_graphs_json_data.aggregator_crop, "amount__sum");
    }
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
            height: 500,
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
    width: "150",
    height: "30",
    performanceColor: '#00bfbf',
    rangeColors: ['#a2d6d6']
}

function total_static_data() {
    $.get("/loop/total_static_data/", {}).done(function(data) {
        var json_data = JSON.parse(data);
        var total_volume = json_data['total_volume']['quantity__sum'];
        var total_farmers_reached = json_data['total_farmers_reached'];
        var total_transportation_cost = json_data['total_transportation_cost']['transportation_cost__sum'];
        var total_farmer_share = json_data['total_transportation_cost']['farmer_share__sum'];
        var total_expenditure = total_transportation_cost - total_farmer_share;
        var sustainability = total_farmer_share / total_transportation_cost * 100;
        document.getElementById('total_volume_card').innerHTML = parseFloat(total_volume).toFixed(2);
        document.getElementById('total_farmers_card').innerHTML = total_farmers_reached;
        document.getElementById('total_expenditure_card').innerHTML = parseFloat(total_transportation_cost).toFixed(2) - parseFloat(total_farmer_share).toFixed(2);
        document.getElementById('sustainability_card').innerHTML = parseFloat(sustainability).toFixed(2).concat(" %");

        $('#total_volume_bullet').sparkline([1000000, total_volume, 1500000], bullet_options);

        $('#total_farmers_bullet').sparkline([1500, total_farmers_reached, 5000], bullet_options);

        $('#total_expenditure_bullet').sparkline([1000000, total_expenditure, 5000000], bullet_options);

        $('#sustainability_bullet').sparkline([60, sustainability, 100], bullet_options);
    })
}

function show_side_bar() {}

function recent_graphs_data() {
    $.get("/loop/recent_graphs_data/", {}).done(function(data) {
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
    width: '150',
    height: '40',
    lineColor: '#00bfbf',
    fillColor: '#dde1df',
    lineWidth: 2
}

function plot_cards_data() {
    var avg = get_average();
    var avg_vol = avg[0];
    document.getElementById('recent_volume_card').innerHTML = parseFloat(avg_vol[0]).toFixed(2);
    $('#recent_volume_sparkline').sparkline(avg_vol.reverse(), sparkline_option);

    var active_farmers = avg[1];
    document.getElementById('recent_active_farmers_card').innerHTML = active_farmers[0];
    $('#recent_active_farmers_sparkline').sparkline(active_farmers.reverse(), sparkline_option);

    var data = get_cpk(avg_vol);
    var cpk = data[0];
    document.getElementById('cpk_card').innerHTML = parseFloat(cpk[0]).toFixed(2);
    $('#cpk_sparkline').sparkline(cpk.reverse(), sparkline_option);

    var sustainability = data[1];
    document.getElementById('recent_sustainability_card').innerHTML = parseFloat(sustainability[0]).toFixed(2);
    $('#recent_sustainability_sparkline').sparkline(sustainability.reverse(), sparkline_option);

}

function get_average() {
    var today = new Date('2016-05-31');
    today.setDate(today.getDate() - days_to_average);
    var avg_vol = [];
    var active_farmers = [];
    var active_farmers_id = [];
    var j = 0,
        temp = 0;
    //If no data is present for a period of days_to_average initially
    while (today >= new Date(stats[j]['date'])) {
        avg_vol.push(0);
        active_farmers.push(0);
        today.setDate(today.getDate() - days_to_average);
    }
    while (j < stats.length && today < new Date(stats[j]['date'])) {
        temp += stats[j]['quantity__sum'];
        var farmer_id = stats[j]['farmer__id'];
        if (active_farmers_id.indexOf(farmer_id) == -1) {
            active_farmers_id.push(farmer_id);
        }
        j++;
        if (j < stats.length && today >= new Date(stats[j]['date'])) {
            avg_vol.push(temp / days_to_average);
            temp = 0;
            today.setDate(today.getDate() - days_to_average);
            active_farmers.push(active_farmers_id.length);
            active_farmers_id = [];
            //If no data is present for a period of days_to_average
            while (today >= new Date(stats[j]['date'])) {
                avg_vol.push(0);
                active_farmers.push(0);
                today.setDate(today.getDate() - days_to_average);
            }
        }
    }
    avg_vol.push(temp / days_to_average);
    active_farmers.push(active_farmers_id.length);

    return [avg_vol, active_farmers];
}

function get_cpk(avg_vol) {
    var today = new Date('2016-05-31');
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
        temp += transportation[j]['transportation_cost__sum'] - transportation[j]['farmer_share__sum'];
        f_share += transportation[j]['farmer_share__sum'];
        j++;
        if (j < transportation.length && today >= new Date(transportation[j]['date'])) {
            cpk.push((temp / days_to_average) / avg_vol[k]);
            sustainability_per_kg.push(f_share / avg_vol[k]);
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
    cpk.push((temp / days_to_average) / avg_vol[k]);
    sustainability_per_kg.push(f_share / avg_vol[k]);
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

    for (var i = 0; i < stats.length; i++) {
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
    for (var i = 0; i < transportation.length; i++) {
        var agg_index = aggregators_details.map(function(e) {
            return e.user_id
        }).indexOf(transportation[i]['user_created__id']);
        var mandi_index = mandis.map(function(e) {
            return e.id
        }).indexOf(transportation[i]['mandi__id']);
        temp_aggregator_cost[agg_index] += (transportation[i]['transportation_cost__sum'] - transportation[i]['farmer_share__sum']);
        temp_mandi_cost[mandi_index] += (transportation[i]['transportation_cost__sum'] - transportation[i]['farmer_share__sum']);
    }

    for (var i = 0; i < temp_aggregator_cost.length; i++) {
        if (temp_aggregator_volume[i] != 0)
            temp_aggregator_cost[i] /= temp_aggregator_volume[i];
    }
    for (var i = 0; i < temp_mandi_cost.length; i++) {
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
    plot($('#total_volume_graph'), sorted_vol[0], sorted_vol[1], counter_volume);
    plot($('#total_farmers_graph'), sorted_farmer[0], sorted_farmer[1], counter_farmer);
    plot($('#cpk_graph'), sorted_cpk[0], sorted_cpk[1], counter_cost);

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
    plot($('#total_volume_graph'), sorted_vol[0], sorted_vol[1], counter_volume);
    plot($('#cpk_graph'), sorted_cpk[0], sorted_cpk[1], counter_cost);

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
    plot($('#total_volume_graph'), sorted_vol[0], sorted_vol[1], counter_volume);
    plot($('#cpk_graph'), sorted_cpk[0], sorted_cpk[1], counter_cost);

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

function plot(id, x_axis, data, counter) {
    var series = [];
    var temp_series = {};
    temp_series['name'] = "Volume";
    temp_series['type'] = "bar";
    temp_series['showInLegend'] = false;
    temp_series['data'] = data.slice(counter, counter + 5);
    // temp_series['pointPadding']=0;
    // temp_series['groupPadding']=0.1;

    series.push(temp_series);
    plot_stacked_chart(id, x_axis.slice(counter, counter + 5), series);
}

function farmer_count_aggregator_wise() {
    $.get("/loop/farmer_count_aggregator_wise/").done(function(data) {
        var json_data = JSON.parse(data);

        aggregator_farmers = new Array(aggregators_details.length).fill(0);
        for (var i = 0; i < json_data['farmers_count'].length; i++) {
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
            update_graphs();
            transport_cost_graph($('#mandi_cost'), mandi_ids, mandi_names, aggregator_ids, aggregator_names, aggregator_graphs_json_data.transportation_cost_mandi);
            cpk_spk_graph(mandi_ids, mandi_names, aggregator_ids, aggregator_names, aggregator_graphs_json_data);
        });
}

function aggregator_graph(container, axis, axis_names, axis_parameter, values, values_names, json_data, parameter) {
    var series = [];
    var x_axis = new Array(axis.length);

    for (var i = 0; i < axis.length; i++) {
        x_axis[i] = axis_names[i];
    }

    for (var i = 0; i < values.length; i++) {
        var temp_vol = {};
        temp_vol['name'] = values_names[i];
        temp_vol['type'] = "bar";
        temp_vol['stacking'] = "normal";
        temp_vol['data'] = new Array(axis.length).fill(0.0);
        temp_vol['showInLegend'] = false;

        series.push(temp_vol);
    }
    for (var i = 0; i < json_data.length; i++) {
        var agg_index = values.indexOf(json_data[i]['user_created__id'].toString());
        var index = axis.indexOf(json_data[i][axis_parameter].toString());

        series[agg_index]['data'][index] = json_data[i][parameter];
    }

    plot_stacked_chart(container, x_axis, series, '', 'kg');
}

function transport_cost_graph(container, mandi_ids, mandi_names, aggregator_ids, aggregator_names, json_data) {
    var series = [];
    var mandis = new Array(mandi_ids.length);
    for (var i = 0; i < mandi_ids.length; i++) {
        mandis[i] = mandi_names[i];
    }

    for (var i = 0; i < aggregator_names.length; i++) {
        var temp_cost = {};
        temp_cost['name'] = aggregator_names[i];
        temp_cost['type'] = "bar";
        temp_cost['stacking'] = "normal";
        temp_cost['showInLegend'] = false;
        temp_cost['data'] = new Array(mandi_ids.length).fill(0);
        series.push(temp_cost);
    }
    for (var i = 0; i < json_data.length; i++) {
        var agg_index = aggregator_ids.indexOf(json_data[i]['user_created__id'].toString());
        var index = mandi_ids.indexOf(json_data[i]['mandi__id'].toString());

        series[agg_index]['data'][index] = json_data[i]['transportation_cost__sum'] - json_data[i]['farmer_share__sum'];
    }
    plot_stacked_chart(container, mandis, series, '', 'Rs');
}

function cpk_spk_graph(mandi_ids, mandi_names, aggregator_ids, aggregator_names, json_data) {
    var vol_stats = json_data.aggregator_mandi;
    var cost_stats = json_data.transportation_cost_mandi;
    var series_cpk = [];
    var series_spk = [];
    var mandis = new Array(mandi_ids.length);
    for (var i = 0; i < mandi_ids.length; i++) {
        mandis[i] = mandi_names[i];
    }
    mandi_vol = [];
    mandi_cost_cpk = [];
    mandi_cost_spk = [];
    for (var i = 0; i < aggregator_names.length; i++) {
        var temp = {};
        var temp_spk = {};
        temp['name'] = aggregator_names[i];
        temp['type'] = "bar";
        temp['stacking'] = "normal";
        temp['showInLegend'] = false;
        temp['data'] = new Array(mandi_ids.length).fill(0.0);

        temp_spk['name'] = aggregator_names[i];
        temp_spk['type'] = "bar";
        temp_spk['stacking'] = "normal";
        temp_spk['showInLegend'] = false;
        temp_spk['data'] = new Array(mandi_ids.length).fill(0.0);

        series_cpk.push(temp);
        series_spk.push(temp_spk);
        mandi_vol.push(new Array(mandi_ids.length).fill(0.0));
        mandi_cost_cpk.push(new Array(mandi_ids.length).fill(0.0));
        mandi_cost_spk.push(new Array(mandi_ids.length).fill(0.0));
    }

    for (var i = 0; i < vol_stats.length; i++) {
        var agg_index = aggregator_ids.indexOf(vol_stats[i]['user_created__id'].toString());
        var index = mandi_ids.indexOf(vol_stats[i]['mandi__id'].toString());
        mandi_vol[agg_index][index] = vol_stats[i]['quantity__sum'];
    }
    console.log(mandi_vol);
    for (var i = 0; i < cost_stats.length; i++) {
        var agg_index = aggregator_ids.indexOf(cost_stats[i]['user_created__id'].toString());
        var index = mandi_ids.indexOf(cost_stats[i]['mandi__id'].toString());
        mandi_cost_cpk[agg_index][index] = cost_stats[i]['transportation_cost__sum'] - cost_stats[i]['farmer_share__sum'];
        mandi_cost_spk[agg_index][index] = cost_stats[i]['farmer_share__sum'];
          }
          console.log(mandi_cost_cpk);


    for (var i = 0; i < aggregator_names.length; i++) {
        for (var j = 0; j < mandi_names.length; j++) {
            // console.log("vol" + mandi_vol[i][j]);
            // console.log("cost" + mandi_cost_cpk[i][j]);
            series_cpk[i]['data'][j] = mandi_vol[i][j] > 0 ? mandi_cost_cpk[i][j] / mandi_vol[i][j] : 0.0;
            series_spk[i]['data'][j] = mandi_vol[i][j] > 0 ? mandi_cost_spk[i][j] / mandi_vol[i][j] : 0.0;
            //      series_spk[i]['data'][j]=(mandi_cost_spk[i][j]/mandi_vol[i][j]);
        }
    }
    // console.log(series_cpk);
     plot_stacked_chart($('#cpk'), mandis, series_cpk, '', 'Rs');
     plot_stacked_chart($('#spk'), mandis, series_spk, '', 'Rs');
}

/* This file should contain all the JS for Loop dashboard */
window.onload = initialize;

function initialize() {
    // initialize any library here
    $("select").material_select();
    $(".button-collapse").sideNav({
        closeOnClick: true
    });
    $(".button-collapse1").sideNav();

    var today = new Date();
    $("#to_date").val(today.getFullYear() + "-" + (today.getMonth() + 1) + "-" + today.getDate());
    today.setMonth(today.getMonth() - 3);
    $("#from_date").val(today.getFullYear() + "-" + (today.getMonth() + 1) + "-" + today.getDate());

    hide_nav('home');

    total_static_data();
    recent_graphs_data();
    days_to_average = 15;

    gaddidar = true;
    selected_tab = "aggregator";

    time_series_frequency = 1;

    get_filter_data();
    set_filterlistener();
    $('#aggregator_payment_tab').hide();
    $("#download_payment_sheets").hide();

}

//datepicker
$('.datepicker').pickadate({
    selectMonths: true, // Creates a dropdown to control month
    selectYears: 15, // Creates a dropdown of 15 years to control year
    format: 'yyyy-mm-dd',
    max: true,
    onSet: function(element) {
        if (element.select) {
            this.close();
        }
    }
});

//To hide the second navigation bar that comes on analytics and time series page only
function hide_nav(tab) {
    $("#filters_nav").hide();
    $("#home_div").hide();
    $("#analytics_div").hide();
    $("#time_series_div").hide();
    $("#payments_div").hide();

    $("#home_tab").removeClass('active');
    $("#payments_tab").removeClass('active');
    $("#analytics_tab").removeClass('active');
    $("#time_series_tab").removeClass('active');

    if (tab == 'home') {
        $("#home_div").show();
        $("#home_tab").addClass('active');
    } else if (tab == 'payments') {
        $("#payments_div").show();
        $("#payments_tab").addClass('active');
    }
}

//To show the second navigation bar that comes on analytics and time series page only
function show_nav(tab) {
    $("#home_tab").removeClass('active');
    $("#payments_tab").removeClass('active');
    $("#analytics_tab").removeClass('active');
    $("#time_series_tab").removeClass('active');
    $("#filters_nav").show();
    $("#home_div").hide();
    $("#payments_div").hide();

    if (tab == "analytics") {
        $("#analytics_div").show();
        $("#time_series_div").hide();
        $(".analytics_tabs").show();
        $("#analytics_tab").addClass('active');
    } else if (tab == "time_series") {
        $("#analytics_div").hide();
        $("#time_series_div").show();
        $(".analytics_tabs").hide();
        $("#time_series_tab").addClass('active');
    }
}

// function clear_payment_table(){
//   $("#table2_wrapper").hide();
// }

bullet_options = {
    type: "bullet",
    width: "100",
    height: "30",
    performanceColor: '#00bfbf',
    rangeColors: ['#a2d6d6'],
    targetColor: '#ffffff',
};

sparkline_option = {
    type: 'line',
    width: '100',
    height: '40',
    lineColor: '#00bfbf',
    fillColor: '#dde1df',
    lineWidth: 2
};


//To compute data for home page overall cards
function total_static_data() {
    $.get("/loop/total_static_data/", {}).done(function(data) {
        var json_data = JSON.parse(data);

        var total_volume = json_data['total_volume']['quantity__sum'];

        var total_amount = json_data['total_volume']['amount__sum'];

        var total_farmers_reached = json_data['total_farmers_reached'];
        var total_repeat_farmers = json_data['total_repeat_farmers']

        var total_transportation_cost = 0;
        var total_farmer_share = 0;

        for (var i = 0; i < json_data['total_transportation_cost'].length; i++) {
            total_transportation_cost += json_data['total_transportation_cost'][i]['transportation_cost__sum'];
            total_farmer_share += json_data['total_transportation_cost'][i]['farmer_share__sum'];
        }

        var total_expenditure = total_transportation_cost - total_farmer_share;
        var total_volume_for_transport = json_data['total_volume_for_transport']['quantity__sum'];

        var sustainability = total_farmer_share / total_transportation_cost * 100;

        var clusters = json_data['total_cluster_reached'];

        var total_cpk = total_transportation_cost / total_volume_for_transport;

        var kg = "Kg";
        var rs = "₹";

        // document.getElementById('cluster_card').innerHTML = clusters;
        plot_solid_guage($('#cluster_bullet'), clusters, 35);
        // $('#cluster_bullet').sparkline([30, clusters, 50], bullet_options);

        // document.getElementById('total_farmers_card').innerHTML = total_farmers_reached + " <sub style='font-size: 12px'>" + parseFloat((total_repeat_farmers / total_farmers_reached) * 100).toFixed(2) + "%" + "</sub>";
        plot_solid_guage($('#total_farmers_bullet'), total_farmers_reached, 2000);
        // $('#total_farmers_bullet').sparkline([1500, total_farmers_reached, 5000], bullet_options);

        // document.getElementById('total_volume_card').innerHTML = parseFloat(total_volume).toFixed(0).concat(kg);
        plot_solid_guage($('#total_volume_bullet'), parseInt(total_volume), 5500000);
        // $('#total_volume_bullet').sparkline([1000000, total_volume, 1500000], bullet_options);

        // document.getElementById('revenue_card').innerHTML = rs.concat(parseFloat(total_amount).toFixed(0));
        plot_solid_guage($('#revenue_bullet'), parseInt(total_amount), 27000000);
        // $('#revenue_bullet').sparkline([10000000, total_amount, 15000000], bullet_options);

        // document.getElementById('total_expenditure_card').innerHTML = parseFloat(total_cpk).toFixed(2); //rs.concat(parseFloat(total_transportation_cost).toFixed(2) - parseFloat(total_farmer_share).toFixed(2));
        plot_solid_guage($('#total_expenditure_bullet'), parseFloat(total_cpk.toFixed(2)), 0.4);

        // document.getElementById('sustainability_card').innerHTML = parseFloat(sustainability).toFixed(2).concat(" %");
        plot_solid_guage($('#sustainability_bullet'), parseFloat(sustainability.toFixed(2)), 60);
    })
}


//To request data for recent graphs on home page
function recent_graphs_data() {
    $.get("/loop/recent_graphs_data/", {}).done(function(data) {
        json_data = JSON.parse(data);

        dates = json_data['dates'];
        aggregators_details = json_data.aggregators;
        mandis = json_data['mandis'];
        stats = json_data['stats'];
        transportation = json_data['transportation_cost'];
        crops = json_data['crops'];

        plot_cards_data();

        cummulative_farmer_and_volume();
    });
}


//To plot and show data for recents graphs on home page
function plot_cards_data() {
    var avg = get_average(); // Retunts [avg_volume, active_farmers, avg_amount]
    var avg_vol = avg[0];
    var kg = "Kg";
    var rs = "₹";

    var active_clusters = avg[3];
    document.getElementById('recent_cluster_card').innerHTML = active_clusters[0];
    $("#recent_cluster_sparkline").sparkline(active_clusters.reverse(), sparkline_option);

    document.getElementById('recent_volume_card').innerHTML = (avg_vol[0]).toFixed(0).concat(kg);
    $('#recent_volume_sparkline').sparkline(avg_vol.reverse(), sparkline_option);

    var active_farmers = avg[1];
    document.getElementById('recent_active_farmers_card').innerHTML = active_farmers[0];
    $('#recent_active_farmers_sparkline').sparkline(active_farmers.reverse(), sparkline_option);

    var avg_amt = avg[2];
    document.getElementById('recent_revenue_card').innerHTML = rs.concat((avg_amt[0]).toFixed(0));
    $('#recent_revenue_sparkline').sparkline(avg_amt.reverse(), sparkline_option);

    var data = get_cpk(avg_vol.reverse());
    var cpk = data[0];
    document.getElementById('cpk_card').innerHTML = rs.concat(parseFloat(cpk[0]).toFixed(2));
    $('#cpk_sparkline').sparkline(cpk.reverse(), sparkline_option);

    var sustainability = data[1];
    document.getElementById('recent_sustainability_card').innerHTML = parseFloat(sustainability[0]).toFixed(2) + "%";
    $('#recent_sustainability_sparkline').sparkline(sustainability.reverse(), sparkline_option);
}


//Helper function to calculate average for 7,15,30,60 days for above function
function get_average() {

    var today = new Date();

    today.setDate(today.getDate() - days_to_average);

    var avg_vol = [];

    var avg_amt = [];

    var active_farmers = [];
    var active_farmers_id = [];
    var active_clusters = [];
    var active_clusters_id = [];

    var j = 0,
        temp_vol = 0,
        temp_amt = 0;
    //If no data is present for a period of days_to_average initially
    while (today >= new Date(stats[j]['date'])) {
        avg_vol.push(0);
        avg_amt.push(0);
        active_farmers.push(0);
        active_clusters.push(0);
        today.setDate(today.getDate() - days_to_average);
    }

    var stats_length = stats.length;
    while (j < stats_length && today < new Date(stats[j]['date'])) {
        temp_vol += stats[j]['quantity__sum'];
        temp_amt += stats[j]['amount__sum'];

        var farmer_id = stats[j]['farmer__id'];
        if (active_farmers_id.indexOf(farmer_id) == -1) {
            active_farmers_id.push(farmer_id);
        }
        var cluster_id = stats[j]['user_created__id'];
        if (active_clusters_id.indexOf(cluster_id) == -1) {
            active_clusters_id.push(cluster_id);
        }
        j++;
        if (j < stats_length && today >= new Date(stats[j]['date'])) {
            avg_vol.push(temp_vol);
            avg_amt.push(temp_amt);
            temp_vol = 0;
            temp_amt = 0;

            active_farmers.push(active_farmers_id.length);
            active_farmers_id = [];

            active_clusters.push(active_clusters_id.length);
            active_clusters_id = [];

            today.setDate(today.getDate() - days_to_average);

            //If no data is present for a period of days_to_average
            while (today >= new Date(stats[j]['date'])) {
                avg_vol.push(0);
                avg_amt.push(0);
                active_farmers.push(0);
                active_clusters.push(0);
                today.setDate(today.getDate() - days_to_average);
            }
        }
    }

    avg_vol.push(temp_vol);
    avg_amt.push(temp_amt);
    active_farmers.push(active_farmers_id.length);
    active_clusters.push(active_clusters_id.length);

    return [avg_vol, active_farmers, avg_amt, active_clusters];
}


//Helper function to calculate average cpk for 7,15,30,60 days for above function
function get_cpk(avg_vol) {

    var today = new Date();
    today.setDate(today.getDate() - days_to_average);

    var cpk = [];
    var sustainability_per_kg = [];

    var j = 0, // To loop through transportation details
        temp = 0,
        k = 0, // keeping note of position in avg_vol
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
            if (avg_vol[k] == 0) {
                cpk.push(0);
                sustainability_per_kg.push(0);
            } else {
                cpk.push(temp / avg_vol[k]);
                sustainability_per_kg.push(f_share / temp * 100);
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

    if (avg_vol[k] == 0) {
        cpk.push(0);
        sustainability_per_kg.push(0);
    } else {
        cpk.push(temp / avg_vol[k]);
        sustainability_per_kg.push(f_share / temp * 100);
    }

    //Adding 0 cost for previous data making length of both arrays same
    for (var i = cpk.length; i < avg_vol.length; i++) {
        cpk.push(0);
        sustainability_per_kg.push(0);
    }
    return [cpk, sustainability_per_kg];
}


//To show cummulative farmer and volume graph present on Home page
function cummulative_farmer_and_volume() {

    var all_dates = [];
    var farmer_ids = []

    var first_date = new Date(dates[dates.length - 1]);
    while (first_date <= new Date(dates[0])) {
        all_dates.push(first_date.getTime());
        first_date.setDate(first_date.getDate() + 1)
    }

    var cumm_volume = new Array(all_dates.length).fill(0.0);
    var cumm_farmers = new Array(all_dates.length).fill(0.0);
    var temp_volume = {}
    temp_volume['name'] = "volume";
    temp_volume['data'] = [];
    temp_volume['type'] = 'spline';
    temp_volume['pointInterval'] = 24 * 3600 * 1000;
    temp_volume['pointStart'] = all_dates[all_dates.length - 1]; // Pointing to the starting date
    temp_volume['showInLegend'] = true;
    var temp_farmers = {}
    temp_farmers['name'] = "farmers";
    temp_farmers['data'] = [];
    temp_farmers['type'] = 'spline';
    temp_farmers['pointInterval'] = 24 * 3600 * 1000;
    temp_farmers['pointStart'] = all_dates[all_dates.length - 1]; // Pointing to the starting date
    temp_farmers['showInLegend'] = true;

    var stats_length = stats.length;
    for (var i = stats_length - 1; i >= 0; i--) {
        var index = all_dates.indexOf(new Date(stats[i]['date']).getTime());
        if (farmer_ids.indexOf(stats[i]['farmer__id']) == -1) {
            farmer_ids.push(stats[i]['farmer__id']);
            cumm_farmers[index] += 1;

        }
        cumm_volume[index] += stats[i]['quantity__sum'];
    }

    temp_volume['data'].push([all_dates[0], cumm_volume[0]]);
    temp_farmers['data'].push([all_dates[0], cumm_farmers[0]]);

    for (var i = 1; i < cumm_volume.length; i++) {
        cumm_volume[i] += cumm_volume[i - 1];
        cumm_farmers[i] += cumm_farmers[i - 1];
        temp_volume['data'].push([all_dates[i], cumm_volume[i]]);
        temp_farmers['data'].push([all_dates[i], cumm_farmers[i]]);
    }

    var series = [];
    series.push(temp_volume);
    series.push(temp_farmers);

    createMaster($('#detail_container'), $('#master_container'), series);
}


//Helper function to change class of tabs present on navigation bar
function change_tab(tab) {
    selected_tab = tab;
    $('#aggregator_tab').removeClass('active');
    $('#mandi_tab').removeClass('active');
    $('#crop_tab').removeClass('active');
    change_graph();
}

//To change graphs on analytics page (Aggregator, Mandi, Crop)
function change_graph(parameter) {

    $("#aggregator_visits").removeClass("active");
    $("#aggregator_amount").removeClass("active");
    $("#aggregator_volume").addClass("active");
    $('ul.tabs').tabs();

    $("#aggregator_visits").show();
    $("#cpk_cost").show();
    $("#crop_prices_min_max").hide();
    $("#gaddidar_aggregator_graph").hide();
    $("#aggregator_farmer_count").show();
    if (selected_tab == "aggregator") {
        $('#aggregator_tab').addClass('active');
        update_graphs_aggregator_wise(parameter);
    }
    if (selected_tab == "mandi") {
        $('#mandi_tab').addClass('active');
        $("#gaddidar_aggregator_graph").show();
        $("#aggregator_farmer_count").hide();
        update_graphs_mandi_wise(parameter);
        if (gaddidar) {
            update_graphs_gaddidar_wise(parameter);
            gaddidar = false;
        }

    }
    if (selected_tab == "crop") {
        $('#crop_tab').addClass('active');
        $("#aggregator_visits").hide();
        $("#cpk_cost").hide();
        $("#crop_prices_min_max").show();
        update_graphs_crop_wise(parameter);
    }
}

//To check for any items data change (textview, drop downs)
function set_filterlistener() {
    $("#recent_cards_data_frequency").change(function() {
        days_to_average = $('#recent_cards_data_frequency :selected').val()
        plot_cards_data();
    });

    $('#get_data').click(function() {
        get_data();
    });

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

    // For graphs in time series
    $("#crop_max_min_avg").change(function() {
        var crop_id = $('#crop_max_min_avg :selected').val()
        crop_prices_graph(crop_id);
    });

    $("#aggregator_payments").change(function() {
        var aggregator_id = $('#aggregator_payments :selected').val();
        if (table_created) {
            // outliers_table.clear().destroy();
            $('#outliers_data').html("");
        }
        aggregator_payment_sheet(payments_data.aggregator_data, aggregator_id);
        // $("#table2_wrapper").show();
        $("#download_payment_sheets").show();
        outliers_summary(aggregator_id);
    });

    // $("#transporter_payments").change(function() {
    //     var transporter_id = $('#transporter_payments :selected').val()
    //     transporter_payment_sheet(payments_data.transportation_data, transporter_id);
    //     // $("#table2_wrapper").show();
    // });
    // $("#gaddidar_payments").change(function() {
    //     var gaddidar_id = $('#gaddidar_payments :selected').val()
    //     gaddidar_payment_sheet(payments_data.gaddidar_data, gaddidar_id);
    //     // $("#table2_wrapper").show();
    // });

    $("#time_series_frequency").change(function() {
        time_series_frequency = $('#time_series_frequency :selected').val()
        if (time_series_frequency == 1) {
            createMaster1($('#detail_container_time_series'), $('#master_container_time_series'), time_series_volume_amount_farmers);
            createMaster2($('#detail_container_cpk'), $('#master_container_cpk'), time_series_cpk_spk);
        } else {
            createMaster1($('#detail_container_time_series'), $('#master_container_time_series'), get_frequency_data(start_date, end_date, time_series_volume_amount_farmers, time_series_frequency, false));
            createMaster2($('#detail_container_cpk'), $('#master_container_cpk'), get_frequency_cpk(start_date, end_date, time_series_cpk_spk, time_series_frequency, false));
        }
    });

}


//To make a call when filters are changed
function get_filter_data() {
    $.get("/loop/filter_data/", {})
        .done(function(data) {
            var data_json = JSON.parse(data);
            aggregators_for_filter = data_json.aggregators;
            mandis_for_filter = data_json.mandis;
            gaddidars_for_filter = data_json.gaddidars;
            crops_for_filter = data_json.crops;
            transporter_for_filter = data_json.transporters;
            fill_aggregator_filter(aggregators_for_filter);
            fill_crop_filter(crops_for_filter);
            fill_mandi_filter(mandis_for_filter);
            fill_gaddidar_filter(gaddidars_for_filter);
            get_data();
        });
}


//To make aggregators list for filter page
function fill_aggregator_filter(data_json) {
    $.each(data_json, function(index, data) {
        create_filter($('#aggregators'), data.user__id, data.name, true);
    });
}

//To make crops list for filter page
function fill_crop_filter(data_json) {
    $.each(data_json, function(index, data) {
        create_filter($('#crops'), data.id, data.crop_name, true);
    });
}

//To make mandis list for filter page
function fill_mandi_filter(data_json) {
    $.each(data_json, function(index, data) {
        create_filter($('#mandis'), data.id, data.mandi_name, true);
    });
}

//To make gaddidars list for filter page
function fill_gaddidar_filter(data_json) {
    $.each(data_json, function(index, data) {
        create_filter($('#gaddidars'), data.id, data.gaddidar_name, true);
    });
}

//To enter data for aggregator, mandi,crop,gaddidar filter dynamically
function create_filter(tbody_obj, id, name, checked) {
    var row = $('<tr>');
    var td_name = $('<td>').html(name);
    row.append(td_name);
    var checkbox_html = '<input type="checkbox" class="black" data=' + id + ' id="' + name + id + '" checked="checked" value = ' + name + ' /><label for="' + name + id + '"></label>';
    var td_checkbox = $('<td>').html(checkbox_html);
    row.append(td_checkbox);
    tbody_obj.append(row);
}

//To get data after filters are aplied
function get_data() {
    start_date = $('#from_date').val();
    end_date = $('#to_date').val();
    // Get rest of the filters
    aggregator_ids = [];
    aggregator_names = [];
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
        get_data_for_bar_graphs(start_date, end_date, aggregator_ids, crop_ids, mandi_ids, gaddidar_ids);
        get_data_for_line_graphs(start_date, end_date, aggregator_ids, crop_ids, mandi_ids, gaddidar_ids);
        // genterate_payment_sheet(start_date, end_date);
    }
}

function get_data_for_bar_graphs(start_date, end_date, aggregator_ids, crop_ids, mandi_ids, gaddidar_ids) {
    $.get("/loop/new_aggregator_wise_data/", {
            'start_date': start_date,
            'end_date': end_date,
            'aggregator_ids[]': aggregator_ids,
            'crop_ids[]': crop_ids,
            'mandi_ids[]': mandi_ids,
            'gaddidar_ids[]': gaddidar_ids
        })
        .done(function(data) {
            bar_graphs_json_data = JSON.parse(data);
            totals();
            change_graph();
        });
}


function update_graphs_aggregator_wise(chart) {
    if (chart == null) {
        $('#1stgraph').text("Aggregator Wise");
        aggregator_graph($('#aggregator_mandi'), aggregator_ids, aggregator_names, 'user_created__id', mandi_ids, mandi_names, 'mandi__id', bar_graphs_json_data.aggregator_mandi, "quantity__sum");
        $('#2ndgraph').text("Cost per kg");
        cpk_spk_graph($('#mandi_cost'), aggregator_ids, aggregator_names, 'user_created__id', mandi_ids, mandi_names, 'mandi__id', bar_graphs_json_data);
        repeat_farmers($('#farmers_count'), aggregator_ids, aggregator_names, 'user_created__id', mandi_ids, mandi_names, 'mandi__id', bar_graphs_json_data.total_repeat_farmers);
    } else {

        if (chart == "volume") {
            aggregator_graph($('#aggregator_mandi'), aggregator_ids, aggregator_names, 'user_created__id', mandi_ids, mandi_names, 'mandi__id', bar_graphs_json_data.aggregator_mandi, "quantity__sum");

        } else if (chart == "amount") {
            aggregator_graph($('#aggregator_mandi'), aggregator_ids, aggregator_names, 'user_created__id', mandi_ids, mandi_names, 'mandi__id', bar_graphs_json_data.aggregator_mandi, "amount__sum");

        } else if (chart == "visits") {
            aggregator_graph($('#aggregator_mandi'), aggregator_ids, aggregator_names, 'user_created__id', mandi_ids, mandi_names, 'mandi__id', bar_graphs_json_data.aggregator_mandi, "mandi__id__count");
        }

        if (chart == "cost_recovered") {
            $('#2ndgraph').text("Total Cost")
            transport_cost_graph($('#mandi_cost'), aggregator_ids, aggregator_names, 'user_created__id', mandi_ids, mandi_names, 'mandi__id', bar_graphs_json_data.transportation_cost_mandi);
        } else if (chart == "cpk_spk") {
            $('#2ndgraph').text("Cost per kg")
            cpk_spk_graph($('#mandi_cost'), aggregator_ids, aggregator_names, 'user_created__id', mandi_ids, mandi_names, 'mandi__id', bar_graphs_json_data);
        }
    }
}

function update_graphs_mandi_wise(chart) {
    if (chart == null) {
        aggregator_graph($('#aggregator_mandi'), mandi_ids, mandi_names, 'mandi__id', gaddidar_ids, gaddidar_names, 'gaddidar__id', bar_graphs_json_data.mandi_gaddidar, "quantity__sum");
        cpk_spk_graph($('#mandi_cost'), mandi_ids, mandi_names, 'mandi__id', aggregator_ids, aggregator_names, 'user_created__id', bar_graphs_json_data);
    } else {

        if (chart == "volume") {
            aggregator_graph($('#aggregator_mandi'), mandi_ids, mandi_names, 'mandi__id', gaddidar_ids, gaddidar_names, 'gaddidar__id', bar_graphs_json_data.mandi_gaddidar, "quantity__sum");

        } else if (chart == "amount") {
            aggregator_graph($('#aggregator_mandi'), mandi_ids, mandi_names, 'mandi__id', gaddidar_ids, gaddidar_names, 'gaddidar__id', bar_graphs_json_data.mandi_gaddidar, "amount__sum");

        } else if (chart == "visits") {
            aggregator_graph($('#aggregator_mandi'), mandi_ids, mandi_names, 'mandi__id', aggregator_ids, aggregator_names, 'user_created__id', bar_graphs_json_data.aggregator_mandi, "mandi__id__count");
        }

        if (chart == "cost_recovered") {
            transport_cost_graph($('#mandi_cost'), mandi_ids, mandi_names, 'mandi__id', aggregator_ids, aggregator_names, 'user_created__id', bar_graphs_json_data.transportation_cost_mandi);
        } else if (chart == "cpk_spk") {
            cpk_spk_graph($('#mandi_cost'), mandi_ids, mandi_names, 'mandi__id', aggregator_ids, aggregator_names, 'user_created__id', bar_graphs_json_data);
        }
    }
}

function update_graphs_gaddidar_wise(chart) {
    if (chart == null) {
        aggregator_graph($('#aggregator_gaddidar'), gaddidar_ids, gaddidar_names, 'gaddidar__id', aggregator_ids, aggregator_names, 'user_created__id', bar_graphs_json_data.aggregator_gaddidar, "quantity__sum");
        // cpk_spk_graph($('#mandi_cost'), mandi_ids, mandi_names, 'mandi__id', aggregator_ids, aggregator_names, 'user_created__id', bar_graphs_json_data);
    } else {
        if (chart == "volume") {
            aggregator_graph($('#aggregator_gaddidar'), gaddidar_ids, gaddidar_names, 'gaddidar__id', aggregator_ids, aggregator_names, 'user_created__id', bar_graphs_json_data.aggregator_gaddidar, "quantity__sum");

        } else if (chart == "amount") {
            aggregator_graph($('#aggregator_gaddidar'), gaddidar_ids, gaddidar_names, 'gaddidar__id', aggregator_ids, aggregator_names, 'user_created__id', bar_graphs_json_data.aggregator_gaddidar, "amount__sum");

        }

        // if (chart=="cost_recovered"){
        //     $('#2ndgraph').text("Total Cost")
        //     transport_cost_graph($('#mandi_cost'),  mandi_ids, mandi_names, 'mandi__id', aggregator_ids, aggregator_names, 'user_created__id', bar_graphs_json_data.transportation_cost_mandi);
        // }else if(chart == "cpk_spk"){
        //     $('#2ndgraph').text("Cost per kg")
        //     cpk_spk_graph($('#mandi_cost'), mandi_ids, mandi_names, 'mandi__id', aggregator_ids, aggregator_names, 'user_created__id', bar_graphs_json_data);
        // }
    }
}

function update_graphs_crop_wise(chart) {

    if (chart == null) {
        aggregator_graph($('#aggregator_mandi'), crop_ids, crop_names, 'crop__id', mandi_ids, mandi_names, 'mandi__id', bar_graphs_json_data.mandi_crop, "quantity__sum");
        max_min_graph($('#mandi_cost'), bar_graphs_json_data.crop_prices)
        farmer_crop_visits($("#farmers_count"), bar_graphs_json_data.crop_prices)

    } else {

        if (chart == "volume") {
            aggregator_graph($('#aggregator_mandi'), crop_ids, crop_names, 'crop__id', mandi_ids, mandi_names, 'mandi__id', bar_graphs_json_data.mandi_crop, "quantity__sum");

        } else if (chart == "amount") {
            aggregator_graph($('#aggregator_mandi'), crop_ids, crop_names, 'crop__id', mandi_ids, mandi_names, 'mandi__id', bar_graphs_json_data.mandi_crop, "amount__sum");
        }
    }
}

function totals() {
    var total_volume = 0;
    var total_amount = 0;
    var total_visits = 0;
    var total_cost = 0;
    var total_recovered = 0;
    var volume_amount_visits_data = bar_graphs_json_data.aggregator_mandi;
    var transport_data = bar_graphs_json_data.transportation_cost_mandi;

    for (var i = 0; i < volume_amount_visits_data.length; i++) {
        total_volume += volume_amount_visits_data[i]["quantity__sum"];
        total_amount += volume_amount_visits_data[i]["amount__sum"];
        total_visits += volume_amount_visits_data[i]["mandi__id__count"];
    }

    for (var i = 0; i < transport_data.length; i++) {
        total_cost += transport_data[i]['transportation_cost__sum']
        total_recovered += transport_data[i]['farmer_share__sum'];
    }

    var cpk = (total_cost / total_volume).toFixed(2);
    var spk = (total_recovered / total_volume).toFixed(2);

    $("#aggregator_volume").text("Volume: " + parseFloat(total_volume).toFixed(2));
    $("#aggregator_amount").text("amount: " + parseFloat(total_amount).toFixed(2));
    $("#aggregator_visits").text("visits: " + total_visits);
    $("#aggregator_cpk").text("SPK:CPK :: " + spk + ":" + cpk);
    $("#aggregator_cost").text("Recovered:Total :: " + total_recovered + ":" + total_cost);

}

//Volume, Amount, Visits graph on analytics page is being plotted from this
function aggregator_graph(container, axis, axis_names, axis_parameter, values, values_names, values_parameter, json_data, parameter) {
    var series = [];
    var drilldown = {};

    drilldown['series'] = [];

    // These three values are to show at top

    var temp = {};
    temp['name'] = "Total";
    temp['type'] = "bar";
    temp['colorByPoint'] = false;
    temp['data'] = [];
    temp['pointWidth'] = 15;


    for (var i = 0; i < axis.length; i++) {
        temp['data'].push({
            'name': axis_names[i],
            'y': 0,
            'drilldown': axis_names[i]
        });
        drilldown['series'].push({
            'name': axis_names[i],
            'id': axis_names[i],
            'data': [],
            'type': 'bar',
            'xAxis': 1,
            'pointWidth': 15
        });
        for (var j = 0; j < values_names.length; j++) {
            drilldown['series'][i]['data'].push({
                "name": values_names[j],
                "y": 0
            });
        }
    }
    temp['showInLegend'] = false;
    series.push(temp);

    for (var i = 0; i < json_data.length; i++) {

        var drilldown_index = values.indexOf(json_data[i][values_parameter].toString());
        var index = axis.indexOf(json_data[i][axis_parameter].toString());

        drilldown['series'][index]['data'][drilldown_index]['y'] += json_data[i][parameter]

        series[0]['data'][index]['y'] += json_data[i][parameter];
    }

    series[0]['data'].sort(function(a, b) {
        return b['y'] - a['y'];
    });

    for (var i = 0; i < axis.length; i++) {
        drilldown['series'][i]['data'].sort(function(a, b) {
            return b['y'] - a['y']
        });
        for (var j = 0; drilldown['series'][i]['data'].length; j++) {
            if (drilldown['series'][i]['data'][j]['y'] == 0) {
                drilldown['series'][i]['data'] = drilldown['series'][i]['data'].slice(0, j);
                break;
            }
        }
    }


    plot_drilldown(container, series, drilldown, false);

}

//Recovered total graph on analytics page is being plotted from this
function transport_cost_graph(container, axis, axis_names, axis_parameter, values, values_names, values_parameter, json_data) {
    var series = [];
    var drilldown = {};
    drilldown['allowPointDrilldown'] = false;
    drilldown['series'] = [];
    var temp_cost = {};
    temp_cost['name'] = "Total Cost";
    temp_cost['type'] = "bar";
    temp_cost['showInLegend'] = false;
    temp_cost['data'] = [];
    temp_cost['pointWidth'] = 15;
    temp_cost['pointPlacement'] = 0;

    var temp_cost_recovered = {};
    temp_cost_recovered['name'] = "Cost Recovered";
    temp_cost_recovered['type'] = "bar";
    temp_cost_recovered['showInLegend'] = false;
    temp_cost_recovered['data'] = [];
    temp_cost_recovered['pointWidth'] = 15;
    temp_cost_recovered['pointPlacement'] = 0;

    series.push(temp_cost);
    series.push(temp_cost_recovered);

    var data_for_sorting = []
    for (var i = 0; i < axis.length; i++) {
        data_for_sorting.push({
            'name': axis_names[i],
            'cost': 0,
            'cost_recovered': 0
        })
        drilldown['series'].push({
            'name': axis_names[i],
            'id': axis_names[i] + "cpk",
            'data': []
        })
        drilldown['series'].push({
            'name': axis_names[i],
            'id': axis_names[i] + "spk",
            'data': []
        })
        for (var j = 0; j < values.length; j++) {
            drilldown['series'][i * 2]['data'].push([values_names[j], null]);
            drilldown['series'][i * 2 + 1]['data'].push([values_names[j], null]);
        }
    }

    var json_data_length = json_data.length;
    for (var i = 0; i < json_data_length; i++) {
        var index = axis.indexOf(json_data[i][axis_parameter].toString());
        var drilldown_index = values.indexOf(json_data[i][values_parameter].toString())
        drilldown['series'][index * 2]['data'][drilldown_index][1] += json_data[i]['transportation_cost__sum']
        drilldown['series'][index * 2 + 1]['data'][drilldown_index][1] += json_data[i]['farmer_share__sum']
        data_for_sorting[index]['cost'] += json_data[i]['transportation_cost__sum']
        data_for_sorting[index]['cost_recovered'] += json_data[i]['farmer_share__sum'];
    }

    data_for_sorting.sort(function(a, b) {
        return (b['cost']) - (a['cost']);
    });

    for (var i = 0; i < axis.length; i++) {
        series[0]['data'].push({
            'name': data_for_sorting[i]['name'],
            'y': data_for_sorting[i]['cost'],
            'drilldown': data_for_sorting[i]['name'] + "cpk"
        });
        series[1]['data'].push({
            'name': data_for_sorting[i]['name'],
            'y': data_for_sorting[i]['cost_recovered'],
            'drilldown': data_for_sorting[i]['name'] + "spk"
        });
    }

    for (var i = 0; i < drilldown['series'].length; i++) {
        drilldown['series'][i]['data'].sort(function(a, b) {
            return b[1] - a[1]
        });

    }

    plot_drilldown(container, series, drilldown, false);
}

//Cpk and Spk on analytics page is being plotted from this
function cpk_spk_graph(container, axis, axis_names, axis_parameter, values, values_names, values_parameter, json_data) {
    var vol_stats = json_data.aggregator_mandi;
    var cost_stats = json_data.transportation_cost_mandi;
    var series = [];
    var drilldown = {};
    drilldown['allowPointDrilldown'] = false;
    drilldown['series'] = [];

    var values_vol = new Array(axis.length).fill(0.0);
    var values_vol_drilldown = [];

    var values_cost_cpk = new Array(axis.length).fill(0.0);
    var values_cost_cpk_drilldown = [];
    var values_cost_spk = new Array(axis.length).fill(0.0);
    var values_cost_spk_drilldown = [];
    var temp_cpk = {};
    var temp_spk = {};
    temp_cpk['name'] = 'cpk';
    temp_cpk['type'] = "bar";
    temp_cpk['showInLegend'] = false;
    temp_cpk['data'] = [];
    temp_cpk['pointWidth'] = 15;
    temp_cpk['pointPlacement'] = 0;


    temp_spk['name'] = 'spk';
    temp_spk['type'] = "bar";
    temp_spk['showInLegend'] = false;
    temp_spk['data'] = [];
    temp_spk['pointWidth'] = 15;
    temp_spk['pointPlacement'] = 0;

    series.push(temp_cpk);
    series.push(temp_spk);

    for (var i = 0; i < axis.length; i++) {
        values_vol_drilldown.push(new Array(values.length).fill(null));
        values_cost_cpk_drilldown.push(new Array(values.length).fill(null));
        values_cost_spk_drilldown.push(new Array(values.length).fill(null));

    }

    for (var i = 0; i < vol_stats.length; i++) {
        var index = axis.indexOf(vol_stats[i][axis_parameter].toString());
        var drilldown_index = values.indexOf(vol_stats[i][values_parameter].toString());
        values_vol[index] += vol_stats[i]['quantity__sum'];
        values_vol_drilldown[index][drilldown_index] += vol_stats[i]['quantity__sum'];
    }
    for (var i = 0; i < cost_stats.length; i++) {
        var index = axis.indexOf(cost_stats[i][axis_parameter].toString());
        var drilldown_index = values.indexOf(cost_stats[i][values_parameter].toString());
        values_cost_cpk[index] += cost_stats[i]['transportation_cost__sum'];
        values_cost_spk[index] += cost_stats[i]['farmer_share__sum'];
        values_cost_cpk_drilldown[index][drilldown_index] += cost_stats[i]['transportation_cost__sum'];
        values_cost_spk_drilldown[index][drilldown_index] += cost_stats[i]['farmer_share__sum'];

    }
    var data_for_sorting = []
    for (var i = 0; i < axis.length; i++) {
        data_for_sorting.push({
            'name': axis_names[i],
            'cpk': values_vol[i] > 0 ? values_cost_cpk[i] / values_vol[i] : 0.0,
            'spk': values_vol[i] > 0 ? values_cost_spk[i] / values_vol[i] : 0.0
        });
        drilldown['series'].push({
            'name': axis_names[i],
            'id': axis_names[i] + "cpk",
            'data': [],
            'xAxis': 1,
            'pointWidth': 15
        });
        drilldown['series'].push({
            'name': axis_names[i],
            'id': axis_names[i] + "spk",
            'data': [],
            'xAxis': 1,
            'pointWidth': 15
        });
        for (var j = 0; j < values.length; j++) {
            if (values_vol_drilldown[i][j] > 0) {
                drilldown['series'][i * 2]['data'].push([values_names[j], values_cost_cpk_drilldown[i][j] / values_vol_drilldown[i][j]]);
                drilldown['series'][i * 2 + 1]['data'].push([values_names[j], values_cost_spk_drilldown[i][j] / values_vol_drilldown[i][j]]);
            }
        }
    }

    data_for_sorting.sort(function(a, b) {
        return (b['cpk']) - (a['cpk']);
    });

    for (var i = 0; i < axis_names.length; i++) {
        series[0]['data'].push({
            'name': data_for_sorting[i]['name'],
            'y': data_for_sorting[i]['cpk'],
            'drilldown': data_for_sorting[i]['name'] + "cpk"
        });
        series[1]['data'].push({
            'name': data_for_sorting[i]['name'],
            'y': data_for_sorting[i]['spk'],
            'drilldown': data_for_sorting[i]['name'] + "spk"
        });
    }

    for (var i = 0; i < drilldown['series'].length; i++) {
        drilldown['series'][i]['data'].sort(function(a, b) {
            return b[1] - a[1]
        });
    }

    plot_drilldown(container, series, drilldown, true);
}

//Analytocs Aggregator tab to caluclate farmers count is being calculated from this
function repeat_farmers(container, axis, axis_names, axis_parameter, values, values_names, values_parameter, json_data) {
    var series = [];
    var drilldown = {};
    drilldown['series'] = [];

    var temp_total = {};
    temp_total['name'] = "Total Farmers";
    temp_total['type'] = "bar";
    temp_total['showInLegend'] = false;
    temp_total['data'] = [];
    temp_total['pointPadding'] = 0.3;
    temp_total['pointPlacement'] = 0;

    var temp_repeat = {};
    temp_repeat['name'] = "Total Repeat Farmers";
    temp_repeat['type'] = "bar";
    temp_repeat['showInLegend'] = false;
    temp_repeat['data'] = [];
    temp_repeat['pointPadding'] = 0.4;
    temp_repeat['pointPlacement'] = 0;

    var data_for_sorting = []

    for (var i = 0; i < axis.length; i++) {
        data_for_sorting.push({
            'name': axis_names[i],
            'total_farmers': 0,
            'total_repeat_farmers': 0
        })

        drilldown['series'].push({
            'name': axis_names[i],
            'id': axis_names[i],
            'data': []
        })
        for (var j = 1; j < 10; j++) {
            drilldown['series'][i]['data'].push(["" + j, null]);
        }
        drilldown['series'][i]['data'].push(["10+", null]);
    }
    series.push(temp_total);
    series.push(temp_repeat);
    var json_data_length = json_data.length;
    for (var i = 0; i < json_data_length; i++) {
        var index = axis.indexOf(json_data[i][axis_parameter].toString());
        var count = json_data[i]['farmer_count'];
        data_for_sorting[index]['total_farmers'] += 1;
        if (count > 1) {
            data_for_sorting[index]['total_repeat_farmers'] += 1;
        }
        if (count < 10) {
            drilldown['series'][index]['data'][count - 1][1] += 1;
        } else {
            drilldown['series'][index]['data'][9][1] += 1;
        }
    }

    data_for_sorting.sort(function(a, b) {
        return b['total_farmers'] - a['total_farmers'];
    });

    for (var i = 0; i < axis.length; i++) {
        series[0]['data'].push({
            'name': data_for_sorting[i]['name'],
            'y': data_for_sorting[i]['total_farmers'],
            'drilldown': data_for_sorting[i]['name']
        });
        series[1]['data'].push({
            'name': data_for_sorting[i]['name'],
            'y': data_for_sorting[i]['total_repeat_farmers']
        })

    }
    plot_drilldown(container, series, drilldown);
}

//Analytics Crops tab  Max Min graph is being plotted here
function max_min_graph(container, json_data) {

    json_data.sort(function(a, b) {
        return (b['price__max'] - b['price__min']) - (a['price__max'] - a["price__min"])
    })

    var x_axis = []
    var series = [{
        "name": "Max_Min",
        "data": []
    }]

    for (var i = 0; i < json_data.length; i++) {
        x_axis.push(json_data[i]['crop__crop_name'])
        series[0]['data'].push([json_data[i]['price__min'], json_data[i]['price__max']])
    }

    plot_max_min(container, x_axis, series)
}

// Computing data to display how many farmers brought a particular crop - Analytics Crops tab
function farmer_crop_visits(container, json_data) {
    var series = [];
    var temp_repeat = {};
    temp_repeat['name'] = "Total Farmers";
    temp_repeat['type'] = "bar";
    temp_repeat['showInLegend'] = false;
    temp_repeat['data'] = [];

    json_data.sort(function(a, b) {
        return (b['farmer__count']) - (a['farmer__count'])
    })

    series.push(temp_repeat);

    for (var i = 0; i < json_data.length; i++) {
        series[0]['data'].push([json_data[i]['crop__crop_name'], json_data[i]['farmer__count']])
    }

    plot_stacked_chart(container, series)

}

//Data for Time series grpahs request is being made here
function get_data_for_line_graphs(start_date, end_date, aggregator_ids, crop_ids, mandi_ids, gaddidar_ids) {
    $.get("/loop/data_for_line_graph/", {
            'start_date': start_date,
            'end_date': end_date,
            'aggregator_ids[]': aggregator_ids,
            'crop_ids[]': crop_ids,
            'mandi_ids[]': mandi_ids,
            'gaddidar_ids[]': gaddidar_ids
        })
        .done(function(data) {
            line_json_data = JSON.parse(data);
            show_line_graphs();
            fill_crop_drop_down();
            //Setting bandha gobhi to default When the page loads
            crop_prices_graph(3);
        });
}

//To fill crops name in drop down on Time series page
function fill_crop_drop_down() {
    var tbody_obj = $('#crop_max_min_avg');
    tbody_obj.html("");
    tbody_obj.append('<option value="" disabled selected> Choose a Crop </option>');
    $.each(crops_for_filter, function(index, data) {
        var li_item = '<option value=' + data.id + '>' + data.crop_name + '</option>';
        tbody_obj.append(li_item);
    });
    $('select').material_select();
}



function show_line_graphs() {
    var json_data = line_json_data.aggregator_data;
    var farmer_data = line_json_data.farmer;
    var transport_data = line_json_data.transport_data;
    var dates = line_json_data['dates']
    var all_dates = [];

    var first_date = new Date(dates[0]);
    while (first_date <= new Date(dates[dates.length - 1])) {
        all_dates.push(first_date.getTime());
        first_date.setDate(first_date.getDate() + 1)
    }
    time_series_volume_amount_farmers = [{
        'name': "volume",
        'type': 'areaspline',
        'data': [],
        'color': 'rgba(0,0,0,0.3)',
        'pointStart': all_dates[0],
        'pointInterval': 24 * 3600 * 1000

    }, {
        'name': "Amount",
        'type': 'areaspline',
        'data': [],
        'color': 'rgba(0,0,255,0.3)',
        'pointStart': all_dates[0],
        'pointInterval': 24 * 3600 * 1000
    }, {
        'name': "Farmers",
        'type': 'column',
        'data': [],
        'color': 'rgba(0,255,0,0.3)',
        'pointStart': all_dates[0],
        'pointInterval': 24 * 3600 * 1000
    }]

    time_series_cpk_spk = [{
        'name': "cpk",
        'type': 'areaspline',
        'data': [],
        'color': 'rgba(0,0,255,0.3)',
        'pointStart': all_dates[0],
        'pointInterval': 24 * 3600 * 1000
    }, {
        'name': "spk",
        'type': 'areaspline',
        'data': [],
        'color': 'rgba(0,255,0,0.3)',
        'pointStart': all_dates[0],
        'pointInterval': 24 * 3600 * 1000
    }];


    for (var i = 0; i < all_dates.length; i++) {
        time_series_volume_amount_farmers[0]['data'].push([all_dates[i], null]);
        time_series_volume_amount_farmers[1]['data'].push([all_dates[i], null]);
        time_series_volume_amount_farmers[2]['data'].push([all_dates[i], null]);
    }

    for (var i = 0; i < json_data.length; i++) {
        var index = all_dates.indexOf(new Date(json_data[i]['date']).getTime());
        time_series_volume_amount_farmers[0]['data'][index][1] += json_data[i]['quantity__sum'];
        time_series_volume_amount_farmers[1]['data'][index][1] += json_data[i]['amount__sum'];
    }
    transport_cost = new Array(all_dates.length).fill(null);
    farmer_share = new Array(all_dates.length).fill(null);
    for (var i = 0; i < transport_data.length; i++) {
        var index = all_dates.indexOf(new Date(transport_data[i]['date']).getTime());
        transport_cost[index] += transport_data[i]['transportation_cost__sum'];
        farmer_share[index] += transport_data[i]['farmer_share__sum'];
    }

    for (var i = 0; i < all_dates.length; i++) {
        time_series_cpk_spk[0]['data'].push([all_dates[i], time_series_volume_amount_farmers[0]['data'][i][1] > 0 ? transport_cost[i] / time_series_volume_amount_farmers[0]['data'][i][1] : null]);
        time_series_cpk_spk[1]['data'].push([all_dates[i], time_series_volume_amount_farmers[0]['data'][i][1] > 0 ? farmer_share[i] / time_series_volume_amount_farmers[0]['data'][i][1] : null]);
    }

    for (var i = 0; i < farmer_data.length; i++) {
        var index = all_dates.indexOf(new Date(farmer_data[i]['date']).getTime());
        time_series_volume_amount_farmers[2]['data'][index][1] += farmer_data[i]['farmer__count'];
    }

    createMaster1($('#detail_container_time_series'), $('#master_container_time_series'), time_series_volume_amount_farmers)
    createMaster2($('#detail_container_cpk'), $('#master_container_cpk'), time_series_cpk_spk);
}


//To show max, min , avg prices for crops in time series page
function crop_prices_graph(crop_id) {
    var json_data = line_json_data.crop_prices;
    var dates = line_json_data['dates'];
    var all_dates = [];

    var first_date = new Date(dates[0]);
    while (first_date <= new Date(dates[dates.length - 1])) {
        all_dates.push(first_date.getTime());
        first_date.setDate(first_date.getDate() + 1)
    }

    var series = [{
        'name': 'Range',
        'type': 'boxplot',

    }, {
        'name': 'Average Price',
        'type': 'line',

    }];

    var ranges = [];
    var avgs = [];

    for (var i = 0; i < all_dates.length; i++) {
        ranges.push([all_dates[i], null, null, null, null, null]);
        avgs.push([all_dates[i], null])
    }


    for (var i = 0; i < json_data.length; i++) {
        var index = all_dates.indexOf(new Date(json_data[i]['date']).getTime());

        if (json_data[i]['crop__id'].toString() == crop_id) {
            ranges[index][1] = json_data[i]['price__min'];
            ranges[index][2] = json_data[i]['amount__sum'] / json_data[i]['quantity__sum'];
            ranges[index][4] = json_data[i]['amount__sum'] / json_data[i]['quantity__sum'];
            ranges[index][5] = json_data[i]['price__max'];
            avgs[index][1] = json_data[i]['amount__sum'] / json_data[i]['quantity__sum'];
        }
    }

    series[1]['data'] = avgs;
    series[0]['data'] = ranges;

    plot_area_range_graph($("#container3"), series);

}

//To change frequency of time series graphs
function get_frequency_data(start_date, end_date, series, frequency, averaged) {
    var first_date = new Date(start_date);
    var final_date = new Date(end_date);
    new_series = [];

    if (frequency == 7) {
        var new_x_axis = [];
        while (first_date < final_date) {
            new_x_axis.push(first_date.getTime());
            first_date.setDate(first_date.getDate() + 7);
        }
    } else if (frequency == 15) {
        var new_x_axis = [];
        while (first_date < final_date) {
            if (first_date.getDate() <= 15) {
                new_x_axis.push(new Date(first_date.getFullYear() + "-" + (first_date.getMonth() + 1) + "-" + "01").getTime());
            } else {
                new_x_axis.push(new Date(first_date.getFullYear() + "-" + (first_date.getMonth() + 1) + "-" + "16").getTime());
            }
            first_date.setDate(first_date.getDate() + 15);
            if (first_date.getDate() == 31) {
                first_date.setDate(first_date.getDate() + 1);
            }
        };
    } else if (frequency == 30) {
        var new_x_axis = [];
        first_date.setDate(1)
        while (first_date <= final_date) {
            new_x_axis.push(new Date(first_date.getFullYear() + "-" + (first_date.getMonth() + 1) + "-" + "01").getTime());
            first_date.setMonth(first_date.getMonth() + 1);
        }
    }

    for (i = 0; i < series.length; i++) {
        var temp_series = {};
        temp_series['name'] = series[i]['name'];
        temp_series['data'] = new Array(new_x_axis.length);
        temp_series['color'] = series[i]['color'];
        temp_series['type'] = series[i]['type'];
        for (var j = 0; j < new_x_axis.length; j++) {
            temp_series['data'][j] = [new_x_axis[j], 0]
        }
        temp_series['pointStart'] = new_x_axis[0];
        temp_series['pointInterval'] = time_series_frequency * 24 * 3600 * 1000;
        var count = 0;
        var temp = 0;
        var index = 0;
        for (k = 0; k < series[i]['data'].length; k++) {

            var temp_date = new Date(series[i]['data'][k][0]);
            if (new Date(new_x_axis[index + 1]) <= new Date(series[i]['data'][k][0])) {
                index += 1;
            }
            if (averaged) {
                if (temp != index) {
                    temp_series['data'][temp][1] = temp_series['data'][temp][1] / count;
                    count = 0;
                }
            }
            temp_series['data'][index][1] += series[i]['data'][k][1];
            count += 1;
            var temp = index;
        }
        if (averaged) {
            temp_series['data'][temp][1] /= count;
        }
        new_series.push(temp_series);


    }
    return new_series;
}


function get_frequency_cpk(start_date, end_date, series, frequency, averaged) {

    var first_date = new Date(start_date);
    var final_date = new Date(end_date);
    new_series = [];

    if (frequency == 7) {
        var new_x_axis = [];
        while (first_date < final_date) {
            new_x_axis.push(first_date.getTime());
            first_date.setDate(first_date.getDate() + 7);
        }
    } else if (frequency == 15) {
        var new_x_axis = [];
        while (first_date < final_date) {
            if (first_date.getDate() <= 15) {
                new_x_axis.push(new Date(first_date.getFullYear() + "-" + (first_date.getMonth() + 1) + "-" + "01").getTime());
            } else {
                new_x_axis.push(new Date(first_date.getFullYear() + "-" + (first_date.getMonth() + 1) + "-" + "16").getTime());
            }
            first_date.setDate(first_date.getDate() + 15);
            if (first_date.getDate() == 31) {
                first_date.setDate(first_date.getDate() + 1);
            }
        };
    } else if (frequency == 30) {
        var new_x_axis = [];
        first_date.setDate(1)
        while (first_date <= final_date) {
            new_x_axis.push(new Date(first_date.getFullYear() + "-" + (first_date.getMonth() + 1) + "-" + "01").getTime());
            first_date.setMonth(first_date.getMonth() + 1);
        }
    }


    var temp_series_cpk = {};
    temp_series_cpk['name'] = series[0]['name'];
    temp_series_cpk['data'] = [];
    temp_series_cpk['color'] = series[0]['color'];
    temp_series_cpk['type'] = series[0]['type'];
    temp_series_cpk['pointStart'] = new_x_axis[0];
    temp_series_cpk['pointInterval'] = time_series_frequency * 24 * 3600 * 1000;
    var temp_series_spk = {};
    temp_series_spk['name'] = series[1]['name'];
    temp_series_spk['data'] = [];
    temp_series_spk['color'] = series[1]['color'];
    temp_series_spk['type'] = series[1]['type'];
    temp_series_spk['pointStart'] = new_x_axis[0];
    temp_series_spk['pointInterval'] = time_series_frequency * 24 * 3600 * 1000;
    var count = 0;
    var temp = 0;
    var index = 0;
    var new_transport_cost = new Array(new_x_axis.length).fill(0);
    var new_farmer_share = new Array(new_x_axis.length).fill(0);
    var new_volume = new Array(new_x_axis.length).fill(0);
    for (k = 0; k < series[0]['data'].length; k++) {

        if (new Date(new_x_axis[index + 1]) <= new Date(series[0]['data'][k][0])) {
            index += 1;
        }

        new_volume[index] += time_series_volume_amount_farmers[0]['data'][k][1];
        new_transport_cost[index] += transport_cost[k];
        new_farmer_share[index] += farmer_share[k];
    }

    for (var i = 0; i < new_x_axis.length; i++) {
        temp_series_cpk['data'].push([new_x_axis[i], new_volume[i] > 0 ? new_transport_cost[i] / new_volume[i] : null]);
        temp_series_spk['data'].push([new_x_axis[i], new_volume[i] > 0 ? new_farmer_share[i] / new_volume[i] : null]);
    }
    new_series.push(temp_series_cpk);
    new_series.push(temp_series_spk);



    return new_series;

}


function plot_stacked_chart(container_obj, dict) {

    if (dict[0]['data'].length >= 6) {
        var max = 5;
    } else {
        var max = dict[0]['data'].length - 1;
    }
    container_obj.highcharts({
        chart: {
            height: 300,
        },

        title: {
            text: null
        },
        xAxis: {
            type: 'category',
            labels: {
                rotation: 0
            },
            min: 0,
            max: max
        },
        scrollbar: {
            enabled: true,
        },
        yAxis: [{
            min: 0,
            title: {
                text: null
            },
            gridLineColor: 'transparent',
        }],
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            borderWidth: 0
        },
        tooltip: {
            headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
            pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:.2f}</b> <br/>'
        },

        plotOptions: {
            bar: {
                grouping: false,
                showCheckbox: true,
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

function plot_drilldown(container_obj, dict, drilldown, floats) {

    if (dict[0]['data'].length >= 6) {
        var max = 5;
    } else {
        var max = dict[0]['data'].length - 1;
    }
    if (floats) {
        format = '{point.y:.2f}'
    } else {
        format = '{point.y:.0f}'
    }
    var chart1 = container_obj.highcharts({
        chart: {
            type: 'bar',
            height: 300,
            zoomType: 'x',
            // events: {
            //          drilldown: function (e) {
            //             this.xAxis[0].update({max: null});
            //             this.scroller.scrollbar.hide();
            //             this.scroller.scrollbarGroup.hide();
            //             this.scroller.scrollbarRifles.attr({
            //                 'stroke-width': 0
            //             });
            //          },
            //          drillup: function (e) {
            //             this.scroller.scrollbar.show();
            //             this.scroller.scrollbarGroup.show();
            //             this.scroller.scrollbarRifles.attr({
            //                 'stroke-width': 1
            //             });

            //             var _self = this.xAxis[0];
            //             setTimeout(function () {
            //                 _self.setExtremes(0, max);
            //             }, 1);

            //          },
            //      }
        },
        title: {
            text: null
        },
        subtitle: {
            text: null
        },
        xAxis: [{
            type: 'category',
            max: max
        }, {
            type: 'category',
            max: null
        }],
        yAxis: {
            title: {
                text: null
            },
            min: 0,
            max: dict[0]['data'][0]['y'],
            gridLineColor: 'transparent',

        },
        scrollbar: {
            enabled: true
        },
        legend: {
            enabled: false
        },
        plotOptions: {
            series: {
                grouping: false,
                borderWidth: 0,
                dataLabels: {
                    enabled: true,
                    format: format
                }
            }
        },

        tooltip: {
            headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
            pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>' + format + '</b> <br/>'
        },
        series: dict,
        drilldown: drilldown
    });
}


function plot_max_min(container, x_axis, dict) {

    if (dict[0]['data'].length >= 6) {
        var max = 5;
    } else {
        var max = dict[0]['data'].length - 1;
    }

    container.highcharts({

        chart: {
            type: 'columnrange',
            inverted: true,
            height: 300
        },

        title: {
            text: null
        },



        xAxis: {
            categories: x_axis,
            min: 0,
            max: max,

        },

        yAxis: {
            title: {
                text: null
            },
            min: 0,
            gridLineColor: 'transparent',
        },

        scrollbar: {
            enabled: true,
        },

        plotOptions: {
            columnrange: {
                dataLabels: {
                    enabled: true,
                    formatter: function() {
                        return this.y;
                    }
                }
            }
        },

        legend: {
            enabled: false
        },

        series: dict

    });

};


function createDetail(detail_container, masterChart, dict) {

    // prepare the detail chart
    var myDict = []
    var detailData = [],
        detailStart = dict[0]['data'][0][0];

    $.each(masterChart.series, function() {
        if (this.name == "volume") {
            axis = 0;
        } else {
            axis = 1;
        }
        var temp = {};
        temp['name'] = this.name;
        temp['type'] = this.type;
        temp['data'] = new Array();
        temp['yAxis'] = axis;
        temp['pointStart'] = detailStart;
        temp['pointInterval'] = 24 * 3600 * 1000;
        temp['showInLegend'] = true;
        $.each(this.data, function() {
            if (this.x >= detailStart) {
                temp['data'].push(this.y);
            }

        });
        myDict.push(temp)
    });

    // create a detail chart referenced by a global variable
    width = detail_container.width();
    detailChart = detail_container.highcharts({
        chart: {
            width: width
        },
        title: {
            text: null
        },
        credits: {
            enabled: false
        },

        xAxis: {
            type: 'datetime'
        },
        yAxis: [{
            title: {
                text: null
            },
            maxZoom: 0.1,

        }, {
            title: {
                text: null
            },

            opposite: true
        }],
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
            areaspline: {
                fillOpacity: 0.5
            },
            series: {
                marker: {
                    enabled: true,
                    radius: 2.5,
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
function createMaster(detail_container, master_container, dict) {
    master_container.highcharts({
            chart: {
                zoomType: 'x',
                events: {

                    // listen to the selection event on the master chart to update the
                    // extremes of the detail chart
                    selection: function(event) {
                        var extremesObject = event.xAxis[0],
                            min = extremesObject.min,
                            max = extremesObject.max,
                            detailData = [],
                            xAxis = this.xAxis[0],
                            myDict = [];

                        $.each(this.series, function() {
                            var temp = {};
                            temp['name'] = this.name;
                            temp['data'] = new Array();
                            temp['pointStart'] = dict[0]['data'][0][0];
                            temp['pointInterval'] = 24 * 3600 * 1000;
                            $.each(this.data, function() {
                                if (this.x > min && this.x < max) {
                                    temp['data'].push([this.x, this.y]);
                                }
                            });
                            myDict.push(temp);
                        });

                        // reverse engineer the last part of the data

                        // move the plot bands to reflect the new detail span
                        xAxis.removePlotBand('mask-before');
                        xAxis.addPlotBand({
                            id: 'mask-before',
                            from: dict[0]['data'][0][0], //data[0][0],
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
                        var pos = 0;
                        $.each(this.series, function() {
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
            yAxis: [{
                gridLineWidth: 0,
                labels: {
                    enabled: false
                },
                title: {
                    text: null
                },
                min: 0.6,
                showFirstLabel: false
            }, {
                gridLineWidth: 0,
                labels: {
                    enabled: false
                },
                title: {
                    text: null
                },
                min: 0.6,
                showFirstLabel: false
            }],
            tooltip: {
                formatter: function() {
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

        }, function(masterChart) {
            createDetail(detail_container, masterChart, dict);
        })
        .highcharts(); // return chart instance
}

function createDetail1(detail_container, masterChart, dict) {

    // prepare the detail chart
    var myDict = []
    var detailData = [],
        detailStart = dict[0]['data'][0][0];

    $.each(masterChart.series, function() {
        if (this.name == "volume") {
            axis = 0;
        } else {
            axis = 1;
        }
        var temp = {};
        temp['name'] = this.name;
        temp['type'] = this.type;
        temp['data'] = new Array();
        temp['yAxis'] = axis;
        temp['color'] = this.color;
        temp['pointStart'] = detailStart;
        temp['pointInterval'] = time_series_frequency * 24 * 3600 * 1000;
        temp['showInLegend'] = true;
        $.each(this.data, function() {
            if (this.x >= detailStart) {
                temp['data'].push(this.y);
            }

        });
        myDict.push(temp)
    });

    // create a detail chart referenced by a global variable
    width = detail_container.width();
    detailChart1 = detail_container.highcharts({
        chart: {
            width: width
        },
        credits: {
            enabled: false
        },
        title: {
            text: null
        },

        xAxis: {
            type: 'datetime'
        },
        yAxis: [{
            title: {
                text: null
            },
            maxZoom: 0.1,

        }, {
            title: {
                text: null
            },

            opposite: true
        }],
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
            areaspline: {
                fillOpacity: 0.3
            },
            column: {
                fillOpacity: 0.3
            },
            series: {
                marker: {
                    enabled: true,
                    radius: 2.5,
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
function createMaster1(detail_container, master_container, dict) {
    master_container.highcharts({
            chart: {
                zoomType: 'x',
                events: {

                    // listen to the selection event on the master chart to update the
                    // extremes of the detail chart
                    selection: function(event) {
                        var extremesObject = event.xAxis[0],
                            min = extremesObject.min,
                            max = extremesObject.max,
                            detailData = [],
                            xAxis = this.xAxis[0],
                            myDict = [];

                        $.each(this.series, function() {
                            var temp = {};
                            temp['name'] = this.name;
                            temp['data'] = new Array();
                            temp['pointStart'] = this.pointStart;
                            temp['pointInterval'] = this.pointInterval;
                            temp['color'] = this.color;
                            $.each(this.data, function() {
                                if (this.x > min && this.x < max) {
                                    temp['data'].push([this.x, this.y]);
                                }
                            });
                            myDict.push(temp);
                        });

                        // reverse engineer the last part of the data

                        // move the plot bands to reflect the new detail span
                        xAxis.removePlotBand('mask-before');
                        xAxis.addPlotBand({
                            id: 'mask-before',
                            from: dict[0]['data'][0][0], //data[0][0],
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
                        var pos = 0;
                        $.each(this.series, function() {
                            detailChart1.series[pos].setData(myDict[pos].data);
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
            yAxis: [{
                gridLineWidth: 0,
                labels: {
                    enabled: false
                },
                title: {
                    text: null
                },
                min: 0.6,
                showFirstLabel: false
            }, {
                gridLineWidth: 0,
                labels: {
                    enabled: false
                },
                title: {
                    text: null
                },
                min: 0.6,
                showFirstLabel: false
            }],
            tooltip: {
                formatter: function() {
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

        }, function(masterChart) {
            createDetail1(detail_container, masterChart, dict);
        })
        .highcharts(); // return chart instance
}

function createDetail2(detail_container, masterChart, dict) {

    // prepare the detail chart
    var myDict = []
    var detailData = [],
        detailStart = dict[0]['data'][0][0];

    $.each(masterChart.series, function() {
        if (this.name == "volume") {
            axis = 0;
        } else {
            axis = 1;
        }
        var temp = {};
        temp['name'] = this.name;
        temp['type'] = this.type;
        temp['data'] = new Array();
        temp['yAxis'] = axis;
        temp['pointStart'] = detailStart;
        temp['pointInterval'] = time_series_frequency * 24 * 3600 * 1000;
        temp['showInLegend'] = true;
        $.each(this.data, function() {
            if (this.x >= detailStart) {
                temp['data'].push(this.y);
            }

        });
        myDict.push(temp)
    });

    // create a detail chart referenced by a global variable
    var width = detail_container.width();
    detailChart2 = detail_container.highcharts({
        chart: {
            width: width
        },
        credits: {
            enabled: false
        },

        xAxis: {
            type: 'datetime'
        },
        title: {
            text: null
        },
        yAxis: [{
            title: {
                text: null
            },
            maxZoom: 0.1,

        }, {
            title: {
                text: null
            },

            opposite: true
        }],
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
            areaspline: {
                fillOpacity: 0.5
            },
            series: {
                marker: {
                    enabled: true,
                    radius: 2.5,
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
function createMaster2(detail_container, master_container, dict) {
    master_container.highcharts({
            chart: {
                zoomType: 'x',
                events: {

                    // listen to the selection event on the master chart to update the
                    // extremes of the detail chart
                    selection: function(event) {
                        var extremesObject = event.xAxis[0],
                            min = extremesObject.min,
                            max = extremesObject.max,
                            detailData = [],
                            xAxis = this.xAxis[0],
                            myDict = [];

                        $.each(this.series, function() {
                            var temp = {};
                            temp['name'] = this.name;
                            temp['data'] = new Array();
                            temp['pointStart'] = this.pointStart;
                            temp['pointInterval'] = this.pointInterval;
                            $.each(this.data, function() {
                                if (this.x > min && this.x < max) {
                                    temp['data'].push([this.x, this.y]);
                                }
                            });
                            myDict.push(temp);
                        });

                        // reverse engineer the last part of the data

                        // move the plot bands to reflect the new detail span
                        xAxis.removePlotBand('mask-before');
                        xAxis.addPlotBand({
                            id: 'mask-before',
                            from: dict[0]['data'][0][0], //data[0][0],
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
                        var pos = 0;
                        $.each(this.series, function() {
                            detailChart2.series[pos].setData(myDict[pos].data);
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
            yAxis: [{
                gridLineWidth: 0,
                labels: {
                    enabled: false
                },
                title: {
                    text: null
                },
                min: 0.6,
                showFirstLabel: false
            }, {
                gridLineWidth: 0,
                labels: {
                    enabled: false
                },
                title: {
                    text: null
                },
                min: 0.6,
                showFirstLabel: false
            }],
            tooltip: {
                formatter: function() {
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

        }, function(masterChart) {
            createDetail2(detail_container, masterChart, dict);
        })
        .highcharts(); // return chart instance
}


function plot_area_range_graph(container, dict) {
    width = $("#container2").width()
    container.highcharts({

        chart: {
            zoomType: 'x',
            width: width
        },

        title: {
            text: null
        },

        xAxis: {
            type: 'datetime'
        },

        yAxis: {
            title: {
                text: null
            },
            min: 0,
        },

        tooltip: {
            crosshairs: true,
            shared: true,
            formatter: function() {
                return "Avg: " + parseFloat(this.points[1]['y']).toFixed(2) + "<br/>" + "Range: " + this.points[0]['point']['low'] + "-" + this.points[0]['point']['high'];
            }

        },
        plotOptions: {
            boxplot: {
                color: '#ffffff',
                stemColor: '#000000',
                whiskerColor: '#000000'

            }
        },

        legend: {},

        series: dict
    });
}


// To fill aggregator drop down on Payment page
function fill_drop_down(container, data_json, id_parameter, name_parameter, caption) {
    var tbody_obj = container;
    tbody_obj.html("");
    tbody_obj.append('<option value="" disabled selected> Choose a ' + caption + ' </option>');
    $.each(data_json, function(index, data) {
        var li_item = '<option value=' + data[id_parameter] + '>' + data[name_parameter] + '</option>';
        tbody_obj.append(li_item);
    });
    $('select').material_select();
}

//To compute aggregator, transporter, gaddidar payments table
function aggregator_payment_sheet(data_json, aggregator) {

    var aggregator_payment = payments_data.aggregator_data;
    var transport_payment = payments_data.transportation_data;
    var gaddidar_payment = payments_data.gaddidar_data;

    var sno = 1;
    var str1 = "Rs. ";
    var data_set = [];
    var gaddidar_data_set = [];
    var transporter_data_set = [];
    var dates = [];
    var mandis = [];
    var quantites = [];
    var gaddidar_amount = [];
    var farmers = [];
    var transport_cost = [];
    var farmer_share = [];
    for (var i = 0; i < aggregator_payment.length; i++) {

        if (aggregator == aggregator_payment[i]['user_created__id'].toString()) {
            var date_index = dates.indexOf(aggregator_payment[i]['date'])
            if (date_index == -1) {
                dates.push(aggregator_payment[i]['date']);
                mandis.push([]);
                quantites.push([]);
                gaddidar_amount.push([]);
                farmers.push([]);
                transport_cost.push([]);
                farmer_share.push([]);
                date_index = dates.indexOf(aggregator_payment[i]['date'])
            }
            var mandi_index = mandis[date_index].indexOf(aggregator_payment[i]['mandi__mandi_name'])
            if (mandi_index == -1) {
                mandis[date_index].push(aggregator_payment[i]['mandi__mandi_name']);
                quantites[date_index].push(0);
                gaddidar_amount[date_index].push(0);
                farmers[date_index].push(0);
                transport_cost[date_index].push(0);
                farmer_share[date_index].push(0);
                mandi_index = mandis[date_index].indexOf(aggregator_payment[i]['mandi__mandi_name'])
            }
            quantites[date_index][mandi_index] += aggregator_payment[i]['quantity__sum'];
            gaddidar_amount[date_index][mandi_index] += aggregator_payment[i]['quantity__sum'] * aggregator_payment[i]['gaddidar__commission'];
            farmers[date_index][mandi_index] += aggregator_payment[i]['farmer__count'];

            gaddidar_data_set.push([aggregator_payment[i]['date'], aggregator_payment[i]['gaddidar__gaddidar_name'], aggregator_payment[i]['mandi__mandi_name'], aggregator_payment[i]['quantity__sum'], aggregator_payment[i]['gaddidar__commission'], (aggregator_payment[i]['quantity__sum'] * aggregator_payment[i]['gaddidar__commission'])]);

        }

    };
    for (var i = 0; i < transport_payment.length; i++) {
        if (aggregator == transport_payment[i]['user_created__id'].toString()) {
            date_index = dates.indexOf(transport_payment[i]['date']);
            mandi_index = mandis[date_index].indexOf(transport_payment[i]['mandi__mandi_name']);
            transport_cost[date_index][mandi_index] += transport_payment[i]['transportation_cost__sum'];
            farmer_share[date_index][mandi_index] = transport_payment[i]['farmer_share'];
            transporter_data_set.push([transport_payment[i]['date'], transport_payment[i]['mandi__mandi_name'], transport_payment[i]['transportation_vehicle__transporter__transporter_name'], transport_payment[i]['transportation_vehicle__vehicle__vehicle_name'], transport_payment[i]['transportation_vehicle__vehicle_number'], transport_payment[i]['transportation_cost__sum']])
        }
    }

    var total_volume = 0;
    var total_payment = 0;
    for (var i = 0; i < dates.length; i++) {
        for (var j = 0; j < mandis[i].length; j++) {
            var net_payment = quantites[i][j] * 0.25 - gaddidar_amount[i][j] + transport_cost[i][j] - farmer_share[i][j];
            data_set.push([sno, dates[i], mandis[i][j], (quantites[i][j]).toString().concat(" Kg"), farmers[i][j], (quantites[i][j] * 0.25).toFixed(2), transport_cost[i][j], farmer_share[i][j], (gaddidar_amount[i][j]).toFixed(0), net_payment]);
            sno += 1
            total_volume += quantites[i][j]
            total_payment += net_payment
        }
    }

    $('#table2').DataTable({
        destroy: true,

        data: data_set,
        columns: [{
            title: "S No"
        }, {
            title: "Date"
        }, {
            title: "Mandi"
        }, {
            title: "Volume"
        }, {
            title: "Farmers"
        }, {
            title: "Aggregator Payment"
        }, {
            title: "Transport Cost"
        }, {
            title: "Farmer Share"
        }, {
            title: "Gaddidar Commission"
        }, {
            title: "Payment"
        }],
        "dom": '<"clear">',
        "pageLength": 20,
        // "tableTools": {
        //     "sSwfPath": "/media/app_dashboards/js/swf/copy_csv_xls_pdf.swf"
        // }
    });

    $("#table2").hide();
    // $("#table2").tableExport([],"total_payment");

    $('#table3').DataTable({
        destroy: true,
        data: gaddidar_data_set,
        columns: [{
            title: "Date"
        }, {
            title: "Gaddidar"
        }, {
            title: "Market"
        }, {
            title: "Quantity"
        }, {
            title: "Commission"
        }, {
            title: "Share"
        }],
        "dom": '<"clear">',
        "pageLength": 20,

    });
    $("#table3").hide();
    // $("#table3").tableExport([],"Gaddidar");
    $('#table4').DataTable({
        destroy: true,
        data: transporter_data_set,
        columns: [{
            title: "Date"
        }, {
            title: "Market"
        }, {
            title: "Transporter"
        }, {
            title: "Vehicle"
        }, {
            title: "Vehicle Number"
        }, {
            title: "Transport Cost"
        }],
        "dom": '<"clear">',
        "pageLength": 20,

    });
    $("#table4").hide();
    // $("#table4").tableExport([],"transport");


}

//To get data for aggregator, transporter, gaddidar payment sheets from server for specified time period
function get_payments_data() {
    payments_start_date = $("#payments_from_date").val();
    payments_to_date = $("#payments_to_date").val();
    if (payments_start_date != "" && payments_to_date != "" && new Date(payments_start_date) < new Date(payments_to_date) && new Date(payments_to_date) - new Date(payments_start_date) <= 1296000000) {
        $.get("/loop/payments/", {
            'start_date': payments_start_date,
            'end_date': payments_to_date
        }).done(function(data) {
            $('#aggregator_payment_tab').show();

            payments_data = JSON.parse(data);
            outliers_data = payments_data.outlier_data;
            outliers_transport_data = payments_data.outlier_transport_data;
            outlier_daily_data = payments_data.outlier_daily_data;
            fill_drop_down($('#aggregator_payments'), aggregators_for_filter, 'user__id', 'name', 'Aggregator');

        });
    } else {
        alert("Invalid Date Range")
    }
}


//To create table for 15 elements of outliers
function outliers_summary(aggregator_id) {
    var start_date = new Date(payments_start_date);
    var end_date = new Date(payments_to_date);
    var dates = [];
    while (start_date <= end_date) {
        dates.push(start_date.getTime());
        start_date.setDate(start_date.getDate() + 1);
    }

    var quantites = new Array(dates.length).fill(0);
    var farmers = new Array(dates.length).fill(0);

    for (var i = 0; i < outliers_data.length; i++) {
        if (aggregator_id == outliers_data[i]['user_created__id']) {

            var index = dates.indexOf(new Date(outliers_data[i]['date']).getTime());
            quantites[index] += (outliers_data[i]['quantity__sum']);
            farmers[index] += (outliers_data[i]['farmer__count']);
        }
    }

    transport_data = new Array(dates.length).fill(0);

    for (var i = 0; i < outliers_transport_data.length; i++) {
        if (aggregator_id == outliers_transport_data[i]['user_created__id']) {
            var index = dates.indexOf(new Date(outliers_transport_data[i]['date']).getTime());
            transport_data[index] += outliers_transport_data[i]['transportation_cost__sum'];

        }
    }

    var cpk = [];
    $("#outliers").html("");
    for (var i = 0; i < dates.length; i++) {
        // cpk.push(quantites[i] > 0 ? transport_data[i] / quantites[i] : 0.0);
        if (farmers[i] == 0) {
            $('<td class="center" onclick="create_outliers_table(' + dates[i] + ',' + aggregator_id + ')">' + new Date(dates[i]).getDate() + '</td>').appendTo('#outliers');
        } else if (farmers[i] < 3) { //cpk[i] > 0.6
            $('<td class="center" style="background-color:rgba(255,0,0,0.2)" onclick="create_outliers_table(' + dates[i] + ',' + aggregator_id + ')">' + new Date(dates[i]).getDate() + '</td>').appendTo('#outliers');
        } else {
            $('<td class="center" style="background-color:rgba(0,255,0,0.2)" onclick="create_outliers_table(' + dates[i] + ',' + aggregator_id + ')">' + new Date(dates[i]).getDate() + '</td>').appendTo('#outliers');
        }
    }

}

//To check if table is already created, If yes then destroy child table and recreate it
table_created = false;

function create_outliers_table(date, aggregator_id) {
    if (table_created) {
        outliers_table.clear().destroy();
    } else {
        table_created = true;
    }

    var data_set = [];
    var sno = 1;

    console.log(outliers_data);
    for (var i = 0; i < outliers_data.length; i++) {
        if (new Date(date).getTime() == new Date(outliers_data[i]['date']).getTime() && aggregator_id == outliers_data[i]['user_created__id']) {

            data_set.push(["", sno, outliers_data[i]['date'], outliers_data[i]['mandi__mandi_name'], outliers_data[i]['farmer__count'], outliers_data[i]['quantity__sum'], outliers_data[i]['gaddidar__commission__sum']])
            sno += 1;
        }
    }

    for (var i = 0; i < outliers_transport_data.length; i++) {
        if (new Date(date).getTime() == new Date(outliers_transport_data[i]['date']).getTime() && aggregator_id == outliers_transport_data[i]['user_created__id']) {
            for (var j = 0; j < data_set.length; j++) {
                if (data_set[j].indexOf(outliers_transport_data[i]['mandi__mandi_name'])) {
                    data_set[j].splice(-2, 0, outliers_transport_data[i]['transportation_cost__sum']);
                    data_set[j].splice(-1, 0, outliers_transport_data[i]['farmer_share__sum']);
                } else {
                    data_set[j].splice(-2, 0, 0);
                    data_set[j].splice(-1, 0, 0);
                }
            }
        }
    }
    $("#outliers_data").html("");
    outliers_table = $('#outliers_data').DataTable({
        destroy: true,
        data: data_set,
        columns: [{
            "className": 'details-control',
            "orderable": false,
            "data": "",
            "defaultContent": ''
        }, {
            title: "S No"
        }, {
            title: "Date"
        }, {
            title: "Mandi"
        }, {
            title: "Farmers"
        }, {
            title: "Quantity"
        }, {
            title: "Transport Cost"
        }, {
            title: "Farmer Share"
        }, {
            title: "Gaddidar Commission"
        }],
        "dom": '<"clear">',

    });

    $('#outliers_data tbody').on('click', 'td.details-control', function() {
        var tr = $(this).closest('tr');
        var row = outliers_table.row(tr);
        // row.child.hide();
        if (!row.child.isShown()) {
            // This row is already open - close it
            row.child(show_detailed_data(row.data(), aggregator_id)).show();
            tr.addClass('shown');
        } else {
            // Open this row
            row.child(false).remove();
            tr.removeClass('shown');

        }
    });
}

//To show child row for an outlier element
function show_detailed_data(d, aggregator_id) {
    // `d` is the original data object for the row
    var detailed_table = $('<table></table>');

    var data_set = [];
    var sno = 1;
    for (var i = 0; i < outlier_daily_data.length; i++) {
        if (new Date(d[2]).getTime() == new Date(outlier_daily_data[i]['date']).getTime() && d[3] == outlier_daily_data[i]['mandi__mandi_name'] && aggregator_id == outlier_daily_data[i]['user_created__id']) {
            data_set.push([sno, outlier_daily_data[i]['gaddidar__gaddidar_name'], outlier_daily_data[i]['farmer__name'], outlier_daily_data[i]['quantity__sum'], outlier_daily_data[i]['crop__crop_name'], outlier_daily_data[i]['price'], outlier_daily_data[i]['gaddidar__commission']])
            sno += 1;
        }
    }
    detailed_table.DataTable({
        destroy: true,
        data: data_set,
        columns: [{
            title: "S No"
        }, {
            title: "Gaddidar"
        }, {
            title: "Farmers"
        }, {
            title: "Quantity"
        }, {
            title: "Crop"
        }, {
            title: "Price"
        }, {
            title: "Commission"
        }],
        "dom": 'T<"clear">rtip',
    });
    return detailed_table;
}



function download_payments_data() {
    $("#table2").tableExport([], "Total_payment");
    $("#table3").tableExport([], "Gaddidar_payment_sheet");
    $("#table4").tableExport([], "Transporter_payment_sheet");
}

function plot_solid_guage(container, present, target) {
    var gaugeOptions = {
        chart: {
            type: 'solidgauge',
            width: 170,
            height: 100
        },
        exporting: {
            enabled: false
        },
        title: null,

        pane: {
            center: ['50%', '85%'],
            size: '140%',
            startAngle: -90,
            endAngle: 90,
            background: {
                backgroundColor: (Highcharts.theme && Highcharts.theme.background2) || '#EEE',
                innerRadius: '60%',
                outerRadius: '100%',
                shape: 'arc'
            }
        },

        tooltip: {
            enabled: false
        },

        // the value axis
        yAxis: {
            stops: [
                [0.1, '#55BF3B'], // green
                [0.5, '#DDDF0D'], // yellow
                [0.9, '#DF5353'] // red
            ],
            lineWidth: 0,
            minorTickInterval: null,
            tickPixelInterval: 400,
            tickWidth: 0,
            title: {
                y: -70
            },
            labels: {
                y: 16
            }
        },

        plotOptions: {
            solidgauge: {
                dataLabels: {
                    y: 5,
                    borderWidth: 0,
                    useHTML: true
                }
            }
        }
    };

    // The speed gauge
    container.highcharts(Highcharts.merge(gaugeOptions, {
        yAxis: {
            min: 0,
            max: target,
            title: {
                text: 'Target'
            }
        },

        credits: {
            enabled: false
        },

        series: [{
            name: 'Present',
            data: [present],
            dataLabels: {
                format: null
            },
            tooltip: {
                valueSuffix: null
            }
        }]

    }));
}

// function gaddidar_cpk_spk_graph(container, axis, axis_names, axis_parameter, values, values_names, values_parameter, json_data) {
//     var vol_stats = json_data.aggregator_gaddidar;
//     var cost_stats = json_data.transportation_cost_mandi;
//     var series = [];
//     var drilldown = {};
//     drilldown['series'] = [];

//     values_vol = new Array(axis.length).fill(0.0);
//     values_vol_gaddidar = new Array(axis.length).fill(0.0);

//     values_vol_drilldown = [];

//     values_cost_cpk = new Array(axis.length).fill(0.0);
//     values_cost_cpk_drilldown = [];
//     values_cost_spk = new Array(axis.length).fill(0.0);
//     values_cost_spk_drilldown = [];
//     var temp = {};
//     var temp_spk = {};
//     temp['name'] = 'cpk';
//     temp['type'] = "bar";
//     temp['showInLegend'] = false;
//     temp['data'] =[];
//     temp['pointPadding'] = 0.3;
//     temp['pointPlacement'] = 0;


//     temp_spk['name'] = 'spk';
//     temp_spk['type'] = "bar";
//     temp_spk['showInLegend'] = false;
//     temp_spk['data'] = [];
//     temp_spk['pointPadding'] = 0.4;
//     temp_spk['pointPlacement'] = 0;

//     series.push(temp);
//     series.push(temp_spk);

//     for (var i = 0; i < axis.length; i++){
//         values_vol_drilldown.push(new Array(values.length).fill(null));
//         values_cost_cpk_drilldown.push(new Array(values.length).fill(null));
//         values_cost_spk_drilldown.push(new Array(values.length).fill(null));

//     }

//     for (var i = 0; i < vol_stats.length; i++) {
//         var index = axis.indexOf(vol_stats[i][axis_parameter].toString());
//         var drilldown_index = values.indexOf(vol_stats[i][values_parameter].toString());
//         values_vol[index] += vol_stats[i]['quantity__sum'];
//         values_vol_drilldown[index][drilldown_index] += vol_stats[i]['quantity__sum'];
//     }
//     for (var i = 0; i < cost_stats.length; i++) {
//         var index = axis.indexOf(cost_stats[i][axis_parameter].toString());
//         var drilldown_index = values.indexOf(cost_stats[i][values_parameter].toString());
//         values_cost_cpk[index] += cost_stats[i]['transportation_cost__sum'] ;
//         values_cost_spk[index] += cost_stats[i]['farmer_share__sum'];
//         values_cost_cpk_drilldown[index][drilldown_index] += cost_stats[i]['transportation_cost__sum'];
//         values_cost_spk_drilldown[index][drilldown_index] += cost_stats[i]['farmer_share__sum'];

//     }
//     var data_for_sorting=[]
//     for (var i = 0; i < axis.length; i++) {
//        data_for_sorting.push({'name':axis_names[i], 'cpk':values_vol[i] > 0 ? values_cost_cpk[i] / values_vol[i] : 0.0, 'spk':values_vol[i] > 0 ? values_cost_spk[i] / values_vol[i] : 0.0});
//        drilldown['series'].push({'name':axis_names[i], 'id': axis_names[i]+"cpk", 'data':[]});
//        drilldown['series'].push({'name':axis_names[i], 'id': axis_names[i]+"spk", 'data':[]});
//        for (var j=0; j<values.length; j++){
//             drilldown['series'][i*2]['data'].push([values_names[j], values_vol_drilldown[i][j] > 0 ? values_cost_cpk_drilldown[i][j] / values_vol_drilldown[i][j] : 0.0 ]);
//             drilldown['series'][i*2+1]['data'].push([values_names[j], values_vol_drilldown[i][j] > 0 ? values_cost_spk_drilldown[i][j] / values_vol_drilldown[i][j] : 0.0 ]);
//        }
//     }

//     data_for_sorting.sort(function(a,b){
//         return (b['cpk']-b['spk']) - (a['cpk']-a['spk']);
//     });

//     for (var i = 0; i < axis_names.length; i++) {
//         series[0]['data'].push({'name': data_for_sorting[i]['name'], 'y':data_for_sorting[i]['cpk'], 'drilldown':data_for_sorting[i]['name']+"cpk" });
//         series[1]['data'].push({'name': data_for_sorting[i]['name'], 'y':data_for_sorting[i]['spk'], 'drilldown':data_for_sorting[i]['name']+"spk"});
//     }

//     for (var i=0; i<drilldown['series'].length; i++){
//         drilldown['series'][i]['data'].sort(function(a,b){
//             return b[1] - a[1]
//         });
//     }

//     plot_drilldown(container, series, drilldown);
// }


/* Formatting function for row details - modify as you need */

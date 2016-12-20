/* This file should contain all the JS for Loop dashboard */
window.onload = initialize;

var language, selected_tab, selected_parameter, selected_page;
var days_to_average, time_series_frequency;
//Arrays containing ids and corresponding names as were selected in the filters.
var aggregator_ids, aggregator_names, crop_ids, crop_names, mandi_ids, mandi_names, gaddidar_ids, gaddidar_names;
//Variables for second nav bar which is visible in analytics and time series tabs.
var start_date, end_date;
//Json for filters.
var aggregators_for_filter, mandis_for_filter, gaddidars_for_filter, crops_for_filter, croplanguage_for_filter, transporter_for_filter;
//Variables for capturing complete json data for analytics and time series tabs.
var bar_graphs_json_data, line_json_data;
//Variables for time series graphs.
var time_series_volume_amount_farmers, time_series_cpk_spk;
//Variables for payments tab.
var payments_start_date, payments_to_date;
var payments_data, outliers_data, outliers_transport_data, outlier_daily_data, payments_gaddidar_contribution;
//GENERAL CONSTANTS
var AGGREGATOR_INCENTIVE_PERCENTAGE = 0.25;
var ENGLISH_LANGUAGE = "English";
var REGIONAL_LANGUAGE = "Regional";
var HOME = "home";
var PAYMENTS_PAGE = "payments";
var ANALYTICS_PAGE = "analytics";
var TIME_SERIES_PAGE = "time_series";
var RUPEE = "₹ ";
var KG = "Kg";
var VOLUME = "volume",
    MANDI = "mandi",
    VISITS = "visits",
    CROP = "crop",
    AGGREGATOR = "aggregator",
    AMOUNT = "amount";
var QUANTITY__SUM = "quantity__sum",
    AMOUNT__SUM = "amount__sum",
    MANDI__ID = "mandi__id",
    USER_CREATED__ID = "user_created__id";

var aggregator_sheet_name = "", gaddidar_sheet_name = "", transporter_sheet_name = "" ;



function initialize() {
    // initialize any library here
    language = ENGLISH_LANGUAGE;
    $("select").material_select();
    $(".button-collapse").sideNav({
        closeOnClick: true
    });
    $(".button-collapse1").sideNav();

    var today = new Date();
    $("#to_date").val(today.getFullYear() + "-" + (today.getMonth() + 1) + "-" + today.getDate());
    today.setMonth(today.getMonth() - 1);
    $("#from_date").val(today.getFullYear() + "-" + (today.getMonth() + 1) + "-" + today.getDate());

    showLoader();
    total_static_data();
    recent_graphs_data(language);
    days_to_average = 15;

    gaddidar = true;
    selected_tab = AGGREGATOR;
    selected_parameter = VOLUME;
    selected_page = HOME;

    time_series_frequency = 1;

    get_filter_data(language);
    set_filterlistener();
    $('#aggregator_payment_tab').hide();
    $("#download_payment_sheets").hide();
}

function showLoader() {
    $("#loader").show();
    hide_nav();
}

function hideLoader() {
    $("#loader").hide();
    hide_nav(HOME);
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
    $("#filters_nav").removeClass('show');
    $("#filters_nav").addClass('hide');
    $("#home_div").hide();
    $("#analytics_div").hide();
    $("#time_series_div").hide();
    $("#payments_div").hide();

    $("#home_tab").removeClass('active');
    $("#payments_tab").removeClass('active');
    $("#analytics_tab").removeClass('active');
    $("#time_series_tab").removeClass('active');

    if (tab == HOME) {
        $("#home_div").show();
        $("#home_tab").addClass('active');
        selected_page = HOME;
    } else if (tab == PAYMENTS_PAGE) {
        $("#payments_div").show();
        $("#payments_tab").addClass('active');
        selected_page = PAYMENTS_PAGE;
    }
}

//To show the second navigation bar that comes on analytics and time series page only
function show_nav(tab) {
    $("#home_tab").removeClass('active');
    $("#payments_tab").removeClass('active');
    $("#analytics_tab").removeClass('active');
    $("#time_series_tab").removeClass('active');
    $("#filters_nav").removeClass('hide');
    $("#filters_nav").addClass('show');
    $("#home_div").hide();
    $("#payments_div").hide();

    if (tab == ANALYTICS_PAGE) {
        selected_page = ANALYTICS_PAGE;
        $("#analytics_div").show();
        $("#time_series_div").hide();
        $(".analytics_tabs").show();
        $("#analytics_tab").addClass('active');
        PlotAnalyticsGraphs();
    } else if (tab == TIME_SERIES_PAGE) {
        selected_page = TIME_SERIES_PAGE;
        $("#analytics_div").hide();
        $("#time_series_div").show();
        $(".analytics_tabs").hide();
        $("#time_series_tab").addClass('active');
        PlotTimeSeriesGraphs();
    }
}

function PlotAnalyticsGraphs() {
    totals();
    change_graph();
}

function PlotTimeSeriesGraphs() {
    show_line_graphs();
    fill_crop_drop_down();
    //Setting crop with max volume to default
    crop_prices_graph(-1);
}

bullet_options = {
    type: "bullet",
    width: "100",
    height: "30",
    performanceColor: '#00bfbf',
    rangeColors: ['#a2d6d6'],
    targetColor: '#ffffff'
}

sparkline_option = {
    type: 'line',
    width: '150',
    height: '60',
    lineColor: '#00bfbf',
    fillColor: '#dde1df',
    lineWidth: 2
}

//To compute data for home page overall cards
function total_static_data() {
    $.get("/loop/total_static_data/", {}).done(function(data) {
        hideLoader();
        var json_data = JSON.parse(data);
        var total_volume = json_data['total_volume'][QUANTITY__SUM];
        var total_amount = json_data['total_volume'][AMOUNT__SUM];
        var total_farmers_reached = json_data['total_farmers_reached'];
        var total_repeat_farmers = json_data['total_repeat_farmers']
        var total_transportation_cost = 0;
        var total_farmer_share = 0;

        for (var i = 0; i < json_data['total_transportation_cost'].length; i++) {
            total_transportation_cost += json_data['total_transportation_cost'][i]['transportation_cost__sum'];
            total_farmer_share += json_data['total_transportation_cost'][i]['farmer_share__sum'];
        }

        var total_gaddidar_contribution = json_data['total_gaddidar_contribution'];
        var total_aggregator_cost = total_volume * AGGREGATOR_INCENTIVE_PERCENTAGE;
        var sustainability = (total_farmer_share + total_gaddidar_contribution) / (total_transportation_cost + total_aggregator_cost) * 100;

        var clusters = json_data['total_cluster_reached'];
        var total_cpk = (total_transportation_cost + total_aggregator_cost) / total_volume;

        plot_solid_guage($('#cluster_bullet'), 0, clusters, 25);
        plot_solid_guage($('#total_farmers_bullet'), 0, total_farmers_reached, 2000);
        plot_solid_guage($('#total_volume_bullet'), 0, parseInt(total_volume), 5000000);
        plot_solid_guage($('#revenue_bullet'), 0, parseInt(total_amount), 25000000);
        plot_solid_guage($('#total_expenditure_bullet'), -1, parseFloat(0 - total_cpk.toFixed(2)), 0);
        plot_solid_guage($('#sustainability_bullet'), 0, parseFloat(sustainability.toFixed(2)), 50);
    });
}

//To request data for recent graphs on home page
function recent_graphs_data(language) {
    $.get("/loop/recent_graphs_data/", {}).done(function(data) {
        json_data = JSON.parse(data);
        dates = json_data['dates'];
        stats = json_data['stats'];
        transportation = json_data['transportation_cost'];
        gaddidar_contribution_recent_graph = json_data['gaddidar_contribution'];
        plot_cards_data();
        cummulative_farmer_and_volume();
    });
}

//To plot and show data for recents graphs on home page
function plot_cards_data() {
    var avg = get_average(); // Retunts [avg_vol, active_farmers, avg_amt, active_clusters,avg_gaddidar_share]
    var avg_vol = avg[0];
    var avg_gaddidar_contribution = avg[4];
    var active_clusters = avg[3];
    document.getElementById('recent_cluster_card').innerHTML = '&nbsp;&nbsp;&nbsp;' + active_clusters[0];
    $("#recent_cluster_sparkline").sparkline(active_clusters.reverse(), sparkline_option);

    document.getElementById('recent_volume_card').innerHTML = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + (avg_vol[0].toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")).concat(KG);
    $('#recent_volume_sparkline').sparkline(avg_vol.reverse(), sparkline_option);

    var active_farmers = avg[1];
    document.getElementById('recent_active_farmers_card').innerHTML = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + active_farmers[0];
    $('#recent_active_farmers_sparkline').sparkline(active_farmers.reverse(), sparkline_option);

    var avg_amt = avg[2];
    document.getElementById('recent_revenue_card').innerHTML = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + RUPEE.concat(avg_amt[0].toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","));
    $('#recent_revenue_sparkline').sparkline(avg_amt.reverse(), sparkline_option);

    var data = get_cpk(avg_vol.reverse(), avg_gaddidar_contribution);
    var cpk = data[0];
    document.getElementById('cpk_card').innerHTML = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + RUPEE.concat(parseFloat(cpk[0]).toFixed(2));
    $('#cpk_sparkline').sparkline(cpk.reverse(), sparkline_option);

    var sustainability = data[1];
    document.getElementById('recent_sustainability_card').innerHTML = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + parseFloat(sustainability[0]).toFixed(2) + "%";
    $('#recent_sustainability_sparkline').sparkline(sustainability.reverse(), sparkline_option);
}


//Helper function to calculate average for 7,15,30,60 days for above function
function get_average() {
    var today = new Date();
    today.setDate(today.getDate() - days_to_average);

    var gaddidar_day = new Date();
    gaddidar_day.setDate(gaddidar_day.getDate() - days_to_average);

    var avg_vol = [];
    var avg_amt = [];

    var active_farmers = [];
    var active_farmers_id = [];
    var active_clusters = [];
    var active_clusters_id = [];
    var avg_gaddidar_share = [];

    var j = 0,
        k = 0,
        temp_vol = 0,
        temp_amt = 0,
        temp_gaddidar_share = 0;

    var gaddidar_share = [];
    var dates_of_transaction = dates.length;
    for (var i = 0; i < dates_of_transaction; i++) {
        gaddidar_share.push(0);
    }
    var gaddidar_contribution_length = gaddidar_contribution_recent_graph.length;
    for (var i = 0; i < gaddidar_contribution_length; i++) {
        var index = dates.indexOf(gaddidar_contribution_recent_graph[i]['date']);
        if (index != -1) {
            gaddidar_share[index] += gaddidar_contribution_recent_graph[i]['amount'];
        }
    }

    while (gaddidar_day >= new Date(dates[k])) {
        avg_gaddidar_share.push(0);
        gaddidar_day.setDate(gaddidar_day.getDate() - days_to_average);
    }

    var gaddidar_contribution_length = gaddidar_contribution_recent_graph.length;
    while (k < gaddidar_contribution_length && gaddidar_day < new Date(dates[k])) {
        temp_gaddidar_share += gaddidar_share[k];
        k++;
        if (k < gaddidar_contribution_length && gaddidar_day >= new Date(dates[k])) {
            avg_gaddidar_share.push(temp_gaddidar_share.toFixed(0));
            temp_gaddidar_share = 0;
            gaddidar_day.setDate(gaddidar_day.getDate() - days_to_average);

            //If no data is present for a period of days_to_average
            while (gaddidar_day >= new Date(dates[k])) {
                avg_gaddidar_share.push(0);
                gaddidar_day.setDate(gaddidar_day.getDate() - days_to_average);
            }
        }
    }
    avg_gaddidar_share.push(temp_gaddidar_share);

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
        temp_vol += stats[j][QUANTITY__SUM];
        temp_amt += stats[j][AMOUNT__SUM];

        var farmer_id = stats[j]['farmer__id'];
        if (active_farmers_id.indexOf(farmer_id) == -1) {
            active_farmers_id.push(farmer_id);
        }
        var cluster_id = stats[j][USER_CREATED__ID];
        if (active_clusters_id.indexOf(cluster_id) == -1) {
            active_clusters_id.push(cluster_id);
        }
        j++;
        if (j < stats_length && today >= new Date(stats[j]['date'])) {
            avg_vol.push(temp_vol.toFixed(0));
            avg_amt.push(temp_amt.toFixed(0));
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
    return [avg_vol, active_farmers, avg_amt, active_clusters, avg_gaddidar_share];
}


//Helper function to calculate average cpk for 7,15,30,60 days for above function
function get_cpk(avg_vol, avg_gaddidar_contribution) {
    var today = new Date();
    today.setDate(today.getDate() - days_to_average);
    var cpk = [];
    var sustainability_per_kg = [];

    var j = 0, // To loop through transportation details
        transportation_cost = 0,
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
        transportation_cost += parseFloat(transportation[j]['transportation_cost__sum']); // - transportation[j]['farmer_share__sum'];
        f_share += parseFloat(transportation[j]['farmer_share__sum']);
        j++;
        if (j < transportation.length && today >= new Date(transportation[j]['date'])) {
            if (avg_vol[k] == 0) {
                cpk.push(0);
                sustainability_per_kg.push(0);
            } else {
                var recovered = parseFloat(f_share) + parseFloat(avg_gaddidar_contribution[k]);
                var cost = parseFloat(transportation_cost) + parseFloat(avg_vol[k]) * AGGREGATOR_INCENTIVE_PERCENTAGE;
                var cpk_value = parseFloat(cost) / parseFloat(avg_vol[k]);
                var spk_value = (parseFloat(recovered) / parseFloat(cost)) * 100;
                cpk.push(cpk_value.toFixed(2));
                sustainability_per_kg.push(spk_value.toFixed(2));
            }

            k++;
            today.setDate(today.getDate() - days_to_average);
            transportation_cost = 0;
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
        var recovered = parseFloat(f_share) + parseFloat(avg_gaddidar_contribution[k]);
        var cost = parseFloat(transportation_cost) + parseFloat(avg_vol[k]) * AGGREGATOR_INCENTIVE_PERCENTAGE;
        var cpk_value = parseFloat(cost) / parseFloat(avg_vol[k]);
        var spk_value = (parseFloat(recovered) / parseFloat(cost)) * 100;
        cpk.push(cpk_value.toFixed(2));
        sustainability_per_kg.push(spk_value.toFixed(2));
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
    var farmer_ids = [];

    var first_date = new Date(dates[dates.length - 1]);
    while (first_date <= new Date(dates[0])) {
        all_dates.push(first_date.getTime());
        first_date.setDate(first_date.getDate() + 1)
    }

    var cumm_volume = new Array(all_dates.length).fill(0.0);
    var cumm_farmers = new Array(all_dates.length).fill(0.0);
    var temp_volume = {};
    temp_volume['name'] = "volume";
    temp_volume['data'] = [];
    temp_volume['type'] = 'spline';
    temp_volume['pointInterval'] = 24 * 3600 * 1000;
    temp_volume['pointStart'] = all_dates[all_dates.length - 1]; // Pointing to the starting date
    temp_volume['showInLegend'] = true;
    var temp_farmers = {};
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
        cumm_volume[index] += stats[i][QUANTITY__SUM];
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

    createMasterForCummulativeVolumeAndFarmer($('#detail_container'), $('#master_container'), series);
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
    $("#aggregator_cpk").addClass("active");
    $("#aggregator_cost").removeClass("active");

    $('ul.tabs').tabs();

    $("#aggregator_visits").show();
    $("#cpk_cost").show();
    $("#crop_prices_min_max").hide();
    $("#gaddidar_aggregator_graph").hide();
    $("#aggregator_farmer_count").show();
    if (selected_tab == AGGREGATOR) {
        $("#farmer_count_tab").addClass("active");
        $('#aggregator_tab').addClass('active');
        update_graphs_aggregator_wise(parameter);
    } else if (selected_tab == MANDI) {
        $('#mandi_tab').addClass('active');
        $("#gaddidar_aggregator_graph").show();
        $("#aggregator_farmer_count").hide();
        $("#gaddidar_volume").addClass("active");
        update_graphs_mandi_wise(parameter);
        update_graphs_gaddidar_wise(selected_parameter);
    } else if (selected_tab == CROP) {
        $("#farmer_count_tab").addClass("active");
        $('#crop_tab').addClass('active');
        $("#aggregator_visits").hide();
        $("#cpk_cost").hide();
        $("#crop_prices_min_max").show();
        update_graphs_crop_wise(parameter);
    }
}

//To check for any items data change (textview, drop downs, button click)
function set_filterlistener() {
    $("#recent_cards_data_frequency").change(function() {
        days_to_average = $('#recent_cards_data_frequency :selected').val();
        plot_cards_data();
    });

    $('#get_data').click(function() {
        time_series_frequency = 1;
        $('#time_series_frequency option[value="' + 1 + '"]').prop('selected', true);
        $('#time_series_frequency').material_select();
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
        var crop_id = $('#crop_max_min_avg :selected').val();
        crop_prices_graph(crop_id);
    });

    $("#download-payment-sheet").click(function() {
        if ($('#aggregator_payments :selected').val() == '') {
                alert("Please select an aggregator to download the payment sheet");
             }
        else
        {

            xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() {
            var a;
            if (xhttp.readyState === 4 && xhttp.status === 200) {
            a = document.createElement('a');
            a.href = window.URL.createObjectURL(xhttp.response);
            a.download = aggregator_sheet_name;
            a.style.display = 'none';
            document.body.appendChild(a);
            return a.click();
                }
            };
            xhttp.open("POST", "/loop/get_payment_sheet/", true);
            xhttp.setRequestHeader("Content-Type", "application/json");
            xhttp.responseType = 'blob';
            var data_json = {
                aggregator_data:{
                    name: aggregator_sheet_name,
                    data : aggregator_data_set     
                },

                gaddidar_data: {
                    name : gaddidar_sheet_name,
                    data : gaddidar_data_set    
                },

                transporter_data:{
                    name : transporter_sheet_name,
                    data : transporter_data_set
                 }
            };
            xhttp.send(JSON.stringify(data_json));
        }

});


    $("#aggregator_payments").change(function() {
        var aggregator_id = $('#aggregator_payments :selected').val();
        if (table_created) {
            $('#outliers_data').html("");
        }
        aggregator_payment_sheet(payments_data.aggregator_data, aggregator_id);
        $("#download_payment_sheets").show();
        $('#aggregator_payment_details').show();
        outliers_summary(aggregator_id);
    });



    $("#time_series_frequency").change(function() {
        time_series_frequency = $('#time_series_frequency :selected').val();
        if (time_series_frequency == 1) {
            createMasterForVolAmtTimeSeries($('#detail_container_time_series'), $('#master_container_time_series'), time_series_volume_amount_farmers);
            createMasterForCpkSpkTimeSeries($('#detail_container_cpk'), $('#master_container_cpk'), time_series_cpk_spk);
        } else {
            createMasterForVolAmtTimeSeries($('#detail_container_time_series'), $('#master_container_time_series'), get_frequency_data(start_date, end_date, time_series_volume_amount_farmers, time_series_frequency, false));
            createMasterForCpkSpkTimeSeries($('#detail_container_cpk'), $('#master_container_cpk'), get_frequency_cpk(start_date, end_date, time_series_cpk_spk, time_series_frequency, false));
        }
    });

    $('#payments_from_date').change(function() {
        var start_date = $('#payments_from_date').val();
        if (start_date != '') {
            $("#aggregator_payment_tab").hide();
            $("#download_payment_sheets").hide();
            $('#aggregator_payment_details').hide();
            $('#payments_to_date').prop('disabled', false);
            var from_date = new Date(new Date(start_date));
            var daysInMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
            if (from_date.getDate() >= 16 && daysInMonth[from_date.getMonth()] != (from_date.getDate() + 16)) {
                $('#payments_to_date').val(from_date.getFullYear() + "-" + (from_date.getMonth() + 1) + "-" + daysInMonth[from_date.getMonth()]);
            } else {
                $('#payments_to_date').val(from_date.getFullYear() + "-" + (from_date.getMonth() + 1) + "-" + (from_date.getDate() + 14));
            }
        } else {
            $('#payments_to_date').val('');
        }
    });

    $('#payments_to_date').change(function() {
        var end_date = $('#payments_to_date').val();
        if (end_date != '') {
            $("#aggregator_payment_tab").hide();
            $("#download_payment_sheets").hide();
            $('#aggregator_payment_details').hide();
        } else {
            $('#payments_to_date').val('');
        }
    });

    $('#get_filter_data_button').click(function() {
        gaddidar = true;
        get_data();
    });
}


//To make a call when filters are changed
function get_filter_data(language) {
    $.get("/loop/filter_data/", {
            language: language
        })
        .done(function(data) {
            var data_json = JSON.parse(data);
            aggregators_for_filter = data_json.aggregators;
            mandis_for_filter = data_json.mandis;
            gaddidars_for_filter = data_json.gaddidars;
            crops_for_filter = data_json.crops;
            croplanguage_for_filter = data_json.croplanguage;
            transporter_for_filter = data_json.transporters;
            fill_aggregator_filter(aggregators_for_filter, language);
            fill_mandi_filter(mandis_for_filter, language);
            fill_gaddidar_filter(gaddidars_for_filter, language);
            if (language == ENGLISH_LANGUAGE)
                fill_crop_filter(croplanguage_for_filter);
            else
                fill_crop_filter(crops_for_filter);

            get_data();
        });
}


//To make aggregators list for filter page
function fill_aggregator_filter(data_json, language) {
    filter_remove_elements($('#aggregators'));
    if (language == ENGLISH_LANGUAGE) {
        $.each(data_json, function(index, data) {
            create_filter($('#aggregators'), data.user__id, data.name_en, true);
        });
    } else {
        $.each(data_json, function(index, data) {
            create_filter($('#aggregators'), data.user__id, data.name, true);
        });
    }
}

//To make crops list for filter page
function fill_crop_filter(data_json) {
    filter_remove_elements($('#crops'));
    $.each(data_json, function(index, data) {
        create_filter($('#crops'), data.id, data.crop_name, true);
    });
}

//To make mandis list for filter page
function fill_mandi_filter(data_json, language) {
    filter_remove_elements($('#mandis'));
    if (language == ENGLISH_LANGUAGE) {
        $.each(data_json, function(index, data) {
            create_filter($('#mandis'), data.id, data.mandi_name_en, true);
        });
    } else {
        $.each(data_json, function(index, data) {
            create_filter($('#mandis'), data.id, data.mandi_name, true);
        });
    }
}

//To make gaddidars list for filter page
function fill_gaddidar_filter(data_json, language) {
    filter_remove_elements($('#gaddidars'));
    if (language == ENGLISH_LANGUAGE) {
        $.each(data_json, function(index, data) {
            create_filter($('#gaddidars'), data.id, data.gaddidar_name_en, true);
        });
    } else {
        $.each(data_json, function(index, data) {
            create_filter($('#gaddidars'), data.id, data.gaddidar_name, true);
        });
    }
}

function filter_remove_elements(tbody_obj) {
    tbody_obj.empty();
}
//To enter data for aggregator, mandi,crop,gaddidar filter dynamically
function create_filter(tbody_obj, id, name, checked) {
    var row = $('<tr>');
    var td_name = $('<td>').html(name);
    row.append(td_name);
    var checkbox_html = '<input type="checkbox" class="black" data=' + id + ' id="' + name + id + '" checked="checked" value = "' + name + '" /><label for="' + name + id + '"></label>';
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
        $('#modal1').openModal();
    } else {
        $(".button-collapse1").sideNav('hide');
        get_data_for_bar_graphs(start_date, end_date, aggregator_ids, crop_ids, mandi_ids, gaddidar_ids);
        get_data_for_line_graphs(start_date, end_date, aggregator_ids, crop_ids, mandi_ids, gaddidar_ids);
    }
}

function get_data_for_bar_graphs(start_date, end_date, aggregator_ids, crop_ids, mandi_ids, gaddidar_ids) {
    $.get("/loop/data_for_drilldown_graphs/", {
            'start_date': start_date,
            'end_date': end_date,
            'aggregator_ids[]': aggregator_ids,
            'crop_ids[]': crop_ids,
            'mandi_ids[]': mandi_ids,
            'gaddidar_ids[]': gaddidar_ids
        })
        .done(function(data) {
            bar_graphs_json_data = JSON.parse(data);
            if (selected_page == ANALYTICS_PAGE) {
                PlotAnalyticsGraphs();
            }
        });
}


function update_graphs_aggregator_wise(chart) {
    if (chart == null) {
        aggregator_graph($('#aggregator_mandi'), aggregator_ids, aggregator_names, USER_CREATED__ID, mandi_ids, mandi_names, MANDI__ID, bar_graphs_json_data.aggregator_mandi, QUANTITY__SUM);
        cpk_spk_graph($('#mandi_cost'), aggregator_ids, aggregator_names, USER_CREATED__ID, mandi_ids, mandi_names, MANDI__ID, bar_graphs_json_data);
        repeat_farmers($('#farmers_count'), aggregator_ids, aggregator_names, USER_CREATED__ID, mandi_ids, mandi_names, MANDI__ID, bar_graphs_json_data.total_repeat_farmers);
    } else {
        if (chart == VOLUME) {
            aggregator_graph($('#aggregator_mandi'), aggregator_ids, aggregator_names, USER_CREATED__ID, mandi_ids, mandi_names, MANDI__ID, bar_graphs_json_data.aggregator_mandi, QUANTITY__SUM);
        } else if (chart == AMOUNT) {
            aggregator_graph($('#aggregator_mandi'), aggregator_ids, aggregator_names, USER_CREATED__ID, mandi_ids, mandi_names, MANDI__ID, bar_graphs_json_data.aggregator_mandi, AMOUNT__SUM);
        } else if (chart == VISITS) {
            aggregator_graph($('#aggregator_mandi'), aggregator_ids, aggregator_names, USER_CREATED__ID, mandi_ids, mandi_names, MANDI__ID, bar_graphs_json_data.aggregator_mandi, "mandi__id__count");
        }
        if (chart == "cost_recovered") {
            $('#2ndgraph').text("Total Cost");
            transport_cost_graph($('#mandi_cost'), aggregator_ids, aggregator_names, USER_CREATED__ID, mandi_ids, mandi_names, MANDI__ID, bar_graphs_json_data);
        } else if (chart == "cpk_spk") {
            $('#2ndgraph').text("Cost per kg");
            cpk_spk_graph($('#mandi_cost'), aggregator_ids, aggregator_names, USER_CREATED__ID, mandi_ids, mandi_names, MANDI__ID, bar_graphs_json_data);
        }
    }
}

function update_graphs_mandi_wise(chart) {
    if (chart == null) {
        aggregator_graph($('#aggregator_mandi'), mandi_ids, mandi_names, MANDI__ID, gaddidar_ids, gaddidar_names, 'gaddidar__id', bar_graphs_json_data.mandi_gaddidar, QUANTITY__SUM);
        cpk_spk_graph($('#mandi_cost'), mandi_ids, mandi_names, MANDI__ID, aggregator_ids, aggregator_names, USER_CREATED__ID, bar_graphs_json_data);
    } else {
        if (chart == VOLUME) {
            aggregator_graph($('#aggregator_mandi'), mandi_ids, mandi_names, MANDI__ID, gaddidar_ids, gaddidar_names, 'gaddidar__id', bar_graphs_json_data.mandi_gaddidar, QUANTITY__SUM);
        } else if (chart == AMOUNT) {
            aggregator_graph($('#aggregator_mandi'), mandi_ids, mandi_names, MANDI__ID, gaddidar_ids, gaddidar_names, 'gaddidar__id', bar_graphs_json_data.mandi_gaddidar, AMOUNT__SUM);
        } else if (chart == VISITS) {
            aggregator_graph($('#aggregator_mandi'), mandi_ids, mandi_names, MANDI__ID, aggregator_ids, aggregator_names, USER_CREATED__ID, bar_graphs_json_data.aggregator_mandi, "mandi__id__count");
        }
        if (chart == "cost_recovered") {
            transport_cost_graph($('#mandi_cost'), mandi_ids, mandi_names, MANDI__ID, aggregator_ids, aggregator_names, USER_CREATED__ID, bar_graphs_json_data);
        } else if (chart == "cpk_spk") {
            cpk_spk_graph($('#mandi_cost'), mandi_ids, mandi_names, MANDI__ID, aggregator_ids, aggregator_names, USER_CREATED__ID, bar_graphs_json_data);
        }
    }
}

function update_graphs_gaddidar_wise(chart) {
    if (chart == null) {
        selected_parameter = null;
        aggregator_graph($('#aggregator_gaddidar'), gaddidar_ids, gaddidar_names, 'gaddidar__id', aggregator_ids, aggregator_names, USER_CREATED__ID, bar_graphs_json_data.aggregator_gaddidar, QUANTITY__SUM);
    } else {
        if (chart == VOLUME) {
            selected_parameter = VOLUME;
            aggregator_graph($('#aggregator_gaddidar'), gaddidar_ids, gaddidar_names, 'gaddidar__id', aggregator_ids, aggregator_names, USER_CREATED__ID, bar_graphs_json_data.aggregator_gaddidar, QUANTITY__SUM);
        } else if (chart == AMOUNT) {
            selected_parameter = AMOUNT;
            aggregator_graph($('#aggregator_gaddidar'), gaddidar_ids, gaddidar_names, 'gaddidar__id', aggregator_ids, aggregator_names, USER_CREATED__ID, bar_graphs_json_data.aggregator_gaddidar, AMOUNT__SUM);
        }
    }
}

function update_graphs_crop_wise(chart) {
    if (chart == null) {
        aggregator_graph($('#aggregator_mandi'), crop_ids, crop_names, 'crop__id', mandi_ids, mandi_names, MANDI__ID, bar_graphs_json_data.mandi_crop, QUANTITY__SUM);
        max_min_graph($('#mandi_cost'), crop_ids, crop_names, 'crop__id', mandi_ids, mandi_names, MANDI__ID, bar_graphs_json_data);
        farmer_crop_visits($("#farmers_count"), bar_graphs_json_data.crop_prices);
    } else {
        if (chart == VOLUME) {
            aggregator_graph($('#aggregator_mandi'), crop_ids, crop_names, 'crop__id', mandi_ids, mandi_names, MANDI__ID, bar_graphs_json_data.mandi_crop, QUANTITY__SUM);
        } else if (chart == AMOUNT) {
            aggregator_graph($('#aggregator_mandi'), crop_ids, crop_names, 'crop__id', mandi_ids, mandi_names, MANDI__ID, bar_graphs_json_data.mandi_crop, AMOUNT__SUM);
        }
    }
}

function totals() {
    var total_volume = 0;
    var total_amount = 0;
    var total_visits = 0;
    var total_cost = 0;
    var total_recovered = 0;
    var gaddidar_share = 0;
    var volume_without_crop_gaddidar_filter = 0;
    var volume_amount_visits_data = bar_graphs_json_data.aggregator_mandi;
    var transport_data = bar_graphs_json_data.transportation_cost_mandi;
    var gaddidar_contribution = bar_graphs_json_data.gaddidar_contribution;

    for (var i = 0; i < volume_amount_visits_data.length; i++) {
        total_volume += volume_amount_visits_data[i][QUANTITY__SUM];
        total_amount += volume_amount_visits_data[i][AMOUNT__SUM];
        total_visits += volume_amount_visits_data[i]["mandi__id__count"];
    }

    for (var i = 0; i < transport_data.length; i++) {
        total_cost += transport_data[i]['transportation_cost__sum']
        total_recovered += transport_data[i]['farmer_share__sum'];
    }

    var gaddidar_contribution_length = gaddidar_contribution.length;
    for (var i = 0; i < gaddidar_contribution_length; i++) {
        gaddidar_share += gaddidar_contribution[i]['amount'];
        volume_without_crop_gaddidar_filter += gaddidar_contribution[i][QUANTITY__SUM];
    }

    var cpk = ((total_cost + volume_without_crop_gaddidar_filter * AGGREGATOR_INCENTIVE_PERCENTAGE) / volume_without_crop_gaddidar_filter).toFixed(2);
    var spk = ((total_recovered + gaddidar_share) / volume_without_crop_gaddidar_filter).toFixed(2);

    total_recovered += gaddidar_share;
    total_cost += volume_without_crop_gaddidar_filter * AGGREGATOR_INCENTIVE_PERCENTAGE;

    $("#aggregator_volume").text("Volume: " + parseFloat(total_volume).toFixed(0) + " " + KG);
    $("#aggregator_amount").text("amount: " + RUPEE + parseFloat(total_amount).toFixed(0));
    $("#aggregator_visits").text("visits: " + total_visits);
    $("#aggregator_cpk").text("SPK/CPK : " + spk + "/" + cpk);
    $("#aggregator_cost").text("Recovered/Total : " + RUPEE + total_recovered.toFixed(2) + "/ " + RUPEE + total_cost.toFixed(2));

}

//Volume, Amount, Visits graph on analytics page is being plotted from this
function aggregator_graph(container, axis, axis_names, axis_parameter, values, values_names, values_parameter, json_data, parameter) {
    var series = [];
    var drilldown = {};
    drilldown['series'] = [];

    var temp = {};
    temp['name'] = "Total";
    temp['type'] = "bar";
    temp['colorByPoint'] = false;
    temp['data'] = [];
    temp['pointWidth'] = 15;

    var main_series = new Array(axis.length).fill(0);
    var values_drilldown = [];

    for (var i = 0; i < axis.length; i++) {
        values_drilldown.push(new Array(values.length).fill(0));
    }

    for (var i = 0; i < json_data.length; i++) {
        var index = axis.indexOf(json_data[i][axis_parameter].toString());
        var drilldown_index = values.indexOf(json_data[i][values_parameter].toString());
        main_series[index] += json_data[i][parameter];
        values_drilldown[index][drilldown_index] += json_data[i][parameter];
    }

    for (var i = 0; i < axis.length; i++) {
        temp['data'].push({
            'name': axis_names[i],
            'y': main_series[i],
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
            if (values_drilldown[i][j] > 0) {
                drilldown['series'][i]['data'].push({
                    "name": values_names[j],
                    "y": values_drilldown[i][j]
                });
            }
        }
    }

    temp['showInLegend'] = false;
    series.push(temp);

    series[0]['data'].sort(function(a, b) {
        return b['y'] - a['y'];
    });

    for (var i = 0; i < drilldown['series'].length; i++) {
        drilldown['series'][i]['data'].sort(function(a, b) {
            return b['y'] - a['y'];
        });
    }
    plot_drilldown(container, series, drilldown, false);
}

//Recovered total graph on analytics page is being plotted from this
function transport_cost_graph(container, axis, axis_names, axis_parameter, values, values_names, values_parameter, json_data) {

    var transportation_cost_mandi = json_data.transportation_cost_mandi;
    var gaddidar_contribution = json_data.gaddidar_contribution;
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

    var values_cost = new Array(axis.length).fill(0);
    var values_cost_drilldown = [];
    var values_cost_recovered = new Array(axis.length).fill(0);
    var values_cost_recovered_drilldown = [];

    for (var i = 0; i < axis.length; i++) {
        values_cost_drilldown.push(new Array(values.length).fill(0));
        values_cost_recovered_drilldown.push(new Array(values.length).fill(0));
    }

    for (var i = 0; i < transportation_cost_mandi.length; i++) {
        var index = axis.indexOf(transportation_cost_mandi[i][axis_parameter].toString());
        var drilldown_index = values.indexOf(transportation_cost_mandi[i][values_parameter].toString());
        values_cost[index] += transportation_cost_mandi[i]['transportation_cost__sum'];
        values_cost_recovered[index] += transportation_cost_mandi[i]['farmer_share__sum'];
        values_cost_drilldown[index][drilldown_index] += transportation_cost_mandi[i]['transportation_cost__sum'];
        values_cost_recovered_drilldown[index][drilldown_index] += transportation_cost_mandi[i]['farmer_share__sum'];
    }

    var gaddidar_contribution_length = gaddidar_contribution.length;
    for (var i = 0; i < gaddidar_contribution_length; i++) {
        var index = axis.indexOf(gaddidar_contribution[i][axis_parameter].toString());
        var drilldown_index = values.indexOf(gaddidar_contribution[i][values_parameter].toString());
        values_cost[index] += (gaddidar_contribution[i][QUANTITY__SUM] * AGGREGATOR_INCENTIVE_PERCENTAGE);
        values_cost_recovered[index] += gaddidar_contribution[i]['amount'];
        values_cost_drilldown[index][drilldown_index] += (gaddidar_contribution[i][QUANTITY__SUM] * AGGREGATOR_INCENTIVE_PERCENTAGE);
        values_cost_recovered_drilldown[index][drilldown_index] += gaddidar_contribution[i]['amount'];
    }

    var data_for_sorting = [];
    for (var i = 0; i < axis.length; i++) {
        data_for_sorting.push({
            'name': axis_names[i],
            'cost': values_cost[i],
            'cost_recovered': values_cost_recovered[i]
        });
        drilldown['series'].push({
            'name': axis_names[i],
            'id': axis_names[i] + "cost",
            'data': [],
            'xAxis': 1,
            'pointWidth': 15
        });
        drilldown['series'].push({
            'name': axis_names[i],
            'id': axis_names[i] + "recovered",
            'data': [],
            'xAxis': 1,
            'pointWidth': 15
        });
        for (var j = 0; j < values.length; j++) {
            if (values_cost_drilldown[i][j] > 0) {
                drilldown['series'][i * 2]['data'].push([values_names[j], values_cost_drilldown[i][j]]);
                drilldown['series'][i * 2 + 1]['data'].push([values_names[j], values_cost_recovered_drilldown[i][j]]);
            }
        }
    }

    data_for_sorting.sort(function(a, b) {
        return (b['cost']) - (a['cost']);
    });

    for (var i = 0; i < axis.length; i++) {
        series[0]['data'].push({
            'name': data_for_sorting[i]['name'],
            'y': data_for_sorting[i]['cost'],
            'drilldown': data_for_sorting[i]['name'] + "cost"
        });
        series[1]['data'].push({
            'name': data_for_sorting[i]['name'],
            'y': data_for_sorting[i]['cost_recovered'],
            'drilldown': data_for_sorting[i]['name'] + "recovered"
        });
    }

    for (var i = 0; i < drilldown['series'].length; i++) {
        drilldown['series'][i]['data'].sort(function(a, b) {
            return b[1] - a[1];
        });
    }
    plot_drilldown(container, series, drilldown, false);
}

//Cpk and Spk on analytics page is being plotted from this
function cpk_spk_graph(container, axis, axis_names, axis_parameter, values, values_names, values_parameter, json_data) {
    //Not considering crops filter while calculating cpk and spk
    // var vol_stats = json_data.transactions_details_without_crops;
    //TODO: can merge vol_stats and gaddidar_shre_stats as the data is without applying crop filters
    var vol_stats = json_data.gaddidar_contribution;
    var cost_stats = json_data.transportation_cost_mandi;
    var gaddidar_share_stats = json_data.gaddidar_contribution;
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
        values_vol[index] += vol_stats[i][QUANTITY__SUM];
        values_vol_drilldown[index][drilldown_index] += vol_stats[i][QUANTITY__SUM];
    }
    for (var i = 0; i < cost_stats.length; i++) {
        var index = axis.indexOf(cost_stats[i][axis_parameter].toString());
        var drilldown_index = values.indexOf(cost_stats[i][values_parameter].toString());
        values_cost_cpk[index] += cost_stats[i]['transportation_cost__sum'];
        values_cost_spk[index] += cost_stats[i]['farmer_share__sum'];
        values_cost_cpk_drilldown[index][drilldown_index] += cost_stats[i]['transportation_cost__sum'];
        values_cost_spk_drilldown[index][drilldown_index] += cost_stats[i]['farmer_share__sum'];
    }

    for (var i = 0; i < gaddidar_share_stats.length; i++) {
        var index = axis.indexOf(gaddidar_share_stats[i][axis_parameter].toString());
        var drilldown_index = values.indexOf(gaddidar_share_stats[i][values_parameter].toString());
        values_cost_spk[index] += gaddidar_share_stats[i]['amount'];
        values_cost_spk_drilldown[index][drilldown_index] += gaddidar_share_stats[i]['amount'];
    }

    var data_for_sorting = [];
    for (var i = 0; i < axis.length; i++) {
        data_for_sorting.push({
            'name': axis_names[i],
            'cpk': values_vol[i] > 0 ? ((values_cost_cpk[i] + values_vol[i] * AGGREGATOR_INCENTIVE_PERCENTAGE) / values_vol[i]) : 0.0,
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
                drilldown['series'][i * 2]['data'].push([values_names[j], (values_cost_cpk_drilldown[i][j] + values_vol_drilldown[i][j] * AGGREGATOR_INCENTIVE_PERCENTAGE) / values_vol_drilldown[i][j]]);
                drilldown['series'][i * 2 + 1]['data'].push([values_names[j], values_cost_spk_drilldown[i][j] / values_vol_drilldown[i][j]]);
            }
        }
    }

    data_for_sorting.sort(function(a, b) {
        return (b['cpk']) - (a['cpk']);
    });

    for (var i = 0; i < axis.length; i++) {
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
            return b[1] - a[1];
        });
    }

    plot_drilldown(container, series, drilldown, true);
}

//Analytocs Aggregator tab to caluclate farmers count is being calculated from this
function repeat_farmers(container, axis, axis_names, axis_parameter, values, values_names, values_parameter, json_data) {
    var series = [];
    var drilldown = {};
    drilldown['allowPointDrilldown'] = false;
    drilldown['series'] = [];

    var temp_total = {};
    temp_total['name'] = "Total Farmers";
    temp_total['type'] = "bar";
    temp_total['showInLegend'] = false;
    temp_total['data'] = [];
    temp_total['pointPadding'] = 0.3;
    temp_total['pointPlacement'] = 0;
    temp_total['pointWidth'] = 15;

    var temp_repeat = {};
    temp_repeat['name'] = "Total Repeat Farmers";
    temp_repeat['type'] = "bar";
    temp_repeat['showInLegend'] = false;
    temp_repeat['data'] = [];
    temp_repeat['pointPadding'] = 0.4;
    temp_repeat['pointPlacement'] = 0;
    temp_repeat['pointWidth'] = 15;

    var data_for_sorting = [];

    for (var i = 0; i < axis.length; i++) {
        data_for_sorting.push({
            'name': axis_names[i],
            'total_farmers': 0,
            'total_repeat_farmers': 0
        });
        drilldown['series'].push({
            'name': axis_names[i],
            'id': axis_names[i],
            'data': []
        });
        for (var j = 1; j < 10; j++) {
            drilldown['series'][i]['data'].push(["" + j, 0]);
        }
        drilldown['series'][i]['data'].push(["10+", 0]);
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
            'y': data_for_sorting[i]['total_repeat_farmers'],
            'drilldown': data_for_sorting[i]['name']
        });
    }
    plot_drilldown(container, series, drilldown, false);
}

//Analytics Crops tab  Max Min graph is being plotted here
function max_min_graph(container, crop_ids, crop_names, crop_parameter, mandi_ids, mandi_names, mandi_parameter, json_data) {
    var json_data_crop = json_data.crop_prices;
    var json_data_mandi = json_data.mandi_crop_prices;

    var series = [];
    var drilldown = {};
    drilldown['series'] = [];

    var temp = {};
    temp['name'] = "Min_Max";
    temp['colorByPoint'] = false;
    temp['data'] = [];
    temp['pointWidth'] = 15;

    for (var i = 0; i < crop_ids.length; i++) {
        temp['data'].push({
            'name': crop_names[i],
            'low': 0,
            'high': 0,
            'drilldown': crop_names[i]
        });
        drilldown['series'].push({
            'name': crop_names[i],
            'id': crop_names[i],
            'data': [],
            'pointWidth': 15,
            'xAxis': 1
        });
        for (var j = 0; j < mandi_names.length; j++) {
            drilldown['series'][i]['data'].push({
                "name": mandi_names[j],
                "low": 0,
                "high": 0
            });
        }
    }
    temp['showInLegend'] = false;
    series.push(temp);

    for (var i = 0; i < json_data_mandi.length; i++) {
        var drilldown_index = mandi_ids.indexOf(json_data_mandi[i][mandi_parameter].toString());
        var index = crop_ids.indexOf(json_data_mandi[i][crop_parameter].toString());
        drilldown['series'][index]['data'][drilldown_index]['low'] = json_data_mandi[i]['price__min'];
        drilldown['series'][index]['data'][drilldown_index]['high'] = json_data_mandi[i]['price__max'];
    }
    var max_crop_price = 0;
    for (var i = 0; i < json_data_crop.length; i++) {
        var index = crop_ids.indexOf(json_data_crop[i][crop_parameter].toString());
        series[0]['data'][index]['low'] = json_data_crop[i]['price__min'];
        series[0]['data'][index]['high'] = json_data_crop[i]['price__max'];
        if (max_crop_price < json_data_crop[i]['price__max']) {
            max_crop_price = json_data_crop[i]['price__max'];
        }
    }
    for (var i = series[0]['data'].length - 1; i >= 0; i--) {
        if (series[0]['data'][i]['high'] == 0) {
            series[0]['data'].splice(i, 1);
            drilldown['series'].splice(i, 1);
        }
    }
    for (var i = 0; i < series[0]['data'].length; i++) {
        for (var j = drilldown['series'][i]['data'].length - 1; j >= 0; j--) {
            if (drilldown['series'][i]['data'][j]['high'] == 0) {
                drilldown['series'][i]['data'].splice(j, 1);
            }
        }
    }
    for (var i = 0; i < series[0]['data'].length; i++) {
        drilldown['series'][i]['data'].sort(function(a, b) {
            return (b['high'] - b['low']) - (a['high'] - a["low"]);
        });
    }
    series[0]['data'].sort(function(a, b) {
        return (b['high'] - b['low']) - (a['high'] - a["low"]);
    });
    plot_drilldown1(container, series, drilldown, false, max_crop_price);
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
        return (b['farmer__count']) - (a['farmer__count']);
    });
    series.push(temp_repeat);

    for (var i = 0; i < json_data.length; i++) {
        if (language == ENGLISH_LANGUAGE) {
            series[0]['data'].push([json_data[i]['crop__crop_name_en'], json_data[i]['farmer__count']]);
        } else {
            series[0]['data'].push([json_data[i]['crop__crop_name'], json_data[i]['farmer__count']]);
        }
    }
    plot_stacked_chart(container, series);
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
            if (selected_page == TIME_SERIES_PAGE) {
                PlotTimeSeriesGraphs();
            }
        });
}

//To fill crops name in drop down on Time series page
function fill_crop_drop_down() {
    var tbody_obj = $('#crop_max_min_avg');
    tbody_obj.html("");
    tbody_obj.append('<option value="" disabled selected> Choose a Crop </option>');
    var crops_names_time_series;
    if (language == ENGLISH_LANGUAGE)
        crops_names_time_series = croplanguage_for_filter;
    else
        crops_names_time_series = crops_for_filter;
    $.each(crops_names_time_series, function(index, data) {
        var li_item = '<option value=' + data.id + '>' + data.crop_name + '</option>';
        tbody_obj.append(li_item);
    });
    $('select').material_select();
}


//To show time series graohs for volumr,amount,farmer count, cpk,spk
function show_line_graphs() {
    var json_data = line_json_data.aggregator_data;
    // var farmer_data = line_json_data.farmer;
    var transport_data = line_json_data.transport_data;
    var dates_and_farmer_count = line_json_data.dates;
    var gaddidar_contribution = bar_graphs_json_data.gaddidar_contribution;
    var all_dates = [];

    try {
        var first_date = new Date(dates_and_farmer_count[0]['date']);
        while (first_date <= new Date(dates_and_farmer_count[dates_and_farmer_count.length - 1]['date'])) {
            all_dates.push(first_date.getTime());
            first_date.setDate(first_date.getDate() + 1);
        }
        time_series_volume_amount_farmers = [{
            'name': "Volume",
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
        }];

        time_series_cpk_spk = [{
            'name': "Cost per Kg",
            'type': 'areaspline',
            'data': [],
            'color': 'rgba(0,0,255,0.3)',
            'pointStart': all_dates[0],
            'pointInterval': 24 * 3600 * 1000
        }, {
            'name': "Sustainability per Kg",
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
            time_series_volume_amount_farmers[0]['data'][index][1] += json_data[i][QUANTITY__SUM];
            time_series_volume_amount_farmers[1]['data'][index][1] += json_data[i][AMOUNT__SUM];
        }
        transport_cost = new Array(all_dates.length).fill(0);
        farmer_share = new Array(all_dates.length).fill(0);

        for (var i = 0; i < transport_data.length; i++) {
            var index = all_dates.indexOf(new Date(transport_data[i]['date']).getTime());
            transport_cost[index] += transport_data[i]['transportation_cost__sum'];
            farmer_share[index] += transport_data[i]['farmer_share__sum'];
        }

        var gaddidar_contribution_length = gaddidar_contribution.length;
        for (var i = 0; i < gaddidar_contribution_length; i++) {
            var index = all_dates.indexOf(new Date(gaddidar_contribution[i]['date']).getTime());
            farmer_share[index] += gaddidar_contribution[i]['amount'];
        }
        for (var i = 0; i < all_dates.length; i++) {
            time_series_cpk_spk[0]['data'].push([all_dates[i], time_series_volume_amount_farmers[0]['data'][i][1] > 0 ? ((transport_cost[i] + time_series_volume_amount_farmers[0]['data'][i][1] * AGGREGATOR_INCENTIVE_PERCENTAGE) / time_series_volume_amount_farmers[0]['data'][i][1]) : null]);

            time_series_cpk_spk[1]['data'].push([all_dates[i], time_series_volume_amount_farmers[0]['data'][i][1] > 0 ? (farmer_share[i] / time_series_volume_amount_farmers[0]['data'][i][1]) : null]);
        }

        for (var i = 0; i < dates_and_farmer_count.length; i++) {
            var index = all_dates.indexOf(new Date(dates_and_farmer_count[i]['date']).getTime());
            time_series_volume_amount_farmers[2]['data'][index][1] += dates_and_farmer_count[i]['farmer__count'];
        }
        createMasterForVolAmtTimeSeries($('#detail_container_time_series'), $('#master_container_time_series'), time_series_volume_amount_farmers)
        createMasterForCpkSpkTimeSeries($('#detail_container_cpk'), $('#master_container_cpk'), time_series_cpk_spk);
    } catch (err) {
        alert("No Data is available for the current time period and filters applied.");
    }
}


//To show max, min , avg prices for crops in time series page
function crop_prices_graph(crop_id) {
    var json_data = line_json_data.crop_prices;
    var dates = line_json_data.dates;
    var all_dates = [];

    var first_date = new Date(dates[0]['date']);
    while (first_date <= new Date(dates[dates.length - 1]['date'])) {
        all_dates.push(first_date.getTime());
        first_date.setDate(first_date.getDate() + 1);
    }

    var series = [{
        'name': 'Range',
        'type': 'boxplot'
    }, {
        'name': 'Average Price',
        'type': 'line'
    }];

    var ranges = [];
    var avgs = [];

    for (var i = 0; i < all_dates.length; i++) {
        ranges.push([all_dates[i], null, null, null, null, null]);
        avgs.push([all_dates[i], null]);
    }

    var max_vol = 0;
    //By default selecting the crop with max volume
    if (crop_id == -1) {
        for (var i = 0; i < json_data.length; i++) {
            if (json_data[i][QUANTITY__SUM] > max_vol) {
                max_vol = json_data[i][QUANTITY__SUM];
                crop_id = json_data[i]['crop__id'].toString();
            }
        }
        $('#crop_max_min_avg option[value="' + crop_id + '"]').prop('selected', true);
        $('#crop_max_min_avg').material_select();
    }

    for (var i = 0; i < json_data.length; i++) {
        var index = all_dates.indexOf(new Date(json_data[i]['date']).getTime());

        if (json_data[i]['crop__id'].toString() == crop_id) {
            ranges[index][1] = json_data[i]['price__min'];
            var avg = json_data[i][AMOUNT__SUM] / json_data[i][QUANTITY__SUM];
            ranges[index][2] = avg;
            ranges[index][4] = avg;
            ranges[index][5] = json_data[i]['price__max'];
            avgs[index][1] = avg;
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
    var new_series = [];

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

    for (var i = 0; i < series.length; i++) {
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
    var new_series = [];

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
    for (var k = 0; k < series[0]['data'].length; k++) {
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
            height: 300
        },
        credits: {
            enabled: false
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
            enabled: true
        },
        yAxis: [{
            min: 0,
            title: {
                text: null
            },
            gridLineColor: 'transparent'
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
            zoomType: 'x'
        },
        credits: {
            enabled: false
        },
        exporting: {
            enabled: false
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
            gridLineColor: 'transparent'
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

function plot_drilldown1(container_obj, dict, drilldown, floats, max_scale) {
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
            type: 'columnrange',
            height: 300,
            inverted: true
        },
        exporting: {
            enabled: false
        },
        credits: {
            enabled: false
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
            max: max_scale,
            gridLineColor: 'transparent'
        },
        scrollbar: {
            enabled: true
        },
        legend: {
            enabled: false
        },
        plotOptions: {
            columnrange: {
                grouping: false,
                dataLabels: {
                    enabled: true,
                    format: format
                }
            }
        },
        series: dict,
        drilldown: drilldown
    });
}

function createDetailForCummulativeVolumeAndFarmer(detail_container, masterChart, dict) {
    // prepare the detail chart
    var myDict = [];
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
    // width = detail_container.width();
    detailChart = detail_container.highcharts({
        chart: {
            // width: width
        },
        title: {
            text: "Volume and Farmers Cummulative Count"
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
            maxZoom: 0.1
        }, {
            title: {
                text: null
            },
            opposite: true
        }],
        tooltip: {
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
            shadow: true
        },
        series: myDict,

        exporting: {
            enabled: false
        }

    }).highcharts(); // return chart
}

// create the master chart
function createMasterForCummulativeVolumeAndFarmer(detail_container, master_container, dict) {
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
            createDetailForCummulativeVolumeAndFarmer(detail_container, masterChart, dict);
        })
        .highcharts(); // return chart instance
}

function createDetailForVolAmtTimeSeries(detail_container, masterChart, dict) {

    // prepare the detail chart
    var myDict = [];
    var detailData = [],
        detailStart = dict[0]['data'][0][0];

    $.each(masterChart.series, function() {
        if (this.name == "Volume") {
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
        myDict.push(temp);

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
            maxZoom: 0.1

        }, {
            title: {
                text: null
            },
            opposite: true
        }],
        tooltip: {
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
            align: 'center',
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
function createMasterForVolAmtTimeSeries(detail_container, master_container, dict) {
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
            createDetailForVolAmtTimeSeries(detail_container, masterChart, dict);
        })
        .highcharts(); // return chart instance
}

function createDetailForCpkSpkTimeSeries(detail_container, masterChart, dict) {
    // prepare the detail chart
    var myDict = []
    var detailData = [],
        detailStart = dict[0]['data'][0][0];

    $.each(masterChart.series, function() {
        if (this.name == "Volume") {
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
            maxZoom: 0.1
        }, {
            title: {
                text: null
            },
            opposite: true
        }],
        tooltip: {
            valueDecimals: 2,
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
            align: 'center',
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
function createMasterForCpkSpkTimeSeries(detail_container, master_container, dict) {
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
            createDetailForCpkSpkTimeSeries(detail_container, masterChart, dict);
        })
        .highcharts(); // return chart instance
}


function plot_area_range_graph(container, dict) {
    //Initially width of container3 is 0
    container_width = $("#container3").width();
    if (container_width == 0) {
        container_width = $("#container2").width();
    }
    container.highcharts({
        chart: {
            zoomType: 'x',
            width: container_width
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
            min: 0
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
    tbody_obj.append('<option value="" disabled selected> Choose ' + caption + ' </option>');
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
    var gaddidar_contribution_data = payments_data.gaddidar_data;
    // var gaddidar_payment = payments_data.gaddidar_data;

    var sno = 1;
    aggregator_data_set = [];
    gaddidar_data_set = [];
    transporter_data_set = [];
    var dates = [];
    var mandis = [];
    var quantites = [];
    var gaddidar_amount = [];
    var farmers = [];
    var transport_cost = [];
    var farmer_share = [];
    for (var i = 0; i < aggregator_payment.length; i++) {
        if (aggregator == aggregator_payment[i][USER_CREATED__ID].toString()) {
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
            quantites[date_index][mandi_index] += aggregator_payment[i][QUANTITY__SUM];
            gaddidar_amount[date_index][mandi_index] += aggregator_payment[i][QUANTITY__SUM] * aggregator_payment[i]['gaddidar__commission'];
            farmers[date_index][mandi_index] += aggregator_payment[i]['farmer__count'];

            gaddidar_data_set.push([aggregator_payment[i]['date'], aggregator_payment[i]['gaddidar__gaddidar_name'], aggregator_payment[i]['mandi__mandi_name'], parseFloat(aggregator_payment[i][QUANTITY__SUM].toFixed(2)), 0, 0]);
        }
    }

    var gaddidar_contribution_data_length = gaddidar_contribution_data.length;
    for (var i = 0; i < gaddidar_contribution_data_length; i++) {
        if (aggregator == payments_gaddidar_contribution[i][USER_CREATED__ID].toString()) {
            for (var j = 0; j < gaddidar_data_set.length; j++) {
                if (gaddidar_data_set[j].indexOf(payments_gaddidar_contribution[i]['date']) != -1 &&
                    gaddidar_data_set[j].indexOf(payments_gaddidar_contribution[i]['gaddidar__name']) != -1) {
                    gaddidar_data_set[j][4] = parseFloat(payments_gaddidar_contribution[i]['gaddidar_discount'].toFixed(2));
                    gaddidar_data_set[j][5] = parseFloat(payments_gaddidar_contribution[i]['amount'].toFixed(2));
                }
            }
        }
    }

    for (var i = 0; i < transport_payment.length; i++) {
        if (aggregator == transport_payment[i][USER_CREATED__ID].toString()) {
            date_index = dates.indexOf(transport_payment[i]['date']);
            mandi_index = mandis[date_index].indexOf(transport_payment[i]['mandi__mandi_name']);
            transport_cost[date_index][mandi_index] += transport_payment[i]['transportation_cost__sum'];
            farmer_share[date_index][mandi_index] = transport_payment[i]['farmer_share'];

            transporter_data_set.push([transport_payment[i]['date'], transport_payment[i]['mandi__mandi_name'], transport_payment[i]['transportation_vehicle__transporter__transporter_name'], transport_payment[i]['transportation_vehicle__vehicle__vehicle_name'], transport_payment[i]['transportation_vehicle__vehicle_number'], parseFloat(transport_payment[i]['transportation_cost__sum'].toFixed(2))]);
        }
    }

    var total_volume = 0;
    var total_payment = 0;
    for (var i = 0; i < dates.length; i++) {
        for (var j = 0; j < mandis[i].length; j++) {
            var net_payment = (quantites[i][j] * AGGREGATOR_INCENTIVE_PERCENTAGE) + transport_cost[i][j] - farmer_share[i][j];
            aggregator_data_set.push([sno.toString(), dates[i], mandis[i][j], parseFloat(quantites[i][j].toFixed(2)), parseFloat((quantites[i][j] * AGGREGATOR_INCENTIVE_PERCENTAGE).toFixed(2)), transport_cost[i][j], farmer_share[i][j], 0, parseFloat(net_payment.toFixed(2))]);
            sno += 1;
        }
    }

    for (var i = 0; i < gaddidar_contribution_data_length; i++) {
        if (aggregator == payments_gaddidar_contribution[i][USER_CREATED__ID].toString()) {
            for (var j = 0; j < aggregator_data_set.length; j++) {
                if (aggregator_data_set[j].indexOf(payments_gaddidar_contribution[i]['date']) != -1 && aggregator_data_set[j].indexOf(payments_gaddidar_contribution[i]['mandi__name']) != -1) {
                    aggregator_data_set[j][7] += parseFloat(payments_gaddidar_contribution[i]['amount']);
                    aggregator_data_set[j][8] = parseFloat((aggregator_data_set[j][8] - parseFloat(payments_gaddidar_contribution[i]['amount'])).toFixed(2));
                    break;
                }
            }
        }
    }


    

    var formatVal = function (yourNumber) {
    //Seperates the components of the number
        var n= yourNumber.toString().split(".");
    //Comma-fies the first part
        if(n[0])
            {
                n[0] = n[0].replace(/\B(?=(\d{3})+(?!\d))/g, ","); //convert numbers of the form 1156 -> 1,156
            }
            if(n[1] != null)
            {
                var a = n[1].toString();
                n[1] = parseInt(a.charAt(0));
            }
            return n.join(".");
        }


    var finalFormat = function (value){
        if(value.indexOf('.') === -1)
            return parseFloat(value).toLocaleString() + '.00';
        else
            return parseFloat(parseFloat(value).toFixed(2)).toLocaleString();
    }


      $('#table2').DataTable({
        destroy: true,
        data: aggregator_data_set,
        columns: [{
            title: "S No"
        }, {
            title: "Date"
        }, {
            title: "Market"
        }, {
            title: "Quantity[Q] (in Kg)"
        }, {
            title: "Aggregator Payment[AP] (in Rs) (0.25*Q)"
        }, {
            title: "Transport Cost[TC] (in Rs)"
        }, {
            title: "Farmers' Contribution[FC] (in Rs)"
        }, {
            title: "Commission Agent Contribution[CAC] (in Rs)"
        }, {
            title: "Total Payment(in Rs) (AP + TC - FC - CAC)"
        }],
        "dom": 'T<"clear">rtip',
        "pageLength": 2,
        "oTableTools": {
            "sSwfPath": "/media/social_website/scripts/libs/tabletools_media/swf/copy_csv_xls_pdf.swf",
            "aButtons": [{
                "sExtends": "csv",
                "sButtonText": "Download",
                "bBomInc": true,
                "sTitle": "Loop_India_Bihar_Aggregator Payment_" + getFormattedDate(aggregator) + "Payment Summary"
            }]
        },
       
        "footerCallback": function ( row, data, start, end, display ) {
            var api = this.api(), data;

            //Total of every column    
            column_set = [3,4,5,6,7,8];
            for(var i=0; i<column_set.length; i++)
            {
                total = api.column( column_set[i]).data().reduce( function (a, b) {
                            return a + b;
                        }, 0 );
                $( api.column( column_set[i]).footer() ).html(finalFormat(total+""));
            }

        }
    });

    

    $('#table3').DataTable({
        destroy: true,
        data: gaddidar_data_set,
        columns: [{
            title: "Date"
        }, {
            title: "Commission Agent"
        }, {
            title: "Market"
        }, {
            title: "Quantity[Q] (in Kg)"
        }, {
            title: "Commission Agent Discount[CAD] (in Rs/Kg)"
        }, {
            title: "Commission Agent Contribution[CAC] (in Rs) (Q*CAD)"
        }],
        "dom": 'T<"clear">rtip',
        "pageLength": 2,
        "oTableTools": {
            "sSwfPath": "/media/social_website/scripts/libs/tabletools_media/swf/copy_csv_xls_pdf.swf",
            "aButtons": [{
                "sExtends": "csv",
                "sButtonText": "Download",
                "bBomInc": true,
                "sTitle": "Loop_India_Bihar_Aggregator Payment_" + getFormattedDate(aggregator) + "Commission Agent Details"
            }]
        },
        
        "footerCallback": function ( row, data, start, end, display ) {
            var api = this.api(), data;
        
            //Total of every column    
            column_set = [3,5];
            for(var i=0; i<column_set.length; i++)
            {
                total = api.column( column_set[i]).data().reduce( function (a, b) {
                            return a + b;
                        }, 0 );
                $( api.column( column_set[i]).footer() ).html(finalFormat(total+""));
            }

        }

    });
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
            title: "Vehicle Type"
        }, {
            title: "Vehicle Number"
        }, {
            title: "Transport Cost (in Rs)"
        }],
        "dom": 'T<"clear">rtip',
        "pageLength": 2,
        "oTableTools": {
            "sSwfPath": "/media/social_website/scripts/libs/tabletools_media/swf/copy_csv_xls_pdf.swf",
            "aButtons": [{
                "sExtends": "csv",
                "sButtonText": "Download",
                "bBomInc": true,
                "sTitle": "Loop_India_Bihar_Aggregator Payment_" + getFormattedDate(aggregator) + "Transporter Details"
            }]
        },
        "footerCallback": function ( row, data, start, end, display ) {
            var api = this.api(), data;

            // Total over all pages
            total5 = api
                .column( 5 )
                .data()
                .reduce( function (a, b) {
                    return a + b;
                }, 0 );
           
            // Update footer
            $( api.column( 5 ).footer() ).html(
                finalFormat(total5+"")
            );

        }

    });

    aggregator_sheet_name = "Aggregator Payment_" + getFormattedDate(aggregator) + "Payment Summary";
    gaddidar_sheet_name = "Aggregator Payment_" + getFormattedDate(aggregator) + "Commission Agent Details";
    transporter_sheet_name = "Aggregator Payment_" + getFormattedDate(aggregator) + "Transporter Details";

}

function getFormattedDate(aggregator_id) {
    var monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "June",
        "July", "Aug", "Sept", "Oct", "Nov", "Dec"
    ];
    var aggregator_index = aggregator_ids.indexOf(aggregator_id);
    var name = aggregator_names[aggregator_index];
    var fromDate = new Date(payments_start_date);
    var toDate = new Date(payments_to_date);
    var str = name + "_" + monthNames[fromDate.getMonth()] + fromDate.getDate() + " to " + monthNames[toDate.getMonth()] + toDate.getDate() + "_";
    return str;
}

//To get data for aggregator, transporter, gaddidar payment sheets from server for specified time period
function get_payments_data() {
    payments_start_date = $("#payments_from_date").val();
    payments_to_date = $("#payments_to_date").val();
    if (payments_start_date != "" && payments_to_date != "" && Date.parse(payments_start_date) < Date.parse(payments_to_date) && new Date(payments_start_date) < new Date(payments_to_date) && new Date(payments_to_date) - new Date(payments_start_date) <= 1296000000) {
        $.get("/loop/payments/", {
            'start_date': payments_start_date,
            'end_date': payments_to_date
        }).done(function(data) {
            $('#aggregator_payment_tab').show();

            payments_data = JSON.parse(data);
            outliers_data = payments_data.outlier_data;
            outliers_transport_data = payments_data.outlier_transport_data;
            outlier_daily_data = payments_data.outlier_daily_data;
            payments_gaddidar_contribution = payments_data.gaddidar_data;
            fill_drop_down($('#aggregator_payments'), aggregators_for_filter, 'user__id', 'name', 'Aggregator');

        });
    } else {
        alert("Please select valid date range \n 1. Date Range should not exceed 15 days. \n 2. Please make sure that <To> date is after <From> date.");
    }
}

//To create table for 15 elements of outliers
function outliers_summary(aggregator_id) {
    var start_date = new Date(payments_start_date);
    var start_date_time = new Date(start_date.getFullYear() + "-" + (start_date.getMonth() + 1) + "-" + start_date.getDate()).getTime();
    var diff = start_date.getTime() - start_date_time;
    var end_date = new Date(payments_to_date);
    var dates = [];
    while (start_date.getTime() <= (end_date.getTime() + diff)) {
        dates.push(start_date.getTime());
        start_date.setDate(start_date.getDate() + 1);
    }

    var quantites = new Array(dates.length).fill(0);
    var farmers = new Array(dates.length).fill(0);

    for (var i = 0; i < outliers_data.length; i++) {
        if (aggregator_id == outliers_data[i][USER_CREATED__ID]) {
            var index = dates.indexOf(new Date(outliers_data[i]['date']).getTime());
            quantites[index] += (outliers_data[i][QUANTITY__SUM]);
            farmers[index] += (outliers_data[i]['farmer__count']);
        }
    }

    transport_data = new Array(dates.length).fill(0);

    for (var i = 0; i < outliers_transport_data.length; i++) {
        if (aggregator_id == outliers_transport_data[i][USER_CREATED__ID]) {
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

    for (var i = 0; i < outliers_data.length; i++) {
        if (new Date(date).getTime() == new Date(outliers_data[i]['date']).getTime() && aggregator_id == outliers_data[i][USER_CREATED__ID]) {

            data_set.push(["", sno, outliers_data[i]['date'], outliers_data[i]['mandi__mandi_name'], outliers_data[i]['farmer__count'], outliers_data[i][QUANTITY__SUM], 0, 0, 0]);
            //parameters are transportation cost,farmer share and gaddidar contribution sum
            sno += 1;
        }
    }

    var transportation_length = outliers_transport_data.length;
    for (var i = 0; i < transportation_length; i++) {
        if (new Date(date).getTime() == new Date(outliers_transport_data[i]['date']).getTime() && aggregator_id == outliers_transport_data[i][USER_CREATED__ID]) {
            for (var j = 0; j < data_set.length; j++) {
                if (data_set[j].indexOf(outliers_transport_data[i]['mandi__mandi_name']) != -1) {
                    data_set[j][6] = outliers_transport_data[i]['transportation_cost__sum'];
                    data_set[j][7] = outliers_transport_data[i]['farmer_share__sum'];
                }
            }
        }
    }

    var gaddidar_contribution_length = payments_gaddidar_contribution.length;
    for (var i = 0; i < gaddidar_contribution_length; i++) {
        if (new Date(date).getTime() == new Date(payments_gaddidar_contribution[i]['date']).getTime() && aggregator_id == payments_gaddidar_contribution[i][USER_CREATED__ID]) {
            for (var j = 0; j < data_set.length; j++) {
                if (data_set[j].indexOf(payments_gaddidar_contribution[i]['mandi__name']) != -1) {
                    data_set[j][8] += payments_gaddidar_contribution[i]['amount'];
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
            title: "Gaddidar Discount"
        }],
        "dom": '<"clear">'
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
        if (new Date(d[2]).getTime() == new Date(outlier_daily_data[i]['date']).getTime() && d[3] == outlier_daily_data[i]['mandi__mandi_name'] && aggregator_id == outlier_daily_data[i][USER_CREATED__ID]) {
            data_set.push([sno, d[2], outlier_daily_data[i]['gaddidar__gaddidar_name'], outlier_daily_data[i]['farmer__name'], outlier_daily_data[i]['crop__crop_name'], outlier_daily_data[i][QUANTITY__SUM], outlier_daily_data[i]['price'], 0]);
            sno += 1;
        }
    }

    var gaddidar_contribution_length = payments_gaddidar_contribution.length;
    for (var i = 0; i < gaddidar_contribution_length; i++) {
        if (new Date(d[2]).getTime() == new Date(payments_gaddidar_contribution[i]['date']).getTime() && aggregator_id == payments_gaddidar_contribution[i][USER_CREATED__ID]) {
            for (var j = 0; j < data_set.length; j++) {
                if (data_set[j].indexOf(payments_gaddidar_contribution[i]['gaddidar__name'])!=-1) {
                    data_set[j][7] = payments_gaddidar_contribution[i]['gaddidar_discount'];
                }
            }
        }
    }

    detailed_table.DataTable({
        destroy: true,
        data: data_set,
        columns: [{
            title: "S No"
        }, {
            title: "Date"
        }, {
            title: "Gaddidar"
        }, {
            title: "Farmers"
        }, {
            title: "Crop"
        }, {
            title: "Quantity"
        }, {
            title: "Price"
        }, {
            title: "Discount Rate"
        }],
        "dom": 'T<"clear">rtip'
    });
    return detailed_table;
}

function plot_solid_guage(container, minimum, present, target) {
    var gaugeOptions = {
        chart: {
            type: 'solidgauge',
            width: 180,
            height: 100,
            plotBackgroundColor: null,
            plotBackgroundImage: null,
            plotBorderWidth: 0,
            plotShadow: false,
            margin: [-10, 0, 0, 0]
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
                [0.1, '#DF5353'],
                [0.5, '#DDDF0D'],
                [0.9, '#55BF3B']
            ],
            lineWidth: 0,
            minorTickInterval: null,
            tickPixelInterval: 400,
            tickWidth: 0,
            // tickAmount:2,
            title: {
                y: -70
            },
            labels: {
                y: 16
            }
        },
        plotOptions: {
            solidgauge: {
                // innerRadius: '75%',
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
            min: minimum,
            max: target
        },
        credits: {
            enabled: false
        },
        series: [{
            name: 'Present',
            data: [present],
            dataLabels: {
                format: '<div style="text-align:center"><span style="font-size:16px;color:' +
                    ((Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black') + '">' + present.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") + '</span><br/>' +
                    '</div>'
            },
            tooltip: {
                valueSuffix: null
            }
        }]
    }));
}

function change_language(lang) {
    language = lang;
    fill_aggregator_filter(aggregators_for_filter, language);
    fill_mandi_filter(mandis_for_filter, language);
    fill_gaddidar_filter(gaddidars_for_filter, language);
    if (language == ENGLISH_LANGUAGE)
        fill_crop_filter(croplanguage_for_filter);
    else
        fill_crop_filter(crops_for_filter);
    get_data();
    if (selected_page == ANALYTICS_PAGE || selected_page == TIME_SERIES_PAGE) {
        show_nav(selected_page);
    }
}



/* This file should contain all the JS for Loop dashboard */
window.onload = initialize;

var language, selected_tab, selected_parameter, selected_page, country_id = 1;
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
//TODO : TO be removed
var AGGREGATOR_INCENTIVE_PERCENTAGE = 0.25;
var ENGLISH_LANGUAGE = "English";
var REGIONAL_LANGUAGE = "Regional";
var HOME = "home";
var PAYMENTS_PAGE = "payments";
var ANALYTICS_PAGE = "analytics";
var TIME_SERIES_PAGE = "time_series";
var RUPEE = "₹ ";
var TAKA = "৳ ";
var CURRENCY = RUPEE;
var HINDI_ID = 1;
var BANGLA_ID = 3;

var KG = " Kg";

var VOLUME = "volume",
  MANDI = "mandi",
  VISITS = "visits",
  CROP = "crop",
  AGGREGATOR = "aggregator",
  AMOUNT = "amount";
var QUANTITY__SUM = "quantity__sum",
  AMOUNT__SUM = "amount__sum",
  MANDI__ID = "mandi__id",
  USER_CREATED__ID = "user_created__id",
  GADDIDAR__ID = "gaddidar__id";
var MASTER_HOME = 3,
  MASTER_TIME_SERIES_VOL_AMT = 1,
  MASTER_TIME_SERIES_CPK_SPK = 2;

var aggregator_sheet_name = "",
  gaddidar_sheet_name = "",
  transporter_sheet_name = "";

var globalApi;
var initialLoadComplete;
var gaddidar, table_created;
var dates, stats, transportation, gaddidar_contribution_recent_graph, aggregator_incentive_cost;
var detailChartHome, detailChartTimeSeriesVol, detailChartTimeSeriesCPK;
var superEditMode = 0;

function initialize() {
  initialLoadComplete = false;
  language = ENGLISH_LANGUAGE;
  $("select").material_select();
  $(".button-collapse").sideNav({
    closeOnClick: true
  });
  $(".button-collapse1").sideNav();
  $("#totalpaytext").text("Payments("+CURRENCY+")");
  $("#recentpaytext").text("Payments("+CURRENCY+")");
  var today = new Date();
  $("#to_date").val(today.getFullYear() + "-" + (today.getMonth() + 1) + "-" + today.getDate());
  $("#to_date_drawer").val(today.getFullYear() + "-" + (today.getMonth() + 1) + "-" + today.getDate());
  today.setDate(today.getDate() - 15);
  $("#from_date").val(today.getFullYear() + "-" + (today.getMonth() + 1) + "-" + today.getDate());
  $("#from_date_drawer").val(today.getFullYear() + "-" + (today.getMonth() + 1) + "-" + today.getDate());
  showLoader();
  total_static_data(country_id);
  recent_graphs_data(language, country_id);
  days_to_average = 15;

  gaddidar = true;
  selected_tab = AGGREGATOR;
  selected_parameter = VOLUME;
  selected_page = HOME;

  time_series_frequency = 1;

  get_filter_data(language, country_id);
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
  if (tab == HOME && selected_page == PAYMENTS_PAGE && ($('#ToolTables_table2_1').length || $('#ToolTables_table3_1').length) && (!$('#ToolTables_table2_1').hasClass('disable-button') || !$('#ToolTables_table3_1').hasClass('disable-button')))
    var answer = confirm('You have Unsaved Changes. Do you want to stay on this page?');
  if (answer) {
    tab = PAYMENTS_PAGE;
  }
  if (tab == HOME) {
    $('#login_modal').closeModal();
    $("#home_div").show();
    $("#home_tab").addClass('active');
    selected_page = HOME;
  } else if (tab == PAYMENTS_PAGE && initialLoadComplete) {
    selected_page = PAYMENTS_PAGE;
    if (window.localStorage.login_timestamp != null && parseInt(window.localStorage.login_timestamp) + 86400 * 1000 >= new Date().getTime()) {
      $("#payments_div").show();
      $("#payments_tab").addClass('active');
    } else {
      window.localStorage.clear();
      $('#login_modal').openModal({
        dismissible: false
      });
      $('#loginbtn').click(function() {
        var username = $('#username').val().trim();
        var password = $('#password').val().trim();
        if (username.length == 0 || password.length == 0) {
          $('#error_div').show();
          document.getElementById('error_message').innerHTML = "* Username and Password are required fields.";
        } else {
          $.post("/loop/login/", {
            'username': username,
            'password': password
          }).done(function(data) {
            var login_data = JSON.parse(data);
            window.localStorage.name = login_data['user_name'];
            window.localStorage.akey = login_data['key'];
            window.localStorage.user_id = login_data['user_id'];
            globalApi = login_data['key'];
            window.localStorage.login_timestamp = new Date().getTime();
            if (localStorage.akey != null) {
              $('#login_modal').closeModal();
              $("#payments_div").show();
              $("#payments_tab").addClass('active');
            }
          }).fail(function() {
            $('#error_div').show();
            document.getElementById('error_message').innerHTML = "Incorrect username or password.";
          });
        }
      });
      $('#goto_home').click(function() {
        hide_nav(HOME);
      });
    }
  }
}
//To show the second navigation bar that comes on analytics and time series page only
function show_nav(tab) {
  if (initialLoadComplete) {
    $("#home_tab").removeClass('active');
    $("#payments_tab").removeClass('active');
    $("#analytics_tab").removeClass('active');
    $("#time_series_tab").removeClass('active');
    $("#filters_nav").removeClass('hide');
    $("#filters_nav").addClass('show');
    $("#home_div").hide();
    $("#payments_div").hide();
    $('#login_modal').closeModal();
    if (selected_page == PAYMENTS_PAGE && ($('#ToolTables_table2_1').length || $('#ToolTables_table3_1').length) && (!$('#ToolTables_table2_1').hasClass('disable-button') || !$('#ToolTables_table3_1').hasClass('disable-button')))
      var answer = confirm('You have Unsaved Changes. Do you want to stay on this page?');
    if (answer) {
      hide_nav(PAYMENTS_PAGE);
      tab = PAYMENTS_PAGE;
    }
    //if login modal is being shown disable it.

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

var bullet_options = {
  type: "bullet",
  width: "100",
  height: "30",
  performanceColor: '#00bfbf',
  rangeColors: ['#a2d6d6'],
  targetColor: '#ffffff'
}

var sparkline_option = {
  type: 'line',
  width: '150',
  height: '60',
  lineColor: '#00bfbf',
  fillColor: '#dde1df',
  lineWidth: 2
}

var generalOptions = {
  title: {
    text: null
  },
  subtitle: {
    text: null
  },
  legend: {
    enabled: false
  },
  credits: {
    enabled: false
  },
  exporting: {
    enabled: false
  }
}

var timeSeriesMasterOptions = {
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
  plotOptions: {
    series: {
      fillColor: {
        linearGradient: [0, 0, 0, 70],
        stops: [
          // [0, Highcharts.getOptions().colors[0]],
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
  }
}
var timeSeriesDetailOptions = {
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
    enabled: true,
    align: 'center',
    x: 0,
    verticalAlign: 'top',
    y: 0,
    floating: true,
    borderColor: '#CCC',
    borderWidth: 1,
    shadow: false
  }
}

var drilldownGraphOptions = {
  chart: {
    height: 300,
    zoomType: 'x'
  },
  yAxis: {
    title: {
      text: null
    },
    min: 0,
    gridLineColor: 'transparent'
  },
  scrollbar: {
    enabled: true
  },
  tooltip: {
    headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
  }
}


//To compute data for home page overall cards
function total_static_data(country_id) {
  $.get("/loop/total_static_data/", {
    'country_id': country_id
  }).done(function(data) {
    hideLoader();
    var json_data = JSON.parse(data);

    var total_volume = json_data['aggregated_result']['quantity'][0];
    var total_amount = json_data['aggregated_result']['amount'][0];
    var total_farmers_reached = json_data['total_farmers_reached'];
    var total_transportation_cost = json_data['aggregated_result']['transportation_cost'][0];
    var total_farmer_share = json_data['aggregated_result']['farmer_share'][0];
    var total_gaddidar_contribution = json_data['aggregated_result']['gaddidar_share'][0];
    var total_aggregator_cost = json_data['aggregated_result']['aggregator_incentive'][0];

    var sustainability = (parseFloat(total_farmer_share) + parseFloat(total_gaddidar_contribution)) / (parseFloat(total_transportation_cost) + parseFloat(total_aggregator_cost)) * 100;

    var clusters = json_data['total_cluster_reached'];
    var total_cpk = (parseFloat(total_transportation_cost) + parseFloat(total_aggregator_cost)) / parseFloat(total_volume);

    plot_solid_guage($('#cluster_bullet'), 0, clusters, 50);
    plot_solid_guage($('#total_farmers_bullet'), 0, total_farmers_reached, 5000);
    plot_solid_guage($('#total_volume_bullet'), 0, parseInt(total_volume), 5000000);
    plot_solid_guage($('#revenue_bullet'), 0, parseInt(total_amount), 50000000);
    plot_solid_guage($('#total_expenditure_bullet'), -1, parseFloat(0 - total_cpk.toFixed(2)), 0);
    plot_solid_guage($('#sustainability_bullet'), 0, parseFloat(sustainability.toFixed(2)), 50);
  });
}

//To request data for recent graphs on home page
function recent_graphs_data(language, country_id) {
  $.get("/loop/recent_graphs_data/", {
    'country_id': country_id
  }).done(function(data) {
    var json_data = JSON.parse(data.replace(/\bNaN\b/g, 0));
    aggregated_result = json_data['aggregated_result'];
    plot_cards_data();
    cummulative_farmer_and_volume(json_data['cummulative_vol_farmer']);
    initialLoadComplete = true;
  });
}

//To plot and show data for recents graphs on home page
function plot_cards_data() {
  var days_by_group = aggregated_result[days_to_average];
  var len_group = days_by_group.length;
  var c_vol = [];
  var c_amt = [];
  var c_cpk = [],
    c_sustainability = [],
    c_active_clusters = [],
    c_active_farmers = [];
  for (var i = 0; i < len_group; i++) {
    var active_cluster = days_by_group[i]['active_cluster'];
    var farmer_count = days_by_group[i]['distinct_farmer_count'];
    var vol = parseFloat(days_by_group[i][QUANTITY__SUM]);
    var amt = parseFloat(days_by_group[i][AMOUNT__SUM]);
    var cost = parseFloat(days_by_group[i]['transportation_cost__sum']) + parseFloat(days_by_group[i]['aggregator_incentive__sum']);
    var recovered = parseFloat(days_by_group[i]['farmer_share__sum']) + parseFloat(days_by_group[i]['gaddidar_share__sum']);
    var cpk = parseFloat(cost) / parseFloat(vol);
    var spk = (parseFloat(recovered) / parseFloat(cost)) * 100;
    c_vol.push(vol);
    c_amt.push(amt);
    c_cpk.push(cpk.toFixed(2));
    c_sustainability.push(spk.toFixed(2));
    c_active_clusters.push(active_cluster);
    c_active_farmers.push(farmer_count)
  }
  document.getElementById('recent_cluster_card').innerHTML = '&nbsp;&nbsp;&nbsp;' + c_active_clusters[0];
  $("#recent_cluster_sparkline").sparkline(c_active_clusters.reverse(), sparkline_option);

  document.getElementById('recent_volume_card').innerHTML = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + (c_vol[0].toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")).concat(KG);
  $('#recent_volume_sparkline').sparkline(c_vol.reverse(), sparkline_option);

  document.getElementById('recent_active_farmers_card').innerHTML = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + c_active_farmers[0];
  $('#recent_active_farmers_sparkline').sparkline(c_active_farmers.reverse(), sparkline_option);

  document.getElementById('recent_revenue_card').innerHTML = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + CURRENCY.concat(c_amt[0].toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","));
  $('#recent_revenue_sparkline').sparkline(c_amt.reverse(), sparkline_option);

  document.getElementById('cpk_card').innerHTML = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + CURRENCY.concat(parseFloat(c_cpk[0]).toFixed(2));
  $('#cpk_sparkline').sparkline(c_cpk.reverse(), sparkline_option);

  document.getElementById('recent_sustainability_card').innerHTML = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + parseFloat(c_sustainability[0]).toFixed(2) + "%";
  $('#recent_sustainability_sparkline').sparkline(c_sustainability.reverse(), sparkline_option);
}

//To show cummulative farmer and volume graph present on Home page
function cummulative_farmer_and_volume(cum_vol_farmer) {
  var all_dates = [];
  var vol_farmer_length = Object.keys(cum_vol_farmer).length;
  var first_date = new Date(cum_vol_farmer[0]['date']);
  var last_date = new Date(cum_vol_farmer[vol_farmer_length - 1]['date']);
  while (first_date <= last_date) {
    all_dates.push(first_date.getTime());
    first_date.setDate(first_date.getDate() + 1);
  }

  var total_days = all_dates.length;

  var cumm_volume = new Array(total_days).fill(0.0);
  var cumm_farmers = new Array(total_days).fill(0.0);
  var temp_volume = {};
  temp_volume['name'] = "Volume";
  temp_volume['data'] = [];
  temp_volume['type'] = 'spline';
  temp_volume['pointInterval'] = 24 * 3600 * 1000;
  temp_volume['pointStart'] = all_dates[total_days - 1]; // Pointing to the starting date
  temp_volume['showInLegend'] = true;
  var temp_farmers = {};
  temp_farmers['name'] = "Farmers";
  temp_farmers['data'] = [];
  temp_farmers['type'] = 'spline';
  temp_farmers['pointInterval'] = 24 * 3600 * 1000;
  temp_farmers['pointStart'] = all_dates[total_days - 1]; // Pointing to the starting date
  temp_farmers['showInLegend'] = true;

  for (var i = 0; i < vol_farmer_length; i++) {
    var index = all_dates.indexOf(new Date(cum_vol_farmer[i]['date']).getTime());
    cumm_farmers[index] = cum_vol_farmer[i]['cum_distinct_farmer'];
    cumm_volume[index] = cum_vol_farmer[i]['cum_vol'];
  }

  for (var i = 0; i < total_days; i++) {
    if (cumm_farmers[i] == 0) {
      cumm_farmers[i] = cumm_farmers[i - 1];
      cumm_volume[i] = cumm_volume[i - 1];
    }
    temp_volume['data'].push([all_dates[i], cumm_volume[i]]);
    temp_farmers['data'].push([all_dates[i], cumm_farmers[i]]);
  }

  var series = [];
  series.push(temp_volume);
  series.push(temp_farmers);

  createMasterForTimeSeries($('#detail_container'), $('#master_container'), series, MASTER_HOME);
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


function change_payment(parameter) {
  if (parameter == 'summary_payments') {
    if (superEditMode == 1) {
      //            $("#gaddidar_payments").parent().addClass('disabled');
      //            $("#transportation_payments").parent().addClass('disabled');
      window.alert("Please submit currently edited table first");
    } else {
      $('#table2_wrapper').parent().removeAttr('style');
      $('#table3_wrapper').parent().css('display', 'none');
      $('#table4_wrapper').parent().css('display', 'none');
    }
  } else if (parameter == 'gaddidar_payments') {
    if (superEditMode == 1) {
      //            $("#summary_payments").parent().addClass('disabled');
      //            $("#transportation_payments").parent().addClass('disabled');
      window.alert("Please submit currently edited table first");
    } else {
      $('#table2_wrapper').parent().css('display', 'none');
      $('#table3_wrapper').parent().removeAttr('style');
      $('#table4_wrapper').parent().css('display', 'none');
    }
  } else if (parameter == 'transportation_payments') {
    if (superEditMode == 1) {
      //            $("#summary_payments").parent().addClass('disabled');
      //            $("#transportation_payments").parent().addClass('disabled');
      window.alert("Please submit currently edited table first");
    } else {
      $('#table2_wrapper').parent().css('display', 'none');
      $('#table3_wrapper').parent().css('display', 'none');
      $('#table4_wrapper').parent().removeAttr('style');
    }
  } else {
    if (superEditMode == 1) {
      //            $("#gaddidar_payments").parent().addClass('disabled');
      //            $("#summary_payments").parent().addClass('disabled');
      window.alert("Please submit currently edited table first");
    } else {
      $('#table2_wrapper').parent().css('display', 'none');
      $('#table3_wrapper').parent().css('display', 'none');
      $('#table4_wrapper').parent().removeAttr('style');
    }
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
    get_data("", country_id);
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
    if (superEditMode == 1) {
      window.alert('Please finish editing first');
    } else {

      if ($('#aggregator_payments :selected').val() == '') {
        alert("Please select an aggregator to download the payment sheet");
      } else {
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

        aggregator_data_set_copy = aggregator_data_set.slice();
        gaddidar_data_set_copy = gaddidar_data_set.slice();
        for (var i = 0; i < aggregator_data_set_copy.length; i++) {
          aggregator_data_set_copy[i] = aggregator_data_set_copy[i].slice(0, 9);
          aggregator_data_set_copy[i].push(aggregator_data_set[i][11])
          aggregator_data_set_copy[i].push(aggregator_data_set[i][12])
        }

        for (var i = 0; i < gaddidar_data_set_copy.length; i++) {
          gaddidar_data_set_copy[i] = gaddidar_data_set_copy[i].slice(0, 6);
          gaddidar_data_set_copy[i].push(gaddidar_data_set[i][9]);
        }

        var data_json = {
          aggregator_data: {
            sheet_heading: aggregator_sheet_name,
            sheet_name: 'Aggregator',
            data: aggregator_data_set_copy
          },

          gaddidar_data: {
            sheet_heading: gaddidar_sheet_name,
            sheet_name: 'Commission Agent',
            data: gaddidar_data_set_copy
          },

          transporter_data: {
            sheet_heading: transporter_sheet_name,
            sheet_name: 'Transporter',
            data: transporter_data_set
          }
        };

        var header_json = header_dict;

        var cell_format = {
          bold: 0,
          font_size: 10,
          num_format: '#,##0.00',
          text_wrap: true
        }

        var json_to_send = {
          header: header_json,
          data: data_json,
          cell_format: cell_format,
          sheet_header: 'Loop India Bihar',
          sheet_footer: 'This is an automated generated sheet'

        }

        xhttp.send(JSON.stringify(json_to_send));
      }
    }
  });

  $("#aggregator_payments").change(function() {
    var aggregator_id = $('#aggregator_payments :selected').val();
    var agg_id = $(this).children(":selected").attr("id");
    $("select").material_select();
    var aggregator_name_input = $(this).children(":selected")[0].innerHTML;

    if (table_created) {
      $('#outliers_data').html("");
    }
    aggregator_payment_sheet(payments_data.aggregator_data, aggregator_id, agg_id, aggregator_name_input);
    //      console.log(payments_data.aggregator_data);
    $("#download_payment_sheets").show();
    $('#aggregator_payment_details').show();
    outliers_summary(aggregator_id);
  });

  $("#time_series_frequency").change(function() {
    time_series_frequency = $('#time_series_frequency :selected').val();
    if (time_series_frequency == 1) {
      createMasterForTimeSeries($('#detail_container_time_series'), $('#master_container_time_series'), time_series_volume_amount_farmers, MASTER_TIME_SERIES_VOL_AMT);
      createMasterForTimeSeries($('#detail_container_cpk'), $('#master_container_cpk'), time_series_cpk_spk, MASTER_TIME_SERIES_CPK_SPK);
    } else {
      createMasterForTimeSeries($('#detail_container_time_series'), $('#master_container_time_series'), get_frequency_data(start_date, end_date, time_series_volume_amount_farmers, time_series_frequency, false), MASTER_TIME_SERIES_VOL_AMT);
      createMasterForTimeSeries($('#detail_container_cpk'), $('#master_container_cpk'), get_frequency_cpk(start_date, end_date, time_series_cpk_spk, time_series_frequency, false), MASTER_TIME_SERIES_CPK_SPK);
    }
  });

  $('#payments_from_date').change(function() {
    var start_date = $('#payments_from_date').val();
    if (start_date != '') {
      hidePaymentDetails();
      $('#payments_to_date').prop('disabled', false);
      var from_date = new Date(new Date(start_date));
      var daysInMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
      if (from_date.getDate() >= 16) {
        if (from_date.getFullYear() % 4 == 0 && from_date.getMonth() == 1) {
          $('#payments_to_date').val(from_date.getFullYear() + "-" + (from_date.getMonth() + 1) + "-" + "29");
        } else {
          $('#payments_to_date').val(from_date.getFullYear() + "-" + (from_date.getMonth() + 1) + "-" + daysInMonth[from_date.getMonth()]);
        }
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
      hidePaymentDetails();
    } else {
      $('#payments_to_date').val('');
    }
  });

  $('#get_filter_data_button').click(function() {
    gaddidar = true;
    get_data("", country_id);
  });
}

function hidePaymentDetails() {
  $("#aggregator_payment_tab").hide();
  $("#download_payment_sheets").hide();
  $('#aggregator_payment_details').hide();
}

//To make a call when filters are changed
function get_filter_data(language, country_id) {
  $.get("/loop/filter_data/", {
      language: language,
      'country_id': country_id
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
        fill_crop_filter(crops_for_filter);
      else
      {
        // If country is India, then Regional Language is Hindi
        if (country_id == 1)
          fill_crop_filter(croplanguage_for_filter[HINDI_ID]);
        // If country is Bangladesh, then Regional Language is Bangla
        else if (country_id == 2)
          fill_crop_filter(croplanguage_for_filter[BANGLA_ID]);
      }
      get_data("", country_id);
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
function get_data(location, country_id) {
  if (location == 'drawer') {
    start_date = $('#from_date_drawer').val();
    end_date = $('#to_date_drawer').val();
  } else {
    start_date = $('#from_date').val();
    end_date = $('#to_date').val();
  }
  // Get rest of the filters
  if (Date.parse(start_date) > Date.parse(end_date)) {
    $('#modal1').openModal();
  } else {
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
    // $(".button-collapse1").sideNav('hide');
    get_data_for_bar_graphs(start_date, end_date, aggregator_ids, crop_ids, mandi_ids, gaddidar_ids, country_id);
    get_data_for_line_graphs(start_date, end_date, aggregator_ids, crop_ids, mandi_ids, gaddidar_ids, country_id);
  }
}

function get_data_for_bar_graphs(start_date, end_date, aggregator_ids, crop_ids, mandi_ids, gaddidar_ids, country_id) {
  $.get("/loop/data_for_drilldown_graphs/", {
      'start_date': start_date,
      'end_date': end_date,
      'country_id': country_id,
      'a_id[]': aggregator_ids,
      'c_id[]': crop_ids,
      'm_id[]': mandi_ids,
      'g_id[]': gaddidar_ids,
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
  var aggregator_cost = 0;
  var volume_amount_visits_data = bar_graphs_json_data.aggregator_mandi;
  var transport_data = bar_graphs_json_data.transportation_cost_mandi;
  var gaddidar_contribution = bar_graphs_json_data.gaddidar_contribution;
  var aggregator_incentive = bar_graphs_json_data.aggregator_incentive_cost;

  for (var i = 0; i < volume_amount_visits_data.length; i++) {
    total_volume += volume_amount_visits_data[i][QUANTITY__SUM];
    total_amount += volume_amount_visits_data[i][AMOUNT__SUM];
    total_visits += volume_amount_visits_data[i]["mandi__id__count"];
  }

  for (var i = 0; i < transport_data.length; i++) {
    total_cost += parseFloat(transport_data[i]['transportation_cost__sum']);
    total_recovered += parseFloat(transport_data[i]['farmer_share__sum']);
  }

  var gaddidar_contribution_length = gaddidar_contribution.length;
  for (var i = 0; i < gaddidar_contribution_length; i++) {
    gaddidar_share += parseFloat(gaddidar_contribution[i]['amount']);
    volume_without_crop_gaddidar_filter += parseFloat(gaddidar_contribution[i][QUANTITY__SUM]);
  }

  for (var i = 0; i < aggregator_incentive.length; i++) {
    aggregator_cost += parseFloat(aggregator_incentive[i]['amount']);
  }

  //TODO - DONE : use AI from json data
  var cpk = ((total_cost + aggregator_cost) / volume_without_crop_gaddidar_filter).toFixed(2);
  var spk = ((total_recovered + gaddidar_share) / volume_without_crop_gaddidar_filter).toFixed(2);

  total_recovered += gaddidar_share;
  //TODO - DONE : use AI from json data
  // total_cost += volume_without_crop_gaddidar_filter * AGGREGATOR_INCENTIVE_PERCENTAGE;
  total_cost += aggregator_cost;

  $("#aggregator_volume").text("Volume: " + parseFloat(total_volume).toFixed(0) + " " + KG);
  $("#aggregator_amount").text("amount: " + CURRENCY + parseFloat(total_amount).toFixed(0));
  $("#aggregator_visits").text("visits: " + total_visits);
  $("#aggregator_cpk").text("SPK/CPK : " + spk + "/" + cpk);
  $("#aggregator_cost").text("Recovered/Total : " + CURRENCY + total_recovered.toFixed(2) + "/ " + CURRENCY + total_cost.toFixed(2));

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
  var max_scale = series[0]['data'][0]['y'];
  plot_drilldown(container, series, drilldown, false, max_scale, 'bar');
}

//Recovered total graph on analytics page is being plotted from this
function transport_cost_graph(container, axis, axis_names, axis_parameter, values, values_names, values_parameter, json_data) {

  var transportation_cost_mandi = json_data.transportation_cost_mandi;
  var gaddidar_contribution = json_data.gaddidar_contribution;
  var aggregator_incentive_cost = json_data.aggregator_incentive_cost;

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
    //TODO : DONE another for loop would be required to add AI
    // values_cost[index] += (gaddidar_contribution[i][QUANTITY__SUM] * AGGREGATOR_INCENTIVE_PERCENTAGE);
    values_cost_recovered[index] += gaddidar_contribution[i][AMOUNT];
    // values_cost_drilldown[index][drilldown_index] += (gaddidar_contribution[i][QUANTITY__SUM] * AGGREGATOR_INCENTIVE_PERCENTAGE);
    values_cost_recovered_drilldown[index][drilldown_index] += gaddidar_contribution[i][AMOUNT];
  }

  var aggregator_incentive_cost_length = aggregator_incentive_cost.length;
  for (var i = 0; i < aggregator_incentive_cost_length; i++) {
    var index = axis.indexOf(aggregator_incentive_cost[i][axis_parameter].toString());
    var drilldown_index = values.indexOf(aggregator_incentive_cost[i][values_parameter].toString());
    values_cost[index] += aggregator_incentive_cost[i][AMOUNT];
    values_cost_drilldown[index][drilldown_index] += aggregator_incentive_cost[i][AMOUNT];
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

  //Error in sorting as the array contains 2 types of data points and sorting can be done one 1 only
  // for (var i = 0; i < drilldown['series'].length; i+=2) {
  //     drilldown['series'][i]['data'].sort(function(a, b) {
  //         return b[1] - a[1];
  //     });
  // }
  var max_scale = series[0]['data'][0]['y'];
  plot_drilldown(container, series, drilldown, false, max_scale, 'bar');
}

//Cpk and Spk on analytics page is being plotted from this
function cpk_spk_graph(container, axis, axis_names, axis_parameter, values, values_names, values_parameter, json_data) {
  //Not considering crops filter while calculating cpk and spk
  // var vol_stats = json_data.transactions_details_without_crops;
  //TODO: can merge vol_stats and gaddidar_shre_stats as the data is without applying crop filters
  var vol_stats = json_data.gaddidar_contribution;
  var cost_stats = json_data.transportation_cost_mandi;
  var gaddidar_share_stats = json_data.gaddidar_contribution;
  var aggregator_incentive_cost = json_data.aggregator_incentive_cost;

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

  var aggregator_incentive_cost_length = aggregator_incentive_cost.length;
  for (var i = 0; i < aggregator_incentive_cost_length; i++) {
    var index = axis.indexOf(aggregator_incentive_cost[i][axis_parameter].toString());
    var drilldown_index = values.indexOf(aggregator_incentive_cost[i][values_parameter].toString());
    values_cost_cpk[index] += aggregator_incentive_cost[i][AMOUNT];
    values_cost_cpk_drilldown[index][drilldown_index] += aggregator_incentive_cost[i][AMOUNT];
  }

  var data_for_sorting = [];
  for (var i = 0; i < axis.length; i++) {
    data_for_sorting.push({
      'name': axis_names[i],
      //TODO : DONE another for loop would be required to add AI values in values_cost_cpk
      'cpk': values_vol[i] > 0 ? (values_cost_cpk[i] / values_vol[i]) : 0.0,
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
        //TODO : DONE another for loop would be required to add AI values in values_cost_cpk
        drilldown['series'][i * 2]['data'].push([values_names[j], values_cost_cpk_drilldown[i][j] / values_vol_drilldown[i][j]]);
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
  //Error in sorting as the array contains 2 types of data points and sorting can be done one 1 only
  // for (var i = 0; i < drilldown['series'].length; i+=2) {
  //     drilldown['series'][i]['data'].sort(function(a, b) {
  //         return b[1] - a[1];
  //     });
  // }
  var max_scale = series[0]['data'][0]['y'];
  plot_drilldown(container, series, drilldown, true, max_scale, 'bar');
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
  var max_scale = series[0]['data'][0]['y'];
  plot_drilldown(container, series, drilldown, false, max_scale, 'bar');
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
  plot_drilldown(container, series, drilldown, false, max_crop_price, 'columnrange');
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
      series[0]['data'].push([json_data[i]['crop__crop_name'], json_data[i]['farmer__count']]);
    } 
    else {
      if (country_id == 1)
        series[0]['data'].push([json_data[i]['crop__crop_name_hi'], json_data[i]['farmer__count']]);
      else if (country_id == 2)
        series[0]['data'].push([json_data[i]['crop__crop_name_bn'], json_data[i]['farmer__count']]);
    }
  }

  // plot_stacked_chart(container, series);
  plot_drilldown(container, series, {}, false, json_data[0]['farmer__count'], 'bar');
}

//Data for Time series grpahs request is being made here
function get_data_for_line_graphs(start_date, end_date, aggregator_ids, crop_ids, mandi_ids, gaddidar_ids, country_id) {
  $.get("/loop/data_for_line_graph/", {
      'start_date': start_date,
      'end_date': end_date,
      'country_id': country_id,
      'a_id[]': aggregator_ids,
      'c_id[]': crop_ids,
      'm_id[]': mandi_ids,
      'g_id[]': gaddidar_ids
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
    crops_names_time_series = crops_for_filter;
  else
  {
    // If country is India, then Regional Language is Hindi
    if (country_id == 1)
      crops_names_time_series = croplanguage_for_filter[HINDI_ID];
    // If country is Bangladesh, then Regional Language is Bangla
    else if (country_id == 2)
      crops_names_time_series = croplanguage_for_filter[BANGLA_ID];
  }
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
  var aggregator_incentive_cost = bar_graphs_json_data.aggregator_incentive_cost;
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

    aggregator_incentive_amount = new Array(all_dates.length).fill(0.0);
    var aggregator_incentive_cost_length = aggregator_incentive_cost.length;
    for (var i = 0; i < aggregator_incentive_cost_length; i++) {
      var date_index = all_dates.indexOf(new Date(aggregator_incentive_cost[i]['date']).getTime());
      aggregator_incentive_amount[date_index] += aggregator_incentive_cost[i][AMOUNT];
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
      //TODO : DONE - another for loop would be required to add AI values in amount
      time_series_cpk_spk[0]['data'].push([all_dates[i], time_series_volume_amount_farmers[0]['data'][i][1] > 0 ? ((transport_cost[i] + aggregator_incentive_amount[i]) / time_series_volume_amount_farmers[0]['data'][i][1]) : null]);

      time_series_cpk_spk[1]['data'].push([all_dates[i], time_series_volume_amount_farmers[0]['data'][i][1] > 0 ? (farmer_share[i] / time_series_volume_amount_farmers[0]['data'][i][1]) : null]);
    }

    for (var i = 0; i < dates_and_farmer_count.length; i++) {
      var index = all_dates.indexOf(new Date(dates_and_farmer_count[i]['date']).getTime());
      time_series_volume_amount_farmers[2]['data'][index][1] += dates_and_farmer_count[i]['farmer__count'];
    }
    createMasterForTimeSeries($('#detail_container_time_series'), $('#master_container_time_series'), time_series_volume_amount_farmers, MASTER_TIME_SERIES_VOL_AMT);
    createMasterForTimeSeries($('#detail_container_cpk'), $('#master_container_cpk'), time_series_cpk_spk, MASTER_TIME_SERIES_CPK_SPK);
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
  var first_date = new Date(start_date).getTime();
  var final_date = new Date(end_date).getTime();
  var new_series = [];
  var new_x_axis = [];

  while (first_date <= final_date) {
    new_x_axis.push(first_date);
    first_date += frequency * 86400 * 1000;
  }

  for (var i = 0; i < series.length; i++) {
    var temp_series = {};
    temp_series['name'] = series[i]['name'];
    temp_series['data'] = new Array(new_x_axis.length);
    temp_series['color'] = series[i]['color'];
    temp_series['type'] = series[i]['type'];
    for (var j = 0; j < new_x_axis.length; j++) {
      temp_series['data'][j] = [new_x_axis[j], 0];
    }
    temp_series['pointStart'] = new_x_axis[0];
    temp_series['pointInterval'] = time_series_frequency * 24 * 3600 * 1000;
    var count = 0;
    var index = 0;
    var temp = index;
    for (k = 0; k < series[i]['data'].length; k++) {

      // var temp_date = new Date(series[i]['data'][k][0]);
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
      temp = index;
    }
    if (averaged) {
      temp_series['data'][temp][1] /= count;
    }
    new_series.push(temp_series);
  }
  return new_series;
}


function get_frequency_cpk(start_date, end_date, series, frequency, averaged) {
  var first_date = new Date(start_date).getTime();
  var final_date = new Date(end_date).getTime();
  var new_series = [];
  var new_x_axis = [];
  while (first_date <= final_date) {
    new_x_axis.push(first_date);
    first_date += frequency * 86400 * 1000;
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
  var index = 0;
  var new_transport_cost = new Array(new_x_axis.length).fill(0);
  var new_farmer_share = new Array(new_x_axis.length).fill(0);
  var new_volume = new Array(new_x_axis.length).fill(0);
  var new_aggregator_cost = new Array(new_x_axis.length).fill(0);
  for (var k = 0; k < series[0]['data'].length; k++) {
    if (new Date(new_x_axis[index + 1]) <= new Date(series[0]['data'][k][0])) {
      index += 1;
    }
    new_volume[index] += time_series_volume_amount_farmers[0]['data'][k][1];
    new_transport_cost[index] += transport_cost[k];
    new_farmer_share[index] += farmer_share[k];
    new_aggregator_cost[index] += aggregator_incentive_amount[k];
  }

  for (var i = 0; i < new_x_axis.length; i++) {
    temp_series_cpk['data'].push([new_x_axis[i], new_volume[i] > 0 ? (new_transport_cost[i] + new_aggregator_cost[i]) / new_volume[i] : null]);
    temp_series_spk['data'].push([new_x_axis[i], new_volume[i] > 0 ? new_farmer_share[i] / new_volume[i] : null]);
  }
  new_series.push(temp_series_cpk);
  new_series.push(temp_series_spk);

  return new_series;
}

function plot_drilldown(container_obj, dict, drilldown, floats, max_scale, chart_type) {
  var max, format;
  if (dict[0]['data'].length >= 6) {
    max = 5;
  } else {
    max = dict[0]['data'].length - 1;
  }

  if (floats) {
    format = '{point.y:.2f}';
  } else {
    format = '{point.y:.0f}';
  }

  var chart1 = container_obj.highcharts(Highcharts.merge(generalOptions, drilldownGraphOptions, {
    chart: {
      type: chart_type,
      inverted: true
    },
    xAxis: [{
      type: 'category',
      max: max,
    }, {
      type: 'category',
      max: null
    }],
    yAxis: {
      max: max_scale
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
      pointFormat: '<span>{point.name}</span>: <b>' + format + '</b> <br/>'
    },
    series: dict,
    drilldown: drilldown
  }));
}

function createDetailForCummulativeVolumeAndFarmer(detail_container, masterChart, dict) {
  // prepare the detail chart
  var myDict = [];
  var detailData = [],
    detailStart = dict[0]['data'][0][0];
  var axis;

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
    temp['pointInterval'] = 24 * 3600 * 1000;
    temp['showInLegend'] = true;
    $.each(this.data, function() {
      if (this.x >= detailStart) {
        temp['data'].push(this.y);
      }
    });
    myDict.push(temp);
  });

  // create a detail chart referenced by a global variable
  var width = detail_container.width();
  detailChartHome = detail_container.highcharts(Highcharts.merge(generalOptions, timeSeriesDetailOptions, {
    chart: {
      width: width
    },
    title: {
      text: "Volume and Farmers Cummulative Count"
    },
    xAxis: {
      type: 'datetime'
    },
    yAxis: [{
      title: {
        text: "Volume"
      }
    }, {
      title: {
        text: "Farmers"
      },
      opposite: true
    }],
    legend: {
      align: 'right',
      backgroundColor: (Highcharts.theme && Highcharts.theme.background2) || 'white',
    },
    series: myDict,
  })).highcharts(); // return chart
}

function createDetailForVolAmtTimeSeries(detail_container, masterChart, dict) {
  // prepare the detail chart
  var myDict = [];
  var detailData = [],
    detailStart = dict[0]['data'][0][0];
  var axis;

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
  var width = detail_container.width();
  detailChartTimeSeriesVol = detail_container.highcharts(Highcharts.merge(generalOptions, timeSeriesDetailOptions, {
    chart: {
      width: width
    },
    series: myDict,
    legend: {
      backgroundColor: (Highcharts.theme && Highcharts.theme.background2) || 'white'
    },
    yAxis: [{
      title: {
        text: 'Volume'
      }
    }, {
      title: {
        text: null
      },
      opposite: true
    }]
  })).highcharts(); // return chart
}

// create the master chart
function createMasterForTimeSeries(detail_container, master_container, dict, chart) {
  master_container.highcharts(Highcharts.merge(generalOptions, timeSeriesMasterOptions, {
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
            if (chart == MASTER_TIME_SERIES_VOL_AMT) {
              detailChartTimeSeriesVol.series[pos].setData(myDict[pos].data);
            } else if (chart == MASTER_TIME_SERIES_CPK_SPK) {
              detailChartTimeSeriesCPK.series[pos].setData(myDict[pos].data);
            } else if (chart == MASTER_HOME) {
              detailChartHome.series[pos].setData(myDict[pos].data);
            }
            pos++;
          });
          return false;
        }
      }
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
    series: dict,
    plotOptions: {
      series: {
        fillColor: {
          stops: [
            [0, Highcharts.getOptions().colors[0]],
            [1, 'rgba(255,255,255,0)']
          ]
        }
      }
    }
  }), function(masterChart) {
    if (chart == MASTER_TIME_SERIES_VOL_AMT) {
      createDetailForVolAmtTimeSeries(detail_container, masterChart, dict);
    } else if (chart == MASTER_TIME_SERIES_CPK_SPK) {
      createDetailForCpkSpkTimeSeries(detail_container, masterChart, dict);
    } else if (chart == MASTER_HOME) {
      createDetailForCummulativeVolumeAndFarmer(detail_container, masterChart, dict);
    }
  }); // return chart instance
}

function createDetailForCpkSpkTimeSeries(detail_container, masterChart, dict) {
  // prepare the detail chart
  var myDict = [];
  var detailData = [],
    detailStart = dict[0]['data'][0][0];

  $.each(masterChart.series, function() {
    if (this.name == "cpk") {
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
    myDict.push(temp);
  });

  // create a detail chart referenced by a global variable
  var width = detail_container.width();
  detailChartTimeSeriesCPK = detail_container.highcharts(Highcharts.merge(generalOptions, timeSeriesDetailOptions, {
    chart: {
      width: width
    },
    legend: {
      backgroundColor: (Highcharts.theme && Highcharts.theme.background2) || 'white'
    },
    series: myDict,
    yAxis: [{
      title: {
        text: null
      }
    }, {
      title: {
        text: null
      },
      opposite: true
    }]
  })).highcharts(); // return chart
}

function plot_area_range_graph(container, dict) {
  var container_width = $("#container3").width();
  container.highcharts(Highcharts.merge(generalOptions, {
    chart: {
      zoomType: 'x',
      width: container_width
    },
    xAxis: {
      type: 'datetime'
    },
    yAxis: {
      title: {
        text: 'Price'
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
    series: dict
  }));
}


// To fill aggregator drop down on Payment page
function fill_drop_down(container, data_json, id_parameter, name_parameter, caption, id) {
  var tbody_obj = container;
  tbody_obj.html("");
  tbody_obj.append('<option value="" disabled selected> Choose ' + caption + ' </option>');
  $.each(data_json, function(index, data) {
    var li_item = '<option value = ' + data[id_parameter] + ' id = ' + data[id] + '>' + data[name_parameter] + '</option>';
    tbody_obj.append(li_item);
  });
  $('select').material_select();
}
//To compute aggregator, transporter, gaddidar payments table
function aggregator_payment_sheet(data_json, aggregator, agg_id, aggregator_name_input) {
  var aggregator_payment = payments_data.aggregator_data;
  var transport_payment = payments_data.transportation_data;
  var gaddidar_contribution_data = payments_data.gaddidar_data;
  var aggregator_incentive = payments_data.aggregator_incentive;

  var sno = 1;
  aggregator_data_set = [];
  gaddidar_data_set = [];
  transporter_data_set = [];
  var dates = [];
  var mandis = [];
  var quantites = [];
  var gaddidar_amount = [];
  // var farmers = [];
  var transport_cost = [];
  var farmer_share = [];
  var aggregator_payment_length = aggregator_payment.length;
  for (var i = 0; i < aggregator_payment_length; i++) {
    if (aggregator == aggregator_payment[i][USER_CREATED__ID].toString()) {
      var date_index = dates.indexOf(aggregator_payment[i]['date']);
      if (date_index == -1) {
        dates.push(aggregator_payment[i]['date']);
        mandis.push([]);
        quantites.push([]);
        gaddidar_amount.push([]);
        // farmers.push([]);
        transport_cost.push([]);
        farmer_share.push([]);
        date_index = dates.indexOf(aggregator_payment[i]['date']);
      }
      var mandi_index = mandis[date_index].map(function(e) {
        return e.mandi_name;
      }).indexOf(aggregator_payment[i]['mandi__mandi_name']);
      if (mandi_index == -1) {
        mandis[date_index].push({
          mandi_name: aggregator_payment[i]['mandi__mandi_name'],
          mandi_id: aggregator_payment[i][MANDI__ID]
        });
        quantites[date_index].push(0);
        gaddidar_amount[date_index].push(0);
        // farmers[date_index].push(0);
        transport_cost[date_index].push(0);
        farmer_share[date_index].push({
          farmer_share_amount: 0,
          farmer_share_comment: null
        });
        mandi_index = mandis[date_index].map(function(e) {
          return e.mandi_name;
        }).indexOf(aggregator_payment[i]['mandi__mandi_name']);
      }
      quantites[date_index][mandi_index] += aggregator_payment[i][QUANTITY__SUM];
      gaddidar_amount[date_index][mandi_index] += aggregator_payment[i][QUANTITY__SUM] * aggregator_payment[i]['gaddidar__commission'];
      // farmers[date_index][mandi_index] += aggregator_payment[i]['farmer__count'];
      gaddidar_data_set.push([aggregator_payment[i]['date'], aggregator_payment[i]['gaddidar__gaddidar_name'], aggregator_payment[i]['mandi__mandi_name'], parseFloat(aggregator_payment[i][QUANTITY__SUM].toFixed(2)), 0, 0, aggregator_payment[i][MANDI__ID], aggregator_payment[i][GADDIDAR__ID], agg_id, "", parseFloat(aggregator_payment[i][AMOUNT__SUM].toFixed(2)), aggregator_payment[i]['gaddidar__discount_criteria']]);

    }
  }

  var gaddidar_contribution_data_length = gaddidar_contribution_data.length;
  for (var i = 0; i < gaddidar_contribution_data_length; i++) {
    if (aggregator == payments_gaddidar_contribution[i][USER_CREATED__ID].toString()) {
      for (var j = 0; j < gaddidar_data_set.length; j++) {
        if (gaddidar_data_set[j].indexOf(payments_gaddidar_contribution[i]['date']) != -1 &&
          gaddidar_data_set[j].indexOf(payments_gaddidar_contribution[i]['gaddidar__name']) != -1) {
          gaddidar_data_set[j][4] = parseFloat(payments_gaddidar_contribution[i]['gaddidar_discount']);
          gaddidar_data_set[j][5] = parseFloat(payments_gaddidar_contribution[i]['amount']);
          gaddidar_data_set[j][9] = payments_gaddidar_contribution[i]['comment'];
        }
      }
    }
  }

  var transport_payment_length = transport_payment.length;
  for (var i = 0; i < transport_payment_length; i++) {
    if (aggregator == transport_payment[i][USER_CREATED__ID].toString()) {
      date_index = dates.indexOf(transport_payment[i]['date']);
      mandi_index = mandis[date_index].map(function(e) {
        return e.mandi_name;
      }).indexOf(transport_payment[i]['mandi__mandi_name']);
      transport_cost[date_index][mandi_index] += transport_payment[i]['transportation_cost__sum'];
      farmer_share[date_index][mandi_index].farmer_share_amount = transport_payment[i]['farmer_share'];
      farmer_share[date_index][mandi_index].farmer_share_comment = transport_payment[i]['farmer_share_comment'];

      transporter_data_set.push([transport_payment[i]['date'], transport_payment[i]['mandi__mandi_name'], transport_payment[i]['transportation_vehicle__transporter__transporter_name'],
        transport_payment[i]['transportation_vehicle__transporter__transporter_phone'], transport_payment[i]['transportation_vehicle__vehicle__vehicle_name'], transport_payment[i]['transportation_vehicle__vehicle_number'], parseFloat(transport_payment[i]['transportation_cost__sum'].toFixed(2)), transport_payment[i]['transportation_cost_comment'], transport_payment[i]['mandi__id'], transport_payment[i]['transportation_vehicle__id'], transport_payment[i]['timestamp'], i
      ]);
    }
  }
  var total_volume = 0;
  var total_payment = 0;
  for (var i = 0; i < dates.length; i++) {
    for (var j = 0; j < mandis[i].length; j++) {
      //TODO : DONE to be moved to below for loop where we are adding aggregator_outlier
      var net_payment = transport_cost[i][j] - farmer_share[i][j].farmer_share_amount;

      aggregator_data_set.push([sno.toString(), dates[i], mandis[i][j].mandi_name, parseFloat(quantites[i][j].toFixed(2)), 0, transport_cost[i][j], farmer_share[i][j].farmer_share_amount, 0, parseFloat(net_payment.toFixed(2)), agg_id, mandis[i][j].mandi_id, "", farmer_share[i][j].farmer_share_comment]);

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

  var aggregator_incentive_length = aggregator_incentive.length;
  for (var i = 0; i < aggregator_incentive_length; i++) {
    if (aggregator == aggregator_incentive[i][USER_CREATED__ID].toString()) {
      for (var j = 0; j < aggregator_data_set.length; j++) {
        if (aggregator_data_set[j].indexOf(aggregator_incentive[i]['date']) != -1 && aggregator_data_set[j].indexOf(aggregator_incentive[i]['mandi__name']) != -1) {
          aggregator_data_set[j][4] = parseFloat(aggregator_incentive[i]['amount']);
          aggregator_data_set[j][8] = (parseFloat(aggregator_data_set[j][8]) + parseFloat(aggregator_data_set[j][4])).toFixed(2);
          aggregator_data_set[j][11] = aggregator_incentive[i]['comment'];
          break;
        }
      }
    }
  }
  //TODO: to be removed. Added fot temporary purposes.
  var data_set_length = aggregator_data_set.length;
  aggregator_data_set.push([sno.toString(), "", "Mobile Recharge ", "", 150, "", "", "", 150, "", "", "", ""]);

  var gaddidar_data_set_clone = [];
  for (var i = 0; i < gaddidar_data_set.length; i++) {
    gaddidar_data_set_clone.push(gaddidar_data_set[i].slice());
    if (gaddidar_data_set[i][11] == 1)
      gaddidar_data_set_clone[i][4] = parseFloat(gaddidar_data_set_clone[i][4]) * 100 + '%';
  }
  $(window).on('beforeunload', function() {
    if (!$('#ToolTables_table2_1').hasClass('disable-button') || !$('#ToolTables_table3_1').hasClass('disable-button'))
      return "You have Unsaved Changes";
  });

  var $this;
  var flag_edit_Table2 = false;
  var rows_table2 = {};
  var rows_table2_farmer = {};
  var editedAggregator = 0;
  var editedFarmer = 0;

  function initializeAggregatorModal() {
    $('#aggregator_date_row').val($this.parent()[0].childNodes[1].innerHTML);
    $('#aggregator_mandi_row').val($this.parent()[0].childNodes[2].innerHTML);
    $('#aggregator_volume_row').val($this.parent()[0].childNodes[3].innerHTML);
    $('#aggregator_commission_row').val(parseFloat($this.parent()[0].childNodes[4].innerHTML / ($this.parent()[0].childNodes[3].innerHTML)).toFixed(2));
    $('#aggregator_share_row').val(parseFloat($this.parent()[0].childNodes[4].innerHTML).toFixed(2));
    $('#aggregator_comment_row').val($this.parent()[0].childNodes[9].innerHTML);
    $('#aggregator_error_div').hide();
  }

  function initializeFarmerModal() {
    $('#farmer_date_row').val($this.parent()[0].childNodes[1].innerHTML);
    $('#farmer_mandi_row').val($this.parent()[0].childNodes[2].innerHTML);
    $('#farmer_volume_row').val($this.parent()[0].childNodes[3].innerHTML);
    $('#farmer_transport_cost_row').val($this.parent()[0].childNodes[5].innerHTML);
    $('#farmer_gaddidar_commission_row_farmer').val($this.parent()[0].childNodes[7].innerHTML);
    $('#farmer_commission_row').val(parseFloat($this.parent()[0].childNodes[6].innerHTML / ($this.parent()[0].childNodes[3].innerHTML)).toFixed(2));
    $('#farmer_share_row').val(parseFloat($this.parent()[0].childNodes[6].innerHTML).toFixed(2));
    $('#farmer_comment_row').val($this.parent()[0].childNodes[10].innerHTML);
    $('#farmer_error_div').hide();
  }

  function inputValidation(field) {
    return field.val().toString().match(/^[0-9]*[.]?[0-9]+$/);
  }

  function actionOnInvalidValidation(formfield, divfield, errorfield) {
    formfield.focus();
    divfield.show();
    errorfield[0].innerHTML = "* Value you have entered is invalid.";
  }
  var aggregatorResetClick = false;
  var farmerResetClick = false
  $('#table2').on('click', 'tbody td', function(e) {
    $this = $(this);
    //console.log(aggregator_data_set[$this.context.parentNode.rowIndex-1][$this.context.cellIndex]);
    if ($this.context.cellIndex === 4 && flag_edit_Table2 == true) {
      initializeAggregatorModal();
      $('#aggregator_modal').openModal();
      $('#aggregator_commission_row').focus();
    } else if ($this.context.cellIndex === 6 && flag_edit_Table2 == true) {
      initializeFarmerModal();
      $('#farmer_modal').openModal();
      $('#farmer_commission_row').focus();
    }

  });
  $('#aggregator_commission_row').on('change', function() {
    if (!inputValidation($('#aggregator_commission_row'))) {
      actionOnInvalidValidation($('#aggregator_commission_row'), $('#aggregator_error_div'), $('#aggregator_error_message'));
    } else {
      $('#aggregator_share_row').val(parseFloat(($this.parent()[0].childNodes[3].innerHTML) * $('#aggregator_commission_row').val()).toFixed(2));
      if ($('#aggregator_commission_row').val().trim() != '' && $('#aggregator_share_row').val().trim() != $this.parent()[0].childNodes[4].innerHTML)
        editedAggregator = 1;
    }
  });
  $('#aggregator_share_row').on('change', function() {
    if (!inputValidation($('#aggregator_share_row'))) {
      actionOnInvalidValidation($('#aggregator_share_row'), $('#aggregator_error_div'), $('#aggregator_error_message'))
    } else {
      $('#aggregator_commission_row').val(parseFloat($('#aggregator_share_row').val() / ($this.parent()[0].childNodes[3].innerHTML)).toFixed(2));
      if ($('#aggregator_share_row').val().trim() != '' && $('#aggregator_share_row').val().trim() != $this.parent()[0].childNodes[4].innerHTML)
        editedAggregator = 1;
    }
  });
  $('#aggregator_comment_row').on('change', function() {
    if ($('#aggregator_comment_row').val().trim() != '' && editedAggregator == 0)
      editedAggregator = 2;
  });
  $('#farmer_commission_row').on('change', function() {
    if (!inputValidation($('#farmer_commission_row'))) {
      actionOnInvalidValidation($('#farmer_commission_row'), $('#farmer_error_div'), $('#farmer_error_message'));
    } else {
      $('#farmer_share_row').val(parseFloat(($this.parent()[0].childNodes[3].innerHTML) * $('#farmer_commission_row').val()).toFixed(2));
      if ($('#farmer_commission_row').val().trim() != '' && $('#farmer_share_row').val().trim() != $this.parent()[0].childNodes[6].innerHTML)
        editedFarmer = 1;

    }
  });
  $('#farmer_share_row').on('change', function() {
    if (!inputValidation($('#farmer_share_row'))) {
      actionOnInvalidValidation($('#farmer_share_row'), $('#farmer_error_div'), $('#farmer_error_message'));
    } else {
      $('#farmer_commission_row').val(parseFloat($('#farmer_share_row').val() / ($this.parent()[0].childNodes[3].innerHTML)).toFixed(2));
      if ($('#farmer_share_row').val().trim() != '' && $('#farmer_share_row').val().trim() != $this.parent()[0].childNodes[6].innerHTML)
        editedFarmer = 1;
    }
  });
  $('#farmer_comment_row').on('change', function() {
    if ($('#farmer_comment_row').val().trim() != '' && editedFarmer == 0)
      editedFarmer = 2;
  });

  $('#aggregator_commission_row').keypress(function(event) {
    if (event.keyCode === 13) {
      $('#aggregator_comment_row').focus();
    }
  });
  $('#aggregator_share_row').keypress(function(event) {
    if (event.keyCode === 13) {
      $('#aggregator_comment_row').focus();
    }
  });
  $('#aggregator_comment_row').keypress(function(event) {
    if (event.keyCode === 13) {
      if (!inputValidation($('#aggregator_share_row'))) {
        actionOnInvalidValidation($('#aggregator_share_row'), $('#aggregator_error_div'), $('#aggregator_error_message'));
      } else if (!inputValidation($('#aggregator_commission_row'))) {
        actionOnInvalidValidation($('#aggregator_share_row'), $('#aggregator_error_div'), $('#aggregator_error_message'));
      } else {
        $('#aggregator_comment_row').trigger('change');
        $('#aggregator_submit_modal').trigger('click');
      }
    }
  });
  $('#farmer_commission_row').keypress(function(event) {
    if (event.keyCode === 13) {
      $('#farmer_comment_row').focus();
    }
  });
  $('#farmer_share_row').keypress(function(event) {
    if (event.keyCode === 13) {
      $('#farmer_comment_row').focus();
    }
  });
  $('#farmer_comment_row').keypress(function(event) {
    if (event.keyCode === 13) {
      if (!inputValidation($('#farmer_share_row'))) {
        actionOnInvalidValidation($('#farmer_share_row'), $('#farmer_error_div'), $('#farmer_error_message'));
      } else if (!inputValidation($('#farmer_commission_row'))) {
        actionOnInvalidValidation($('#farmer_commission_row'), $('#farmer_error_div'), $('#farmer_error_message'));
      } else {
        $('#farmer_comment_row').trigger('change');
        $('#farmer_submit_modal').trigger('click');
      }
    }
  });
  $('#farmer_close').on('click', function() {
    farmerResetClick = false;
    $('#farmer_modal').closeModal();
  });
  $('#farmer_reset_modal').on('click', function() {
    farmerResetClick = true;

    $('#farmer_share_row').val($('#table2').DataTable().cell($this.context.parentNode.rowIndex - 1, 6).data());
    $('#farmer_commission_row').val(parseFloat($('#table2').DataTable().cell($this.context.parentNode.rowIndex - 1, 6).data() / $this.parent()[0].childNodes[3].innerHTML).toFixed(2));
    $('#farmer_comment_row').val($('#table2').DataTable().cell($this.context.parentNode.rowIndex - 1, 12).data());

  });
  $('#farmer_submit_modal').on('click', function(ev) {
    if (!inputValidation($('#farmer_commission_row'))) {
      ev.preventDefault();
      $('#farmer_commission_row').val($this.parent()[0].childNodes[6].textContent / $this.parent()[0].childNodes[3].innerHTML);
      $('#farmer_share_row').val($this.parent()[0].childNodes[6].textContent);
      $('#farmer_commission_row').focus();
      return false;
    } else if (!inputValidation($('#farmer_share_row'))) {
      ev.preventDefault();
      $('#farmer_commission_row').val($this.parent()[0].childNodes[6].textContent / $this.parent()[0].childNodes[3].innerHTML);
      $('#farmer_share_row').val($this.parent()[0].childNodes[6].textContent);
      $('#farmer_share_row').focus();
      return false;
    } else if (farmerResetClick && editedFarmer == 0) {
      $this.parent()[0].childNodes[6].innerHTML = $('#table2').DataTable().cell($this.context.parentNode.rowIndex - 1, 6).data();
      $this.parent()[0].childNodes[10].innerHTML = $('#table2').DataTable().cell($this.context.parentNode.rowIndex - 1, 12).data();
      delete rows_table2_farmer[$this.context.parentNode.rowIndex];
      $this.removeAttr('class');
      $this.closest('tr').children('td:nth-child(11)')[0].className = '';
      $this.addClass('editcolumn');
      farmerResetClick = false;
    } else if (editedFarmer != 0) {

      $this.parent()[0].childNodes[6].innerHTML = $('#farmer_share_row').val();
      $this.parent()[0].childNodes[10].innerHTML = $('#farmer_comment_row').val() + ' - ' + window.localStorage.name;
      $this.parent()[0].childNodes[8].innerHTML = parseFloat(parseFloat($this.parent()[0].childNodes[5].innerHTML) + parseFloat($this.parent()[0].childNodes[4].innerHTML) - parseFloat($this.parent()[0].childNodes[7].innerHTML) - parseFloat($this.parent()[0].childNodes[6].innerHTML)).toFixed(2);
      if ((parseFloat($this.parent()[0].childNodes[4].innerHTML) + parseFloat($this.parent()[0].childNodes[5].innerHTML)) < parseFloat($this.parent()[0].childNodes[6].innerHTML)) {

        //  $this.parent().css('background-color', '#E5FEB5').css('font-weight', 'bold').css('color', '#009');
        $this.removeAttr('class');
        $this.addClass('editedcelledge');
        $this.closest('tr').children('td:nth-child(11)')[0].className = 'editedcelledge';

      } else {
        $this.removeAttr('class');
        $this.addClass('editedcell');
        $this.closest('tr').children('td:nth-child(11)')[0].className = 'editedcell';
        $this.closest('tr').children('td:nth-child(11)')[0].className = 'editedcell';
        // $this.parent().css('background-color', '#E5FEB5').css('font-weight', 'bold').css('color', '#009');
      }
      var row_id = $this.context.parentNode.rowIndex;
      rows_table2_farmer[row_id] = true;
      editedFarmer = 0;

      $('#farmer_error_div').hide();
    }
    $("#farmer_modal").closeModal();
  });
  $('#aggregator_close').on('click', function() {
    aggregatorResetClick = false;
    $('#aggregator_modal').closeModal();
  })
  $('#aggregator_reset_modal').on('click', function() {
    aggregatorResetClick = true;
    $('#aggregator_share_row').val($('#table2').DataTable().cell($this.context.parentNode.rowIndex - 1, 4).data());
    $('#aggregator_commission_row').val(parseFloat($('#table2').DataTable().cell($this.context.parentNode.rowIndex - 1, 4).data() / $this.parent()[0].childNodes[3].innerHTML).toFixed(2))
    $('#aggregator_comment_row').val($('#table2').DataTable().cell($this.context.parentNode.rowIndex - 1, 11).data());
  });
  $('#aggregator_submit_modal').on('click', function(ev) {
    if (!inputValidation($('#aggregator_commission_row'))) {
      ev.preventDefault();
      $('#aggregator_commission_row').val($this.parent()[0].childNodes[5].textContent / $this.parent()[0].childNodes[4].innerHTML);
      $('#aggregator_share_row').val($this.parent()[0].childNodes[5].textContent);
      $('#aggregator_commission_row').focus();
      return false;
    } else if (!inputValidation($('#aggregator_share_row'))) {
      ev.preventDefault();
      $('#aggregagtor_commission_row').val($this.parent()[0].childNodes[5].textContent / $this.parent()[0].childNodes[4].innerHTML);
      $('#aggregagtor_share_row').val($this.parent()[0].childNodes[5].textContent);
      $('#aggregator_commission_row').focus();
      return false;
    } else if (aggregatorResetClick && editedAggregator == 0) {
      $this.parent()[0].childNodes[4].innerHTML = $('#table2').DataTable().cell($this.context.parentNode.rowIndex - 1, 4).data();
      $this.parent()[0].childNodes[9].innerHTML = $('#table2').DataTable().cell($this.context.parentNode.rowIndex - 1, 11).data();
      delete rows_table2[$this.context.parentNode.rowIndex];
      $this.removeAttr('class');
      $this.closest('tr').children('td:nth-child(10)')[0].className = '';
      $this.addClass('editcolumn');
      aggregatorResetClick = false;
    } else if (editedAggregator != 0) {
      $('#aggregator_modal').closeModal();
      $this.parent()[0].childNodes[4].innerHTML = $('#aggregator_share_row').val();
      $this.parent()[0].childNodes[9].innerHTML = $('#aggregator_comment_row').val() + ' - ' + window.localStorage.name;
      $this.parent()[0].childNodes[8].innerHTML = parseFloat(parseFloat($this.parent()[0].childNodes[5].innerHTML) + parseFloat($this.parent()[0].childNodes[4].innerHTML) - parseFloat($this.parent()[0].childNodes[7].innerHTML) - parseFloat($this.parent()[0].childNodes[6].innerHTML)).toFixed(2)
      if (parseFloat($this.parent()[0].childNodes[4].innerHTML / $this.parent()[0].childNodes[3].innerHTML) > 0.5) {
        $this.removeAttr('class');
        $this.addClass('editedcelledge');
        $this.closest('tr').children('td:nth-child(10)')[0].className = 'editedcelledge';
      } else {
        $this.removeAttr('class');
        $this.addClass('editedcell');
        $this.closest('tr').children('td:nth-child(10)')[0].className = 'editedcell';
      }
      var row_id = $this.context.parentNode.rowIndex;
      rows_table2[row_id] = true;
      editedAggregator = 0;
      $('#aggregator_error_div').hide();
    }
    $('#aggregator_modal').closeModal();
  });

  var finalFormat = function(value) {
    if (value.indexOf('.') === -1)
      return parseFloat(value).toLocaleString() + '.00';
    else
      return parseFloat(parseFloat(value).toFixed(2)).toLocaleString();
  }

  function processAggregatorRow(rows_table2, editedData) {
    for (var keys in rows_table2) {
      var row_data = {};
      var mandi_idDict = {};
      var gaddidar_idDict = {};
      var aggregator_idDict = {};
      row_data['date'] = $('#table2').DataTable().cell(keys - 1, 1).data();
      row_data['amount'] = $('#table2 tr').eq(parseInt(keys) + 1)[0].childNodes[4].innerHTML;
      mandi_idDict['online_id'] = $('#table2').DataTable().cell(keys - 1, 10).data();
      row_data['mandi'] = mandi_idDict;
      aggregator_idDict['online_id'] = $('#table2').DataTable().cell(keys - 1, 9).data();
      row_data['aggregator'] = aggregator_idDict;
      row_data['comment'] = $('#table2 tr').eq(parseInt(keys) + 1)[0].childNodes[9].innerHTML;
      editedData.push(row_data);
    }
    return editedData;
  }

  function processFarmerRow(rows_table2_farmer, editedDataFarmer) {
    for (var keys in rows_table2_farmer) {
      var row_data = {};
      var mandi_idDict = {};
      var gaddidar_idDict = {};
      var aggregator_idDict = {};
      row_data['date'] = $('#table2').DataTable().cell(keys - 1, 1).data();
      row_data['amount'] = $('#table2 tr').eq(parseInt(keys) + 1)[0].childNodes[6].innerHTML;
      mandi_idDict['online_id'] = $('#table2').DataTable().cell(keys - 1, 10).data();
      row_data['mandi'] = mandi_idDict;
      row_data['comment'] = $('#table2 tr').eq(parseInt(keys) + 1)[0].childNodes[10].innerHTML;
      aggregator_idDict['online_id'] = $('#table2').DataTable().cell(keys - 1, 9).data();
      row_data['aggregator'] = aggregator_idDict;
      row_data['user_created_id'] = $('#aggregator_payments :selected').val();
      row_data['user_modified_id'] = window.localStorage.user_id;
      editedDataFarmer.push(row_data);
    }
    return editedDataFarmer;
  }
  var gaddidarResetClicked = false;
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
    }, {
      title: "Aggregator Id",
      visible: false
    }, {
      title: "Mandi Id",
      visible: false
    }, {
      title: "Aggregator Comment",
      defaultContent: " "
    }, {
      title: "Farmer Comment",
      defaultContent: " "
    }],
    "dom": 'T<"clear">rtip',
    "pageLength": 1000,
    "oTableTools": {
      "sSwfPath": "/media/social_website/scripts/libs/tabletools_media/swf/copy_csv_xls_pdf.swf",
      "aButtons": [{

        "sExtends": "text",
        "sButtonText": "Edit",
        "fnClick": function(nButton, oConfig) {
          $('#ToolTables_table2_1').removeClass('disable-button');
          flag_edit_Table2 = true;
          superEditMode = 1;
          $("#gaddidar_payments").parent().addClass('disabled');
          $("#transportation_payments").parent().addClass('disabled');
          var colCount = $('#table2').dataTable().fnSettings().aoColumns.length - 1;
          for (var column = 0; column < colCount; column++)
            $('#table2').dataTable().fnSettings().aoColumns[column].bSortable = false;
          $('#table2').find('tr td:nth-child(5)').addClass('editcolumn');
          $('#table2').find('tr td:nth-child(7)').addClass('editcolumn');
          $('#aggregator_payment_tab :input')[0].disabled = true;
          $('#ToolTables_table2_0').addClass('disable-button');
          $('#payments_from_date').parent().parent().addClass('disable-button');
          $('#payments_from_date').removeClass('black-text');
          $('#payments_to_date').removeClass('black-text');
        }
      }, {
        "sExtends": "ajax",
        "sButtonText": "Submit",
        "sButtonClass": "disable-button",
        "sAjaxUrl": "/loop/api/v1/aggregatorshareoutliers/",

        "fnClick": function(nButton, oConfig) {
          var aggregatorAjaxSuccess = 0;
          var farmerAjaxSuccess = 0;
          var editedDataAggregator = [];
          var editedDataFarmer = [];
          $('#ToolTables_table2_0').removeClass('disable-button');
          editedDataAggregator = processAggregatorRow(rows_table2, editedDataAggregator);
          editedDataFarmer = processFarmerRow(rows_table2_farmer, editedDataFarmer);
          var sData = this.fnGetTableData(oConfig);
          var aggregatorObjects = {
            "objects": editedDataAggregator
          };
          var farmerObjects = {
            "objects": editedDataFarmer
          };
          if (Object.keys(rows_table2).length > 0) {
            $.ajax({
              url: oConfig.sAjaxUrl,
              type: 'patch',
              dataType: 'json',
              async: false,
              contentType: "application/json; charset=utf-8",
              headers: {
                "Authorization": "ApiKey " + window.localStorage.name + ":" + window.localStorage.akey
              },
              data: JSON.stringify(aggregatorObjects),
              success: function() {
                alert("Success : Aggregator Data");
                aggregatorAjaxSuccess = 1;
                for (var keys in rows_table2) {

                  aggregator_data_set[keys - 1][4] = parseFloat($('#table2 tr').eq(parseInt(keys) + 1)[0].childNodes[4].innerHTML);
                  aggregator_data_set[keys - 1][11] = $('#table2 tr').eq(parseInt(keys) + 1)[0].childNodes[9].innerHTML;
                }
                rows_table2 = [];
              },
              error: function() {
                aggregatorAjaxSuccess = -1;
                alert("Error While Syncing Aggregator Data");
              },
              timeout: 10000
            });
          }
          if (Object.keys(rows_table2_farmer).length > 0) {
            $.ajax({
              url: "/loop/farmer_payment_update/",
              type: 'PATCH',
              dataType: 'json',
              contentType: "application/json; charset=utf-8",
              async: false,
              data: JSON.stringify(farmerObjects),
              success: function() {
                alert("Success : Farmer Data");
                farmerAjaxSuccess = 1;
                for (var keys in rows_table2_farmer) {
                  aggregator_data_set[keys - 1][6] = parseFloat($('#table2 tr').eq(parseInt(keys) + 1)[0].childNodes[6].innerHTML);
                  aggregator_data_set[keys - 1][12] = $('#table2 tr').eq(parseInt(keys) + 1)[0].childNodes[10].innerHTML;
                }
                rows_table2_farmer = [];
              },
              error: function() {
                farmerAjaxSuccess = -1;
                alert("Error While Syncing Farmer Data");
              },
              timeout: 10000
            });
          }

          if (aggregatorAjaxSuccess != -1 && farmerAjaxSuccess != -1) {
            if (!($('#ToolTables_table3_0').hasClass('disable-button'))) {
              $('#aggregator_payment_tab :input')[0].disabled = false;
              $('#payments_from_date').parent().parent().removeClass('disable-button');
              $('#payments_from_date').addClass('black-text');
              $('#payments_to_date').addClass('black-text');
            }
            superEditMode = 0;
            $("#gaddidar_payments").parent().removeClass('disabled');
            $("#transportation_payments").parent().removeClass('disabled');
            $('#table2').find('td').removeClass("editcolumn");
            $('#table2').find('td').removeClass("editedcell");
            $('#table2').find('td').removeClass("editedcelledge");
            $('#ToolTables_table2_1').addClass('disable-button');
            flag_edit_Table2 = false;
            var colCount = $('#table2').dataTable().fnSettings().aoColumns.length;
            for (var column = 0; column < colCount; column++)
              $('#table2').dataTable().fnSettings().aoColumns[column].bSortable = true;
          }

        }
      }]
    },

    "footerCallback": function(row, data, start, end, display) {
      var api = this.api(),
        data;
      //Total of every column
      column_set = [3, 4, 5, 6, 7, 8];
      for (var i = 0; i < column_set.length; i++) {
        total = api.column(column_set[i]).data().reduce(function(a, b) {
          if (a === "") {
            a = 0;
          }
          if (b === "") {
            b = 0;
          }
          return parseFloat(a) + parseFloat(b);
        }, 0);
        $(api.column(column_set[i]).footer()).html(finalFormat(total + ""));
      }
    }
  });

  function initializeGaddidarModal() {
    $('#gaddidar_date_row').val($this.parent()[0].childNodes[0].innerHTML);
    $('#gaddidar_mandi_row').val($this.parent()[0].childNodes[2].innerHTML);
    $('#gaddidar_row').val($this.parent()[0].childNodes[1].innerHTML);
    $('#gaddidar_quantity_row').val($this.parent()[0].childNodes[3].innerHTML);
    $('#gaddidar_share_row').val(parseFloat($this.parent()[0].childNodes[5].textContent).toFixed(2));
    $('#gaddidar_amount_row').val(parseFloat($('#table3').DataTable().cell($this.context.parentNode.rowIndex - 1, 10).data()));
    $('#gaddidar_comment_row').val($this.parent()[0].childNodes[6].textContent);
    if ($('#table3').DataTable().cell($this.context.parentNode.rowIndex - 1, 11).data() == 1) {
      $('#gaddidar_commission_row').val(parseFloat($this.parent()[0].childNodes[4].innerHTML.split('%')[0]).toFixed(2));
      $('#gaddidar_commission_label')[0].innerHTML = 'Commission Agent Discount[CAD] (%)';
    } else {
      $('#gaddidar_commission_label')[0].innerHTML = 'Commission Agent Discount[CAD] (in Rs/Kg)';
      $('#gaddidar_commission_row').val(parseFloat($this.parent()[0].childNodes[4].innerHTML).toFixed(2));
    }
    $('#gaddidar_error_div').hide();
  }
  var flag_edit_Table3 = false;
  var rows_table3 = {};
  var editedGaddidar = 0;
  $('#table3').on('click', 'tbody td', function(e) {
    $this = $(this);
    if (flag_edit_Table3 == true && ($this.context.cellIndex === 4 || $this.context.cellIndex === 5)) {
      initializeGaddidarModal();
      $('#gaddidar_modal').openModal();
      if ($this.context.cellIndex === 4) {
        $('#gaddidar_commission_row').focus();
      } else {
        $('#gaddidar_share_row').focus();
      }
    }
  });
  $('#gaddidar_commission_row').on('change', function() {
    if (!inputValidation($('#gaddidar_commission_row'))) {
      actionOnInvalidValidation($('#gaddidar_commission_row'), $('#gaddidar_error_div'), $('#gaddidar_error_message'));
    } else {
      if ($('#table3').DataTable().cell($this.context.parentNode.rowIndex - 1, 11).data() == 0) {
        $('#gaddidar_share_row').val(parseFloat($this.parent()[0].childNodes[3].innerHTML * $('#gaddidar_commission_row').val()).toFixed(2));
      } else {
        $('#gaddidar_share_row').val(parseFloat($('#table3').DataTable().cell($this.context.parentNode.rowIndex - 1, 10).data() * ($('#gaddidar_commission_row').val() / 100)).toFixed(2));
      }

      if ($('#gaddidar_commission_row').val().trim() != '' && $('#gaddidar_commission_row').val().trim() != $this.parent()[0].childNodes[3].innerHTML)
        editedGaddidar = 1;
    }
  });

  $('#gaddidar_share_row').on('change', function() {
    if (!inputValidation($('#gaddidar_share_row'))) {
      actionOnInvalidValidation($('#gaddidar_share_row'), $('#gaddidar_error_div'), $('#gaddidar_error_message'));
    } else {
      if ($('#table3').DataTable().cell($this.context.parentNode.rowIndex - 1, 11).data() == 0) {
        $('#gaddidar_commission_row').val(parseFloat($('#gaddidar_share_row').val() / $this.parent()[0].childNodes[3].innerHTML).toFixed(2));
      } else {
        $('#gaddidar_commission_row').val((parseFloat($('#gaddidar_share_row').val() / $('#table3').DataTable().cell($this.context.parentNode.rowIndex - 1, 10).data()).toFixed(2)) * 100);
      }
      if ($('#gaddidar_commission_row').val().trim() != '' && $('#gaddidar_commission_row').val().trim() != $this.parent()[0].childNodes[4].innerHTML)
        editedGaddidar = 3;
    }
  });

  $('#gaddidar_comment_row').on('change', function() {
    if ($('#gaddidar_comment_row').val().trim() != '' && editedGaddidar == 0)
      editedGaddidar = 2;
  });
  $('#gaddidar_commission_row').keypress(function(event) {
    if (event.keyCode === 13) {
      $('#gaddidar_comment_row').focus();
    }
  });

  $('#gaddidar_share_row').keypress(function(event) {
    if (event.keyCode === 13) {
      $('#gaddidar_comment_row').focus();
    }
  });

  $('#gaddidar_comment_row').keypress(function(event) {
    if (event.keyCode === 13) {
      if (!inputValidation($('#gaddidar_commission_row'))) {
        actionOnInvalidValidation($('#gaddidar_commission_row'), $('#gaddidar_error_div'), $('#gaddidar_error_message'));
      } else if (!inputValidation($('#gaddidar_share_row'))) {
        actionOnInvalidValidation($('#gaddidar_share_row'), $('#gaddidar_error_div'), $('#gaddidar_error_message'));
      } else {
        $('#gaddidar_comment_row').trigger('change');
        $('#gaddidar_submit_modal').trigger('click');
      }
    }
  });
  $('#gaddidar_close').on('click', function() {
    gaddidarResetClicked = false;
    $('#gaddidar_modal').closeModal();
  })
  $('#gaddidar_reset_modal').on('click', function() {
    gaddidarResetClicked = true;
    $('#gaddidar_share_row').val($('#table3').DataTable().cell($this.context.parentNode.rowIndex - 1, 5).data());
    if ($('#table3').DataTable().cell($this.context.parentNode.rowIndex - 1, 11).data() == 1)
      $('#gaddidar_commission_row').val(parseFloat($('#table3').DataTable().cell($this.context.parentNode.rowIndex - 1, 4).data().split('%')[0]).toFixed(2));
    else
      $('#gaddidar_commission_row').val($('#table3').DataTable().cell($this.context.parentNode.rowIndex - 1, 4).data());
    $('#gaddidar_comment_row').val($('#table3').DataTable().cell($this.context.parentNode.rowIndex - 1, 9).data());
  });
  $('#gaddidar_submit_modal').on('click', function(ev) {
    if (!inputValidation($('#gaddidar_commission_row'))) {
      ev.preventDefault();
      $('#gaddidar_commission_row').val($this.parent()[0].childNodes[4].innerHTML);
      $('#gaddidar_share_row').val($this.parent()[0].childNodes[5].textContent);
      $('#gaddidar_commission_row').focus();
      return false;

    } else if (!inputValidation($('#gaddidar_share_row'))) {
      ev.preventDefault();
      $('#gaddidar_commission_row').val($this.parent()[0].childNodes[4].innerHTML);
      $('#gaddidar_share_row').val($this.parent()[0].childNodes[5].textContent);
      $('#gaddidar_share_row').focus();
      return false;

    } else if (gaddidarResetClicked && editedGaddidar == 0) {
      $this.parent()[0].childNodes[4].innerHTML = $('#table3').DataTable().cell($this.context.parentNode.rowIndex - 1, 4).data();
      $this.parent()[0].childNodes[5].innerHTML = $('#table3').DataTable().cell($this.context.parentNode.rowIndex - 1, 5).data();
      $this.parent()[0].childNodes[6].innerHTML = $('#table3').DataTable().cell($this.context.parentNode.rowIndex - 1, 9).data();
      delete rows_table3[$this.context.parentNode.rowIndex];
      $this.removeAttr('class');
      $this.closest('tr').children('td:nth-child(5)')[0].className = 'editcolumn';
      $this.closest('tr').children('td:nth-child(6)')[0].className = 'editcolumn';
      $this.closest('tr').children('td:nth-child(7)')[0].className = '';
      $this.addClass('editcolumn');
      gaddidarResetClicked = false;
    } else if (editedGaddidar != 0) {
      $('#gaddidar_modal').closeModal();
      if ($('#table3').DataTable().cell($this.context.parentNode.rowIndex - 1, 11).data() == 1)
        $this.parent()[0].childNodes[4].innerHTML = $('#gaddidar_commission_row').val() + '%';
      else
        $this.parent()[0].childNodes[4].innerHTML = $('#gaddidar_commission_row').val();
      $this.parent()[0].childNodes[5].innerHTML = $('#gaddidar_share_row').val();
      $this.parent()[0].childNodes[6].innerHTML = $('#gaddidar_comment_row').val() + ' - ' + window.localStorage.name;
      if ($('#table3').DataTable().cell($this.context.parentNode.rowIndex - 1, 11).data() == 1) {
        if (parseFloat($this.parent()[0].childNodes[4].innerHTML) / 100 > 0.1) {
          $this.closest('tr').children('td:nth-child(5)')[0].className = 'editedcelledge';
          $this.closest('tr').children('td:nth-child(6)')[0].className = 'editedcelledge';
          $this.closest('tr').children('td:nth-child(7)')[0].className = 'editedcelledge';
        } else {
          $this.closest('tr').children('td:nth-child(5)')[0].className = 'editedcell';
          $this.closest('tr').children('td:nth-child(6)')[0].className = 'editedcell';
          $this.closest('tr').children('td:nth-child(7)')[0].className = 'editedcell';
        }
      } else {
        if (parseFloat($this.parent()[0].childNodes[4].innerHTML) > 1) {
          $this.closest('tr').children('td:nth-child(5)')[0].className = 'editedcelledge';
          $this.closest('tr').children('td:nth-child(6)')[0].className = 'editedcelledge';
          $this.closest('tr').children('td:nth-child(7)')[0].className = 'editedcelledge';
        } else {
          $this.closest('tr').children('td:nth-child(5)')[0].className = 'editedcell';
          $this.closest('tr').children('td:nth-child(6)')[0].className = 'editedcell';
          $this.closest('tr').children('td:nth-child(7)')[0].className = 'editedcell';
        }
      }
      var row_id = $this.context.parentNode.rowIndex;
      rows_table3[row_id] = true;
      editedGaddidar = 0;
    }
    $('#gaddidar_modal').closeModal();
  });

  function processGaddidarRow(rows_table3, editedData) {
    for (var keys in rows_table3) {
      var row_data = {}
      var mandi_idDict = {}
      var gaddidar_idDict = {}
      var aggregator_idDict = {}
      row_data['date'] = $('#table3').DataTable().cell(keys - 1, 0).data();
      row_data['amount'] = $('#table3 tr').eq(parseInt(keys) + 1)[0].childNodes[5].innerHTML;
      mandi_idDict['online_id'] = $('#table3').DataTable().cell(keys - 1, 6).data();
      row_data['mandi'] = mandi_idDict
      gaddidar_idDict['online_id'] = $('#table3').DataTable().cell(keys - 1, 7).data();
      row_data['gaddidar'] = gaddidar_idDict
      aggregator_idDict['online_id'] = $('#table3').DataTable().cell(keys - 1, 8).data();
      row_data['aggregator'] = aggregator_idDict
      row_data['comment'] = $('#table3 tr').eq(parseInt(keys) + 1)[0].childNodes[6].innerHTML;
      editedData.push(row_data);
    }
    return editedData;
  }

  $('#table3').DataTable({
    destroy: true,
    data: gaddidar_data_set_clone,
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
    }, {
      title: "Mandi Id",
      visible: false
    }, {
      title: "Gaddidar Id",
      visible: false
    }, {
      title: "Aggregator Id",
      visible: false
    }, {
      title: "Comment"

    }, {
      title: "Amount",
      visible: false
    }, {
      title: "Discount Criteria",
      visible: false
    }],
    "dom": 'T<"clear">rtip',
    //"dom":'Bfrtip',

    "pageLength": 1000,

    "oTableTools": {
      "sSwfPath": "/media/social_website/scripts/libs/tabletools_media/swf/copy_csv_xls_pdf.swf",
      "aButtons": [{

        "sExtends": "text",
        "sButtonText": "Edit",
        "fnClick": function(nButton, oConfig) {
          $('#aggregator_payment_tab :input')[0].disabled = true;
          superEditMode = 1;
          $("#summary_payments").parent().addClass('disabled');
          $("#transportation_payments").parent().addClass('disabled');
          $('#ToolTables_table3_1').removeClass('disable-button');
          $('#ToolTables_table3_0').addClass('disable-button');
          $('#payments_from_date').parent().parent().addClass('disable-button');
          $('#payments_from_date').removeClass('black-text');
          $('#payments_to_date').removeClass('black-text');
          flag_edit_Table3 = true;
          $('#table3').find('tr td:nth-child(5)').addClass('editcolumn');
          $('#table3').find('tr td:nth-child(6)').addClass('editcolumn');
          var colCount = $('#table3').dataTable().fnSettings().aoColumns.length;
          for (var column = 0; column < colCount; column++)
            $('#table3').dataTable().fnSettings().aoColumns[column].bSortable = false;

        }
      }, {
        "sExtends": "ajax",
        "sButtonText": "Submit",
        "sButtonClass": "disable-button",
        "sAjaxUrl": "/loop/api/v1/gaddidarshareoutliers/",
        "fnClick": function(nButton, oConfig) {
          var editedDataGaddidar = [];
          var gaddidarAjaxSuccess = 0;
          $('#ToolTables_table3_0').removeClass('disable-button');
          editedDataGaddidar = processGaddidarRow(rows_table3, editedDataGaddidar);
          var sData = this.fnGetTableData(oConfig);
          var gaddidarObjects = {
            "objects": editedDataGaddidar

          };
          if (Object.keys(rows_table3).length > 0)
            $.ajax({
              url: oConfig.sAjaxUrl,
              type: 'patch',
              dataType: 'json',
              async: false,
              contentType: "application/json; charset=utf-8",
              headers: {
                "Authorization": "ApiKey " + window.localStorage.name + ":" + window.localStorage.akey
              },
              data: JSON.stringify(gaddidarObjects),
              success: function() {
                alert("Success : Gaddidar Data");
                gaddidarAjaxSuccess = 1;
                for (var keys in rows_table3) {
                  if (($('#table3 tr').eq(parseInt(keys) + 1)[0].childNodes[4].innerHTML).indexOf('%') >= 0) {
                    gaddidar_data_set[keys - 1][4] = parseFloat(($('#table3 tr').eq(parseInt(keys) + 1)[0].childNodes[4].innerHTML).split('%')[0]) / 100;
                  } else {
                    gaddidar_data_set[keys - 1][4] = parseFloat($('#table3 tr').eq(parseInt(keys) + 1)[0].childNodes[4].innerHTML);
                  }
                  gaddidar_data_set[keys - 1][5] = parseFloat($('#table3 tr').eq(parseInt(keys) + 1)[0].childNodes[5].innerHTML);
                  gaddidar_data_set[keys - 1][6] = parseFloat($('#table3 tr').eq(parseInt(keys) + 1)[0].childNodes[6].innerHTML);
                  gaddidar_data_set_clone[keys - 1][4] = $('#table3 tr').eq(parseInt(keys) + 1)[0].childNodes[4].innerHTML;
                  gaddidar_data_set_clone[keys - 1][5] = parseFloat($('#table3 tr').eq(parseInt(keys) + 1)[0].childNodes[5].innerHTML);
                  gaddidar_data_set_clone[keys - 1][6] = parseFloat($('#table3 tr').eq(parseInt(keys) + 1)[0].childNodes[6].innerHTML);
                }
                rows_table3 = [];
                get_payments_data();
                delay = 6000;
                setTimeout(function() {
                  $("#aggregator_payments").val(aggregator).change();
                  $("#aggregator_payment_tab :input").val(aggregator_name_input);

                }, delay);

              },
              error: function() {
                alert("Error While Syncing Gaddidar Data");
                gaddidarAjaxSuccess = -1;
                /*  $('#table3').dataTable().fnClearTable();
                  $('#table3').dataTable().fnAddData(gaddidar_data_set);
                  rows_table3 = [];*/
              },
              timeout: 10000
            });
          if (gaddidarAjaxSuccess != -1) {
            if (!($('#ToolTables_table2_0').hasClass('disable-button'))) {
              $('#aggregator_payment_tab :input')[0].disabled = false;
              $('#payments_from_date').parent().parent().removeClass('disable-button');
              $('#payments_from_date').addClass('black-text');
              $('#payments_to_date').addClass('black-text');
            }
            var colCount = $('#table3').dataTable().fnSettings().aoColumns.length;
            for (var column = 0; column < colCount; column++)
              $('#table3').dataTable().fnSettings().aoColumns[column].bSortable = true;
            $('#table3').find('td').removeClass("editcolumn");
            $('#table3').find('td').removeClass("editedcell");
            $('#table3').find('td').removeClass("editedcelledge");
            flag_edit_Table3 = false;
            $('#ToolTables_table3_1').addClass('disable-button');
            superEditMode = 0;
            $("#summary_payments").parent().removeClass('disabled');
            $("#transportation_payments").parent().removeClass('disabled');
          }
        }
      }]
    },
    "footerCallback": function(row, data, start, end, display) {
      var api = this.api(),
        data;
      //Total of every column
      column_set = [3, 5];
      for (var i = 0; i < column_set.length; i++) {
        total = api.column(column_set[i]).data().reduce(function(a, b) {
          return a + b;
        }, 0);
        $(api.column(column_set[i]).footer()).html(finalFormat(total + ""));
      }
    }
  });
  var flag_edit_Table4 = false;
  var editedTransportation = 0;
  var rows_table4 = {};

  function initializeTransportModal() {
    $('#transportation_date_row').val($this.parent()[0].childNodes[0].innerHTML);
    $('#transportation_mandi_row').val($this.parent()[0].childNodes[1].innerHTML);
    $('#transportation_transporter_row').val($this.parent()[0].childNodes[2].innerHTML);

    $('#transportation_vehicle_row').val($this.parent()[0].childNodes[4].innerHTML);
    $('#transportation_number_row').val($this.parent()[0].childNodes[5].innerHTML);
    $('#transportation_cost_row').val(parseFloat($this.parent()[0].childNodes[6].textContent).toFixed(2));
    $('#transportation_comment_row').val($this.parent()[0].childNodes[7].textContent);
    $('#transportation_error_div').hide();
  };


  $('#table4').on('click', 'tbody td', function(e) {
    $this = $(this);
    if (flag_edit_Table4 == true && ($this.context.cellIndex === 6)) {
      initializeTransportModal();
      $('#transportation_modal').openModal();
      $('#transportation_cost_row').focus();
    }
  });
  $('#transportation_close').on('click', function() {
    transportationResetClick = false;
    $('#transportation_modal').closeModal();
  });
  $('#transportation_cost_row').on('change', function() {
    if (!inputValidation($('#transportation_cost_row'))) {
      actionOnInvalidValidation($('#transportation_share_row'), $('#transportation_error_div'), $('#transportation_error_message'));
    } else if ($('#transportation_cost_row').val().trim() != '' && $('#transportation_cost_row').val().trim() != $this.parent()[0].childNodes[6].innerHTML) {
      editedTransportation = 1;
    }
  });
  $('#transportation_comment_row').on('change', function() {
    if ($('#transportation_comment_row').val().trim() != '' && editedTransportation == 0) {
      editedTransportation = 2;
    }

  });
  $('#transportation_cost_row').keypress(function(event) {
    if (event.keyCode === 13) {
      $('#transportation_comment_row').focus();
    }
  });
  $('#transportation_comment_row').keypress(function(event) {
    if (event.keyCode === 13) {
      if (!inputValidation($('#transportation_cost_row'))) {
        actionOnInvalidValidation($('#transportation_share_row'), $('#transportation_error_div'), $('#transportation_error_message'));
        $('#transportation_cost_row').focus();
      } else {
        $('#transportation_submit_modal').trigger('click');
      }
    }
  });
  $('#transportation_reset_modal').on('click', function() {
    transportationResetClick = true;
    $('#transportation_cost_row').val($('#table4').DataTable().cell($this.context.parentNode.rowIndex - 1, 6).data());
    $('#transportation_comment_row').val($('#table4').DataTable().cell($this.context.parentNode.rowIndex - 1, 7).data());
  });
  $('#transportation_submit_modal').on('click', function(ev) {
    if (!inputValidation($('#transportation_cost_row'))) {
      ev.preventDefault();
      $('#transportation_cost_row').val($this.parent()[0].childNodes[6].textContent);
      $('#aggregator_commission_row').focus();
      return false;
    } else if (transportationResetClick) {
      $this.parent()[0].childNodes[6].innerHTML = parseFloat($('#table4').DataTable().cell($this.context.parentNode.rowIndex - 1, 6).data()).toFixed(2);
      $this.closest('tr').children('td:nth-child(8)')[0].innerHTML = $('#table4').DataTable().cell($this.context.parentNode.rowIndex - 1, 7).data();
      delete rows_table4[$this.context.parentNode.rowIndex];
      $this.removeAttr('class');
      $this.closest('tr').children('td:nth-child(8)')[0].className = '';
      $this.addClass('editcolumn');
      transportationResetClick = false;
    } else if (editedTransportation != 0) {
      $('#transportation_modal').closeModal();
      $this.parent()[0].childNodes[6].innerHTML = $('#transportation_cost_row').val();
      $this.parent()[0].childNodes[7].innerHTML = $('#transportation_comment_row').val() + ' - ' + window.localStorage.name;
      $this.removeAttr('class');
      $this.addClass('editedcell');
      $this.closest('tr').children('td:nth-child(8)')[0].className = 'editedcell';
      var row_id = $this.context.parentNode.rowIndex;
      rows_table4[row_id] = true;
      editedTransportation = 0;
      $('#transportation_error_div').hide();
    }
    $('#transportation_modal').closeModal();
  });

  function processTransportationRow(rows_table4, editedData) {
    for (var keys in rows_table4) {
      var row_data = {};
      var aggregator_idDict = {};
      var mandi_idDict = {};
      var transportationvehicle_idDict = {};
      //row_data['id'] = $('#table4').DataTable().cell(keys - 1, 0).data();
      aggregator_idDict['online_id'] = agg_id;
      row_data['aggregator'] = aggregator_idDict;
      mandi_idDict['online_id'] = $('#table4').DataTable().cell(keys - 1, 8).data();
      row_data['mandi'] = mandi_idDict;
      transportationvehicle_idDict["online_id"] = $('#table4').DataTable().cell(keys - 1, 9).data();
      row_data['transportation_vehicle'] = transportationvehicle_idDict;
      row_data['date'] = $('#table4').DataTable().cell(keys - 1, 0).data();
      row_data['timestamp'] = $('#table4').DataTable().cell(keys - 1, 10).data();
      row_data['transportation_cost'] = $('#table4 tr').eq(parseInt(keys) + 1)[0].childNodes[6].innerHTML;
      row_data['transportation_cost_comment'] = $('#table4 tr').eq(parseInt(keys) + 1)[0].childNodes[7].innerHTML;
      editedData.push(row_data);
    }
    return editedData;
  }

  var transportationResetClick = false;
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
      title: "Phone Number"
    }, {
      title: "Vehicle Type"
    }, {
      title: "Vehicle Number"
    }, {
      title: "Transport Cost (in Rs)"
    }, {
      title: "Comment",
      defaultContent: " "
    }, {
      title: "Mandi Id",
      visible: false
    }, {
      title: "Transportation Vehicle Id",
      visible: false
    }, {
      title: "Timestamp",
      visible: false
    }, {
      title: "RowId",
      visible: false
    }],
    "dom": 'T<"clear">rtip',
    "pageLength": 1000,
    "oTableTools": {
      "sSwfPath": "/media/social_website/scripts/libs/tabletools_media/swf/copy_csv_xls_pdf.swf",
      "aButtons": [{

        "sExtends": "text",
        "sButtonText": "Edit",
        "fnClick": function(nButton, oConfig) {
          $('#aggregator_payment_tab :input')[0].disabled = true;
          superEditMode = 1;
          $("#summary_payments").parent().addClass('disabled');
          $("#gaddidar_payments").parent().addClass('disabled');
          $('#ToolTables_table4_1').removeClass('disable-button');
          $('#ToolTables_table4_0').addClass('disable-button');
          $('#payments_from_date').parent().parent().addClass('disable-button');
          $('#payments_from_date').removeClass('black-text');
          $('#payments_to_date').removeClass('black-text');
          flag_edit_Table4 = true;
          $('#table4').find('tr td:nth-child(7)').addClass('editcolumn');
          //$('#table4').find('tr td:nth-child(7)').addClass('editcolumn');
          var colCount = $('#table4').dataTable().fnSettings().aoColumns.length;
          for (var column = 0; column < colCount; column++)
            $('#table4').dataTable().fnSettings().aoColumns[column].bSortable = false;

        }
      }, {
        "sExtends": "ajax",
        "sButtonText": "Submit",
        "sButtonClass": "disable-button",
        "sAjaxUrl": "/loop/api/v1/daytransportation/",
        "fnClick": function(nButton, oConfig) {
          var editedDataTransportation = [];
          var transportationAjaxSuccess = 0;
          $('#ToolTables_table4_0').removeClass('disable-button');
          flag_edit_Table4 = false;
          $('#ToolTables_table4_1').addClass('disable-button');
          superEditMode = 0;
          $("#summary_payments").parent().removeClass('disabled');
          $("#gaddidar_payments").parent().removeClass('disabled');
          $('#table4').find('td').removeClass("editcolumn");
          $('#table4').find('td').removeClass("editedcell");
          $('#table4').find('td').removeClass("editedcelledge");
          editedDataTransportation = processTransportationRow(rows_table4, editedDataTransportation);
          //console.log(editedDataTransportation);
          //editedDataGaddidar = processGaddidarRow(rows_table3, editedDataGaddidar);
          var sData = this.fnGetTableData(oConfig);
          var transportationObjects = {
            "objects": editedDataTransportation

          };
          if (Object.keys(rows_table4).length > 0) {
            $.ajax({
              url: oConfig.sAjaxUrl,
              type: 'patch',
              dataType: 'json',
              async: false,
              contentType: "application/json; charset=utf-8",
              headers: {
                "Authorization": "ApiKey " + window.localStorage.name + ":" + window.localStorage.akey
              },
              data: JSON.stringify(transportationObjects),
              success: function() {
                alert("Success : Transportation Data");
                transportationAjaxSuccess = 1;
                for (var keys in rows_table4) {
                  transporter_data_set[keys - 1][6] = parseFloat($('#table4 tr').eq(parseInt(keys) + 1)[0].childNodes[6].innerHTML);
                  transporter_data_set[keys - 1][7] = $('#table4 tr').eq(parseInt(keys) + 1)[0].childNodes[7].innerHTML;
                  //console.log(transporter_data_set[keys - 1][7]);
                  transport_payment[transporter_data_set[keys - 1][11]]['transportation_cost__sum'] = transporter_data_set[keys - 1][6];
                  transport_payment[transporter_data_set[keys - 1][11]]['transportation_cost_comment'] = transporter_data_set[keys - 1][7];
                }
                rows_table4 = [];
                get_payments_data();
                delay = 6000;
                setTimeout(function() {
                  $("#aggregator_payments").val(aggregator).change();
                  $("#aggregator_payment_tab :input").val(aggregator_name_input);

                }, delay);

              },
              error: function() {
                alert("Error While Syncing Transportation Data");
                transportationAjaxSuccess = -1;

              },
              timeout: 10000
            });
            //console.log(rows_table4)
          }
          if (transportationAjaxSuccess != -1) {
            if (!($('#ToolTables_table4_0').hasClass('disable-button'))) {
              $('#aggregator_payment_tab :input')[0].disabled = false;
              $('#payments_from_date').parent().parent().removeClass('disable-button');
              $('#payments_from_date').addClass('black-text');
              $('#payments_to_date').addClass('black-text');
            }
            var colCount = $('#table4').dataTable().fnSettings().aoColumns.length;
            for (var column = 0; column < colCount; column++)
              $('#table4').dataTable().fnSettings().aoColumns[column].bSortable = true;
            $('#table4').find('td').removeClass("editcolumn");
            $('#table4').find('td').removeClass("editedcell");
            $('#table4').find('td').removeClass("editedcelledge");
            flag_edit_Table4 = false;
            $('#ToolTables_table4_1').addClass('disable-button');
            superEditMode = 0;
            $("#summary_payments").parent().removeClass('disabled');
            $("#transportation_payments").parent().removeClass('disabled');
          }
        }
      }]
    },
    "footerCallback": function(row, data, start, end, display) {
      var api = this.api(),
        data;

      // Total over all pages
      var totalCost = api
        .column(6)
        .data()
        .reduce(function(a, b) {
          return a + b;

        }, 0);


      // Update footer
      $(api.column(7).footer()).html(
        finalFormat(totalCost + "")
      );
    }
  });

  aggregator_sheet_name = "Aggregator Payment_" + getFormattedDate(aggregator) + "Payment Summary";
  gaddidar_sheet_name = "Aggregator Payment_" + getFormattedDate(aggregator) + "Commission Agent Details";
  transporter_sheet_name = "Aggregator Payment_" + getFormattedDate(aggregator) + "Transporter Details";
  create_data_for_excel_download();
}

function create_data_for_excel_download() {
  header_dict = {
    'aggregator': [{
        'column_width': 2.45,
        'formula': null,
        'label': 'S No',
        'total': false
      },
      {
        'column_width': 9,
        'formula': null,
        'label': 'Date',
        'total': false
      },
      {
        'column_width': 9.64,
        'formula': null,
        'label': 'Market',
        'total': false
      },
      {
        'column_width': 7.64,
        'formula': null,
        'label': 'Quantity [Q] (in Kg)',
        'total': true
      },
      {
        'column_width': 10.64,
        'formula': null,
        'label': 'Aggregator Payment [AP] (in Rs) (0.25*Q)',
        'total': true
      },
      {
        'column_width': 8,
        'formula': null,
        'label': 'Transport Cost [TC] (in Rs)',
        'total': true
      },
      {
        'column_width': 10.18,
        'formula': null,
        'label': "Farmers' Contribution [FC] (in Rs)",
        'total': true
      },
      {
        'column_width': 10.18,
        'formula': null,
        'label': 'Commission Agent Contribution [CAC] (in Rs)',
        'total': true
      },
      {
        'column_width': 8.73,
        'formula': 'E + F - G - H',
        'label': 'Total Payment (in Rs) (AP + TC - FC - CAC)',
        'total': true
      },
      {
        'column_width': 8,
        'formula': null,
        'label': 'Aggregator Comment',
        'total': false
      },
      {
        'column_width': 8,
        'formula': null,
        'label': 'Farmer Comment',
        'total': false
      }
    ],
    'gaddidar': [{
        'column_width': 9.4,
        'formula': null,
        'label': 'Date',
        'total': false
      },
      {
        'column_width': 18.3,
        'formula': null,
        'label': 'Commission Agent',
        'total': false
      },
      {
        'column_width': 11,
        'formula': null,
        'label': 'Market',
        'total': false
      },
      {
        'column_width': 10,
        'formula': null,
        'label': 'Quantity [Q] (in Kg)',
        'total': true
      },
      {
        'column_width': 13,
        'formula': null,
        'label': 'Commission Agent Discount [CAD] (in Rs/Kg)',
        'total': false
      },
      {
        'column_width': 16,
        'formula': null,
        'label': 'Commission Agent Contribution [CAC] (in Rs) (Q*CAD)',
        'total': true
      },
      {
        'column_width': 10,
        'formula': null,
        'label': 'Comment',
        'total': false
      }
    ],
    'transporter': [{
        'column_width': 8.4,
        'formula': null,
        'label': 'Date',
        'total': false
      },
      {
        'column_width': 11,
        'formula': null,
        'label': 'Market',
        'total': false
      },
      {
        'column_width': 17.3,
        'formula': null,
        'label': 'Transporter',
        'total': false
      },
      {
        'column_width': 11,
        'formula': null,
        'label': 'Phone Number',
        'total': false
      },
      {
        'column_width': 9.4,
        'formula': null,
        'label': 'Vehicle',
        'total': false
      },
      {
        'column_width': 11,
        'formula': null,
        'label': 'Vehicle Number',
        'total': false
      },
      {
        'column_width': 13,
        'formula': null,
        'label': 'Tranport Cost (in Rs)',
        'total': true
      }
    ]
  };
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
  hidePaymentDetails();
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
      if (language == ENGLISH_LANGUAGE) {
        fill_drop_down($('#aggregator_payments'), aggregators_for_filter, 'user__id', 'name_en', 'Aggregator', 'id');
      } else {
        fill_drop_down($('#aggregator_payments'), aggregators_for_filter, 'user__id', 'name', 'Aggregator', 'id');
      }
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
        if (data_set[j].indexOf(payments_gaddidar_contribution[i]['gaddidar__name']) != -1) {
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
    "dom": 'T<"clear">rtip',
    "pageLength": 20
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
  container.highcharts(Highcharts.merge(generalOptions, gaugeOptions, {
    yAxis: {
      min: minimum,
      max: target
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
    fill_crop_filter(crops_for_filter);
  else
  {
    // If country is India, then Regional Language is Hindi
    if (country_id == 1)
      fill_crop_filter(croplanguage_for_filter[HINDI_ID]);
    // If country is Bangladesh, then Regional Language is Bangla
    else if (country_id == 2)
      fill_crop_filter(croplanguage_for_filter[BANGLA_ID]);
  }
  get_data("", country_id);
  if (selected_page == ANALYTICS_PAGE || selected_page == TIME_SERIES_PAGE) {
    show_nav(selected_page);
  }
}

function change_country(country) {

  country_id = country;
  if (country_id == 1){
    CURRENCY = RUPEE;
    $("#totalpaytext").text("Payments("+CURRENCY+")");
    $("#recentpaytext").text("Payments("+CURRENCY+")");

  }
  else{
    CURRENCY = TAKA;
    $("#totalpaytext").text("Payments("+CURRENCY+")");
    $("#recentpaytext").text("Payments("+CURRENCY+")");

  }
  total_static_data(country);
  recent_graphs_data(language, country);
  get_filter_data(language, country);
}

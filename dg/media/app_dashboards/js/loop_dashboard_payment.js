/* This file should contain all the JS for Loop dashboard */
window.onload = initialize;

var language, country_id = 1, state_id = -1;
var selected_aggregator_state, selected_aggregator_country;
//Arrays containing ids and corresponding names as were selected in the filters.
var aggregator_ids, aggregator_names, aggregator_states, aggregators_countries, crop_ids, crop_names, mandi_ids, mandi_names, gaddidar_ids, gaddidar_names;
//Json for filters.
var aggregators_for_filter, aggregators_for_admin, mandis_for_filter, gaddidars_for_filter, crops_for_filter, croplanguage_for_filter, transporter_for_filter;
//Variables for payments tab.
var payments_start_date, payments_to_date, selected_aggregator, agg_id, payment_model;
var payments_data, outliers_data, outliers_transport_data, outlier_daily_data, payments_gaddidar_contribution;
var aggregator_payment, transport_payment, gaddidar_contribution_data, aggregator_incentive;
var aggregator_table_created = false;
var gaddidar_table_created = false;
var transporter_table_created = false;
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

//var TIME_DIFF_THIRTY_DAYS = 2592000000;
var TIME_DIFF_THIRTY_DAYS = 5184000000;

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

var PAYMENT_SUMMARY = {
  SNO : null,
  DATE : null,
  MANDI_NAME : null,
  QUANTITY : null,
  QUANTITY_POST_DEDUCTION : null,
  AGGREGATOR_INCENTIVE : null,
  FARMER_SHARE_IN_AGGREGATOR_INCENTIVE: null,
  TRANSPORT_COST : null,
  FARMER_SHARE : null,
  GADDIDAR_SHARE : null,
  NET_PAYMENT : null,
  AGGREGATOR_COMMENT : null,
  FARMER_COMMENT : null,
  AGG_ID : null,
  MANDI_ID : null,
  NET_QUANTITY : null
};

var COMMISSION_AGENT_DETAILS = {
  DATE : null,
  GADDIDAR_NAME : null,
  MANDI_NAME : null,
  QUANTITY : null,
  GADDIDAR_DISCOUNT : null,
  GADDIDAR_COMMISSION : null,
  GADDIDAR_COMMENT : null,
  MANDI_ID : null,
  GADDIDAR_ID : null,
  AGG_ID : null,
  AMOUNT : null,
  GADDIDAR_DISCOUNT_CRITERIA : null
};

var TRANSPORTER_DETAILS = {
  DATE : null,
  MANDI_NAME : null,
  TRANSPORTER_NAME : null,
  TRANSPORTER_PHONE : null,
  VEHICLE_TYPE : null,
  VEHICLE_NUMBER : null,
  TRANSPORT_COST : null,
  TRANSPORTER_COMMENT : null,
  MANDI_ID : null,
  TRANSPORTATION_VEHICLE_ID : null,
  TIMESTAMP : null,
  ROW_ID : null
};

var globalApi;
var initialLoadComplete;
var gaddidar, table_created;
var dates, stats, transportation, gaddidar_contribution_recent_graph, aggregator_incentive_cost;
var detailChartHome, detailChartTimeSeriesVol, detailChartTimeSeriesCPK;
var superEditMode = 0;
var executed_calc_functions = new Set();
var dates = [];
var mandis = [];
var quantites = [];
var gaddidar_amount = [];
var transport_cost = [];
var farmer_share = [];

//functions to compute table data
var calc_functions = {
  gaddidar_data: function() {
    for (var i = 0; i < aggregator_payment.length; i++) {
      var date_index = dates.indexOf(aggregator_payment[i]['date']);
      if (date_index == -1) {
        dates.push(aggregator_payment[i]['date']);
        mandis.push([]);
        quantites.push([]);
        gaddidar_amount.push([]);
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
      gaddidar_data_set[i][COMMISSION_AGENT_DETAILS.DATE] = aggregator_payment[i]['date'];    
      gaddidar_data_set[i][COMMISSION_AGENT_DETAILS.GADDIDAR_NAME] = aggregator_payment[i]['gaddidar__gaddidar_name'];    
      gaddidar_data_set[i][COMMISSION_AGENT_DETAILS.MANDI_NAME] = aggregator_payment[i]['mandi__mandi_name'];    
      gaddidar_data_set[i][COMMISSION_AGENT_DETAILS.QUANTITY] = parseFloat(aggregator_payment[i][QUANTITY__SUM].toFixed(2));    
      gaddidar_data_set[i][COMMISSION_AGENT_DETAILS.MANDI_ID] = aggregator_payment[i][MANDI__ID];    
      gaddidar_data_set[i][COMMISSION_AGENT_DETAILS.GADDIDAR_ID] = aggregator_payment[i][GADDIDAR__ID];    
      gaddidar_data_set[i][COMMISSION_AGENT_DETAILS.AGG_ID] = agg_id;    
      gaddidar_data_set[i][COMMISSION_AGENT_DETAILS.AMOUNT] = parseFloat(aggregator_payment[i][AMOUNT__SUM].toFixed(2));    
      gaddidar_data_set[i][COMMISSION_AGENT_DETAILS.GADDIDAR_DISCOUNT_CRITERIA] = aggregator_payment[i]['gaddidar__discount_criteria'];        
    }
  },
  gaddidar_commission: function() {
    for (var i = 0; i < gaddidar_contribution_data.length; i++) {
      for (var j = 0; j < gaddidar_data_set.length; j++) {
        if (gaddidar_data_set[j].indexOf(gaddidar_contribution_data[i]['date']) != -1 && gaddidar_data_set[j].indexOf(gaddidar_contribution_data[i]['gaddidar__name']) != -1) {
          gaddidar_data_set[j][COMMISSION_AGENT_DETAILS.GADDIDAR_DISCOUNT] = parseFloat(gaddidar_contribution_data[i]['gaddidar_discount']);
          gaddidar_data_set[j][COMMISSION_AGENT_DETAILS.GADDIDAR_COMMISSION] = parseFloat(gaddidar_contribution_data[i]['amount']);
          gaddidar_data_set[j][COMMISSION_AGENT_DETAILS.GADDIDAR_COMMENT] = gaddidar_contribution_data[i]['comment'];
        }
      }
    }
  },
  gaddidar_amount: function() {
    for (var i = 0; i < gaddidar_contribution_data.length; i++) {
      var date_index = dates.indexOf(gaddidar_contribution_data[i]['date']);
      if (date_index != -1) {
        var mandi_index = mandis[date_index].map(function(e) {
          return e.mandi_name;
        }).indexOf(gaddidar_contribution_data[i]['mandi__name']);
        if (mandi_index != -1) {
          gaddidar_amount[date_index][mandi_index] += parseFloat(gaddidar_contribution_data[i]['amount']);
        }
      }
    }
  },
  transporter_data: function() {
    for (var i = 0; i < transport_payment.length; i++) {
      date_index = dates.indexOf(transport_payment[i]['date']);
      mandi_index = mandis[date_index].map(function(e) {
        return e.mandi_name;
      }).indexOf(transport_payment[i]['mandi__mandi_name']);
      transport_cost[date_index][mandi_index] += transport_payment[i]['transportation_cost__sum'];
      farmer_share[date_index][mandi_index].farmer_share_amount = transport_payment[i]['farmer_share'];
      farmer_share[date_index][mandi_index].farmer_share_comment = transport_payment[i]['farmer_share_comment'];

      transporter_data_set[i][TRANSPORTER_DETAILS.DATE] = transport_payment[i]['date'];
      transporter_data_set[i][TRANSPORTER_DETAILS.MANDI_NAME] = transport_payment[i]['mandi__mandi_name'];
      transporter_data_set[i][TRANSPORTER_DETAILS.TRANSPORTER_NAME] = transport_payment[i]['transportation_vehicle__transporter__transporter_name'];
      transporter_data_set[i][TRANSPORTER_DETAILS.TRANSPORTER_PHONE] = transport_payment[i]['transportation_vehicle__transporter__transporter_phone'];
      transporter_data_set[i][TRANSPORTER_DETAILS.VEHICLE_TYPE] = transport_payment[i]['transportation_vehicle__vehicle__vehicle_name'];
      transporter_data_set[i][TRANSPORTER_DETAILS.VEHICLE_NUMBER] = transport_payment[i]['transportation_vehicle__vehicle_number'];
      transporter_data_set[i][TRANSPORTER_DETAILS.TRANSPORT_COST] = parseFloat(transport_payment[i]['transportation_cost__sum'].toFixed(2));
      transporter_data_set[i][TRANSPORTER_DETAILS.TRANSPORTER_COMMENT] = transport_payment[i]['transportation_cost_comment'];
      transporter_data_set[i][TRANSPORTER_DETAILS.MANDI_ID] = transport_payment[i]['mandi__id'];
      transporter_data_set[i][TRANSPORTER_DETAILS.TRANSPORTATION_VEHICLE_ID] = transport_payment[i]['transportation_vehicle__id'];
      transporter_data_set[i][TRANSPORTER_DETAILS.TIMESTAMP] = transport_payment[i]['timestamp'];
      transporter_data_set[i][TRANSPORTER_DETAILS.ROW_ID] = i;
    }
  },
  aggregator_data: function() {
    var sno = 0;
    for (var i = 0; i < dates.length; i++) {
      for (var j = 0; j < mandis[i].length; j++) {
        aggregator_data_set[sno][PAYMENT_SUMMARY.SNO] = (sno+1).toString();
        aggregator_data_set[sno][PAYMENT_SUMMARY.DATE] = dates[i];
        aggregator_data_set[sno][PAYMENT_SUMMARY.MANDI_NAME] = mandis[i][j].mandi_name;
        aggregator_data_set[sno][PAYMENT_SUMMARY.QUANTITY] = parseFloat(quantites[i][j].toFixed(2));
        aggregator_data_set[sno][PAYMENT_SUMMARY.TRANSPORT_COST] = transport_cost[i][j];
        aggregator_data_set[sno][PAYMENT_SUMMARY.FARMER_SHARE] = farmer_share[i][j].farmer_share_amount;
        aggregator_data_set[sno][PAYMENT_SUMMARY.GADDIDAR_SHARE] = gaddidar_amount[i][j];
        aggregator_data_set[sno][PAYMENT_SUMMARY.FARMER_COMMENT] = farmer_share[i][j].farmer_share_comment;
        aggregator_data_set[sno][PAYMENT_SUMMARY.AGG_ID] = agg_id;
        aggregator_data_set[sno][PAYMENT_SUMMARY.MANDI_ID] = mandis[i][j].mandi_id;
        
        sno += 1;
      }
    }
  },
  aggregator_incentive: function() {
    for (var i = 0; i < aggregator_incentive.length; i++) {
      for (var j = 0; j < aggregator_data_set.length; j++) {
        if (aggregator_data_set[j].indexOf(aggregator_incentive[i]['date']) != -1 && aggregator_data_set[j].indexOf(aggregator_incentive[i]['mandi__name']) != -1) {
          aggregator_data_set[j][PAYMENT_SUMMARY.AGGREGATOR_INCENTIVE] = parseFloat(aggregator_incentive[i]['amount']);
          aggregator_data_set[j][PAYMENT_SUMMARY.AGGREGATOR_COMMENT] = aggregator_incentive[i]['comment'];
          aggregator_data_set[j][PAYMENT_SUMMARY.NET_PAYMENT] = (parseFloat(aggregator_data_set[j][PAYMENT_SUMMARY.AGGREGATOR_INCENTIVE]) + parseFloat(aggregator_data_set[j][PAYMENT_SUMMARY.TRANSPORT_COST]) - parseFloat(aggregator_data_set[j][PAYMENT_SUMMARY.GADDIDAR_SHARE]) - parseFloat(aggregator_data_set[j][PAYMENT_SUMMARY.FARMER_SHARE])).toFixed(2);
          break;
        }
      }
    }
  },
  quantity_post_deduction: function() {
    for (var i = 0; i < aggregator_incentive.length; i++) {
      for (var j = 0; j < aggregator_data_set.length; j++) {
        if (aggregator_data_set[j].indexOf(aggregator_incentive[i]['date']) != -1 && aggregator_data_set[j].indexOf(aggregator_incentive[i]['mandi__name']) != -1) {
          aggregator_data_set[j][PAYMENT_SUMMARY.QUANTITY_POST_DEDUCTION] = parseFloat(aggregator_incentive[i]['quantity__sum']);
          break;
        }
      }
    }
  },
  farmer_share_in_aggregator_incentive_half: function() {
    for (var i = 0; i < aggregator_data_set.length; i++) {
      aggregator_data_set[i][PAYMENT_SUMMARY.FARMER_SHARE_IN_AGGREGATOR_INCENTIVE] = (aggregator_data_set[i][PAYMENT_SUMMARY.QUANTITY]/2);
    }
  },
  farmer_share_in_aggregator_incentive_one_fourth: function() {
    for (var i = 0; i < aggregator_data_set.length; i++) {
      aggregator_data_set[i][PAYMENT_SUMMARY.FARMER_SHARE_IN_AGGREGATOR_INCENTIVE] = (aggregator_data_set[i][PAYMENT_SUMMARY.QUANTITY]/4);
    }
  }
};

function initialize() {
  initialLoadComplete = false;
  language = ENGLISH_LANGUAGE;
  if(localStorage.getItem("language_id") != null)
  {
    language = localStorage.getItem("language_id")
  }
  if(localStorage.getItem("country_id") != null)
  {
    country_id = localStorage.getItem("country_id")
  }
  $("select").material_select();
  $(".button-collapse").sideNav({
    closeOnClick: true
  });
  $(".button-collapse1").sideNav();
  get_admin_assigned_loopuser_data();
  //get_filter_data(language, country_id);
  initialLoadComplete = true;
  set_filterlistener();
  hidePaymentDetails();
  hideLoader(); 
}

function showLoader() {
  $("#loader").show();
}

function hideLoader() {
  $("#loader").hide();
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

function prepare_data_set_for_excel_download(data_set_copy, data_set_name, data_set) {
  for (var i = 0; i < data_set.length; i++) {
    data_set_copy.push([]);
    for (var j = 0; j < payment_model[data_set_name].length; j++) {
      if ( payment_model[data_set_name][j]["visible"] == true) {
        data_set_copy[i].push(data_set[i][j]);
      }
    }
  }
  return data_set_copy;
}
//To check for any items data change (textview, drop downs, button click)
function set_filterlistener() {
  $("#download_payment_sheet").click(function() {
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

        aggregator_data_set_copy = [];
        gaddidar_data_set_copy = [];
        transporter_data_set_copy = [];

        aggregator_data_set_copy = prepare_data_set_for_excel_download(aggregator_data_set_copy, "aggregator_data_set", aggregator_data_set);
        gaddidar_data_set_copy = prepare_data_set_for_excel_download(gaddidar_data_set_copy, "gaddidar_data_set", gaddidar_data_set);
        transporter_data_set_copy = prepare_data_set_for_excel_download(transporter_data_set_copy, "transporter_data_set", transporter_data_set);
        
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
            data: transporter_data_set_copy
          }
        };

        var header_json = header_dict;

        var cell_format = {
          bold: 0,
          font_size: 9,
          num_format: '#,##0.00',
          text_wrap: true
        }

        var json_to_send = {
          header: header_json,
          data: data_json,
          cell_format: cell_format,
          sheet_header: 'Loop ' + selected_aggregator_state + ' (' + selected_aggregator_country + ')',
          sheet_footer: 'This is an automated generated sheet'

        }

        xhttp.send(JSON.stringify(json_to_send));
      }
    }
  });

  $("#aggregator_payments").change(function() {
    hidePaymentDetails();    
    selected_aggregator = $(this).children(":selected");
    var aggregator_index = aggregator_ids.indexOf(parseInt(selected_aggregator.val()));
    selected_aggregator_state = aggregator_states[aggregator_index];
    selected_aggregator_country = aggregators_countries[aggregator_index];

    $("select").material_select();
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
}

function hidePaymentDetails() {
  $("#aggregator_payment_tab").hide();
  $("#download_payment_sheet").hide();
  $('#aggregator_payment_details').hide();
}

//To make a call when filters are changed
function get_filter_data(language, country_id) {
  $.get("/loop/filter_data/", {
      language: language,
      'country_id': country_id,
      'state_id': state_id
    })
    .done(function(data) {
      var data_json = JSON.parse(data);
      aggregators_for_filter = data_json.aggregators;
      mandis_for_filter = data_json.mandis;
      gaddidars_for_filter = data_json.gaddidars;
      crops_for_filter = data_json.crops;
      croplanguage_for_filter = data_json.croplanguage;
      transporter_for_filter = data_json.transporters;
      aggregator_ids = []
      aggregator_names = []
      aggregator_states = []
      aggregators_countries = []
      $.each(aggregators_for_filter,function(index,aggregator_data){
        aggregator_ids.push(aggregator_data.user__id);
        aggregator_names.push(aggregator_data.name_en);
        aggregator_states.push(aggregator_data.village__block__district__state__state_name_en);
        aggregators_countries.push(aggregator_data.village__block__district__state__country__country_name);
      });
      if (language == ENGLISH_LANGUAGE) {
        fill_drop_down($('#aggregator_payments'), aggregators_for_filter, 'user__id', 'name_en', 'Aggregator', 'id');
      } else {
        fill_drop_down($('#aggregator_payments'), aggregators_for_filter, 'user__id', 'name', 'Aggregator', 'id');
      }
    });
}

function get_admin_assigned_loopuser_data() {
  $.get("/loop/admin_assigned_loopusers_data/", {
      user_id: window.localStorage.user_id
    })
    .done(function(data) {
      var data_json = JSON.parse(data);
      aggregators_for_admin = data_json.aggregators;
      aggregator_ids = []
      aggregator_names = []
      aggregator_states = []
      aggregators_countries = []
      $.each(aggregators_for_admin,function(index,aggregator_data){
        aggregator_ids.push(aggregator_data.user__id);
        aggregator_names.push(aggregator_data.name_en);
        aggregator_states.push(aggregator_data.village__block__district__state__state_name_en);
        aggregators_countries.push(aggregator_data.village__block__district__state__country__country_name);
      });
      if (language == ENGLISH_LANGUAGE) {
        fill_drop_down($('#aggregator_payments'), aggregators_for_admin, 'user__id', 'name_en', 'Aggregator', 'id');
      } else {
        fill_drop_down($('#aggregator_payments'), aggregators_for_admin, 'user__id', 'name', 'Aggregator', 'id');
      }
    });
}

// To fill aggregator drop down on Payment page
function fill_drop_down(container, data_json, id_parameter, name_parameter, caption, id) {
  var tbody_obj = container;
  tbody_obj.html("");
  tbody_obj.append('<option value="" disabled selected> Choose ' + caption + ' </option>');
  $.each(data_json, function(index, data) {
    var li_item = '<option value = ' + data[id_parameter] + ' id = ' + data[id] + '>' + data[name_parameter] + ' (' + data[id_parameter] + ')' +'</option>';
    tbody_obj.append(li_item);
  });
  $('select').material_select();
}

//To compute the payment model to be used for the aggregator
function get_payment_model() {
  var max_model_start_date = null;
  var model_ID = 0;

  for(var i=1; i < models.length; i++) {
    if(models[i]["geography"][selected_aggregator_country]) {
      if(models[i]["geography"][selected_aggregator_country].indexOf(selected_aggregator_state) != -1) {
        if(max_model_start_date == null || (new Date(payments_start_date) - new Date(models[i]["start_date"]) >= 0 && new Date(models[i]["start_date"]) - new Date(max_model_start_date) > 0)) {
          max_model_start_date = models[i]["start_date"];
          model_ID = i;
        }
      }
    }    
  }

  return models[model_ID];
}

function initialize_table_constants(table) {
  for(var key in table) {
    table[key] = null;
  }
}

function calculate_data_for_table(table_data) {
  for(var i=0; i < payment_model[table_data].length; i++) {
    if(payment_model[table_data][i]["dependency"]) {
      for(var j=0; j < payment_model[table_data][i]["dependency"].length; j++) {
        if(!executed_calc_functions.has(payment_model[table_data][i]["dependency"][j])) {
          calc_functions[payment_model[table_data][i]["dependency"][j]]();
          executed_calc_functions.add(payment_model[table_data][i]["dependency"][j]);
        }
      }
    }
    if(payment_model[table_data][i]["calc_function"] && !executed_calc_functions.has(payment_model[table_data][i]["calc_function"])) {
      calc_functions[payment_model[table_data][i]["calc_function"]]();
      executed_calc_functions.add(payment_model[table_data][i]["calc_function"]);
    }    
  }
}
//To compute aggregator, transporter, gaddidar payments table
function aggregator_payment_sheet(data_json, aggregator, agg_id, aggregator_name_input) {
  aggregator_payment = payments_data.aggregator_data;
  transport_payment = payments_data.transportation_data;
  gaddidar_contribution_data = payments_data.gaddidar_data;
  aggregator_incentive = payments_data.aggregator_incentive;

  //selected_aggregator_country = 'Bangladesh';

  payment_model = get_payment_model();

  var default_aggregator_data_set = [];
  var default_gaddidar_data_set = [];
  var default_transporter_data_set = [];

  var aggregator_data_table_columns = [];
  var gaddidar_data_table_columns = [];
  var transporter_data_table_columns = [];

  var aggregator_data_table_totals = [];
  var gaddidar_data_table_totals = [];
  var transporter_data_table_totals = [];  

  aggregator_data_set = [];
  gaddidar_data_set = [];
  transporter_data_set = [];

  initialize_table_constants(PAYMENT_SUMMARY);
  initialize_table_constants(COMMISSION_AGENT_DETAILS);
  initialize_table_constants(TRANSPORTER_DETAILS);

  for(var i=0; i < payment_model["aggregator_data_set"].length; i++) {
    default_aggregator_data_set.push(payment_model["aggregator_data_set"][i]["default_val"]);
    PAYMENT_SUMMARY[payment_model["aggregator_data_set"][i]["col_const"]] = i;
    aggregator_data_table_columns.push({
      title: payment_model["aggregator_data_set"][i]["title"],
      visible: payment_model["aggregator_data_set"][i]["visible"]
    });
    if(payment_model["aggregator_data_set"][i]["total"] == true) {
      aggregator_data_table_totals.push(i);
    }
  }
  PAYMENT_SUMMARY["NET_QUANTITY"] = PAYMENT_SUMMARY[payment_model["net_quantity_const"]];

  for(var i = 0; i < aggregator_incentive.length; i++) {
    aggregator_data_set.push(default_aggregator_data_set.slice());
  }

  for(var i=0; i < payment_model["gaddidar_data_set"].length; i++) {
    default_gaddidar_data_set.push(payment_model["gaddidar_data_set"][i]["default_val"]);
    COMMISSION_AGENT_DETAILS[payment_model["gaddidar_data_set"][i]["col_const"]] = i;
    gaddidar_data_table_columns.push({
      title: payment_model["gaddidar_data_set"][i]["title"],
      visible: payment_model["gaddidar_data_set"][i]["visible"]
    });
    if(payment_model["gaddidar_data_set"][i]["total"] == true) {
      gaddidar_data_table_totals.push(i);
    }
  }

  for(var i = 0; i < aggregator_payment.length; i++) {
    gaddidar_data_set.push(default_gaddidar_data_set.slice());
  }

  for(var i=0; i < payment_model["transporter_data_set"].length; i++) {
    default_transporter_data_set.push(payment_model["transporter_data_set"][i]["default_val"]);
    TRANSPORTER_DETAILS[payment_model["transporter_data_set"][i]["col_const"]] = i;
    transporter_data_table_columns.push({
      title: payment_model["transporter_data_set"][i]["title"],
      visible: payment_model["transporter_data_set"][i]["visible"]
    });
    if(payment_model["transporter_data_set"][i]["total"] == true) {
      transporter_data_table_totals.push(i);
    }
  }

  for(var i = 0; i < transport_payment.length; i++) {
    transporter_data_set.push(default_transporter_data_set.slice());
  }

  executed_calc_functions.clear();
  dates = [];
  mandis = [];
  quantites = [];
  gaddidar_amount = [];
  transport_cost = [];
  farmer_share = [];

  calculate_data_for_table("aggregator_data_set");
  calculate_data_for_table("gaddidar_data_set");
  calculate_data_for_table("transporter_data_set"); 

  //Adding mobile recharge entry for aggregator in Payment Sheet
  aggregator_data_set.push(default_aggregator_data_set.slice());
  var aggregator_data_set_length = aggregator_data_set.length;
  aggregator_data_set[aggregator_data_set_length-1][PAYMENT_SUMMARY.SNO] = aggregator_data_set_length.toString();
  aggregator_data_set[aggregator_data_set_length-1][PAYMENT_SUMMARY.MANDI_NAME] = "Mobile Recharge";
  aggregator_data_set[aggregator_data_set_length-1][PAYMENT_SUMMARY.AGGREGATOR_INCENTIVE] = parseFloat("150").toFixed(2);
  aggregator_data_set[aggregator_data_set_length-1][PAYMENT_SUMMARY.NET_PAYMENT] = parseFloat("150").toFixed(2);

  
  //gaddidar data clone
  var gaddidar_data_set_clone = [];
  for (var i = 0; i < gaddidar_data_set.length; i++) {
    gaddidar_data_set_clone.push(gaddidar_data_set[i].slice());
    if (gaddidar_data_set[i][COMMISSION_AGENT_DETAILS.GADDIDAR_DISCOUNT_CRITERIA] == 1)
      gaddidar_data_set_clone[i][COMMISSION_AGENT_DETAILS.GADDIDAR_DISCOUNT] = parseFloat(gaddidar_data_set_clone[i][COMMISSION_AGENT_DETAILS.GADDIDAR_DISCOUNT]) * 100 + '%';
  }

  $(window).on('beforeunload', function() {
    if (superEditMode == 1)
      return "You have Unsaved Changes";
  });

  var $this;
  var flag_edit_Table2 = false;
  var rows_table2 = {};
  var rows_table2_farmer = {};
  var editedAggregator = 0;
  var editedFarmer = 0;

  function initializeAggregatorModal() {
    $('#aggregator_date_row').val($this.parent()[0].childNodes[PAYMENT_SUMMARY.DATE].innerHTML);
    $('#aggregator_mandi_row').val($this.parent()[0].childNodes[PAYMENT_SUMMARY.MANDI_NAME].innerHTML);
    $('#aggregator_volume_row').val($this.parent()[0].childNodes[PAYMENT_SUMMARY.NET_QUANTITY].innerHTML);
    $('#aggregator_commission_row').val(parseFloat($this.parent()[0].childNodes[PAYMENT_SUMMARY.AGGREGATOR_INCENTIVE].innerHTML / ($this.parent()[0].childNodes[PAYMENT_SUMMARY.NET_QUANTITY].innerHTML)).toFixed(2));
    $('#aggregator_share_row').val(parseFloat($this.parent()[0].childNodes[PAYMENT_SUMMARY.AGGREGATOR_INCENTIVE].innerHTML).toFixed(2));
    $('#aggregator_comment_row').val($this.parent()[0].childNodes[PAYMENT_SUMMARY.AGGREGATOR_COMMENT].innerHTML);
    $('#aggregator_error_div').hide();
  }

  function initializeFarmerModal() {
    $('#farmer_date_row').val($this.parent()[0].childNodes[PAYMENT_SUMMARY.DATE].innerHTML);
    $('#farmer_mandi_row').val($this.parent()[0].childNodes[PAYMENT_SUMMARY.MANDI_NAME].innerHTML);
    $('#farmer_volume_row').val($this.parent()[0].childNodes[PAYMENT_SUMMARY.QUANTITY].innerHTML);
    $('#farmer_transport_cost_row').val($this.parent()[0].childNodes[PAYMENT_SUMMARY.TRANSPORT_COST].innerHTML);
    $('#farmer_gaddidar_commission_row_farmer').val($this.parent()[0].childNodes[PAYMENT_SUMMARY.GADDIDAR_SHARE].innerHTML);
    $('#farmer_commission_row').val(parseFloat($this.parent()[0].childNodes[PAYMENT_SUMMARY.FARMER_SHARE].innerHTML / ($this.parent()[0].childNodes[PAYMENT_SUMMARY.QUANTITY].innerHTML)).toFixed(2));
    $('#farmer_share_row').val(parseFloat($this.parent()[0].childNodes[PAYMENT_SUMMARY.FARMER_SHARE].innerHTML).toFixed(2));
    $('#farmer_comment_row').val($this.parent()[0].childNodes[PAYMENT_SUMMARY.FARMER_COMMENT].innerHTML);
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
    if ($this.context.cellIndex === PAYMENT_SUMMARY.AGGREGATOR_INCENTIVE && flag_edit_Table2 == true) {
      initializeAggregatorModal();
      $('#aggregator_modal').openModal();
      $('#aggregator_commission_row').focus();
    } else if ($this.context.cellIndex === PAYMENT_SUMMARY.FARMER_SHARE && flag_edit_Table2 == true) {
      initializeFarmerModal();
      $('#farmer_modal').openModal();
      $('#farmer_commission_row').focus();
    }

  });
  $('#aggregator_commission_row').on('change', function() {
    if (!inputValidation($('#aggregator_commission_row'))) {
      actionOnInvalidValidation($('#aggregator_commission_row'), $('#aggregator_error_div'), $('#aggregator_error_message'));
    } else {
      $('#aggregator_share_row').val(parseFloat(($this.parent()[0].childNodes[PAYMENT_SUMMARY.NET_QUANTITY].innerHTML) * $('#aggregator_commission_row').val()).toFixed(2));
      if ($('#aggregator_commission_row').val().trim() != '' && $('#aggregator_share_row').val().trim() != $this.parent()[0].childNodes[PAYMENT_SUMMARY.AGGREGATOR_INCENTIVE].innerHTML)
        editedAggregator = 1;
    }
  });
  $('#aggregator_share_row').on('change', function() {
    if (!inputValidation($('#aggregator_share_row'))) {
      actionOnInvalidValidation($('#aggregator_share_row'), $('#aggregator_error_div'), $('#aggregator_error_message'))
    } else {
      $('#aggregator_commission_row').val(parseFloat($('#aggregator_share_row').val() / ($this.parent()[0].childNodes[PAYMENT_SUMMARY.NET_QUANTITY].innerHTML)).toFixed(2));
      if ($('#aggregator_share_row').val().trim() != '' && $('#aggregator_share_row').val().trim() != $this.parent()[0].childNodes[PAYMENT_SUMMARY.AGGREGATOR_INCENTIVE].innerHTML)
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
      $('#farmer_share_row').val(parseFloat(($this.parent()[0].childNodes[PAYMENT_SUMMARY.QUANTITY].innerHTML) * $('#farmer_commission_row').val()).toFixed(2));
      if ($('#farmer_commission_row').val().trim() != '' && $('#farmer_share_row').val().trim() != $this.parent()[0].childNodes[PAYMENT_SUMMARY.FARMER_SHARE].innerHTML)
        editedFarmer = 1;

    }
  });
  $('#farmer_share_row').on('change', function() {
    if (!inputValidation($('#farmer_share_row'))) {
      actionOnInvalidValidation($('#farmer_share_row'), $('#farmer_error_div'), $('#farmer_error_message'));
    } else {
      $('#farmer_commission_row').val(parseFloat($('#farmer_share_row').val() / ($this.parent()[0].childNodes[PAYMENT_SUMMARY.QUANTITY].innerHTML)).toFixed(2));
      if ($('#farmer_share_row').val().trim() != '' && $('#farmer_share_row').val().trim() != $this.parent()[0].childNodes[PAYMENT_SUMMARY.FARMER_SHARE].innerHTML)
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

    $('#farmer_share_row').val($('#table2').DataTable().cell($this.context.parentNode.rowIndex - 1, PAYMENT_SUMMARY.FARMER_SHARE).data());
    $('#farmer_commission_row').val(parseFloat($('#table2').DataTable().cell($this.context.parentNode.rowIndex - 1, PAYMENT_SUMMARY.FARMER_SHARE).data() / $this.parent()[0].childNodes[PAYMENT_SUMMARY.QUANTITY].innerHTML).toFixed(2));
    $('#farmer_comment_row').val($('#table2').DataTable().cell($this.context.parentNode.rowIndex - 1, PAYMENT_SUMMARY.FARMER_COMMENT).data());

  });
  $('#farmer_submit_modal').on('click', function(ev) {
    if (!inputValidation($('#farmer_commission_row'))) {
      ev.preventDefault();
      $('#farmer_commission_row').val($this.parent()[0].childNodes[PAYMENT_SUMMARY.FARMER_SHARE].textContent / $this.parent()[0].childNodes[PAYMENT_SUMMARY.QUANTITY].innerHTML);
      $('#farmer_share_row').val($this.parent()[0].childNodes[PAYMENT_SUMMARY.FARMER_SHARE].textContent);
      $('#farmer_commission_row').focus();
      return false;
    } else if (!inputValidation($('#farmer_share_row'))) {
      ev.preventDefault();
      $('#farmer_commission_row').val($this.parent()[0].childNodes[PAYMENT_SUMMARY.FARMER_SHARE].textContent / $this.parent()[0].childNodes[PAYMENT_SUMMARY.QUANTITY].innerHTML);
      $('#farmer_share_row').val($this.parent()[0].childNodes[PAYMENT_SUMMARY.FARMER_SHARE].textContent);
      $('#farmer_share_row').focus();
      return false;
    } else if (farmerResetClick && editedFarmer == 0) {
      $this.parent()[0].childNodes[PAYMENT_SUMMARY.FARMER_SHARE].innerHTML = $('#table2').DataTable().cell($this.context.parentNode.rowIndex - 1, PAYMENT_SUMMARY.FARMER_SHARE).data();
      $this.parent()[0].childNodes[PAYMENT_SUMMARY.FARMER_COMMENT].innerHTML = $('#table2').DataTable().cell($this.context.parentNode.rowIndex - 1, PAYMENT_SUMMARY.FARMER_COMMENT).data();
      delete rows_table2_farmer[$this.context.parentNode.rowIndex];
      $this.removeAttr('class');
      $this.closest('tr').children('td:nth-child('+(PAYMENT_SUMMARY.FARMER_COMMENT+1)+')')[0].className = '';
      $this.addClass('editcolumn');
      farmerResetClick = false;
    } else if (editedFarmer != 0) {

      $this.parent()[0].childNodes[PAYMENT_SUMMARY.FARMER_SHARE].innerHTML = $('#farmer_share_row').val();
      $this.parent()[0].childNodes[PAYMENT_SUMMARY.FARMER_COMMENT].innerHTML = $('#farmer_comment_row').val() + ' - ' + window.localStorage.name;
      $this.parent()[0].childNodes[PAYMENT_SUMMARY.NET_PAYMENT].innerHTML = parseFloat(parseFloat($this.parent()[0].childNodes[PAYMENT_SUMMARY.TRANSPORT_COST].innerHTML) + parseFloat($this.parent()[0].childNodes[PAYMENT_SUMMARY.AGGREGATOR_INCENTIVE].innerHTML) - parseFloat($this.parent()[0].childNodes[PAYMENT_SUMMARY.GADDIDAR_SHARE].innerHTML) - parseFloat($this.parent()[0].childNodes[PAYMENT_SUMMARY.FARMER_SHARE].innerHTML)).toFixed(2);
      if ((parseFloat($this.parent()[0].childNodes[PAYMENT_SUMMARY.AGGREGATOR_INCENTIVE].innerHTML) + parseFloat($this.parent()[0].childNodes[PAYMENT_SUMMARY.TRANSPORT_COST].innerHTML)) < parseFloat($this.parent()[0].childNodes[PAYMENT_SUMMARY.FARMER_SHARE].innerHTML)) {

        //  $this.parent().css('background-color', '#E5FEB5').css('font-weight', 'bold').css('color', '#009');
        $this.removeAttr('class');
        $this.addClass('editedcelledge');
        $this.closest('tr').children('td:nth-child('+(PAYMENT_SUMMARY.FARMER_COMMENT+1)+')')[0].className = 'editedcelledge';

      } else {
        $this.removeAttr('class');
        $this.addClass('editedcell');
        $this.closest('tr').children('td:nth-child('+(PAYMENT_SUMMARY.FARMER_COMMENT+1)+')')[0].className = 'editedcell';
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
    $('#aggregator_share_row').val($('#table2').DataTable().cell($this.context.parentNode.rowIndex - 1, PAYMENT_SUMMARY.AGGREGATOR_INCENTIVE).data());
    $('#aggregator_commission_row').val(parseFloat($('#table2').DataTable().cell($this.context.parentNode.rowIndex - 1, PAYMENT_SUMMARY.AGGREGATOR_INCENTIVE).data() / $this.parent()[0].childNodes[PAYMENT_SUMMARY.NET_QUANTITY].innerHTML).toFixed(2))
    $('#aggregator_comment_row').val($('#table2').DataTable().cell($this.context.parentNode.rowIndex - 1, PAYMENT_SUMMARY.AGGREGATOR_COMMENT).data());
  });
  $('#aggregator_submit_modal').on('click', function(ev) {
    if (!inputValidation($('#aggregator_commission_row'))) {
      ev.preventDefault();
      $('#aggregator_commission_row').val($this.parent()[0].childNodes[PAYMENT_SUMMARY.AGGREGATOR_INCENTIVE].textContent / $this.parent()[0].childNodes[PAYMENT_SUMMARY.NET_QUANTITY].innerHTML);
      $('#aggregator_share_row').val($this.parent()[0].childNodes[PAYMENT_SUMMARY.AGGREGATOR_INCENTIVE].textContent);
      $('#aggregator_commission_row').focus();
      return false;
    } else if (!inputValidation($('#aggregator_share_row'))) {
      ev.preventDefault();
      $('#aggregagtor_commission_row').val($this.parent()[0].childNodes[PAYMENT_SUMMARY.AGGREGATOR_INCENTIVE].textContent / $this.parent()[0].childNodes[PAYMENT_SUMMARY.NET_QUANTITY].innerHTML);
      $('#aggregagtor_share_row').val($this.parent()[0].childNodes[PAYMENT_SUMMARY.AGGREGATOR_INCENTIVE].textContent);
      $('#aggregator_commission_row').focus();
      return false;
    } else if (aggregatorResetClick && editedAggregator == 0) {
      $this.parent()[0].childNodes[PAYMENT_SUMMARY.AGGREGATOR_INCENTIVE].innerHTML = $('#table2').DataTable().cell($this.context.parentNode.rowIndex - 1, PAYMENT_SUMMARY.AGGREGATOR_INCENTIVE).data();
      $this.parent()[0].childNodes[PAYMENT_SUMMARY.AGGREGATOR_COMMENT].innerHTML = $('#table2').DataTable().cell($this.context.parentNode.rowIndex - 1, PAYMENT_SUMMARY.AGGREGATOR_COMMENT).data();
      delete rows_table2[$this.context.parentNode.rowIndex];
      $this.removeAttr('class');
      $this.closest('tr').children('td:nth-child('+(PAYMENT_SUMMARY.AGGREGATOR_COMMENT+1)+')')[0].className = '';
      $this.addClass('editcolumn');
      aggregatorResetClick = false;
    } else if (editedAggregator != 0) {
      $('#aggregator_modal').closeModal();
      $this.parent()[0].childNodes[PAYMENT_SUMMARY.AGGREGATOR_INCENTIVE].innerHTML = $('#aggregator_share_row').val();
      $this.parent()[0].childNodes[PAYMENT_SUMMARY.AGGREGATOR_COMMENT].innerHTML = $('#aggregator_comment_row').val() + ' - ' + window.localStorage.name;
      $this.parent()[0].childNodes[PAYMENT_SUMMARY.NET_PAYMENT].innerHTML = parseFloat(parseFloat($this.parent()[0].childNodes[PAYMENT_SUMMARY.TRANSPORT_COST].innerHTML) + parseFloat($this.parent()[0].childNodes[PAYMENT_SUMMARY.AGGREGATOR_INCENTIVE].innerHTML) - parseFloat($this.parent()[0].childNodes[PAYMENT_SUMMARY.GADDIDAR_SHARE].innerHTML) - parseFloat($this.parent()[0].childNodes[PAYMENT_SUMMARY.FARMER_SHARE].innerHTML)).toFixed(2)
      if (parseFloat($this.parent()[0].childNodes[PAYMENT_SUMMARY.AGGREGATOR_INCENTIVE].innerHTML / $this.parent()[0].childNodes[PAYMENT_SUMMARY.NET_QUANTITY].innerHTML) > 0.5) {
        $this.removeAttr('class');
        $this.addClass('editedcelledge');
        $this.closest('tr').children('td:nth-child('+(PAYMENT_SUMMARY.AGGREGATOR_COMMENT+1)+')')[0].className = 'editedcelledge';
      } else {
        $this.removeAttr('class');
        $this.addClass('editedcell');
        $this.closest('tr').children('td:nth-child('+(PAYMENT_SUMMARY.AGGREGATOR_COMMENT+1)+')')[0].className = 'editedcell';
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
      row_data['date'] = $('#table2').DataTable().cell(keys - 1, PAYMENT_SUMMARY.DATE).data();
      row_data['amount'] = $('#table2 tr').eq(parseInt(keys) + 1)[0].childNodes[PAYMENT_SUMMARY.AGGREGATOR_INCENTIVE].innerHTML;
      mandi_idDict['online_id'] = $('#table2').DataTable().cell(keys - 1, PAYMENT_SUMMARY.MANDI_ID).data();
      row_data['mandi'] = mandi_idDict;
      aggregator_idDict['online_id'] = $('#table2').DataTable().cell(keys - 1, PAYMENT_SUMMARY.AGG_ID).data();
      row_data['aggregator'] = aggregator_idDict;
      row_data['comment'] = $('#table2 tr').eq(parseInt(keys) + 1)[0].childNodes[PAYMENT_SUMMARY.AGGREGATOR_COMMENT].innerHTML;
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
      row_data['date'] = $('#table2').DataTable().cell(keys - 1, PAYMENT_SUMMARY.DATE).data();
      row_data['amount'] = $('#table2 tr').eq(parseInt(keys) + 1)[0].childNodes[PAYMENT_SUMMARY.FARMER_SHARE].innerHTML;
      mandi_idDict['online_id'] = $('#table2').DataTable().cell(keys - 1, PAYMENT_SUMMARY.MANDI_ID).data();
      row_data['mandi'] = mandi_idDict;
      row_data['comment'] = $('#table2 tr').eq(parseInt(keys) + 1)[0].childNodes[PAYMENT_SUMMARY.FARMER_COMMENT].innerHTML;
      aggregator_idDict['online_id'] = $('#table2').DataTable().cell(keys - 1, PAYMENT_SUMMARY.AGG_ID).data();
      row_data['aggregator'] = aggregator_idDict;
      row_data['user_created_id'] = $('#aggregator_payments :selected').val();
      row_data['user_modified_id'] = window.localStorage.user_id;
      editedDataFarmer.push(row_data);
    }
    return editedDataFarmer;
  }
  var paymentTableDom = '<"clear">rtip'
  if (new Date() - new Date(payments_to_date) <= TIME_DIFF_THIRTY_DAYS){
    paymentTableDom = 'T<"clear">rtip'
  }

  if (aggregator_table_created) {
    aggregator_table.clear().destroy();
  } else {
    aggregator_table_created = true;
  }

  $('#payment_sheet').html("");
  $('<th>Total:</th>').appendTo('#payment_sheet');
  for (var i = 1; i < aggregator_data_table_columns.length; i++) {
    $('<th></th>').appendTo('#payment_sheet');
  }

  aggregator_table = $('#table2').DataTable({
    destroy: true,
    data: aggregator_data_set,
    columns: aggregator_data_table_columns,
    "dom": paymentTableDom,
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
          $('#table2').find('td:nth-child('+(PAYMENT_SUMMARY.AGGREGATOR_INCENTIVE+1)+')').addClass('editcolumn');
          $('#table2').find('td:nth-child('+(PAYMENT_SUMMARY.FARMER_SHARE+1)+')').addClass('editcolumn');
          $('#ToolTables_table2_0').addClass('disable-button');
          $('#payments_from_date').parent().parent().addClass('disable-button');
          $('#payments_to_date').parent().parent().addClass('disable-button');
          $('#aggregator_payments').parent().parent().addClass('disable-button');
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

                  aggregator_data_set[keys - 1][PAYMENT_SUMMARY.AGGREGATOR_INCENTIVE] = parseFloat($('#table2 tr').eq(parseInt(keys) + 1)[0].childNodes[PAYMENT_SUMMARY.AGGREGATOR_COMMENT].innerHTML);
                  aggregator_data_set[keys - 1][PAYMENT_SUMMARY.AGGREGATOR_COMMENT] = $('#table2 tr').eq(parseInt(keys) + 1)[0].childNodes[PAYMENT_SUMMARY.AGGREGATOR_COMMENT].innerHTML;
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
                  aggregator_data_set[keys - 1][PAYMENT_SUMMARY.FARMER_SHARE] = parseFloat($('#table2 tr').eq(parseInt(keys) + 1)[0].childNodes[PAYMENT_SUMMARY.FARMER_SHARE].innerHTML);
                  aggregator_data_set[keys - 1][PAYMENT_SUMMARY.FARMER_COMMENT] = $('#table2 tr').eq(parseInt(keys) + 1)[0].childNodes[PAYMENT_SUMMARY.FARMER_COMMENT].innerHTML;
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
              $('#payments_from_date').parent().parent().removeClass('disable-button');
              $('#payments_to_date').parent().parent().removeClass('disable-button');
              $('#aggregator_payments').parent().parent().removeClass('disable-button');
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
      for (var i = 1; i < aggregator_data_table_columns.length; i++) {
        if(aggregator_data_table_totals.indexOf(i) != -1) {
          total = api.column(i).data().reduce(function(a, b) {
            if (a === "") {
              a = 0;
            }
            if (b === "") {
              b = 0;
            }
            return parseFloat(a) + parseFloat(b);
          }, 0);
          
          $(api.column(i).footer()).html(finalFormat(total + ""));
        } else {
          $(api.column(i).footer()).html("");
        }
      }
    }
  });

  var gaddidarResetClicked = false;
  function initializeGaddidarModal() {
    $('#gaddidar_date_row').val($this.parent()[0].childNodes[COMMISSION_AGENT_DETAILS.DATE].innerHTML);
    $('#gaddidar_mandi_row').val($this.parent()[0].childNodes[COMMISSION_AGENT_DETAILS.MANDI_NAME].innerHTML);
    $('#gaddidar_row').val($this.parent()[0].childNodes[COMMISSION_AGENT_DETAILS.GADDIDAR_NAME].innerHTML);
    $('#gaddidar_quantity_row').val($this.parent()[0].childNodes[COMMISSION_AGENT_DETAILS.QUANTITY].innerHTML);
    $('#gaddidar_share_row').val(parseFloat($this.parent()[0].childNodes[COMMISSION_AGENT_DETAILS.GADDIDAR_COMMISSION].textContent).toFixed(2));
    $('#gaddidar_amount_row').val(parseFloat($('#table3').DataTable().cell($this.context.parentNode.rowIndex - 1, COMMISSION_AGENT_DETAILS.AMOUNT).data()));
    $('#gaddidar_comment_row').val($this.parent()[0].childNodes[COMMISSION_AGENT_DETAILS.GADDIDAR_COMMENT].textContent);
    if ($('#table3').DataTable().cell($this.context.parentNode.rowIndex - 1, COMMISSION_AGENT_DETAILS.GADDIDAR_DISCOUNT_CRITERIA).data() == 1) {
      $('#gaddidar_commission_row').val(parseFloat($this.parent()[0].childNodes[COMMISSION_AGENT_DETAILS.GADDIDAR_DISCOUNT].innerHTML.split('%')[0]).toFixed(2));
      $('#gaddidar_commission_label')[0].innerHTML = 'Commission Agent Discount[CAD] (%)';
    } else {
      $('#gaddidar_commission_label')[0].innerHTML = 'Commission Agent Discount[CAD] (in Rs/Kg)';
      $('#gaddidar_commission_row').val(parseFloat($this.parent()[0].childNodes[COMMISSION_AGENT_DETAILS.GADDIDAR_DISCOUNT].innerHTML).toFixed(2));
    }
    $('#gaddidar_error_div').hide();
  }
  var flag_edit_Table3 = false;
  var rows_table3 = {};
  var editedGaddidar = 0;
  $('#table3').on('click', 'tbody td', function(e) {
    $this = $(this);
    if (flag_edit_Table3 == true && ($this.context.cellIndex === COMMISSION_AGENT_DETAILS.GADDIDAR_DISCOUNT || $this.context.cellIndex === COMMISSION_AGENT_DETAILS.GADDIDAR_COMMISSION)) {
      initializeGaddidarModal();
      $('#gaddidar_modal').openModal();
      if ($this.context.cellIndex === COMMISSION_AGENT_DETAILS.GADDIDAR_DISCOUNT) {
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
      if ($('#table3').DataTable().cell($this.context.parentNode.rowIndex - 1, COMMISSION_AGENT_DETAILS.GADDIDAR_DISCOUNT_CRITERIA).data() == 0) {
        $('#gaddidar_share_row').val(parseFloat($this.parent()[0].childNodes[COMMISSION_AGENT_DETAILS.QUANTITY].innerHTML * $('#gaddidar_commission_row').val()).toFixed(2));
      } else {
        $('#gaddidar_share_row').val(parseFloat($('#table3').DataTable().cell($this.context.parentNode.rowIndex - 1, COMMISSION_AGENT_DETAILS.AMOUNT).data() * ($('#gaddidar_commission_row').val() / 100)).toFixed(2));
      }

      if ($('#gaddidar_commission_row').val().trim() != '' && $('#gaddidar_commission_row').val().trim() != $this.parent()[0].childNodes[COMMISSION_AGENT_DETAILS.QUANTITY].innerHTML)
        editedGaddidar = 1;
    }
  });

  $('#gaddidar_share_row').on('change', function() {
    if (!inputValidation($('#gaddidar_share_row'))) {
      actionOnInvalidValidation($('#gaddidar_share_row'), $('#gaddidar_error_div'), $('#gaddidar_error_message'));
    } else {
      if ($('#table3').DataTable().cell($this.context.parentNode.rowIndex - 1, COMMISSION_AGENT_DETAILS.GADDIDAR_DISCOUNT_CRITERIA).data() == 0) {
        $('#gaddidar_commission_row').val(parseFloat($('#gaddidar_share_row').val() / $this.parent()[0].childNodes[COMMISSION_AGENT_DETAILS.QUANTITY].innerHTML).toFixed(2));
      } else {
        $('#gaddidar_commission_row').val((parseFloat($('#gaddidar_share_row').val() / $('#table3').DataTable().cell($this.context.parentNode.rowIndex - 1, COMMISSION_AGENT_DETAILS.AMOUNT).data()).toFixed(2)) * 100);
      }
      if ($('#gaddidar_commission_row').val().trim() != '' && $('#gaddidar_commission_row').val().trim() != $this.parent()[0].childNodes[COMMISSION_AGENT_DETAILS.GADDIDAR_DISCOUNT].innerHTML)
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
    $('#gaddidar_share_row').val($('#table3').DataTable().cell($this.context.parentNode.rowIndex - 1, COMMISSION_AGENT_DETAILS.GADDIDAR_COMMISSION).data());
    if ($('#table3').DataTable().cell($this.context.parentNode.rowIndex - 1, COMMISSION_AGENT_DETAILS.GADDIDAR_DISCOUNT_CRITERIA).data() == 1)
      $('#gaddidar_commission_row').val(parseFloat($('#table3').DataTable().cell($this.context.parentNode.rowIndex - 1, COMMISSION_AGENT_DETAILS.GADDIDAR_DISCOUNT).data().split('%')[0]).toFixed(2));
    else
      $('#gaddidar_commission_row').val($('#table3').DataTable().cell($this.context.parentNode.rowIndex - 1, COMMISSION_AGENT_DETAILS.GADDIDAR_DISCOUNT).data());
    $('#gaddidar_comment_row').val($('#table3').DataTable().cell($this.context.parentNode.rowIndex - 1, COMMISSION_AGENT_DETAILS.GADDIDAR_COMMENT).data());
  });
  $('#gaddidar_submit_modal').on('click', function(ev) {
    if (!inputValidation($('#gaddidar_commission_row'))) {
      ev.preventDefault();
      $('#gaddidar_commission_row').val($this.parent()[0].childNodes[COMMISSION_AGENT_DETAILS.GADDIDAR_DISCOUNT].innerHTML);
      $('#gaddidar_share_row').val($this.parent()[0].childNodes[COMMISSION_AGENT_DETAILS.GADDIDAR_COMMISSION].textContent);
      $('#gaddidar_commission_row').focus();
      return false;

    } else if (!inputValidation($('#gaddidar_share_row'))) {
      ev.preventDefault();
      $('#gaddidar_commission_row').val($this.parent()[0].childNodes[COMMISSION_AGENT_DETAILS.GADDIDAR_DISCOUNT].innerHTML);
      $('#gaddidar_share_row').val($this.parent()[0].childNodes[COMMISSION_AGENT_DETAILS.GADDIDAR_COMMISSION].textContent);
      $('#gaddidar_share_row').focus();
      return false;

    } else if (gaddidarResetClicked && editedGaddidar == 0) {
      $this.parent()[0].childNodes[COMMISSION_AGENT_DETAILS.GADDIDAR_DISCOUNT].innerHTML = $('#table3').DataTable().cell($this.context.parentNode.rowIndex - 1, COMMISSION_AGENT_DETAILS.GADDIDAR_DISCOUNT).data();
      $this.parent()[0].childNodes[COMMISSION_AGENT_DETAILS.GADDIDAR_COMMISSION].innerHTML = $('#table3').DataTable().cell($this.context.parentNode.rowIndex - 1, COMMISSION_AGENT_DETAILS.GADDIDAR_COMMISSION).data();
      $this.parent()[0].childNodes[COMMISSION_AGENT_DETAILS.GADDIDAR_COMMENT].innerHTML = $('#table3').DataTable().cell($this.context.parentNode.rowIndex - 1, COMMISSION_AGENT_DETAILS.GADDIDAR_COMMENT).data();
      delete rows_table3[$this.context.parentNode.rowIndex];
      $this.removeAttr('class');
      $this.closest('tr').children('td:nth-child('+(COMMISSION_AGENT_DETAILS.GADDIDAR_DISCOUNT+1)+')')[0].className = 'editcolumn';
      $this.closest('tr').children('td:nth-child('+(COMMISSION_AGENT_DETAILS.GADDIDAR_COMMISSION+1)+')')[0].className = 'editcolumn';
      $this.closest('tr').children('td:nth-child('+(COMMISSION_AGENT_DETAILS.GADDIDAR_COMMENT+1)+')')[0].className = '';
      $this.addClass('editcolumn');
      gaddidarResetClicked = false;
    } else if (editedGaddidar != 0) {
      $('#gaddidar_modal').closeModal();
      if ($('#table3').DataTable().cell($this.context.parentNode.rowIndex - 1, COMMISSION_AGENT_DETAILS.GADDIDAR_DISCOUNT_CRITERIA).data() == 1)
        $this.parent()[0].childNodes[COMMISSION_AGENT_DETAILS.GADDIDAR_DISCOUNT].innerHTML = $('#gaddidar_commission_row').val() + '%';
      else
        $this.parent()[0].childNodes[COMMISSION_AGENT_DETAILS.GADDIDAR_DISCOUNT].innerHTML = $('#gaddidar_commission_row').val();
      $this.parent()[0].childNodes[COMMISSION_AGENT_DETAILS.GADDIDAR_COMMISSION].innerHTML = $('#gaddidar_share_row').val();
      $this.parent()[0].childNodes[COMMISSION_AGENT_DETAILS.GADDIDAR_COMMENT].innerHTML = $('#gaddidar_comment_row').val() + ' - ' + window.localStorage.name;
      if ($('#table3').DataTable().cell($this.context.parentNode.rowIndex - 1, COMMISSION_AGENT_DETAILS.GADDIDAR_DISCOUNT_CRITERIA).data() == 1) {
        if (parseFloat($this.parent()[0].childNodes[COMMISSION_AGENT_DETAILS.GADDIDAR_DISCOUNT].innerHTML) / 100 > 0.1) {
          $this.closest('tr').children('td:nth-child('+(COMMISSION_AGENT_DETAILS.GADDIDAR_DISCOUNT+1)+')')[0].className = 'editedcelledge';
          $this.closest('tr').children('td:nth-child('+(COMMISSION_AGENT_DETAILS.GADDIDAR_COMMISSION+1)+')')[0].className = 'editedcelledge';
          $this.closest('tr').children('td:nth-child('+(COMMISSION_AGENT_DETAILS.GADDIDAR_COMMENT+1)+')')[0].className = 'editedcelledge';
        } else {
          $this.closest('tr').children('td:nth-child('+(COMMISSION_AGENT_DETAILS.GADDIDAR_DISCOUNT+1)+')')[0].className = 'editedcell';
          $this.closest('tr').children('td:nth-child('+(COMMISSION_AGENT_DETAILS.GADDIDAR_COMMISSION+1)+')')[0].className = 'editedcell';
          $this.closest('tr').children('td:nth-child('+(COMMISSION_AGENT_DETAILS.GADDIDAR_COMMENT+1)+')')[0].className = 'editedcell';
        }
      } else {
        if (parseFloat($this.parent()[0].childNodes[COMMISSION_AGENT_DETAILS.GADDIDAR_DISCOUNT].innerHTML) > 1) {
          $this.closest('tr').children('td:nth-child('+(COMMISSION_AGENT_DETAILS.GADDIDAR_DISCOUNT+1)+')')[0].className = 'editedcelledge';
          $this.closest('tr').children('td:nth-child('+(COMMISSION_AGENT_DETAILS.GADDIDAR_COMMISSION+1)+')')[0].className = 'editedcelledge';
          $this.closest('tr').children('td:nth-child('+(COMMISSION_AGENT_DETAILS.GADDIDAR_COMMENT+1)+')')[0].className = 'editedcelledge';
        } else {
          $this.closest('tr').children('td:nth-child('+(COMMISSION_AGENT_DETAILS.GADDIDAR_DISCOUNT+1)+')')[0].className = 'editedcell';
          $this.closest('tr').children('td:nth-child('+(COMMISSION_AGENT_DETAILS.GADDIDAR_COMMISSION+1)+')')[0].className = 'editedcell';
          $this.closest('tr').children('td:nth-child('+(COMMISSION_AGENT_DETAILS.GADDIDAR_COMMENT+1)+')')[0].className = 'editedcell';
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
      row_data['date'] = $('#table3').DataTable().cell(keys - 1, COMMISSION_AGENT_DETAILS.DATE).data();
      row_data['amount'] = $('#table3 tr').eq(parseInt(keys) + 1)[0].childNodes[COMMISSION_AGENT_DETAILS.GADDIDAR_COMMISSION].innerHTML;
      mandi_idDict['online_id'] = $('#table3').DataTable().cell(keys - 1, COMMISSION_AGENT_DETAILS.MANDI_ID).data();
      row_data['mandi'] = mandi_idDict
      gaddidar_idDict['online_id'] = $('#table3').DataTable().cell(keys - 1, COMMISSION_AGENT_DETAILS.GADDIDAR_ID).data();
      row_data['gaddidar'] = gaddidar_idDict
      aggregator_idDict['online_id'] = $('#table3').DataTable().cell(keys - 1, COMMISSION_AGENT_DETAILS.AGG_ID).data();
      row_data['aggregator'] = aggregator_idDict
      row_data['comment'] = $('#table3 tr').eq(parseInt(keys) + 1)[0].childNodes[COMMISSION_AGENT_DETAILS.GADDIDAR_COMMENT].innerHTML;
      editedData.push(row_data);
    }
    return editedData;
  }

  if (gaddidar_table_created) {
    gaddidar_table.clear().destroy();
  } else {
    gaddidar_table_created = true;
  }
  $('#commission_agent_details').html("");
  $('<th>Total:</th>').appendTo('#commission_agent_details');
  for (var i = 1; i < gaddidar_data_table_columns.length; i++) {
    $('<th></th>').appendTo('#commission_agent_details');
  }
  gaddidar_table = $('#table3').DataTable({
    destroy: true,
    data: gaddidar_data_set_clone,
    columns: gaddidar_data_table_columns,
    "dom": paymentTableDom,
    //"dom":'Bfrtip',

    "pageLength": 1000,

    "oTableTools": {
      "sSwfPath": "/media/social_website/scripts/libs/tabletools_media/swf/copy_csv_xls_pdf.swf",
      "aButtons": [{

        "sExtends": "text",
        "sButtonText": "Edit",
        "fnClick": function(nButton, oConfig) {
          superEditMode = 1;
          $("#summary_payments").parent().addClass('disabled');
          $("#transportation_payments").parent().addClass('disabled');
          $('#ToolTables_table3_1').removeClass('disable-button');
          $('#ToolTables_table3_0').addClass('disable-button');
          $('#payments_from_date').parent().parent().addClass('disable-button');
          $('#payments_to_date').parent().parent().addClass('disable-button');
          $('#aggregator_payments').parent().parent().addClass('disable-button');
          $('#payments_from_date').removeClass('black-text');
          $('#payments_to_date').removeClass('black-text');
          flag_edit_Table3 = true;
          $('#table3').find('td:nth-child('+(COMMISSION_AGENT_DETAILS.GADDIDAR_DISCOUNT+1)+')').addClass('editcolumn');
          $('#table3').find('td:nth-child('+(COMMISSION_AGENT_DETAILS.GADDIDAR_COMMISSION+1)+')').addClass('editcolumn');
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
                  if (($('#table3 tr').eq(parseInt(keys) + 1)[0].childNodes[COMMISSION_AGENT_DETAILS.GADDIDAR_DISCOUNT].innerHTML).indexOf('%') >= 0) {
                    gaddidar_data_set[keys - 1][COMMISSION_AGENT_DETAILS.GADDIDAR_DISCOUNT] = parseFloat(($('#table3 tr').eq(parseInt(keys) + 1)[0].childNodes[COMMISSION_AGENT_DETAILS.GADDIDAR_DISCOUNT].innerHTML).split('%')[0]) / 100;
                  } else {
                    gaddidar_data_set[keys - 1][COMMISSION_AGENT_DETAILS.GADDIDAR_DISCOUNT] = parseFloat($('#table3 tr').eq(parseInt(keys) + 1)[0].childNodes[COMMISSION_AGENT_DETAILS.GADDIDAR_DISCOUNT].innerHTML);
                  }
                  gaddidar_data_set[keys - 1][COMMISSION_AGENT_DETAILS.GADDIDAR_COMMISSION] = parseFloat($('#table3 tr').eq(parseInt(keys) + 1)[0].childNodes[COMMISSION_AGENT_DETAILS.GADDIDAR_COMMISSION].innerHTML);
                  gaddidar_data_set[keys - 1][COMMISSION_AGENT_DETAILS.GADDIDAR_COMMENT] = parseFloat($('#table3 tr').eq(parseInt(keys) + 1)[0].childNodes[COMMISSION_AGENT_DETAILS.GADDIDAR_COMMENT].innerHTML);
                  gaddidar_data_set_clone[keys - 1][COMMISSION_AGENT_DETAILS.GADDIDAR_DISCOUNT] = $('#table3 tr').eq(parseInt(keys) + 1)[0].childNodes[COMMISSION_AGENT_DETAILS.GADDIDAR_DISCOUNT].innerHTML;
                  gaddidar_data_set_clone[keys - 1][COMMISSION_AGENT_DETAILS.GADDIDAR_COMMISSION] = parseFloat($('#table3 tr').eq(parseInt(keys) + 1)[0].childNodes[COMMISSION_AGENT_DETAILS.GADDIDAR_COMMISSION].innerHTML);
                  gaddidar_data_set_clone[keys - 1][COMMISSION_AGENT_DETAILS.GADDIDAR_COMMENT] = parseFloat($('#table3 tr').eq(parseInt(keys) + 1)[0].childNodes[COMMISSION_AGENT_DETAILS.GADDIDAR_COMMENT].innerHTML);
                }
                rows_table3 = [];
                get_payments_data();
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
              $('#payments_from_date').parent().parent().removeClass('disable-button');
              $('#payments_to_date').parent().parent().removeClass('disable-button');
              $('#aggregator_payments').parent().parent().removeClass('disable-button');
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
      for (var i = 1; i < gaddidar_data_table_columns.length; i++) {
        if(gaddidar_data_table_totals.indexOf(i) != -1) {
          total = api.column(i).data().reduce(function(a, b) {
            if (a === "") {
              a = 0;
            }
            if (b === "") {
              b = 0;
            }
            return parseFloat(a) + parseFloat(b);
          }, 0);
          $(api.column(i).footer()).html(finalFormat(total + ""));
        } else {
          $(api.column(i).footer()).html("");
        }
      }
    }
  });
  var flag_edit_Table4 = false;
  var editedTransportation = 0;
  var rows_table4 = {};

  function initializeTransportModal() {
    $('#transportation_date_row').val($this.parent()[0].childNodes[TRANSPORTER_DETAILS.DATE].innerHTML);
    $('#transportation_mandi_row').val($this.parent()[0].childNodes[TRANSPORTER_DETAILS.MANDI_NAME].innerHTML);
    $('#transportation_transporter_row').val($this.parent()[0].childNodes[TRANSPORTER_DETAILS.TRANSPORTER_NAME].innerHTML);

    $('#transportation_vehicle_row').val($this.parent()[0].childNodes[TRANSPORTER_DETAILS.VEHICLE_TYPE].innerHTML);
    $('#transportation_number_row').val($this.parent()[0].childNodes[TRANSPORTER_DETAILS.VEHICLE_NUMBER].innerHTML);
    $('#transportation_cost_row').val(parseFloat($this.parent()[0].childNodes[TRANSPORTER_DETAILS.TRANSPORT_COST].textContent).toFixed(2));
    $('#transportation_comment_row').val($this.parent()[0].childNodes[TRANSPORTER_DETAILS.TRANSPORTER_COMMENT].textContent);
    $('#transportation_error_div').hide();
  };


  $('#table4').on('click', 'tbody td', function(e) {
    $this = $(this);
    if (flag_edit_Table4 == true && ($this.context.cellIndex === TRANSPORTER_DETAILS.TRANSPORT_COST)) {
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
    } else if ($('#transportation_cost_row').val().trim() != '' && $('#transportation_cost_row').val().trim() != $this.parent()[0].childNodes[TRANSPORTER_DETAILS.TRANSPORT_COST].innerHTML) {
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
    $('#transportation_cost_row').val($('#table4').DataTable().cell($this.context.parentNode.rowIndex - 1, TRANSPORTER_DETAILS.TRANSPORT_COST).data());
    $('#transportation_comment_row').val($('#table4').DataTable().cell($this.context.parentNode.rowIndex - 1, TRANSPORTER_DETAILS.TRANSPORTER_COMMENT).data());
  });
  $('#transportation_submit_modal').on('click', function(ev) {
    if (!inputValidation($('#transportation_cost_row'))) {
      ev.preventDefault();
      $('#transportation_cost_row').val($this.parent()[0].childNodes[TRANSPORTER_DETAILS.TRANSPORT_COST].textContent);
      $('#aggregator_commission_row').focus();
      return false;
    } else if (transportationResetClick) {
      $this.parent()[0].childNodes[TRANSPORTER_DETAILS.TRANSPORT_COST].innerHTML = parseFloat($('#table4').DataTable().cell($this.context.parentNode.rowIndex - 1, TRANSPORTER_DETAILS.TRANSPORT_COST).data()).toFixed(2);
      $this.closest('tr').children('td:nth-child('+(TRANSPORTER_DETAILS.TRANSPORTER_COMMENT+1)+')')[0].innerHTML = $('#table4').DataTable().cell($this.context.parentNode.rowIndex - 1, TRANSPORTER_DETAILS.TRANSPORTER_COMMENT).data();
      delete rows_table4[$this.context.parentNode.rowIndex];
      $this.removeAttr('class');
      $this.closest('tr').children('td:nth-child('+(TRANSPORTER_DETAILS.TRANSPORTER_COMMENT+1)+')')[0].className = '';
      $this.addClass('editcolumn');
      transportationResetClick = false;
    } else if (editedTransportation != 0) {
      $('#transportation_modal').closeModal();
      $this.parent()[0].childNodes[TRANSPORTER_DETAILS.TRANSPORT_COST].innerHTML = $('#transportation_cost_row').val();
      $this.parent()[0].childNodes[TRANSPORTER_DETAILS.TRANSPORTER_COMMENT].innerHTML = $('#transportation_comment_row').val() + ' - ' + window.localStorage.name;
      $this.removeAttr('class');
      $this.addClass('editedcell');
      $this.closest('tr').children('td:nth-child('+(TRANSPORTER_DETAILS.TRANSPORTER_COMMENT+1)+')')[0].className = 'editedcell';
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
      mandi_idDict['online_id'] = $('#table4').DataTable().cell(keys - 1, TRANSPORTER_DETAILS.MANDI_ID).data();
      row_data['mandi'] = mandi_idDict;
      transportationvehicle_idDict["online_id"] = $('#table4').DataTable().cell(keys - 1, TRANSPORTER_DETAILS.TRANSPORTATION_VEHICLE_ID).data();
      row_data['transportation_vehicle'] = transportationvehicle_idDict;
      row_data['date'] = $('#table4').DataTable().cell(keys - 1, TRANSPORTER_DETAILS.DATE).data();
      row_data['timestamp'] = $('#table4').DataTable().cell(keys - 1, TRANSPORTER_DETAILS.TIMESTAMP).data();
      row_data['transportation_cost'] = $('#table4 tr').eq(parseInt(keys) + 1)[0].childNodes[TRANSPORTER_DETAILS.TRANSPORT_COST].innerHTML;
      row_data['transportation_cost_comment'] = $('#table4 tr').eq(parseInt(keys) + 1)[0].childNodes[TRANSPORTER_DETAILS.TRANSPORTER_COMMENT].innerHTML;
      editedData.push(row_data);
    }
    return editedData;
  }

  var transportationResetClick = false;
  if (transporter_table_created) {
    transporter_table.clear().destroy();
  } else {
    transporter_table_created = true;
  }
  $('#transporter_details').html("");
  $('<th>Total:</th>').appendTo('#transporter_details');
  for (var i = 1; i < transporter_data_table_columns.length; i++) {
    $('<th></th>').appendTo('#transporter_details');
  }
  transporter_table = $('#table4').DataTable({
    destroy: true,
    data: transporter_data_set,
    columns: transporter_data_table_columns,
    "dom": paymentTableDom,
    "pageLength": 1000,
    "oTableTools": {
      "sSwfPath": "/media/social_website/scripts/libs/tabletools_media/swf/copy_csv_xls_pdf.swf",
      "aButtons": [{

        "sExtends": "text",
        "sButtonText": "Edit",
        "fnClick": function(nButton, oConfig) {
          superEditMode = 1;
          $("#summary_payments").parent().addClass('disabled');
          $("#gaddidar_payments").parent().addClass('disabled');
          $('#ToolTables_table4_1').removeClass('disable-button');
          $('#ToolTables_table4_0').addClass('disable-button');
          $('#payments_from_date').parent().parent().addClass('disable-button');
          $('#payments_to_date').parent().parent().addClass('disable-button');
          $('#aggregator_payments').parent().parent().addClass('disable-button');
          $('#payments_from_date').removeClass('black-text');
          $('#payments_to_date').removeClass('black-text');
          flag_edit_Table4 = true;
          $('#table4').find('td:nth-child('+(TRANSPORTER_DETAILS.TRANSPORT_COST+1)+')').addClass('editcolumn');
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
                  transporter_data_set[keys - 1][TRANSPORTER_DETAILS.TRANSPORT_COST] = parseFloat($('#table4 tr').eq(parseInt(keys) + 1)[0].childNodes[TRANSPORTER_DETAILS.TRANSPORT_COST].innerHTML);
                  transporter_data_set[keys - 1][TRANSPORTER_DETAILS.TRANSPORTER_COMMENT] = $('#table4 tr').eq(parseInt(keys) + 1)[0].childNodes[TRANSPORTER_DETAILS.TRANSPORTER_COMMENT].innerHTML;
                  //console.log(transporter_data_set[keys - 1][7]);
                  transport_payment[transporter_data_set[keys - 1][TRANSPORTER_DETAILS.ROW_ID]]['transportation_cost__sum'] = transporter_data_set[keys - 1][TRANSPORTER_DETAILS.TRANSPORT_COST];
                  transport_payment[transporter_data_set[keys - 1][TRANSPORTER_DETAILS.ROW_ID]]['transportation_cost_comment'] = transporter_data_set[keys - 1][TRANSPORTER_DETAILS.TRANSPORTER_COMMENT];
                }
                rows_table4 = [];
                get_payments_data();
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
              $('#payments_from_date').parent().parent().removeClass('disable-button');
              $('#payments_to_date').parent().parent().removeClass('disable-button');
              $('#aggregator_payments').parent().parent().removeClass('disable-button');
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
      //Total of every column
      for (var i = 1; i < transporter_data_table_columns.length; i++) {
        if(transporter_data_table_totals.indexOf(i) != -1) {
          total = api.column(i).data().reduce(function(a, b) {
            if (a === "") {
              a = 0;
            }
            if (b === "") {
              b = 0;
            }
            return parseFloat(a) + parseFloat(b);
          }, 0);
          $(api.column(i).footer()).html(finalFormat(total + ""));
        } else {
          $(api.column(i).footer()).html("");
        }
      }
    }
  });

  aggregator_sheet_name = "Aggregator Payment_" + getFormattedDate(aggregator) + "Payment Summary_" + getCurrentTime();
  gaddidar_sheet_name = "Aggregator Payment_" + getFormattedDate(aggregator) + "Commission Agent Details_" + getCurrentTime();
  transporter_sheet_name = "Aggregator Payment_" + getFormattedDate(aggregator) + "Transporter Details_" + getCurrentTime();
  header_dict = payment_model["header_dict"];
}

function getFormattedDate(aggregator_id) {
  var monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "June",
    "July", "Aug", "Sept", "Oct", "Nov", "Dec"
  ];
  var aggregator_index = aggregator_ids.indexOf(parseInt(aggregator_id));
  var name = (aggregator_names[aggregator_index]).replace('.', '');
  var fromDate = new Date(payments_start_date);
  var toDate = new Date(payments_to_date);
  var str = name + "(" + aggregator_id + ")" + "_" + monthNames[fromDate.getMonth()] + fromDate.getDate() + " to " + monthNames[toDate.getMonth()] + toDate.getDate() + "_";
  return str;
}

function getCurrentTime() {
  var now = new Date();
  var date = now.getDate()+"-"+(now.getMonth()+1)+"-"+now.getFullYear();
  var time = now.getHours()+":"+now.getMinutes()+":"+now.getSeconds();
  var str = "(" + date + " " + time + ")";
  return str;
}

//To get data for aggregator, transporter, gaddidar payment sheets from server for specified time period
function get_payments_data() {
  hidePaymentDetails();
  payments_start_date = $("#payments_from_date").val();
  payments_to_date = $("#payments_to_date").val();
  aggregator_id = $('#aggregator_payments :selected').val(); 
  if (payments_start_date != "" && payments_to_date != "" && Date.parse(payments_start_date) < Date.parse(payments_to_date) && new Date(payments_start_date) < new Date(payments_to_date) && new Date(payments_to_date) - new Date(payments_start_date) <= 1296000000 && aggregator_id != "") {
    showLoader();
    $.get("/loop/payments/", {
      'start_date': payments_start_date,
      'end_date': payments_to_date,
      'aggregator_id': aggregator_id
    }).done(function(data) {
      hideLoader();
      $('#aggregator_payment_tab').show();
      $('#download_payment_sheet').show();
      $("#aggregator_payment_details").show();
      payments_data = JSON.parse(data);

      outliers_data = payments_data.outlier_data;
      outliers_transport_data = payments_data.outlier_transport_data;
      outlier_daily_data = payments_data.outlier_daily_data;
      payments_gaddidar_contribution = payments_data.gaddidar_data;
      agg_id = selected_aggregator.attr("id");
      aggregator_payment_sheet(payments_data.aggregator_data, selected_aggregator.val(), selected_aggregator.attr("id"), selected_aggregator[0].innerHTML);
      if (table_created) {
      $('#outliers_data').html("");
    }
    outliers_summary(aggregator_id);
    });
  } else {
    alert("Please select valid date range \n 1. Date Range should not exceed 15 days. \n 2. Please make sure that <To> date is after <From> date. \n 3. Please select an aggregator.");
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

/* This file should contain all the JS for Loop dashboard */
window.onload = initialize;

var language, selected_tab, selected_parameter, selected_page, country_id = 1, state_id = -1;
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
  get_filter_data(language, country_id);
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
//To check for any items data change (textview, drop downs, button click)
function set_filterlistener() {
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
          aggregator_data_set_copy[i] = aggregator_data_set_copy[i].slice(0, 10);
          aggregator_data_set_copy[i].push(aggregator_data_set[i][12])
          aggregator_data_set_copy[i].push(aggregator_data_set[i][13])
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
          font_size: 9,
          num_format: '#,##0.00',
          text_wrap: true
        }

        var json_to_send = {
          header: header_json,
          data: data_json,
          cell_format: cell_format,
          sheet_header: 'Loop ' + localStorage.state + ' (' + localStorage.country + ')',
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
  $("#download_payment_sheets").hide();
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
      $.each(aggregators_for_filter,function(index,aggregator_data){
        aggregator_ids.push(aggregator_data.user__id);
        aggregator_names.push(aggregator_data.name_en);
      });
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

      aggregator_data_set.push([sno.toString(), dates[i], mandis[i][j].mandi_name, parseFloat(quantites[i][j].toFixed(2)), parseFloat(quantites[i][j].toFixed(2)), 0, transport_cost[i][j], farmer_share[i][j].farmer_share_amount, 0, parseFloat(net_payment.toFixed(2)), agg_id, mandis[i][j].mandi_id, "", farmer_share[i][j].farmer_share_comment]);

      sno += 1;
    }
  }

  for (var i = 0; i < gaddidar_contribution_data_length; i++) {
    if (aggregator == payments_gaddidar_contribution[i][USER_CREATED__ID].toString()) {
      for (var j = 0; j < aggregator_data_set.length; j++) {
        if (aggregator_data_set[j].indexOf(payments_gaddidar_contribution[i]['date']) != -1 && aggregator_data_set[j].indexOf(payments_gaddidar_contribution[i]['mandi__name']) != -1) {
          aggregator_data_set[j][8] += parseFloat(payments_gaddidar_contribution[i]['amount']);
          aggregator_data_set[j][9] = parseFloat((aggregator_data_set[j][9] - parseFloat(payments_gaddidar_contribution[i]['amount'])).toFixed(2));
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
          aggregator_data_set[j][4] = parseFloat(aggregator_incentive[i]['quantity__sum']);
          aggregator_data_set[j][5] = parseFloat(aggregator_incentive[i]['amount']);
          aggregator_data_set[j][9] = (parseFloat(aggregator_data_set[j][9]) + parseFloat(aggregator_data_set[j][5])).toFixed(2);
          aggregator_data_set[j][12] = aggregator_incentive[i]['comment'];
          break;
        }
      }
    }
  }
  //TODO: to be removed. Added fot temporary purposes.
  var data_set_length = aggregator_data_set.length;
  aggregator_data_set.push([sno.toString(), "", "Mobile Recharge ", "", "", 150, "", "", "", 150, "", "", "", ""]);

  var gaddidar_data_set_clone = [];
  for (var i = 0; i < gaddidar_data_set.length; i++) {
    gaddidar_data_set_clone.push(gaddidar_data_set[i].slice());
    if (gaddidar_data_set[i][11] == 1)
      gaddidar_data_set_clone[i][4] = parseFloat(gaddidar_data_set_clone[i][4]) * 100 + '%';
  }
  $(window).on('beforeunload', function() {
    if (!$('#ToolTables_table2_1').hasClass('disable-button') || !$('#ToolTables_table3_1').hasClass('disable-button') || !$('#ToolTables_table4_1').hasClass('disable-button'))
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
    $('#aggregator_net_volume_row').val($this.parent()[0].childNodes[4].innerHTML);
    $('#aggregator_commission_row').val(parseFloat($this.parent()[0].childNodes[5].innerHTML / ($this.parent()[0].childNodes[4].innerHTML)).toFixed(2));
    $('#aggregator_share_row').val(parseFloat($this.parent()[0].childNodes[5].innerHTML).toFixed(2));
    $('#aggregator_comment_row').val($this.parent()[0].childNodes[10].innerHTML);
    $('#aggregator_error_div').hide();
  }

  function initializeFarmerModal() {
    $('#farmer_date_row').val($this.parent()[0].childNodes[1].innerHTML);
    $('#farmer_mandi_row').val($this.parent()[0].childNodes[2].innerHTML);
    $('#farmer_volume_row').val($this.parent()[0].childNodes[3].innerHTML);
    $('#farmer_net_volume_row').val($this.parent()[0].childNodes[4].innerHTML);
    $('#farmer_transport_cost_row').val($this.parent()[0].childNodes[6].innerHTML);
    $('#farmer_gaddidar_commission_row_farmer').val($this.parent()[0].childNodes[8].innerHTML);
    $('#farmer_commission_row').val(parseFloat($this.parent()[0].childNodes[7].innerHTML / ($this.parent()[0].childNodes[4].innerHTML)).toFixed(2));
    $('#farmer_share_row').val(parseFloat($this.parent()[0].childNodes[7].innerHTML).toFixed(2));
    $('#farmer_comment_row').val($this.parent()[0].childNodes[11].innerHTML);
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
    if ($this.context.cellIndex === 5 && flag_edit_Table2 == true) {
      initializeAggregatorModal();
      $('#aggregator_modal').openModal();
      $('#aggregator_commission_row').focus();
    } else if ($this.context.cellIndex === 7 && flag_edit_Table2 == true) {
      initializeFarmerModal();
      $('#farmer_modal').openModal();
      $('#farmer_commission_row').focus();
    }

  });
  $('#aggregator_commission_row').on('change', function() {
    if (!inputValidation($('#aggregator_commission_row'))) {
      actionOnInvalidValidation($('#aggregator_commission_row'), $('#aggregator_error_div'), $('#aggregator_error_message'));
    } else {
      $('#aggregator_share_row').val(parseFloat(($this.parent()[0].childNodes[4].innerHTML) * $('#aggregator_commission_row').val()).toFixed(2));
      if ($('#aggregator_commission_row').val().trim() != '' && $('#aggregator_share_row').val().trim() != $this.parent()[0].childNodes[5].innerHTML)
        editedAggregator = 1;
    }
  });
  $('#aggregator_share_row').on('change', function() {
    if (!inputValidation($('#aggregator_share_row'))) {
      actionOnInvalidValidation($('#aggregator_share_row'), $('#aggregator_error_div'), $('#aggregator_error_message'))
    } else {
      $('#aggregator_commission_row').val(parseFloat($('#aggregator_share_row').val() / ($this.parent()[0].childNodes[4].innerHTML)).toFixed(2));
      if ($('#aggregator_share_row').val().trim() != '' && $('#aggregator_share_row').val().trim() != $this.parent()[0].childNodes[5].innerHTML)
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
      $('#farmer_share_row').val(parseFloat(($this.parent()[0].childNodes[4].innerHTML) * $('#farmer_commission_row').val()).toFixed(2));
      if ($('#farmer_commission_row').val().trim() != '' && $('#farmer_share_row').val().trim() != $this.parent()[0].childNodes[7].innerHTML)
        editedFarmer = 1;

    }
  });
  $('#farmer_share_row').on('change', function() {
    if (!inputValidation($('#farmer_share_row'))) {
      actionOnInvalidValidation($('#farmer_share_row'), $('#farmer_error_div'), $('#farmer_error_message'));
    } else {
      $('#farmer_commission_row').val(parseFloat($('#farmer_share_row').val() / ($this.parent()[0].childNodes[4].innerHTML)).toFixed(2));
      if ($('#farmer_share_row').val().trim() != '' && $('#farmer_share_row').val().trim() != $this.parent()[0].childNodes[7].innerHTML)
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

    $('#farmer_share_row').val($('#table2').DataTable().cell($this.context.parentNode.rowIndex - 1, 7).data());
    $('#farmer_commission_row').val(parseFloat($('#table2').DataTable().cell($this.context.parentNode.rowIndex - 1, 7).data() / $this.parent()[0].childNodes[4].innerHTML).toFixed(2));
    $('#farmer_comment_row').val($('#table2').DataTable().cell($this.context.parentNode.rowIndex - 1, 13).data());

  });
  $('#farmer_submit_modal').on('click', function(ev) {
    if (!inputValidation($('#farmer_commission_row'))) {
      ev.preventDefault();
      $('#farmer_commission_row').val($this.parent()[0].childNodes[7].textContent / $this.parent()[0].childNodes[4].innerHTML);
      $('#farmer_share_row').val($this.parent()[0].childNodes[7].textContent);
      $('#farmer_commission_row').focus();
      return false;
    } else if (!inputValidation($('#farmer_share_row'))) {
      ev.preventDefault();
      $('#farmer_commission_row').val($this.parent()[0].childNodes[7].textContent / $this.parent()[0].childNodes[4].innerHTML);
      $('#farmer_share_row').val($this.parent()[0].childNodes[7].textContent);
      $('#farmer_share_row').focus();
      return false;
    } else if (farmerResetClick && editedFarmer == 0) {
      $this.parent()[0].childNodes[7].innerHTML = $('#table2').DataTable().cell($this.context.parentNode.rowIndex - 1, 7).data();
      $this.parent()[0].childNodes[11].innerHTML = $('#table2').DataTable().cell($this.context.parentNode.rowIndex - 1, 13).data();
      delete rows_table2_farmer[$this.context.parentNode.rowIndex];
      $this.removeAttr('class');
      $this.closest('tr').children('td:nth-child(12)')[0].className = '';
      $this.addClass('editcolumn');
      farmerResetClick = false;
    } else if (editedFarmer != 0) {

      $this.parent()[0].childNodes[7].innerHTML = $('#farmer_share_row').val();
      $this.parent()[0].childNodes[11].innerHTML = $('#farmer_comment_row').val() + ' - ' + window.localStorage.name;
      $this.parent()[0].childNodes[9].innerHTML = parseFloat(parseFloat($this.parent()[0].childNodes[6].innerHTML) + parseFloat($this.parent()[0].childNodes[5].innerHTML) - parseFloat($this.parent()[0].childNodes[8].innerHTML) - parseFloat($this.parent()[0].childNodes[7].innerHTML)).toFixed(2);
      if ((parseFloat($this.parent()[0].childNodes[5].innerHTML) + parseFloat($this.parent()[0].childNodes[6].innerHTML)) < parseFloat($this.parent()[0].childNodes[7].innerHTML)) {

        //  $this.parent().css('background-color', '#E5FEB5').css('font-weight', 'bold').css('color', '#009');
        $this.removeAttr('class');
        $this.addClass('editedcelledge');
        $this.closest('tr').children('td:nth-child(12)')[0].className = 'editedcelledge';

      } else {
        $this.removeAttr('class');
        $this.addClass('editedcell');
        $this.closest('tr').children('td:nth-child(12)')[0].className = 'editedcell';
        $this.closest('tr').children('td:nth-child(12)')[0].className = 'editedcell';
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
    $('#aggregator_share_row').val($('#table2').DataTable().cell($this.context.parentNode.rowIndex - 1, 5).data());
    $('#aggregator_commission_row').val(parseFloat($('#table2').DataTable().cell($this.context.parentNode.rowIndex - 1, 5).data() / $this.parent()[0].childNodes[4].innerHTML).toFixed(2))
    $('#aggregator_comment_row').val($('#table2').DataTable().cell($this.context.parentNode.rowIndex - 1, 12).data());
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
      $this.parent()[0].childNodes[5].innerHTML = $('#table2').DataTable().cell($this.context.parentNode.rowIndex - 1, 5).data();
      $this.parent()[0].childNodes[10].innerHTML = $('#table2').DataTable().cell($this.context.parentNode.rowIndex - 1, 12).data();
      delete rows_table2[$this.context.parentNode.rowIndex];
      $this.removeAttr('class');
      $this.closest('tr').children('td:nth-child(11)')[0].className = '';
      $this.addClass('editcolumn');
      aggregatorResetClick = false;
    } else if (editedAggregator != 0) {
      $('#aggregator_modal').closeModal();
      $this.parent()[0].childNodes[5].innerHTML = $('#aggregator_share_row').val();
      $this.parent()[0].childNodes[10].innerHTML = $('#aggregator_comment_row').val() + ' - ' + window.localStorage.name;
      $this.parent()[0].childNodes[9].innerHTML = parseFloat(parseFloat($this.parent()[0].childNodes[6].innerHTML) + parseFloat($this.parent()[0].childNodes[5].innerHTML) - parseFloat($this.parent()[0].childNodes[8].innerHTML) - parseFloat($this.parent()[0].childNodes[7].innerHTML)).toFixed(2)
      if (parseFloat($this.parent()[0].childNodes[5].innerHTML / $this.parent()[0].childNodes[4].innerHTML) > 0.5) {
        $this.removeAttr('class');
        $this.addClass('editedcelledge');
        $this.closest('tr').children('td:nth-child(11)')[0].className = 'editedcelledge';
      } else {
        $this.removeAttr('class');
        $this.addClass('editedcell');
        $this.closest('tr').children('td:nth-child(11)')[0].className = 'editedcell';
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
      row_data['amount'] = $('#table2 tr').eq(parseInt(keys) + 1)[0].childNodes[5].innerHTML;
      mandi_idDict['online_id'] = $('#table2').DataTable().cell(keys - 1, 11).data();
      row_data['mandi'] = mandi_idDict;
      aggregator_idDict['online_id'] = $('#table2').DataTable().cell(keys - 1, 10).data();
      row_data['aggregator'] = aggregator_idDict;
      row_data['comment'] = $('#table2 tr').eq(parseInt(keys) + 1)[0].childNodes[10].innerHTML;
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
      row_data['amount'] = $('#table2 tr').eq(parseInt(keys) + 1)[0].childNodes[7].innerHTML;
      mandi_idDict['online_id'] = $('#table2').DataTable().cell(keys - 1, 11).data();
      row_data['mandi'] = mandi_idDict;
      row_data['comment'] = $('#table2 tr').eq(parseInt(keys) + 1)[0].childNodes[11].innerHTML;
      aggregator_idDict['online_id'] = $('#table2').DataTable().cell(keys - 1, 10).data();
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
      title: "Quantity[Q'] (in Kg)"
    }, {
      title: "Quantity Post Deduction[Q] (in Kg)"
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
          $('#table2').find('tr td:nth-child(6)').addClass('editcolumn');
          $('#table2').find('tr td:nth-child(8)').addClass('editcolumn');
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

                  aggregator_data_set[keys - 1][5] = parseFloat($('#table2 tr').eq(parseInt(keys) + 1)[0].childNodes[5].innerHTML);
                  aggregator_data_set[keys - 1][12] = $('#table2 tr').eq(parseInt(keys) + 1)[0].childNodes[10].innerHTML;
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
                  aggregator_data_set[keys - 1][7] = parseFloat($('#table2 tr').eq(parseInt(keys) + 1)[0].childNodes[7].innerHTML);
                  aggregator_data_set[keys - 1][13] = $('#table2 tr').eq(parseInt(keys) + 1)[0].childNodes[11].innerHTML;
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
                delay = 8000;
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
                delay = 8000;
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
        'column_width': 9,
        'formula': null,
        'label': 'Market',
        'total': false
      },
      {
        'column_width': 7,
        'formula': null,
        'label': "Quantity [Q'] (in Kg)",
        'total': true
      },
      {
        'column_width': 7,
        'formula': null,
        'label': 'Quantity Post Deduction [Q] (in Kg)',
        'total': true
      },
      {
        'column_width': 8.64,
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
        'column_width': 8.18,
        'formula': null,
        'label': "Farmers' Contribution [FC] (in Rs)",
        'total': true
      },
      {
        'column_width': 8.18,
        'formula': null,
        'label': 'Commission Agent Contribution [CAC] (in Rs)',
        'total': true
      },
      {
        'column_width': 8.73,
        'formula': 'F + G - H - I',
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
  var aggregator_index = aggregator_ids.indexOf(parseInt(aggregator_id));
  var name = aggregator_names[aggregator_index];
  var fromDate = new Date(payments_start_date);
  var toDate = new Date(payments_to_date);
  var str = name + "(" + aggregator_id + ")" + "_" + monthNames[fromDate.getMonth()] + fromDate.getDate() + " to " + monthNames[toDate.getMonth()] + toDate.getDate() + "_";
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

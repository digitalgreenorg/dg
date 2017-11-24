/**
 * Created by Lokesh on 2016-06-09.
 */
// JavaScript Document

// To remove Conflict
var j$ = jQuery.noConflict();
var chosendeos = [];
var bflag = 0;
var tflag = 0;

j$(document).ready(function() {

  var stdate = document.getElementById('sdate');
  var current_date = new Date();
  var current_month = current_date.getMonth() + 2;
  var current_year = current_date.getFullYear().toString();

  var from_block_month_list = [];
  var to_block_month_list = [];
  for (var month = current_month; month <= 12; month++) {
    from_block_month_list.push(month);
    to_block_month_list.push(month);
  }

  j$(stdate).monthpicker();
  j$(stdate).monthpicker('disableMonths', from_block_month_list);

  j$(stdate).monthpicker().bind('monthpicker-change-year', function (e, year) {
      if(year == current_year) {
        j$(stdate).monthpicker('disableMonths', from_block_month_list);
      } else if(year > current_year) {
          j$(stdate).monthpicker('disableMonths', [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]); // (re)enables all
      } else {
        j$(stdate).monthpicker('disableMonths', []); // (re)enables all
      }

  });

  var etdate = document.getElementById('edate');
  j$(etdate).monthpicker();
  j$(etdate).monthpicker('disableMonths', to_block_month_list);

  j$(etdate).monthpicker().bind('monthpicker-change-year', function (e, year) {
      if(year == current_year) {
        j$(etdate).monthpicker('disableMonths', to_block_month_list);
      }else if(year > current_year) {
          j$(etdate).monthpicker('disableMonths', [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]); // (re)enables all
      }  else {
        j$(etdate).monthpicker('disableMonths', []); // (re)enables all
      }
  });

  var id = 11;
  var name = 'BRLPS';
  setpartnerlistdiv(id, name);
});

// function setpartnerlistdiv(text)
function setpartnerlistdiv(id, name) {
      var partner_id = id;
      var partner_name = name;
      
      var listitems = '<option value = ' + partner_id + ' >' + name + '</option>';
      j$("select#partnerlist").append(listitems);
      j$("select#partnerlist").show();
      j$('#partnerlist').chosen();
      districtfilter(partner_id);
    }

function districtfilter(partner_id)
    {
       j$.ajax(
       {
        type:'GET',
        data:{
        'partner': partner_id
        },
        url: window.location.origin + "/coco/mrp/getdistrict",

        success: function(data){

            j$("select#districtlist").show();
            var listitems = '<option value = -1> -------</option>';

            for (var i = 0; i < data.length; i++)
            {
              listitems += '<option id = "' + data[i].village__block__district__id +  '"value = ' + partner_id + '>' + data[i].village__block__district__district_name + '</option>';
            }
            j$("select#districtlist").append(listitems);
            j$('#districtlist').chosen();
        },
        error: function(data){
                alert("Sorry there was an error!");
        }
      });
    }

function setdistrictlistdiv(partner_id) 
    {
      var text = j$('#districtlist option:selected');
      var district_id = text.attr('id');
      if(district_id != -1) {
        blockfilter(district_id);
      } 
    }

function blockfilter(district_id) {
    j$.ajax(
        {
            type: 'GET',
            data: {
                'district': district_id
            },
            url: window.location.origin + "/coco/mrp/getblock",

            success: function (data) {
                if(bflag == 0) {
                  j$("select#blocklist").show();
                  j$('#blocklist').chosen();
                  bflag = 1;
                }
                
                var listitems = '<option value = -1>-------</option>';
                for (var i = 0; i < data.length; i++) {
                    listitems += '<option id="' + data[i].id +'"value = ' + district_id + '>'+ data[i].block_name + '</option>';
                }
                
                j$('#blocklist').val('').find('option').remove().end();
                j$("select#blocklist").append(listitems);
                j$('#blocklist').trigger('chosen:updated');
            },
            error: function (data) {
                alert("Sorry there was an error!");
            }
        });
}


function mrp_payment_goclicked() 
  {
    var sdate = document.getElementById("sdate").value;
    var edate = document.getElementById("edate").value;
    var partner = document.getElementById("partnername");
    var partner_name = j$("#partnerlist option:selected").text();
    var district = document.getElementById("districtname");
    var district_name = j$("#districtlist option:selected").text();
    var block = document.getElementById("blockname");
    var block_name = j$("#blocklist option:selected").text();
    if ((sdate == "" || edate == "" || partner_name == "" || district_name == "" ||  block_name == "" || block_name == "-------")) {
      alert("Information Incomplete! Please fill missing entries");
    }else {
      var sdateArr = sdate.split("/");
      var edateArr = edate.split("/");
      if((sdateArr[1] > edateArr[1]) || (sdateArr[1] == edateArr[1] && sdateArr[0] > edateArr[0])) {
        alert("Choose Correct date range");
      } else {
        j$(document).ready(function () {
            j$.blockUI({ css: {
                border: 'none',
                padding: '15px',
                backgroundColor: '#000',
                '-webkit-border-radius': '10px',
                '-moz-border-radius': '10px',
                opacity: .5,
                color: '#ffffff'
            } });
        });
        
        j$.ajax({

            type: 'GET',
            data: {
                'start_date' : sdate,
                'end_date' : edate,
                'partner_name' : partner_name,
                'district_name' : district_name,
                'block_name': block_name
            },

            url: window.location.origin + "/coco/mrp/report",

            success: function (data) {
                j$.unblockUI();
                var listitems = data;
                if(tflag == 1) {
                  j$('#example').dataTable().fnDestroy();
                  j$('#example').empty();
                }
                j$("#example").dataTable({

                    "dom": 'B<"clear">lfrtip',
                    "bDeferRender": true,
                    "AutoWidth": false,
                    "columnDefs": [
                      { "title": "My column title", "targets": 0 }
                    ],
                    "aoColumns": [
                        {sTitle: "S. No."},
                        {sTitle: "Name"},
                        {sTitle: "Total Screening"},
                        {sTitle: "Successful Screening"},
                        {sTitle: "Screening amount"},
                        {sTitle: "Adoptions"},
                        {sTitle: "Adoptions Amount"},
                        {sTitle: "Total Amount"}
                    ],

                    "aaData": data['output'] ,      //aaData takes array_table_values and push data in the table.
                "swfPath" : "/media/social_website/scripts/libs/tabletools_media/swf/copy_csv_xls.swf",
                "buttons": [
            
                    {
                    "extend": 'copyHtml5',
                    "text": 'Copy to Clipboard',
                    "title": 'MRP Payment'
                    },
                    {
                    "extend": 'csvHtml5',
                    "text": 'Download in CSV',
                    "title":'MRP Payment'
                    }
                ]
                });
                tflag = 1;
                $('.dt-buttons').css('float','right');
             },
            error: function (data) {
                j$.unblockUI();
                alert("Sorry there was an error!");
            }
        });
      }
    }
}
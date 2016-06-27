/**
 * Created by Lokesh on 2016-06-09.
 */
// JavaScript Document

var pflag = 0;
var diflag = 0;
var chosendeos = [];
var bflag = 0;
var tflag = 0;

function partnersetter()
    {
      if (pflag == 0)
      {
          document.getElementById('partnerlist').classList.remove('nodisplay');
          document.getElementById('partnerlist').classList.add('blockdisplay');
          document.getElementById('districtlist').classList.remove('blockdisplay');
          document.getElementById('districtlist').classList.add('nodisplay');
          document.getElementById('blocklist').classList.remove('blockdisplay');
          document.getElementById('blocklist').classList.add('nodisplay');
          pflag = 1;
      }

      else if (pflag == 1)
      {
          document.getElementById('partnerlist').classList.remove('blockdisplay');
          document.getElementById('partnerlist').classList.add('nodisplay');
          pflag = 0;
      }

}

$(document).ready(function() {

  var stdate = document.getElementById('sdate');
  $(stdate).monthpicker();
  var etdate = document.getElementById('edate');
  $(etdate).monthpicker();
  var id = 11;
  var name = 'BRLPS';
  setpartnerlistdiv(id, name);

  // $.ajax(
  //       {
  //         type:'GET',
  //         url: window.location.origin + "/analytics/mrptool/getpartner",

  //         success: function(data) {
  //            var listitems = '';
  //            for (var j = 0; j < data.length; j++)
  //            {
  //              listitems += '<li class=' + '"item h-overflow"' + 'id="' + data[j].id +  '"onclick="' + 'setpartnerlistdiv(this)' + '">' + data[j].partner_name + '</li>';
  //            }
  //            // $("ul#partnerlist")[0].innerHTML= listitems;
  //            $("ul#partnerlist").html(listitems);
  //         },
  //         error: function(data){
  //            alert("Sorry there was an error while partner!");
  //         }
  //       });

});

// function setpartnerlistdiv(text)
function setpartnerlistdiv(id, name)
    {
      // var partner_id = text.id;
      var partner_id = id;
      // var partner_name = $(text).html();//text.innerText.trim();
      var partner_name = name;
      $("div#partnername").html(partner_name);
      $("div#districtname").html("Choose District");
      document.getElementById('districtlist').classList.remove('nodisplay');
      document.getElementById('districtlist').classList.add('blockdisplay');
      diflag = 1;
      districtfilter(partner_id);
    }

function districtsetter()
    {
      if (diflag == 0)
      {
          document.getElementById('districtlist').classList.remove('nodisplay');
          document.getElementById('districtlist').classList.add('blockdisplay');
          document.getElementById('partnerlist').classList.remove('blockdisplay');
          document.getElementById('partnerlist').classList.add('nodisplay');
          document.getElementById('blocklist').classList.remove('blockdisplay');
          document.getElementById('blocklist').classList.add('nodisplay');
          diflag = 1;
      }

      else if (diflag == 1)
      {
          document.getElementById('districtlist').classList.remove('blockdisplay');
          document.getElementById('districtlist').classList.add('nodisplay');
          diflag = 0;
      }
    }

function districtfilter(partner_id)
    {
       $.ajax(
       {
        type:'GET',
        data:{
        'partner': partner_id
        },
        url: window.location.origin + "/analytics/mrptool/getdistrict",

        success: function(data){

            var listitems = '';
            for (var i = 0; i < data.length; i++)
            {

              listitems += '<li class=' + '"item h-overflow"' + 'id="' + data[i].village__block__district__id +  '"onclick="' + 'setdistrictlistdiv(this' + ',' + partner_id + ')' + '">' + data[i].village__block__district__district_name + '</li>';
            }
            $("ul#districtlist").html(listitems);
        },
        error: function(data){
                alert("Sorry there was an error!");
        }
      });
    }

function setdistrictlistdiv(text, partner_id) {
      chosendeos = [];
      var district_name = $(text).html();//text.innerText.trim();
      var district_id = text.id
      $("div#districtname").html(district_name);
      $("div#blockname").html("Choose Block");
      document.getElementById('blocklist').classList.remove('nodisplay');
      document.getElementById('blocklist').classList.add('blockdisplay');
      bflag = 1;
      blockfilter(district_id);
}

/* MRP payment code starts here */

function blocksetter() {
    if (bflag == 0) {
        document.getElementById('blocklist').classList.remove('nodisplay');
        document.getElementById('blocklist').classList.add('blockdisplay');
        document.getElementById('districtlist').classList.remove('blockdisplay');
        document.getElementById('districtlist').classList.add('nodisplay');
        document.getElementById('partnerlist').classList.remove('blockdisplay');
        document.getElementById('partnerlist').classList.add('nodisplay');
        bflag = 1;
    }
    else if (bflag == 1) {

        document.getElementById('blocklist').classList.remove('blockdisplay');
        document.getElementById('blocklist').classList.add('nodisplay');
        bflag = 0;

    }
}

function blockfilter(district_id) {
  
    $.ajax(
        {
            type: 'GET',
            data: {
                'district': district_id
            },
            url: window.location.origin + "/analytics/mrptool/getblock",

            success: function (data) {

                var listitems = '';
                for (var i = 0; i < data.length; i++) {
                    listitems += '<li class=' + '"item h-overflow"' + 'id="' + data[i].id + '"onclick="' + 'setblocklistdiv(this' + ',' + district_id + ')' + '">' + data[i].block_name + '</li>';
                }
                $("ul#blocklist").html(listitems);
            },
            error: function (data) {
                alert("Sorry there was an error!");
            }
        });
}

function setblocklistdiv(text, district_id) {
    var block_name = $(text).html();//text.innerText.trim();
    $("div#blockname").html(block_name);
    document.getElementById('blocklist').classList.remove('nodisplay');
    document.getElementById('blocklist').classList.add('blockdisplay');
    bflag = 1;
}

function mrp_payment_goclicked() {


    var sdate = document.getElementById("sdate").value;
    var edate = document.getElementById("edate").value;
    var partner = document.getElementById("partnername");
    var partner_name = $(partner).html();
    var district = document.getElementById("districtname");
    var district_name = $(district).html();
    var block = document.getElementById("blockname");
    var block_name = $(block).html();
    
    if (sdate == "" || edate == "" || partner_name == "" || district_name == "" ||  block_name == "" ) {
      alert("Information Incomplete! Please fill missing entries");
    } else {

      $(document).ready(function () {
          $.blockUI({ css: {
              border: 'none',
              padding: '15px',
              backgroundColor: '#000',
              '-webkit-border-radius': '10px',
              '-moz-border-radius': '10px',
              opacity: .5,
              color: '#ffffff'
          } });
      });
      
      $.ajax({

          type: 'GET',
          data: {
              'start_date' : sdate,
              'end_date' : edate,
              'partner_name' : partner_name,
              'district_name' : district_name,
              'block_name': block_name
          },

          url: window.location.origin + "/analytics/mrptool/report",

          success: function (data) {
              $.unblockUI();
              var listitems = data;
              if(tflag == 1) {
                $('#example').dataTable().fnDestroy();
                $('#example').empty();
              }
              $("#example").dataTable({

                  "sDom": 'T<"clear">lfrtip',
                  "bDeferRender": true,
                  "bAutoWidth": false,
                  "aoColumns": [
                      {sTitle: "S.no"},
                      {sTitle: "Name"},
                      {sTitle: "Total Screening"},
                      {sTitle: "Successful Screening"},
                      {sTitle: "Screening amount"},
                      {sTitle: "Adoptions"},
                      {sTitle: "Adoptions Amount"},
                      {sTitle: "Total Amount"}
                  ],

                  "aaData": data['output'] ,      //aaData takes array_table_values and push data in the table.
          "oTableTools":{

              "sSwfPath": "/media/social_website/scripts/libs/tabletools_media/swf/copy_csv_xls.swf",
  			"aButtons": [
  	                           {
  	                               "sExtends": "copy",
  	                               "sButtonText": "Copy to Clipboard"
  	                           },
  	                           {
  	                               "sExtends": "xls",
  	                               "sButtonText": "Download in Excel"
  	                           }
  	                       ]
                      }
              })
              tflag = 1;
           },
          error: function (data) {
              alert("Sorry there was an error !");
          }
      });
    }
}

/* MRP Payment code ends here */

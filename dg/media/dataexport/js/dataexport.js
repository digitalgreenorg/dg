jQuery(document).ready(function ($) {
  start_date = "", end_date = ""
  $('.badge').css('cursor','pointer');
  $('[data-toggle="popover"]').popover();
  var start = moment().subtract(365, 'days');
  var end = moment();
  $('input[name="date_period"]').daterangepicker({
  autoUpdateInput: true,
  locale: {
      format: 'YYYY-MM-DD'
    },
    startDate: start,
    endDate: end,
    autoApply:true,
    maxDate: new Date(),
    maxSpan:{
      'years': 1
    }
  })

  $('#id_data').select2({placeholder: "Select data for screening or Adoption"});
  $('#id_data_category').select2({placeholder: "Select data for health or Agriculture"});
  $('#id_country').select2({placeholder: "Select Country"});
  $('#id_state').select2({placeholder: "Select State"});


  $('table').addClass('stripe');
    $('table').css('border-collape','collapse');
    $('#sidebarCollapse').click(function(){
      if($('#page-content-wrapper').hasClass('active')){
        $('.badge').text('Hide Filters')
        $('#page-content-wrapper').removeClass('active');
        $('#sidebar-wrapper').removeClass('active');

      }
      else{
        $('.badge').text('Show Filters')
        $('#sidebar-wrapper').addClass('active');
        $('#page-content-wrapper').addClass('active');


      }
    });

    $('.dataframe tfoot th').each( function () {
      var title = $('.dataframe thead th').eq( $(this).index() ).text();
      $(this).html( '<input type="text" placeholder="Search '+title+'" />' );
    } );

    var table = $('.dataframe').DataTable({
      lengthChange: false,
     buttons: [
     'excel'
     ]
   });

    table.buttons().container()
    .appendTo( '#DataTables_Table_1_wrapper .col-md-6:eq(0)' );


    $(".dataframe tfoot input").on( 'keyup change', function () {
      table
      .column( $(this).parent().index()+':visible' )
      .search( this.value )
      .draw();
    } );
    $($('.dt-buttons')[0]).hide()
    $('tr').css('text-align','left');
    
});

// country dropdown change to fetch states
// TO DO: this should be inside a function
$('#id_country').on('change', function() {
  $("#id_state").html('').select2({data: [{id: '', text: ''}]});
  // $('#id_state').val('').trigger('change');
  $('#id_state').children('option:first').remove();
  var country_id = $("#id_country option:selected").val();
    $.ajax({
      type: "GET",
      url: "/coco/export/get/state/"+country_id+'/',
      datatype: 'json',
      success: function(data){
        console.log(data)
         $("#id_state").select2({data: data.results});
      }
  });
});


   
// Main Ajax Call after selecting filters to fetch data
$("#data-extract").submit(function(event){
  event.preventDefault();
  // removing the html of this div to clear the data
  $('#wrapper-demo').html('');
  $('#loader').show();
  // serializing the form
  var data = $('#data-extract').serialize();
  $.ajax({
    type:"POST",
    url:"/coco/export/",
    data: data,
    dataType: 'html',
    success: function(response){
     $('#loader').hide();
     $('#wrapper-demo').html(response)
     $('#id_total_screenings').html($(response).filter('#tot_screenings').html())
     $('#id_total_adoptions').html($(response).filter('#tot_adoptions').html())
     $('#id_total_viewers').html($(response).filter('#tot_unique_viewers').html())
     $('#id_total_unique_adopters').html($(response).filter('#tot_unique_adopters').html())
     $($('.dataframe')[0]).addClass('table0');
     $($('.dataframe')[1]).addClass('table1');

     var table_0 = $('table.table0').DataTable({
        lengthChange: false,
     });

     var table_1 = $('table.table1').DataTable({
        lengthChange: false,
        buttons: ['excel']
     });

     table_1.buttons().container().prependTo( $(table_1.table().container()) );
     
     $($('.dt-buttons')[0]).css('width','10%');
     $('.buttons-excel').css('width','100%');


    $('table').addClass('table table-hover table-no-bordered');

    $('.dataframe tfoot th').each( function () {
      var title = $('.dataframe thead th').eq( $(this).index() ).text();
      $(this).html( '<input type="text" placeholder="Search '+title+'" />' );
    } );

    $(".dataframe tfoot input").on( 'keyup change', function () {
      table_0.column( $(this).parent().index()+':visible' ).search( this.value ).draw();
      table_1.column( $(this).parent().index()+':visible' ).search( this.value ).draw();
    } );


    $('tr').css('text-align','left');
      
    },
    error: function(error){
      console.log(error)
    }
  });
  return false;
});


// Upload validation checks

// File size should be less than 2 MB
var maxSizeExceeded = false;
$("#id_datafile").change(function () {
  $('#id_datafile-error').html('');
  if(this.files[0].size / 1024 / 1024 > 2){
      maxSizeExceeded = true;
    }
  else
    maxSizeExceeded = false;
});

// validating the file before uploading
$('#data-upload').validate({
   ignore: [],
   rules:{
       datafile: {
            required: true,
            extension: "csv"
        }
   },
   messages:{
       datafile:{
          required:"Please upload the file",
          extension:"Please upload a Valid file"
        }
   },
   submitHandler: function(form) {
    if(!maxSizeExceeded){
      form.submit();
      }
    else{
      alert('Max upload limit is 2 MB');
    }
    }
})

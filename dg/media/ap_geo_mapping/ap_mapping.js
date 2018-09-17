jQuery(document).ready(function($){
    

    $("select").css('width','40%');
    $("span.select2").css('min-width','40%');


    if(flag == "False"){
      $("#id_geographytype").select2();
      $("#id_apgeo").select2();
      $("#id_cocogeo").select2();
      $("#id_apgeo").html('').select2({data: [{id: '', text: ''}]});
      $("#id_cocogeo").html('').select2({data: [{id: '', text: ''}]});


      $.ajax({
            type: "GET",
            url: "/coco/get/geography/District/",
            datatype: 'json',
            success: function(data){
              // console.log(data)
              $("#id_apgeo").select2({data: data.results[0]});
              $("#id_cocogeo").select2({data: data.results[1]});
            },
            error: function(error){
              console.log(error)
            }
          });
    }
    else{
      $("#id_geographytype").select2();
      $("#id_apgeo").select2();
      $("#id_cocogeo").select2();
      $("#id_apgeo").html('').select2({data: [{id: '', text: ''}]});
      $("#id_cocogeo").html('').select2({data: [{id: '', text: ''}]});


      $.ajax({
            type: "GET",
            url: "/coco/get/geography/"+geo_type+"/",
            datatype: 'json',
            success: function(data){
              // console.log(data)
              $("#id_apgeo").select2({data: data.results[0]});
              $("#id_cocogeo").select2({data: data.results[1]});
            },
            error: function(error){
              console.log(error)
            }
          });
    }
    
    $("#id_geographytype").on('change', function(){
      $("#id_apgeo").html('').select2({data: [{id: '', text: ''}]});
      $("#id_cocogeo").html('').select2({data: [{id: '', text: ''}]});
      var selected_geography = $(this).val();
      //console.log(selected);
      $.ajax({
          type: "GET",
          url: "/coco/get/geography/"+selected_geography+'/',
          datatype: 'json',
          success: function(data){
            // console.log(data)
            $("#id_apgeo").select2({data: data.results[0]});
            $("#id_cocogeo").select2({data: data.results[1]});
          },
          error: function(error){
            console.log(error)
          }
        });
    });
  })
  $(function(){
	alert("Hi");
   // $("select#id_village").change(function(){
    $("#id_village").change(function(){

	alert("Hi");

      $.getJSON("/feeds/subcat/"+$(this).val()+"/", function(j) {
        var options = '<option value="">---------- </option>';
        for (var i = 0; i < j.length; i++) {
          options += '<option value="' + parseInt(j[i].pk) + '">' + j[i].fields['longname'] + '</option>';
        }
        $("#id_facilitator").html(options);
        $("#id_facilitator option:first").attr('selected', 'selected');
        $("#id_facilitator").attr('disabled', false);
      })
      $("#id_village").attr('selected', 'selected');
    })

  })

function filter_village()
{	
	if($("#id_village").val()>0)
	{
			var village_name = $('#id_village :selected').text();
			var options = '<option value="' + $('#id_village').val() + '">' + village_name + '</option>';
			alert(options);
		        for (var i = 0; i < 30; i++) 
			{
				$("#id_form-"+i+"-village").html(options);
				$("#id_form-"+i+"-village option:first").attr('selected', 'selected');
	        	}

	}

}

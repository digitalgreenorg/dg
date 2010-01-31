function filter()
{

	if($("#id_village").val()>0)
	{


	        $.getJSON("/feeds/groups/"+$("#id_village").val()+"/", function(j)
		{
			var options = '<option value="">---------- </option>';
		        for (var i = 0; i < j.length; i++) 
			{
		          options += '<option value="' + parseInt(j[i].pk) + '">' + j[i].fields['group_name'] + '</option>';
	        	}
		        $("#id_group").html(options);
		        $("#id_group").attr('selected', 'selected');
		        $("#id_group").attr('disabled', false);
		})
	}
	else
	{
		//$("id_animator").html('<option value="-1">Select Valid Village</option>');
		//$("id_animator").attr('disabled',true);

	}

}

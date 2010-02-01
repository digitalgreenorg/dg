function filter()
{

	if($("#id_village").val()>0)
	{

	        $.getJSON("/feeds/animators/"+$("#id_village").val()+"/", function(j)
		{
			var options = '<option value="">---------- </option>';
		        for (var i = 0; i < j.length; i++) 
			{
		          options += '<option value="' + parseInt(j[i].pk) + '">' + j[i].fields['name'] + '</option>';
	        	}
		        $("#id_animator").html(options);
		        $("#id_animator option:first").attr('selected', 'selected');
		        $("#id_animator").attr('disabled', false);
		})

	        $.getJSON("/feeds/groups/"+$("#id_village").val()+"/", function(j)
		{
			var options = '<option value="">---------- </option>';
		        for (var i = 0; i < j.length; i++) 
			{
		          options += '<option value="' + parseInt(j[i].pk) + '">' + j[i].fields['group_name'] + '</option>';
	        	}
		        $("#id_farmer_groups_targeted").html(options);
		        $("#id_farmer_groups_targeted option:first").attr('selected', 'selected');
		        $("#id_farmer_groups_targeted").attr('disabled', false);
		})
	}
	else
	{
		//$("id_animator").html('<option value="-1">Select Valid Village</option>');
		//$("id_animator").attr('disabled',true);

	}

}

function filter()
{
	alert('entered');
        $.getJSON("/feeds/animators/"+$("select#id_village").val()+"/", function(j)
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

	        $("#id_village").attr('selected', 'selected');
}

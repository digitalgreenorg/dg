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
		        $("#id_facilitator").html(options);
                        $("#id_facilitator option:first").attr('selected', 'selected');
                        $("#id_facilitator").attr('disabled', false);

			$("#id_cameraoperator").html(options);
		        $("#id_cameraoperator option:first").attr('selected', 'selected');
		        $("#id_cameraoperator").attr('disabled', false);
		})



                /*$.getJSON("/feeds/persons_village/"+$("#id_village").val()+"/", function(j)
                {
			var options;
                        //var options = '<option value="">---------- </option>';
                        for (var i = 0; i < j.length; i++)
                        {
                          options += '<option value="' + parseInt(j[i].pk) + '">' + j[i].fields['person_name'] + '</option>';
                        }
                        $("#id_farmers_shown_from").html(options);
                        $("#id_farmers_shown_from option:first").attr('selected', 'selected');
                        $("#id_farmers_shown_from").attr('disabled', false);
                })*/


	}

}

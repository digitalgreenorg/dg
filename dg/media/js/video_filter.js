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
		});
	}
}

//<!-- For Search's drop-down list -->

$(document).ready(function(){	   
		
	//Function called on clicking 'Go' button for region select drop-downs
	function regionSelect() {
		url = "./?state="+$("#stateId").val(){% if from_date and to_date %}+"&from_date={{from_date}}&to_date={{to_date}}"{%endif%};
		if(!($("#districtId").attr("disabled")))
			url += "&district="+$("#districtId").val();
		if(!($("#blockId").attr("disabled"))) 
			url += "&block="+$("#blockId").val();
		if(!($("#villageId").attr("disabled")))
			url += "&village="+$("#villageId").val();
			
		window.location.href = url;
	}
	
	//Function to enable/disable and fill option in Selects for region select drop downs
    function dochange(src, val) {
		$.ajax({ type: "GET", 
				url: "/output/dropdownval/?geog="+src+"&id="+val,
				success: function(html) {                    
              		var flag = false;
					$(".select").each(function() {
						if(flag == true)
							$(this).val(-1).attr('disabled','disabled');
						if (this.name == src)
							flag = true;
					
					});
				   $("#"+src+"Id").html(html).removeAttr('disabled');                   
              }
         });
        }


});
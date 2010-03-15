function filter_person()
{	
		var counter = 0;
		var foo = [];
		var grps=new Array();
		$('#id_farmer_groups_targeted :selected').each(function(i, selected){
			foo[i] = $(selected).text();
			grps[i] = $(selected).val();
		});
		init_form = table.parent().parent('div.tabular').find("input[id$='INITIAL_FORMS']").val();
		
		$.ajax({ type: "GET", 
				dataType: 'json',
				url: "/feeds/persons/", 
				data:{groups:grps, init:init_form},
				success: function(obj){
							if(obj.html=='Error')
								return;
							if(obj.tot_val == '1')
								alert("Selected Group has no Person registered.");
							
							new_html = (obj.html).replace(/--prac_list--/g, obj.prac);
							table = $('div.inline-group div.tabular').find('table');
							
							if(init_form == 0)
						 		table.find('tbody').html(new_html);
						 	else {  
						 		table.find('tbody tr').each(function() {
						 			if($(this).is('.has_original')) {
								        $(this).prev('input').attr('checked', true);
	            						$(this).addClass('deleted_row').hide();
	            					}
	            					else
	            						$(this).remove()
							    });
							    table.find('tbody').append(new_html);
						 	}
						 	table.parent().parent('div.tabular').find("input[id$='TOTAL_FORMS']").val(obj.tot_val);
						 }
				 
			 });
		
		return;
}
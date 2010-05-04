// "Add"-link html code. Defaults to Django's "+" image icon, but could use text instead.
add_link_html = '<h2>Add New Row <img src = "/media/img/admin/icon_addlink.gif" width="10" height="10"></h2>';
// "Delete"-link html code. Defaults to Django's "x" image icon, but could use text instead.
delete_link_html = '<img src="/media/img/admin/icon_deletelink.gif" ' +
    'width="10" height="10" alt="Delete row" style="margin-top:0.5em" />';
position_field = 'position'; // Name of inline model field (integer) used for ordering. Defaults to "position".


//This is the HTML template used for "Add new Row" button
template = '<tr class="row1"> \
    <td class="delete"></td> \
	<td class="original"> \
		  <input type="hidden" id="id_personmeetingattendance_set-0-id" name="personmeetingattendance_set-0-id"> \
          <input type="hidden" id="id_personmeetingattendance_set-0-screening" name="personmeetingattendance_set-0-screening"> \
    </td> \
    <td class="person"> \
		<select id="id_personmeetingattendance_set-0-person" name="personmeetingattendance_set-0-person"> \
			<option selected="selected" value="">---------</option> \
			--per_list-- \
		</select> \
	</td> \
	<td class="expressed_interest_practice"> \
        <select id="id_personmeetingattendance_set-0-expressed_interest_practice" name="personmeetingattendance_set-0-expressed_interest_practice"> \
		<option selected="selected" value="">---------</option> \
		--prac_list-- \
		</select>\
	</td> \
    <td class="expressed_interest"> \
		<input type="text" maxlength="500" name="personmeetingattendance_set-0-expressed_interest" class="vTextField" id="id_personmeetingattendance_set-0-expressed_interest"> \
    </td> \
    <td class="expressed_adoption_practice"> \
        <select id="id_personmeetingattendance_set-0-expressed_adoption_practice" name="personmeetingattendance_set-0-expressed_adoption_practice"> \
			<option selected="selected" value="">---------</option> \
			--prac_list-- \
		</select> \
    </td> \
    <td class="expressed_adoption"> \
        <input type="text" maxlength="500" name="personmeetingattendance_set-0-expressed_adoption" class="vTextField" id="id_personmeetingattendance_set-0-expressed_adoption"> \
    </td> \
    <td class="expressed_question_practice"> \
        <select id="id_personmeetingattendance_set-0-expressed_question_practice" name="personmeetingattendance_set-0-expressed_question_practice"> \
			<option selected="selected" value="">---------</option> \
			--prac_list-- \
			</select> \
    </td> \
    <td class="expressed_question"> \
        <input type="text" maxlength="500" name="personmeetingattendance_set-0-expressed_question" class="vTextField" id="id_personmeetingattendance_set-0-expressed_question"> \
    </td> \
</tr>';

//To store the List of Practices. This is only set once on page load, and reused later(many times) when required
var _prac_list = '';

//This is the Template variable after replacing Prac_list and --per_list-- in Template variable. This is appended on clicking "Add new Row"
_new_template = '';

//is_edit: Flag if the page has village present on load
//is_inited: Flag if the page has been initialized once using init_add_screening() function
var is_edit,is_inited = false;


function  showStatus(msg){
	$('#screen').css({ opacity: 0.7, 'width':$(document).width(),'height':$(document).height(), 'display':'inline'});
	$('#box').css({'display': 'block'});
	if(msg != null)
		$('#box').html(msg);	
}

function hideStatus() {
	$('#box').css('display', 'none');
	$('#screen').css('display', 'none');
}

var screening_page = {
init :function() {
	alert('function is called');
	$('body').append('<div id="box"></div><div id="screen"></div>');
	$(window).resize(function(){
		$('#box').css("display") == 'block'?showStatus(null):"";
	});
	
	
	vil_id = $("#id_village").val()
	var pg_selected = $("#id_farmer_groups_targeted").val() || [];
	
	if(vil_id>0 && pg_selected>0) {
		showStatus("Intializing the page. Please wait.");
		alert('inside edit');
		//Case when village is already entered on page load
		is_edit = true;		
		var w  = window.location.href.split('/')
		var id = w[w.length-2]
		
		$.ajax({ type: "GET", 
				dataType: 'html',
				url: "/dashboard/getattendance/"+id+"/", 
				success: function(obj) {		
					$('div.inline-group div.tabular').html('')
					$('div.inline-group div.tabular').append(obj)
					
					$.ajax({ type: "GET", 
						dataType: 'json',
						url: "/feeds/person_pract/", 
						data:{vil_id:vil_id,mode:2},
						success: function(obj) {		
							//storing practice_list			
							template = (template).replace(/--prac_list--/g, obj.prac_list);
							_prac_list = obj.prac_list;
				
							//For "Add new Row" template, replacing ther person list of block of the village
							_new_template = (template).replace(/--per_list--/g, obj.per_list);			
							initialize_add_screening();
							hideStatus();
						}
					});
					
					$("#id_farmer_groups_targeted").attr('onchange', 'filter_person()');
				}
		});
		
	}
	else {
		alert('else');
		is_edit = false;
		$("#id_farmer_groups_targeted").attr('onchange', 'filter_person()');
	}
	
	
}
};


//Function to clear section of Person-Meeting-Attendance
function clear_table(tab) {

	//IF village was not selected on load, means that there aren't presaved rows
	if(!is_edit) {	
		if(tab.find('tbody').length > 0)
			tab.find('tbody').html('');
		return;
	}
	//If village was selected, it might be 'edit page'. For pre-selected persons, marks them for deletion and hide.
	//					Remove Other persons(newly added ones) 
	table.find('tbody tr:not(:hidden)').each(
		function(){
 			if($(this).is('.has_original')) { 			
		        $(this).find('td.delete input').attr('checked', true);
				$(this).addClass('deleted_row').hide();
			}
			else
				$(this).remove();
	});
	
}

//Function to perform some more initialized functions on load	
function initialize_add_screening() {
	if(is_inited)
		return;
	else
		is_inited = true;
	
	tabu = $('div.inline-group div.tabular');
	table = tabu.find('table');
	alert('here1');
	// Hide initial deleted rows
	table.find('td.delete input:checkbox:checked').parent('td').parent('tr').addClass('deleted_row').hide();
	
	// "Add"-button in bottom of inline for adding new rows
	tabu.find('fieldset').after('<a class="add" href="#">' + add_link_html + '</a>');
	alert('here2');
	tabu.find('a.add').click(function(){
	   table.append(_new_template);
    	
	   create_delete_button(table.find('tr:last td.delete'));                
	    
	    update_positions($(this).parent().find('table'), true);
	    
	    // Place for special code to re-enable javascript widgets after clone (e.g. an ajax-autocomplete field)
	    // Fictive example: new_item.find('.autocomplete').each(function() { $(this).triggerHandler('autocomplete'); });
	}).removeAttr('href').css('cursor', 'pointer');
	alert('here3');
	// "Delete"-buttons for each row that replaces the default checkbox 
	table.find('tr:not(.add_template) td.delete').each(
		function() {
		    create_delete_button($(this));
	});  
	alert('here4');
}

// Function for creating fancy delete buttons
function create_delete_button(td)
{
     // Replace checkbox with image
    td.find('input:checkbox').hide();
    td.append('<a class="delete" href="#">' + delete_link_html + '</a>');
    
    td.find('a.delete').click(function(){
        current_row = $(this).parent('td').parent('tr');
        table = current_row.parent().parent();
        if (current_row.is('.has_original')) // This row has already been saved once, so we must keep checkbox
        {
            $(this).prev('input').attr('checked', true);
            current_row.addClass('deleted_row').hide();
        }
        else // This row has never been saved so we can just remove the element completely
        {
            current_row.remove();
        }
        
        update_positions(table, true);
    }).removeAttr('href').css('cursor', 'pointer');
}

// Updates "position"-field values based on row order in table
function update_positions(table, update_ids)
{
    even = true
    num_rows = 0
    position = 0;

    // Set correct position: Filter through all trs, excluding first th tr and last hidden template tr
    table.find('tbody tr:not(.add_template):not(.deleted_row)').each(function() {
            // Update row coloring
            $(this).removeClass('row1 row2');
            if (even)
            {
                $(this).addClass('row1');
                even = false;
            }
            else
            {
                $(this).addClass('row2');
                even = true;
            }
       
    });
    
    table.find('tbody tr.has_original').each(function() {
        num_rows++;
    });
    
    table.find('tbody tr:not(.has_original):not(.add_template)').each(function() {
        if (update_ids) update_id_fields($(this), num_rows);
        num_rows++;
    });    
    
    table.find('tbody tr.add_template').each(function() {
        if (update_ids) update_id_fields($(this), num_rows)
        num_rows++;
    });

    table.parent().parent('div.tabular').find("input[id$='TOTAL_FORMS']").val(num_rows);
}

// Updates actual id and name attributes of inputs, selects and so on.
// Required for Django validation to keep row order.
function update_id_fields(row, new_position)
{
    // Fix IDs, names etc.
    
    // <select ...>
    row.find('select').each(function() {
        // id=...
        old_id = $(this).attr('id').toString();
        new_id = old_id.replace(/([^ ]+\-)[0-9]+(\-[^ ]+)/i, "$1" + new_position + "$2");
        $(this).attr('id', new_id)
        
        // name=...
        old_id = $(this).attr('name').toString();
        new_id = old_id.replace(/([^ ]+\-)[0-9]+(\-[^ ]+)/i, "$1" + new_position + "$2");
        $(this).attr('name', new_id)
    });
    
    // <input ...>
    row.find('input').each(function() {
        // id=...
        old_id = $(this).attr('id').toString();
        new_id = old_id.replace(/([^ ]+\-)[0-9]+(\-[^ ]+)/i, "$1" + new_position + "$2");
        $(this).attr('id', new_id)
        
        // name=...
        old_id = $(this).attr('name').toString();
        new_id = old_id.replace(/([^ ]+\-)[0-9]+(\-[^ ]+)/i, "$1" + new_position + "$2");
        $(this).attr('name', new_id)
    });
    
    // <a ...>
    row.find('a').each(function() {
        // id=...
        old_id = $(this).attr('id').toString();
        new_id = old_id.replace(/([^ ]+\-)[0-9]+(\-[^ ]+)/i, "$1" + new_position + "$2");
        $(this).attr('id', new_id)
    });
    
    // Are there other element types...? Add here.
}

//Function called on Person Selection
function filter_person() {	
	showStatus("Loading persons..");
	//Get the Value of 'Initial-forms' and Person Group selected.
	grps = $('#id_farmer_groups_targeted').val();
	tabu = $('div.inline-group div.tabular');
	table = tabu.find('table');
	init_form = table.parent().parent('div.tabular').find("input[id$='INITIAL_FORMS']").val();
	
	$.ajax({ type: "GET", 
		dataType: 'json',
		url: "/get/person/", 
		data:{groups:grps,},
		success: function(obj) {		
			//For "Add new Row" template, replacing ther person list of block of the village
			template = (template).replace(/--per_list--/g, obj.per_list);			
			initialize_add_screening();
		}
	});	
	
	$.ajax({ type: "GET", 
		dataType: 'json',
		url: "/feeds/persons/", 
		data:{groups:grps, init:init_form,mode:1},
		success: function(obj){
				if(obj.html=='Error') {
					alert('Sorry, some error Occured. Please notify Systems Team.');
					return;
				}
					
				//Case when No Person is present in the person groups.
				if(obj.tot_val == init_form) {
					alert("Selected Group has no Person registered.");
					clear_table(table);
					table.parent().parent('div.tabular').find("input[id$='TOTAL_FORMS']").val(obj.tot_val);
					hideStatus();
					return;
				}
						
				//Create & append the list of persons 
				_new_template = (template).replace(/--prac_list--/g, obj.prac);
				_prac_list = obj.prac;
				
				new_html = (obj.html).replace(/--prac_list--/g, _prac_list);
				table = $('div.inline-group div.tabular').find('table');						
				clear_table(table);
			    table.append(new_html);			
			  	//Set Total forms
			 	table.parent().parent('div.tabular').find("input[id$='TOTAL_FORMS']").val(obj.tot_val);
			 	hideStatus();
		}
	});
}

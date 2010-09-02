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
var app_status;

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

var screening_page_offline = {
init :function(id) {
	is_inited = false;
	$('body').append('<div id="box"></div><div id="screen"></div>');
	$(window).resize(function(){
		$('#box').css("display") == 'block'?showStatus(null):"";
	});
	try {
			var db = google.gears.factory.create('beta.database');
			db.open('digitalgreendatabase');
			var rs = db.execute('select u.app_status from user u');
			if(rs.field(0) == 0 ) {
				app_status = 0
				// Offline case
			}
			else if (rs.field(0) == 1) {
				app_status = 1
				// Online case
			}
			rs.close();
			db.close();
	}
	catch(err) {
			// If an exception is caught, assume online case
			app_status = 1;
			db.close();
	}

	// Edit case
	if(parseFloat(id) > 0) {
		// Edit Online case
		is_edit = true;	
		if (app_status == 1){						
			vil_id = $("#id_village").val()
			var pg_selected = $("#id_farmer_groups_targeted").val() || [];
		
			if(vil_id>0 && pg_selected.length >0) {
			//Case when village is already entered on page load
				showStatus("Intializing the page. Please wait.");
			
				// Get the person meeting attendance data, requires the screening id.
				$.ajax({ type: "GET", 
					dataType: 'html',
					url: "/dashboard/getattendance/"+id+"/", 
					success: function(obj) {		
						$('div.inline-group div.tabular').html('')
						$('div.inline-group div.tabular').append(obj)
					
						// Set the practice and person list for the "add new row"
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
					}
				});
			}
		}
		else if (app_status ==0){
			// Code for offline edit case
			// 1) Retrive the rows of person meeting attendance
			// 2) Retrive the person and practice fields from the local database 
			// 3) Add new row template to the html
				showStatus("Intializing the page. Please wait.");
				$("#id_farmer_groups_targeted").attr('disabled', 'true');
				$("#save").hide();
				$('<span style="color:Red">Editing of screening data is not allowed while you are offline</span>').insertBefore("#content-main");
				var db = google.gears.factory.create('beta.database');
				db.open('digitalgreendatabase');
				
				var table = $('div.inline-group div.tabular').find('table');						
				table.append('<tbody></tbody>');
				
				var person_meeting_attendance = db.execute("SELECT pma.id, pma.screening_id, p.id, p.person_name, "+
										"pma.expressed_interest_practice_id, p1.practice_name, pma.expressed_interest, "+
										"pma.expressed_adoption_practice_id, p2.practice_name, pma.expressed_adoption, "+
										"pma.expressed_question_practice_id, p3.practice_name, pma.expressed_question "+
										"FROM person_meeting_attendance pma "+
										"LEFT JOIN practices p1 ON (pma.expressed_interest_practice_id = p1.id ) "+
										"LEFT JOIN practices p2 ON (pma.expressed_adoption_practice_id = p2.id ) "+
										"LEFT JOIN practices p3 ON (pma.expressed_question_practice_id = p3.id ) "+
										"JOIN person p ON pma.person_id = p.id "+
										"WHERE pma.screening_id="+id);
				
				var i = 0;
				var row_class;
				var tot_form = 0;
				while(person_meeting_attendance.isValidRow()){
					if(i%2==0) {
						row_class = "row1";
					}
					else {
						row_class = "row2";
					}
					html =	"<tr class="+row_class+">"+
								"<td class='delete'> Delete not allowed </td>"+
								"<td class='original'> "+
									"<input type='hidden' id='id_personmeetingattendance_set-"+i+"-id' name='personmeetingattendance_set-'+i+'-id' value='"+person_meeting_attendance.field(0)+"'> "+
									"<input type='hidden' id='id_personmeetingattendance_set-"+i+"-screening' name='personmeetingattendance_set-'+i+'-screening' value='"+person_meeting_attendance.field(1)+"'> "+
								"</td>"+
								
								"<td class='person'>"+
									"<select id='id_personmeetingattendance_set-"+i+"-person' name='personmeetingattendance_set-"+i+"-person'> "+
										"<option selected='selected' value='"+person_meeting_attendance.field(2)+"'>"+person_meeting_attendance.field(3)+"</option> "+
									"</select>"+
								"</td>"+
								
								"<td class='expressed_interest_practice'>"+
									"<select id='id_personmeetingattendance_set-"+i+"-expressed_interest_practice' name='personmeetingattendance_set-"+i+"-expressed_interest_practice'>";
								
					if(person_meeting_attendance.field(4))
						html += "<option selected='selected' value='"+person_meeting_attendance.field(4)+"'>"+ person_meeting_attendance.field(5) +"</option> ";
					else
						html += "<option selected='selected' value=''>---------</option>";
								
					html +=	"</select>"+
								"</td> "+
								"<td class='expressed_interest'> ";
								
					if(person_meeting_attendance.field(6))
						html += "<input type='text' maxlength='500' name='personmeetingattendance_set-"+i+"-expressed_interest' class='vTextField' id='id_personmeetingattendance_set-"+i+"-expressed_interest' value='"+person_meeting_attendance.field(6)+"'>";
					else
						html += "<input type='text' maxlength='500' name='personmeetingattendance_set-"+i+"-expressed_interest' class='vTextField' id='id_personmeetingattendance_set-"+i+"-expressed_interest' value=''>";
								
					html += "</td> "+
							"<td class='expressed_adoption_practice'> "+
								"<select id='id_personmeetingattendance_set-"+i+"-expressed_adoption_practice' name='personmeetingattendance_set-"+i+"-expressed_adoption_practice'> ";
					
					if(person_meeting_attendance.field(7))
						html += "<option selected='selected' value='"+person_meeting_attendance.field(7)+"'>"+person_meeting_attendance.field(8)+"</option>";
					else
						html += "<option selected='selected' value=''>---------</option>";
									
					html += "</select> "+
								"</td> "+
								"<td class='expressed_adoption'> ";
								
					if(person_meeting_attendance.field(9))
						html += "<input type='text' maxlength='500' name='personmeetingattendance_set-"+i+"-expressed_adoption' class='vTextField' id='id_personmeetingattendance_set-"+i+"-expressed_adoption' value='"+person_meeting_attendance.field(9)+"'> ";
					else
						html += "<input type='text' maxlength='500' name='personmeetingattendance_set-"+i+"-expressed_interest' class='vTextField' id='id_personmeetingattendance_set-"+i+"-expressed_interest' value=''>";
								
					html += "</td>"+
								"<td class='expressed_question_practice'> "+
									"<select id='id_personmeetingattendance_set-"+i+"-expressed_question_practice' name='personmeetingattendance_set-"+i+"-expressed_question_practice'>";
					
					if(person_meeting_attendance.field(10))
						html += "<option selected='selected' value='"+person_meeting_attendance.field(10)+"'>"+person_meeting_attendance.field(11)+"</option> ";
					else
						html += "<option selected='selected' value=''>---------</option>";
						
					html += "</select> "+
								"</td> "+
								"<td class='expressed_question'> ";
								
					if(person_meeting_attendance.field(12))
						html += "<input type='text' maxlength='500' name='personmeetingattendance_set-"+i+"-expressed_question' class='vTextField' id='id_personmeetingattendance_set-"+i+"-expressed_question' value='"+person_meeting_attendance.field(12)+"'> ";
					else
						html += "<input type='text' maxlength='500' name='personmeetingattendance_set-"+i+"-expressed_interest' class='vTextField' id='id_personmeetingattendance_set-"+i+"-expressed_interest' value=''>";
										
					html += "</td > "+
							"</tr>";
							
					table.find('tbody').append(html);
					tot_form += 1;
					i +=1;
					person_meeting_attendance.next();
				}
				table.parent().parent('div.tabular').find("input[id$='TOTAL_FORMS']").val(tot_form);
				person_meeting_attendance.close();
				db.close();
				hideStatus();
				
		}
	} // Add case 
	else {
		is_edit = false;
		var pg_selected = $("#id_farmer_groups_targeted").val() || [];
		
		// Case, when the add form has some validation error and the person group is selected.
		if(pg_selected.length >0) {
			filter_person()
		}
		
		if(app_status==0) {
			var table = $('div.inline-group div.tabular').find('table');						
			table.append('<tbody></tbody>');
		}
	}

	$("#id_farmer_groups_targeted").change(function(){filter_person()});
	
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
	// Hide initial deleted rows
	table.find('td.delete input:checkbox:checked').parent('td').parent('tr').addClass('deleted_row').hide();
	// "Add"-button in bottom of inline for adding new rows
	tabu.find('fieldset').after('<a class="add" href="#">' + add_link_html + '</a>');
	tabu.find('a.add').click(function(){
	   table.append(_new_template);
    	
	   create_delete_button(table.find('tr:last td.delete'));                
	    
	    update_positions($(this).parent().find('table'), true);
	    
	    // Place for special code to re-enable javascript widgets after clone (e.g. an ajax-autocomplete field)
	    // Fictive example: new_item.find('.autocomplete').each(function() { $(this).triggerHandler('autocomplete'); });
	}).removeAttr('href').css('cursor', 'pointer');
	// "Delete"-buttons for each row that replaces the default checkbox 
	table.find('tr:not(.add_template) td.delete').each(
		function() {
		    create_delete_button($(this));
	});  
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

//Function called on Person Group Selection
function filter_person() {
	if(is_inited || !is_edit) {
	var grps = $("#id_farmer_groups_targeted").val() || [];
	if( grps.length > 0) {
		if(app_status == 0 ) {
			showStatus("Loading persons..");	
			var table = $('div.inline-group div.tabular').find('table');			
			var db = google.gears.factory.create('beta.database');
			db.open('digitalgreendatabase');
			var prac = db.execute("SELECT P.id , P.PRACTICE_NAME FROM PRACTICES P ORDER BY P.PRACTICE_NAME");
			var prac_options = [];
			while(prac.isValidRow()) {
				prac_options.push('<option value="'+prac.field(0)+'">'+prac.field(1)+'</option>');
				prac.next();
			}
			// Add practice to add new row template
			template = (template).replace(/--prac_list--/g, prac_options.join('\n'));
			var persons_list_for_add_new_row = db.execute("SELECT P.id, P.person_name, V.village_name FROM PERSON P JOIN VILLAGE V on P.village_id = V.id ORDER BY P.person_name");
			var person_options = [];
			while(persons_list_for_add_new_row.isValidRow()) {
				person_options.push('<option value="'+persons_list_for_add_new_row.field(0)+'">'+persons_list_for_add_new_row.field(1) +'(' + persons_list_for_add_new_row.field(2) + ')'+'</option>');
				persons_list_for_add_new_row.next();
			}	
			// Add person to add new row template 
			_new_template = (template).replace(/--per_list--/g, person_options.join('\n'));
			// Add "add new row" button
			initialize_add_screening();
			//alert('before sql execute');
			var persons = db.execute("SELECT DISTINCT P.id, P.person_name FROM PERSON P where P.group_id in ("+grps.join(", ")+")");	
			var tot_form = 0;
			var row ='';
			while (persons.isValidRow()) {
				var per = '<option value="'+persons.field(0)+'" selected="true">'+persons.field(1)+'</option>'
				//var row = (off_template).replace(/--per_list--/g, per);
				row = row  + (template).replace(/--per_list--/g, per);
				//table.find('tbody').append(row);
				tot_form += 1;
				persons.next();
			}	
			clear_table(table);
			table.find('tbody').append(row);
			table.find('tr:not(.add_template) td.delete').each(
			function() {
				create_delete_button($(this));
			});
			update_positions(table, true);
			table.parent().parent('div.tabular').find("input[id$='TOTAL_FORMS']").val(tot_form);
			prac.close();
			persons.close();
			db.close();
			hideStatus();
		}	
		else {
			// Online case
			showStatus("Loading persons..");
			//Get the Value of 'Initial-forms' and Person Group selected.
			grps = $('#id_farmer_groups_targeted').val();
			tabu = $('div.inline-group div.tabular');
			table = tabu.find('table');
			init_form = table.parent().parent('div.tabular').find("input[id$='INITIAL_FORMS']").val();
	
			// Get all the person of the block to which the group belongs.
			// This person list will be used for "add-new row" template
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
	
			// Get the list of the person belonging to the selected person group
			// Also get the list of the practices for "add new row" template
			$.ajax({ type: "GET", 
				dataType: 'json',
				url: "/feeds/persons/modified/", 
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
	}
	}
	
}


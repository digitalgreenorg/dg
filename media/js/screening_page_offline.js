// "Add"-link html code. Defaults to Django's "+" image icon, but could use text instead.
add_link_html = '<h2>Add New Row <img src = "/media/img/admin/icon_addlink.gif" width="10" height="10"></h2>';
// "Delete"-link html code. Defaults to Django's "x" image icon, but could use text instead.
delete_link_html = '<img src="/media/img/admin/icon_deletelink.gif" ' +
    'width="10" height="10" alt="Delete row" style="margin-top:0.5em" />';
position_field = 'position'; // Name of inline model field (integer) used for ordering. Defaults to "position".

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
	
	if (!window.google || !google.gears) {
		app_status = 1;
	}
	else {
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
	}
	
	// Edit case
	if(parseFloat(id) > 0) {
		// Edit Online case

		is_edit = true;						
		var pg_selected = $("#id_farmer_groups_targeted").val() || [];
        
        if (app_status == 1) {
                var village = $("#id_village").val() || [];
                setup_add_new_row(village, function(data){
                    _new_template = ich.row_template(data);
                });
        }
        
		if(pg_selected.length >0) {
        
            //Case when village is already entered on page load
            showStatus("Intializing the page. Please wait.");
        
            
            
            var table = $('div.inline-group div.tabular').find('table');
            table.append('<tbody  class="row_zebra"></tbody>');
            
            get_persons_for_screening(id, function(person_list){
                clear_table(table);
                for (index in person_list) {
                    get_pma(person_list[index], id, table, function(data){
                        add_attendance_form(data, table);
                    });
                }
            });
            
            update_positions(table, true);
            
            if (app_status == 0) {
                $("#id_farmer_groups_targeted").attr('disabled', 'true');
    			$("#save").hide();
    			$('<span style="color:Red">Editing of screening data is not allowed while you are offline</span>').insertBefore("#content-main");
            }
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

	$("#id_farmer_groups_targeted").change(function(){filter_person();});
	$("#id_village").change(function(){filter_by_village();});
	
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
	tab.find('tbody tr:not(:hidden)').each(
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
	   table.append(_new_template.clone())
    	
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

function filter_by_village(){
    if(is_inited || !is_edit) {
        var village = $('#id_village').val() || [];
        if (village.length > 0) {
            showStatus("Updating...");
            console.log("Village " + village)
            get_filtered_data_for_village(village, function (data){
                update_filtered_data_for_village(data);
                hideStatus();
            });
        }
    }
}

//Function called on Person Group Selection
function filter_person() {
	if(is_inited || !is_edit) {
        var grps = $("#id_farmer_groups_targeted").val() || [];
        if( grps.length > 0) {
            
            showStatus("Loading persons...");
            
            var village = $("#id_village").val() || [];
            setup_add_new_row(village, function(data){
                _new_template = ich.row_template(data);
            });
            
            var table = $('div.inline-group div.tabular').find('table'); 
            get_persons_for_group(grps, function(person_list){
                clear_table(table);
                for (index in person_list) {
                    get_attendance_form_for_person(person_list[index], table, function(data){
                        add_attendance_form(data, table);
                    });
                }
            });
            
            update_positions(table, true);
            hideStatus();
        }
    }
}

function add_attendance_form(data,table){
    var new_row = ich.row_template(data);
    table.append(new_row);
    initialize_add_screening();
    update_positions(table, true);
}

function update_filtered_data_for_village(data) {
    var op = Object;
    op.option_list = data.animators;
    var anim_options = ich.options_template(op);
    $("#id_animator").html(anim_options);
    op.option_list = data.groups;
    var group_options = ich.multioptions_template(op);
    $("#id_farmer_groups_targeted").html(group_options);
}

$(document).ready(function() {
    $.ajaxSettings.traditional = true;
    $('.delete_row').removeAttr('href').css('cursor', 'pointer');
    $('.delete_row').live('click', function() {
        var current_row = $(this).parent('tr');
        var table = current_row.parent().parent();
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
    });
    
});

function select_options(option, empty_option)
{
    var select_option_list = '';
    var empty_option_str = '<option selected=\'selected\' value=\'\'>---------</option>';
    if (empty_option == true) {
        select_option_list= empty_option_str;
    }
    for (index in option) {
        var string = option[index][1];
        var value = option[index][0];
        var option_string = '<option value=\''+value+'\' selected=\'true\'>'+string+'</option>';
        select_option_list = select_option_list + option_string;
    }
    return select_option_list;
}

function setup_add_new_row (village, callbackfn) {
    
    if (app_status == 1) {
        $.ajax({
    	    type: "GET",
    	    dataType: 'json',
    	    url: "/dashboard/screeningsinvillage/"+village+"/",
    	    success: function(data){
    	       callbackfn(data);
    	    }
    	});
	}
	else {
	    var db = google.gears.factory.create('beta.database');
    	db.open('digitalgreendatabase');
    	
    	var persons_list_for_add_new_row = db.execute("SELECT P.id, P.person_name, P.father_name, V.village_name FROM PERSON P JOIN VILLAGE V on P.village_id = V.id WHERE V.id='"+village+"' ORDER BY P.person_name");
    	var person_options = [];
    	while(persons_list_for_add_new_row.isValidRow()) {
    		if(persons_list_for_add_new_row.field(2) == null || persons_list_for_add_new_row.field(2).toString() == '') {
    			person_options.push({'value': persons_list_for_add_new_row.field(0),'string': persons_list_for_add_new_row.field(1) +' (' + persons_list_for_add_new_row.field(3) + ')'});
    		}
    		else {
    			person_options.push({'value': persons_list_for_add_new_row.field(0), 'string': persons_list_for_add_new_row.field(1) +' (' + persons_list_for_add_new_row.field(2) + ')'+' (' + persons_list_for_add_new_row.field(3) + ')'});
    		}
    		persons_list_for_add_new_row.next();
    	}
    	
    	var prac = db.execute("select distinct practices.id, practices.practice_name as practices from practices, VIDEO_related_agricultural_practices, screening_videos_screened, screening where practices.id=VIDEO_related_agricultural_practices.practices_id and VIDEO_related_agricultural_practices.video_id=screening_videos_screened.video_id and screening_videos_screened.screening_id=screening.id and screening.village_id LIKE '"+village+"'");
    	var practice_options = [];
    	while(prac.isValidRow()) {
    		practice_options.push({'value':prac.field(0), 'string':prac.field(1)});
    		prac.next();
    	}

    	data = {
    	    'practice_list': practice_options,
    	    'person_list': person_options
    	};
    	
    	callbackfn(data);
    	
    	prac.close();
    	persons_list_for_add_new_row.close();
    	db.close();
	}
}

function get_persons_for_screening (screening_id, callbackfn) {
    if (app_status == 1) {
        $.ajax({
            type: "GET",
            dataType: 'json',
            url: "/dashboard/personsinscreening/" + screening_id + "/",
            success: function(person_list){
                callbackfn(person_list);
            }
        });
    }
    else {
        var db = google.gears.factory.create('beta.database');
        db.open('digitalgreendatabase');
        var persons = db.execute("select person_id from person_meeting_attendance where screening_id="+screening_id);
        var person_list = [];
        while (persons.isValidRow()) {
          person_list.push(persons.field(0));
          persons.next();
        }
        callbackfn(person_list);
        persons.close();
        db.close();
    }
}

function get_pma(person_id, screening_id, table, callbackfn) {
    if (app_status == 1) {
        $.ajax({
            type: 'GET',
            dataType: 'json',
            url: "/dashboard/personmeetingattendance/" + person_id + "/" + screening_id + "/",
            success: function(data){
                callbackfn(data, table);
            }
        });
    }
    else {
        var db = google.gears.factory.create('beta.database');
        db.open('digitalgreendatabase');
        
        var practice_list = [];
        var practice_rs = db.execute("select distinct practices.id, practices.practice_name as practices from practices, VIDEO_related_agricultural_practices, screening_videos_screened, screening, person_meeting_attendance where practices.id=VIDEO_related_agricultural_practices.practices_id and VIDEO_related_agricultural_practices.video_id=screening_videos_screened.video_id and screening_videos_screened.screening_id=screening.id and screening.id=person_meeting_attendance.screening_id and person_meeting_attendance.person_id LIKE '"+ person_id + "'");
        while (practice_rs.isValidRow()){
            practice_list.push({'value': practice_rs.field(0), 'string':practice_rs.field(1) });
            practice_rs.next();
        }
        practice_rs.close();
        var query_str = "SELECT pma.id, pma.screening_id, p.id, p.person_name, "+
                                "pma.expressed_question, "+
        						"pma.expressed_adoption_practice_id, p2.practice_name, "+
        						"pma.interested " +
        						"FROM person_meeting_attendance pma "+
        						"LEFT JOIN practices p2 ON (pma.expressed_adoption_practice_id = p2.id ) "+
        						"JOIN person p ON pma.person_id = p.id "+
        						"WHERE pma.screening_id="+screening_id+ " " + 
        						"AND pma.person_id="+person_id;
        console.log(query_str);
        var pma = db.execute(query_str);
        var data = new Object;
        try {
             // This should yield exactly one row.
                if (pma.isValidRow()) {
                    data['person_list'] = [{'value': pma.field(2), 'string': pma.field(3)}];
                    data['expressed_question_comment'] = pma.field(4);
                    data['practice_list'] = practice_list;
                    data['interested'] = true;
                    if (pma.field(7)==0) {
                        data['interested'] = false;
                    }
                    if(pma.field(5) != null && pma.field(5).toString() != '') {
                        data['selected_expressed_adoption_practice'] = {'value': pma.field(5), 'string': pma.field(6)};
                    }
                }
                callbackfn(data,table);
                pma.close();
                db.close();
        }
        catch (error) {
            console.log(error);
        }
    }
}


function get_persons_for_group(grps, callbackfn) {
	if (app_status == 1) {
		$.ajax({
			type: "GET",
			dataType: 'json',
			url: "/dashboard/personsingroup/", 
			data:{groups:grps},
			success: function(data){
                callbackfn(data);
			}
        });
	}
	else {
        var db = google.gears.factory.create('beta.database');
        db.open('digitalgreendatabase');
        
        var persons = db.execute("SELECT P.id FROM PERSON P where P.group_id in ("+grps.join(", ")+")");
        var person_list = [];
        while (persons.isValidRow()) {
          person_list.push(persons.field(0));
          persons.next();
        }
        callbackfn(person_list);
        persons.close();
        db.close();
	}
}

function get_filtered_data_for_village (village_id, callbackfn) {
    if (app_status == 1) {
        $.ajax({
            type:'GET',
            dataType: 'json',
            url:"/dashboard/filtereddataforvillage/"+village_id+"/",
            success:function(data){
                callbackfn(data);
            }
        });
    }
    else {
        
    }
}

function get_attendance_form_for_person (person_id, table, callbackfn) {
    if (app_status == 1) {
        $.ajax({
            type:'GET',
            dataType: 'json',
            url:"/dashboard/practicesforperson/"+person_id+"/",
            success:function(data){
                callbackfn(data, table);
            }
        });
    }
    else {
        var db = google.gears.factory.create('beta.database');
        db.open('digitalgreendatabase');
        
        var person_list = [];
        var rsCount = 0;

        var person_rs = db.execute("SELECT DISTINCT P.id, P.person_name, P.father_name, V.village_name FROM PERSON P JOIN VILLAGE V on P.village_id = V.id where P.id LIKE '"+person_id+"'");
        while (person_rs.isValidRow()){
            if(person_rs.field(2) == null || person_rs.field(2).toString() == '') {
                person_list.push({'value': person_rs.field(0), 'string':person_rs.field(1) +' (' + person_rs.field(3) + ')' });
            }
            else {
                person_list.push({'value': person_rs.field(0) , 'string': person_rs.field(1) +' (' + person_rs.field(2) + ')'});
            }
            person_rs.next();
            rsCount++;
        }
        person_rs.close();
        if ((rsCount > 1)||(rsCount == 0)) {
            console.log("How exactly?");
        }
        
        var practice_list = [];
        var practice_rs = db.execute("select distinct practices.id, practices.practice_name as practices from practices, VIDEO_related_agricultural_practices, screening_videos_screened, screening, person_meeting_attendance where practices.id=VIDEO_related_agricultural_practices.practices_id and VIDEO_related_agricultural_practices.video_id=screening_videos_screened.video_id and screening_videos_screened.screening_id=screening.id and screening.id=person_meeting_attendance.screening_id and person_meeting_attendance.person_id LIKE '"+ person_id + "'");
        while (practice_rs.isValidRow()){
            practice_list.push({'value': practice_rs.field(0), 'string':practice_rs.field(1) });
            practice_rs.next();
        }
        
        data = {
            'person_list': person_list,
            'practice_list': practice_list
        };
        callbackfn(data, table);
        
        person_rs.close();
        practice_rs.close();
        db.close();
    }
}

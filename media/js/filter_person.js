add_link_html = '<h2>Add New Row <img width="10" height="10" src="/media/img/admin/icon_addlink.gif"/></h2>';
// "Delete"-link html code. Defaults to Django's "x" image icon, but could use text instead.
delete_link_html = '<img src="/media/img/admin/icon_deletelink.gif" ' +
    'width="10" height="10" alt="Delete row" style="margin-top:0.5em" />';
position_field = 'position'; // Name of inline model field (integer) used for ordering. Defaults to "position".


function filter_person()
{	
		var counter = 0;
		var foo = [];
		$('#id_farmer_groups_targeted :selected').each(function(i, selected){
			foo[i] = $(selected).text();
			temp = $(selected).val();
			t_body = $('div.inline-group div.tabular').find('table tbody');
			t_body.find('tr:gt(0)').remove();
			$.getJSON("/feeds/persons/"+$(selected).val()+"/", function(j)
                	{
                        	var options;
	                        for (var i = 0; i < j.length; i++)
	                        {
				  add_row();
	                          options = '<option value="' + parseInt(j[i].pk) + '">' + j[i].fields['person_name'] + '</option>';
	                          $("#id_personmeetingattendance_set-"+counter+"-person").html(options);
                                  $("#id_personmeetingattendance_set-"+counter+"-person option:first").attr('selected', 'selected');
                                  $("#id_personmeetingattendance_set-"+counter+"-person").attr('disabled', false);
			          counter++;
	                        }
        	        })

		});

}

function add_row()
{
	old_item = $('div.inline-group div.tabular').find('table tr.add_template')
        new_item = old_item.clone(true);



        create_delete_button(new_item.find('td.delete'));
        new_item.removeClass('add_template').show();

        $('div.inline-group div.tabular').find('table').append(new_item);

        update_positions($('div.inline-group div.tabular').find('table'), true);
}


function delete_row()
{
	old_item = $('div.inline-group div.tabular').find('table tr.add_template')
        new_item = old_item.clone(true);
        //current_row = new_item.find('a.delete').parent('td').parent('tr');
	current_row = $('div.inline-group div.tabular').find('table tr:last')
        table = current_row.parent().parent();
        if (current_row.is('.has_original')) // This row has already been saved once, so we must keep checkbox
        {
            current_row.find('a.delete').prev('input').attr('checked', true);
            current_row.addClass('deleted_row').hide();
        }
        else // This row has never been saved so we can just remove the element completely
        {
            current_row.remove();
        }

        update_positions(table, true);


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
        if (position_field != '')
        {
            // Update position field
            $(this).find('td.' + position_field + ' input').val(position + 1);
            position++;
        }
        else
        {
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


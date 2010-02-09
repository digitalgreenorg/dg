package com.digitalgreen.dashboardgwt.client;

public class Regions {
	
	final static String REGION_CONTENT_TITLE = "<h1>Add region</h1>";
	
	final static String REGION_CONTENT_HTML = "<div>" +
			"<fieldset class='module aligned '>" +
			"<div class='form-row region_name  '>" +
			"<div>" +
			"<label for='id_region_name' class='required'>Region name:</label><input id='id_region_name' type='text' class='vTextField' name='region_name' maxlength='100' />" +
			"</div>" +
			"</div>" +
			"<div class='form-row start_date'>" +
			"<div><label for='id_start_date'>Start date:</label><input id='id_start_date' type='text' class='vDateField' name='start_date' size='10' />" +
			"</div>" +
			"</div>"+
			"</fieldset>" +
			"</div>";

	final static String REGION_LISTING_TITLE = "<h1>Select region to change</h1>";
	
	final static String REGION_LISTING_DIV = "<ul class='object-tools'>"+
											 "<li>" + 
											 "<a href='/dashboard/region/add/' class='addlink'> Add region </a>"+
											 "</li>"+
											 "</ul>" +
											 "<div class='module' id='changelist'></div>";
	
	final static String REGION_LISTING_HTML = "<div class='actions'>"+
							"<label>Action: <select name='action'>"+
							"<option value='' selected='selected'>---------</option>"+
							"<option value='delete_selected'>Delete selected regions</option>"+
							"</select></label>"+
							"<button type='submit' class='button' title='Run the selected action' name='index' value='0'>Go</button>"+
							"</div>"+
							"<table cellspacing='0'>"+
							"<thead>"+
							"<tr>"+
							"<th>"+
							"<input style='display: inline;' type='checkbox' id='action-toggle' />"+
							"</th><th>"+
							"Region"+
							"</th>"+
							"</tr>"+
							"</thead>"+
							"<tbody>";


	}
package com.digitalgreen.dashboardgwt.client.templates;

public class DevelopmentManagersTemplate {

	final static private String dmListFormHtml = "<div class='actions'>" +
								"<label>Action: <select name='action'>" +
									"<option value='' selected='selected'>---------</option>" +
									"<option value='delete_selected'>Delete selected development managers</option>" +
									"</select>" +
								"</label>" +
								"<button type='submit' class='button' title='Run the selected action' name='index' value='0'>Go</button>" +
								"</div>" +
								"<table cellspacing='0'>" +
									"<thead>" +
										"<tr>" +
											"<th>" +
												"<input type='checkbox' id='action-toggle' />" +
											"</th>" +
											"<th>" +
												"<a href='?ot=asc&amp;o=1'>" +
												"Name" +
												"</a>" +
											"</th>" +
											"<th>" +
												"<a href='?ot=asc&amp;o=2'>" +
												"Region" +
												"</a>" +
											"</th>" +
										"</tr>" +
									"</thead>" +
									"<tbody>" +
										"<div id='data-rows'" +       // Insert data rows here
										"</div>" +
									"</tbody>" +
								"</table>";

	final static private String dmListHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
							"<div id='content' class='flex'>" +
								"<h1>Select Development Manager to change</h1>" +
								"<div id='content-main'>" +
									"<ul class='object-tools'>" +
										"<li id='add-link'>" +                // Insert add link here
										"</li>" +
									"</ul>" +
									"<div class='module' id='changelist'>" +
										"<form action='' method='post'>" +
											"<div id='listing-form-body'>" +  // Insert form data here
											"</div>" +
										"</form>" +
									"</div>" +
								"</div>" +
							"</div>";
	
	final static private String dmAddHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
							"<div id='content' class='colM'>" +
								"<h1>Add Development Manager</h1>" +
								"<div id='content-main'>" +
									"<form enctype='multipart/form-data' action='' method='post' id='developmentmanager_form'>" +
										"<div>" +
											"<fieldset class='module aligned '>" +
												"<div class='form-row name  '>" +
													"<div>" +
														"<label for='id_name' class='required'>Name:</label><input id='id_name' type='text' class='vTextField' name='name' maxlength='100' />" +
													"</div>" +
												"</div>" +
												"<div class='form-row age  '>" +
													"<div>" +
														"<label for='id_age'>Age:</label><input id='id_age' type='text' class='vIntegerField' name='age' />" +
													"</div>" +
												"</div>" +
												"<div class='form-row gender  '>" +
													"<div>" +
														"<label for='id_gender' class='required'>Gender:</label><select name='gender' id='id_gender'>" +
															"<option value='' selected='selected'>---------</option>" +
															"<option value='M'>Male</option>" +
															"<option value='F'>Female</option>" +
														"</select>" +
													"</div>" +
												"</div>" +
												"<div class='form-row hire_date  '>" +
													"<div>" +
														"<label for='id_hire_date'>Hire date:</label><input id='id_hire_date' type='text' class='vDateField' name='hire_date' size='10' />" +
													"</div>" +
												"</div>" +
												"<div class='form-row phone_no  '>" +
													"<div>" +
														"<label for='id_phone_no'>Phone no:</label><input id='id_phone_no' type='text' class='vTextField' name='phone_no' maxlength='100' />" +
													"</div>" +
												"</div>" +
												"<div class='form-row address  '>" +
													"<div>" +
														"<label for='id_address'>Address:</label><input id='id_address' type='text' class='vTextField' name='address' maxlength='500' />" +
													"</div>" +
												"</div>" +
												"<div class='form-row speciality  '>" +
													"<div>" +
														"<label for='id_speciality'>Speciality:</label><textarea id='id_speciality' rows='10' cols='40' name='speciality' class='vLargeTextField'></textarea>" +
													"</div>" +
												"</div>" +
												"<div class='form-row region  '>" +
													"<div>" +
														"<label for='id_region' class='required'>Region:</label><select name='region' id='id_region'>" +
															"<option value='' selected='selected'>---------</option>" +
															"</select><a href='/admin/dashboard/region/add/' class='add-another' id='add_id_region' onclick='return showAddAnotherPopup(this);'> <img src='/media/img/admin/icon_addlink.gif' width='10' height='10' alt='Add Another'/></a>" +
													"</div>" +
												"</div>" +
												"<div class='form-row start_day  '>" +
													"<div>" +
														"<label for='id_start_day'>Start day:</label><input id='id_start_day' type='text' class='vDateField' name='start_day' size='10' />" +
													"</div>" +
												"</div>" +
											"</fieldset>" +
											"<div class='submit-row' >" +
												"<input type='submit' value='Save' class='default' name='_save' />" +
												"<input id='save_a' type='submit' value='Save and add another' name='_addanother'/>" +
												"<input id='save_c' type='submit' value='Save and continue editing' name='_continue' />" +
											"</div>" +
												"<script type='text/javascript'>document.getElementById('id_name').focus();</script>" +
												"<script type='text/javascript'>" +
												"</script>" +
										"</div>" +
									"</form>" +
								"</div>" +
							"</div>";	
}

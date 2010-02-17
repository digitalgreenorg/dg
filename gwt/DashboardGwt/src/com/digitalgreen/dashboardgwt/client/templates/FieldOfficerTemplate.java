package com.digitalgreen.dashboardgwt.client.templates;

public class FieldOfficerTemplate {

	final static private String fieldofficerListFormHtml = "<div class='actions'>" +
								"<label>Action: <select name='action'>" +
									"<option value='' selected='selected'>---------</option>" +
									"<option value='delete_selected'>Delete selected field officers</option>" +
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
												"Field officer" +
											"</th>" +
										"</tr>" +
									"</thead>" +
									"<tbody>" +
										"<div id='data-rows'" +       // Insert data rows here
										"</div>" +
									"</tbody>" +
								"</table>";
	
	final static private String fieldofficerListHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
								"<div id='content' class='flex'>" +
									"<h1>Select Field Officer to change</h1>" +
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
	
	final static private String fieldofficeAddHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
								"<div id='content' class='colM'>" +
									"<h1>Add field officer</h1>" +
									"<div id='content-main'>" +
										"<form enctype='multipart/form-data' action='' method='post' id='fieldofficer_form'>" +
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
												"</fieldset>" +
												"<div class='submit-row' >" +
													"<input type='submit' value='Save' class='default' name='_save' />" +
												"</div>" +
												"<script type='text/javascript'>document.getElementById('id_name').focus();</script>" +
												"<script type='text/javascript'>" +
												"</script>" +
											"</div>" +
										"</form>" +
									"</div>" +
									"<br class='clear' />" +
									"</div>";
}

package com.digitalgreen.dashboardgwt.client.templates;

public class PartnersTemplate {
	
	final static private String partnersListFormHtml = "<div class='actions'>" +
								"<label>Action: <select name='action'>" +
									"<option value='' selected='selected'>---------</option>" +
									"<option value='delete_selected'>Delete selected Partners</option>" +
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
											"Partner" +
										"</th>" +
									"</tr>" +
								"</thead>" +
								"<tbody>" +
									"<div id='data-rows'" +       // Insert data rows here
									"</div>" +
								"</tbody>" +
							"</table>";
	
	final static private String partnersListHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
								"<div id='content' class='flex'>" +
									"<h1>Select Partner to change</h1>" +
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
	
	final static private String partnersAddHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
								"<div id='content' class='colM'>" +
									"<h1>Add Partner</h1>" +
									"<div id='content-main'>" +
										"<form enctype='multipart/form-data' action='' method='post' id='partners_form'>" +
											"<div>" +
												"<fieldset class='module aligned '>" +
													"<div class='form-row partner_name  '>" +
														"<div>" +
															"<label for='id_partner_name' class='required'>Partner name:</label><input id='id_partner_name' type='text' class='vTextField' name='partner_name' maxlength='100' />" +
														"</div>" +
													"</div>" +
													"<div class='form-row date_of_association  '>" +
														"<div>" +
															"<label for='id_date_of_association'>Date of association:</label><input id='id_date_of_association' type='text' class='vDateField' name='date_of_association' size='10' />" +
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
												"<script type='text/javascript'>document.getElementById('id_partner_name').focus();</script>" +
												"<script type='text/javascript'>" +
												"</script>" +
											"</div>" +
										"</form>" +
									"</div>" +
									"<br class='clear' />" +
								"</div>";

}

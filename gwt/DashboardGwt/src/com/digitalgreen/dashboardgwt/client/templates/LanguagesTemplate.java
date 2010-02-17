package com.digitalgreen.dashboardgwt.client.templates;

public class LanguagesTemplate {
	
	final static private String languagesListFormHtml = "<div class='actions'>" +
							"<label>Action: <select name='action'>" +
								"<option value='' selected='selected'>---------</option>" +
								"<option value='delete_selected'>Delete selected languages</option>" +
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
										"Language" +
									"</th>" +
								"</tr>" +
							"</thead>" +
							"<tbody>" +
								"<div id='data-rows'" +       // Insert data rows here
								"</div>" +
							"</tbody>" +
						"</table>";
	
	final static private String languagesFormHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
								"<div id='content' class='flex'>" +
									"<h1>Select Language to change</h1>" +
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
	
	final static private String languagesAddHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
								"<div id='content' class='colM'>" +
									"<h1>Add language</h1>" +
									"<div id='content-main'>" +
										"<form enctype='multipart/form-data' action='' method='post' id='language_form'>" +
											"<div>" +
												"<fieldset class='module aligned '>" +
													"<div class='form-row language_name  '>" +
														"<div>" +
															"<label for='id_language_name' class='required'>Language name:</label><input id='id_language_name' type='text' class='vTextField' name='language_name' maxlength='100' />" +
														"</div>" +
													"</div>" +
												"</fieldset>" +
												"<div class='submit-row' >" +
													"<input type='submit' value='Save' class='default' name='_save' />" +
												"</div>" +
												"<script type='text/javascript'>document.getElementById('id_language_name').focus();</script>" +
												"<script type='text/javascript'>" +
												"</script>" +
											"</div>" +
										"</form>" +
									"</div>" +
									"<br class='clear' />" +
								"</div>";

}

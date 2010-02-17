package com.digitalgreen.dashboardgwt.client.templates;

public class EquipmentsTemplate {
	
	final static private String equipementsListFormHtml = "";
	
	final static private String equipmentsListHtml = "";
	
	final static private String equipmentsAddHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" + 
								"<div id='content' class='colM'>" +
									"<h1>Add equipment</h1>" +
									"<div id='content-main'>" +
										"<form enctype='multipart/form-data' action='' method='post' id='equipment_form'>" +
											"<div>" +
												"<fieldset class='module aligned '>" +
													"<div class='form-row equipment_type  '>" +
														"<div>" +
															"<label for='id_equipment_type' class='required'>Equipment type:</label><input id='id_equipment_type' type='text' class='vTextField' name='equipment_type' maxlength='300' />" +
														"</div>" +
													"</div>" +
													"<div class='form-row model_no  '>" +
														"<div>" +
															"<label for='id_model_no'>Model no:</label><input id='id_model_no' type='text' class='vTextField' name='model_no' maxlength='300' />" +
														"</div>" +
													"</div>" +
													"<div class='form-row serial_no  '>" +
														"<div>" +
															"<label for='id_serial_no'>Serial no:</label><input id='id_serial_no' type='text' class='vTextField' name='serial_no' maxlength='300' />" +
														"</div>" +
													"</div>" +
													"<div class='form-row cost  '>" +
														"<div>" +
															"<label for='id_cost'>Cost:</label><input type='text' name='cost' id='id_cost' />" +
														"</div>" +
													"</div>" +
													"<div class='form-row procurement_date  '>" +
														"<div>" +
															"<label for='id_procurement_date'>Procurement date:</label><input id='id_procurement_date' type='text' class='vDateField' name='procurement_date' size='10' />" +
														"</div>" +
													"</div>" +
													"<div class='form-row warranty_expiration_date  '>" +
														"<div>" +
															"<label for='id_warranty_expiration_date'>Warranty expiration date:</label><input id='id_warranty_expiration_date' type='text' class='vDateField' name='warranty_expiration_date' size='10' />" +
														"</div>" +
													"</div>" +
													"<div class='form-row equipmentholder  '>" +
														"<div>" +
															"<label for='id_equipmentholder'>Equipmentholder:</label><select name='equipmentholder' id='id_equipmentholder'>" +
																"<option value='' selected='selected'>---------</option>" +
															"</select>" +
														"</div>" +
													"</div>" +
												"</fieldset>" +
												"<div class='submit-row' >" +
													"<input type='submit' value='Save' class='default' name='_save' />" +
													"<input type='submit' value='Save and add another' name='_addanother'  />" +
													"<input type='submit' value='Save and continue editing' name='_continue' />" +
												"</div>" +
												"<script type='text/javascript'>document.getElementById('id_equipment_type').focus();</script>" +
												"<script type='text/javascript'>" +
												"</script>" +
											"</div>" +
										"</form>" +
									"</div>" +
									"<br class='clear' />" +
								"</div>";
}

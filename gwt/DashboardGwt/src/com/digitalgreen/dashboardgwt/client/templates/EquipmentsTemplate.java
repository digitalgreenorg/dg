package com.digitalgreen.dashboardgwt.client.templates;

import java.util.HashMap;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.EquipmentsData;
import com.digitalgreen.dashboardgwt.client.servlets.Equipments;
import com.google.gwt.user.client.Window;

public class EquipmentsTemplate extends BaseTemplate{
	
	public EquipmentsTemplate(RequestContext requestContext) {
		super(requestContext);
	}
	
	@Override
	public void fill() {
		String templateType = "Equipment";
		String templatePlainType = "dashboard/equipment/add/";
		RequestContext requestContext = new RequestContext();
		HashMap args = new HashMap();
		args.put("action", "add");
		requestContext.setArgs(args);
		Equipments addEquipmentsServlet = new Equipments(requestContext);
		RequestContext saveRequestContext = new RequestContext(RequestContext.METHOD_POST);
		Form saveForm = new Form((new EquipmentsData()).getNewData());
		saveRequestContext.setForm(saveForm);
		Equipments saveEquipment = new Equipments(saveRequestContext);
				
		// Draw the content of the template depending on the request type (GET/POST)
		super.fillDGTemplate(templateType, equipmentsListHtml, equipmentsAddHtml, addDataToElementID);
		// Add it to the rootpanel
		super.fill();
		
		this.fillListings();
		// Now add hyperlinks
		super.fillDGLinkControls(templatePlainType, templateType, equipmentsListFormHtml, addEquipmentsServlet);
		// Now add any submit control buttons
		super.fillDgFormFields(saveEquipment);
	}
	
	protected void fillListings() {
		HashMap queryArgs = this.getRequestContext().getArgs();
		String queryArg = (String)queryArgs.get("action");
		// If we're unsure, just default to list view
		if(queryArg == null || queryArg != "add") {
			// 	Add Listings
			List equipments = (List)queryArgs.get("listing");			
			if(equipments  != null){
				String tableRows ="";
				String style;
				EquipmentsData.Data equipment;
				for (int row = 0; row < equipments.size(); ++row) {
					if(row%2==0)
						style= "row2";
					else
						style = "row1";
					equipment = (EquipmentsData.Data) equipments.get(row);
					tableRows += "<tr class='" + style + "'>" +
								  "<td><input type='checkbox' class='action-select' value='"+ equipment.getId() 
								  + "' name='_selected_action' /></td> <th><a href='/admin/dashboard/equipment/"+ equipment.getId() 
								  +"/'>" + equipment.getEquipmentType()+"</a></th>" +
									"<td>"+ equipment.getModelNo()+ "</td>" +
									"<td>"+ equipment.getSerialNo()+ "</td>" +
								"</tr>";
					
					}
				equipmentsListFormHtml = equipmentsListFormHtml + tableRows + "</tbody></table>";
			}
		}
	}
	

	final private String addDataToElementID[] = null;
	
	private String equipmentsListFormHtml = "<div class='actions'>" +
									"<label>Action: <select name='action'>" + 
										"<option value='' selected='selected'>---------</option>" + 
										"<option value='delete_selected'>Delete selected equipments</option>" + 
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
													"Equipment type" +
												"</a>" +
											"</th>" +
											"<th>" + 
												"<a href='?ot=asc&amp;o=2'>" + 
													"Model no" +
												"</a>" +
											"</th>" +
											"<th>" + 
												"<a href='?ot=asc&amp;o=3'>" + 
													"Serial no" +
												"</a>" +
											"</th>" + 
										"</tr>" + 
									"</thead>" + 
									"<tbody>";
	
	final private String equipmentsListHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
									"<div id='content' class='flex'>" +
										"<h1>Select Equipment to change</h1>" +
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
	
	final private String equipmentsAddHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" + 
								"<div id='content' class='colM'>" +
									"<h1>Add equipment</h1>" +
									"<div id='content-main'>" +
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
										"<input id='save' value='Save' class='default' name='_save' />"	+
										"</div>" +
									"</div>" +
									"<br class='clear' />" +
								"</div>"+
	"<script src='/media/js/admin/DateTimeShortcuts.js' type='text/javascript'></script>" +	
	"<script type='text/javascript'>DateTimeShortcuts.init()</script>";
	
}

package com.digitalgreen.dashboardgwt.client.templates;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.FieldOfficersData;
import com.digitalgreen.dashboardgwt.client.servlets.FieldOfficers;
import com.google.gwt.user.client.ui.Hyperlink;


public class FieldOfficerTemplate extends BaseTemplate{
	
	public FieldOfficerTemplate(RequestContext requestContext) {
		super(requestContext);
		this.formTemplate = new Form((new FieldOfficersData()).getNewData());;
	}
	
	@Override
	public void fill() {
		String templateType = "Field Officer";
		String templatePlainType = "dashboard/fieldofficer/add";
		RequestContext requestContext = new RequestContext();
		HashMap args = new HashMap();
		args.put("action", "add");
		requestContext.setArgs(args);
		requestContext.setForm(this.formTemplate);
		RequestContext saveRequestContext = new RequestContext(RequestContext.METHOD_POST);
		saveRequestContext.setForm(this.formTemplate);
		FieldOfficers addFieldOfficersServlet = new FieldOfficers(requestContext);
		FieldOfficers saveFieldOfficer = new FieldOfficers(saveRequestContext);
		
		// Draw the content of the template depending on the request type (GET/POST)
		super.fillDGTemplate(templateType, fieldofficerListHtml, fieldofficerAddHtml, addDataToElementID);
		
		// Add it to the rootpanel
		super.fill();
		
		//Now add listings
		List<Hyperlink> links =  this.fillListings();
		
		// Now add hyperlinks
		super.fillDgListPage(templatePlainType, templateType, fieldofficerListFormHtml, addFieldOfficersServlet, links);
		
		// Now add any submit control buttons
		super.fillDgFormPage(saveFieldOfficer);
	}
	
	final private String addDataToElementID[] = null;

	public List<Hyperlink> fillListings(){
		HashMap queryArgs = this.getRequestContext().getArgs();
		String queryArg = (String)queryArgs.get("action");
		List<Hyperlink> links = new ArrayList<Hyperlink>();
		
		// If we're unsure, just default to list view
		if(queryArg.equals("list")) {
			
			// Add Listing
			List fieldOfficers = (List)queryArgs.get("listing");
			if(fieldOfficers != null){
				String tableRows = "";
				String style;
				FieldOfficersData.Data fieldofficer;
				RequestContext requestContext = null;
				for (int row=0; row<fieldOfficers.size(); ++row){
					if(row%2 == 0)
						style = "row2";
					else 
						style = "row1";
					fieldofficer = (FieldOfficersData.Data) fieldOfficers.get(row);
					requestContext = new RequestContext();
					requestContext.getArgs().put("action", "edit");
					requestContext.getArgs().put("id", fieldofficer.getId());
					requestContext.setForm(this.formTemplate);
					links.add(this.createHyperlink("<a href='#dashboard/fieldofficer/"+ fieldofficer.getId() +"/'>" +
							fieldofficer.getFieldOfficerName() + "</a>",
							"dashboard/fieldofficer/"+ fieldofficer.getId() +"/",
							new FieldOfficers(requestContext)));
					tableRows += "<tr class='" + style + "'><td><input type='checkbox' class='actoin-select' value='" + 
									fieldofficer.getId() + "' name='_selected_action' /></td>" +
									"<th id = 'row" + row + "'></th></tr>";
				}
				fieldofficerListFormHtml = fieldofficerListFormHtml + tableRows + "</tbody></table>";
			}
		}
		return links;
	}

	private String fieldofficerListFormHtml = "<script type='text/javascript' src='/media/js/admin/DateTimeShortcuts.js'></script>" +
												"<script type='text/javascript' src='/media/js/calendar.js'></script>" +
								"<div class='actions'>" +
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
												"<a href='?ot=asc&amp;o=1'>" +
													"Field officer" +
												"</a>" +
											"</th>" +
										"</tr>" +
									"</thead>" +
									"<tbody>";
	
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
	
	final static private String fieldofficerAddHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
								"<div id='content' class='colM'>" +
									"<h1>Add Field Officer</h1>" +
									"<div id='content-main'>" +
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
											"<input id='save' type='button' value='Save' class='default' name='_save' />" +
										"</div>" +
										"<script type='text/javascript'>document.getElementById('id_name').focus();</script>" +
									"</div>" +
									"<br class='clear' />" +
								"</div>" ;
}
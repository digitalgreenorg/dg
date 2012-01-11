package com.digitalgreen.dashboardgwt.client.templates;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.DevelopmentManagersData;
import com.digitalgreen.dashboardgwt.client.data.StatesData;
import com.digitalgreen.dashboardgwt.client.servlets.DevelopmentManagers;
import com.digitalgreen.dashboardgwt.client.servlets.States;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.Hyperlink;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

public class DevelopmentManagersTemplate extends BaseTemplate {
	
	public DevelopmentManagersTemplate(RequestContext requestContext){
		super(requestContext);
		this.formTemplate = new Form((new DevelopmentManagersData()).getNewData());
	}
	
	@Override
	public void fill() {
		String templateType = "Development Manager";
		String templatePlainType = "dashboard/developmentmanager/add/";
		RequestContext requestContext = new RequestContext();
		HashMap args = new HashMap();
		args.put("action", "add");
		requestContext.setArgs(args);
		requestContext.setForm(this.formTemplate);
		DevelopmentManagers addDevelopmentManagersServlet = new DevelopmentManagers(requestContext);
		RequestContext saveRequestContext = new RequestContext(RequestContext.METHOD_POST);
		saveRequestContext.setForm(this.formTemplate);
		DevelopmentManagers saveDevelopmentManager = new DevelopmentManagers(saveRequestContext);
		
		// Draw the content of the template depending on the request type (GET/POST)
		super.fillDGTemplate(templateType, dmListHtml, dmAddHtml, addDataToElementID);
		// Add it to the rootpanel
		super.fill();
		//Now add listings
		List<Hyperlink> links =  this.fillListings();
		// Now add hyperlinks
		super.fillDgListPage(templatePlainType, templateType, dmListFormHtml, addDevelopmentManagersServlet, links);
		// Now add any submit control buttons
		this.displayCalendar();
		super.fillDgFormPage(saveDevelopmentManager);
	}
	
	protected List<Hyperlink> fillListings() {
		
		HashMap queryArgs = this.getRequestContext().getArgs();
		String queryArg = (String)queryArgs.get("action");
		List<Hyperlink> links = new ArrayList<Hyperlink>();
		// If we're unsure, just default to list view
		if(queryArg.equals("list")) {
			// 	Add Listings
			List developmentmanagers = (List)queryArgs.get("listing");			
			if(developmentmanagers  != null){
				String tableRows ="";
				String style;
				DevelopmentManagersData.Data developmentmanager;
				RequestContext requestContext = null;
				for (int row = 0; row < developmentmanagers.size(); ++row) {
					if(row%2==0)
						style= "row2";
					else
						style = "row1";
					developmentmanager = (DevelopmentManagersData.Data) developmentmanagers.get(row);
					requestContext = new RequestContext();
					requestContext.getArgs().put("action", "edit");
					requestContext.getArgs().put("id", developmentmanager.getId());
					requestContext.setForm(this.formTemplate);
					links.add(this.createHyperlink("<a href='#dashboard/developmentmanager/" + developmentmanager.getId() + "/'>" +
							developmentmanager.getName() + "</a>",
							"dashboard/developmentmanager/" + developmentmanager.getId() + "/",
							new DevelopmentManagers(requestContext)));
					tableRows += "<tr class='" + style + "'>" +
								  "<td><input type='checkbox' class='action-select' value='"+ developmentmanager.getId() + "' name='_selected_action' /></td>" +
								  "<th id = 'row" + row + "'></th>" +
									"<td>"+ developmentmanager.getRegion().getRegionName() + "</td>" +
								"</tr>";
				}
				dmListFormHtml = dmListFormHtml + tableRows + "</tbody></table>";
			}
		}
		return links;
	}
	//Loading javascript for displaying calendar in Google chrome browser
	public static native void displayCalendar() /*-{
		$wnd.DateTimeShortcuts.init();		
	}-*/;
	
	final private String addDataToElementID[] = {"id_region"};

	private String dmListFormHtml = "<div class='actions'>" +
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
									"<tbody>" ;

	final private String dmListHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
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
	
	final private String dmAddHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
							"<div id='content' class='colM'>" +
								"<h1>Add Development Manager</h1>" +
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
												"<div class='form-row speciality  '>" +
													"<div>" +
														"<label for='id_speciality'>Speciality:</label><textarea id='id_speciality' rows='10' cols='40' name='speciality' class='vLargeTextField'></textarea>" +
													"</div>" +
												"</div>" +
												"<div class='form-row region  '>" +
													"<div>" +
														"<label for='id_region' class='required'>Region:</label><select name='region' id='id_region'>" +
															"<option value='' selected='selected'>---------</option>" +
															"</select>" +
													"</div>" +
												"</div>" +
												"<div class='form-row start_day  '>" +
													"<div>" +
														"<label for='id_start_day'>Start day:</label><input id='id_start_day' type='text' class='vDateField' name='start_day' size='10' />" +
													"</div>" +
												"</div>" +
											"</fieldset>" +
											"<div class='submit-row' >" +
												"<input id='save' type='button' value='Save' class='default' name='_save' />" +
											"</div>" +
												"<script type='text/javascript'>document.getElementById('id_name').focus();</script>" +
								"</div>" +
							"</div>" ;
}
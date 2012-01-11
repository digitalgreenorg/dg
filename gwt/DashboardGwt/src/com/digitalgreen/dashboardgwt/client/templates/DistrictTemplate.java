package com.digitalgreen.dashboardgwt.client.templates;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.DistrictsData;
import com.digitalgreen.dashboardgwt.client.servlets.Districts;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.Hyperlink;

public class DistrictTemplate extends BaseTemplate{
	
	public DistrictTemplate(RequestContext requestContext) {
		super(requestContext);
		this.formTemplate = new Form((new DistrictsData()).getNewData());
	}
	
	@Override
	public void fill() {
		String templateType = "District";
		String templatePlainType = "dashboard/district/add/";
		RequestContext requestContext = new RequestContext();
		HashMap args = new HashMap();
		args.put("action", "add");
		requestContext.setArgs(args);
		requestContext.setForm(this.formTemplate);
		Districts addDistrictsServlet = new Districts(requestContext);
		RequestContext saveRequestContext = new RequestContext(RequestContext.METHOD_POST);
		saveRequestContext.setForm(this.formTemplate);
		Districts saveDistrict = new Districts(saveRequestContext);
		
		// Draw the content of the template depending on the request type (GET/POST)
		super.fillDGTemplate(templateType, districtListHtml, districtAddHtml, addDataToElementID);
		// Add it to the rootpanel
		super.fill();
		//Now add listings
		List<Hyperlink> links = this.fillListings();
		// Now add hyperlinks
		super.fillDgListPage(templatePlainType, templateType, districtListFormHtml, addDistrictsServlet, links);
		// Now add any submit control buttons
		this.displayCalendar();
		super.fillDgFormPage(saveDistrict);
	}
	
	protected List<Hyperlink> fillListings(){
		HashMap queryArgs = this.getRequestContext().getArgs();
		String queryArg = (String)queryArgs.get("action");
		List<Hyperlink> links = new ArrayList<Hyperlink>();
		// If we're unsure, just default to list view
		if(queryArg.equals("list")) {
			// Add Listings
			List districts = (List)queryArgs.get("listing");
			if (districts != null) {
				String tableRows ="";
				String style;
				DistrictsData.Data district;
				RequestContext requestContext = null;
				for ( int row = 0; row < districts.size(); row++) {
					if(row%2==0)
						style= "row2";
					else
						style = "row1";
					district = (DistrictsData.Data) districts.get(row);
					requestContext = new RequestContext();
					requestContext.getArgs().put("action", "edit");
					requestContext.getArgs().put("id", district.getId());
					requestContext.setForm(this.formTemplate);
					links.add(this.createHyperlink("<a href='#dashboard/district/" + district.getId() +"/'>" +
							district.getDistrictName() + "</a>",
							"dashboard/district/" + district.getId() +"/",
							new Districts(requestContext)));
					tableRows += "<tr class='" + style + "'>" +
									"<td><input type='checkbox' class='action-select' value='" + district.getId() + "' name='_selected_action' /></td>" +
									"<th id = 'row" + row + "'></th>" +
									"<td>" + district.getState().getStateName() + "</td><td>" + district.getFieldOfficer().getFieldOfficerName() + 
									"</td><td>" + district.getPartner().getPartnerName() + "</td>" +
								"</tr>";
				}
				districtListFormHtml = districtListFormHtml + tableRows + "</tbody></table>";
			}
		}
		return links;
	}
	//Loading javascript for displaying calendar in Google chrome browser
	public static native void displayCalendar() /*-{
		$wnd.DateTimeShortcuts.init();		
	}-*/;

	final private String addDataToElementID[] = {"id_state", "id_fieldofficer", "id_partner"};
	
	private String districtListFormHtml = "<div class='actions'>" +
								"<label>Action: <select name='action'>" +
									"<option value='' selected='selected'>---------</option>" +
									"<option value='delete_selected'>Delete selected districts</option>" +
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
												"District name" +
											"</a>" +
										"</th>" +
										"<th>" +
											"<a href='?ot=asc&amp;o=2'>" +
												"State" +
											"</a>" +
										"</th>" +
										"<th>" +
											"<a href='?ot=asc&amp;o=3'>" +
												"Fieldofficer" +
											"</a>" +
										"</th>" +
										"<th>" +
											"<a href='?ot=asc&amp;o=4'>" +
												"Partner" +
											"</a>" +
										"</th>" +
									"</tr>" +
								"</thead>" +
								"<tbody>";
	
	final private String districtListHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
								"<div id='content' class='flex'>" +
									"<h1>Select district to change</h1>" +
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
	
	final private String districtAddHtml =  "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
						"<div id='content' class='colM'>" +
						"<h1>Add district</h1>" +
							"<div id='content-main'>" +
								"<fieldset class='module aligned '>" +
									"<div class='form-row district_name  '>" +
										"<div>" +
											"<label for='id_district_name' class='required'>District name:</label><input id='id_district_name' type='text' class='vTextField' name='district_name' maxlength='100' />" +
										"</div>" +
									"</div>" +
									"<div class='form-row start_date  '>" +
										"<div>" +
											"<label for='id_start_date'>Start date:</label><input id='id_start_date' type='text' class='vDateField' name='start_date' size='10' />" +
										"</div>" +
									"</div>" +
									"<div class='form-row state  '>" +
										"<div>" +
											"<label for='id_state' class='required'>State:</label><select name='state' id='id_state'>" +
												"<option value='' selected='selected'>---------</option>" +
											"</select>" +
										"</div>" +
									"</div>" +
									"<div class='form-row fieldofficer  '>" +
										"<div>" +
											"<label for='id_fieldofficer' class='required'>Fieldofficer:</label><select name='fieldofficer' id='id_fieldofficer'>" +
												"<option value='' selected='selected'>---------</option>" +
											"</select>" +
										"</div>" +
									"</div>" +
									"<div class='form-row fieldofficer_startday  '>" +
										"<div>" +
											"<label for='id_fieldofficer_startday'>Fieldofficer startday:</label><input id='id_fieldofficer_startday' type='text' class='vDateField' name='fieldofficer_startday' size='10' />" +
										"</div>" +
									"</div>" +
									"<div class='form-row partner  '>" +
										"<div>" +
											"<label for='id_partner' class='required'>Partner:</label><select name='partner' id='id_partner'>" +
												"<option value='' selected='selected'>---------</option>" +
											"</select>" +
										"</div>" +
									"</div>" +
								"</fieldset>" +
								"<div class='submit-row' >" +
									"<input id='save' type='button' value='Save' class='default' name='_save' />" +
								"</div>" +
								"<script type='text/javascript'>document.getElementById('id_district_name').focus();</script>" +
							"</div>" +
							"<br class='clear' />" +
						"</div>";
}
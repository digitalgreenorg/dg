package com.digitalgreen.dashboardgwt.client.templates;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.StatesData;
import com.digitalgreen.dashboardgwt.client.servlets.States;
import com.google.gwt.user.client.ui.Hyperlink;

public class StatesTemplate extends BaseTemplate{
	
	public StatesTemplate(RequestContext requestContext) {
		super(requestContext);
	}
	
	@Override
	public void fill() {
		String templateType = "State";
		String templatePlainType = "dashboard/state/add/";
		RequestContext requestContext = new RequestContext();
		HashMap args = new HashMap();
		args.put("action", "add");
		requestContext.setArgs(args);
		States addStatesServlet = new States(requestContext);
		RequestContext saveRequestContext = new RequestContext(RequestContext.METHOD_POST);
		Form saveForm = new Form((new StatesData()).getNewData());
		saveRequestContext.setForm(saveForm);
		States saveState = new States(saveRequestContext);
		
		// Draw the content of the template depending on the request type (GET/POST)
		super.fillDGTemplate(templateType, statesListHtml, statesAddHtml, addDataToElementID);
		// Add it to the rootpanel
		super.fill();
		//Now add listings
		List<Hyperlink> links =  this.fillListings();
		// Now add hyperlinks
		super.fillDgListPage(templatePlainType, templateType, statesListFormHtml, addStatesServlet, links);
		// Now add any submit control buttons
		super.fillDgFormPage(saveState);
	}
	
	protected List<Hyperlink> fillListings() {
		HashMap queryArgs = this.getRequestContext().getArgs();
		String queryArg = (String)queryArgs.get("action");
		List<Hyperlink> links = new ArrayList<Hyperlink>();
		// If we're unsure, just default to list view
		if(queryArg.equals("list")) {
			// 	Add Listings
			List states = (List)queryArgs.get("listing");			
			if(states  != null){
				String tableRows ="";
				String style;
				StatesData.Data state;
				RequestContext requestContext = null;
				for (int row = 0; row < states.size(); ++row) {
					if(row%2==0)
						style= "row2";
					else
						style = "row1";
					state = (StatesData.Data) states.get(row);
					requestContext = new RequestContext();
					requestContext.getArgs().put("action", "edit");
					requestContext.getArgs().put("id", state.getId());
					links.add(this.createHyperlink("<a href='#dashboard/state/" + state.getId() + "/'>" +
							state.getStateName() + "</a>", new States(requestContext)));
					tableRows += "<tr class='" +style+ "'>" +
								  "<td><input type='checkbox' class='action-select' value='"+ state.getId() + "' name='_selected_action' /></td>" +
									"<th id = 'row" + row + "'></th>" +
									"<td>"+ state.getRegion().getRegionName() + "</td>" +
								"</tr>";
				}
				statesListFormHtml = statesListFormHtml + tableRows + "</tbody></table>";
			}
		}
		return links;
	}
	
	
	
	// A list of Element IDs that need to receive the data before the template is loaded. 
	final private String addDataToElementID[] = {"id_region"};
	
	private String statesListFormHtml = "<div class='actions'>" +
    							"<label>Action: <select name='action'>" +
    								"<option value='' selected='selected'>---------</option>" +
    								"<option value='delete_selected'>Delete selected states</option>" +
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
    											"State name" +
    										"</a>" +
    									"</th>" +
    									"<th>" +
    										"<a href='?ot=asc&amp;o=2'>" +
    											"Region" +
    										"</a>" +
    									"</th>" +
    								"</tr>" +
    							"</thead>" +
    							"<tbody>";

	// Fill ids:  listing-form-body, add-link
	final  private String statesListHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
								"<div id='content' class='flex'>" +
									"<h1>Select State to change</h1>" +
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

	final  private String statesAddHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
								"<div id='content' class='colM'>" +
									"<h1>Add State</h1>" +
									"<div id='content-main'>" +
										//"<!--form enctype='multipart/form-data' action='' method='post' id='state_form'-->" +
											//"<div>" +
												"<fieldset class='module aligned '>" +
													"<div class='form-row state_name  '>" +
														"<div>" +
															"<label for='id_state_name' class='required'>State name:</label><input id='id_state_name' type='text' class='vTextField' name='state_name' maxlength='100' />" +
														"</div>" +
													"</div>" +
													"<div class='form-row region  '>" +
														"<div>" +
															"<label for='id_region' class='required'>Region:</label><select name='region' id='id_region'>" +
																"<option value='' selected='selected'>---------</option>" +
															"</select>" +
														"</div>" +
													"</div>" +
													"<div class='form-row start_date  '>" +
														"<div>" +
															"<label for='id_start_date'>Start date:</label><input id='id_start_date' type='text' class='vDateField' name='start_date' size='10' />" +
														"</div>" +
													"</div>" +
												"</fieldset>" +
												"<div class='submit-row' >" +
													"<input id='save' value='Save' class='default' name='_save' />" +
												"</div>" +
												"<script type='text/javascript'>document.getElementById('id_state_name').focus();</script>" +
											//"</div>" +
										//"</form>" +
									"</div>" +
									"<br class='clear' />" +
								"</div>"+
								"<script src='/media/js/admin/DateTimeShortcuts.js' type='text/javascript'></script>" +	
								"<script type='text/javascript'>DateTimeShortcuts.init()</script>"; 
}
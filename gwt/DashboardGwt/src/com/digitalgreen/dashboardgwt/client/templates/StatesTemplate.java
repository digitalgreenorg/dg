package com.digitalgreen.dashboardgwt.client.templates;

import java.util.HashMap;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.servlets.States;

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
		States saveState = new States(new RequestContext(RequestContext.METHOD_POST));
		// Draw the content of the template depending on the request type (GET/POST)
		super.fillDGTemplate(templateType, statesListHtml, statesAddHtml);
		// Add it to the rootpanel
		super.fill();
		// Now add hyperlinks
		super.fillDGLinkControls(templatePlainType, templateType, statesListFormHtml, addStatesServlet);
		// Now add any submit control buttons
		super.fillDGSubmitControls(saveState);
	}
	
	final static private String statesListFormHtml = "<div class='actions'>" +
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
    							"<tbody>"  +
    								"<div id='data-rows'" +       // Insert data rows here
    								"</div>" +
    							"</tbody>" +
    						"</table>";

	// Fill ids:  listing-form-body, add-link
	final static private String statesListHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
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

	final static private String statesAddHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
								"<div id='content' class='colM'>" +
									"<h1>Add State</h1>" +
									"<div id='content-main'>" +
										"<form enctype='multipart/form-data' action='' method='post' id='state_form'>" +
											"<div>" +
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
															"</select><a href='/admin/dashboard/region/add/' class='add-another' id='add_id_region' onclick='return showAddAnotherPopup(this);'> <img src='/media/img/admin/icon_addlink.gif' width='10' height='10' alt='Add Another'/></a>" +
														"</div>" +
													"</div>" +
													"<div class='form-row start_date  '>" +
														"<div>" +
															"<label for='id_start_date'>Start date:</label><input id='id_start_date' type='text' class='vDateField' name='start_date' size='10' />" +
														"</div>" +
													"</div>" +
												"</fieldset>" +
												"<div class='submit-row' >" +
													"<input type='submit' value='Save' class='default' name='_save' />" +
												"</div>" +
												"<script type='text/javascript'>document.getElementById('id_state_name').focus();</script>" +
												"<script type='text/javascript'>" +
												"</script>" +
											"</div>" +
										"</form>" +
									"</div>" +
									"<br class='clear' />" +
								"</div>"; 
}
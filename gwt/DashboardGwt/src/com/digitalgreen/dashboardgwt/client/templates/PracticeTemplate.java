package com.digitalgreen.dashboardgwt.client.templates;

import java.util.HashMap;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.servlets.Practices;

public class PracticeTemplate  extends BaseTemplate{
	
	public PracticeTemplate(RequestContext requestContext) {
		super(requestContext);
	}
	
	@Override
	public void fill() {
		String templateType = "Practice";
		String templatePlainType = "dashboard/practices/add/";
		RequestContext requestContext = new RequestContext();
		HashMap args = new HashMap();
		args.put("action", "add");
		requestContext.setArgs(args);
		Practices addPracticesServlet = new Practices(requestContext);
		Practices practice = new Practices(BaseTemplate.setupDgPostContext(this.getDgFormId()));
		// Draw the content of the template depending on the request type (GET/POST)
		super.fillDGTemplate(templateType, practiceListHtml, practiceAddHtml);
		// Add it to the rootpanel
		super.fill();
		// Now add hyperlinks
		super.fillDGLinkControls(templatePlainType, templateType, practiceListFormHtml, addPracticesServlet);
		// Now add any submit control buttons
		super.fillDGSubmitControls(practice);
	}

	final static private String practiceListFormHtml = "<div class='actions'>" +
    							"<label>Action: <select name='action'>" +
    								"<option value='' selected='selected'>---------</option>" +
    								"<option value='delete_selected'>Delete selected Practices</option>" +
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
    										"Practice" +
    									"</th>" +
    								"</tr>" +
    							"</thead>" +
    							"<tbody>" +
    								"<div id='data-rows'" +       // Insert data rows here
    								"</div>" +
    							"</tbody>" +
    						"</table>";
	
	final static private String practiceListHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
								"<div id='content' class='flex'>" +
									"<h1>Select Practice to change</h1>" +
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
	
	final static private String practiceAddHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
								"<div id='content' class='colM'>" +
									"<h1>Add Practice</h1>" +
									"<div id='content-main'>" +
										"<form enctype='multipart/form-data' action='' method='post' id='practices_form'>" +
											"<div>" +
												"<fieldset class='module aligned '>" +
													"<div class='form-row practice_name  '>" +
														"<div>" +
															"<label for='id_practice_name' class='required'>Practice name:</label>" +
															"<input id='id_practice_name' type='text' class='vTextField' name='practice_name' maxlength='200' />" +
														"</div>" +
													"</div>" +
													"<div class='form-row seasonality  '>" +
														"<div>" +
															"<label for='id_seasonality' class='required'>Seasonality:</label>" +
																"<select name='seasonality' id='id_seasonality'>" +
																"<option value='' selected='selected'>---------</option>" +
																"<option value='Jan'>January</option>" +
																"<option value='Feb'>February</option>" +
																"<option value='Mar'>March</option>" +
																"<option value='Apr'>April</option>" +
																"<option value='May'>May</option>" +
																"<option value='Jun'>June</option>" +
																"<option value='Jul'>July</option>" +
																"<option value='Aug'>August</option>" +
																"<option value='Sep'>September</option>" +
																"<option value='Oct'>October</option>" +
																"<option value='Nov'>November</option>" +
																"<option value='Dec'>December</option>" +
																"<option value='Kha'>Kharif</option>" +
																"<option value='Rab'>Rabi</option>" +
																"<option value='Rou'>Round the year</option>" +
																"<option value='Rai'>Rainy season</option>" +
																"<option value='Sum'>Summer season</option>" +
																"<option value='Win'>Winter season</option>" +
															"</select>" +
														"</div>" +
													"</div>" +
													"<div class='form-row summary  '>" +
														"<div>" +
															"<label for='id_summary'>Summary:</label>" +
															"<textarea id='id_summary' rows='10' cols='40' name='summary' class='vLargeTextField'></textarea>" +
														"</div>" +
													"</div>" +
												"</fieldset>" +
												"<div class='submit-row' >" +
													"<input type='submit' value='Save' class='default' name='_save' />" +
												"</div>" +
												"<script type='text/javascript'>document.getElementById('id_practice_name').focus();</script>" +
												"<script type='text/javascript'>" +
												"</script>" +
											"</div>" +
										"</form>" +
									"</div>" +
									"<br class='clear' />" +
								"</div>";

}
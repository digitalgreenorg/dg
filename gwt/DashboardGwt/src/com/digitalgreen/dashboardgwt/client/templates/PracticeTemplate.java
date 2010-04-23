package com.digitalgreen.dashboardgwt.client.templates;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.PracticesData;
import com.digitalgreen.dashboardgwt.client.servlets.Practices;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.Hyperlink;

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
		RequestContext saveRequestContext = new RequestContext(RequestContext.METHOD_POST);
		Form saveForm = new Form((new PracticesData()).getNewData());
		saveRequestContext.setForm(saveForm);
		Practices addPracticesServlet = new Practices(requestContext);
		Practices savePractice = new Practices(saveRequestContext);
		
		// Draw the content of the template depending on the request type (GET/POST)
		super.fillDGTemplate(templateType, practiceListHtml, practiceAddHtml, addDataToElementID);
		// Add it to the rootpanel
		super.fill();
		//Now add listings
		List<Hyperlink> links =  this.fillListings();
		// Now add hyperlinks
		super.fillDgListPage(templatePlainType, templateType, practiceListFormHtml, addPracticesServlet, links);
		// Now add any submit control buttons
		super.fillDgFormPage(savePractice);
	}
	
	public List<Hyperlink> fillListings(){
		HashMap queryArgs = this.getRequestContext().getArgs();
		String queryArg = (String)queryArgs.get("action");
		List<Hyperlink> links = new ArrayList<Hyperlink>();
		// If we're unsure, just default to list view
		if(queryArg == null || queryArg != "add"){
			// Add listing
			List practices = (List)queryArgs.get("listing");
			if(practices != null){
				String tableRows = "";
				String style;
				PracticesData.Data practice;
				RequestContext requestContext = null;
				for(int row = 0; row < practices.size(); ++row){
					if(row%2 == 0)
						style = "row2";
					else
						style = "row1";
					practice = (PracticesData.Data)practices.get(row);
					requestContext = new RequestContext();
					requestContext.getArgs().put("action", "edit");
					requestContext.getArgs().put("id", practice.getId());
					links.add(this.createHyperlink("<a href='#dashboard/practice/"+ practice.getId() +"/'>" +
							practice.getPracticeName()+"</a>", new Practices(requestContext)));
					tableRows += "<tr class='" + style + "'><td><input type='checkbox' class='action-select' value='" +  
									practice.getId() + "' name='_selected_action' /></td>" +
									"<th id = 'row" + row + "'></th></tr>";
				}
				practiceListFormHtml = practiceListFormHtml + tableRows + "</tbody></table>";
			}
		}
		return links;
	}

	final private String addDataToElementID[] = null;
	
	private String practiceListFormHtml = "<script type='text/javascript' src='/media/js/admin/DateTimeShortcuts.js'></script>" +
							"<script type='text/javascript' src='/media/js/calendar.js'></script>" +
							"<div class='actions'>" +
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
	    									"<a href='?ot=asc&amp;o=1'>" +
	    										"Practice" +
    										"</a>" +
    									"</th>" +
    								"</tr>" +
    							"</thead>" +
    							"<tbody>";
	
	final private String practiceListHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
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
	
	final private String practiceAddHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
								"<div id='content' class='colM'>" +
									"<h1>Add Practice</h1>" +
									"<div id='content-main'>" +
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
											"<input id='save' value='Save' class='default' name='_save' />" +
										"</div>" +
										"<script type='text/javascript'>document.getElementById('id_practice_name').focus();</script>" +
									"</div>" +
									"<br class='clear' />" +
								"</div>" +
								"<script src='/media/js/admin/DateTimeShortcuts.js' type='text/javascript'></script>" +	
								"<script type='text/javascript'>DateTimeShortcuts.init()</script>";
}
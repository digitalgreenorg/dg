package com.digitalgreen.dashboardgwt.client.templates;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.servlets.Regions;
import com.digitalgreen.dashboardgwt.client.servlets.Screenings;
import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.Button;
import com.google.gwt.user.client.ui.FormPanel;
import com.google.gwt.user.client.ui.HTMLPanel;
import com.google.gwt.user.client.ui.Hyperlink;
import com.google.gwt.user.client.ui.RootPanel;

import java.util.HashMap;

public class RegionsTemplate extends BaseTemplate {
	public RegionsTemplate(RequestContext requestContext) {
		super(requestContext);
	}
	
	@Override
	public void fill() {
		String templateType = "Region";
		String templatePlainType = "dashboard/region/add/";
		RequestContext requestContext = new RequestContext();
		HashMap args = new HashMap();
		args.put("action", "add");
		requestContext.setArgs(args);
		Regions addRegionServlet = new Regions(requestContext);
		Regions saveRegion = new Regions(new RequestContext(RequestContext.METHOD_POST));
		// Draw the content of the template depending on the request type (GET/POST)
		super.fillDGTemplate(templateType, regionsListHtml, regionsAddHtml);
		// Add it to the rootpanel
		super.fill();
		// Now add hyperlinks
		super.fillDGLinkControls(templatePlainType, templateType, regionsListFormHtml, addRegionServlet);
		// Now add any submit control buttons
		super.fillDGSubmitControls(saveRegion);
	}
	
	final static private String regionsListFormHtml = "<div class='actions'>" +
						"<label>Action: <select name='action'>" +
							"<option value='' selected='selected'>---------</option>" +
							"<option value='delete_selected'>Delete selected regions</option>" +
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
										"Region" +
									"</a>" +
								"</th>" +
							"</tr>" +
						"</thead>" +
						"<tbody>" +
							"<div id='data-rows'" +       // Insert data rows here
							"</div>" +
						"</tbody>" +
					"</table>";
						
	final static private String regionsListHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
						"<div id='content' class='flex'>" +
							"<h1>Select region to change</h1>" +
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
	
	final static private String regionsAddHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
		"<div id='content' class='colM'>" +
			"<h1>Add Regions</h1>" +
			"<div id='content-main'>" +
				"<fieldset class='module aligned '>" +
					"<div class='form-row region_name  '>" +
						"<div>" +
							"<label for='id_region_name' class='required'>Region name:</label><input id='id_region_name' type='text' class='vTextField' name='region_name' maxlength='100' />" +
						"</div>" +
					"</div>" +
					"<div class='form-row start_date'>" +
						"<div>" +
							"<label for='id_start_date'>Start date:</label>" +
							"<input id='id_start_date' type='text' class='vDateField' name='start_date' size='10' />" +
						"</div>" +
					"</div>" +
				"</fieldset>" +
				"<div class='submit-row'>" +
					"<input id='save' type='submit' value='Save' class='default' name='_save' />" +
				"</div>" +
			"</div>" +
		"</div>";
	}
package com.digitalgreen.dashboardgwt.client.templates;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.RegionsData;
import com.digitalgreen.dashboardgwt.client.servlets.Regions;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.Hyperlink;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

public class RegionsTemplate extends BaseTemplate {
	public RegionsTemplate(RequestContext requestContext) {
		super(requestContext);
		this.formTemplate = new Form((new RegionsData()).getNewData());
	}
	
	@Override
	public void fill() {
		String templateType = "Region";
		String templatePlainType = "dashboard/region/add/";
		RequestContext requestContext = new RequestContext();
		HashMap args = new HashMap();
		args.put("action", "add");
		requestContext.setArgs(args);
		requestContext.setForm(this.formTemplate);
		Regions addRegionServlet = new Regions(requestContext);
		RequestContext saveRequestContext = new RequestContext(RequestContext.METHOD_POST);
		saveRequestContext.setForm(this.formTemplate);
		Regions saveRegion = new Regions(saveRequestContext);
		// Draw the content of the template depending on the request type (GET/POST)
		super.fillDGTemplate(templateType, regionsListHtml, regionsAddHtml, addDataToElementID);
		// Add it to the rootpanel
		super.fill();
		//Now add listings
		List<Hyperlink> links =  this.fillListings();
		// Now add hyperlinks
		super.fillDgListPage(templatePlainType, templateType, regionsListFormHtml, addRegionServlet, links);
		// Now add any submit control buttons
		super.fillDgFormPage(saveRegion);
	}
	
	protected List<Hyperlink> fillListings() {
		HashMap queryArgs = this.getRequestContext().getArgs();
		String queryArg = (String)queryArgs.get("action");
		List<Hyperlink> links = new ArrayList<Hyperlink>();
		// If we're unsure, just default to list view
		if(queryArg.equals("list")) {
			// 	Add Listings
			List regions = (List)queryArgs.get("listing");			
			if(regions  != null){
				String tableRows ="";
				String style;
				RegionsData.Data region;
				RequestContext requestContext = null;
				for (int row = 0; row < regions.size(); ++row) {
					if(row%2==0)
						style= "row2";
					else
						style = "row1";
					region = (RegionsData.Data) regions.get(row);
					requestContext = new RequestContext();
					requestContext.getArgs().put("action", "edit");
					requestContext.getArgs().put("id", region.getId());
					requestContext.setForm(this.formTemplate);
					links.add(this.createHyperlink("<a href='#dashboard/region/" + region.getId() + "/'>" +
							region.getRegionName() + "</a>",
							"dashboard/region/" + region.getId() + "/",
							new Regions(requestContext)));
					tableRows += "<tr class='" + style + "'><td><input type='checkbox' class='action-select' value='" + 
								region.getId() + "' name='_selected_action' /></td>" +
								"<th id = 'row" + row + "'></th></tr>";
				}
				regionsListFormHtml = regionsListFormHtml + tableRows + "</tbody></table>";
			}
		}
		return links;
	}
	
	final private String addDataToElementID[] = null;
	
	private String regionsListFormHtml = "<script type='text/javascript' src='/media/js/admin/DateTimeShortcuts.js'></script>" +
						"<script type='text/javascript' src='/media/js/calendar.js'></script>" +
						"<div class='actions'>" +
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
						"<tbody>";

	final  private String regionsListHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
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
	
	final  private String regionsAddHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
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
					"<input id='save' type='button' value='Save' class='default' name='_save' />" +
				"</div>" +
			"</div>" +
		"</div>" +
		"<script src='/media/js/admin/DateTimeShortcuts.js' type='text/javascript'></script>" +	
		"<script type='text/javascript'>DateTimeShortcuts.init()</script>";
	}
package com.digitalgreen.dashboardgwt.client.templates;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.LanguagesData;
import com.digitalgreen.dashboardgwt.client.data.RegionsData;
import com.digitalgreen.dashboardgwt.client.servlets.Languages;
import com.digitalgreen.dashboardgwt.client.servlets.Regions;
import com.google.gwt.user.client.ui.Hyperlink;

public class LanguagesTemplate extends BaseTemplate{
	
	public LanguagesTemplate(RequestContext requestContext) {
		super(requestContext);
	}
	
	@Override
	public void fill() {
		String templateType = "Languages";
		String templatePlainType = "dashboard/language/add/";
		RequestContext requestContext = new RequestContext();
		HashMap args = new HashMap();
		args.put("action", "add");
		requestContext.setArgs(args);
		RequestContext saveRequestContext = new RequestContext(RequestContext.METHOD_POST);
		Form saveForm = new Form((new LanguagesData()).getNewData());
		saveRequestContext.setForm(saveForm);
		Languages addLanguagesServlet = new Languages(requestContext);
		Languages saveLanguage = new Languages(saveRequestContext);
		
		// Draw the content of the template depending on the request type (GET/POST)
		super.fillDGTemplate(templateType, languagesListHtml, languagesAddHtml, addDataToElementID);
		// Add it to the rootpanel
		super.fill();
		//Now add listings
		List<Hyperlink> links =  this.fillListings();
		// Now add hyperlinks
		super.fillDgListPage(templatePlainType, templateType, languagesListFormHtml, addLanguagesServlet, links);
		// Now add any submit control buttons
		super.fillDgFormPage(saveLanguage);
	}
	
	protected List<Hyperlink> fillListings() {
		HashMap queryArgs = this.getRequestContext().getArgs();
		String queryArg = (String)queryArgs.get("action");
		List<Hyperlink> links = new ArrayList<Hyperlink>();
		// If we're unsure, just default to list view
		if(queryArg.equals("list")) {
			// 	Add Listings
			List languages = (List)queryArgs.get("listing");			
			if(languages  != null){
				String tableRows ="";
				String style;
				LanguagesData.Data language;
				RequestContext requestContext = null;
				for (int row = 0; row < languages.size(); ++row) {
					if(row%2==0)
						style= "row2";
					else
						style = "row1";
					language = (LanguagesData.Data) languages.get(row);
					requestContext = new RequestContext();
					requestContext.getArgs().put("action", "edit");
					requestContext.getArgs().put("id", language.getId());
					links.add(this.createHyperlink("<a href='#dashboard/language/" + language.getId() +"/'>" +
							language.getLanguageName() + "</a>", new Languages(requestContext)));
					tableRows += "<tr class='" + style + "'><td><input type='checkbox' class='action-select' value='" + 
									language.getId() + "' name='_selected_action' /></td>" +
									"<th id = 'row" + row + "'></th></tr>";
				}
				languagesListFormHtml = languagesListFormHtml + tableRows + "</tbody></table>";
			}
		}
		return links;
	}
	
	final private String addDataToElementID[] = null;
	
	private String languagesListFormHtml = "<script type='text/javascript' src='/media/js/admin/DateTimeShortcuts.js'></script>" +
											"<script type='text/javascript' src='/media/js/calendar.js'></script>" + 
							"<div class='actions'>" +
							"<label>Action: <select name='action'>" +
								"<option value='' selected='selected'>---------</option>" +
								"<option value='delete_selected'>Delete selected languages</option>" +
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
										"Language" +
									"</a>" +
								"</th>" +
							"</tr>" +
						"</thead>" +
						"<tbody>";
	
	final private String languagesListHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
								"<div id='content' class='flex'>" +
									"<h1>Select Language to change</h1>" +
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
	
	final private String languagesAddHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
								"<div id='content' class='colM'>" +
									"<h1>Add language</h1>" +
									"<div id='content-main'>" +
										"<fieldset class='module aligned '>" +
											"<div class='form-row language_name  '>" +
												"<div>" +
													"<label for='id_language_name' class='required'>Language name:</label><input id='id_language_name' type='text' class='vTextField' name='language_name' maxlength='100' />" +
												"</div>" +
											"</div>" +
										"</fieldset>" +
										"<div class='submit-row' >" +
											"<input id='save' value='Save' class='default' name='_save' />" +
										"</div>" +
										"<script type='text/javascript'>document.getElementById('id_language_name').focus();</script>" +
									"</div>" +
									"<br class='clear' />" +
								"</div>" +
								"<script src='/media/js/admin/DateTimeShortcuts.js' type='text/javascript'></script>" +	
								"<script type='text/javascript'>DateTimeShortcuts.init()</script>";
}
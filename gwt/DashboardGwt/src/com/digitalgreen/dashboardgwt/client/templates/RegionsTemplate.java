package com.digitalgreen.dashboardgwt.client.templates;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.servlets.Regions;
import com.digitalgreen.dashboardgwt.client.servlets.Screenings;
import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.user.client.ui.Button;
import com.google.gwt.user.client.ui.FormPanel;
import com.google.gwt.user.client.ui.HTMLPanel;
import com.google.gwt.user.client.ui.Hyperlink;
import com.google.gwt.user.client.ui.RootPanel;

import java.util.HashMap;

public class RegionsTemplate extends BaseTemplate {
	private FormPanel postForm = null;
	private HTMLPanel displayHtml = null;
	
	public RegionsTemplate(RequestContext requestContext) {
		super(requestContext);
	}
	
	public FormPanel getPostForm() {
		return this.postForm;
	}
	
	private void fillUserDefined() {
		HashMap queryArgs = this.getRequestContext().getArgs();
		String queryArg = (String)queryArgs.get("action");
		// If we're unsure, just default to list view
		if(queryArg == null || queryArg != "add") {
			HTMLPanel listFormHtml = new HTMLPanel(regionsListFormHtml);
			RootPanel.get("listing-form-body").insert(listFormHtml, 0);
			Hyperlink addLink = new Hyperlink();
			addLink.setHTML("<a class='addlink' href='#add-regions-link'> Add region </a>");
			// Take them to the add page for screenings
			addLink.addClickHandler(new ClickHandler() {
				public void onClick(ClickEvent event) {
					RequestContext requestContext = new RequestContext();
					HashMap args = new HashMap();
					args.put("action", "add");
					requestContext.setArgs(args);
					// Give the servlet control
					Regions region = new Regions(requestContext);
					region.response();
				}
			});
			RootPanel.get("add-link").add(addLink);
		}
	}
	
	@Override
	public void fill() {
		if(this.getRequestContext().getMethodTypeCtx() == RequestContext.METHOD_GET) {
			HashMap queryArgs = this.getRequestContext().getArgs();
			String queryArg = (String)queryArgs.get("action");
			if(queryArg == "add") {
				this.postForm = new FormPanel();
				this.postForm.setAction(RequestContext.getServerUrl() + "add_region");
			    this.postForm.setEncoding(FormPanel.ENCODING_MULTIPART);
			    this.postForm.setMethod(FormPanel.METHOD_POST);
				this.displayHtml = new HTMLPanel(regionsAddHtml);
			    this.postForm.add(this.displayHtml);
				super.setContentPanel(this.postForm);
				super.setContentClassName("colM");
				this.fillSubmitControls();
			} else {
				this.displayHtml = new HTMLPanel(regionsListHtml);
				super.setContentPanel(this.displayHtml);
				super.setContentClassName("flex");
			}
		}	
		super.fill();
		fillUserDefined();	
	}
	
	@Override
	public void fillSubmitControls() {
		if(this.getRequestContext().getMethodTypeCtx() == RequestContext.METHOD_GET) {
			Button b = new Button("Save");
		    b.setStyleName("button default");
		    b.addClickHandler(new ClickHandler() {
				public void onClick(ClickEvent event) {
					Regions region = new Regions(new RequestContext(RequestContext.METHOD_POST, 
												 getPostForm()));
					region.response();
				}
		    });
			super.setSubmitControlsPanel(b);
			super.fillSubmitControls();
		}
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
						
	final static private String regionsListHtml = "<h1>Select region to change</h1>" +
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
							"</div>";
	
	final static private String regionsAddHtml = "<h1>Add Regions</h1>" +
			"<div>" +
				"<fieldset class='module aligned '>" +
					"<div class='form-row region_name  '>" +
						"<div>" +
							"<label for='id_region_name' class='required'>Region name:</label><input id='id_region_name' type='text' class='vTextField' name='region_name' maxlength='100' />" +
						"</div>" +
					"</div>" +
					"<div class='form-row start_date'>" +
						"<div><label for='id_start_date'>Start date:</label><input id='id_start_date' type='text' class='vDateField' name='start_date' size='10' />" +
					"</div>" +
				"</fieldset>" +
			"</div>";
	
	}
package com.digitalgreen.dashboardgwt.client.templates;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.servlets.Regions;
import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.user.client.ui.Button;
import com.google.gwt.user.client.ui.FormPanel;
import com.google.gwt.user.client.ui.HTMLPanel;
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
	
	@Override
	public void fill() {
		if(this.getRequestContext().getMethodTypeCtx() == RequestContext.METHOD_GET) {
			HashMap queryArgs = this.getRequestContext().getArgs();
			String queryArg = (String)queryArgs.get("action");
			if(queryArg == "add") {
				this.postForm = new FormPanel();
				this.postForm.setAction(this.getRequestContext().getFormAction());
			    this.postForm.setEncoding(FormPanel.ENCODING_MULTIPART);
			    this.postForm.setMethod(FormPanel.METHOD_POST);
				this.displayHtml = new HTMLPanel(regionsAddHtml);
			    this.postForm.add(this.displayHtml);
				super.setContentPanel(this.postForm);
				this.fillSubmitControls();
			} else {
				this.displayHtml = new HTMLPanel(regionsListHtml);
				super.setContentPanel(this.displayHtml);
			}
		}	
		super.fill();
	}
	
	@Override
	public void fillSubmitControls() {
		if(this.getRequestContext().getMethodTypeCtx() == RequestContext.METHOD_POST) {
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
	
	final static String regionsListHtml = "";
	final static String regionsAddHtml = "<h1>Add Regions</h1>" +
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
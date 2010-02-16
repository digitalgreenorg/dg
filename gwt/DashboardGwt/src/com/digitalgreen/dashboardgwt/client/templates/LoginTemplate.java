package com.digitalgreen.dashboardgwt.client.templates;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.servlets.Login;
import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.Button;
import com.google.gwt.user.client.ui.FormPanel;
import com.google.gwt.user.client.ui.HTMLPanel;
import com.google.gwt.user.client.ui.RootPanel;

public class LoginTemplate extends Template {
	private FormPanel postForm = null;
	private HTMLPanel formHtml = null;
	
	public LoginTemplate(RequestContext requestContext) {
		super(requestContext);
	}
	
	public FormPanel getPostForm() {
		return this.postForm;
	}

	@Override
	public void fill() {
		super.setBodyStyle("login");
		this.postForm = new FormPanel();
		this.postForm.setAction(RequestContext.getServerUrl() + "admin/");
	    this.postForm.setEncoding(FormPanel.ENCODING_MULTIPART);
	    this.postForm.setMethod(FormPanel.METHOD_POST);
	    HTMLPanel formHtml = new HTMLPanel(loginHtml);
	    this.postForm.add(formHtml);
		RootPanel.get().add(this.getPostForm());
		this.fillSubmitControls();
	}
	
	public void fillSubmitControls() {
		Button b = Button.wrap(RootPanel.get("submit-button").getElement());
	    b.addClickHandler(new ClickHandler() {
			public void onClick(ClickEvent event) {
				Login login = new Login(new RequestContext(RequestContext.METHOD_POST, 
													   	   getPostForm()));
				login.response();
			}
	    });	
	}

	final static private String loginHtml = "<div id='container'>" +
					"<!-- Header -->" +
					"<div id='header'>" +
						"<div id='branding'>" +
							"<h1 id='site-name'>Digital Green administration</h1>" +
						"</div>" +
					"</div>" +
					"<div id='content' class='colM'>" +
						"<div id='content-main'>" +
							"<div class='form-row'>" +
								"<label for='id_username'>Username:</label> <input type='text' name='username' id='id_username' />" +
							"</div>" +
							"<div class='form-row'>" +
    							"<label for='id_password'>Password:</label> <input type='password' name='password' id='id_password' />" +
    						"</div>" +
    						"<div class='submit-row'>" +
    							"<label> </label>" +
    							"<input id='submit-button' type='submit' value='Log in'/>" +
    						"</div>" +
    					"</div>" +
    				"</div>" +
    			"</div>";
}

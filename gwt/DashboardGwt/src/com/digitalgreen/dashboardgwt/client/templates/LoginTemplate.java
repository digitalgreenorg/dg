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

public class LoginTemplate extends BaseTemplate {
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
		this.postForm = new FormPanel();
		this.postForm.setAction(RequestContext.getServerUrl() + "admin/");
	    this.postForm.setEncoding(FormPanel.ENCODING_MULTIPART);
	    this.postForm.setMethod(FormPanel.METHOD_POST);
	    HTMLPanel formHtml = new HTMLPanel(loginHtml);
	    this.postForm.add(formHtml);
		super.setContentPanel(this.postForm);
	    super.fill();
	    this.fillSubmitControls();
	}

	@Override
	public void fillSubmitControls() {
		// Add submit controls html here
		Button b = new Button("Login");
	    b.setStyleName("submit-row");
	    b.addClickHandler(new ClickHandler() {
			public void onClick(ClickEvent event) {
				Login login = new Login(new RequestContext(RequestContext.METHOD_POST, 
													   	   getPostForm()));
				login.response();
			}
	    });
	    super.setSubmitControlsPanel(b);
	    RootPanel.get("content").add(b);
	}

	final static private String loginHtml = "<div id='content' class='colM'>" +
						"<h1>Login</h1>" +
						"<div id='content-main'></div>" +
						"<div class='form-row'>" +
    						"<label for='id_username'>Username:</label> <input type='text' name='username' id='id_username' />" +
						"</div>" +
    					"<div class='form-row'>" +
    						"<label for='id_password'>Password:</label> <input type='password' name='password' id='id_password' />" +
    					"</div>" +
    					"</div>";
}

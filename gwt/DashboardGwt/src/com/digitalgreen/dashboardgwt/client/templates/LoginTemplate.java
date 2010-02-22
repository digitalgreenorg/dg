package com.digitalgreen.dashboardgwt.client.templates;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.servlets.Login;
import com.google.gwt.core.client.JavaScriptException;
import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.json.client.JSONException;
import com.google.gwt.json.client.JSONObject;
import com.google.gwt.json.client.JSONParser;
import com.google.gwt.json.client.JSONValue;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.Button;
import com.google.gwt.user.client.ui.FormPanel;
import com.google.gwt.user.client.ui.HTMLPanel;
import com.google.gwt.user.client.ui.RootPanel;
import com.google.gwt.core.client.JsArray;

public class LoginTemplate extends Template {
	private FormPanel postForm = null;
	private HTMLPanel formHtml = null;
	private HTMLPanel baseHtml = null;
	
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
		this.postForm.getElement().setId("login-form");
		this.postForm.setAction(RequestContext.getServerUrl() + "admin/");
	    this.postForm.setEncoding(FormPanel.ENCODING_MULTIPART);
	    this.postForm.setMethod(FormPanel.METHOD_POST);
	    baseHtml = new HTMLPanel(loginHtml); 
	    postForm.add(baseHtml);
	    RootPanel.get().add(postForm);
	    this.fillSubmitControls();
	}
	
	public void fillSubmitControls() {
		Button b = Button.wrap(RootPanel.get("submit-button").getElement());
		final String id = this.postForm.getElement().getId();
	    b.addClickHandler(new ClickHandler() {
			public void onClick(ClickEvent event) {
				Window.alert("BEFORE setupDg");
				Login login = new Login(BaseTemplate.setupDgPostContext(id));
				login.response();
			}
	    });
	}

	final static private String loginHtml =
		"<link rel='stylesheet' type='text/css' href='/media/css/login.css' />"+
		"<div id='container'>" + 
			"<div id='header'>"+
    			"<div id='branding'>"+
    				"<h1 id='site-name'>Digital Green administration</h1>"+
    			"</div>"+
    		"</div>"+
    		"<div id='content' class='colM'>"+
    			"<div id='content-main'>" +
    				"<div class='form-row'>"+
    					"<label for='id_username'>Username:</label> <input type='text' name='username' id='id_username' />"+
    				"</div>" +
    				"<div class='form-row'>"+
						"<label for='id_password'>Password:</label> <input type='password' name='password' id='id_password' />"+
						"<input type='hidden' name='this_is_the_login_form' value='1' />"+
					"</div>"+
					"<div class='submit-row'>"+
						"<label>&nbsp;</label><input id='submit-button' type='submit' value='Log in' />"+
					"</div>" +
    			"</div>"+
	    		"<br class='clear' />"+
	    	"</div>"+    
	    "</div>";
}

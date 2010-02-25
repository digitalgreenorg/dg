package com.digitalgreen.dashboardgwt.client.templates;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.LoginData;
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
	private HTMLPanel baseHtml = null;
	private Form loginAddForm = null;
	
	public LoginTemplate(RequestContext requestContext) {
		super(requestContext);
		// TODO:  Instantiate all possible form templates.  Enable this.
		// this.loginAddForm = new Form((new LoginData()).getData());
	}

	private Form getLoginAddForm() {
		// TODO Auto-generated method stub
		return this.loginAddForm; 
	}
	
	@Override
	public void fill() {
		super.setBodyStyle("login");
		this.postForm = new FormPanel();
		this.postForm.getElement().setId("login-form");
		this.postForm.setEncoding(FormPanel.ENCODING_MULTIPART);
	    this.postForm.setMethod(FormPanel.METHOD_POST);
	    this.baseHtml = new HTMLPanel(loginHtml); 
	    postForm.add(this.baseHtml);
	    RootPanel.get().add(this.postForm);
	    super.fill();
	    this.fillSubmitControls();
	}
	
	public void fillSubmitControls() {
		Button b = Button.wrap(RootPanel.get("submit-button").getElement());
		final String id = this.postForm.getElement().getId();
	    b.addClickHandler(new ClickHandler() {
			public void onClick(ClickEvent event) {
				RequestContext requestContext = new RequestContext(RequestContext.METHOD_POST);
				String formQueryString = BaseTemplate.getFormString("login-form");
				// TODO:  Finish the form implementation before doing this
				requestContext.setQueryString(formQueryString);
				Login login = new Login(requestContext);
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
    		"<div id='error-space'></div>" +
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

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
	private HTMLPanel baseHtml = null;
	
	public LoginTemplate(RequestContext requestContext) {
		super(requestContext);
	}
	
	public FormPanel getPostForm() {
		return this.postForm;
	}
	
	//public native static void test() /*-{
	//	<link rel='stylesheet' type='text/css' href='/media/css/login.css' />
	//}-*/;
	

	@Override
	public void fill() {
		super.setBodyStyle("login");
		this.postForm = new FormPanel();
		this.postForm.setAction(RequestContext.getServerUrl() + "admin/");
	    this.postForm.setEncoding(FormPanel.ENCODING_MULTIPART);
	    this.postForm.setMethod(FormPanel.METHOD_POST);
	    baseHtml = new HTMLPanel(loginHtml); 
	    formHtml = new HTMLPanel(login);
	    postForm.add(formHtml);
	    RootPanel.get().add(baseHtml);
	    RootPanel.get("content-main").add(postForm);
	    //this.postForm.add(formHtml);
		//RootPanel.get().add(this.getPostForm());
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

	final static private String loginHtml =
		"<link rel='stylesheet' type='text/css' href='/media/css/login.css' />"+
		"<div id='container'>" + 
			"<div id='header'>"+
    			"<div id='branding'>"+
    				"<h1 id='site-name'>Digital Green administration</h1>"+
    			"</div>"+
    		"</div>"+
    		"<div id='content' class='colM'>"+
    			"<div id='content-main'></div>"+
	    		"<br class='clear' />"+
	    	"</div>"+    
	    "</div>";
		
		
		
		
		
		/*"<div id='container'>" +
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
    			"</div>";*/
	
	final static private String login =	
			"<div class='form-row'>"+
				"<label for='id_username'>Username:</label> <input type='text' name='username' id='id_username' />"+
			"</div>"+
			"<div class='form-row'>"+
				"<label for='id_password'>Password:</label> <input type='password' name='password' id='id_password' />"+
				"<input type='hidden' name='this_is_the_login_form' value='1' />"+
			"</div>"+
			"<div class='submit-row'>"+
				"<label>&nbsp;</label><input id='submit-button' type='submit' value='Log in' />"+
			"</div>";
		
		
		
		/*	"<div id='container'>" + 
				"<div id='header'>"+
	        		"<div id='branding'>"+
	        			"<h1 id='site-name'>Digital Green administration</h1>"+
	        		"</div>"+
	        	"</div>"+
	    	    "<div id='content' class='colM'>"+
	    	    	"<div id='content-main'>"+
	    	    		"<div class='form-row'>"+
	    	    			"<label for='id_username'>Username:</label> <input type='text' name='username' id='id_username' />"+
	    	    		"</div>"+
	    	    		"<div class='form-row'>"+
	    	    			"<label for='id_password'>Password:</label> <input type='password' name='password' id='id_password' />"+
	    	    			"<input type='hidden' name='this_is_the_login_form' value='1' />"+
	    	    		"</div>"+
	    	    		"<div class='submit-row'>"+
	    	    			"<label>&nbsp;</label><input id='submit-button' type='submit' value='Log in' />"+
	    	    		"</div>"+
	    	    	"</div>"+        
	    	    	"<br class='clear' />"+
	    	    "</div>"+    
	    	"</div>"; */
	

		
	
}

package com.digitalgreen.dashboardgwt.client.templates;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.servlets.BaseServlet;
import com.digitalgreen.dashboardgwt.client.servlets.Login;
import com.google.gwt.dom.client.Element;
import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.event.logical.shared.ValueChangeEvent;
import com.google.gwt.event.logical.shared.ValueChangeHandler;
import com.google.gwt.user.client.History;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.Button;
import com.google.gwt.user.client.ui.FormPanel;
import com.google.gwt.user.client.ui.Hyperlink;
import com.google.gwt.user.client.ui.Label;
import com.google.gwt.user.client.ui.Panel;
import com.google.gwt.user.client.ui.HTMLPanel;
import com.google.gwt.user.client.ui.RootPanel;

public class BaseTemplate extends Template {
	private Panel baseContentHtmlPanel;
	protected FormPanel postForm = null;
	protected HTMLPanel displayHtml = null;
	protected Label usrStr = new Label();
	protected Label errMsg = new Label();
	String historyToken = "";	
	
	public BaseTemplate(RequestContext requestContext) {
		super(requestContext);
		initUI();
	}
	
	private void initUI() {
		this.baseContentHtmlPanel = new HTMLPanel(BaseContentHtml);
		RootPanel.get().insert(this.baseContentHtmlPanel, 0);
	}
	
	public FormPanel getPostForm() {
		return this.postForm;
	}
	
	public void setContentClassName(String className) {
		RootPanel.get("content").setStyleName(className);
	}
	
	public void setUserLable(String usr){
		this.usrStr.setText(usr);
	}
	
	public String getUserLabel(){
		return this.usrStr.getText();
	}
	
	public void setErrMsg(String msg){
		this.errMsg.setText(msg);
	}
	
	public String getErrMsg(){
		return this.errMsg.getText();
	}
	
	public void setHistoryToken(String token){
		this.historyToken = token;
	}
	
	public String getHistoryToken(){
		return this.historyToken;
	}
	
	@Override
	public void fill() {
		RootPanel.get("user-name").add(new HTMLPanel("b", this.getRequestContext().getDefaultLoggedInUserArg() + "."));
		RootPanel.get("logout").insert(logoutHyperlink(), 0);
		RootPanel.get("container").add(this.getContentPanel());
		super.fill();
	}
	
	protected void fillDGLinkControls(String templateType,
									  String templatePlainType,
								      String inputListFormHtml, 
								      final BaseServlet servlet) {
		HashMap queryArgs = this.getRequestContext().getArgs();
		String queryArg = (String)queryArgs.get("action");
		// If we're unsure, just default to list view
		if(queryArg == null || queryArg != "add") {
			HTMLPanel listFormHtml = new HTMLPanel(inputListFormHtml);
			RootPanel.get("listing-form-body").insert(listFormHtml, 0);
			Hyperlink addLink = new Hyperlink();
			addLink.setHTML("<a class='addlink' href='#" + 
					templateType + 
					"'> Add " + templatePlainType + "</a>");
			// Take them to the add page for screenings
			addLink.addClickHandler(new ClickHandler() {
				public void onClick(ClickEvent event) {
					Template.addLoadingMessage();
					servlet.response();
				}
			});
			RootPanel.get("add-link").add(addLink);			
		}
	}
	
	protected void fillDGTemplate(String templateType, 
								  String listHtml,
								  String addHtml) {
		super.setBodyStyle("dashboard-screening change-form");
		HashMap queryArgs = this.getRequestContext().getArgs();
		String queryArg = (String)queryArgs.get("action");
		String requestMethod = this.getRequestContext().getMethodTypeCtx();
		if(requestMethod == RequestContext.METHOD_GET) {
			if(queryArg == "add") {
				this.postForm = new FormPanel();
				this.postForm.getElement().setId("add-form");
				this.postForm.setAction(RequestContext.getServerUrl() + 
						"add_" + 
						templateType);
				this.postForm.setEncoding(FormPanel.ENCODING_MULTIPART);
				this.postForm.setMethod(FormPanel.METHOD_POST);
				this.displayHtml = new HTMLPanel(addHtml);
				this.postForm.add(this.displayHtml);
				super.setContentPanel(this.postForm);
			}else {
				this.displayHtml = new HTMLPanel(listHtml);
				
				super.setContentPanel(this.displayHtml);
			}
		}	
	}
	
	
	
	protected void fillDGSubmitControls(final BaseServlet servlet) {
		if(this.getRequestContext().getMethodTypeCtx() == RequestContext.METHOD_GET) {
			Button b = Button.wrap(RootPanel.get("save").getElement());
			
			//b.addStyleName(".button.default, input.default[type=\"submit\"], .submit-row input.default ");
		    b.addClickHandler(new ClickHandler() {
				public void onClick(ClickEvent event) {
					Template.addLoadingMessage();
					// The query string can only be formed if we're on the page with 
					// the add-form id, set when we got a GET request on the page
					String formQueryString = BaseTemplate.getFormString("add-form");
					servlet.getRequestContext().setQueryString(formQueryString);
					servlet.response();
				}
		    });
		}
	}
	
	private Hyperlink logoutHyperlink(){
		Hyperlink link = new Hyperlink("<a href='#/logout'>Log out</a>", true, null);
		link.setStyleName("logoutClass");
		link.addClickHandler(new ClickHandler() {
			public void onClick(ClickEvent event) {
				RequestContext requestContext = new RequestContext(RequestContext.METHOD_POST);
				requestContext.getArgs().put("action", "logout");
				Login login = new Login(requestContext);
				login.response();
			}
		});
		
		return link;
	}
	
	public static native String getForm(String formId) /*-{
		return $wnd.getFormHtml(formId);
	}-*/;

	public static native String getFormString(String formId) /*-{
		return $wnd.getFormString(formId);
	}-*/;
		
	public static native String populateForm(String formId, String queryString) /*-{
		return $wnd.populateForm(formId, queryString);
	}-*/;
	
	final String BaseContentHtml = "<!-- Container -->" +
	"<div id='container'>" +
		"<!-- Header -->" +
		"<div id='header'>" +
			"<div id='branding'>" +
				"<h1 id='site-name'>Digital Green Administration</h1>" +
			"</div>" +
			"<div id='user-tools'>Welcome, <span id='user-name'></span>" +
			"<span id='logout'></span>" +
			"</div>" +
		"</div>" +
		"<div id='error-space'></div>" +
		"<!-- END Header -->" +
		"<!-- Content -->" +                 // Content gets added by subclasses
		"<!-- Submit Button -->" +           // For now gets added by subclasses
		"</div>" +
		"<!-- END Content -->" +
		"<div id='footer'></div>" +
	"</div>" +
	"<!-- END Container -->";
}
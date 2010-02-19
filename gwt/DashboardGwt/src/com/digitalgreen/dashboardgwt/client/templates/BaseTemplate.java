package com.digitalgreen.dashboardgwt.client.templates;

import java.util.HashMap;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.servlets.BaseServlet;
import com.digitalgreen.dashboardgwt.client.servlets.Login;
import com.digitalgreen.dashboardgwt.client.servlets.Regions;
import com.digitalgreen.dashboardgwt.client.servlets.Screenings;
import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.Button;
import com.google.gwt.user.client.ui.FocusWidget;
import com.google.gwt.user.client.ui.FormPanel;
import com.google.gwt.user.client.ui.Hyperlink;
import com.google.gwt.user.client.ui.Panel;
import com.google.gwt.user.client.ui.HTMLPanel;
import com.google.gwt.user.client.ui.RootPanel;
import com.google.gwt.user.client.ui.VerticalPanel;
import com.google.gwt.user.client.ui.Widget;

public class BaseTemplate extends Template {
	private Panel baseContentHtmlPanel;
	protected FormPanel postForm = null;
	protected HTMLPanel displayHtml = null;
	
	public BaseTemplate(RequestContext requestContext) {
		super(requestContext);
		initUI();
	}
	
	private void initUI() {
		this.baseContentHtmlPanel = new HTMLPanel(BaseContentHtml);
		RootPanel.get().clear();
		RootPanel.get().insert(this.baseContentHtmlPanel, 0);
	}
	
	public FormPanel getPostForm() {
		return this.postForm;
	}
	
	public void setContentClassName(String className) {
		RootPanel.get("content").setStyleName(className);
	}
	
	@Override
	public void fill() {
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
		    b.addClickHandler(new ClickHandler() {
				public void onClick(ClickEvent event) {				
					servlet.response();
				}
		    });
		}
	}
	
	private Hyperlink logoutHyperlink(){
		Hyperlink link = new Hyperlink("<a href='/logout'>Logout</a>", true, null);
		link.addClickHandler(new ClickHandler() {
			public void onClick(ClickEvent event) {
				RequestContext requestContext = new RequestContext(RequestContext.METHOD_POST, getPostForm());
				requestContext.getArgs().put("action", "logout");
				Login login = new Login(requestContext);
				login.response();
			}
		});
		
		return link;
	}

	final String BaseContentHtml = "<!-- Container -->" +
	"<div id='container'>" +
		"<!-- Header -->" +
		"<div id='header'>" +
			"<div id='branding'>" +
				"<h1 id='site-name'>Digital Green Administration</h1>" +
			"</div>" +
			"<div id='user-tools'>" +
				"Welcome," +
				"<strong id='username'>digitalgreen</strong>." +
				"<label id='logout'>" +
				"</label>" +
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
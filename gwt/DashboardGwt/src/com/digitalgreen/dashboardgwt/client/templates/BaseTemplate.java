package com.digitalgreen.dashboardgwt.client.templates;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.ApplicationConstants;
import com.digitalgreen.dashboardgwt.client.common.Form;
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
import com.google.gwt.user.client.ui.HTML;
import com.google.gwt.user.client.ui.HorizontalPanel;
import com.google.gwt.user.client.ui.KeyboardListener;
import com.google.gwt.user.client.ui.KeyboardListenerAdapter;
import com.google.gwt.user.client.ui.ScrollPanel;
import com.google.gwt.user.client.ui.TextBox;
import com.google.gwt.user.client.ui.UIObject;
import com.google.gwt.user.client.ui.Hyperlink;
import com.google.gwt.user.client.ui.Label;
import com.google.gwt.user.client.ui.Panel;
import com.google.gwt.user.client.ui.HTMLPanel;
import com.google.gwt.user.client.ui.RootPanel;
import com.google.gwt.user.client.ui.VerticalPanel;
import com.google.gwt.user.client.ui.Widget;

public class BaseTemplate extends Template {
	private Panel baseContentHtmlPanel;
	protected FormPanel postForm = null;
	protected HTMLPanel displayHtml = null;
	protected Form formTemplate = null;

	public BaseTemplate() {
		super();
	}
	
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
	
	@Override
	public void fill() {
		RootPanel.get("user-name").add(new HTMLPanel("b", ApplicationConstants.getUsernameCookie() + "."));
		RootPanel.get("logout").insert(logoutHyperlink(), 0);
		RootPanel.get("sub-container").add(this.getContentPanel());
		super.fill();
	}
	
	protected void fillDgListPage(String templateType,
			  String templatePlainType,
		      String inputListFormHtml, 
		      final BaseServlet servlet, 
		      List<Hyperlink> links) {
		HashMap queryArgs = this.getRequestContext().getArgs();
		String queryArg = (String)queryArgs.get("action");
		//If we're unsure, just default to list view
		if(queryArg.equals("list")) {
			HTMLPanel listFormHtml = new HTMLPanel(inputListFormHtml);
			RootPanel.get("listing-form-body").insert(listFormHtml, 0);
			Hyperlink addLink = new Hyperlink();
			addLink.setHTML("<a class='addlink' href='#" + 
					templateType + 
					"'> Add " + templatePlainType + "</a>");
			// Take them to the add page
			addLink.addClickHandler(new ClickHandler() {
				public void onClick(ClickEvent event) {
					Template.addLoadingMessage();
					servlet.response();
				}
			});
			if(RootPanel.get("add-link")!=null)
				RootPanel.get("add-link").add(addLink);
			//End of Add new entity Link
			for(int i = 0; i < links.size(); i++){
				RootPanel.get("row"+i).add(links.get(i));
			}
			//SearchUI is Added only for some child templates
			if(RootPanel.get("search") != null) {
				final Button searchButton = Button.wrap(RootPanel.get("search").getElement());
				final TextBox searchBox = TextBox.wrap(RootPanel.get("searchbar").getElement());
				searchButton.addClickHandler(new ClickHandler() {
					public void onClick(ClickEvent event) {
						searchResponse(servlet, searchBox.getValue());
					}
			    });
				//To handle enter key for search text box
				searchBox.addKeyboardListener(new KeyboardListenerAdapter() {
				      public void onKeyPress(Widget sender, char keyCode, int modifiers) {
				        if (keyCode == (char) KEY_ENTER) {
				        	searchButton.click();
				        	((TextBox)sender).cancelKey();
				        }
				      }
				    });				
			}
		}
	}
	
	public void searchResponse(final BaseServlet servlet, final String searchVal) {
		Template.addLoadingMessage();
		RequestContext searchRequestContext = new RequestContext();
		searchRequestContext.getArgs().put("action","list");
		searchRequestContext.getArgs().put("operation","search");
		searchRequestContext.getArgs().put("pageNum","1");
		searchRequestContext.getArgs().put("searchText",searchVal);
		servlet.setRequestContext(searchRequestContext);
		servlet.response();
	}
	
	public Hyperlink createPageHyperlink(String linkText, String tokenText, final BaseServlet servlet, 
			final String pageNum, final String operation, final String searchText) {
		Hyperlink addLink = new Hyperlink(linkText, true, tokenText);
		addLink.addClickHandler(new ClickHandler() {
			public void onClick(ClickEvent event) {
				Template.addLoadingMessage();
				RequestContext paginationRequestContext = new RequestContext();
				if(operation == "search") {
					paginationRequestContext.getArgs().put("operation","search");
					paginationRequestContext.getArgs().put("searchText",searchText);
				}
				paginationRequestContext.getArgs().put("action","list");
				paginationRequestContext.getArgs().put("pageNum",pageNum);
				servlet.setRequestContext(paginationRequestContext);
				servlet.response();
			}
		});
		return addLink;
	}
	
	public Hyperlink createHyperlink(String linkText, String tokenText, final BaseServlet servlet){
		Hyperlink addLink = new Hyperlink(linkText, true, tokenText); 
		addLink.addClickHandler(new ClickHandler() {
				public void onClick(ClickEvent event) {
					Template.addLoadingMessage();
					servlet.response();
				}
			});
		return addLink;
	}
	
	protected void fillDGTemplate(String templateType, 
								  String listHtml,
								  String addHtml, String addDataToElementID[]) {
		super.setBodyStyle("dashboard-screening change-form");
		HashMap queryArgs = this.getRequestContext().getArgs();
		String queryArg = (String)queryArgs.get("action");
		if(queryArg.equals("add") || queryArg.equals("edit")) {
			this.postForm = new FormPanel();
			this.postForm.getElement().setId("add-form");
			this.postForm.setAction(RequestContext.getServerUrl() + 
					"add_" + 
					templateType);
			this.postForm.setEncoding(FormPanel.ENCODING_MULTIPART);
			this.postForm.setMethod(FormPanel.METHOD_POST);
			this.displayHtml = new HTMLPanel(addHtml);				
			String addData = (String)queryArgs.get("addPageData");
			if(addData != null && addDataToElementID != null && addDataToElementID.length > 0  ){
				HTMLPanel h = new HTMLPanel(addData);
				for(int i = 0; i< addDataToElementID.length;i++){
					this.displayHtml.getElementById(addDataToElementID[i]).setInnerHTML(h.getElementById(addDataToElementID[i]).getInnerHTML());
				}
			}
			this.postForm.add(this.displayHtml);
			super.setContentPanel(this.postForm);
		} else {
			this.displayHtml = new HTMLPanel(listHtml);				
			super.setContentPanel(this.displayHtml);
		}
	}	
	
	public static String createEditQueryString(String html){
		FormPanel form = new FormPanel();
		form.getElement().setId("tempEditForm");
		form.add(new HTMLPanel(html));
		HTMLPanel tempEditDiv = new HTMLPanel("<div id='tempEditDiv' style='display:none;'></div>");
		RootPanel.get("footer").insert(tempEditDiv,0);
		RootPanel.get("tempEditDiv").add(form);
		String queryString = BaseTemplate.getFormString("tempEditForm");
		RootPanel.get("tempEditDiv").removeFromParent();
		return queryString;
	}
	
	protected void fillDgFormPage(final BaseServlet servlet) {
		HashMap queryArgs = this.getRequestContext().getArgs();
		String queryArg = (String)queryArgs.get("action");
		if(this.getRequestContext().getMethodTypeCtx().equals(RequestContext.METHOD_GET) && 
				(queryArg.equals("add") || queryArg.equals("edit"))) {
			if(this.requestContext.getArgs().get("action").equals("edit")) {
				servlet.getRequestContext().getArgs().put("id", this.requestContext.getArgs().get("id"));
			}
			servlet.getRequestContext().getArgs().put("action", this.getRequestContext().getArgs().get("action"));
			Button b = Button.wrap(RootPanel.get("save").getElement());
			b.addClickHandler(new ClickHandler() {
				// This gets executed on a POST request.
				public void onClick(ClickEvent event) {
					Template.addLoadingMessage();
					// The query string can only be formed if we're on the page with 
					// the add-form id, set when we got a GET request on the page
					String formQueryString = BaseTemplate.getFormString("add-form");
					servlet.getRequestContext().getArgs().put("redirect_to", "list");
					servlet.getRequestContext().getForm().setQueryString(formQueryString);
					servlet.response();
				}
		    });
			// Fill up form with whatever's in the query string.
			String queryString = this.getRequestContext().getForm().getQueryString();
			if(queryString != null) {
				BaseTemplate.putFormString(queryString, "add-form");
			}
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
	
	public void showGlassDoorMessage(String htmlMsg) {
		BaseTemplate.showGlassDoorMessageJavascript(htmlMsg);
	}
	
	public static native void showGlassDoorMessageJavascript(String htmlMsg) /*-{
		return $wnd.showGlassDoorMessage(htmlMsg);
	}-*/;

	public void hideGlassDoorMessage() {
		BaseTemplate.hideGlassDoorMessageJavascript();
	}
	
	public static native void hideGlassDoorMessageJavascript() /*-{
		return $wnd.hideGlassDoorMessage();
	}-*/;

	// HTML form -> query string
	public static native String getFormString(String formId) /*-{
		return $wnd.getFormString(formId);
	}-*/;
	
	// Query string -> HTML form
	public static native String putFormString(String queryString, String formId) /*-{
		return $wnd.putFormString(queryString, formId);
	}-*/;
	
	
	final String BaseContentHtml = "<!-- Container -->" +
	"<div id='container'>" +
		"<!-- Header -->" +
		"<div id='header'>" +
			"<div id='branding'>" +
				"<h1 id='site-name'><a href='/coco/home.html'><img src='/media/img/admin/coco-logo.png' /></a></h1>" +
			"</div>" +
			"<div id='user-tools'>Welcome, <span id='user-name'></span>" +
			"<span id='logout'></span>" +
			"</div>" +
		"</div>" +
		"<div id='info-space'></div>" +
		"<div id='loading-space'></div>" +
		"<!-- END Header -->" +
		"<!-- Content -->" +                 // Content gets added by subclasses
		"<!-- Submit Button -->" +           // For now gets added by subclasses
		"<!-- END Content -->" +
		"<div id='sub-container' style='clear: both;'>" +
		"</div>" +
		"<div id='toolbar'></div>" +
		"<div id='pagination-footer'></div>" +
		"<div id='footer'></div>" +
		"<div id='box'></div>" +
		"<div id='screen'></div>" +
	"</div>" +
	"<!-- END Container -->";
}

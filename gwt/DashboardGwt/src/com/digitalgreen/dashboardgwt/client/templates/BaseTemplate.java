package com.digitalgreen.dashboardgwt.client.templates;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.servlets.BaseServlet;
import com.digitalgreen.dashboardgwt.client.servlets.Regions;
import com.digitalgreen.dashboardgwt.client.servlets.Screenings;
import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.FocusWidget;
import com.google.gwt.user.client.ui.Hyperlink;
import com.google.gwt.user.client.ui.Panel;
import com.google.gwt.user.client.ui.HTMLPanel;
import com.google.gwt.user.client.ui.RootPanel;
import com.google.gwt.user.client.ui.VerticalPanel;
import com.google.gwt.user.client.ui.Widget;

public class BaseTemplate extends Template {
	
	private Panel baseContentHtmlPanel;
	private Widget submitControlsPanel = null; // this is separate because separate in above HTML
	
	public BaseTemplate(RequestContext requestContext) {
		super(requestContext);
		initUI();
	}
	
	/*
	public void addHyperLinkHandler(String id, final BaseServlet gotoServlet) {
		//link.addClickHandler(new ClickHandler() {
			public void onClick(ClickEvent event) {
				gotoServlet.response();
			}
		});
	}
	 */
	
	private void initUI() {
		this.baseContentHtmlPanel = new HTMLPanel(BaseContentHtml);
		RootPanel.get().clear();
		RootPanel.get().insert(this.baseContentHtmlPanel, 0);
	}
	
	public RequestContext getRequestContext() {
		return this.requestContext;
	}
	
	public void setSubmitControlsPanel(Widget w) {
		this.submitControlsPanel = w;
	}
	
	public void setContentClassName(String className) {
		RootPanel.get("content").setStyleName(className);
	}
	
	// Override this
	@Override
	public void fill() {
		RootPanel.get("container").add(this.getContentPanel());
	}
	
	// Override this
	public void fillSubmitControls() {
		RootPanel.get("content").add(this.submitControlsPanel);
	}

	final String BaseContentHtml = "<!-- Container -->" +
	"<div id='container'>" +
		"<!-- Header -->" +
		"<div id='header'>" +
			"<div id='branding'>" +
				"<h1 id='site-name'>Digital Green administration</h1>" +
			"</div>" +
			"<div id='user-tools'>" +
				"Welcome," +
				"<strong>digitalgreen</strong>." +
				"<a href='/admin/logout/'>Log out</a>" +
			"</div>" +
		"</div>" +
		"<!-- END Header -->" +
		"<!-- Content -->" +                 // Content gets added by subclasses
		"<!-- Submit Button -->" +           // For now gets added by subclasses
		"</div>" +
		"<!-- END Content -->" +
		"<div id='footer'></div>" +
	"</div>" +
	"<!-- END Container -->";
}
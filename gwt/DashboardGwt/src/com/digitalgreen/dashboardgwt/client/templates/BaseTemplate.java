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

public class BaseTemplate {
	
	private Panel baseContentHtmlPanel;
	private Widget contentPanel = null;
	private Widget submitControlsPanel = null; // this is separate because separate in above HTML
	protected RequestContext requestContext = null;
	
	public BaseTemplate(RequestContext requestContext) {
		this.requestContext = requestContext;
		initUI();
	}
	
	private void addHyperLinkHandler(Hyperlink link, final BaseServlet gotoServlet) {
		link.addClickHandler(new ClickHandler() {
			public void onClick(ClickEvent event) {
				gotoServlet.response();
			}
		});
	}

	private void initUI() {
		this.baseContentHtmlPanel = new HTMLPanel(BaseContentHtml);
		RootPanel.get().clear();
		RootPanel.get().insert(this.baseContentHtmlPanel, 0);
		
		/*
		Hyperlink l1 = new Hyperlink("Animator assigned villages", true, "l1");
		addHyperLinkHandler(l1, new BaseServlet());
	    Hyperlink l2 = new Hyperlink("Animators", true, "l2");
	    addHyperLinkHandler(l2, new BaseServlet());
	    Hyperlink l3 = new Hyperlink("Blocks", true, "l3");
	    addHyperLinkHandler(l3, new BaseServlet());
	    Hyperlink l4 = new Hyperlink("Development managers", true, "l4");
	    addHyperLinkHandler(l4, new BaseServlet());
	    Hyperlink l5 = new Hyperlink("Districts", true, "l5");
	    addHyperLinkHandler(l5, new BaseServlet());
	    Hyperlink l6 = new Hyperlink("Equipments", true, "l6");
	    addHyperLinkHandler(l6, new BaseServlet());
	    Hyperlink l7 = new Hyperlink("Field officers", true, "l7");
	    addHyperLinkHandler(l7, new BaseServlet());
	    Hyperlink l8 = new Hyperlink("Languages", true, "l8");
	    addHyperLinkHandler(l8, new BaseServlet());
	    Hyperlink l9 = new Hyperlink("Partners", true, "l9");
	    addHyperLinkHandler(l9, new BaseServlet());
	    Hyperlink l10 = new Hyperlink("Person groups", true, "l10");
	    addHyperLinkHandler(l10, new BaseServlet());
	    Hyperlink l11 = new Hyperlink("Persons", true, "l11");
	    addHyperLinkHandler(l11, new BaseServlet());
	    Hyperlink l12 = new Hyperlink("Practices", true, "l12");
	    addHyperLinkHandler(l12, new BaseServlet());
	    Hyperlink l13 = new Hyperlink("Regions", true, "l13");
	    addHyperLinkHandler(l13, new Regions());
	    Hyperlink l14 = new Hyperlink("Screenings", true, "l14");
	    addHyperLinkHandler(l14, new Screenings());
	    Hyperlink l15 = new Hyperlink("States", true, "l15");
	    addHyperLinkHandler(l15, new BaseServlet());
	    Hyperlink l16 = new Hyperlink("Trainings", true, "l16");
	    addHyperLinkHandler(l16, new BaseServlet());
	    Hyperlink l17 = new Hyperlink("Videos", true, "l17");
	    addHyperLinkHandler(l17, new BaseServlet());
	    Hyperlink l18 = new Hyperlink("Villages", true, "l18");
	    addHyperLinkHandler(l18, new BaseServlet());
	    
	    VerticalPanel panel = new VerticalPanel();
	    panel.add(l1);
	    panel.add(l2);
	    panel.add(l3);
	    panel.add(l4);
	    panel.add(l5);
	    panel.add(l6);
	    panel.add(l7);
	    panel.add(l8);
	    panel.add(l9);
	    panel.add(l10);
	    panel.add(l11);
	    panel.add(l12);
	    panel.add(l13);
	    panel.add(l14);
	    panel.add(l15);
	    panel.add(l16);
	    panel.add(l17);
	    panel.add(l18);
	    RootPanel.get("panel-listings").add(panel);
	    RootPanel.get("panel-listings").setStyleName("panelListing");
		*/
	}
	
	public RequestContext getRequestContext() {
		return this.requestContext;
	}
	
	public void setBodyStyle(String styleName) {
		RootPanel.get().setStyleName(styleName);
	}	
	public void setContentPanel(Widget w) {
		this.contentPanel = w;
	}
	
	public void setSubmitControlsPanel(Widget w) {
		this.submitControlsPanel = w;
	}
	
	public void setContentClassName(String className) {
		RootPanel.get("content").setStyleName(className);
	}
	
	// Override this
	public void fill() {
		RootPanel.get("container").add(this.contentPanel);
	}
	
	// Override this
	public void fillSubmitControls() {
		RootPanel.get("container").add(this.submitControlsPanel);
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
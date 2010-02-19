package com.digitalgreen.dashboardgwt.client.templates;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.google.gwt.user.client.ui.HTMLPanel;
import com.google.gwt.user.client.ui.RootPanel;
import com.google.gwt.user.client.ui.Widget;

public class Template implements TemplateInterface {

	protected RequestContext requestContext = null;
	private Widget contentPanel = null;
	
	public Template(RequestContext requestContext) {
		this.requestContext = requestContext;
		RootPanel.get().clear();
	}
	
	public void fill() {
		RootPanel.get("error-space").clear();
		if(this.getRequestContext().hasMessages()) {
			String messageStartHtml = "<p class='errornote'>";
			String messageEndHtml = "</p>";
			HTMLPanel messagePanel = new HTMLPanel(messageStartHtml + 
					this.getRequestContext().getMessageString() + 
					messageEndHtml);
			RootPanel.get("error-space").add(messagePanel);
		}
	}

	public RequestContext getRequestContext() {
		return this.requestContext;
	}
	
	public Widget getContentPanel() {
		return this.contentPanel;
	}
	
	public void setContentPanel(Widget w) {
		this.contentPanel = w;
	}
	
	public void setBodyStyle(String styleName) {
		RootPanel.get().setStyleName(styleName);
	}
}

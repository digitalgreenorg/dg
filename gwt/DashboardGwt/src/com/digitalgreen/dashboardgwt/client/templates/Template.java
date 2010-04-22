package com.digitalgreen.dashboardgwt.client.templates;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.google.gwt.user.client.Window;
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
	
	private HTMLPanel getFormattedErrors() {
		Window.alert("getFormattedErrors");
		String errorStartHtml = "<p class='errornote'>";
		String errorEndHtml = "</p>";
		HTMLPanel errorPanel = new HTMLPanel(errorStartHtml + 
				this.getRequestContext().getErrorMessage() + 
				errorEndHtml);
		return errorPanel;
	}
	
	private HTMLPanel getFormattedMessages() {
		Window.alert("getFormattedMessages");
		String messageStartHtml = "<p class='messageStringClass'>";
		String messageEndHtml = "</p>";
		HTMLPanel messagePanel = new HTMLPanel(messageStartHtml + 
				this.getRequestContext().getMessage() + 
				messageEndHtml);
		return messagePanel;
	}
	
	public void fill() {
		if( this.getRequestContext().hasErrorMessages()) {
			RootPanel.get("info-space").insert(this.getFormattedErrors(), 0);	
		} else if(this.getRequestContext().hasMessages()) {
			RootPanel.get("info-space").insert(this.getFormattedMessages(), 0);
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

	private static void addSpinnerMessage(String message) {
		try {
			HTMLPanel imageHtml = new HTMLPanel("<img src='/media/img/admin/ajax-loader.gif' /> ");	
			imageHtml.setStyleName("messageSpinnerClass");
			HTMLPanel messageHtml = new HTMLPanel(message);
			messageHtml.setStyleName("messageSpinnerDivClass");
			RootPanel.get("loading-space").insert(imageHtml, 0);
			RootPanel.get("loading-space").insert(messageHtml, 1);
		} catch (Exception e) {}
	}
	
	public static void addLoadingMessage() {
		addSpinnerMessage("Loading...");
	}
	
	public static void addLoadingMessage(String message) {
		addSpinnerMessage(message);	
	}
}
package com.digitalgreen.dashboardgwt.client;

import com.digitalgreen.dashboardgwt.client.servlets.AnimatorAssignedVillages;
import com.digitalgreen.dashboardgwt.client.servlets.BaseServlet;
import com.google.gwt.event.logical.shared.ValueChangeEvent;
import com.google.gwt.event.logical.shared.ValueChangeHandler;
import com.google.gwt.user.client.History;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.RootPanel;
import com.digitalgreen.dashboardgwt.client.templates.BaseTemplate;
//import com.digitalgreen.dashboardgwt.client.DashboardGwt;

public class MyHistoryListener implements ValueChangeHandler<String> {

	public void onValueChange(ValueChangeEvent<String> event) {
		// TODO redirect to corresponding servlets
		
		//Window.alert("Current State: " + event.getValue());
		
//		Object token  = new Object();
//		token = event.getValue();
//		BaseServlet serv = (BaseServlet)DashboardGwt.getHashValue(token.toString());
//		serv.response();
//		//Window.alert("serv" + DashboardGwt.getHashValue(token.toString()).toString());
//		Window.alert("aftr serv");
	}
}

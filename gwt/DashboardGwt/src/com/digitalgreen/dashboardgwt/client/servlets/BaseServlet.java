package com.digitalgreen.dashboardgwt.client.servlets;

import java.util.Arrays;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.servlets.ServletInterface;
import com.digitalgreen.dashboardgwt.client.templates.BaseTemplate;
import com.digitalgreen.dashboardgwt.client.templates.Template;
import com.google.gwt.user.client.Cookies;

public class BaseServlet implements ServletInterface {
	
	protected RequestContext requestContext = null;	
	private boolean isLoggedInCtx = false;
	
	// Slightly breaks abstraction since the RequestContext should be 
	// created in the template as a GET request, similar to how 
	// POSTs work.
	public BaseServlet() {
		this.requestContext = new RequestContext();
	}
	
	public BaseServlet(RequestContext requestContext) {
		this.requestContext = requestContext;
	}
	
	protected String getMethodTypeCtx() {
		return this.requestContext.getMethodTypeCtx();
	}
	
	public boolean isLoggedIn() {
		return this.isLoggedInCtx;
	}
	
	public void setIsLoggedIn(boolean loggedIn) {
		this.isLoggedInCtx = loggedIn;
	}
	
	public void redirectTo(BaseServlet servlet) {
		servlet.response();
	}

	public void fillTemplate(Template template) {
		template.fill();
	}
	
	// Override this
	public void response() {
		String loggedInCtx = Cookies.getCookie("sessionid");
		// Must have a cookie
		if(loggedInCtx == null || loggedInCtx == "") {
			this.setIsLoggedIn(false);
		} else {
			this.setIsLoggedIn(true);
		}
	}
}
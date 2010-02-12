package com.digitalgreen.dashboardgwt.client.servlets;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.servlets.ServletInterface;
import com.digitalgreen.dashboardgwt.client.templates.BaseTemplate;
import com.google.gwt.user.client.Cookies;

public class BaseServlet implements ServletInterface {
	
	protected RequestContext requestContext;
	protected String cookieValueCtx = null;
	private boolean isLoggedInCtx = false;
	
	public BaseServlet() {
		this.requestContext = new RequestContext();
	}
	
	public BaseServlet(RequestContext requestContext) {
		this.requestContext = requestContext;
	}
	
	protected String getCookieValueCtx() {
		return this.cookieValueCtx;
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

	public void fillTemplate(BaseTemplate template) {
		template.fill();
	}
	
	//Override this
	public void response() {
		this.cookieValueCtx = Cookies.getCookie("sessionid");
		if(this.cookieValueCtx == null) {
			this.setIsLoggedIn(false);
		}
	}
}
package com.digitalgreen.dashboardgwt.client.servlets;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.LoginData;
import com.digitalgreen.dashboardgwt.client.servlets.BaseServlet;
import com.digitalgreen.dashboardgwt.client.templates.LoginTemplate;

public class Login extends BaseServlet {	
	
	public Login() {
		super();
	}
	
	public Login(RequestContext requestContext) {
		super(requestContext);
	}
	
	@Override
	public void response() {
		super.response();
		String method = this.getMethodTypeCtx();
		String cookieValue = this.getCookieValueCtx();
		
		if(this.isLoggedIn()) {
			super.redirectTo(new Index());
		}
		
		if(cookieValue != null && method == RequestContext.METHOD_POST) {
			// Do stuff with posted from coming from template
			// Do a bunch of model layer work here; check username/password info and
			// depending on credentials redirect to Index or back to Login
			super.redirectTo(new Index());
		} else if (method == RequestContext.METHOD_GET) {
			// Most likely do nothing in this GET case
			this.requestContext.setFormAction(LoginData.getFormAction());
			this.fillTemplate(new LoginTemplate(this.requestContext));
		}
	}
}
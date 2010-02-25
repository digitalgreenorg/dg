package com.digitalgreen.dashboardgwt.client.servlets;


import java.util.HashMap;

import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.LoginData;
import com.digitalgreen.dashboardgwt.client.servlets.BaseServlet;
import com.digitalgreen.dashboardgwt.client.templates.LoginTemplate;
import com.google.gwt.user.client.Cookies;
import com.google.gwt.user.client.Window;

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
		
		if(this.isLoggedIn()) {
			super.redirectTo(new Index());
		}

		if(method == RequestContext.METHOD_POST) {
			// - authenticate by checking backend
			// - get some user data like role and set in cookie
			// - set cookie if auth successful
			// - redirect to index
			HashMap queryArgs = (HashMap)this.requestContext.getArgs();
			String queryArg = (String)queryArgs.get("action");
			if(queryArg == "logout"){
				Cookies.removeCookie("username");
				this.redirectTo(new Login());
			} else {
				LoginData loginData = new LoginData(new OnlineOfflineCallbacks(this) {
					public void onlineSuccessCallback(String results) {
						if(results == "1") {
							Cookies.setCookie("username", (String)getServlet().form.get("username"));
							getServlet().redirectTo(new Index());
						} else {
							RequestContext requestContext = new RequestContext();
							requestContext.setMessageString("Invalid credentials, please try again.");
							getServlet().redirectTo(new Login(requestContext));				
						}
					}
					
					public void onlineErrorCallback() {
						RequestContext requestContext = new RequestContext();
						requestContext.setMessageString("There was an internal error.  Please contact support.");
						getServlet().redirectTo(new Login(requestContext));				
					}
					
					public void offlineSuccessCallback(Object results) {
						// If login success in the offline case
						if((Boolean)results) {
							Cookies.setCookie("username", (String)getServlet().form.get("username"));
							getServlet().redirectTo(new Index());
						} else {
							RequestContext requestContext = new RequestContext();
							requestContext.setMessageString("Invalid credentials, please try again");
							getServlet().redirectTo(new Login(requestContext));				
						}
					}
				});
				loginData.apply(loginData.authenticate((String)this.form.get("username"),
						(String)this.form.get("password")));
			}
		} else if (method == RequestContext.METHOD_GET) {
			// Most likely do nothing in this GET case
			this.fillTemplate(new LoginTemplate(this.requestContext));
		}
	}
}
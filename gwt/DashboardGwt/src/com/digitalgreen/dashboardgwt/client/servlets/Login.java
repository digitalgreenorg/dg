package com.digitalgreen.dashboardgwt.client.servlets;


import java.util.HashMap;

import com.digitalgreen.dashboardgwt.client.common.ApplicationConstants;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.BaseData;
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
		if(method.equals(RequestContext.METHOD_POST)) {
			HashMap queryArgs = (HashMap)this.requestContext.getArgs();
			String queryArg = (String)queryArgs.get("action");
			if(queryArg.equals("logout")){
				ApplicationConstants.deleteCookies();
				this.redirectTo(new Login());
			} else {
				    LoginData loginData = new LoginData(new OnlineOfflineCallbacks(this) {
					public void onlineSuccessCallback(String results) {
						if(results.equals("1")) {
							ApplicationConstants.setLoginCookies((String)getServlet().form.get("username"),
									(String)getServlet().form.get("password"));
							getServlet().redirectTo(new Index());
						} else {
							RequestContext requestContext = new RequestContext();
							requestContext.setMessage("Invalid credentials, please try again.");
							getServlet().redirectTo(new Login(requestContext));				
						}
					}
					
					public void onlineErrorCallback(int errorCode) {
						RequestContext requestContext = new RequestContext();
						if (errorCode == BaseData.ERROR_RESPONSE)
							requestContext.setMessage("Unresponsive Server.  Please contact support.");
						else if (errorCode == BaseData.ERROR_SERVER)
							requestContext.setMessage("Problem in the connection with the server.");
						else
							requestContext.setMessage("Unknown error.  Please contact support.");
						getServlet().redirectTo(new Login(requestContext));			
						
					}
					
					public void offlineSuccessCallback(Object results) {
						// If login success in the offline case
						if((Boolean)results) {
							ApplicationConstants.setLoginCookies((String)getServlet().form.get("username"),
									(String)getServlet().form.get("password"));
							getServlet().redirectTo(new Index());
						} else {
							RequestContext requestContext = new RequestContext();
							requestContext.setMessage("Invalid credentials, please try again");
							getServlet().redirectTo(new Login(requestContext));	
						}
					}
				});
				    
				// Comment the below line when you are not running the code form a hosted mode.   
				loginData.apply(loginData.authenticate((String)this.form.get("username"),(String)this.form.get("password")));
				 
				// Comment the below line when you are running the code form a hosted mode.
				// ApplicationConstants.setLoginCookies((String)getServlet().form.get("username"),
				// (String)getServlet().form.get("password"));
				// this.redirectTo(new Index());

			}
		} else if (method.equals(RequestContext.METHOD_GET)) {
			if(this.isLoggedIn()) {
				super.redirectTo(new Index());
			}
			else{
				// Most likely do nothing in this GET case
				this.fillTemplate(new LoginTemplate(this.requestContext));
			}
		}
	}
}
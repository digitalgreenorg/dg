package com.digitalgreen.dashboardgwt.client.servlets;


import java.util.HashMap;
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
				Cookies.removeCookie("sessionid");
				this.redirectTo(new Login());
			} else {
				if(true || LoginData.authenticate((String)this.form.get("username"), 
						(String)this.form.get("password"))) {
					Cookies.setCookie("sessionid", "true");
					this.redirectTo(new Index());	
				} else {
					RequestContext requestContext = new RequestContext();
					requestContext.setMessageString("Invalid credentials, please try again");
					this.redirectTo(new Login(requestContext));
				}
			}
		} else if (method == RequestContext.METHOD_GET) {
			// Most likely do nothing in this GET case
			this.fillTemplate(new LoginTemplate(this.requestContext));
		}
	}
}
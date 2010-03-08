package com.digitalgreen.dashboardgwt.client.servlets;


import com.digitalgreen.dashboardgwt.client.common.ApplicationConstants;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.DashboardGwt;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import java.util.HashMap;

import com.digitalgreen.dashboardgwt.client.data.BaseData;
import com.digitalgreen.dashboardgwt.client.data.UsersData;
import com.digitalgreen.dashboardgwt.client.data.IndexData;
import com.digitalgreen.dashboardgwt.client.data.LoginData;
import com.digitalgreen.dashboardgwt.client.servlets.BaseServlet;
import com.digitalgreen.dashboardgwt.client.templates.IndexTemplate;
import com.google.gwt.user.client.Cookies;
import com.google.gwt.user.client.Window;
public class Index extends BaseServlet {	
	public Index(){
		super();
	}
	
	public Index(RequestContext requestContext) {
		super(requestContext);
	}

	@Override
	public void response () {
		super.response();
		String method = this.getMethodTypeCtx();
		
		if (!this.isLoggedIn()) {
			super.redirectTo(new Login());
		} 
		else {
			if(method == RequestContext.METHOD_POST) {
				HashMap queryArgs = (HashMap)this.requestContext.getArgs();
				String queryArg = (String)queryArgs.get("action");
				if(queryArg == "gooffline"){
					IndexData.createTables();	
					/*IndexData indexData = new IndexData(new OnlineOfflineCallbacks(this) {
						public void onlineSuccessCallback(String results) {
							if(results != "0") {
								Window.alert("GOT A RESPONSE");
								Window.alert("results = " + results);					
								LoginData user = new LoginData();
								user.delete();
								user.create();
								user.insert(results, ApplicationConstants.getUsernameCookie(), ApplicationConstants.getPasswordCookie(), "0", "0");
								ApplicationConstants.toggleConnection(false);
								RequestContext requestContext = new RequestContext();
								requestContext.setMessageString("You are ready to go offline!!. ");
								getServlet().redirectTo(new Index(requestContext));								
							} else {
								RequestContext requestContext = new RequestContext();
								requestContext.setMessageString("You do not have a valid account.Please contact support. ");
								getServlet().redirectTo(new Index(requestContext));				
							}
						}
						
						public void onlineErrorCallback(int errorCode) {
							Window.alert("GOT AN ERROR connecting to server");
							RequestContext requestContext = new RequestContext();
							if (errorCode == BaseData.ERROR_RESPONSE)
								requestContext.setMessageString("Unresponsive Server.  Please contact support.");
							else if (errorCode == BaseData.ERROR_SERVER)
								requestContext.setMessageString("Problem in the connection with the server.");
							else
								requestContext.setMessageString("Unknown error.  Please contact support.");
							getServlet().redirectTo(new Login(requestContext));	
						}
						
						public void offlineSuccessCallback(Object results) {
							// If login success in the offline case
							// This case will never occur for this servlet.
						}
					});*/
					
					// Comment the below line when you are not running the code form a hosted mode.
					//indexData.apply(indexData.getGlobalPrimaryKey(Cookies.getCookie("username")));
					
					/*Comment out the below lines when running the code from an hosted mode*/
					LoginData user = new LoginData();
					user.delete();
					user.create();
					user.insert("1000000", ApplicationConstants.getUsernameCookie(), ApplicationConstants.getPasswordCookie(), "0", "0");
					ApplicationConstants.toggleConnection(false);
					RequestContext requestContext = new RequestContext();
					requestContext.setMessageString("You are ready to go offline!!. ");
					this.redirectTo(new Index(requestContext));
				}
				else if (queryArg == "goonline"){
					LoginData user = new LoginData();
					user.updateAppStatus("1",ApplicationConstants.getUsernameCookie());
					ApplicationConstants.toggleConnection(true);
					RequestContext requestContext = new RequestContext();
					requestContext.setMessageString("You are ready to go Online. While you are online you will be able to sync your changes!");
					this.redirectTo(new Index(requestContext));
				}
			}
			else{
				this.fillTemplate(new IndexTemplate(this.requestContext));
			}
		}
	}
}
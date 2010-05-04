package com.digitalgreen.dashboardgwt.client.servlets;


import com.digitalgreen.dashboardgwt.client.common.ApplicationConstants;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.DashboardGwt;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import java.util.HashMap;

import com.digitalgreen.dashboardgwt.client.data.BaseData;
import com.digitalgreen.dashboardgwt.client.data.FormQueueData;
import com.digitalgreen.dashboardgwt.client.data.Syncronisation;
import com.digitalgreen.dashboardgwt.client.data.UsersData;
import com.digitalgreen.dashboardgwt.client.data.IndexData;
import com.digitalgreen.dashboardgwt.client.data.LoginData;
import com.digitalgreen.dashboardgwt.client.servlets.BaseServlet;
import com.digitalgreen.dashboardgwt.client.templates.IndexTemplate;
import com.google.gwt.gears.client.database.ResultSet;
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
					LoginData user = new LoginData();
					user.updateAppStatus("0",ApplicationConstants.getUsernameCookie());
					ApplicationConstants.toggleConnection(false);
					RequestContext requestContext = new RequestContext();
					requestContext.setMessage("You are ready to go offline!!. ");
					this.redirectTo(new Index(requestContext));
				}
				else if (queryArg == "goonline"){
					LoginData user = new LoginData();
					user.updateAppStatus("1",ApplicationConstants.getUsernameCookie());
					ApplicationConstants.toggleConnection(true);
					RequestContext requestContext = new RequestContext();
					requestContext.setMessage("You are ready to go Online. While you are online you will be able to sync your changes!");
					this.redirectTo(new Index(requestContext));
				}
				else if (queryArg == "sync"){
					Syncronisation syncronisation = new Syncronisation();
					syncronisation.syncFromLocalToMain(this);
				}
				else if (queryArg == "resync"){
					Syncronisation syncronisation = new Syncronisation();
					syncronisation.syncFromMainToLocal(this);
				}
			}
			else{
				this.fillTemplate(new IndexTemplate(this.requestContext));
			}
		}
	}
}
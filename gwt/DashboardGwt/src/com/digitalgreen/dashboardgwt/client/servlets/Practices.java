package com.digitalgreen.dashboardgwt.client.servlets;

import java.util.HashMap;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;

import com.digitalgreen.dashboardgwt.client.data.BaseData;
import com.digitalgreen.dashboardgwt.client.data.PartnersData;
import com.digitalgreen.dashboardgwt.client.templates.PracticeTemplate;
import com.digitalgreen.dashboardgwt.client.data.PracticesData;
import com.google.gwt.user.client.Cookies;
import com.google.gwt.user.client.Window;

import com.google.gwt.json.client.JSONParser;


public class Practices extends BaseServlet{
	
	public Practices(){
		super();
	}
	
	public Practices(RequestContext requestContext){
		super(requestContext);
	}
	
	@Override
	public void response() {
		super.response();
		
		if (!this.isLoggedIn()) {
			super.redirectTo(new Login());
		} else {
			String method = this.getMethodTypeCtx();
			if(method.equals(RequestContext.METHOD_POST)) {
				Form form = this.requestContext.getForm();
				PracticesData practiceData = new PracticesData(new OnlineOfflineCallbacks(this){
					public void onlineSuccessCallback(String results) {
						if(results != null) {
							PracticesData practicesdata = new PracticesData();
							List practices = practicesdata.getListingOnline(results);
							RequestContext requestContext = new RequestContext();
							requestContext.setMessage("Practice successfully saved");
							requestContext.getArgs().put("listing", practices);
							getServlet().redirectTo(new Practices(requestContext));
						} else {
							/*Error in saving the data*/
						}
					}

					public void onlineErrorCallback(int errorCode){
						RequestContext requestContext = new RequestContext();
						if(errorCode == BaseData.ERROR_RESPONSE)
							requestContext.setMessage("Unresponsive Server.  Please contact support.");
						else if (errorCode == BaseData.ERROR_SERVER)
							requestContext.setMessage("Problem in the connection with the server.");
						else
							requestContext.setMessage("Unknown error.  Please contact support.");
						getServlet().redirectTo(new Practices(requestContext));
					}
					
					public void offlineSuccessCallback(Object results) {
						if((Boolean)results) {
							PracticesData practicedata = new PracticesData();
							List practices = practicedata.getPracticesListingOffline();
							RequestContext requestContext = new RequestContext();
							requestContext.setMessage("Practice successfully saved");
							requestContext.getArgs().put("listing", practices);
							getServlet().redirectTo(new Practices(requestContext));
						} else {
							// It's no longer a POST because there was an error, so start again.
							getServlet().getRequestContext().setMethodTypeCtx(RequestContext.METHOD_GET);
							getServlet().getRequestContext().getArgs().put("action", "add");
							getServlet().redirectTo(new Practices(getServlet().getRequestContext()));
						}
					}
				}, form);
				practiceData.apply(practiceData.postPageData());
			}
			else {
				HashMap queryArgs = (HashMap)this.requestContext.getArgs();
				String queryArg = (String)queryArgs.get("action");
				if(queryArg.equals("list")){
					PracticesData practiceData = new PracticesData(new OnlineOfflineCallbacks(this){
						public void onlineSuccessCallback(String results) {
							if(results != null) {
								PracticesData practicedata = new PracticesData();
								List practices = practicedata.getListingOnline(results);
								RequestContext requestContext = new RequestContext();
								requestContext.getArgs().put("listing", practices);
								getServlet().redirectTo(new Practices(requestContext));
							} else {
								/*Error in saving the data*/			
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
							getServlet().redirectTo(new Practices(requestContext));
						}
						
						public void offlineSuccessCallback(Object results) {
							if((Boolean)results) {
								PracticesData practicedata = new PracticesData();
								List practices = practicedata.getPracticesListingOffline();
								RequestContext requestContext = new RequestContext();
								requestContext.getArgs().put("listing", practices);
								getServlet().redirectTo(new Practices(requestContext));
							} else {
								RequestContext requestContext = new RequestContext();
								requestContext.setMessage("Local Database error");
								getServlet().redirectTo(new Practices(requestContext));				
							}
						}
					});
					practiceData.apply(practiceData.getPageData());
				}
				else {
					this.fillTemplate(new PracticeTemplate(this.requestContext));
				}
			}
		}
	}
}

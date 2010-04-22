package com.digitalgreen.dashboardgwt.client.servlets;

import java.util.HashMap;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;

import com.digitalgreen.dashboardgwt.client.data.BaseData;
import com.digitalgreen.dashboardgwt.client.data.LanguagesData;
import com.digitalgreen.dashboardgwt.client.data.PartnersData;
import com.digitalgreen.dashboardgwt.client.templates.LanguagesTemplate;
import com.digitalgreen.dashboardgwt.client.templates.PartnersTemplate;
import com.google.gwt.user.client.Cookies;
import com.google.gwt.user.client.Window;

import com.google.gwt.json.client.JSONParser;


public class Partners extends BaseServlet{
	
	public Partners(){
		super();
	}
	
	public Partners(RequestContext requestContext) {
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
				PartnersData partnerData = new PartnersData(new OnlineOfflineCallbacks(this) {
				public void onlineSuccessCallback(String results) {
					if(results != null) {
						PartnersData partnersData = new PartnersData();
						List partners = partnersData.getListingOnline(results);
						RequestContext requestContext = new RequestContext();
						requestContext.setMessage("Partner successfully saved");
						requestContext.getArgs().put("listing", partners);
						getServlet().redirectTo(new Partners(requestContext ));						
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
					getServlet().redirectTo(new Partners(requestContext));	
				}
					
				public void offlineSuccessCallback(Object results) {
					if((Boolean)results) {
						PartnersData partnerData = new PartnersData();
						List partners = partnerData.getPartnersListingOffline();
						RequestContext requestContext = new RequestContext();
						requestContext.setMessage("Partner successfully saved");
						requestContext.getArgs().put("listing", partners);
						getServlet().redirectTo(new Partners(requestContext ));
					} else {
						// It's no longer a POST because there was an error, so start again.
						getServlet().getRequestContext().setMethodTypeCtx(RequestContext.METHOD_GET);
						getServlet().getRequestContext().getArgs().put("action", "add");
						getServlet().redirectTo(new Partners(getServlet().getRequestContext()));
					}		
				}
			}, form);
				partnerData.apply(partnerData.postPageData());
			}
			else {
				HashMap queryArgs = (HashMap)this.requestContext.getArgs();
				String queryArg = (String)queryArgs.get("action");
				if(queryArg.equals("list")){
					PartnersData partnerData = new PartnersData(new OnlineOfflineCallbacks(this) {
					public void onlineSuccessCallback(String results) {
						if(results != null) {
							PartnersData partnersData = new PartnersData();
							List partners = partnersData.getListingOnline(results);
							RequestContext requestContext = new RequestContext();
							requestContext.getArgs().put("listing", partners);
							getServlet().redirectTo(new Partners(requestContext));						
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
						getServlet().redirectTo(new Partners(requestContext));	
					}
						
					public void offlineSuccessCallback(Object results) {
						if((Boolean)results) {
							PartnersData partnersData = new PartnersData();
							List partners = partnersData.getPartnersListingOffline();
							RequestContext requestContext = new RequestContext();
							requestContext.getArgs().put("listing", partners);
							getServlet().redirectTo(new Partners(requestContext));
						} else {
							RequestContext requestContext = new RequestContext();
							requestContext.setMessage("Local Database error");
							getServlet().redirectTo(new Partners(requestContext));				
						}
					}
					});
					partnerData.apply(partnerData.getPageData());	
				}
				else{
					this.fillTemplate(new PartnersTemplate(this.requestContext));
				}
			}
		}
	}

}

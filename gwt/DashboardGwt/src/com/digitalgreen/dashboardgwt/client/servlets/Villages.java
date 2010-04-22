package com.digitalgreen.dashboardgwt.client.servlets;

import java.util.HashMap;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.BaseData;
import com.digitalgreen.dashboardgwt.client.data.VillagesData;
import com.digitalgreen.dashboardgwt.client.templates.TrainingTemplate;
import com.digitalgreen.dashboardgwt.client.templates.VillagesTemplate;
import com.google.gwt.user.client.Window;

public class Villages extends BaseServlet {
	
	public Villages() {
		super();
	}
	
	public Villages(RequestContext requestContext) {
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
				VillagesData villageData = new VillagesData(new OnlineOfflineCallbacks(this) {
					public void onlineSuccessCallback(String results) {
						if(results != null) {
							VillagesData villageData = new VillagesData();
							List villages = villageData.getListingOnline(results);
							RequestContext requestContext = new RequestContext();
							requestContext.setMessage("Village successfully saved");
							requestContext.getArgs().put("listing", villages);
							getServlet().redirectTo(new Villages(requestContext));
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
						getServlet().redirectTo(new Villages(requestContext));	
					}
					
					public void offlineSuccessCallback(Object results) {
						if((Boolean)results) {
							VillagesData villageData = new VillagesData();
							List villages = villageData.getVillagesListingOffline();
							RequestContext requestContext = new RequestContext();
							requestContext.setMessage("Village successfully saved");
							requestContext.getArgs().put("listing", villages);
							getServlet().redirectTo(new Villages(requestContext));
						} else {
							// It's no longer a POST because there was an error, so start again.
							getServlet().getRequestContext().setMethodTypeCtx(RequestContext.METHOD_GET);
							getServlet().getRequestContext().getArgs().put("action", "add");		
							getServlet().redirectTo(new Villages(getServlet().getRequestContext()));				
						}
						
					}
				}, form);
				
				villageData.apply(villageData.postPageData());
			}
			else {
				HashMap queryArgs = (HashMap)this.requestContext.getArgs();
				String queryArg = (String)queryArgs.get("action");
				if(queryArg.equals("list")){
					VillagesData villageData = new VillagesData(new OnlineOfflineCallbacks(this) {
						public void onlineSuccessCallback(String results) {
							if(results != null) {
								VillagesData villageData = new VillagesData();
								List villages = villageData.getListingOnline(results);
								RequestContext requestContext = new RequestContext();
								requestContext.getArgs().put("listing", villages);
								getServlet().redirectTo(new Villages(requestContext));						
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
							getServlet().redirectTo(new Villages(requestContext));	
						}
						
						public void offlineSuccessCallback(Object results) {
							if((Boolean)results) {
								VillagesData villageData = new VillagesData();
								List villages = villageData.getVillagesListingOffline();
								RequestContext requestContext = new RequestContext();
								requestContext.getArgs().put("listing", villages);
								getServlet().redirectTo(new Villages(requestContext));
							} else {
								RequestContext requestContext = new RequestContext();
								requestContext.setMessage("Local Database error");
								getServlet().redirectTo(new Villages(requestContext));				
							}	
						}
					});
					villageData.apply(villageData.getListPageData());
				}
				else if(queryArg == "add"){
					VillagesData villageData = new VillagesData(new OnlineOfflineCallbacks(this) {
						public void onlineSuccessCallback(String addData) {
							if(addData != null) {
								RequestContext requestContext = new RequestContext();
								requestContext.getArgs().put("action", "add");
								requestContext.getArgs().put("addPageData", addData);
								getServlet().fillTemplate(new VillagesTemplate(requestContext));
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
							getServlet().redirectTo(new Villages(requestContext));	
						}
						
						public void offlineSuccessCallback(Object addData) {
							if((String)addData != null) {
								// Got whatever info we need to display for this GET request, so go ahead
								// and display it by filling in the template.  No need to redirect.
								getServlet().getRequestContext().getArgs().put("addPageData", (String)addData);
								getServlet().fillTemplate(new VillagesTemplate(getServlet().getRequestContext()));
							} else {
								RequestContext requestContext = new RequestContext();
								requestContext.setMessage("Local Database error");
								getServlet().redirectTo(new Villages(requestContext));				
							}	
						}
					});
					villageData.apply(villageData.getAddPageData());	
				}
				else {
					this.fillTemplate(new VillagesTemplate(this.requestContext));
				}
			}
		}
	}
}
package com.digitalgreen.dashboardgwt.client.servlets;

import java.util.HashMap;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.BaseData;
import com.digitalgreen.dashboardgwt.client.data.AnimatorAssignedVillagesData;
import com.digitalgreen.dashboardgwt.client.templates.AnimatorAssignedVillagesTemplate;

public class AnimatorAssignedVillages extends BaseServlet {
	public AnimatorAssignedVillages() {
		super();
	}
	
	public AnimatorAssignedVillages(RequestContext requestContext) {
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
				AnimatorAssignedVillagesData animatorAssignedVillageData = new AnimatorAssignedVillagesData(new OnlineOfflineCallbacks(this) {
					public void onlineSuccessCallback(String results) {
						if(results != null) {
							AnimatorAssignedVillagesData animatorAssignedVillageData = new AnimatorAssignedVillagesData();
							List animatorAssignedVillages = animatorAssignedVillageData.getListingOnline(results);
							RequestContext requestContext = new RequestContext();
							requestContext.setMessageString("AnimatorAssignedVillage successfully saved");
							requestContext.getArgs().put("listing", animatorAssignedVillages);
							getServlet().redirectTo(new AnimatorAssignedVillages(requestContext));
						} else {
							/*Error in saving the data*/			
						}
					}
					
					public void onlineErrorCallback(int errorCode) {
						RequestContext requestContext = new RequestContext();
						if (errorCode == BaseData.ERROR_RESPONSE)
							requestContext.setMessageString("Unresponsive Server.  Please contact support.");
						else if (errorCode == BaseData.ERROR_SERVER)
							requestContext.setMessageString("Problem in the connection with the server.");
						else
							requestContext.setMessageString("Unknown error.  Please contact support.");
						getServlet().redirectTo(new AnimatorAssignedVillages(requestContext));	
					}
					
					public void offlineSuccessCallback(Object results) {
						if((Boolean)results) {
							AnimatorAssignedVillagesData animatorAssignedVillageData = new AnimatorAssignedVillagesData();
							List animatorAssignedVillages = animatorAssignedVillageData.getAnimatorsAssignedVillagesListingOffline();
							RequestContext requestContext = new RequestContext();
							requestContext.setMessageString("AnimatorAssignedVillage successfully saved");
							requestContext.getArgs().put("listing", animatorAssignedVillages);
							getServlet().redirectTo(new AnimatorAssignedVillages(requestContext));
						} else {
							RequestContext requestContext = new RequestContext();
							requestContext.setMessageString("Invalid data, please try again");
							getServlet().redirectTo(new AnimatorAssignedVillages(requestContext));				
						}
						
					}
				}, form);
				
				animatorAssignedVillageData.apply(animatorAssignedVillageData.postPageData());
			}
			else {
				HashMap queryArgs = (HashMap)this.requestContext.getArgs();
				String queryArg = (String)queryArgs.get("action");
				if(queryArg.equals("list")){
					AnimatorAssignedVillagesData animatorAssignedVillageData = new AnimatorAssignedVillagesData(new OnlineOfflineCallbacks(this) {
						public void onlineSuccessCallback(String results) {
							if(results != null) {
								AnimatorAssignedVillagesData animatorAssignedVillageData = new AnimatorAssignedVillagesData();
								List animatorAssignedVillages = animatorAssignedVillageData.getListingOnline(results);
								RequestContext requestContext = new RequestContext();
								requestContext.getArgs().put("listing", animatorAssignedVillages);
								getServlet().redirectTo(new AnimatorAssignedVillages(requestContext));						
							} else {
								/*Error in saving the data*/			
							}
						}

						public void onlineErrorCallback(int errorCode) {
							RequestContext requestContext = new RequestContext();
							if (errorCode == BaseData.ERROR_RESPONSE)
								requestContext.setMessageString("Unresponsive Server.  Please contact support.");
							else if (errorCode == BaseData.ERROR_SERVER)
								requestContext.setMessageString("Problem in the connection with the server.");
							else
								requestContext.setMessageString("Unknown error.  Please contact support.");
							getServlet().redirectTo(new AnimatorAssignedVillages(requestContext));	
						}
						
						public void offlineSuccessCallback(Object results) {
							if((Boolean)results) {
								AnimatorAssignedVillagesData animatorAssignedVillageData = new AnimatorAssignedVillagesData();
								List animatorAssignedVillages = animatorAssignedVillageData.getAnimatorsAssignedVillagesListingOffline();
								RequestContext requestContext = new RequestContext();
								requestContext.getArgs().put("listing", animatorAssignedVillages);
								getServlet().redirectTo(new AnimatorAssignedVillages(requestContext));
							} else {
								RequestContext requestContext = new RequestContext();
								requestContext.setMessageString("Local Database error");
								getServlet().redirectTo(new AnimatorAssignedVillages(requestContext));				
							}	
						}
					});
					animatorAssignedVillageData.apply(animatorAssignedVillageData.getListPageData());
				}
				else if(queryArg == "add"){
					AnimatorAssignedVillagesData animatorAssignedVillageData = new AnimatorAssignedVillagesData(new OnlineOfflineCallbacks(this) {
						public void onlineSuccessCallback(String addData) {
							if(addData != null) {
								RequestContext requestContext = new RequestContext();
								requestContext.getArgs().put("action", "add");
								requestContext.getArgs().put("addPageData", addData);
								getServlet().fillTemplate(new AnimatorAssignedVillagesTemplate(requestContext));
							} else {
								/*Error in saving the data*/			
							}
						}
					
						public void onlineErrorCallback(int errorCode) {
							RequestContext requestContext = new RequestContext();
							if (errorCode == BaseData.ERROR_RESPONSE)
								requestContext.setMessageString("Unresponsive Server.  Please contact support.");
							else if (errorCode == BaseData.ERROR_SERVER)
								requestContext.setMessageString("Problem in the connection with the server.");
							else
								requestContext.setMessageString("Unknown error.  Please contact support.");
							getServlet().redirectTo(new AnimatorAssignedVillages(requestContext));	
						}
						
						public void offlineSuccessCallback(Object addData) {
							if((String)addData != null) {
								RequestContext requestContext = new RequestContext();
								requestContext.getArgs().put("action", "add");
								requestContext.getArgs().put("addPageData", (String)addData);
								getServlet().fillTemplate(new AnimatorAssignedVillagesTemplate(requestContext));
							} else {
								RequestContext requestContext = new RequestContext();
								requestContext.setMessageString("Local Database error");
								getServlet().redirectTo(new AnimatorAssignedVillages(requestContext));				
							}	
						}
					});
					animatorAssignedVillageData.apply(animatorAssignedVillageData.getAddPageData());	
				}
				else {
					this.fillTemplate(new AnimatorAssignedVillagesTemplate(this.requestContext));
				}
			}
		}
	}
}
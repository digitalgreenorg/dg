package com.digitalgreen.dashboardgwt.client.servlets;

import java.util.HashMap;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.BaseData;
import com.digitalgreen.dashboardgwt.client.data.AnimatorsData;
import com.digitalgreen.dashboardgwt.client.templates.AnimatorsTemplate;
import com.digitalgreen.dashboardgwt.client.templates.AnimatorsTemplate;
import com.digitalgreen.dashboardgwt.client.templates.TrainingTemplate;

public class Animators extends BaseServlet{
	
	public Animators(){
		super();
	}
	
	public Animators(RequestContext requestContext){
		super(requestContext);		
	}
	
	@Override
	public void response(){
		super.response();
		
		if(!this.isLoggedIn()){
			super.redirectTo(new Login());
		}else{
			String method = this.getMethodTypeCtx();
			if(method.equals(RequestContext.METHOD_POST)) {
				Form form = this.requestContext.getForm();
				AnimatorsData animatorData = new AnimatorsData(new OnlineOfflineCallbacks(this) {
					public void onlineSuccessCallback(String results) {
						if(results != null) {
							AnimatorsData animatorData = new AnimatorsData();
							List animators = animatorData.getListingOnline(results);
							RequestContext requestContext = new RequestContext();
							requestContext.setMessageString("Animator successfully saved");
							requestContext.getArgs().put("listing", animators);
							getServlet().redirectTo(new Animators(requestContext));
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
						getServlet().redirectTo(new Animators(requestContext));	
					}
					
					public void offlineSuccessCallback(Object results) {
						if((Boolean)results) {
							AnimatorsData animatorData = new AnimatorsData();
							List animators = animatorData.getAnimatorsListingOffline();
							RequestContext requestContext = new RequestContext();
							requestContext.setMessageString("Animator successfully saved");
							requestContext.getArgs().put("listing", animators);
							getServlet().redirectTo(new Animators(requestContext));
						} else {
							// It's no longer a POST because there was an error, so start again.
							getServlet().getRequestContext().setMethodTypeCtx(RequestContext.METHOD_GET);
							getServlet().getRequestContext().getArgs().put("action", "add");		
							getServlet().redirectTo(new  Animators(getServlet().getRequestContext()));				
						}
						
					}
				}, form);
				
				animatorData.apply(animatorData.postPageData());
			}
			else {
				HashMap queryArgs = (HashMap)this.requestContext.getArgs();
				String queryArg = (String)queryArgs.get("action");
				if(queryArg.equals("list")){
					AnimatorsData animatorData = new AnimatorsData(new OnlineOfflineCallbacks(this) {
						public void onlineSuccessCallback(String results) {
							if(results != null) {
								AnimatorsData animatorData = new AnimatorsData();
								List animators = animatorData.getListingOnline(results);
								RequestContext requestContext = new RequestContext();
								requestContext.getArgs().put("listing", animators);
								getServlet().redirectTo(new Animators(requestContext));						
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
							getServlet().redirectTo(new Animators(requestContext));	
						}
						
						public void offlineSuccessCallback(Object results) {
							if((Boolean)results) {
								AnimatorsData animatorData = new AnimatorsData();
								List animators = animatorData.getAnimatorsListingOffline();
								RequestContext requestContext = new RequestContext();
								requestContext.getArgs().put("listing", animators);
								getServlet().redirectTo(new Animators(requestContext));
							} else {
								RequestContext requestContext = new RequestContext();
								requestContext.setMessageString("Local Database error");
								getServlet().redirectTo(new Animators(requestContext));				
							}	
						}
					});
					animatorData.apply(animatorData.getListPageData());
				}
				else if(queryArg == "add"){
					AnimatorsData animatorData = new AnimatorsData(new OnlineOfflineCallbacks(this) {
						public void onlineSuccessCallback(String addData) {
							if(addData != null) {
								RequestContext requestContext = new RequestContext();
								requestContext.getArgs().put("action", "add");
								requestContext.getArgs().put("addPageData", addData);
								getServlet().fillTemplate(new AnimatorsTemplate(requestContext));
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
							getServlet().redirectTo(new Animators(requestContext));	
						}
						
						public void offlineSuccessCallback(Object addData) {
							if((String)addData != null) {
								// Got whatever info we need to display for this GET request, so go ahead
								// and display it by filling in the template.  No need to redirect.
								getServlet().getRequestContext().getArgs().put("addPageData", (String)addData);
								getServlet().fillTemplate(new AnimatorsTemplate(getServlet().getRequestContext()));
							} else {
								RequestContext requestContext = new RequestContext();
								requestContext.setMessageString("Local Database error");
								getServlet().redirectTo(new Animators(requestContext));				
							}	
						}
					});
					animatorData.apply(animatorData.getAddPageData());	
				}
				else {
					this.fillTemplate(new AnimatorsTemplate(this.requestContext));
				}
			}
		}
	}
}
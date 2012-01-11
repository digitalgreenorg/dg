package com.digitalgreen.dashboardgwt.client.servlets;

import java.util.HashMap;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.BaseData;
import com.digitalgreen.dashboardgwt.client.data.AnimatorAssignedVillagesData;
import com.digitalgreen.dashboardgwt.client.templates.AnimatorAssignedVillagesTemplate;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.HTMLPanel;

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
						if(this.getStatusCode() == 200) {
							RequestContext requestContext = new RequestContext();
							requestContext.setMessage("Animator Assigned Village successfully saved");
							requestContext.getArgs().put("action", "list");
							requestContext.getArgs().put("pageNum", "1");
							getServlet().redirectTo(new AnimatorAssignedVillages(requestContext));
						} else {
							getServlet().getRequestContext().setMethodTypeCtx(RequestContext.METHOD_GET);
							getServlet().getRequestContext().setErrorMessage(results) ;
							getServlet().redirectTo(new AnimatorAssignedVillages(getServlet().getRequestContext()));	
						}
					}
					
					public void onlineErrorCallback(int errorCode) {
						getServlet().getRequestContext().setMethodTypeCtx(RequestContext.METHOD_GET);
						if (errorCode == BaseData.ERROR_RESPONSE)
							getServlet().getRequestContext().setErrorMessage("You may be experiencing server/bandwidth problems.  Please try again, or contact support.");
						else if (errorCode == BaseData.ERROR_SERVER)
							getServlet().getRequestContext().setErrorMessage("Problem in the connection with the server.");
						else
							getServlet().getRequestContext().setErrorMessage("Unknown error.  Please contact support.");
						getServlet().redirectTo(new AnimatorAssignedVillages(getServlet().getRequestContext()));	
					}
					
					public void offlineSuccessCallback(Object results) {
						if((Boolean)results) {
							RequestContext requestContext = new RequestContext();
							requestContext.setMessage("Animator Assigned Village successfully saved");
							requestContext.getArgs().put("action", "list");
							requestContext.getArgs().put("pageNum", "1");
							getServlet().redirectTo(new AnimatorAssignedVillages(requestContext));
						} else {
							// It's no longer a POST because there was an error, so start again.
							getServlet().getRequestContext().setMethodTypeCtx(RequestContext.METHOD_GET);
							getServlet().getRequestContext().setErrorMessage(getServlet().getRequestContext().getForm().printFormErrors());
							getServlet().redirectTo(new AnimatorAssignedVillages(getServlet().getRequestContext()));			
						}
					}
				}, form);
				if(this.requestContext.getArgs().get("action").equals("edit")) {
					form.setId((String)this.requestContext.getArgs().get("id"));
					animatorAssignedVillageData.apply(animatorAssignedVillageData.postPageData((String)this.requestContext.getArgs().get("id")));
				}
				else{
					animatorAssignedVillageData.apply(animatorAssignedVillageData.postPageData());
				}
				
			}
			else {
				HashMap queryArgs = (HashMap)this.requestContext.getArgs();
				String queryArg = (String)queryArgs.get("action");
				String pageNum = (String)queryArgs.get("pageNum");
				String operation = (String)queryArgs.get("operation");
				String searchText = "";
				if(operation == "search") {
					searchText = (String)queryArgs.get("searchText");
				}
				if(queryArg.equals("list")){
					AnimatorAssignedVillagesData animatorAssignedVillageData = new AnimatorAssignedVillagesData(new OnlineOfflineCallbacks(this) {
						public void onlineSuccessCallback(String results) {
							String count = this.getResponse().getHeader("X-COUNT");
							getServlet().getRequestContext().getArgs().put("totalRows", count);
							if(this.getStatusCode() == 200) {
								AnimatorAssignedVillagesData animatorAssignedVillageData = new AnimatorAssignedVillagesData();
								if(!results.equals("EOF")){
									List animatorAssignedVillages = animatorAssignedVillageData.getListingOnline(results);
									getServlet().getRequestContext().getArgs().put("listing", animatorAssignedVillages);
								}
								getServlet().fillTemplate(new AnimatorAssignedVillagesTemplate(getServlet().getRequestContext()));
							} else {
								RequestContext requestContext = new RequestContext();
								requestContext.setErrorMessage("Unexpected error occured in retriving data. Please contact support");
								getServlet().redirectTo(new Index(requestContext));
							}
						}

						public void onlineErrorCallback(int errorCode) {
							RequestContext requestContext = new RequestContext();
							if (errorCode == BaseData.ERROR_RESPONSE)
								requestContext.setErrorMessage("You may be experiencing server/bandwidth problems.  Please try again, or contact support.");
							else if (errorCode == BaseData.ERROR_SERVER)
								requestContext.setErrorMessage("Problem in the connection with the server.");
							else
								requestContext.setErrorMessage("Unknown error.  Please contact support.");
							getServlet().redirectTo(new Index(requestContext));
						}
						
						public void offlineSuccessCallback(Object results) {
							if((Boolean)results) {
								AnimatorAssignedVillagesData animatorAssignedVillagesData = new AnimatorAssignedVillagesData();
								List animatorAssignedVillages;
								String pageNum = (String)getServlet().getRequestContext().getArgs().get("pageNum");
								String operation = (String)getServlet().getRequestContext().getArgs().get("operation");
								if(operation == "search") {
									String searchText = (String)getServlet().getRequestContext().getArgs().get("searchText");
									animatorAssignedVillages = animatorAssignedVillagesData.getAnimatorsAssignedVillagesListingOffline(pageNum, searchText);
									requestContext.getArgs().put("totalRows", animatorAssignedVillagesData.getCount(searchText));
								}
								else {
									animatorAssignedVillages = animatorAssignedVillagesData.getAnimatorsAssignedVillagesListingOffline(pageNum);
									requestContext.getArgs().put("totalRows", animatorAssignedVillagesData.getCount());
								}								
								requestContext.getArgs().put("listing", animatorAssignedVillages);
								getServlet().fillTemplate(new AnimatorAssignedVillagesTemplate(getServlet().getRequestContext()));
							} else {
								RequestContext requestContext = new RequestContext();
								requestContext.setErrorMessage("Unexpected local error. Please contact support");
								getServlet().redirectTo(new Index(requestContext));				
							}	
						}
					});
					if (operation == "search") {
						animatorAssignedVillageData.apply(animatorAssignedVillageData.getListPageData(pageNum, searchText));
					} else {
						animatorAssignedVillageData.apply(animatorAssignedVillageData.getListPageData(pageNum));						
					}
				}
				else if(queryArg.equals("add") || queryArg.equals("edit")){
					Form form = this.requestContext.getForm();
					AnimatorAssignedVillagesData animatorAssignedVillageData = new AnimatorAssignedVillagesData(new OnlineOfflineCallbacks(this) {
						public void onlineSuccessCallback(String addData) {
							if(this.getStatusCode() == 200) {
								if(getServlet().getRequestContext().getArgs().get("action").equals("edit")) {
									if(getServlet().getRequestContext().getForm().getQueryString() == null) {
										getServlet().getRequestContext().getForm().setQueryString(Form.retriveQueryStringFromHTMLString(addData));
									}
								}
								getServlet().getRequestContext().getArgs().put("addPageData", addData);
								getServlet().fillTemplate(new AnimatorAssignedVillagesTemplate(getServlet().getRequestContext()));
							} else {
								RequestContext requestContext = new RequestContext();
								requestContext.setErrorMessage("Unexpected error occured in retriving data. Please contact support");
								getServlet().redirectTo(new Index(requestContext));
							}
						}
					
						public void onlineErrorCallback(int errorCode) {
							RequestContext requestContext = new RequestContext();
							if (errorCode == BaseData.ERROR_RESPONSE)
								requestContext.setErrorMessage("You may be experiencing server/bandwidth problems.  Please try again, or contact support.");
							else if (errorCode == BaseData.ERROR_SERVER)
								requestContext.setErrorMessage("Problem in the connection with the server.");
							else
								requestContext.setErrorMessage("Unknown error.  Please contact support.");
							getServlet().redirectTo(new Index(requestContext));	
						}
						
						public void offlineSuccessCallback(Object addData) {
							if((String)addData != null) {
								// Got whatever info we need to display for this GET request, so go ahead
								// and display it by filling in the template.  No need to redirect.
								getServlet().getRequestContext().getArgs().put("addPageData", (String)addData);
								getServlet().fillTemplate(new AnimatorAssignedVillagesTemplate(getServlet().getRequestContext()));
							} else {
								RequestContext requestContext = new RequestContext();
								requestContext.setErrorMessage("Unexpected local error. Please contact support");
								getServlet().redirectTo(new Index(requestContext));				
							}	
						}
					}, form);
					if(queryArg.equals("add")) {
						animatorAssignedVillageData.apply(animatorAssignedVillageData.getAddPageData());
					}
					else{
						form.setId((String)this.requestContext.getArgs().get("id"));
						animatorAssignedVillageData.apply(animatorAssignedVillageData.getAddPageData(this.requestContext.getArgs().get("id").toString()));
					}
				}
			}
		}
	}
}
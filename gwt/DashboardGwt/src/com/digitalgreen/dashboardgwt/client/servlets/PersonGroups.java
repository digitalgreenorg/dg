package com.digitalgreen.dashboardgwt.client.servlets;

import java.util.HashMap;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.BaseData;
import com.digitalgreen.dashboardgwt.client.data.PersonGroupsData;
import com.digitalgreen.dashboardgwt.client.templates.PersonGroupsTemplate;
import com.digitalgreen.dashboardgwt.client.templates.TrainingTemplate;

import com.google.gwt.user.client.Window;

public class PersonGroups extends BaseServlet{
	
	public PersonGroups(){
		super();
	}
	
	public PersonGroups(RequestContext requestContext) {
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
				PersonGroupsData personGroupData = new PersonGroupsData(new OnlineOfflineCallbacks(this) {
					public void onlineSuccessCallback(String results) {
						if(results != null) {
							PersonGroupsData personGroupData = new PersonGroupsData();
							List personGroups = personGroupData.getListingOnline(results);
							RequestContext requestContext = new RequestContext();
							requestContext.setMessageString("PersonGroup successfully saved");
							requestContext.getArgs().put("listing", personGroups);
							getServlet().redirectTo(new PersonGroups(requestContext));
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
						getServlet().redirectTo(new PersonGroups(requestContext));	
					}
					
					public void offlineSuccessCallback(Object results) {
						if((Boolean)results) {
							PersonGroupsData personGroupData = new PersonGroupsData();
							List personGroups = personGroupData.getPersonGroupsListingOffline();
							RequestContext requestContext = new RequestContext();
							requestContext.setMessageString("PersonGroup successfully saved");
							requestContext.getArgs().put("listing", personGroups);
							getServlet().redirectTo(new PersonGroups(requestContext));
						} else {
							// It's no longer a POST because there was an error, so start again.
							getServlet().getRequestContext().setMethodTypeCtx(RequestContext.METHOD_GET);
							getServlet().getRequestContext().getArgs().put("action", "add");		
							getServlet().redirectTo(new PersonGroups(getServlet().getRequestContext()));				
						}
						
					}
				}, form);
				
				personGroupData.apply(personGroupData.postPageData());
			}
			else {
				HashMap queryArgs = (HashMap)this.requestContext.getArgs();
				String queryArg = (String)queryArgs.get("action");
				if(queryArg.equals("list")){
					PersonGroupsData personGroupData = new PersonGroupsData(new OnlineOfflineCallbacks(this) {
						public void onlineSuccessCallback(String results) {
							if(results != null) {
								PersonGroupsData personGroupData = new PersonGroupsData();
								List personGroups = personGroupData.getListingOnline(results);
								RequestContext requestContext = new RequestContext();
								requestContext.getArgs().put("listing", personGroups);
								getServlet().fillTemplate(new PersonGroupsTemplate(requestContext));
								//getServlet().redirectTo(new PersonGroups(requestContext));						
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
							getServlet().redirectTo(new PersonGroups(requestContext));	
						}
						
						public void offlineSuccessCallback(Object results) {
							if((Boolean)results) {
								PersonGroupsData personGroupData = new PersonGroupsData();
								List personGroups = personGroupData.getPersonGroupsListingOffline();
								RequestContext requestContext = new RequestContext();
								requestContext.getArgs().put("listing", personGroups);
								getServlet().redirectTo(new PersonGroups(requestContext));
							} else {
								RequestContext requestContext = new RequestContext();
								requestContext.setMessageString("Local Database error");
								getServlet().redirectTo(new PersonGroups(requestContext));				
							}	
						}
					});
					personGroupData.apply(personGroupData.getListPageData());
				}
				else if(queryArg == "add"){
					PersonGroupsData personGroupData = new PersonGroupsData(new OnlineOfflineCallbacks(this) {
						public void onlineSuccessCallback(String addData) {
							if(addData != null) {
								RequestContext requestContext = new RequestContext();
								requestContext.getArgs().put("action", "add");
								requestContext.getArgs().put("addPageData", addData);
								getServlet().fillTemplate(new PersonGroupsTemplate(requestContext));
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
							getServlet().redirectTo(new PersonGroups(requestContext));	
						}
						
						public void offlineSuccessCallback(Object addData) {
							if((String)addData != null) {
								// Got whatever info we need to display for this GET request, so go ahead
								// and display it by filling in the template.  No need to redirect.
								getServlet().getRequestContext().getArgs().put("addPageData", (String)addData);
								getServlet().fillTemplate(new PersonGroupsTemplate(getServlet().getRequestContext()));
							} else {
								RequestContext requestContext = new RequestContext();
								requestContext.setMessageString("Local Database error");
								getServlet().redirectTo(new PersonGroups(requestContext));				
							}	
						}
					});
					personGroupData.apply(personGroupData.getAddPageData());	
				}
				else {
					this.fillTemplate(new PersonGroupsTemplate(this.requestContext));
				}
			}
		}
	}
}
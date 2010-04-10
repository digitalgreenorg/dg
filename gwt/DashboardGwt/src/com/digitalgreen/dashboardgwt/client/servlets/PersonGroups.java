package com.digitalgreen.dashboardgwt.client.servlets;

import java.util.HashMap;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.BaseData;
import com.digitalgreen.dashboardgwt.client.data.PersonGroupsData;
import com.digitalgreen.dashboardgwt.client.templates.PersonGroupsTemplate;

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
							Window.alert("inside offline callback ");
							PersonGroupsData personGroupData = new PersonGroupsData();
							List personGroups = personGroupData.getPersonGroupsListingOffline();
							RequestContext requestContext = new RequestContext();
							requestContext.setMessageString("PersonGroup successfully saved");
							requestContext.getArgs().put("listing", personGroups);
							getServlet().redirectTo(new PersonGroups(requestContext));
						} else {
							RequestContext requestContext = new RequestContext();
							requestContext.setMessageString("Invalid data, please try again");
							getServlet().redirectTo(new PersonGroups(requestContext));				
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
								RequestContext requestContext = new RequestContext();
								requestContext.getArgs().put("action", "add");
								requestContext.getArgs().put("addPageData", (String)addData);
								getServlet().fillTemplate(new PersonGroupsTemplate(requestContext));
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
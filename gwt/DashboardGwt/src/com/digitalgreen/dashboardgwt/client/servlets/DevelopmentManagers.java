package com.digitalgreen.dashboardgwt.client.servlets;

import java.util.HashMap;
import java.util.List;
import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.BaseData;
import com.digitalgreen.dashboardgwt.client.data.DevelopmentManagersData;
import com.digitalgreen.dashboardgwt.client.templates.DevelopmentManagersTemplate;
import com.google.gwt.dom.client.Element;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.HTMLPanel;
import com.google.gwt.user.client.ui.ListBox;
import com.google.gwt.user.client.ui.RootPanel;
import com.google.gwt.user.client.ui.Widget;
import com.google.gwt.xml.client.XMLParser;
import com.google.gwt.xml.client.Document;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;

public class DevelopmentManagers extends BaseServlet {
	public  DevelopmentManagers(){
		super();
	}
	
	public DevelopmentManagers(RequestContext requestContext) {
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
				DevelopmentManagersData developmentmanagerData = new DevelopmentManagersData(new OnlineOfflineCallbacks(this) {
					public void onlineSuccessCallback(String results) {
						if(results != null) {
							DevelopmentManagersData developmentmanagerdata = new DevelopmentManagersData();
							List developmentmanagers = developmentmanagerdata.getListingOnline(results);
							RequestContext requestContext = new RequestContext();
							requestContext.setMessageString("DevelopmentManager successfully saved");
							requestContext.getArgs().put("listing", developmentmanagers);
							getServlet().redirectTo(new DevelopmentManagers(requestContext ));						
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
						getServlet().redirectTo(new DevelopmentManagers(requestContext));	
					}
					
					public void offlineSuccessCallback(Object results) {
						if((Boolean)results) {
							DevelopmentManagersData developmentmanagerdata = new DevelopmentManagersData();
							List developmentmanagers = developmentmanagerdata.getDevelopmentManagersListingOffline();
							RequestContext requestContext = new RequestContext();
							requestContext.setMessageString("DevelopmentManager successfully saved");
							requestContext.getArgs().put("listing", developmentmanagers);
							getServlet().redirectTo(new DevelopmentManagers(requestContext ));
						} else {
							// It's no longer a POST because there was an error, so start again.
							getServlet().getRequestContext().setMethodTypeCtx(RequestContext.METHOD_GET);
							getServlet().getRequestContext().getArgs().put("action", "add");		
							getServlet().redirectTo(new DevelopmentManagers(getServlet().getRequestContext()));				
						}
						
					}
				}, form);
				
				developmentmanagerData.apply(developmentmanagerData.postPageData());

			}
			else{
				HashMap queryArgs = (HashMap)this.requestContext.getArgs();
				String queryArg = (String)queryArgs.get("action");
				if(queryArg == "list"){
					DevelopmentManagersData developmentmanagerData = new DevelopmentManagersData(new OnlineOfflineCallbacks(this) {
						public void onlineSuccessCallback(String results) {
							if(results != null) {
								DevelopmentManagersData developmentmanagerdata = new DevelopmentManagersData();
								List developmentmanagers = developmentmanagerdata.getListingOnline(results);
								RequestContext requestContext = new RequestContext();
								requestContext.getArgs().put("listing", developmentmanagers);
								getServlet().fillTemplate(new DevelopmentManagersTemplate(requestContext));
								//getServlet().redirectTo(new DevelopmentManagers(requestContext ));						
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
							getServlet().redirectTo(new DevelopmentManagers(requestContext));	
						}
						
						public void offlineSuccessCallback(Object results) {
							if((Boolean)results) {
								DevelopmentManagersData developmentmanagerdata = new DevelopmentManagersData();
								List developmentmanagers = developmentmanagerdata.getDevelopmentManagersListingOffline();
								RequestContext requestContext = new RequestContext();
								requestContext.getArgs().put("listing", developmentmanagers);
								getServlet().fillTemplate(new DevelopmentManagersTemplate(requestContext));
							} else {
								RequestContext requestContext = new RequestContext();
								requestContext.setMessageString("Local Database error");
								getServlet().redirectTo(new DevelopmentManagers(requestContext));				
							}	
						}
					});
					developmentmanagerData.apply(developmentmanagerData.getListPageData());	
				}
				else if(queryArg == "add"){
					DevelopmentManagersData developmentmanagerData = new DevelopmentManagersData(new OnlineOfflineCallbacks(this) {
						public void onlineSuccessCallback(String addData) {
							if(addData != null) {
								RequestContext requestContext = new RequestContext();
								requestContext.getArgs().put("action", "add");
								requestContext.getArgs().put("addPageData", addData);
								getServlet().fillTemplate(new DevelopmentManagersTemplate(requestContext));
								//getServlet().redirectTo(new DevelopmentManagers(requestContext ));						
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
							getServlet().redirectTo(new DevelopmentManagers(requestContext));	
						}
						
						public void offlineSuccessCallback(Object addData) {
							if((String)addData != null) {
								// Got whatever info we need to display for this GET request, so go ahead
								// and display it by filling in the template.  No need to redirect.
								getServlet().getRequestContext().getArgs().put("addPageData", (String)addData);
								getServlet().fillTemplate(new DevelopmentManagersTemplate(getServlet().getRequestContext()));
							} else {
								RequestContext requestContext = new RequestContext();
								requestContext.setMessageString("Local Database error");
								getServlet().redirectTo(new DevelopmentManagers(requestContext));				
							}	
						}
					});
					developmentmanagerData.apply(developmentmanagerData.getAddPageData());	
				}
				else{
					this.fillTemplate(new DevelopmentManagersTemplate(this.requestContext));
				}
				
			}
			
		}
	}
	
}
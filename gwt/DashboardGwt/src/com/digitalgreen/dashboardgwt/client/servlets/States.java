package com.digitalgreen.dashboardgwt.client.servlets;

import java.util.HashMap;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.BaseData;
import com.digitalgreen.dashboardgwt.client.data.StatesData;
import com.digitalgreen.dashboardgwt.client.templates.StatesTemplate;
import com.google.gwt.dom.client.Element;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.HTMLPanel;
import com.google.gwt.user.client.ui.ListBox;
import com.google.gwt.user.client.ui.RootPanel;
import com.google.gwt.user.client.ui.Widget;
import com.google.gwt.xml.client.XMLParser;
import com.google.gwt.xml.client.Document;

public class States extends BaseServlet{
	
	public States(){
		super();
	}
	
	public States(RequestContext requestContext) {
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
				StatesData stateData = new StatesData(new OnlineOfflineCallbacks(this) {
					public void onlineSuccessCallback(String results) {
						if(this.getStatusCode() == 200) {
							StatesData statedata = new StatesData();
							List states = statedata.getListingOnline(results);
							RequestContext requestContext = new RequestContext();
							requestContext.setMessage("State successfully saved");
							requestContext.getArgs().put("listing", states);
							getServlet().redirectTo(new States(requestContext ));						
						} else {
							getServlet().getRequestContext().setMethodTypeCtx(RequestContext.METHOD_GET);
							getServlet().getRequestContext().getArgs().put("action", "add");
							getServlet().getRequestContext().setErrorMessage(results);
							getServlet().redirectTo(new States(getServlet().getRequestContext()));			
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
						getServlet().redirectTo(new States(requestContext));	
					}
					
					public void offlineSuccessCallback(Object results) {
						if((Boolean)results) {
							StatesData statedata = new StatesData();
							List states = statedata.getStatesListingOffline();
							RequestContext requestContext = new RequestContext();
							requestContext.setMessage("State successfully saved");
							requestContext.getArgs().put("listing", states);
							getServlet().redirectTo(new States(requestContext ));
						} else {
							// It's no longer a POST because there was an error, so start again.
							getServlet().getRequestContext().setMethodTypeCtx(RequestContext.METHOD_GET);
							getServlet().getRequestContext().getArgs().put("action", "add");
							getServlet().getRequestContext().setErrorMessage(getServlet().getRequestContext().getForm().printFormErrors());
							getServlet().redirectTo(new States(getServlet().getRequestContext()));				
						}
						
					}
				}, form);
				
				stateData.apply(stateData.postPageData());

			}
			else{
				HashMap queryArgs = (HashMap)this.requestContext.getArgs();
				String queryArg = (String)queryArgs.get("action");
				if(queryArg == "list"){
					StatesData stateData = new StatesData(new OnlineOfflineCallbacks(this) {
						public void onlineSuccessCallback(String results) {
							if(results != null) {
								StatesData statedata = new StatesData();
								List states = statedata.getListingOnline(results);
								RequestContext requestContext = new RequestContext();
								requestContext.getArgs().put("listing", states);
								getServlet().fillTemplate(new StatesTemplate(requestContext));
								//getServlet().redirectTo(new States(requestContext ));						
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
							getServlet().redirectTo(new States(requestContext));	
						}
						
						public void offlineSuccessCallback(Object results) {
							if((Boolean)results) {
								StatesData statedata = new StatesData();
								List states = statedata.getStatesListingOffline();
								RequestContext requestContext = new RequestContext();
								requestContext.getArgs().put("listing", states);
								getServlet().fillTemplate(new StatesTemplate(requestContext));
							} else {
								RequestContext requestContext = new RequestContext();
								requestContext.setMessage("Local Database error");
								getServlet().redirectTo(new States(requestContext));				
							}	
						}
					});
					stateData.apply(stateData.getListPageData());	
				}
				else if(queryArg == "add"){
					StatesData stateData = new StatesData(new OnlineOfflineCallbacks(this) {
						public void onlineSuccessCallback(String addData) {
							if(addData != null) {
								RequestContext requestContext = new RequestContext();
								requestContext.getArgs().put("action", "add");
								requestContext.getArgs().put("addPageData", addData);
								getServlet().fillTemplate(new StatesTemplate(requestContext));
								//getServlet().redirectTo(new States(requestContext ));						
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
							getServlet().redirectTo(new States(requestContext));	
						}
						
						public void offlineSuccessCallback(Object addData) {
							if((String)addData != null) {
								// Got whatever info we need to display for this GET request, so go ahead
								// and display it by filling in the template.  No need to redirect.
								getServlet().getRequestContext().getArgs().put("addPageData", (String)addData);
								getServlet().fillTemplate(new StatesTemplate(getServlet().getRequestContext()));
							} else {
								RequestContext requestContext = new RequestContext();
								requestContext.setMessage("Local Database error");
								getServlet().redirectTo(new States(requestContext));				
							}	
						}
					});
					stateData.apply(stateData.getAddPageData());	
				}
				else{
					this.fillTemplate(new StatesTemplate(this.requestContext));
				}
				
			}
			
		}
	}
}

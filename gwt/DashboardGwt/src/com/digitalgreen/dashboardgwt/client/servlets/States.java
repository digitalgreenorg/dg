package com.digitalgreen.dashboardgwt.client.servlets;

import java.util.HashMap;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.BaseData;
import com.digitalgreen.dashboardgwt.client.data.StatesData;
import com.digitalgreen.dashboardgwt.client.templates.StatesTemplate;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.HTMLPanel;

public class States extends BaseServlet {
	
	public States() {
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
				StatesData statesData = new StatesData(new OnlineOfflineCallbacks(this) {
					public void onlineSuccessCallback(String results) {
						if(this.getStatusCode() == 200) {
							RequestContext requestContext = new RequestContext();
							requestContext.setMessage("State successfully saved");
							requestContext.getArgs().put("action", "list");
							getServlet().redirectTo(new States(requestContext));
						} else {
							getServlet().getRequestContext().setMethodTypeCtx(RequestContext.METHOD_GET);
							getServlet().getRequestContext().setErrorMessage(results) ;
							getServlet().redirectTo(new States(getServlet().getRequestContext()));	
						}
					}
					
					public void onlineErrorCallback(int errorCode) {
						getServlet().getRequestContext().setMethodTypeCtx(RequestContext.METHOD_GET);
						if (errorCode == BaseData.ERROR_RESPONSE)
							getServlet().getRequestContext().setMessage("Unresponsive Server.  Please contact support.");
						else if (errorCode == BaseData.ERROR_SERVER)
							getServlet().getRequestContext().setMessage("Problem in the connection with the server.");
						else
							getServlet().getRequestContext().setMessage("Unknown error.  Please contact support.");
						getServlet().redirectTo(new States(getServlet().getRequestContext()));	
					}
					
					public void offlineSuccessCallback(Object results) {
						if((Boolean)results) {
							RequestContext requestContext = new RequestContext();
							requestContext.setMessage("State successfully saved");
							requestContext.getArgs().put("action", "list");
							getServlet().redirectTo(new States(requestContext));
						} else {
							// It's no longer a POST because there was an error, so start again.
							getServlet().getRequestContext().setMethodTypeCtx(RequestContext.METHOD_GET);
							getServlet().getRequestContext().setErrorMessage(getServlet().getRequestContext().getForm().printFormErrors());
							getServlet().redirectTo(new States(getServlet().getRequestContext()));			
						}
					}
				}, form);
				if(this.requestContext.getArgs().get("action").equals("edit")) {
					form.setId((String)this.requestContext.getArgs().get("id"));
					statesData.apply(statesData.postPageData(form.getId()));
				}
				else{
					statesData.apply(statesData.postPageData());
				}
				
			}
			else {
				HashMap queryArgs = (HashMap)this.requestContext.getArgs();
				String queryArg = (String)queryArgs.get("action");
				if(queryArg.equals("list")){
					StatesData statesData = new StatesData(new OnlineOfflineCallbacks(this) {
						public void onlineSuccessCallback(String results) {
							if(this.getStatusCode() == 200) {
								StatesData statesData = new StatesData();
								if(!results.equals("EOF")){
									List states = statesData.getListingOnline(results);
									getServlet().getRequestContext().getArgs().put("listing", states);
								}
								getServlet().fillTemplate(new StatesTemplate(getServlet().getRequestContext()));						
							} else {
								RequestContext requestContext = new RequestContext();
								requestContext.setErrorMessage("Unexpected error occured in retriving data. Please contact support");
								getServlet().redirectTo(new Index(requestContext));
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
							getServlet().redirectTo(new Index(requestContext));
						}
						
						public void offlineSuccessCallback(Object results) {
							if((Boolean)results) {
								StatesData statesData = new StatesData();
								List states = statesData.getStatesListingOffline();
								requestContext.getArgs().put("listing", states);
								getServlet().fillTemplate(new StatesTemplate(getServlet().getRequestContext()));
							} else {
								RequestContext requestContext = new RequestContext();
								requestContext.setMessage("Unexpected local error. Please contact support");
								getServlet().redirectTo(new Index(requestContext));				
							}	
						}
					});
					statesData.apply(statesData.getListPageData());
				}
				else if(queryArg.equals("add") || queryArg.equals("edit")){
					Form form = this.requestContext.getForm();
					StatesData statesData = new StatesData(new OnlineOfflineCallbacks(this) {
						public void onlineSuccessCallback(String addData) {
							if(this.getStatusCode() == 200) {
								if(getServlet().getRequestContext().getArgs().get("action").equals("edit")) {
									if(getServlet().getRequestContext().getForm().getQueryString() == null) {
										getServlet().getRequestContext().getForm().setQueryString(Form.retriveQueryStringFromHTMLString(addData));
									}
								}
								getServlet().getRequestContext().getArgs().put("addPageData", addData);
								getServlet().fillTemplate(new StatesTemplate(getServlet().getRequestContext()));
							} else {
								RequestContext requestContext = new RequestContext();
								requestContext.setErrorMessage("Unexpected error occured in retriving data. Please contact support");
								getServlet().redirectTo(new Index(requestContext));
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
							getServlet().redirectTo(new Index(requestContext));	
						}
						
						public void offlineSuccessCallback(Object addData) {
							if((String)addData != null) {
								// Got whatever info we need to display for this GET request, so go ahead
								// and display it by filling in the template.  No need to redirect.
								getServlet().getRequestContext().getArgs().put("addPageData", (String)addData);
								getServlet().fillTemplate(new StatesTemplate(getServlet().getRequestContext()));
							} else {
								RequestContext requestContext = new RequestContext();
								requestContext.setMessage("Unexpected local error. Please contact support");
								getServlet().redirectTo(new Index(requestContext));				
							}	
						}
					}, form);
					if(queryArg.equals("add")) {
						statesData.apply(statesData.getAddPageData());
					}
					else{
						form.setId((String)this.requestContext.getArgs().get("id"));
						statesData.apply(statesData.getAddPageData(form.getId()));
					}
				}
			}
		}
	}
}
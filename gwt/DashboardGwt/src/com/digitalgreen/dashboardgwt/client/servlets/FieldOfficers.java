package com.digitalgreen.dashboardgwt.client.servlets;

import java.util.HashMap;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.BaseData;
import com.digitalgreen.dashboardgwt.client.data.FieldOfficersData;
import com.digitalgreen.dashboardgwt.client.templates.FieldOfficerTemplate;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.HTMLPanel;

public class FieldOfficers extends BaseServlet {
	
	public FieldOfficers() {
		super();
	}
	
	public FieldOfficers(RequestContext requestContext) {
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
				FieldOfficersData fieldOfficersData = new FieldOfficersData(new OnlineOfflineCallbacks(this) {
					public void onlineSuccessCallback(String results) {
						if(this.getStatusCode() == 200) {
							RequestContext requestContext = new RequestContext();
							requestContext.setMessage("FieldOfficer successfully saved");
							requestContext.getArgs().put("action", "list");
							getServlet().redirectTo(new FieldOfficers(requestContext));
						} else {
							getServlet().getRequestContext().setMethodTypeCtx(RequestContext.METHOD_GET);
							getServlet().getRequestContext().setErrorMessage(results) ;
							getServlet().redirectTo(new FieldOfficers(getServlet().getRequestContext()));	
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
						getServlet().redirectTo(new FieldOfficers(getServlet().getRequestContext()));	
					}
					
					public void offlineSuccessCallback(Object results) {
						if((Boolean)results) {
							RequestContext requestContext = new RequestContext();
							requestContext.setMessage("FieldOfficer successfully saved");
							requestContext.getArgs().put("action", "list");
							getServlet().redirectTo(new FieldOfficers(requestContext));
						} else {
							// It's no longer a POST because there was an error, so start again.
							getServlet().getRequestContext().setMethodTypeCtx(RequestContext.METHOD_GET);
							getServlet().getRequestContext().setErrorMessage(getServlet().getRequestContext().getForm().printFormErrors());
							getServlet().redirectTo(new FieldOfficers(getServlet().getRequestContext()));			
						}
					}
				}, form);
				if(this.requestContext.getArgs().get("action").equals("edit")) {
					fieldOfficersData.apply(fieldOfficersData.postPageData((String)this.requestContext.getArgs().get("id")));
				}
				else{
					fieldOfficersData.apply(fieldOfficersData.postPageData());
				}
				
			}
			else {
				HashMap queryArgs = (HashMap)this.requestContext.getArgs();
				String queryArg = (String)queryArgs.get("action");
				if(queryArg.equals("list")){
					FieldOfficersData fieldOfficersData = new FieldOfficersData(new OnlineOfflineCallbacks(this) {
						public void onlineSuccessCallback(String results) {
							if(this.getStatusCode() == 200) {
								FieldOfficersData fieldOfficersData = new FieldOfficersData();
								List fieldOfficers = fieldOfficersData.getListingOnline(results);
								getServlet().getRequestContext().getArgs().put("listing", fieldOfficers);
								getServlet().fillTemplate(new FieldOfficerTemplate(getServlet().getRequestContext()));						
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
								FieldOfficersData fieldOfficersData = new FieldOfficersData();
								List fieldOfficers = fieldOfficersData.getFieldOfficersListingOffline();
								requestContext.getArgs().put("listing", fieldOfficers);
								getServlet().fillTemplate(new FieldOfficerTemplate(getServlet().getRequestContext()));
							} else {
								RequestContext requestContext = new RequestContext();
								requestContext.setMessage("Unexpected local error. Please contact support");
								getServlet().redirectTo(new Index(requestContext));				
							}	
						}
					});
					fieldOfficersData.apply(fieldOfficersData.getListPageData());
				}
				else if(queryArg.equals("add") || queryArg.equals("edit")){
					Form form = this.requestContext.getForm();
					FieldOfficersData fieldOfficersData = new FieldOfficersData(new OnlineOfflineCallbacks(this) {
						public void onlineSuccessCallback(String addData) {
							if(this.getStatusCode() == 200) {
								if(getServlet().getRequestContext().getArgs().get("action").equals("edit")) {
									if(getServlet().getRequestContext().getForm().getQueryString() == null) {
										getServlet().getRequestContext().getForm().setQueryString(Form.retriveQueryStringFromHTMLString(addData));
									}
								}
								getServlet().getRequestContext().getArgs().put("addPageData", addData);
								getServlet().fillTemplate(new FieldOfficerTemplate(getServlet().getRequestContext()));
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
								getServlet().fillTemplate(new FieldOfficerTemplate(getServlet().getRequestContext()));
							} else {
								Window.alert("here2");
								RequestContext requestContext = new RequestContext();
								requestContext.setMessage("Unexpected local error. Please contact support");
								getServlet().redirectTo(new Index(requestContext));				
							}	
						}
					}, form);
					if(queryArg.equals("add")) {
						fieldOfficersData.apply(fieldOfficersData.getAddPageData());
					}
					else{
						form.setId((String)this.requestContext.getArgs().get("id"));
						fieldOfficersData.apply(fieldOfficersData.getAddPageData(this.requestContext.getArgs().get("id").toString()));
					}
				}
			}
		}
	}
}
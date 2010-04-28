package com.digitalgreen.dashboardgwt.client.servlets;

import java.util.HashMap;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.BaseData;
import com.digitalgreen.dashboardgwt.client.data.PracticesData;
import com.digitalgreen.dashboardgwt.client.templates.PracticeTemplate;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.HTMLPanel;

public class Practices extends BaseServlet {
	
	public Practices() {
		super();
	}
	
	public Practices(RequestContext requestContext) {
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
				PracticesData practicesData = new PracticesData(new OnlineOfflineCallbacks(this) {
					public void onlineSuccessCallback(String results) {
						if(this.getStatusCode() == 200) {
							RequestContext requestContext = new RequestContext();
							requestContext.setMessage("Practices successfully saved");
							requestContext.getArgs().put("action", "list");
							getServlet().redirectTo(new Practices(requestContext));
						} else {
							getServlet().getRequestContext().setMethodTypeCtx(RequestContext.METHOD_GET);
							getServlet().getRequestContext().setErrorMessage(results) ;
							getServlet().redirectTo(new Practices(getServlet().getRequestContext()));	
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
						getServlet().redirectTo(new Practices(getServlet().getRequestContext()));	
					}
					
					public void offlineSuccessCallback(Object results) {
						if((Boolean)results) {
							RequestContext requestContext = new RequestContext();
							requestContext.setMessage("Practice successfully saved");
							requestContext.getArgs().put("action", "list");
							getServlet().redirectTo(new Practices(requestContext));
						} else {
							// It's no longer a POST because there was an error, so start again.
							getServlet().getRequestContext().setMethodTypeCtx(RequestContext.METHOD_GET);
							getServlet().getRequestContext().setErrorMessage(getServlet().getRequestContext().getForm().printFormErrors());
							getServlet().redirectTo(new Practices(getServlet().getRequestContext()));			
						}
					}
				}, form);
				if(this.requestContext.getArgs().get("action").equals("edit")) {
					form.setId((String)this.requestContext.getArgs().get("id"));
					practicesData.apply(practicesData.postPageData(form.getId()));
				}
				else{
					practicesData.apply(practicesData.postPageData());
				}
				
			}
			else {
				HashMap queryArgs = (HashMap)this.requestContext.getArgs();
				String queryArg = (String)queryArgs.get("action");
				if(queryArg.equals("list")){
					PracticesData practicesData = new PracticesData(new OnlineOfflineCallbacks(this) {
						public void onlineSuccessCallback(String results) {
							if(this.getStatusCode() == 200) {
								PracticesData practicesData = new PracticesData();
								List practices = practicesData.getListingOnline(results);
								getServlet().getRequestContext().getArgs().put("listing", practices);
								getServlet().fillTemplate(new PracticeTemplate(getServlet().getRequestContext()));						
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
								PracticesData practicesData = new PracticesData();
								List practices = practicesData.getPracticesListingOffline();
								requestContext.getArgs().put("listing", practices);
								getServlet().fillTemplate(new PracticeTemplate(getServlet().getRequestContext()));
							} else {
								RequestContext requestContext = new RequestContext();
								requestContext.setMessage("Unexpected local error. Please contact support");
								getServlet().redirectTo(new Index(requestContext));				
							}	
						}
					});
					practicesData.apply(practicesData.getListPageData());
				}
				else if(queryArg.equals("add") || queryArg.equals("edit")){
					Form form = this.requestContext.getForm();
					PracticesData practicesData = new PracticesData(new OnlineOfflineCallbacks(this) {
						public void onlineSuccessCallback(String addData) {
							if(this.getStatusCode() == 200) {
								if(getServlet().getRequestContext().getArgs().get("action").equals("edit")) {
									if(getServlet().getRequestContext().getForm().getQueryString() == null) {
										getServlet().getRequestContext().getForm().setQueryString(Form.retriveQueryStringFromHTMLString(addData));
									}
								}
								getServlet().getRequestContext().getArgs().put("addPageData", addData);
								getServlet().fillTemplate(new PracticeTemplate(getServlet().getRequestContext()));
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
								getServlet().fillTemplate(new PracticeTemplate(getServlet().getRequestContext()));
							} else {
								RequestContext requestContext = new RequestContext();
								requestContext.setMessage("Unexpected local error. Please contact support");
								getServlet().redirectTo(new Index(requestContext));				
							}	
						}
					}, form);
					if(queryArg.equals("add")) {
						practicesData.apply(practicesData.getAddPageData());
					}
					else{
						form.setId((String)this.requestContext.getArgs().get("id"));
						practicesData.apply(practicesData.getAddPageData(form.getId()));
					}
				}
			}
		}
	}
}
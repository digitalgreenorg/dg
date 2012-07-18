package com.digitalgreen.dashboardgwt.client.servlets;

import java.util.HashMap;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.BaseData;
import com.digitalgreen.dashboardgwt.client.data.ScreeningsData;
import com.digitalgreen.dashboardgwt.client.templates.ScreeningsTemplate;
import com.google.gwt.json.client.JSONObject;
import com.google.gwt.json.client.JSONParser;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.HTMLPanel;

public class Screenings extends BaseServlet {
	
	public Screenings() {
		super();
	}
	
	public Screenings(RequestContext requestContext) {
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
				ScreeningsData screeningsData = new ScreeningsData(new OnlineOfflineCallbacks(this) {
					public void onlineSuccessCallback(String results) {
						if(this.getStatusCode() == 200) {
							RequestContext requestContext = new RequestContext();
							requestContext.setMessage("Screenings successfully saved");
							requestContext.getArgs().put("action", "list");
							requestContext.getArgs().put("pageNum", "1");
							getServlet().redirectTo(new Screenings(requestContext));
						} else {
							getServlet().getRequestContext().setMethodTypeCtx(RequestContext.METHOD_GET);
							JSONObject resultObj = JSONParser.parse(results).isObject();
							if(getServlet().getRequestContext().getForm().getQueryString() == null) {
								String formString = resultObj.get("form").isString().stringValue();
								getServlet().getRequestContext().getForm().setQueryString(Form.retriveQueryStringFromHTMLString(formString));
							}
							
							getServlet().getRequestContext().setErrorMessage(resultObj.get("errors").isString().stringValue());
							getServlet().getRequestContext().getArgs().put("addPageData", resultObj.get("form").isString().stringValue());
							
							//getServlet().getRequestContext().getArgs().put("addPageData", addData);
							getServlet().fillTemplate(new ScreeningsTemplate(getServlet().getRequestContext()),true);
							
							//getServlet().getRequestContext().setMethodTypeCtx(RequestContext.METHOD_GET);
							//getServlet().getRequestContext().setErrorMessage(results) ;
							//getServlet().redirectTo(new Screenings(getServlet().getRequestContext()));	
							//RequestContext requestContext = new RequestContext();
							//requestContext.setMessage("Add with ");
							//requestContext.getArgs().put("action", "add");
							//requestContext.getArgs().put("pageNum", "1");
							//getServlet().redirectTo(new Screenings(requestContext));
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
						getServlet().redirectTo(new Screenings(getServlet().getRequestContext()));	
					}
					
					public void offlineSuccessCallback(Object results) {
						if((Boolean)results) {
							RequestContext requestContext = new RequestContext();
							requestContext.setMessage("Screenings successfully saved");
							requestContext.getArgs().put("action", "list");
							requestContext.getArgs().put("pageNum", "1");
							getServlet().redirectTo(new Screenings(requestContext));
						} else {
							// It's no longer a POST because there was an error, so start again.
							getServlet().getRequestContext().setMethodTypeCtx(RequestContext.METHOD_GET);
							getServlet().getRequestContext().setErrorMessage(getServlet().getRequestContext().getForm().printFormErrors());
							getServlet().redirectTo(new Screenings(getServlet().getRequestContext()));			
						}
					}
				}, form);
				if(this.requestContext.getArgs().get("action").equals("edit")) {
					form.setId((String)this.requestContext.getArgs().get("id"));
					screeningsData.apply(screeningsData.postPageData(form.getId()));
				}
				else{
					screeningsData.apply(screeningsData.postPageData());
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
					ScreeningsData screeningsData = new ScreeningsData(new OnlineOfflineCallbacks(this) {
						public void onlineSuccessCallback(String results) {
							/*String count = this.getResponse().getHeader("X-COUNT");
							getServlet().getRequestContext().getArgs().put("totalRows", count);
							if(this.getStatusCode() == 200) {
								ScreeningsData screeningsData = new ScreeningsData();
								if(!results.equals("EOF")){
									List screenings = screeningsData.getListingOnline(results);
									getServlet().getRequestContext().getArgs().put("listing", screenings);
								}
								getServlet().fillTemplate(new ScreeningsTemplate(getServlet().getRequestContext()),true);						
							} else {
								RequestContext requestContext = new RequestContext();
								requestContext.setErrorMessage("Unexpected error occured in retriving data. Please contact support");
								getServlet().redirectTo(new Index(requestContext));
							}*/
							getServlet().fillTemplate(new ScreeningsTemplate(getServlet().getRequestContext()),true);
							
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
								ScreeningsData screeningsData = new ScreeningsData();
								List screenings;
								String pageNum = (String)getServlet().getRequestContext().getArgs().get("pageNum");
								String operation = (String)getServlet().getRequestContext().getArgs().get("operation");
								if(operation == "search") {
									String searchText = (String)getServlet().getRequestContext().getArgs().get("searchText");
									screenings = screeningsData.getScreeningsListingOffline(pageNum, searchText);
									requestContext.getArgs().put("totalRows", screeningsData.getCount(searchText));
								}
								else {
									screenings = screeningsData.getScreeningsListingOffline(pageNum);
									requestContext.getArgs().put("totalRows", screeningsData.getCount());
								}
								requestContext.getArgs().put("listing", screenings);
								getServlet().fillTemplate(new ScreeningsTemplate(getServlet().getRequestContext()),false);
							} else {
								RequestContext requestContext = new RequestContext();
								requestContext.setErrorMessage("Unexpected local error. Please contact support");
								getServlet().redirectTo(new Index(requestContext));				
							}	
						}
					});
					if (operation == "search") {
						screeningsData.apply(screeningsData.getListPageData(pageNum, searchText));
					} else {
						screeningsData.apply(screeningsData.getListPageData(pageNum));						
					}
				}
				else if(queryArg.equals("add") || queryArg.equals("edit")){
					//Window.alert("enterd");
					Form form = this.requestContext.getForm();
					ScreeningsData screeningsData = new ScreeningsData(new OnlineOfflineCallbacks(this) {
						public void onlineSuccessCallback(String results) {
							//Window.alert("Callback()");
							JSONObject resultObj = JSONParser.parse(results).isObject();
							String formString = resultObj.get("form").isString().stringValue();
							
							if(this.getStatusCode() == 200) {
								if(getServlet().getRequestContext().getArgs().get("action").equals("edit")) {
									if(getServlet().getRequestContext().getForm().getQueryString() == null) {
										getServlet().getRequestContext().getForm().setQueryString(Form.retriveQueryStringFromHTMLString(formString));
									}
								}
								getServlet().getRequestContext().getArgs().put("addPageData", formString);
								getServlet().fillTemplate(new ScreeningsTemplate(getServlet().getRequestContext()),true);
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
								getServlet().fillTemplate(new ScreeningsTemplate(getServlet().getRequestContext()),false);
							} else {
								RequestContext requestContext = new RequestContext();
								requestContext.setErrorMessage("Unexpected local error. Please contact support");
								getServlet().redirectTo(new Index(requestContext));				
							}	
						}
					}, form);
					if(queryArg.equals("add")) {
						screeningsData.apply(screeningsData.getAddPageData());
					}
					else{
						form.setId((String)this.requestContext.getArgs().get("id"));
						screeningsData.apply(screeningsData.getAddPageData(form.getId()));
					}
				}
			}
		}
	}
}
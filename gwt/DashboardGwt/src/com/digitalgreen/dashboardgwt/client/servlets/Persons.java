package com.digitalgreen.dashboardgwt.client.servlets;

import java.util.HashMap;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.BaseData;
import com.digitalgreen.dashboardgwt.client.data.PersonsData;
import com.digitalgreen.dashboardgwt.client.templates.PersonsTemplate;
import com.digitalgreen.dashboardgwt.client.templates.TrainingTemplate;


public class Persons extends BaseServlet {
	
	public Persons(){
		super();
	}
	
	public Persons(RequestContext requestContext) {
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
				PersonsData personData = new PersonsData(new OnlineOfflineCallbacks(this) {
					public void onlineSuccessCallback(String results) {
						if(results != null) {
							PersonsData persondata = new PersonsData();
							List persons = persondata.getListingOnline(results);
							RequestContext requestContext = new RequestContext();
							requestContext.setMessageString("Person successfully saved");
							requestContext.getArgs().put("listing", persons);
							getServlet().redirectTo(new Persons(requestContext ));						
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
						getServlet().redirectTo(new Persons(requestContext));	
					}
					
					public void offlineSuccessCallback(Object results) {
						if((Boolean)results) {
							PersonsData persondata = new PersonsData();
							List persons = persondata.getPersonsListingOffline();
							RequestContext requestContext = new RequestContext();
							requestContext.setMessageString("Person successfully saved");
							requestContext.getArgs().put("listing", persons);
							getServlet().redirectTo(new Persons(requestContext ));
						} else {
							// It's no longer a POST because there was an error, so start again.
							getServlet().getRequestContext().setMethodTypeCtx(RequestContext.METHOD_GET);
							getServlet().getRequestContext().getArgs().put("action", "add");		
							getServlet().redirectTo(new Persons(getServlet().getRequestContext()));				
						}
						
					}
				}, form);
				
				personData.apply(personData.postPageData());

			}
			else{
				HashMap queryArgs = (HashMap)this.requestContext.getArgs();
				String queryArg = (String)queryArgs.get("action");
				if(queryArg == "list"){
					PersonsData personData = new PersonsData(new OnlineOfflineCallbacks(this) {
						public void onlineSuccessCallback(String results) {
							if(results != null) {
								PersonsData persondata = new PersonsData();
								List persons = persondata.getListingOnline(results);
								RequestContext requestContext = new RequestContext();
								requestContext.getArgs().put("listing", persons);
								getServlet().fillTemplate(new PersonsTemplate(requestContext));						
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
							getServlet().redirectTo(new Persons(requestContext));	
						}
						
						public void offlineSuccessCallback(Object results) {
							if((Boolean)results) {
								PersonsData persondata = new PersonsData();
								List persons = persondata.getPersonsListingOffline();
								RequestContext requestContext = new RequestContext();
								requestContext.getArgs().put("listing", persons);
								getServlet().fillTemplate(new PersonsTemplate(requestContext));
							} else {
								RequestContext requestContext = new RequestContext();
								requestContext.setMessageString("Local Database error");
								getServlet().redirectTo(new Persons(requestContext));				
							}	
						}
					});
					personData.apply(personData.getListPageData());	
				}
				else if(queryArg == "add"){
					PersonsData personData = new PersonsData(new OnlineOfflineCallbacks(this) {
						public void onlineSuccessCallback(String addData) {
							if(addData != null) {
								// Got whatever info we need to display for this GET request, so go ahead
								// and display it by filling in the template.  No need to redirect.
								getServlet().getRequestContext().getArgs().put("addPageData", (String)addData);
								getServlet().fillTemplate(new PersonsTemplate(getServlet().getRequestContext()));
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
							getServlet().redirectTo(new Persons(requestContext));	
						}
						
						public void offlineSuccessCallback(Object addData) {
							if((String)addData != null) {
								RequestContext requestContext = new RequestContext();
								requestContext.getArgs().put("action", "add");
								requestContext.getArgs().put("addPageData", (String)addData);
								getServlet().fillTemplate(new PersonsTemplate(requestContext));
							} else {
								RequestContext requestContext = new RequestContext();
								requestContext.setMessageString("Local Database error");
								getServlet().redirectTo(new Persons(requestContext));				
							}	
						}
					});
					personData.apply(personData.getAddPageData());	
				} else {
					this.fillTemplate(new PersonsTemplate(this.requestContext));
				}
			}
		}
	}
}
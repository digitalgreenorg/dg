package com.digitalgreen.dashboardgwt.client.servlets;

import java.util.HashMap;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.BaseData;
import com.digitalgreen.dashboardgwt.client.data.ScreeningsData;
import com.digitalgreen.dashboardgwt.client.templates.ScreeningsTemplate;
import com.google.gwt.user.client.Window;

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
				ScreeningsData screeningData = new ScreeningsData(new OnlineOfflineCallbacks(this){
					
					@Override
					public void onlineSuccessCallback(String results) {
						if(results != null) {
							ScreeningsData screeningdata = new ScreeningsData();
							List screenings = screeningdata.getListingOnline(results);
							RequestContext requestContext = new RequestContext();
							requestContext.setMessage("Screenings successfully saved");
							requestContext.getArgs().put("listing", screenings);
							getServlet().redirectTo(new Screenings(requestContext ));
						}
						else {
							Window.alert("Error in saving the data.");
						}
					}
					
					@Override
					public void onlineErrorCallback(int errorCode) {
						RequestContext requestContext = new RequestContext();
						if (errorCode == BaseData.ERROR_RESPONSE)
							requestContext.setMessage("Unresponsive Server.  Please contact support.");
						else if (errorCode == BaseData.ERROR_SERVER)
							requestContext.setMessage("Problem in the connection with the server.");
						else
							requestContext.setMessage("Unknown error.  Please contact support.");
						getServlet().redirectTo(new Screenings(requestContext));	
					}
					
					@Override
					public void offlineSuccessCallback(Object results) {
						if((Boolean)results) {
							ScreeningsData screeningdata = new ScreeningsData();
							List screenings = screeningdata.getScreeningsListingOffline();
							RequestContext requestContext = new RequestContext();
							requestContext.setMessage("Screenings successfully saved");
							requestContext.getArgs().put("listing", screenings);
							getServlet().redirectTo(new Screenings(requestContext ));
						}
						else {
							RequestContext requestContext = new RequestContext();
							requestContext.setMessage("Invalid data, please try again");
							getServlet().redirectTo(new Screenings(requestContext));				
						}
					}
				}, form);
				
				screeningData.apply(screeningData.postPageData());
			}
			else {
				HashMap queryArgs = (HashMap)this.requestContext.getArgs();
				String queryArg = (String)queryArgs.get("action");
				if(queryArg == "list"){
					ScreeningsData screeningData = new ScreeningsData(new OnlineOfflineCallbacks(this){
						
						@Override
						public void onlineSuccessCallback(String results) {
							if(results != null) {
								ScreeningsData screeningdata = new ScreeningsData();
								List screenings = screeningdata.getListingOnline(results);
								RequestContext requestContext = new RequestContext();
								requestContext.getArgs().put("listing", screenings);
								getServlet().fillTemplate(new ScreeningsTemplate(requestContext));
							}
							else {
								Window.alert("Error in saving the data.");
							}
						}
						
						@Override
						public void onlineErrorCallback(int errorCode) {
							RequestContext requestContext = new RequestContext();
							if (errorCode == BaseData.ERROR_RESPONSE)
								requestContext.setMessage("Unresponsive Server.  Please contact support.");
							else if (errorCode == BaseData.ERROR_SERVER)
								requestContext.setMessage("Problem in the connection with the server.");
							else
								requestContext.setMessage("Unknown error.  Please contact support.");
							getServlet().redirectTo(new Screenings(requestContext));
						}
						
						@Override
						public void offlineSuccessCallback(Object results) {
							if((Boolean)results) {
								ScreeningsData screeningdata = new ScreeningsData();
								List screenings = screeningdata.getScreeningsListingOffline();
								RequestContext requestContext = new RequestContext();
								requestContext.getArgs().put("listing", screenings);
								getServlet().fillTemplate(new ScreeningsTemplate(requestContext));
							}
							else {
								RequestContext requestContext = new RequestContext();
								requestContext.setMessage("Local Database error");
								getServlet().redirectTo(new Screenings(requestContext));				
							}
						}
					});
					screeningData.apply(screeningData.getListPageData());
				}
				else if(queryArg == "add"){
					ScreeningsData screeningData = new ScreeningsData(new OnlineOfflineCallbacks(this){
						
						@Override
						public void onlineSuccessCallback(String addData) {
							if(addData != null) {
								RequestContext requestContext = new RequestContext();
								requestContext.getArgs().put("action", "add");
								requestContext.getArgs().put("addPageData", addData);
								getServlet().fillTemplate(new ScreeningsTemplate(requestContext));
							}
							else {
								Window.alert("Error in saving the data.");
							}
						}
						
						@Override
						public void onlineErrorCallback(int errorCode) {
							RequestContext requestContext = new RequestContext();
							if (errorCode == BaseData.ERROR_RESPONSE)
								requestContext.setMessage("Unresponsive Server.  Please contact support.");
							else if (errorCode == BaseData.ERROR_SERVER)
								requestContext.setMessage("Problem in the connection with the server.");
							else
								requestContext.setMessage("Unknown error.  Please contact support.");
							getServlet().redirectTo(new Screenings(requestContext));	
						}
						
						@Override
						public void offlineSuccessCallback(Object addData) {
							if((String)addData != null) {
								RequestContext requestContext = new RequestContext();
								requestContext.getArgs().put("action", "add");
								requestContext.getArgs().put("addPageData", (String)addData);
								getServlet().fillTemplate(new ScreeningsTemplate(requestContext));
							}
							else {
								RequestContext requestContext = new RequestContext();
								requestContext.setMessage("Local Database error");
								getServlet().redirectTo(new Screenings(requestContext));				
							}
						}
					});
					screeningData.apply(screeningData.getAddPageData());
				}
				else {
					this.fillTemplate(new ScreeningsTemplate(this.requestContext));
				}
			}
		}
	}
}
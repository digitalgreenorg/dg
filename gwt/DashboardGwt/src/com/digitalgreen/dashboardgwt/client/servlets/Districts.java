package com.digitalgreen.dashboardgwt.client.servlets;

import java.util.HashMap;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.BaseData;
import com.digitalgreen.dashboardgwt.client.data.DistrictsData;
import com.digitalgreen.dashboardgwt.client.templates.DistrictTemplate;
import com.google.gwt.user.client.Window;

public class Districts extends BaseServlet{

	public Districts(){
		super();
	}
	
	public Districts(RequestContext requestContext) {
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
				DistrictsData districtData = new DistrictsData(new OnlineOfflineCallbacks(this){
					public void onlineSuccessCallback(String results) {
						if(results != null) {
							DistrictsData districtdata = new DistrictsData();
							List districts = districtdata.getListingOnline(results);
							RequestContext requestContext = new RequestContext();
							requestContext.setMessageString("District successfully saved");
							requestContext.getArgs().put("listing", districts);
							getServlet().redirectTo(new Districts(requestContext ));
						}
						else {
							// Error in saving data
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
						getServlet().redirectTo(new Districts(requestContext));
					}
					
					public void offlineSuccessCallback(Object results) {
						if((Boolean)results) {
							DistrictsData districtdata = new DistrictsData();
							List districts = districtdata.getDistrictsListingsOffline();
							RequestContext requestContext = new RequestContext();
							requestContext.setMessageString("District successfully saved");
							requestContext.getArgs().put("listing", districts);
							getServlet().redirectTo(new Districts(requestContext ));
						}
						else {
							// It's no longer a POST because there was an error, so start again.
							getServlet().getRequestContext().setMethodTypeCtx(RequestContext.METHOD_GET);
							getServlet().getRequestContext().getArgs().put("action", "add");		
							getServlet().redirectTo(new Districts(getServlet().getRequestContext()));
						}
					}
				}, form);
				
				districtData.apply(districtData.postPageData());
			}
			else {
				HashMap queryArgs = (HashMap)this.requestContext.getArgs();
				String queryArg = (String)queryArgs.get("action");
				if(queryArg == "list") {
					DistrictsData districtData = new DistrictsData(new OnlineOfflineCallbacks(this){
						public void onlineSuccessCallback(String results) {
							if(results != null) {
								DistrictsData districtdata = new DistrictsData();
								List districts = districtdata.getListingOnline(results);
								RequestContext requestContext = new RequestContext();
								requestContext.getArgs().put("listing", districts);
								getServlet().fillTemplate(new DistrictTemplate(requestContext));
							}
							else {
								// Error in saving the data			
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
							getServlet().redirectTo(new Districts(requestContext));
						}
						
						public void offlineSuccessCallback(Object results) {
							if((Boolean)results) {
								DistrictsData districtdata = new DistrictsData();
								List districts = districtdata.getDistrictsListingsOffline();
								RequestContext requestContext = new RequestContext();
								requestContext.getArgs().put("listing", districts);
								getServlet().fillTemplate(new DistrictTemplate(requestContext));
							} 
							else {
								RequestContext requestContext = new RequestContext();
								requestContext.setMessageString("Local Database error");
								getServlet().redirectTo(new Districts(requestContext));
							}
						}
					});
					districtData.apply(districtData.getListPageData());
				}
				else if(queryArg == "add"){
					DistrictsData districtData = new DistrictsData(new OnlineOfflineCallbacks(this){
						public void onlineSuccessCallback(String addData) {
							if(addData != null) {
								RequestContext requestContext = new RequestContext();
								requestContext.getArgs().put("action", "add");
								requestContext.getArgs().put("addPageData", addData);
								getServlet().fillTemplate(new DistrictTemplate(requestContext));
							}
							else{
								// error in saving data
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
							getServlet().redirectTo(new Districts(requestContext));	
						}
						
						public void offlineSuccessCallback(Object addData) {
							if((String)addData != null) {
								// Got whatever info we need to display for this GET request, so go ahead
								// and display it by filling in the template.  No need to redirect.
								getServlet().getRequestContext().getArgs().put("addPageData", (String)addData);
								getServlet().fillTemplate(new DistrictTemplate(getServlet().getRequestContext()));
							} else {
								RequestContext requestContext = new RequestContext();
								requestContext.setMessageString("Local Database error");
								getServlet().redirectTo(new Districts(requestContext));				
							}
						}
					});
					districtData.apply(districtData.getAddPageData());
				}
				else {
					this.fillTemplate(new DistrictTemplate(this.requestContext));
				}
			}
		}
	}
}
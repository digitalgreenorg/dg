package com.digitalgreen.dashboardgwt.client.servlets;

import java.util.HashMap;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.BaseData;
import com.digitalgreen.dashboardgwt.client.data.RegionsData;
import com.digitalgreen.dashboardgwt.client.templates.RegionsTemplate;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.HTMLPanel;

public class Regions extends BaseServlet {
	public Regions() {
		super();
	}
	
	public Regions(RequestContext requestContext) {
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
				RegionsData regionData = new RegionsData(new OnlineOfflineCallbacks(this) {
					public void onlineSuccessCallback(String results) {
						if(this.getStatusCode() == 200) {
							RegionsData regiondata = new RegionsData();
							List regions = regiondata.getListingOnline(results);
							RequestContext requestContext = new RequestContext();
							requestContext.setMessage("Region successfully saved");
							requestContext.getArgs().put("listing", regions);
							getServlet().redirectTo(new Regions(requestContext ));						
						} else {
							getServlet().getRequestContext().setMethodTypeCtx(RequestContext.METHOD_GET);
							getServlet().getRequestContext().getArgs().put("action", "add");
							getServlet().getRequestContext().setErrorMessage(results);
							getServlet().redirectTo(new Regions(getServlet().getRequestContext()));
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
						getServlet().redirectTo(new Regions(requestContext));	
					}
					
					public void offlineSuccessCallback(Object results) {
						if((Boolean)results) {
							RegionsData regiondata = new RegionsData();
							List regions = regiondata.getRegionsListingOffline();
							RequestContext requestContext = new RequestContext();
							requestContext.setMessage("Region successfully saved");
							requestContext.getArgs().put("listing", regions);
							getServlet().redirectTo(new Regions(requestContext ));
						} else {
							// It's no longer a POST because there was an error, so start again.
							getServlet().getRequestContext().setMethodTypeCtx(RequestContext.METHOD_GET);
							getServlet().getRequestContext().getArgs().put("action", "add");
							getServlet().getRequestContext().setErrorMessage(getServlet().getRequestContext().getForm().printFormErrors());
							getServlet().redirectTo(new Regions(getServlet().getRequestContext()));
						}
						
					}
				}, form);
				
				regionData.apply(regionData.postPageData());

			}
			else {
				HashMap queryArgs = (HashMap)this.requestContext.getArgs();
				String queryArg = (String)queryArgs.get("action");
				if(queryArg.equals("list")){
					RegionsData regionData = new RegionsData(new OnlineOfflineCallbacks(this) {
						public void onlineSuccessCallback(String results) {
							if(results != null) {
								RegionsData regiondata = new RegionsData();
								List regions = regiondata.getListingOnline(results);
								RequestContext requestContext = new RequestContext();
								requestContext.getArgs().put("listing", regions);
								getServlet().redirectTo(new Regions(requestContext ));						
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
							getServlet().redirectTo(new Regions(requestContext));	
						}
						
						public void offlineSuccessCallback(Object results) {
							if((Boolean)results) {
								RegionsData regiondata = new RegionsData();
								List regions = regiondata.getRegionsListingOffline();
								RequestContext requestContext = new RequestContext();
								requestContext.getArgs().put("listing", regions);
								getServlet().redirectTo(new Regions(requestContext ));
							} else {
								RequestContext requestContext = new RequestContext();
								requestContext.setMessage("Local Database error");
								getServlet().redirectTo(new Regions(requestContext));				
							}	
						}
					});
					regionData.apply(regionData.getPageData());	
				}
				else{
					this.fillTemplate(new RegionsTemplate(this.requestContext));
				}
			}
		}
	}
}

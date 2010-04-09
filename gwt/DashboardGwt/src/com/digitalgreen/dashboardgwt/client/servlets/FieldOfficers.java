package com.digitalgreen.dashboardgwt.client.servlets;

import java.util.List;
import java.util.HashMap;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;

import com.digitalgreen.dashboardgwt.client.data.BaseData;
import com.digitalgreen.dashboardgwt.client.data.FieldOfficersData;

import com.digitalgreen.dashboardgwt.client.templates.FieldOfficerTemplate;

import com.google.gwt.user.client.Window;
import com.google.gwt.json.client.JSONParser;

public class FieldOfficers extends BaseServlet{

	public FieldOfficers(){
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
			if(method.equals(RequestContext.METHOD_POST)){
				Form form = this.requestContext.getForm();
				FieldOfficersData fieldOfficerData = new FieldOfficersData(new OnlineOfflineCallbacks(this){
					public void onlineSuccessCallback(String results){
						if(results != null){
							FieldOfficersData fieldofficersData = new FieldOfficersData();
							List fieldOfficers = fieldofficersData.getListingOnline(results);
							RequestContext requestContext = new RequestContext();
							requestContext.setMessageString("Field Officer successfully saved.");
							requestContext.getArgs().put("listing", fieldOfficers);
							getServlet().redirectTo(new FieldOfficers(requestContext));
						} else {
							/*Error in saving the data*/
						}
					}
					
					public void onlineErrorCallback(int errorCode){
						RequestContext requestContext = new RequestContext();
						if (errorCode == BaseData.ERROR_RESPONSE)
							requestContext.setMessageString("Unresponsive Server.  Please contact support.");
						else if (errorCode == BaseData.ERROR_SERVER)
							requestContext.setMessageString("Problem in the connection with the server.");
						else
							requestContext.setMessageString("Unknown error.  Please contact support.");
						getServlet().redirectTo(new FieldOfficers(requestContext));
					}
					
					public void offlineSuccessCallback(Object results) {
						// If login success in the offline case		
						if((Boolean)results) {
							FieldOfficersData fieldOfficerData = new FieldOfficersData();
							List fieldOfficers = fieldOfficerData.getFieldOfficersListingOffline();
							RequestContext requestContext = new RequestContext();
							requestContext.setMessageString("Field Officer successfully saved.");
							requestContext.getArgs().put("listing", fieldOfficers);
							getServlet().redirectTo(new FieldOfficers(requestContext ));
						} else {
							RequestContext requestContext = new RequestContext();
							requestContext.setMessageString("Invalid data, please try again");
							getServlet().redirectTo(new FieldOfficers(requestContext));				
						}
					}
				}, form);
				fieldOfficerData.apply(fieldOfficerData.postPageData());
			}
			else {
				HashMap queryArgs = (HashMap)this.requestContext.getArgs();
				String queryArg = (String)queryArgs.get("action");
				if(queryArg.equals("list")){
					FieldOfficersData fieldOfficerData = new FieldOfficersData(new OnlineOfflineCallbacks(this){
						public void onlineSuccessCallback(String results){
							if(results != null){
								FieldOfficersData fieldofficerdata = new FieldOfficersData();
								List fieldOfficers = fieldofficerdata.getListingOnline(results);
								RequestContext requestContext = new RequestContext();
								requestContext.getArgs().put("listing", fieldOfficers);
								getServlet().redirectTo(new FieldOfficers(requestContext));
							} else {
								/*Error in saving the data*/			
							}
						}
						
						public void onlineErrorCallback(int errorCode){
							RequestContext requestContext = new RequestContext();
							if(errorCode == BaseData.ERROR_RESPONSE){
								requestContext.setMessageString("Unresopnsive Server. Please contact support.");
							}
							else if(errorCode == BaseData.ERROR_SERVER){
								requestContext.setMessageString("Problem in the connection with the server.");
							}
							else
								requestContext.setMessageString("Unknown error.  Please contact support.");
							getServlet().redirectTo(new FieldOfficers(requestContext));
						}
						
						public void offlineSuccessCallback(Object results){
							if((Boolean)results){
								FieldOfficersData fieldofficerdata = new FieldOfficersData();
								List fieldOfficers = fieldofficerdata.getFieldOfficersListingOffline();
								RequestContext requestContext = new RequestContext();
								requestContext.getArgs().put("listing", fieldOfficers);
								getServlet().redirectTo(new FieldOfficers(requestContext));
							}
							else {
								RequestContext requestContext = new RequestContext();
								requestContext.setMessageString("Local Database error");
								getServlet().redirectTo(new FieldOfficers(requestContext));
							}
						}
					});
					fieldOfficerData.apply(fieldOfficerData.getPageData());
					
				}
				else {
					this.fillTemplate(new FieldOfficerTemplate(this.requestContext));
				}
			}
		}
	}
}

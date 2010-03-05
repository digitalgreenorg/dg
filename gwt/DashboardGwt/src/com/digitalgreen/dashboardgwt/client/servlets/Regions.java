package com.digitalgreen.dashboardgwt.client.servlets;

import java.util.HashMap;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.ApplicationConstants;
import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.BaseData;
import com.digitalgreen.dashboardgwt.client.data.IndexData;
import com.digitalgreen.dashboardgwt.client.data.LoginData;
import com.digitalgreen.dashboardgwt.client.data.RegionsData;
import com.digitalgreen.dashboardgwt.client.templates.RegionsTemplate;
import com.digitalgreen.dashboardgwt.client.templates.ScreeningsTemplate;
import com.google.gwt.user.client.Cookies;
import com.google.gwt.user.client.Window;

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
			if(method == RequestContext.METHOD_POST) {

				//this.form = Form.flatten(this.requestContext.getQueryString());

				RegionsData regionData = new RegionsData(new OnlineOfflineCallbacks(this) {
					public void onlineSuccessCallback(String results) {
						if(results != null) {
							/*Data sucessfully saved */
							/*Do something*/								
						} else {
							/*Error in saving the data*/			
						}
					}
					
					public void onlineErrorCallback(int errorCode) {
						Window.alert("GOT AN ERROR connecting to server");
						RequestContext requestContext = new RequestContext();
						if (errorCode == BaseData.ERROR_RESPONSE)
							requestContext.setMessageString("Unresponsive Server.  Please contact support.");
						else if (errorCode == BaseData.ERROR_SERVER)
							requestContext.setMessageString("Problem in the connection with the server.");
						else
							requestContext.setMessageString("Unknown error.  Please contact support.");
						getServlet().redirectTo(new Login(requestContext));	
					}
					
					public void offlineSuccessCallback(Object results) {
						// If login success in the offline case		
						if((Boolean)results) {
							RegionsData regiondata = new RegionsData();
							List regions = regiondata.getRegions();
							RequestContext requestContext = new RequestContext();
							requestContext.getArgs().put("listing", regions);
							getServlet().redirectTo(new Regions(requestContext ));
						} else {
							RequestContext requestContext = new RequestContext();
							requestContext.setMessageString("Invalid data, please try again");
							getServlet().redirectTo(new Regions(requestContext));				
						}
						
					}
				});
				
				// Comment the below line when you are not running the code form a hosted mode.
				regionData.apply(regionData.postPageData(this.requestContext.getQueryString()));

				
				/* Comment out the below lines when running the code in the hosted mode*/ 
				/*RegionsData regiondata = new RegionsData();
				regiondata.createRegion(this.form.get("region_name").toString(), this.form.get("start_date").toString());
				List regions = regiondata.getRegions();
				RequestContext requestContext = new RequestContext();
				requestContext.getArgs().put("listing", regions);
				this.redirectTo(new Regions(requestContext ));*/
			}
			else {
				this.fillTemplate(new RegionsTemplate(this.requestContext));
			}
			
		}
	}
}

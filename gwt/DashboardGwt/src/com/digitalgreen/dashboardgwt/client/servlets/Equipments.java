package com.digitalgreen.dashboardgwt.client.servlets;

import java.util.HashMap;
import java.util.List;
import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.BaseData;
import com.digitalgreen.dashboardgwt.client.data.EquipmentsData;
import com.google.gwt.dom.client.Element;
import com.google.gwt.user.client.Cookies;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.HTMLPanel;
import com.google.gwt.user.client.ui.ListBox;
import com.google.gwt.user.client.ui.RootPanel;
import com.google.gwt.user.client.ui.Widget;
import com.google.gwt.xml.client.XMLParser;
import com.google.gwt.xml.client.Document;
import com.google.gwt.json.client.JSONParser;
import com.digitalgreen.dashboardgwt.client.templates.EquipmentsTemplate;


public class Equipments extends BaseServlet {
	
	public Equipments(){
		super();
	}
	
	public Equipments(RequestContext requestContext) {
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
				EquipmentsData equipmentData = new EquipmentsData(new OnlineOfflineCallbacks(this) {
				public void onlineSuccessCallback(String results) {
					if(results != null) {
						EquipmentsData equipmentsData = new EquipmentsData();
						List equipments = equipmentsData.getListingOnline(results);
						RequestContext requestContext = new RequestContext();
						requestContext.setMessage("Equipment successfully saved");
						requestContext.getArgs().put("listing", equipments);
						getServlet().redirectTo(new Equipments(requestContext));						
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
					getServlet().redirectTo(new Equipments(requestContext));	
				}
					
				public void offlineSuccessCallback(Object results) {
					if((Boolean)results) {
						EquipmentsData equipmentData = new EquipmentsData();
						List equipments = equipmentData.getEquipmentsListingOffline();
						RequestContext requestContext = new RequestContext();
						requestContext.setMessage("Equipment successfully saved");
						requestContext.getArgs().put("listing", equipments);
						getServlet().redirectTo(new Equipments(requestContext ));
					} else {
						// It's no longer a POST because there was an error, so start again.
						getServlet().getRequestContext().setMethodTypeCtx(RequestContext.METHOD_GET);
						getServlet().getRequestContext().getArgs().put("action", "add");
						getServlet().redirectTo(new Equipments(getServlet().getRequestContext()));
					}		
				}
			}, form);
				equipmentData.apply(equipmentData.postPageData());
			}
			else {
				HashMap queryArgs = (HashMap)this.requestContext.getArgs();
				String queryArg = (String)queryArgs.get("action");
				if(queryArg.equals("list")){
					EquipmentsData equipmentData = new EquipmentsData(new OnlineOfflineCallbacks(this) {
					public void onlineSuccessCallback(String results) {
						if(results != null) {
							EquipmentsData equipmentsData = new EquipmentsData();
							List equipments = equipmentsData.getListingOnline(results);
							RequestContext requestContext = new RequestContext();
							requestContext.getArgs().put("listing", equipments);
							getServlet().redirectTo(new Equipments(requestContext));						
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
						getServlet().redirectTo(new Equipments(requestContext));	
					}
						
					public void offlineSuccessCallback(Object addData) {
						if((String)addData != null) {
							// Got whatever info we need to display for this GET request, so go ahead
							// and display it by filling in the template.  No need to redirect.
							getServlet().getRequestContext().getArgs().put("addPageData", (String)addData);
							getServlet().fillTemplate(new EquipmentsTemplate(getServlet().getRequestContext()));
						} else {
							RequestContext requestContext = new RequestContext();
							requestContext.setMessage("Local Database error");
							getServlet().redirectTo(new Equipments(requestContext));				
						}
					}
					});
					equipmentData.apply(equipmentData.getPageData());	
				}
				else{
					this.fillTemplate(new EquipmentsTemplate(this.requestContext));
				}
			}
		}
	}

}

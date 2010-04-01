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
				Form form = (Form)this.requestContext.getArgs().get("form");
				EquipmentsData equipmentData = new EquipmentsData(new OnlineOfflineCallbacks(this) {
				public void onlineSuccessCallback(String results) {
					if(results != null) {
						EquipmentsData equipmentsData = new EquipmentsData();
						List equipments = equipmentsData.getEquipmentsListingOnline(results);
						RequestContext requestContext = new RequestContext();
						requestContext.setMessageString("Equipment successfully saved");
						requestContext.getArgs().put("listing", equipments);
						getServlet().redirectTo(new Equipments(requestContext ));						
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
					getServlet().redirectTo(new Equipments(requestContext));	
				}
					
				public void offlineSuccessCallback(Object results) {
					if((Boolean)results) {
						EquipmentsData equipmentData = new EquipmentsData();
						List equipments = equipmentData.getEquipmentsListingOffline();
						RequestContext requestContext = new RequestContext();
						requestContext.setMessageString("Equipment successfully saved");
						requestContext.getArgs().put("listing", equipments);
						getServlet().redirectTo(new Equipments(requestContext ));
					} else {
						RequestContext requestContext = new RequestContext();
						requestContext.setMessageString("Invalid data, please try again");
						getServlet().redirectTo(new Equipments(requestContext));				
					}		
				}
			}, form, this.requestContext.getQueryString());
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
							List equipments = equipmentsData.getEquipmentsListingOnline(results);
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
							requestContext.setMessageString("Unresponsive Server.  Please contact support.");
						else if (errorCode == BaseData.ERROR_SERVER)
							requestContext.setMessageString("Problem in the connection with the server.");
						else
							requestContext.setMessageString("Unknown error.  Please contact support.");
						getServlet().redirectTo(new Equipments(requestContext));	
					}
						
					public void offlineSuccessCallback(Object results) {
						if((Boolean)results) {
							EquipmentsData equipmentsData = new EquipmentsData();
							List equipments = equipmentsData.getEquipmentsListingOffline();
							RequestContext requestContext = new RequestContext();
							requestContext.getArgs().put("listing", equipments);
							getServlet().redirectTo(new Equipments(requestContext));
						} else {
							RequestContext requestContext = new RequestContext();
							requestContext.setMessageString("Local Database error");
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

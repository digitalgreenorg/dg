package com.digitalgreen.dashboardgwt.client.servlets;

import java.util.HashMap;
import java.util.List;
import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.BaseData;
import com.digitalgreen.dashboardgwt.client.data.BlocksData;
import com.digitalgreen.dashboardgwt.client.templates.BlocksTemplate;
import com.google.gwt.dom.client.Element;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.HTMLPanel;
import com.google.gwt.user.client.ui.ListBox;
import com.google.gwt.user.client.ui.RootPanel;
import com.google.gwt.user.client.ui.Widget;
import com.google.gwt.xml.client.XMLParser;
import com.google.gwt.xml.client.Document;

public class Blocks extends BaseServlet {
	
	public Blocks() {
		super();
	}
	
	public Blocks(RequestContext requestContext) {
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
				BlocksData blockData = new BlocksData(new OnlineOfflineCallbacks(this){
					
					public void onlineSuccessCallback(String results) {
						if(results != null) {
							BlocksData blockdata = new BlocksData();
							List blocks = blockdata.getBlocksOnline(results);
							RequestContext requestContext = new RequestContext();
							requestContext.setMessageString("Block successfully saved");
							requestContext.getArgs().put("listing", blocks);
							getServlet().redirectTo(new Blocks(requestContext ));
						}
						else {
							/*Error in saving the data*/
						}
					}
					
					public  void onlineErrorCallback(int errorCode) {
						RequestContext requestContext = new RequestContext();
						if (errorCode == BaseData.ERROR_RESPONSE)
							requestContext.setMessageString("Unresponsive Server.  Please contact support.");
						else if (errorCode == BaseData.ERROR_SERVER)
							requestContext.setMessageString("Problem in the connection with the server.");
						else
							requestContext.setMessageString("Unknown error.  Please contact support.");
						getServlet().redirectTo(new Blocks(requestContext));	
					}
					
					public void offlineSuccessCallback(Object results) {
						if((Boolean)results) {
							BlocksData blockdata = new BlocksData();
							List blocks = blockdata.getBlocksLsitingOffline();
							RequestContext requestContext = new RequestContext();
							requestContext.setMessageString("Block successfully saved");
							requestContext.getArgs().put("listing", blocks);
							getServlet().redirectTo(new Blocks(requestContext ));
						}
						else {
							RequestContext requestContext = new RequestContext();
							requestContext.setMessageString("Invalid data, please try again");
							getServlet().redirectTo(new Blocks(requestContext));
						}
					}
				}, form, this.requestContext.getQueryString());
				
				blockData.apply(blockData.postPageData());
			}
			else {
				HashMap queryArgs = (HashMap)this.requestContext.getArgs();
				String queryArg = (String)queryArgs.get("action");
				if(queryArg == "list"){
					BlocksData blockData = new BlocksData(new OnlineOfflineCallbacks(this){
						public void onlineSuccessCallback(String results) {
							if(results != null) {
								BlocksData blockdata = new BlocksData();
								List blocks = blockdata.getBlocksOnline(results);
								RequestContext requestContext = new RequestContext();
								requestContext.getArgs().put("listing", blocks);
								getServlet().fillTemplate(new BlocksTemplate(requestContext));
							}
							else {
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
							getServlet().redirectTo(new Blocks(requestContext));	
						}
						
						public void offlineSuccessCallback(Object results) {
							if((Boolean)results) {
								BlocksData blockdata = new BlocksData();
								List blocks = blockdata.getBlocksLsitingOffline();
								RequestContext requestContext = new RequestContext();
								requestContext.getArgs().put("listing", blocks);
								getServlet().fillTemplate(new BlocksTemplate(requestContext));
							}
							else {
								RequestContext requestContext = new RequestContext();
								requestContext.setMessageString("Local Database error");
								getServlet().redirectTo(new Blocks(requestContext));				
							}
						}
					});
					blockData.apply(blockData.getListPageData());
				}
				else if(queryArg == "add"){
					BlocksData blockData = new BlocksData(new OnlineOfflineCallbacks(this){
						public void onlineSuccessCallback(String addData) {
							if(addData != null) {
								RequestContext requestContext = new RequestContext();
								requestContext.getArgs().put("action", "add");
								requestContext.getArgs().put("addPageData", addData);
								getServlet().fillTemplate(new BlocksTemplate(requestContext));
							}
							else {
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
							getServlet().redirectTo(new Blocks(requestContext));	
						}
						
						public void offlineSuccessCallback(Object addData) {
							if((String)addData != null) {
								RequestContext requestContext = new RequestContext();
								requestContext.getArgs().put("action", "add");
								requestContext.getArgs().put("addPageData", (String)addData);
								getServlet().fillTemplate(new BlocksTemplate(requestContext));
							}
							else {
								RequestContext requestContext = new RequestContext();
								requestContext.setMessageString("Local Database error");
								getServlet().redirectTo(new Blocks(requestContext));
							}
						}
					});
					
					blockData.apply(blockData.getAddPageData());
				}
				else {
					this.fillTemplate(new BlocksTemplate(this.requestContext));
				}
			}
		}
	}
}
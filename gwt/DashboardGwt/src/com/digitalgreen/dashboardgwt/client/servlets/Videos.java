package com.digitalgreen.dashboardgwt.client.servlets;

import java.util.HashMap;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.BaseData;
import com.digitalgreen.dashboardgwt.client.data.VideosData;
import com.digitalgreen.dashboardgwt.client.templates.VideosTemplate;

public class Videos extends BaseServlet {
	
	public Videos() {
		super();
	}
	
	public Videos(RequestContext requestContext) {
		super(requestContext);
	}
	
	@Override
	public void response() {
		super.response();
		
		if (!this.isLoggedIn()) {
			super.redirectTo(new Login());
		}else {
			String method = this.getMethodTypeCtx();
			if(method.equals(RequestContext.METHOD_POST)) {
				Form form = (Form)this.requestContext.getArgs().get("form");
				VideosData videoData = new VideosData(new OnlineOfflineCallbacks(this) {
					public void onlineSuccessCallback(String results) {
						if(results != null) {
							VideosData videodata = new VideosData();
							List videos = videodata.getVideosListingOnline(results);
							RequestContext requestContext = new RequestContext();
							requestContext.setMessageString("Video successfully saved");
							requestContext.getArgs().put("listing", videos);
							getServlet().redirectTo(new Videos(requestContext ));						
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
						getServlet().redirectTo(new Videos(requestContext));	
					}
					
					public void offlineSuccessCallback(Object results) {
						if((Boolean)results) {
							VideosData videodata = new VideosData();
							List videos = videodata.getVideosListingOffline();
							RequestContext requestContext = new RequestContext();
							requestContext.setMessageString("Video successfully saved");
							requestContext.getArgs().put("listing", videos);
							getServlet().redirectTo(new Videos(requestContext ));
						} else {
							RequestContext requestContext = new RequestContext();
							requestContext.setMessageString("Invalid data, please try again");
							getServlet().redirectTo(new Videos(requestContext));				
						}
						
					}
				}, form, this.requestContext.getQueryString());
				
				videoData.apply(videoData.postPageData());

			}
			else{
				HashMap queryArgs = (HashMap)this.requestContext.getArgs();
				String queryArg = (String)queryArgs.get("action");
				if(queryArg == "list"){
					VideosData videoData = new VideosData(new OnlineOfflineCallbacks(this) {
						public void onlineSuccessCallback(String results) {
							if(results != null) {
								VideosData videodata = new VideosData();
								List videos = videodata.getVideosListingOnline(results);
								RequestContext requestContext = new RequestContext();
								requestContext.getArgs().put("listing", videos);
								getServlet().fillTemplate(new VideosTemplate(requestContext));						
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
							getServlet().redirectTo(new Videos(requestContext));	
						}
						
						public void offlineSuccessCallback(Object results) {
							if((Boolean)results) {
								VideosData videodata = new VideosData();
								List videos = videodata.getVideosListingOffline();
								RequestContext requestContext = new RequestContext();
								requestContext.getArgs().put("listing", videos);
								getServlet().fillTemplate(new VideosTemplate(requestContext));
							} else {
								RequestContext requestContext = new RequestContext();
								requestContext.setMessageString("Local Database error");
								getServlet().redirectTo(new Videos(requestContext));				
							}	
						}
					});
					videoData.apply(videoData.getListPageData());	
				}
				else if(queryArg == "add"){
					VideosData videoData = new VideosData(new OnlineOfflineCallbacks(this) {
						public void onlineSuccessCallback(String addData) {
							if(addData != null) {
								RequestContext requestContext = new RequestContext();
								requestContext.getArgs().put("action", "add");
								requestContext.getArgs().put("addPageData", addData);
								getServlet().fillTemplate(new VideosTemplate(requestContext));
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
							getServlet().redirectTo(new Videos(requestContext));	
						}
						
						public void offlineSuccessCallback(Object addData) {
							if((String)addData != null) {
								RequestContext requestContext = new RequestContext();
								requestContext.getArgs().put("action", "add");
								requestContext.getArgs().put("addPageData", (String)addData);
								getServlet().fillTemplate(new VideosTemplate(requestContext));
							} else {
								RequestContext requestContext = new RequestContext();
								requestContext.setMessageString("Local Database error");
								getServlet().redirectTo(new Videos(requestContext));				
							}	
						}
					});
					videoData.apply(videoData.getAddPageData());	
				} else {
					this.fillTemplate(new VideosTemplate(this.requestContext));
				}
			}
		}
	}
}
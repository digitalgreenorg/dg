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
				Form form = this.requestContext.getForm();
				VideosData videoData = new VideosData(new OnlineOfflineCallbacks(this) {
					public void onlineSuccessCallback(String results) {
						if(this.getStatusCode() == 200) {
							VideosData videodata = new VideosData();
							List videos = videodata.getListingOnline(results);
							RequestContext requestContext = new RequestContext();
							requestContext.setMessage("Video successfully saved");
							requestContext.getArgs().put("listing", videos);
							getServlet().redirectTo(new Videos(requestContext ));						
						} else {
							getServlet().getRequestContext().setMethodTypeCtx(RequestContext.METHOD_GET);
							getServlet().getRequestContext().getArgs().put("action", "add");
							getServlet().getRequestContext().setErrorMessage(results);
							getServlet().redirectTo(new Videos(getServlet().getRequestContext()));			
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
						getServlet().redirectTo(new Videos(requestContext));	
					}
					
					public void offlineSuccessCallback(Object results) {
						if((Boolean)results) {
							VideosData videodata = new VideosData();
							List videos = videodata.getVideosListingOffline();
							RequestContext requestContext = new RequestContext();
							requestContext.setMessage("Video successfully saved");
							requestContext.getArgs().put("listing", videos);
							getServlet().redirectTo(new Videos(requestContext ));
						} else {
							// It's no longer a POST because there was an error, so start again.
							getServlet().getRequestContext().setMethodTypeCtx(RequestContext.METHOD_GET);
							getServlet().getRequestContext().getArgs().put("action", "add");
							getServlet().getRequestContext().setErrorMessage(getServlet().getRequestContext().getForm().printFormErrors());
							getServlet().redirectTo(new Videos(getServlet().getRequestContext()));
						}
						
					}
				}, form);
				
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
								List videos = videodata.getListingOnline(results);
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
								requestContext.setMessage("Unresponsive Server.  Please contact support.");
							else if (errorCode == BaseData.ERROR_SERVER)
								requestContext.setMessage("Problem in the connection with the server.");
							else
								requestContext.setMessage("Unknown error.  Please contact support.");
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
								requestContext.setMessage("Local Database error");
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
								requestContext.setMessage("Unresponsive Server.  Please contact support.");
							else if (errorCode == BaseData.ERROR_SERVER)
								requestContext.setMessage("Problem in the connection with the server.");
							else
								requestContext.setMessage("Unknown error.  Please contact support.");
							getServlet().redirectTo(new Videos(requestContext));	
						}
						
						public void offlineSuccessCallback(Object addData) {
							if((String)addData != null) {
								// Got whatever info we need to display for this GET request, so go ahead
								// and display it by filling in the template.  No need to redirect.
								getServlet().getRequestContext().getArgs().put("addPageData", (String)addData);
								getServlet().fillTemplate(new VideosTemplate(getServlet().getRequestContext()));
							} else {
								RequestContext requestContext = new RequestContext();
								requestContext.setMessage("Local Database error");
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
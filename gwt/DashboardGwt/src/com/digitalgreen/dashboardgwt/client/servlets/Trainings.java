package com.digitalgreen.dashboardgwt.client.servlets;

import java.util.HashMap;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.BaseData;
import com.digitalgreen.dashboardgwt.client.data.TrainingsData;
import com.digitalgreen.dashboardgwt.client.templates.TrainingTemplate;
import com.google.gwt.user.client.Window;

public class Trainings extends BaseServlet{
	
	public Trainings() {
		super();
	}
	
	public Trainings(RequestContext requestContext) {
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
				TrainingsData trainingData = new TrainingsData(new OnlineOfflineCallbacks(this) {
					public void onlineSuccessCallback(String results) {
						if(results != null) {
							TrainingsData trainingData = new TrainingsData();
							List trainings = trainingData.getListingOnline(results);
							RequestContext requestContext = new RequestContext();
							requestContext.setMessageString("Training successfully saved");
							requestContext.getArgs().put("listing", trainings);
							getServlet().redirectTo(new Trainings(requestContext));
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
						getServlet().redirectTo(new Trainings(requestContext));	
					}

					public void offlineSuccessCallback(Object results) {
						if((Boolean)results) {
							TrainingsData trainingData = new TrainingsData();
							List trainings = trainingData.getTrainingsListingsOffline();
							RequestContext requestContext = new RequestContext();
							requestContext.setMessageString("Training successfully saved");
							requestContext.getArgs().put("listing", trainings);
							getServlet().redirectTo(new Trainings(requestContext));
						} else {
							// It's no longer a POST because there was an error, so start again.
							getServlet().getRequestContext().setMethodTypeCtx(RequestContext.METHOD_GET);
							getServlet().getRequestContext().getArgs().put("action", "add");		
							getServlet().redirectTo(new Trainings(getServlet().getRequestContext()));				
						}
					}
				}, form);
				
				trainingData.apply(trainingData.postPageData());
			}
			else {
				HashMap queryArgs = (HashMap)this.requestContext.getArgs();
				String queryArg = (String)queryArgs.get("action");
				if(queryArg.equals("list")){
					TrainingsData trainingData = new TrainingsData(new OnlineOfflineCallbacks(this) {
						public void onlineSuccessCallback(String results) {
							if(results != null) {
								TrainingsData trainingData = new TrainingsData();
								List trainings = trainingData.getListingOnline(results);
								RequestContext requestContext = new RequestContext();
								requestContext.getArgs().put("listing", trainings);
								getServlet().redirectTo(new Trainings(requestContext));						
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
							getServlet().redirectTo(new Trainings(requestContext));	
						}
						
						public void offlineSuccessCallback(Object results) {
							if((Boolean)results) {
								TrainingsData trainingData = new TrainingsData();
								List trainings = trainingData.getTrainingsListingsOffline();
								RequestContext requestContext = new RequestContext();
								requestContext.getArgs().put("listing", trainings);
								getServlet().redirectTo(new Trainings(requestContext));
							} else {
								RequestContext requestContext = new RequestContext();
								requestContext.setMessageString("Local Database error");
								getServlet().redirectTo(new Trainings(requestContext));				
							}	
						}
					});
					trainingData.apply(trainingData.getListPageData());
				}
				else if(queryArg == "add"){
					TrainingsData trainingData = new TrainingsData(new OnlineOfflineCallbacks(this) {
						public void onlineSuccessCallback(String addData) {
							if(addData != null) {
								RequestContext requestContext = new RequestContext();
								requestContext.getArgs().put("action", "add");
								requestContext.getArgs().put("addPageData", addData);
								getServlet().fillTemplate(new TrainingTemplate(requestContext));
							} else {
								// Must be some internal error, or no data to fetch?
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
							getServlet().redirectTo(new Trainings(requestContext));	
						}
						
						public void offlineSuccessCallback(Object addData) {
							if((String)addData != null) {
								// Got whatever info we need to display for this GET request, so go ahead
								// and display it by filling in the template.  No need to redirect.
								getServlet().getRequestContext().getArgs().put("addPageData", (String)addData);
								getServlet().fillTemplate(new TrainingTemplate(getServlet().getRequestContext()));
							} else {
								RequestContext requestContext = new RequestContext();
								requestContext.setMessageString("Local Database error");
								getServlet().redirectTo(new Trainings(requestContext));				
							}	
						}
					});
					trainingData.apply(trainingData.getAddPageData());	
				}
				else {
					this.fillTemplate(new TrainingTemplate(this.requestContext));
				}
			}
		}
	}
}
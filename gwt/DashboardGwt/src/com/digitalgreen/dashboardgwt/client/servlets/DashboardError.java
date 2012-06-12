package com.digitalgreen.dashboardgwt.client.servlets;

import java.util.HashMap;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.BaseData;
import com.digitalgreen.dashboardgwt.client.data.DashboardErrorData;
import com.digitalgreen.dashboardgwt.client.templates.DashboardErrorTemplate;

public class DashboardError extends BaseServlet {
	
	public DashboardError() {
		super();
	}
	
	public DashboardError(RequestContext requestContext) {
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
				HashMap queryArgs = (HashMap)this.requestContext.getArgs();
				String pageNum = (String)queryArgs.get("pageNum");
				Form form = this.requestContext.getForm();
				DashboardErrorData DashboardErrorData = new DashboardErrorData(new OnlineOfflineCallbacks(this) {
					public void onlineSuccessCallback(String results) {
						if(this.getStatusCode() == 200) {
							RequestContext requestContext = new RequestContext();
							requestContext.setMessage("Some errors were marked as 'Not an error'");
							requestContext.getArgs().put("action", "add");
							requestContext.getArgs().put("pageNum", "1");
							getServlet().redirectTo(new DashboardError(requestContext));
						} else {
							getServlet().getRequestContext().setMethodTypeCtx(RequestContext.METHOD_GET);
							getServlet().getRequestContext().setErrorMessage(results) ;
							getServlet().redirectTo(new DashboardError(getServlet().getRequestContext()));	
						}
					}
					
					public void onlineErrorCallback(int errorCode) {
						getServlet().getRequestContext().setMethodTypeCtx(RequestContext.METHOD_GET);
						if (errorCode == BaseData.ERROR_RESPONSE)
							getServlet().getRequestContext().setErrorMessage("You may be experiencing server/bandwidth problems.  Please try again, or contact support.");
						else if (errorCode == BaseData.ERROR_SERVER)
							getServlet().getRequestContext().setErrorMessage("Problem in the connection with the server.");
						else
							getServlet().getRequestContext().setErrorMessage("Unknown error.  Please contact support.");
						getServlet().redirectTo(new DashboardError(getServlet().getRequestContext()));	
					}
					
					public void offlineSuccessCallback(Object results) {
						RequestContext requestContext = new RequestContext();
						requestContext.setErrorMessage("Dashboard Errors are not visible in offline mode. Please Go Online from Main Page.");
						getServlet().redirectTo(new Index(requestContext));
					}
				}, form);
				DashboardErrorData.apply(DashboardErrorData.postPageData(pageNum));
			}
			else {
				HashMap queryArgs = (HashMap)this.requestContext.getArgs();
				String queryArg = (String)queryArgs.get("action");
				String pageNum = (String)queryArgs.get("pageNum");
				if(queryArg.equals("add")){
					DashboardErrorData dashboardErrorData = new DashboardErrorData(new OnlineOfflineCallbacks(this) {
						public void onlineSuccessCallback(String results) {
							String count = this.getResponse().getHeader("X-COUNT");
							getServlet().getRequestContext().getArgs().put("totalRows", count);
							if(this.getStatusCode() == 200) {
								DashboardErrorData dashboardErrorData = new DashboardErrorData();
								if(!results.equals("EOF")){
									List dashboardError = dashboardErrorData.getListingOnline(results);
									getServlet().getRequestContext().getArgs().put("listing", dashboardError);
								}
								getServlet().fillTemplate(new DashboardErrorTemplate(getServlet().getRequestContext()));					
							} else {
								RequestContext requestContext = new RequestContext();
								requestContext.setErrorMessage("Unexpected error occured in retriving data. Please contact support");
								getServlet().redirectTo(new Index(requestContext));
							}
						}

						public void onlineErrorCallback(int errorCode) {
							RequestContext requestContext = new RequestContext();
							if (errorCode == BaseData.ERROR_RESPONSE)
								requestContext.setErrorMessage("You may be experiencing server/bandwidth problems.  Please try again, or contact support.");
							else if (errorCode == BaseData.ERROR_SERVER)
								requestContext.setErrorMessage("Problem in the connection with the server.");
							else
								requestContext.setErrorMessage("Unknown error.  Please contact support.");
							getServlet().redirectTo(new Index(requestContext));
						}
						
						public void offlineSuccessCallback(Object addData) {
							RequestContext requestContext = new RequestContext();
							requestContext.setErrorMessage("Dashboard Errors are not visible in offline mode. Please Go Online.");
							getServlet().redirectTo(new Index(requestContext));
						}
					});
					dashboardErrorData.apply(dashboardErrorData.getListPageData(pageNum));
				}
			}
		}
	}
}
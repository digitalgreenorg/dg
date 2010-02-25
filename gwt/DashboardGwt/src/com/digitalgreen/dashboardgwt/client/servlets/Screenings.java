package com.digitalgreen.dashboardgwt.client.servlets;

import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.ScreeningsData;
import com.digitalgreen.dashboardgwt.client.templates.ScreeningsTemplate;

public class Screenings extends BaseServlet {
	public Screenings() {
		super();
	}
	
	public Screenings(RequestContext requestContext) {
		super(requestContext);
	}
	
	@Override
	public void response() {
		super.response();
		
		if (!this.isLoggedIn()) {
			super.redirectTo(new Login());
		} else {
			if(this.requestContext.getMethodTypeCtx() == RequestContext.METHOD_POST) {
				// We need to support new form creates and edits in here.
				
			} else if(this.requestContext.getMethodTypeCtx() == RequestContext.METHOD_GET) {
				
				String action = (String)this.requestContext.getArgs().get("action");
				if(action == "add") {
					ScreeningsData screeningData = new ScreeningsData(new OnlineOfflineCallbacks(this) {
						public void onlineSuccessCallback(String results) {
							BaseServlet servlet = getServlet();
							// Do something with the results coming back from the main server.  It's in
							// JSON so need to think about how to deal with this in the servlet layer.  I
							// don't like it but I can't help it because Java doesn't support function
							// pointers AFAIK (maybe through some interface stuff but unneccessary).
							servlet.fillTemplate(new ScreeningsTemplate(servlet.requestContext));
						}
					
						public void offlineSuccessCallback(Object results) {
							BaseServlet servlet = getServlet();
							// Do something with the results that most likely need to get set
							// back into the requestContext so the add page can display them.
							
							servlet.fillTemplate(new ScreeningsTemplate(servlet.requestContext));
						}
				
					});
					screeningData.apply(screeningData.getAddPageData());
				} else {
					// Assume we're getting the screening list page in a GET request.
					ScreeningsData screeningData = new ScreeningsData(new OnlineOfflineCallbacks(this) {
						public void onlineSuccessCallback(String results) {
							BaseServlet servlet = getServlet();
							servlet.fillTemplate(new ScreeningsTemplate(servlet.requestContext));
						}
					
						public void offlineSuccessCallback(Object results) {
							BaseServlet servlet = getServlet();
							// Do something with the results that most likely need to get set
							// back into the requestContext so the add page can display them.
							
							servlet.fillTemplate(new ScreeningsTemplate(servlet.requestContext));
						}
				
					});
					screeningData.apply(screeningData.getListPageData());
				}
			}
		}
	}
}
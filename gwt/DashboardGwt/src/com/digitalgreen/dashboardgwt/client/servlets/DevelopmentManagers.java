package com.digitalgreen.dashboardgwt.client.servlets;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.templates.DevelopmentManagersTemplate;

public class DevelopmentManagers extends BaseServlet {
	public  DevelopmentManagers(){
		super();
	}
	
	public DevelopmentManagers(RequestContext requestContext) {
		super(requestContext);
	}
	
	@Override
	public void response() {
		super.response();
		
		if (!this.isLoggedIn()) {
			super.redirectTo(new Login());
		} else {
			this.fillTemplate(new DevelopmentManagersTemplate(this.requestContext));
		}
	}
}
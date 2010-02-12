package com.digitalgreen.dashboardgwt.client.servlets;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.templates.RegionsTemplate;

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
			this.fillTemplate(new RegionsTemplate(this.requestContext));
		}
	}
}
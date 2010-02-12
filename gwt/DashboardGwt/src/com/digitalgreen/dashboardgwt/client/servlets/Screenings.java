package com.digitalgreen.dashboardgwt.client.servlets;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;
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
		
		this.fillTemplate(new ScreeningsTemplate(this.requestContext));
		/*
		if (!this.isLoggedIn()) {
			super.redirectTo(new Login());
		} else {
			this.fillTemplate(new ScreeningsTemplate(this.requestContext));
		}
		*/
	}
}
package com.digitalgreen.dashboardgwt.client.servlets;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.templates.TrainingTemplate;

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
			this.fillTemplate(new TrainingTemplate(this.requestContext));
		}
	}

}

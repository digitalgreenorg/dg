package com.digitalgreen.dashboardgwt.client.servlets;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.templates.FieldOfficerTemplate;

public class FieldOfficers extends BaseServlet{

	public FieldOfficers(){
		super();
	}
	
	public FieldOfficers(RequestContext requestContext) {
		super(requestContext);
	}
	
	@Override
	public void response() {
		super.response();
		
		if (!this.isLoggedIn()) {
			super.redirectTo(new Login());
		} else {
			this.fillTemplate(new FieldOfficerTemplate(this.requestContext));
		}
	}
}

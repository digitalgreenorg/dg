package com.digitalgreen.dashboardgwt.client.servlets;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.templates.PersonGroupsTemplate;

public class PersonGroups extends BaseServlet{
	
	public PersonGroups(){
		super();
	}
	
	public PersonGroups(RequestContext requestContext) {
		super(requestContext);
	}
	
	@Override
	public void response() {
		super.response();
		
		if (!this.isLoggedIn()) {
			super.redirectTo(new Login());
		} else {
			this.fillTemplate(new PersonGroupsTemplate(this.requestContext));
		}
	}
}

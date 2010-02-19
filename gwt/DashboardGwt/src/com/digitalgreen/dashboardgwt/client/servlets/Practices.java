package com.digitalgreen.dashboardgwt.client.servlets;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.templates.PracticeTemplate;

public class Practices extends BaseServlet{
	
	public Practices(){
		super();
	}
	
	public Practices(RequestContext requestContext){
		super(requestContext);
	}
	
	@Override
	public void response() {
		super.response();
		
		if (!this.isLoggedIn()) {
			super.redirectTo(new Login());
		} else {
			this.fillTemplate(new PracticeTemplate(this.requestContext));
		}
	}
}

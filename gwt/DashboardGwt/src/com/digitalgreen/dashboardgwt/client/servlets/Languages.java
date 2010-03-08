package com.digitalgreen.dashboardgwt.client.servlets;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.templates.LanguagesTemplate;
import com.google.gwt.user.client.Window;

public class Languages extends BaseServlet{
	
	public Languages() {
		super();
	}
	
	public Languages(RequestContext requestContext) {
		super(requestContext);
	}

	@Override
	public void response() {
		super.response();
		
		if (!this.isLoggedIn()) {
			super.redirectTo(new Login());
		} else {
			this.fillTemplate(new LanguagesTemplate(this.requestContext));
		}
	}
}

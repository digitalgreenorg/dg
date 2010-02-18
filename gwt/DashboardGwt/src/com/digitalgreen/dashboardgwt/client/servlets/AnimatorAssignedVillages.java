package com.digitalgreen.dashboardgwt.client.servlets;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.templates.AnimatorAssignedVillagesTemplate;

public class AnimatorAssignedVillages extends BaseServlet {
	public AnimatorAssignedVillages() {
		super();
	}
	
	public AnimatorAssignedVillages(RequestContext requestContext) {
		super(requestContext);
	}
	
	@Override
	public void response() {
		super.response();
		
		if (!this.isLoggedIn()) {
			super.redirectTo(new Login());
		} else {
			this.fillTemplate(new AnimatorAssignedVillagesTemplate(this.requestContext));
		}
	}
}
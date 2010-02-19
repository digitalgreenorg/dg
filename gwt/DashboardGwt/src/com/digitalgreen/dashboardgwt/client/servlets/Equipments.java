package com.digitalgreen.dashboardgwt.client.servlets;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.templates.EquipmentsTemplate;

public class Equipments extends BaseServlet {
	
	public Equipments(){
		super();
	}
	
	public Equipments(RequestContext requestContext) {
		super(requestContext);
	}

	@Override
	public void response() {
		super.response();
		
		if (!this.isLoggedIn()) {
			super.redirectTo(new Login());
		} else {
			this.fillTemplate(new EquipmentsTemplate(this.requestContext));
		}
	}
}

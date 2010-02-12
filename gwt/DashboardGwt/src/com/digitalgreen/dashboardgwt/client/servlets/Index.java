package com.digitalgreen.dashboardgwt.client.servlets;

import com.digitalgreen.dashboardgwt.client.servlets.BaseServlet;
import com.digitalgreen.dashboardgwt.client.templates.IndexTemplate;

public class Index extends BaseServlet {	
	
	@Override
	public void response () {
		super.response();
		this.fillTemplate(new IndexTemplate(this.requestContext));
		/*
		if (!this.isLoggedIn()) {
			super.redirectTo(new Login());
		} else {
			this.fillTemplate(new IndexTemplate(this.requestContext));
		}
		*/
	}
}
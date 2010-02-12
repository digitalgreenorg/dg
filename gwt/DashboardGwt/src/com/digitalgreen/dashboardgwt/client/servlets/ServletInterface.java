package com.digitalgreen.dashboardgwt.client.servlets;

import com.digitalgreen.dashboardgwt.client.templates.BaseTemplate;

interface ServletInterface {
	public void redirectTo(BaseServlet servlet);
	public void fillTemplate(BaseTemplate template);
}
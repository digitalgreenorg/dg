package com.digitalgreen.dashboardgwt.client.servlets;

import com.digitalgreen.dashboardgwt.client.templates.BaseTemplate;
import com.digitalgreen.dashboardgwt.client.templates.Template;

interface ServletInterface {
	public void redirectTo(BaseServlet servlet);
	public void fillTemplate(Template template);
}
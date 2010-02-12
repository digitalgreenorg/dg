package com.digitalgreen.dashboardgwt.client.templates;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.google.gwt.user.client.ui.HTMLPanel;

public class IndexTemplate extends BaseTemplate {
	
	public IndexTemplate(RequestContext requestContext) {
		super(requestContext);
	}
	
	@Override
	public void fill() {
		HTMLPanel indexHtml = new HTMLPanel(indexContentHtml);
		super.setContentPanel(indexHtml);
		super.fill();
	}
	
	final protected String indexContentHtml = "<h1>Index</h1>";
}
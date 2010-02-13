package com.digitalgreen.dashboardgwt.client.data;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.google.gwt.user.client.ui.FormPanel;

public class RegionsData extends BaseData {
	private FormPanel formData;
	
	public RegionsData(RequestContext requestContext) {
		super();
		this.formData = requestContext.getFormPanelCtx();
	}
}
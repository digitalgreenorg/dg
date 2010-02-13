package com.digitalgreen.dashboardgwt.client.data;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.google.gwt.user.client.ui.FormPanel;

public class ScreeningsData extends BaseData {
	private FormPanel formData;
	
	public ScreeningsData(RequestContext requestContext) {
		super();
		this.formData = requestContext.getFormPanelCtx();
	}
}
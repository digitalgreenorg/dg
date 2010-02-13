package com.digitalgreen.dashboardgwt.client.data;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.google.gwt.user.client.ui.FormPanel;

public class LoginData extends BaseData {
	private FormPanel formData;
	
	public LoginData(RequestContext requestContext) {
		super();
		this.formData = requestContext.getFormPanelCtx();
	}
	
}
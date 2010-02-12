package com.digitalgreen.dashboardgwt.client.data;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.google.gwt.user.client.ui.FormPanel;

public class LoginData extends BaseData {
	
	private static String formAction;
	private FormPanel formData;
	
	public LoginData(RequestContext requestContext) {
		super();
		LoginData.formAction = RequestContext.getServerUrl() + "admin";
		this.formData = requestContext.getFormPanelCtx();
	}
	
	public static String getFormAction() {
		return LoginData.formAction;
	}
}
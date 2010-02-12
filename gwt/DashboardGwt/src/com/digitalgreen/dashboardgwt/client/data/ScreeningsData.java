package com.digitalgreen.dashboardgwt.client.data;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.google.gwt.user.client.ui.FormPanel;

public class ScreeningsData extends BaseData {
	private FormPanel formData;
	private static String formAction;
	
	public ScreeningsData(RequestContext requestContext) {
		super();
		ScreeningsData.formAction = RequestContext.getServerUrl() + "screenings";
		this.formData = requestContext.getFormPanelCtx();
	}
	
	public static String getFormAction() {
		return ScreeningsData.formAction;
	}
}
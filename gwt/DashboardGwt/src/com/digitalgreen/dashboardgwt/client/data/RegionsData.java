package com.digitalgreen.dashboardgwt.client.data;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.google.gwt.user.client.ui.FormPanel;

public class RegionsData extends BaseData {
	private FormPanel formData;
	private static String formAction;
	
	public RegionsData(RequestContext requestContext) {
		super();
		RegionsData.formAction = RequestContext.getServerUrl() + "regions";
		this.formData = requestContext.getFormPanelCtx();
	}
	
	public static String getFormAction() {
		return RegionsData.formAction;
	}
}
package com.digitalgreen.dashboardgwt.client.data;

import com.google.gwt.user.client.ui.FormPanel;

interface OnlineDataInterface {
	public void get(String url);
	public void post(FormPanel postForm);
}

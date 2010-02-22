package com.digitalgreen.dashboardgwt.client.data;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.google.gwt.user.client.ui.FormPanel;

public class LoginData extends BaseData {
	
	public class Data extends BaseData.Data {
		private String username;
		private String password;
		
		public Data(String username, String password) {
			this.username = username;
			this.password = password;
		}
	}

	public LoginData(RequestContext requestContext) {
		super();
	}

	public static boolean authenticate(String username, String password) {
		return false;
	}
}
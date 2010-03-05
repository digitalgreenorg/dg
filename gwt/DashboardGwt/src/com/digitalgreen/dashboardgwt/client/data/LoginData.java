package com.digitalgreen.dashboardgwt.client.data;

import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.google.gwt.gears.client.database.DatabaseException;
import com.google.gwt.gears.client.database.ResultSet;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.FormPanel;

public class LoginData extends BaseData {
	
	public class Data extends BaseData.Data {
		private String username;
		private String password;
		
		public Data() {
		}
		
		public Data(String username, String password) {
			this.username = username;
			this.password = password;
		}
	}

	public LoginData() {
		super();
		this.data = new Data();
	}

	public LoginData(OnlineOfflineCallbacks callbacks) {
		super(callbacks);
	}

	public Object authenticate(String username, String password) {
		
		if(this.isOnline()) {
			this.dataOnlineCallbacks.onlineSuccessCallback("1");
			//String postData = "username=" + username + "&password=" + password;
			//this.post("http://127.0.0.1:8000/dashboard/login/", postData);
		} else {
			// Check if DB User row has the same username.
			String query = "SELECT username FROM User WHERE" +
				"username=?;";
			this.select(query, username);
			ResultSet resultSet = this.getResultSet();
			try {
				if(resultSet != null && resultSet.getFieldAsString(0) == "username") {
					resultSet.close();
					return true;
				}
			} catch (DatabaseException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			try {
				resultSet.close();
			} catch (DatabaseException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
		return false;
	}
}
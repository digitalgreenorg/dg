package com.digitalgreen.dashboardgwt.client.data;

import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.google.gwt.gears.client.database.DatabaseException;
import com.google.gwt.gears.client.database.ResultSet;
import com.google.gwt.user.client.Cookies;
import com.google.gwt.user.client.Window;

public class IndexData extends BaseData {
	
		
	public IndexData(OnlineOfflineCallbacks callbacks) {
		super(callbacks);
	}

	public static void createTables(){
		Schema.createSchema();
	}

	public Object getGlobalPrimaryKey(String username) {
		// Make a call to the Django view and get the primary key
		String postData = "username=" + username;
		Window.alert(postData);
		this.post(RequestContext.SERVER_HOST + ":8000/dashboard/getkey/", postData);
		return true;
	}
}
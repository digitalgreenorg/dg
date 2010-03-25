package com.digitalgreen.dashboardgwt.client.data;

import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.google.gwt.gears.client.database.DatabaseException;
import com.google.gwt.gears.client.database.ResultSet;
import com.google.gwt.user.client.Cookies;
import com.google.gwt.user.client.Window;

public class IndexData extends BaseData {
	
	protected static String postURL = "/dashboard/getkey/";
		
	public IndexData(OnlineOfflineCallbacks callbacks) {
		super(callbacks);
	}

	public static void createTables(){
		Schema.createSchema();
	}

	public Object getGlobalPrimaryKey(String username) {
		// Make a call to the Django view and get the primary key
		String postData = "username=" + username;
		//Window.alert(postData);
		this.post(RequestContext.SERVER_HOST + this.postURL, postData);
		return true;
	}
	
	public Boolean checkIfUserEntryExistsInTable(String username){
			BaseData.dbOpen();
			this.select(LoginData.selectUser , username);
			ResultSet resultSet = this.getResultSet();
			if(resultSet.isValidRow()) {		
				LoginData.dbClose();
				return true;
			}
			else{
				LoginData.dbClose();
				return false;
			}
	}
}
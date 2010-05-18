package com.digitalgreen.dashboardgwt.client.data;

import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.google.gwt.gears.client.database.DatabaseException;
import com.google.gwt.gears.client.database.ResultSet;
import com.google.gwt.user.client.Cookies;
import com.google.gwt.user.client.Window;

public class IndexData extends BaseData {
	
	protected static String postURL = "/dashboard/getkey/";
	public final static int STATUS_READY = 0;
	public final static int STATUS_DB_NOT_OPEN = 1;
	public final static int STATUS_SCHEMA_NOT_READY = 2;
	
	public IndexData(OnlineOfflineCallbacks callbacks) {
		super(callbacks);
	}

	public IndexData() {
		super();
	}

	public static void createTables(){
		Schema.createSchema();
	}

	public Object getGlobalPrimaryKey(String username) {
		// Make a call to the Django view and get the primary key
		String postData = "username=" + username;
		this.post(RequestContext.SERVER_HOST + this.postURL, postData);
		return true;
	}
	
	public int checkIfOfflineReady(String username){
			if(!BaseData.dbOpen()) {
				return IndexData.STATUS_DB_NOT_OPEN;
			}
			this.select(LoginData.selectUser , username);
			ResultSet resultSet = this.getResultSet();
			if(this.isValidResultSet()) {		
				BaseData.dbClose();
				return IndexData.STATUS_READY;
			}
			else{
				BaseData.dbClose();
				return IndexData.STATUS_SCHEMA_NOT_READY;
			}
	}
}
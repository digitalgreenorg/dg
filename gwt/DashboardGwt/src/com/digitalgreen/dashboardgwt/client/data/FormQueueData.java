package com.digitalgreen.dashboardgwt.client.data;

import java.util.HashMap;

import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.google.gwt.gears.client.database.DatabaseException;
import com.google.gwt.user.client.Window;

public class FormQueueData extends BaseData {

	protected static String createTable = "CREATE TABLE IF NOT EXISTS `formqueue` " +
										  "(table_id INTEGER NOT NULL, " +
										  "global_pk_id INTEGER NOT NULL PRIMARY KEY, " +
										  "querystring VARCHAR NOT NULL, " +
										  "sync_status BOOLEAN, " +
										  "action CHAR(1)); ";  
	
	protected static String saveQueryString = "INSERT INTO `formqueue` VALUES (? , ? , ? , ? , ?);";
	
	protected static String getUnsyncTableRow = "SELECT * FROM `formqueue` WHERE sync_status=0 LIMIT 1";
	
	protected static String updateSyncStatusOfARow = "UPDATE `formqueue` SET sync_status=1 WHERE global_pk_id=?";
	
	public FormQueueData() {
		super();
	}
	

	public FormQueueData(OnlineOfflineCallbacks callbacks) {
		super(callbacks);
	}
	
	public void saveQueryString(String ...args){
		this.insert(saveQueryString, args);
	}
	
	public Object postPageData() {	
		return false;
	}
	
	
}
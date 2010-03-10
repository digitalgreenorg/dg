package com.digitalgreen.dashboardgwt.client.data;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;

public class FormsData extends BaseData {

	//protected static String TableData = "CREATE TABLE IF NOT EXISTS `table`(table_id INTEGER PRIMARY KEY, table_name VARCHAR NOT NULL );";
	
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `formqueue` " +
										  "(table_id INTEGER NOT NULL, " +
										  "global_pk_id INTEGER NOT NULL PRIMARY KEY, " +
										  "querystring VARCHAR NOT NULL, " +
										  "sync_status BOOLEAN, " +
										  "action CHAR(1)); ";  
	
	//protected static String insertIntoTable = "INSERT INTO `table` (table_name) VALUES ('screening');"
	
	
	public FormsData(RequestContext requestContext) {
		super();
	}
}
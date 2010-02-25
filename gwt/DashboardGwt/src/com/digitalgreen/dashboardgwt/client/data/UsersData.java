package com.digitalgreen.dashboardgwt.client.data;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;

public class UsersData extends BaseData {

	protected static String createTable = "CREATE TABLE IF NOT EXISTS `user` " +
										  "(last_inserted_id INTEGER PRIMARY KEY NOT NULL, " +
										  "username VARCHAR(100), password VARCHAR(100));";  
	
	
	public UsersData(RequestContext requestContext) {
		super();
	}
}
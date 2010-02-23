package com.digitalgreen.dashboardgwt.client.data;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;

public class StatesData extends BaseData {

	final protected static String createTable = "CREATE TABLE IF NOT EXISTS `state` " +
												"(id INTEGER PRIMARY KEY  NOT NULL ," +
												"STATE_NAME VARCHAR(100)  NOT NULL ," +
												"region_id INT  NOT NULL DEFAULT 0," +
												"START_DATE DATE  NULL DEFAULT NULL, " +
												"FOREIGN KEY(region_id) references region(id));"; 
	
	public StatesData(RequestContext requestContext) {
		super();
	}
}
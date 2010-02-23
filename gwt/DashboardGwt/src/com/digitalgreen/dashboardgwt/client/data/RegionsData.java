package com.digitalgreen.dashboardgwt.client.data;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;

public class RegionsData extends BaseData {

	final protected static String createTable = "CREATE TABLE IF NOT EXISTS `region` " +
												"(id INTEGER PRIMARY KEY NOT NULL ," +
												"REGION_NAME VARCHAR(100) NOT NULL ," +
												"START_DATE DATE NULL DEFAULT NULL);";  
	
	public RegionsData(RequestContext requestContext) {
		super();
	}
}
package com.digitalgreen.dashboardgwt.client.data;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;

public class PracticesData extends BaseData {

	protected static String CREATE_TABLE = "CREATE TABLE IF NOT EXISTS `practices` (id INTEGER PRIMARY KEY  NOT NULL ,PRACTICE_NAME VARCHAR(200)  NOT NULL ,SEASONALITY VARCHAR(3)  NOT NULL ,SUMMARY TEXT NULL DEFAULT NULL );";  
	
	public PracticesData(RequestContext requestContext) {
		super();
	}
}
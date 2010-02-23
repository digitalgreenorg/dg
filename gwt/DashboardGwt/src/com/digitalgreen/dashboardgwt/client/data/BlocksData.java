package com.digitalgreen.dashboardgwt.client.data;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;

public class BlocksData extends BaseData {

	final protected static String createTable = "CREATE TABLE IF NOT EXISTS `block` " +
												"(id INTEGER PRIMARY KEY  NOT NULL ," +
												"BLOCK_NAME VARCHAR(100)  NOT NULL ," +
												"START_DATE DATE  NULL DEFAULT NULL," +
												"district_id INT  NOT NULL DEFAULT 0, " +
												"FOREIGN KEY(district_id) REFERENCES district(id));";
	
	public BlocksData(RequestContext requestContext) {
		super();
	}
}
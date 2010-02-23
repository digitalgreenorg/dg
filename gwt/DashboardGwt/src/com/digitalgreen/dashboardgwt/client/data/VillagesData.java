package com.digitalgreen.dashboardgwt.client.data;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;

public class VillagesData extends BaseData {

	final protected static String createTable = "CREATE TABLE IF NOT EXISTS `village` " +
												"(id INTEGER PRIMARY KEY  NOT NULL ," +
												"VILLAGE_NAME VARCHAR(100)  NOT NULL ," +
												"block_id INT  NOT NULL DEFAULT 0," +
												"NO_OF_HOUSEHOLDS INT  NULL DEFAULT NULL," +
												"POPULATION INT  NULL DEFAULT NULL," +
												"ROAD_CONNECTIVITY VARCHAR(100)  NOT NULL ," +
												"CONTROL SMALLINT  NULL DEFAULT NULL," +
												"START_DATE DATE  NULL DEFAULT NULL, " +
												"FOREIGN KEY(block_id) REFERENCES block(id)); ";  
	
	public VillagesData(RequestContext requestContext) {
		super();
	}
}
package com.digitalgreen.dashboardgwt.client.data;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;

public class VillagesData extends BaseData {

	protected static String tableID = "10";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `village` " +
												"(id INTEGER PRIMARY KEY  NOT NULL ," +
												"VILLAGE_NAME VARCHAR(100)  NOT NULL ," +
												"block_id INT  NOT NULL DEFAULT 0," +
												"NO_OF_HOUSEHOLDS INT  NULL DEFAULT NULL," +
												"POPULATION INT  NULL DEFAULT NULL," +
												"ROAD_CONNECTIVITY VARCHAR(100)  NOT NULL ," +
												"CONTROL SMALLINT  NULL DEFAULT NULL," +
												"START_DATE DATE  NULL DEFAULT NULL, " +
												"FOREIGN KEY(block_id) REFERENCES block(id)); ";  
	
	protected static String saveVillageOfflineURL = "/dashboard/savevillageoffline/";
	
	public VillagesData() {
		super();
	}
	
	@Override
	protected String getTableId() {
		return VillagesData.tableID;
	}
}
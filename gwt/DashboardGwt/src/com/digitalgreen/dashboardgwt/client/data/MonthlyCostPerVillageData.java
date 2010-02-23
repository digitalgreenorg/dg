package com.digitalgreen.dashboardgwt.client.data;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;

public class MonthlyCostPerVillageData extends BaseData {
	
	final protected static String createTable = "CREATE TABLE IF NOT EXISTS `monthly_cost_per_village` " +
												"(id INTEGER PRIMARY KEY  NOT NULL ," +
												"village_id INT  NOT NULL DEFAULT 0," +
												"DATE DATE  NOT NULL ," +
												"LABOR_COST FLOAT(0,0)  NULL DEFAULT NULL," +
												"EQUIPMENT_COST FLOAT(0,0)  NULL DEFAULT NULL," +
												"TRANSPORTATION_COST FLOAT(0,0)  NULL DEFAULT NULL," +
												"MISCELLANEOUS_COST FLOAT(0,0)  NULL DEFAULT NULL," +
												"TOTAL_COST FLOAT(0,0)  NULL DEFAULT NULL," +
												"PARTNERS_COST FLOAT(0,0)  NULL DEFAULT NULL," +
												"DIGITALGREEN_COST FLOAT(0,0)  NULL DEFAULT NULL," +
												"COMMUNITY_COST FLOAT(0,0)  NULL DEFAULT NULL, " +
												"FOREIGN KEY(village_id) REFERENCES village(id));";
	
	public MonthlyCostPerVillageData(RequestContext requestContext){
		super();
	}
}

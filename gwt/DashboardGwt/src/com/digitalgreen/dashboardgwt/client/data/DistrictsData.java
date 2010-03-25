package com.digitalgreen.dashboardgwt.client.data;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;

public class DistrictsData extends BaseData {

	protected static String tableID = "8";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `district` " +
												"(id INTEGER PRIMARY KEY  NOT NULL ," +
												"DISTRICT_NAME VARCHAR(100)  NOT NULL ," +
												"START_DATE DATE  NULL DEFAULT NULL," +
												"state_id INT  NOT NULL DEFAULT 0," +
												"fieldofficer_id INT  NOT NULL DEFAULT 0," +
												"FIELDOFFICER_STARTDAY DATE  NULL DEFAULT NULL," +
												"partner_id INT  NOT NULL DEFAULT 0, " +
												"FOREIGN KEY(state_id) REFERENCES state(id), " +
												"FOREIGN KEY(fieldofficer_id) REFERENCES field_officer(id), " +
												"FOREIGN KEY(partner_id) REFERENCES partners(id));";  
	
	protected static String saveDistrictOfflineURL = "/dashboard/savedistrictoffline/";
	
	public DistrictsData() {
		super();
	}
	
	@Override
	protected String getTableId() {
		return DistrictsData.tableID;
	}
}
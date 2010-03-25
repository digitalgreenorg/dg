package com.digitalgreen.dashboardgwt.client.data;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;

public class DevelopmentManagersData extends BaseData {

	protected static String tableID = "4";
	protected static String createTable = "CREATE TABLE  IF NOT EXISTS `development_manager` " +
												"(id INTEGER PRIMARY KEY  NOT NULL ," +
												"NAME VARCHAR(100)  NOT NULL ," +
												"AGE INT  NULL DEFAULT NULL," +
												"GENDER VARCHAR(1)  NOT NULL ," +
												"HIRE_DATE DATE  NULL DEFAULT NULL," +
												"PHONE_NO VARCHAR(100)  NOT NULL, " +
												"ADDRESS VARCHAR(500)  NOT NULL ," +
												"SPECIALITY TEXT  NOT NULL ," +
												"region_id INT  NOT NULL DEFAULT 0," +
												"START_DAY DATE  NULL DEFAULT NULL," +
												"equipmentholder_id INT  NULL DEFAULT NULL," +
												"SALARY FLOAT(0,0)  NULL DEFAULT NULL, " +
												"FOREIGN KEY(region_id) REFERENCES region(id), " +
												"FOREIGN KEY(equipmentholder_id) REFERENCES equipment_holder(id));";
	
	protected static String saveDevelopmentManagerOfflineURL = "/dashboard/savedevelopmentmanageroffline/";

	public DevelopmentManagersData() {
		super();
	}

	@Override
	protected String getTableId() {
		return DevelopmentManagersData.tableID;
	}
}
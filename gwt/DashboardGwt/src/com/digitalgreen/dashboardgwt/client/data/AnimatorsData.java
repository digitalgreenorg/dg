package com.digitalgreen.dashboardgwt.client.data;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;

public class AnimatorsData extends BaseData {

	protected static String tableID = "15";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `animator` " +
												"(id INTEGER PRIMARY KEY  NOT NULL ," +
												"NAME VARCHAR(100)  NOT NULL ," +
												"AGE INT  NULL DEFAULT NULL," +
												"GENDER VARCHAR(1)  NOT NULL ," +
												"CSP_FLAG SMALLINT  NULL DEFAULT NULL," +
												"CAMERA_OPERATOR_FLAG SMALLINT  NULL DEFAULT NULL," +
												"FACILITATOR_FLAG SMALLINT  NULL DEFAULT NULL," +
												"PHONE_NO VARCHAR(100)  NOT NULL ," +
												"ADDRESS VARCHAR(500)  NOT NULL ," +
												"partner_id INT  NOT NULL DEFAULT 0," +
												"home_village_id INT  NOT NULL DEFAULT 0," +
												"equipmentholder_id INT  NULL DEFAULT NULL, " +
												"FOREIGN KEY(partner_id) REFERENCES partners(id), " +
												"FOREIGN KEY(home_village_id) REFERENCES village(id), " +
												"FOREIGN KEY(equipmentholder_id) REFERENCES equipment_holder(id) );";
	
	protected static String saveAnimatorOfflineURL = "/dashboard/saveanimatoroffline/";
	
	public AnimatorsData() {
		super();
	}
	
	@Override
	protected String getTableId() {
		return AnimatorsData.tableID;
	}
}
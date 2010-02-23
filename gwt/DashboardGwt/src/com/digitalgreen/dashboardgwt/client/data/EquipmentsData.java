package com.digitalgreen.dashboardgwt.client.data;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;

public class EquipmentsData extends BaseData {

	final protected static String createTable = "CREATE TABLE IF NOT EXISTS `equipment_id` " +
												"(id INTEGER PRIMARY KEY  NOT NULL ," +
												"EQUIPMENT_TYPE VARCHAR(300)  NOT NULL ," +
												"MODEL_NO VARCHAR(300)  NOT NULL ," +
												"SERIAL_NO VARCHAR(300)  NOT NULL ," +
												"COST FLOAT(0,0)  NULL DEFAULT NULL," +
												"PROCUREMENT_DATE DATE NULL DEFAULT NULL," +
												"WARRANTY_EXPIRATION_DATE DATE  NULL DEFAULT NULL," +
												"equipmentholder_id INT  NULL DEFAULT NULL, " +
												"FOREIGN KEY(equipmentholder_id) REFERENCES equipment_holder(id));";  
	
	public EquipmentsData(RequestContext requestContext) {
		super();
	}
}
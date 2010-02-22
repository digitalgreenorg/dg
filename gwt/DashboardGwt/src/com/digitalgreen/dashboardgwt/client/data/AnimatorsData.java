package com.digitalgreen.dashboardgwt.client.data;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;

public class AnimatorsData extends BaseData {

	protected static String CREATE_TABLE = "CREATE TABLE IF NOT EXISTS `animator` (id INTEGER PRIMARY KEY  NOT NULL ,NAME VARCHAR(100)  NOT NULL ,AGE INT  NULL DEFAULT NULL,GENDER VARCHAR(1)  NOT NULL ,CSP_FLAG SMALLINT  NULL DEFAULT NULL,CAMERA_OPERATOR_FLAG SMALLINT  NULL DEFAULT NULL,FACILITATOR_FLAG SMALLINT  NULL DEFAULT NULL,PHONE_NO VARCHAR(100)  NOT NULL ,ADDRESS VARCHAR(500)  NOT NULL ,partner_id INT  NOT NULL DEFAULT 0,home_village_id INT  NOT NULL DEFAULT 0,equipmentholder_id INT  NULL DEFAULT NULL, FOREIGN KEY(partner_id) REFERENCES partners(id), FOREIGN KEY(home_village_id) REFERENCES village(id), FOREIGN KEY(equipmentholder_id) REFERENCES equipment_holder(id) );"+
	"CREATE TABLE IF NOT EXISTS `animator_assigned_village` (id INTEGER PRIMARY KEY NOT NULL ,animator_id INT  NOT NULL DEFAULT 0,village_id INT  NOT NULL DEFAULT 0,START_DATE DATE  NULL DEFAULT NULL, FOREIGN KEY(animator_id) REFERENCES animator(id), FOREIGN KEY(village_id) REFERENCES village(id));" +
	"CREATE TABLE IF NOT EXISTS `animator_salary_per_month` (id INTEGER PRIMARY KEY NOT NULL ,animator_id INT  NOT NULL DEFAULT 0,DATE DATE  NOT NULL ,TOTAL_SALARY FLOAT(0,0)  NULL DEFAULT NULL,PAY_DATE DATE  NULL DEFAULT NULL, FOREIGN KEY(animator_id) REFERENCES animator(id));";  
	
	public AnimatorsData(RequestContext requestContext) {
		super();
	}
}
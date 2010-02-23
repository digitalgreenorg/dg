package com.digitalgreen.dashboardgwt.client.data;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;

public class FieldOfficersData extends BaseData {

	protected static String createTable = "CREATE TABLE IF NOT EXISTS `field_officer` " +
			"								(id INTEGER PRIMARY KEY NOT NULL ," +
			"								 NAME VARCHAR(100) NOT NULL ," +
			"								 AGE INT NULL DEFAULT NULL," +
			"								 GENDER VARCHAR(1) NOT NULL ," +
			"								 HIRE_DATE DATE NULL DEFAULT NULL," +
			"								 SALARY FLOAT(0,0) NULL DEFAULT NULL," +
			"								 PHONE_NO VARCHAR(100) NOT NULL ," +
			"								 ADDRESS VARCHAR(500) NOT NULL ," +
			"								 reviewer_id INT NULL DEFAULT NULL," +
			"								 equipmentholder_id INT NULL DEFAULT NULL, " +
			"								 FOREIGN KEY(reviewer_id) REFERENCES reviewer(id), " +
			"								 FOREIGN KEY(equipmentholder_id) REFERENCES equipment_holder(id))";  
	
	public FieldOfficersData(RequestContext requestContext) {
		super();
	}
}
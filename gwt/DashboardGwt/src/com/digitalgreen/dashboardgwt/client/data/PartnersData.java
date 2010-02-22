package com.digitalgreen.dashboardgwt.client.data;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;

public class PartnersData extends BaseData {

	protected static String CREATE_TABLE = "CREATE TABLE IF NOT EXISTS `partners` (id INTEGER PRIMARY KEY  NOT NULL ,PARTNER_NAME VARCHAR(100)  NOT NULL ,DATE_OF_ASSOCIATION DATE  NULL DEFAULT NULL,PHONE_NO VARCHAR(100)  NOT NULL ,ADDRESS VARCHAR(500)  NOT NULL ,reviewer_id INT  NULL DEFAULT NULL,equipmentholder_id INT  NULL DEFAULT NULL, FOREIGN KEY(reviewer_id) REFERENCES reviewer(id), FOREIGN KEY(equipmentholder_id) REFERENCES equipment_holder(id) );"; 
	
	public PartnersData(RequestContext requestContext) {
		super();
	}
}
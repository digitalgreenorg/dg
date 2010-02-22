package com.digitalgreen.dashboardgwt.client.data;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;

public class ReviewersData extends BaseData {

	protected static String CREATE_TABLE = "CREATE TABLE IF NOT EXISTS `reviewer` (id INTEGER PRIMARY KEY NOT NULL ,content_type_id INT NOT NULL DEFAULT 0,object_id INT NOT NULL DEFAULT 0);"; 
	
	public ReviewersData(RequestContext requestContext) {
		super();
	}
}
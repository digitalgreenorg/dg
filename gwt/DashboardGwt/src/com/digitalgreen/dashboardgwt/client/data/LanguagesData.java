package com.digitalgreen.dashboardgwt.client.data;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;

public class LanguagesData extends BaseData {

	protected static String CREATE_TABLE = "CREATE TABLE IF NOT EXISTS `language` (id INTEGER PRIMARY KEY  NOT NULL ,language_name VARCHAR(100)  NOT NULL );";  
	
	public LanguagesData(RequestContext requestContext) {
		super();
	}
}
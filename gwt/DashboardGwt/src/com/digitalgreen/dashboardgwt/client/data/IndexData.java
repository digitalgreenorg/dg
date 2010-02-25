package com.digitalgreen.dashboardgwt.client.data;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;

public class IndexData extends BaseData {
	
	public IndexData(RequestContext requestContext) {
		super();
	}
	
	public static void createTables(){
		Schema.createSchema();
	}
}
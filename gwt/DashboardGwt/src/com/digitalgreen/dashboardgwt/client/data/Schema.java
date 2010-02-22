package com.digitalgreen.dashboardgwt.client.data;

public class Schema {
	public static void createSchema() {
		BaseData.dbOpen();
		// Get all create ddls
		
		BaseData.dbClose();
		
	}
	
	public static void dropSchema() {}
}
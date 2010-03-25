package com.digitalgreen.dashboardgwt.client.data;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;

public class ReviewersData extends BaseData {

	protected static String tableID = "3";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `reviewer` " +
												"(id INTEGER PRIMARY KEY NOT NULL ," +
												"content_type_id INT NOT NULL DEFAULT 0," +
												"object_id INT NOT NULL DEFAULT 0);"; 
	protected static String saveReviewerOfflineURL = "/dashboard/saverevieweroffline/";
	
	public ReviewersData() {
		super();
	}

	@Override
	protected String getTableId() {
		return ReviewersData.tableID;
	}
	
}
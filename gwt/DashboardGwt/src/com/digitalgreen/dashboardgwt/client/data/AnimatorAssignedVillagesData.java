package com.digitalgreen.dashboardgwt.client.data;

public class AnimatorAssignedVillagesData extends BaseData{
	
	protected static String tableID = "18";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `animator_assigned_village` " +
												"(id INTEGER PRIMARY KEY NOT NULL ," +
												"animator_id INT  NOT NULL DEFAULT 0," +
												"village_id INT  NOT NULL DEFAULT 0," +
												"START_DATE DATE  NULL DEFAULT NULL, " +
												"FOREIGN KEY(animator_id) REFERENCES animator(id), " +
												"FOREIGN KEY(village_id) REFERENCES village(id));";
	
	protected static String saveAnimatorAssignedVillageOfflineURL = "/dashboard/saveanimatorassignedvillageoffline/";

	public AnimatorAssignedVillagesData(){
		super();
	}
	
	@Override
	protected String getTableId() {
		return AnimatorAssignedVillagesData.tableID;
	}
}
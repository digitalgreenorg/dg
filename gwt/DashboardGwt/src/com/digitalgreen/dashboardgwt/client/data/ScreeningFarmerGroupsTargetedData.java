package com.digitalgreen.dashboardgwt.client.data;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;

public class ScreeningFarmerGroupsTargetedData extends BaseData {
	
	final protected static String createTable = "CREATE TABLE IF NOT EXISTS `screening_farmer_groups_targeted` " +
												"(id INTEGER PRIMARY KEY  NOT NULL ," +
												"screening_id INT  NOT NULL DEFAULT 0," +
												"persongroups_id INT  NOT NULL DEFAULT 0, " +
												"FOREIGN KEY(screening_id) REFERENCES screening(id), " +
												"FOREIGN KEY(persongroups_id) REFERENCES person_groups(id));" ;

	public ScreeningFarmerGroupsTargetedData(RequestContext requestContext){
		super();
	}
}

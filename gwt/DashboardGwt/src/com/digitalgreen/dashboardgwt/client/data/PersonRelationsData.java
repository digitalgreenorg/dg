package com.digitalgreen.dashboardgwt.client.data;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;

public class PersonRelationsData extends BaseData {

	protected static String tableID = "14";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `person_relations` " +
												"(id INTEGER PRIMARY KEY  NOT NULL ," +
												"person_id INT  NOT NULL DEFAULT 0," +
												"relative_id INT  NOT NULL DEFAULT 0," +
												"TYPE_OF_RELATIONSHIP VARCHAR(100)  NOT NULL, " +
												"FOREIGN KEY(person_id) REFERENCES person(id), " +
												"FOREIGN KEY(relative_id) REFERENCES person(id));" ;
	
	protected static String savePersonRelationOfflineURL = "/dashboard/savepersonrelationoffline/";
	
	public PersonRelationsData(){
		super();
	}
	
	@Override
	protected String getTableId() {
		return PersonRelationsData.tableID;
	}
}

package com.digitalgreen.dashboardgwt.client.data;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;

public class PersonAdoptPracticeData extends BaseData{
	
	final protected static String createTable = "CREATE TABLE IF NOT EXISTS `person_adopt_practice` " +
												"(id INTEGER PRIMARY KEY  NOT NULL ," +
												"person_id INT  NOT NULL DEFAULT 0," +
												"practice_id INT  NOT NULL DEFAULT 0," +
												"PRIOR_ADOPTION_FLAG SMALLINT  NULL DEFAULT NULL," +
												"DATE_OF_ADOPTION DATE  NULL DEFAULT NULL," +
												"QUALITY VARCHAR(200)  NOT NULL ," +
												"QUANTITY INT  NULL DEFAULT NULL," +
												"QUANTITY_UNIT VARCHAR(150)  NOT NULL, " +
												"FOREIGN KEY(person_id) REFERENCES person(id), " +
												"FOREIGN KEY(practice_id) REFERENCES practices(id));";

	public PersonAdoptPracticeData(RequestContext requestContext){
		super();
	}
}

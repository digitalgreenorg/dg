package com.digitalgreen.dashboardgwt.client.data;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;

public class PersonsData extends BaseData {

	protected static String CREATE_TABLE = "CREATE TABLE IF NOT EXISTS `person` (id INTEGER PRIMARY KEY  NOT NULL ,PERSON_NAME VARCHAR(100)  NOT NULL ,FATHER_NAME VARCHAR(100)  NOT NULL ,AGE INT  NULL DEFAULT NULL,GENDER VARCHAR(1)  NOT NULL ,PHONE_NO VARCHAR(100)  NOT NULL ,ADDRESS VARCHAR(500)  NOT NULL ,LAND_HOLDINGS INT  NULL DEFAULT NULL,village_id INT  NOT NULL DEFAULT 0,group_id INT  NULL DEFAULT NULL,equipmentholder_id INT  NULL DEFAULT NULL, FOREIGN KEY(village_id) REFERENCES village(id), FOREIGN KEY(group_id) REFERENCES person_groups(id), FOREIGN KEY(equipmentholder_id) REFERENCES equipment_holder(id) ); " +
			"CREATE TABLE IF NOT EXISTS `person_relations` (id INTEGER PRIMARY KEY  NOT NULL ,person_id INT  NOT NULL DEFAULT 0,relative_id INT  NOT NULL DEFAULT 0,TYPE_OF_RELATIONSHIP VARCHAR(100)  NOT NULL, FOREIGN KEY(person_id) REFERENCES person(id), FOREIGN KEY(relative_id) REFERENCES person(id));" +
			"CREATE TABLE IF NOT EXISTS `person_adopt_practice` (id INTEGER PRIMARY KEY  NOT NULL ,person_id INT  NOT NULL DEFAULT 0,practice_id INT  NOT NULL DEFAULT 0,PRIOR_ADOPTION_FLAG SMALLINT  NULL DEFAULT NULL,DATE_OF_ADOPTION DATE  NULL DEFAULT NULL,QUALITY VARCHAR(200)  NOT NULL ,QUANTITY INT  NULL DEFAULT NULL,QUANTITY_UNIT VARCHAR(150)  NOT NULL, FOREIGN KEY(person_id) REFERENCES person(id), FOREIGN KEY(practice_id) REFERENCES practices(id));";  
	
	public PersonsData(RequestContext requestContext) {
		super();
	}
}
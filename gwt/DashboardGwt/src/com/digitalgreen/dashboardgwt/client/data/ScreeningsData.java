package com.digitalgreen.dashboardgwt.client.data;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;

public class ScreeningsData extends BaseData {

	protected static String CREATE_TABLE = "CREATE TABLE IF NOT EXISTS `screening` (id INTEGER PRIMARY KEY  NOT NULL ,DATE DATE  NOT NULL ,START_TIME TIME  NOT NULL ,END_TIME TIME  NOT NULL ,LOCATION VARCHAR(200)  NOT NULL ,TARGET_PERSON_ATTENDANCE INT  NULL DEFAULT NULL,TARGET_AUDIENCE_INTEREST INT  NULL DEFAULT NULL,TARGET_ADOPTIONS INT  NULL DEFAULT NULL,village_id INT  NOT NULL DEFAULT 0,fieldofficer_id INT  NULL DEFAULT NULL,animator_id INT  NOT NULL DEFAULT 0, FOREIGN KEY(village_id) REFERENCES village(id), FOREIGN KEY(fieldofficer_id) REFERENCES field_officer(id), FOREIGN KEY(animator_id) REFERENCES animator(id));"+
	"CREATE TABLE IF NOT EXISTS `screening_farmer_groups_targeted` (id INTEGER PRIMARY KEY  NOT NULL ,screening_id INT  NOT NULL DEFAULT 0,persongroups_id INT  NOT NULL DEFAULT 0, FOREIGN KEY(screening_id) REFERENCES screening(id), FOREIGN KEY(persongroups_id) REFERENCES person_groups(id));" +
	"CREATE TABLE IF NOT EXISTS `screening_videoes_screened` (id INTEGER PRIMARY KEY  NOT NULL ,screening_id INT  NOT NULL DEFAULT 0,video_id INT  NOT NULL DEFAULT 0,  FOREIGN KEY(screening_id) REFERENCES screening(id), FOREIGN KEY(video_id) REFERENCES video(id));"+
	"CREATE TABLE IF NOT EXISTS `person_meeting_attendance` (id INTEGER PRIMARY KEY  NOT NULL ,screening_id INT  NOT NULL DEFAULT 0,person_id INT  NOT NULL DEFAULT 0,expressed_interest_practice_id INT  NULL DEFAULT NULL,EXPRESSED_INTEREST TEXT  NOT NULL ,expressed_adoption_practice_id INT  NULL DEFAULT NULL,EXPRESSED_ADOPTION TEXT  NOT NULL ,expressed_question_practice_id INT  NULL DEFAULT NULL,EXPRESSED_QUESTION TEXT  NOT NULL, FOREIGN KEY(screening_id) REFERENCES screening(id), FOREIGN KEY(person_id) REFERENCES person(id), FOREIGN KEY(expressed_interest_practice_id) REFERENCES practices(id), FOREIGN KEY(expressed_question_practice_id) REFERENCES practices(id), FOREIGN KEY(expressed_adoption_practice_id) REFERENCES practices(id) );";
	
	public ScreeningsData(RequestContext requestContext) {
		super();
	}
}
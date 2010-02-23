package com.digitalgreen.dashboardgwt.client.data;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;

public class PersonMeetingAttendanceData extends BaseData {

	final protected static String createTable = "CREATE TABLE IF NOT EXISTS `person_meeting_attendance` " +
												"(id INTEGER PRIMARY KEY  NOT NULL ," +
												"screening_id INT  NOT NULL DEFAULT 0," +
												"person_id INT  NOT NULL DEFAULT 0," +
												"expressed_interest_practice_id INT  NULL DEFAULT NULL," +
												"EXPRESSED_INTEREST TEXT  NOT NULL ," +
												"expressed_adoption_practice_id INT  NULL DEFAULT NULL," +
												"EXPRESSED_ADOPTION TEXT  NOT NULL ," +
												"expressed_question_practice_id INT  NULL DEFAULT NULL," +
												"EXPRESSED_QUESTION TEXT  NOT NULL, " +
												"FOREIGN KEY(screening_id) REFERENCES screening(id), " +
												"FOREIGN KEY(person_id) REFERENCES person(id), " +
												"FOREIGN KEY(expressed_interest_practice_id) REFERENCES practices(id), " +
												"FOREIGN KEY(expressed_question_practice_id) REFERENCES practices(id), " +
												"FOREIGN KEY(expressed_adoption_practice_id) REFERENCES practices(id) );";
	
	public PersonMeetingAttendanceData(RequestContext requestContext){
		super();
	}
}
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
	
	public class Data extends BaseData.Data {
		final private static String COLLECTION_PREFIX = "personmeetingattendance";
		
		private ScreeningsData.Data screening;      // FK to the Screenings table
		private PersonsData.Data person;
		private int expressed_interest_practice_id;
		private int expressed_adoption_practice_id;
		private int expressed_question_practice_id;
		
		public Data(int id, int screening_id, int person_id, int expressed_interest_practice_id,
				int expressed_adoption_practice_id, int expressed_question_practice_id) {
			this.id = id;
			this.screening = new ScreeningsData().getNewData();
			this.screening.id = screening_id;
			this.person = new PersonsData().getNewData();
			this.person.id = person_id;
			this.expressed_interest_practice_id = expressed_interest_practice_id;
			this.expressed_adoption_practice_id = expressed_adoption_practice_id;
			this.expressed_question_practice_id = expressed_question_practice_id;
		}
	

		@Override
		public void save(BaseData.Data withForeignKey) {
			String foreignKeyClassName = withForeignKey.getClass().getName();
			if(foreignKeyClassName.equals(ScreeningsData.Data.class.getName())) {
				this.screening = (ScreeningsData.Data)withForeignKey;
			} else if (foreignKeyClassName.equals(PersonsData.Data.class.getName())) {
				this.person = (PersonsData.Data)withForeignKey;
			}
			this.save();
		}
	
		@Override
		public void setObjValueFromString(String key, Object val) {
			if(key.equals("id")) {
				this.id = ((Integer)val).intValue();
			} else if(key.equals("screening_id")) {
				this.screening = (new ScreeningsData()).getNewData();
				this.screening.id = ((Integer)val).intValue();
			} else if(key.equals("person_id")) {
				this.person = (new PersonsData()).getNewData();
				this.person.id = ((Integer)val).intValue();
			} else if(key.equals("expressed_interest_practice_id")) {
				this.expressed_interest_practice_id = ((Integer)val).intValue();
			} else if(key.equals("expressed_adoption_practice_id")) {
				this.expressed_adoption_practice_id = ((Integer)val).intValue();
			} else if(key.equals("expressed_question_practice_id")) {
				this.expressed_question_practice_id = ((Integer)val).intValue();
			}
		}
	}
	
	public PersonMeetingAttendanceData(RequestContext requestContext){
		super();
	}
}
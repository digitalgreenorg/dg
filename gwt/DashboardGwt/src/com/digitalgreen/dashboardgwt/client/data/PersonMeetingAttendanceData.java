package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.PersonMeetingAttendanceData.Data;
import com.digitalgreen.dashboardgwt.client.data.PersonMeetingAttendanceData.Type;
import com.google.gwt.core.client.JsArray;
import com.google.gwt.gears.client.database.DatabaseException;
import com.google.gwt.user.client.Window;

public class PersonMeetingAttendanceData extends BaseData {

	public static class Type extends BaseData.Type{
		protected Type(){}
		
		public final native String getScreening() /*-{ return this.fields.screening;}-*/;
		public final native String getPerson() /*-{ return this.fields.person;}-*/;
		public final native String getInterested() /*-{ return this.fields.interested;}-*/;
		public final native String getExpressedInterestPractice() /*-{ return this.fields.expressed_interest_practice; }-*/;
		public final native String getExpressedInterest() /*-{ return $wnd.checkForNullValues(this.fields.expressed_interest); }-*/;
		public final native String getExpressedAdoptionVideo() /*-{ return this.fields.expressed_adoption_video; }-*/;
		public final native String getExpressedAdoption() /*-{ return $wnd.checkForNullValues(this.fields.expressed_adoption); }-*/;
		public final native String getExpressedQuestionPractice() /*-{ return this.fields.expressed_question_practice; }-*/;
		public final native String getExpressedQuestion() /*-{ return $wnd.checkForNullValues(this.fields.expressed_question); }-*/;
		
	}
	
	public class Data extends BaseData.Data {
		final private static String COLLECTION_PREFIX = "personmeetingattendance";
		
		private ScreeningsData.Data screening;// FK to the Screenings table
		private PersonsData.Data person;
		private String interested;
		private String expressed_interest;
		private VideosData.Data expressed_adoption_video;
		private String expressed_adoption;
		private String expressed_question;
		
		
		public Data() {
			super();
		}
		
		public Data(String id, ScreeningsData.Data screening, PersonsData.Data person, 
				String interested, String expressed_question, VideosData.Data expressed_adoption_video,
				String expressed_interest, String expressed_adoption) {
			this.id = id;
			this.screening = screening;
			this.person = person;
			this.interested = interested;
			this.expressed_interest = expressed_interest;
			this.expressed_adoption_video = expressed_adoption_video;
			this.expressed_adoption = expressed_adoption;
			this.expressed_question = expressed_question;
		}
		
		public Data(String id, PersonsData.Data person){
			super();
			this.id = id;
			this.person = person;
		}
		
		public Data(String id, ScreeningsData.Data screening, PersonsData.Data person){
			super();
			this.id = id;
			this.screening = screening;
			this.person = person;
		}
			
		public ScreeningsData.Data getScreening(){
			return this.screening;
		}
		
		public PersonsData.Data getPerson(){
			return this.person;
		}
		public String getInterested(){
			return this.interested;
		}
		public String getExpressedInterest(){
			return this.expressed_interest;
		}
		public VideosData.Data getExpressedAdoptionVideo(){
			return this.expressed_adoption_video;
		}
		public String getExpressedAdoption(){
			return this.expressed_adoption;
		}
		public String getExpressedQuestion(){
			return this.expressed_question;
		}
		
		public BaseData.Data clone(){
			Data obj = new Data();
			obj.person = (new PersonsData()).new Data();
			obj.expressed_adoption_video = (new VideosData()).new Data();
			return obj;
		}
		
		@Override
		public String getPrefixName() {
			return Data.COLLECTION_PREFIX;
		}
		
		@Override
		public void setObjValueFromString(String key, String val) {
			super.setObjValueFromString(key, val);
			if(key.equals("id")) {
				this.id = val;
			}else if(key.equals("screening")) {
				ScreeningsData screening = new ScreeningsData();
				this.screening = screening.getNewData();
				this.screening.id = val;
				
			} else if(key.equals("person")) {
				PersonsData person = new PersonsData();
				this.person = person.getNewData();
				this.person.id = val;
			}  else if(key.equals("expressed_interest")) {
				this.expressed_interest = (String)val;
			} else if(key.equals("expressed_adoption_video")) {
				VideosData expressed_adoption_video = new VideosData();
				this.expressed_adoption_video = expressed_adoption_video.getNewData();
				this.expressed_adoption_video.id = val;
				
			}  else if(key.equals("expressed_adoption")) {
				this.expressed_adoption= (String)val;
			}  else if(key.equals("expressed_question")) {
				this.expressed_question = (String)val;
			} else if(key.equals("interested")) {
				if (val.equals("on")) {
					this.interested = "1";
					val = "1";
				}
				else {
					this.interested = "0";
					val = "0";
				}
			} else {
				return;
			}
			this.addNameValueToQueryString(key, val);
		}
	

		@Override		
		public void save() {
			PersonMeetingAttendanceData personMeetingAttendancesDataDbApis = new PersonMeetingAttendanceData();
			String interested = "0";
			if (this.interested.equals("true")) {
				interested = "1";
			}
			this.id = personMeetingAttendancesDataDbApis.autoInsert(this.id,
						this.screening.getId(),
						this.person.getId(),
						interested, this.expressed_question, this.expressed_adoption_video.getId(), 
						this.expressed_interest, this.expressed_adoption);
			this.addNameValueToQueryString("id", this.id);
		}
		
		@Override
		public void save(BaseData.Data foreignKey) {
			PersonMeetingAttendanceData personMeetingAttendancesDataDbApis = new PersonMeetingAttendanceData();
			if (this.interested == null) {
				this.interested = "0";
			}
			this.id = personMeetingAttendancesDataDbApis.autoInsert(this.id,
						foreignKey.getId(),
						this.person.getId(),
						this.interested, this.expressed_question, this.expressed_adoption_video.getId(),
						this.expressed_interest,
						this.expressed_adoption);
			this.addNameValueToQueryString("id", this.id);
			this.addNameValueToQueryString("screening", foreignKey.getId());
		}
		
		@Override
		public String toQueryString(String id) {
			PersonMeetingAttendanceData personMeetingAttendanceData = new PersonMeetingAttendanceData();
			return this.rowToQueryString(personMeetingAttendanceData.getTableName(), personMeetingAttendanceData.getFields(), "id", id, "");
		}
		
		@Override
		public String toInlineQueryString(String id) {
			PersonMeetingAttendanceData personMeetingAttendanceData = new PersonMeetingAttendanceData();
			return rowToQueryString(personMeetingAttendanceData.getTableName(), personMeetingAttendanceData.getFields(), 
					"screening_id", id, this.COLLECTION_PREFIX + "_set");
		}
		
		@Override
		public String getTableId() {
			PersonMeetingAttendanceData personMeetingAttendancesDataDbApis = new PersonMeetingAttendanceData();
			return personMeetingAttendancesDataDbApis.tableID;
		}
	}
		
		
	public static String tableID = "30";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `person_meeting_attendance` " +
												"(id BIGINT UNSIGNED PRIMARY KEY  NOT NULL ," +
												"screening_id BIGINT UNSIGNED  NOT NULL DEFAULT 0," +
												"person_id BIGINT UNSIGNED  NOT NULL DEFAULT 0," +
												"interested INT NOT NULL DEFAULT 0," + 
												"EXPRESSED_QUESTION TEXT NULL DEFAULT NULL, " +
					                            "expressed_adoption_video_id BIGINT UNSIGNED  NULL DEFAULT NULL," +
												"expressed_interest_practice_id BIGINT UNSIGNED  NULL DEFAULT NULL," +
												"EXPRESSED_INTEREST TEXT NULL DEFAULT NULL ," +
												"EXPRESSED_ADOPTION TEXT NULL DEFAULT NULL," +
												"expressed_question_practice_id BIGINT UNSIGNED  NULL DEFAULT NULL," +
												"FOREIGN KEY(screening_id) REFERENCES screening(id), " +
												"FOREIGN KEY(person_id) REFERENCES person(id), " +
												"FOREIGN KEY(expressed_interest_practice_id) REFERENCES practices(id), " +
												"FOREIGN KEY(expressed_question_practice_id) REFERENCES practices(id), " +
												"FOREIGN KEY(expressed_adoption_video_id) REFERENCES videos(id) );";
	protected static String dropTable = "DROP TABLE IF EXISTS `person_meeting_attendance`;";
	protected static String[] createIndexes = {"CREATE INDEX IF NOT EXISTS person_meeting_attendance_PRIMARY ON person_meeting_attendance(id);", 
	   "CREATE INDEX IF NOT EXISTS person_meeting_attendance_screening_id ON person_meeting_attendance(screening_id);",
	   "CREATE INDEX IF NOT EXISTS person_meeting_attendance_person_id ON person_meeting_attendance(person_id);",
	   "CREATE INDEX IF NOT EXISTS person_meeting_attendance_expressed_interest_practice_id ON person_meeting_attendance(expressed_interest_practice_id);",
	   "CREATE INDEX IF NOT EXISTS person_meeting_attendance_region_expressed_question_practice_id ON person_meeting_attendance(expressed_question_practice_id);",
	   "CREATE INDEX IF NOT EXISTS person_meeting_attendance_region_expressed_adoption_video_id ON person_meeting_attendance(expressed_adoption_video_id);"};
	protected static String selectPersonMeetingAttendances = "SELECT pma.id, p.PERSON_NAME FROM person_meeting_attendance pma, person p" +
			"WHERE pma.person_id = p.id ORDER BY (p.PERSON_NAME);";
	protected static String listPersonMeetingAttendances = "SELECT pma.id,p.id, p.PERSON_NAME, expressed_interest_practice_id" +
			",EXPRESSED_INTEREST,expressed_adoption_video_id, EXPRESSED_ADOPTION,expressed_question_practice_id,EXPRESSED_QUESTION " +
			"FROM person_meeting_attendance pma, person p WHERE p.id = pma.person_id " +
			"ORDER BY (-pma.id);";
	protected static String savePersonMeetingAttendanceOfflineURL = "/dashboard/savepersonmeetingattendanceoffline/";
	protected static String savePersonMeetingAttendanceOnlineURL = "/dashboard/savepersonmeetingattendanceonline/";
	protected static String getPersonMeetingAttendanceOnlineURL = "/dashboard/getpersonmeetingattendancesonline/";
	protected String table_name = "person_meeting_attendance";
	protected String[] fields = {"id", "screening_id","person_id", "interested", "EXPRESSED_QUESTION", "expressed_adoption_video_id",
			"expressed_interest_practice_id", "EXPRESSED_INTEREST",
			"EXPRESSED_ADOPTION","expressed_question_practice_id",};
	
	
	public PersonMeetingAttendanceData() {
		super();
	}
	public PersonMeetingAttendanceData(OnlineOfflineCallbacks callbacks) {
		super(callbacks);
	}
	
	public PersonMeetingAttendanceData(OnlineOfflineCallbacks callbacks, Form form) {
		super(callbacks, form);
	}
	@Override
	public Data getNewData() {
		return new Data();
	}
	
	@Override
	protected String getTableId() {
		return PersonMeetingAttendanceData.tableID;
	}
	
	@Override
	public String getTableName() {
		return this.table_name;
	}
	
	@Override
	protected String[] getFields() {
		return this.fields;
	}
	
	@Override
	protected String getCreateTableSql(){
		return this.createTable;
	}
	
	@Override
	protected String getDeleteTableSql(){
		return this.dropTable;
	}

	@Override
	public String getListingOnlineURL(){
		return PersonMeetingAttendanceData.getPersonMeetingAttendanceOnlineURL;
	}
	
	@Override
	public String getSaveOfflineURL(){
		return PersonMeetingAttendanceData.savePersonMeetingAttendanceOfflineURL;
	}
	
	@Override
	public String getSaveOnlineURL(){
		return PersonMeetingAttendanceData.savePersonMeetingAttendanceOnlineURL;
	}
	
	public final native JsArray<Type> asArrayOfData(String json) /*-{
		return eval(json);
	}-*/;
	
	public List serialize(JsArray<Type> personMeetingAttendanceObjects){
		List personMeetingAttendances = new ArrayList();
		ScreeningsData screening = new ScreeningsData();
		PersonsData person = new PersonsData();
		VideosData video = new VideosData();
		
		for(int i = 0; i < personMeetingAttendanceObjects.length(); i++){
			VideosData.Data adoption_vid = video.new Data();
			ScreeningsData.Data sc = screening.new Data(personMeetingAttendanceObjects.get(i).getScreening());
			PersonsData.Data p = person.new Data(personMeetingAttendanceObjects.get(i).getPerson());

			if(personMeetingAttendanceObjects.get(i).getExpressedAdoptionVideo()!=null){
				adoption_vid = video.new Data(personMeetingAttendanceObjects.get(i).getExpressedAdoptionVideo());
			}
						
			Data personMeetingAttendance = new Data(personMeetingAttendanceObjects.get(i).getPk(),sc,p,
					personMeetingAttendanceObjects.get(i).getInterested(), personMeetingAttendanceObjects.get(i).getExpressedQuestion(), adoption_vid,
					personMeetingAttendanceObjects.get(i).getExpressedInterest(),
					personMeetingAttendanceObjects.get(i).getExpressedAdoption());
			personMeetingAttendances.add(personMeetingAttendance);
		}
		
		return personMeetingAttendances;
	}
	
	public List getPersonMeetingAttendancesListingOffline(){
		BaseData.dbOpen();
		List personMeetingAttendances = new ArrayList();
		PersonsData person = new PersonsData();
		this.select(listPersonMeetingAttendances);
		if (this.getResultSet().isValidRow()){
			try {
				for (int i = 0; this.getResultSet().isValidRow(); ++i, this.getResultSet().next()) {
					PersonsData.Data p = person.new Data(this.getResultSet().getFieldAsString(1),  this.getResultSet().getFieldAsString(2));
					Data personMeetingAttendance = new Data(this.getResultSet().getFieldAsString(0), p);
					personMeetingAttendances.add(personMeetingAttendance);
	    	      }				
			} catch (DatabaseException e) {
				Window.alert("Database Exception : " + e.toString());
				BaseData.dbClose();
			}
			
		}
		BaseData.dbClose();
		return personMeetingAttendances;
	}

	@Override
	public List getListingOnline(String json){
		return this.serialize(this.asArrayOfData(json));		
	}
	
	public List getAllPersonMeetingAttendancesOffline(){
		BaseData.dbOpen();
		List personMeetingAttendances = new ArrayList();
		PersonsData person = new PersonsData();
		this.select(selectPersonMeetingAttendances);
		if (this.getResultSet().isValidRow()){
			try {
				for (int i = 0; this.getResultSet().isValidRow(); ++i, this.getResultSet().next()) {
					PersonsData.Data p = person.new Data(this.getResultSet().getFieldAsString(1),  this.getResultSet().getFieldAsString(2));
					Data personMeetingAttendance = new Data(this.getResultSet().getFieldAsString(0), p);
					personMeetingAttendances.add(personMeetingAttendance);
	    	      }				
			} catch (DatabaseException e) {
				Window.alert("Database Exception : " + e.toString());
				BaseData.dbClose();
			}
			
		}
		BaseData.dbClose();
		return personMeetingAttendances;
	}
	
	
	public Object postPageData() {
		if(BaseData.isOnline()){
			this.post(RequestContext.SERVER_HOST + PersonMeetingAttendanceData.savePersonMeetingAttendanceOnlineURL, this.form.getQueryString());
		}
		else{
			this.save();
			return true;
		}
		return null;
	}
	
	public Object getListPageData(){
		if(BaseData.isOnline()){
			this.get(RequestContext.SERVER_HOST + PersonMeetingAttendanceData.getPersonMeetingAttendanceOnlineURL);
		}
		else{
			return true;
		}
		return false;
	}	
	
	public Object getAddPageData(){
		if(BaseData.isOnline()){
			this.get(RequestContext.SERVER_HOST + PersonMeetingAttendanceData.savePersonMeetingAttendanceOnlineURL);
		}
		return false;
	}
}

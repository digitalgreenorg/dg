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
		public final native String getExpressedInterestPractice() /*-{ return this.fields.expressed_interest_practice; }-*/;
		public final native String getExpressedInterest() /*-{ return $wnd.checkForNullValues(this.fields.expressed_interest); }-*/;
		public final native String getExpressedAdoptionPractice() /*-{ return this.fields.expressed_adoption_practice; }-*/;
		public final native String getExpressedAdoption() /*-{ return $wnd.checkForNullValues(this.fields.expressed_adoption); }-*/;
		public final native String getExpressedQuestionPractice() /*-{ return this.fields.expressed_question_practice; }-*/;
		public final native String getExpressedQuestion() /*-{ return $wnd.checkForNullValues(this.fields.expressed_question); }-*/;
		
	}
	
	public class Data extends BaseData.Data {
		final private static String COLLECTION_PREFIX = "personmeetingattendance";
		
		private ScreeningsData.Data screening;// FK to the Screenings table
		private PersonsData.Data person;
		private PracticesData.Data expressed_interest_practice;
		private String expressed_interest;
		private PracticesData.Data expressed_adoption_practice;
		private String expressed_adoption;
		private PracticesData.Data expressed_question_practice;
		private String expressed_question;
		
		
		public Data() {
			super();
		}
		
		public Data(String id, ScreeningsData.Data screening, PersonsData.Data person, PracticesData.Data expressed_interest_practice,
				String expressed_interest, PracticesData.Data expressed_adoption_practice,String expressed_adoption,
				PracticesData.Data expressed_question_practice, String expressed_question) {
			this.id = id;
			this.screening = screening;
			this.person = person;
			this.expressed_interest_practice =expressed_interest_practice;
			this.expressed_interest = expressed_interest;
			this.expressed_adoption_practice = expressed_adoption_practice;
			this.expressed_adoption = expressed_adoption;
			this.expressed_question_practice = expressed_question_practice;
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
		public PracticesData.Data getExpressedInterestPractice(){
			return this.expressed_interest_practice;
		}
		public String getExpressedInterest(){
			return this.expressed_interest;
		}
		public PracticesData.Data getExpressedAdoptionPractice(){
			return this.expressed_adoption_practice;
		}
		public String getExpressedAdoption(){
			return this.expressed_adoption;
		}
		public PracticesData.Data getExpressedQuestionPractice(){
			return this.expressed_question_practice;
		}
		public String getExpressedQuestion(){
			return this.expressed_question;
		}
		
		public BaseData.Data clone(){
			Data obj = new Data();
			obj.person = (new PersonsData()).new Data();
			obj.expressed_interest_practice = (new PracticesData()).new Data();
			obj.expressed_adoption_practice = (new PracticesData()).new Data();
			obj.expressed_question_practice = (new PracticesData()).new Data();
			return obj;
		}
		
		@Override
		public String getPrefixName() {
			return Data.COLLECTION_PREFIX;
		}
		
		@Override
		public void setObjValueFromString(String key, String val) {
			super.setObjValueFromString(key, val);
			if(key.equals("screening")) {
				ScreeningsData screening = new ScreeningsData();
				this.screening = screening.getNewData();
				this.screening.id = val;
				
			} else if(key.equals("person")) {
				PersonsData person = new PersonsData();
				this.person = person.getNewData();
				this.person.id = val;
				
			}  else if(key.equals("expressed_interest_practice")) {
				PracticesData expressed_interest_practice = new PracticesData();
				this.expressed_interest_practice = expressed_interest_practice.getNewData();
				this.expressed_interest_practice.id = val;
				
			}  else if(key.equals("expressed_interest")) {
				this.expressed_interest = (String)val;
			} else if(key.equals("expressed_adoption_practice")) {
				PracticesData expressed_adoption_practice = new PracticesData();
				this.expressed_adoption_practice = expressed_adoption_practice.getNewData();
				this.expressed_adoption_practice.id = val;
				
			}  else if(key.equals("expressed_adoption")) {
				this.expressed_adoption= (String)val;
			} else if(key.equals("expressed_question_practice")) {
				PracticesData expressed_question_practice = new PracticesData();
				this.expressed_question_practice = expressed_question_practice.getNewData();
				this.expressed_question_practice.id = val;
				
			}  else if(key.equals("expressed_question")) {
				this.expressed_question = (String)val;
			} else {
				return;
			}
			this.addNameValueToQueryString(key, val);
		}
	

		@Override		
		public void save() {
			PersonMeetingAttendanceData personMeetingAttendancesDataDbApis = new PersonMeetingAttendanceData();			
			this.id = personMeetingAttendancesDataDbApis.autoInsert(this.id,
						this.screening.getId(),
						this.person.getId(),
						this.expressed_interest_practice.getId(),this.expressed_interest,
						this.expressed_adoption_practice.getId(),this.expressed_adoption,
						this.expressed_question_practice.getId(),this.expressed_question);
			this.addNameValueToQueryString("id", this.id);
		}
		
		@Override
		public void save(BaseData.Data foreignKey) {
			PersonMeetingAttendanceData personMeetingAttendancesDataDbApis = new PersonMeetingAttendanceData();			
			this.id = personMeetingAttendancesDataDbApis.autoInsert(this.id,
						foreignKey.getId(),
						this.person.getId(),
						this.expressed_interest_practice.getId(),this.expressed_interest,
						this.expressed_adoption_practice.getId(),this.expressed_adoption,
						this.expressed_question_practice.getId(),this.expressed_question);
			this.addNameValueToQueryString("id", this.id);
			this.addNameValueToQueryString("screening", foreignKey.getId());
		}
		
		@Override
		public String getTableId() {
			PersonMeetingAttendanceData personMeetingAttendancesDataDbApis = new PersonMeetingAttendanceData();
			return personMeetingAttendancesDataDbApis.tableID;
		}
	}
		
		
	public static String tableID = "30";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `person_meeting_attendance` " +
												"(id INTEGER PRIMARY KEY  NOT NULL ," +
												"screening_id INT  NOT NULL DEFAULT 0," +
												"person_id INT  NOT NULL DEFAULT 0," +
												"expressed_interest_practice_id INT  NULL DEFAULT NULL," +
												"EXPRESSED_INTEREST TEXT NULL DEFAULT NULL ," +
												"expressed_adoption_practice_id INT  NULL DEFAULT NULL," +
												"EXPRESSED_ADOPTION TEXT NULL DEFAULT NULL," +
												"expressed_question_practice_id INT  NULL DEFAULT NULL," +
												"EXPRESSED_QUESTION TEXT NULL DEFAULT NULL, " +
												"FOREIGN KEY(screening_id) REFERENCES screening(id), " +
												"FOREIGN KEY(person_id) REFERENCES person(id), " +
												"FOREIGN KEY(expressed_interest_practice_id) REFERENCES practices(id), " +
												"FOREIGN KEY(expressed_question_practice_id) REFERENCES practices(id), " +
												"FOREIGN KEY(expressed_adoption_practice_id) REFERENCES practices(id) );";
	protected static String dropTable = "DROP TABLE IF EXISTS `person_meeting_attendance`;";
	protected static String selectPersonMeetingAttendances = "SELECT pma.id, p.PERSON_NAME FROM person_meeting_attendance pma, person p" +
			"WHERE pma.person_id = p.id ORDER BY (p.PERSON_NAME);";
	protected static String listPersonMeetingAttendances = "SELECT pma.id,p.id, p.PERSON_NAME, expressed_interest_practice_id" +
			",EXPRESSED_INTEREST,expressed_adoption_practice_id, EXPRESSED_ADOPTION,expressed_question_practice_id,EXPRESSED_QUESTION " +
			"FROM person_meeting_attendance pma, person p WHERE p.id = pma.person_id " +
			"ORDER BY (-pma.id);";
	protected static String savePersonMeetingAttendanceOfflineURL = "/dashboard/savepersonmeetingattendanceoffline/";
	protected static String savePersonMeetingAttendanceOnlineURL = "/dashboard/savepersonmeetingattendanceonline/";
	protected static String getPersonMeetingAttendanceOnlineURL = "/dashboard/getpersonmeetingattendancesonline/";
	protected String table_name = "person_meeting_attendance";
	protected String[] fields = {"id", "screening_id","person_id", "expressed_interest_practice_id", "EXPRESSED_INTEREST",
			"expressed_adoption_practice_id","EXPRESSED_ADOPTION","expressed_question_practice_id","EXPRESSED_QUESTION"};
		
	
	
	
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
		PracticesData practice = new PracticesData();
		PracticesData.Data interest_pr = practice.new Data();
		PracticesData.Data adoption_pr = practice.new Data();
		PracticesData.Data question_pr = practice.new Data();
		
		for(int i = 0; i < personMeetingAttendanceObjects.length(); i++){
			ScreeningsData.Data sc = screening.new Data(personMeetingAttendanceObjects.get(i).getScreening());
			PersonsData.Data p = person.new Data(personMeetingAttendanceObjects.get(i).getPerson());
			if(personMeetingAttendanceObjects.get(i).getExpressedInterestPractice()!=null){
				interest_pr = practice.new Data(personMeetingAttendanceObjects.get(i).getExpressedInterestPractice());
			}
			if(personMeetingAttendanceObjects.get(i).getExpressedAdoptionPractice()!=null){
				adoption_pr = practice.new Data(personMeetingAttendanceObjects.get(i).getExpressedAdoptionPractice());
			}
			
			if(personMeetingAttendanceObjects.get(i).getExpressedQuestionPractice()!=null){
				question_pr = practice.new Data(personMeetingAttendanceObjects.get(i).getExpressedQuestionPractice());
			}
			
			
			Data personMeetingAttendance = new Data(personMeetingAttendanceObjects.get(i).getPk(),sc,p,
					interest_pr,personMeetingAttendanceObjects.get(i).getExpressedInterest(),
					adoption_pr,personMeetingAttendanceObjects.get(i).getExpressedAdoption(),
					question_pr,personMeetingAttendanceObjects.get(i).getExpressedQuestion());
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

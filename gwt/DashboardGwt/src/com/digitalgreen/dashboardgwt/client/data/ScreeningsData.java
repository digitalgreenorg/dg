package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;
import java.util.List;
import java.lang.StringBuilder;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.DevelopmentManagersData.Data;
import com.digitalgreen.dashboardgwt.client.data.validation.DateValidator;
import com.digitalgreen.dashboardgwt.client.data.validation.IntegerValidator;
import com.digitalgreen.dashboardgwt.client.data.validation.ManyToManyValidator;
import com.digitalgreen.dashboardgwt.client.data.validation.StringValidator;
import com.digitalgreen.dashboardgwt.client.data.validation.TimeValidator;
import com.digitalgreen.dashboardgwt.client.data.validation.UniqueConstraintValidator;
import com.google.gwt.core.client.JsArray;
import com.google.gwt.user.client.Window;
import com.google.gwt.gears.client.database.DatabaseException;

public class ScreeningsData extends BaseData {

	public static class Type extends BaseData.Type{
		protected Type() {}
		public final native String getDate() /*-{ return $wnd.checkForNullValues(this.fields.date); }-*/;
		public final native String getStartTime() /*-{ return $wnd.checkForNullValues(this.fields.start_time);}-*/;
		public final native String getEndTime() /*-{ return $wnd.checkForNullValues(this.fields.end_time); }-*/;
		public final native String getLocation() /*-{ return $wnd.checkForNullValues(this.fields.location); }-*/;
		public final native String getTargetPersonAttendance() /*-{ return $wnd.checkForNullValues(this.fields.target_person_attendance); }-*/;
		public final native String getTargetAudienceInterest() /*-{ return $wnd.checkForNullValues(this.fields.target_audience_interest); }-*/;
		public final native String getTargetAdoptions() /*-{ return $wnd.checkForNullValues(this.fields.target_adoptions); }-*/;
		public final native VillagesData.Type getVillage() /*-{ return this.fields.village }-*/;
		public final native String getFieldOfficer() /*-{ return this.fields.fieldofficer }-*/;
		public final native String getAnimator() /*-{ return this.fields.animator}-*/;	
	}
	
	public class Data extends BaseData.Data {
		
		final private static String COLLECTION_PREFIX = "screening";
		
		private String date;   		
		private String start_time; 
	    private String end_time; 
	    private String location; 
	    private String target_person_attendance;
	    private String target_audience_interest;
	    private String target_adoptions;
	    private VillagesData.Data village;
	    private FieldOfficersData.Data fieldofficer; 
	    private AnimatorsData.Data animator;
	    private ArrayList videoes_screened;
	    private ArrayList farmer_groups_targeted;

	    public Data() {
			super();
			videoes_screened = new ArrayList();
			farmer_groups_targeted = new ArrayList();
			this.addManyToManyRelationship("video", new ScreeningVideosScreenedData(), 
					"videoes_screened");
			this.addManyToManyRelationship("persongroups", new ScreeningFarmerGroupsTargetedData(), 
					"farmer_groups_targeted");
		}
		
	    public Data(String id) {
			super();
			this.id = id;
		}
		
	    
		public Data(String id, String date) {
			super();
			this.id = id;
			this.date = date;
		}
		

		public Data(String id, String date ,String start_time, String end_time, String location,String target_person_attendance,
				String target_audience_interest,VillagesData.Data village,FieldOfficersData.Data fieldofficer, AnimatorsData.Data animator) {

			super();
			this.id = id;
			this.date = date;
			this.start_time = start_time;
			this.end_time = end_time;
			this.location = location;
			this.target_person_attendance = target_person_attendance;
			this.target_audience_interest = target_audience_interest;
			this.target_adoptions = target_adoptions;
			this.village = village;
			this.fieldofficer = fieldofficer;
			this.animator = animator;
		}
		
		public Data(String id, String date ,String start_time, String end_time, String location, String target_person_attendance,
				String target_audience_interest, String target_adoptions, VillagesData.Data village ) {
			
			super();
			this.id = id;
			this.date = date;
			this.start_time = start_time;
			this.end_time = end_time;
			this.location = location;
			this.target_person_attendance = target_person_attendance;
			this.target_audience_interest = target_audience_interest;
			this.target_adoptions = target_adoptions;
			this.village = village;
		}
		
		public String getDate(){
			return this.date;
		}		
		public String getStartTime(){
			return this.start_time;
		}		
		public String getEndTime(){
			return this.end_time;
		}
		public String getLocation(){
			return this.location;
		}
		public String getTargetPersonAttendance(){
			return this.target_person_attendance;
		}
		public String getTargetAudienceInterest(){
			return this.target_audience_interest;
		}
		public String getTargetAdoptions(){
			return this.target_adoptions;
		}
		public VillagesData.Data getVillage(){
			return this.village;
		}
		public FieldOfficersData.Data getFieldOfficer(){
			return this.fieldofficer;
		}
		public AnimatorsData.Data getCameraOperator() { 
			return this.animator;
		}
		
		@Override
		public BaseData.Data clone() {
			Data obj = new Data();
			obj.village = (new VillagesData()).new Data();
			obj.fieldofficer = (new FieldOfficersData()).new Data();
			obj.animator = (new AnimatorsData()).new Data();	
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
			} else if(key.equals("date")) {
				this.date = (String)val;
			} else if(key.equals("start_time")){
				this.start_time = (String)val;
			} else if(key.equals("end_time")) {
				this.end_time = (String)val;
			} else if (key.equals("location")) {
				this.location = (String)val;
			} else if (key.equals("target_person_attendance")){
				this.target_person_attendance = (String)val;
			} else if (key.equals("target_audience_interest")){
				this.target_audience_interest = (String)val;
			} else if (key.equals("target_adoptions")){
				this.target_adoptions = (String)val;
			} else if(key.equals("village")) {
				VillagesData village = new VillagesData();
				this.village = village.getNewData();
				this.village.id = val;
			} else if(key.equals("fieldofficer")){
				FieldOfficersData fieldofficer = new FieldOfficersData();
				this.fieldofficer = fieldofficer.getNewData();
				this.fieldofficer.id = val;
			} else if(key.equals("animator")){
				AnimatorsData animator = new AnimatorsData();
				this.animator = animator.getNewData();
				this.animator.id = val;
			} else if(key.equals("videoes_screened")) {
				videoes_screened.add(val);
			} else if(key.equals("farmer_groups_targeted")) {
				farmer_groups_targeted.add(val);
			} else {
				return;
			}
			this.addNameValueToQueryString(key, val);
		}
		
		@Override
		public boolean validate(){
			DateValidator dateValidator = new DateValidator(this.date, false, false);
			dateValidator.setError("Please make sure 'Date' is NOT EMPTY and is formatted as YYYY-MM-DD.");
			
			TimeValidator startTimeValidator = new TimeValidator(this.start_time, false, false);
			startTimeValidator.setError("Please make sure 'Start time' is NOT EMPTY and is formatted as 'HH:MM:SS' and it must be in 24 HOUR format.");
			
			TimeValidator endTimeValidator = new TimeValidator(this.end_time, false, false);
			endTimeValidator.setError("Please make sure 'End time' is NOT EMPTY and is formatted as 'HH:MM:SS' and it must be in 24 HOUR format.");
			
			StringValidator locationValidator = new StringValidator(this.location, true, false, 0, 200);
			locationValidator.setError("Please make sure that 'Location' in not nore than 200 CHARACTERS.");
			
			StringValidator villageValidator = new StringValidator(this.village.getId(), false, false, 1, 100);
			villageValidator.setError("Please make sure you choose a village for 'Village'.");
			
			StringValidator animatorValidator = new StringValidator(this.village.getId(), false, false, 1, 100);
			animatorValidator.setError("Please make sure you choose a animator for 'Animator'.");
			
			ManyToManyValidator videoScreenedValidator = new ManyToManyValidator(videoes_screened, false);
			videoScreenedValidator.setError("Please make sure you add some animators for 'Videoes screened'.");
			
			IntegerValidator targetPersonAttendanceValidator = new IntegerValidator(this.target_person_attendance, true, false);
			targetPersonAttendanceValidator.setError("Please make sure that 'Target person attendance' is a number.");
			
			IntegerValidator targetAudienceIntereseValidator = new IntegerValidator(this.target_audience_interest, true, false);
			targetAudienceIntereseValidator.setError("Please make sure that 'Target audience interest' is a number.");
			
			IntegerValidator targetAdoptionsValidator = new IntegerValidator(this.target_adoptions, true, false);
			targetAdoptionsValidator.setError("Please make sure that 'Target adoptions' is a number.");
			
			ManyToManyValidator farmerGroupValidator = new ManyToManyValidator(farmer_groups_targeted, false);
			farmerGroupValidator.setError("Please make sure you add some farmer groups for 'Farmer groups targeted'.");
			
			ArrayList uniqueDate = new ArrayList();
			uniqueDate.add("date");
			uniqueDate.add(this.date);
			
			ArrayList uniqueStartTime = new ArrayList();
			uniqueStartTime.add("start_time");
			uniqueStartTime.add(this.start_time);
			
			ArrayList uniqueEndTime = new ArrayList();
			uniqueEndTime.add("end_time");
			uniqueEndTime.add(this.end_time);
			
			ArrayList uniqueLocation = new ArrayList();
			uniqueLocation.add("location");
			uniqueLocation.add(this.location);
			
			ArrayList uniqueVillage = new ArrayList();
			uniqueVillage.add("village_id");
			uniqueVillage.add(this.village.getId());
			
			ArrayList uniqueTogether = new ArrayList();
			uniqueTogether.add(uniqueDate);
			uniqueTogether.add(uniqueStartTime);
			uniqueTogether.add(uniqueEndTime);
			uniqueTogether.add(uniqueLocation);
			uniqueTogether.add(uniqueVillage);
			
			UniqueConstraintValidator uniqueDateStartEndTimeLocationVillageId = new UniqueConstraintValidator(uniqueTogether, new ScreeningsData());
			uniqueDateStartEndTimeLocationVillageId.setError("The Date, Start time, End time, Location, and Village are already in the system.  Please make sure they are unique.");
			uniqueDateStartEndTimeLocationVillageId.setCheckId(this.getId());
			
			ArrayList validatorList = new ArrayList();
			validatorList.add(dateValidator);
			validatorList.add(startTimeValidator);
			validatorList.add(endTimeValidator);
			validatorList.add(locationValidator);
			validatorList.add(villageValidator);
			validatorList.add(animatorValidator);
			validatorList.add(videoScreenedValidator);
			validatorList.add(targetPersonAttendanceValidator);
			validatorList.add(targetAudienceIntereseValidator);
			validatorList.add(targetAdoptionsValidator);
			validatorList.add(farmerGroupValidator);
			validatorList.add(uniqueDateStartEndTimeLocationVillageId);
			return this.executeValidators(validatorList);
		}
		
		@Override
		public void save() {
			ScreeningsData screeningsDataDbApis = new ScreeningsData();			
			this.id = screeningsDataDbApis.autoInsert(this.id, 
					this.date, 
					this.start_time,
					this.end_time, 
					this.location,
					this.target_person_attendance, 
					this.target_audience_interest, 
					this.target_adoptions,
					this.village.getId(),
					this.fieldofficer.getId(),
					this.animator.getId());
			this.addNameValueToQueryString("id", this.id);

		}
		
		@Override
		public String toQueryString(String id) {
			ScreeningsData screeningsData = new ScreeningsData();
			return this.rowToQueryString(screeningsData.getTableName(), screeningsData.getFields(), "id", id, "");
		}
		
		@Override
		public String getTableId() {
			ScreeningsData screeningsDataDbApis = new ScreeningsData();
			return screeningsDataDbApis.tableID;
		}
	}
	
	public static String tableID = "29";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `screening` " +
												"(id INTEGER PRIMARY KEY  NOT NULL ," +
												"DATE DATE  NOT NULL ," +
												"START_TIME TIME  NOT NULL ," +
												"END_TIME TIME  NOT NULL ," +
												"LOCATION VARCHAR(200) NULL," +
												"TARGET_PERSON_ATTENDANCE INT  NULL DEFAULT NULL," +
												"TARGET_AUDIENCE_INTEREST INT  NULL DEFAULT NULL," +
												"TARGET_ADOPTIONS INT  NULL DEFAULT NULL," +
												"village_id INT  NOT NULL DEFAULT 0," +
												"fieldofficer_id INT  NULL DEFAULT NULL," +
												"animator_id INT  NOT NULL DEFAULT 0, " +
												"FOREIGN KEY(village_id) REFERENCES village(id), " +
												"FOREIGN KEY(fieldofficer_id) REFERENCES field_officer(id), " +
												"FOREIGN KEY(animator_id) REFERENCES animator(id));";
	protected static String dropTable = "DROP TABLE IF EXISTS `screening`;";
	protected static String selectScreenings = "SELECT sc.id, sc.DATE, sc.location FROM screening sc ORDER BY (sc.DATE);";
	protected static String listScreenings = "SELECT sc.id, sc.DATE, sc.start_time,sc.end_time, sc.location, sc.target_person_attendance," +
			"sc.target_audience_interest, sc.target_adoptions, sc.village_id,vil.village_name FROM screening sc JOIN village vil " +
			"ON sc.village_id = vil.id ORDER BY (-sc.id);";
	protected static String saveScreeningOnlineURL = "/dashboard/savescreeningonline/";
	protected static String getScreeningOnlineURL = "/dashboard/getscreeningsonline/";
	protected static String saveScreeningOfflineURL = "/dashboard/savescreeningoffline/";
	protected String table_name = "screening";
	protected String[] fields = {"id", "date", "start_time", "end_time", "location", "target_person_attendance", "target_audience_interest",
									"target_adoptions","village", "fieldofficer", "animator"}; 
	
	public ScreeningsData() {
		super();
	}
	
	public ScreeningsData(OnlineOfflineCallbacks callbacks) {
		super(callbacks);
	}
	
	public ScreeningsData(OnlineOfflineCallbacks callbacks, Form form) {
		super(callbacks, form);
	}
	
	@Override
	public Data getNewData() {
		return new Data();
	}
	
	@Override
	protected String getTableId() {
		return ScreeningsData.tableID;
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
		return ScreeningsData.getScreeningOnlineURL;
	}
	
	@Override
	public String getSaveOfflineURL(){
		return ScreeningsData.saveScreeningOfflineURL;
	}
	
	@Override
	public String getSaveOnlineURL(){
		return ScreeningsData.saveScreeningOnlineURL;
	}
	
	public final native JsArray<Type> asArrayOfData(String json) /*-{
		return eval(json);
	}-*/;
	
	public List serialize(JsArray<Type> screeningObjects){
		List screenings = new ArrayList();
		VillagesData village = new VillagesData();
		FieldOfficersData fieldOfficer = new FieldOfficersData();
		AnimatorsData animator = new AnimatorsData();

		for(int i = 0; i < screeningObjects.length(); i++){
			FieldOfficersData.Data fo = fieldOfficer.new Data();
			VillagesData.Data v = village.new Data(screeningObjects.get(i).getVillage().getPk(), 
										screeningObjects.get(i).getVillage().getVillageName());
						
			if(screeningObjects.get(i).getFieldOfficer()!=null){
				fo = fieldOfficer.new Data(screeningObjects.get(i).getFieldOfficer());
			}
			
			AnimatorsData.Data a = animator.new Data(screeningObjects.get(i).getAnimator());
			Data screening = new Data(screeningObjects.get(i).getPk(),
					screeningObjects.get(i).getDate(),
					screeningObjects.get(i).getStartTime(),
					screeningObjects.get(i).getEndTime(),
					screeningObjects.get(i).getLocation(),
					screeningObjects.get(i).getTargetPersonAttendance(),
					screeningObjects.get(i).getTargetAudienceInterest(),
					v,
					fo,
					a);

			screenings.add(screening);
		}
		
		return screenings;
	}
	
	@Override
	public List getListingOnline(String json){
		return this.serialize(this.asArrayOfData(json));		
	}
	
	public List getScreeningsListingOffline(){
		BaseData.dbOpen();
		List screenings = new ArrayList();
		VillagesData village = new VillagesData();
		this.select(listScreenings);
		if (this.getResultSet().isValidRow()){
			try {
				for (int i = 0; this.getResultSet().isValidRow(); ++i, this.getResultSet().next()) {
					
					VillagesData.Data v = village.new Data(this.getResultSet().getFieldAsString(8),  this.getResultSet().getFieldAsString(9));
					
					Data screening = new Data(this.getResultSet().getFieldAsString(0), this.getResultSet().getFieldAsString(1), 
											this.getResultSet().getFieldAsString(2),this.getResultSet().getFieldAsString(3), 
											this.getResultSet().getFieldAsString(4),this.getResultSet().getFieldAsString(5),
											this.getResultSet().getFieldAsString(6),this.getResultSet().getFieldAsString(7), v);
					
					screenings.add(screening);
				}
			}
			catch (DatabaseException e) {
				Window.alert("Database Exception : " + e.toString());
				BaseData.dbClose();
			}
		}
		BaseData.dbClose();
		return screenings;
	}
	
	public List getAllScreeningsOffline(){
		BaseData.dbOpen();
		List screenings = new ArrayList();
		this.select(selectScreenings);
		if (this.getResultSet().isValidRow()){
			try {
				for (int i = 0; this.getResultSet().isValidRow(); ++i, this.getResultSet().next()) {
					Data screening = new Data(this.getResultSet().getFieldAsString(0), this.getResultSet().getFieldAsString(1));
					screenings.add(screening);
				}
			}
			catch (DatabaseException e) {
				Window.alert("Database Exception : " + e.toString());
				BaseData.dbClose();
			}
		}
		BaseData.dbClose();
		return screenings;
	}
	
	
	public Object postPageData() {
		if(BaseData.isOnline()){
			this.post(RequestContext.SERVER_HOST + ScreeningsData.saveScreeningOnlineURL, this.form.getQueryString());
		}
		else{
			if(this.validate()) {
				this.save();
				return true;
			}
		}
		return false;
	}
	
	public Object postPageData(String id) {
		if(BaseData.isOnline()){
			this.post(RequestContext.SERVER_HOST + this.saveScreeningOnlineURL + id + "/", this.form.getQueryString());
		}
		else{
			if(this.validate()) {
				this.save();
				return true;
			}
		}
		return false;
	}
	
	// Get all information/data to displayt he screening list page.
	public Object getListPageData() {
		if(BaseData.isOnline()) {
			this.get(RequestContext.SERVER_HOST + ScreeningsData.getScreeningOnlineURL);
		} else {
			return true;
		}
		return false;	
	}
	
	public String retrieveDataAndConvertResultIntoHtml(){
		
		StringBuilder sbHtml = new StringBuilder();
		
		VillagesData villageData = new VillagesData();
		List villages = villageData.getAllVillagesOffline();
		VillagesData.Data village;
		sbHtml.append("<select name=\"village\" id=\"id_village\">" + 
						"<option value=''>---------</option>");
		for(int i = 0; i < villages.size(); i++){
			village = (VillagesData.Data)villages.get(i);
			sbHtml.append("<option value = \"" + village.getId() +"\">" + village.getVillageName() + "</option>");
		}
		sbHtml.append("</select>");		
		
		AnimatorsData animatorData = new AnimatorsData();
		List animators = animatorData.getAllAnimatorsWithVillageOffline();
		AnimatorsData.Data animator;
		sbHtml.append("<select name=\"animator\" id=\"id_animator\">" + 
						"<option value='' >---------</option>");
		for(int i = 0; i < animators.size(); i++){
			animator = (AnimatorsData.Data)animators.get(i);
			Window.alert("animator.getVillage().getVillageName() = " + animator.getVillage().getVillageName());
			sbHtml.append("<option value = \"" + animator.getId() +"\">" + animator.getAnimatorName() + '('+ animator.getVillage().getVillageName() +')' + "</option>");
		}
		sbHtml.append("</select>");
		
		VideosData videoData = new VideosData();
		List videos = videoData.getAllVideosOffline();
		VideosData.Data video;
		sbHtml.append("<select name=\"videoes_screened\" id=\"id_videoes_screened\">" + 
						"<option value='' >---------</option>");
		for(int i = 0; i < videos.size(); i++){
			video = (VideosData.Data)videos.get(i);
			sbHtml.append("<option value = \"" + video.getId() +"\">" + video.getTitle() + "</option>");
		}
		sbHtml.append("</select>");
		
		FieldOfficersData fieldOfficerData = new FieldOfficersData();
		List fieldOfficers = fieldOfficerData.getAllFieldOfficersOffline();
		FieldOfficersData.Data fieldOfficer;
		sbHtml.append("<select name=\"fieldofficer\" id=\"id_fieldofficer\">" + 
						"<option value=''>---------</option>");
		for(int i = 0; i < fieldOfficers.size(); i++){
			fieldOfficer = (FieldOfficersData.Data)fieldOfficers.get(i);
			sbHtml.append("<option value = \"" + fieldOfficer.getId() +"\">" + fieldOfficer.getFieldOfficerName() + "</option>");
		}
		sbHtml.append("</select>");
		
		PersonGroupsData personGroupData = new PersonGroupsData();
		List personGroups = personGroupData.getAllPersonGroupsWithVillageOffline();
		PersonGroupsData.Data personGroup;
		sbHtml.append("<select name=\"farmer_groups_targeted\" id=\"id_farmer_groups_targeted\">" + 
						"<option value=''>---------</option>");
		for(int i = 0; i < personGroups.size(); i++){
			personGroup = (PersonGroupsData.Data)personGroups.get(i);
			sbHtml.append("<option value = \"" + personGroup.getId() +"\">" + personGroup.getPersonGroupName() + '('+ personGroup.getVillage().getVillageName() +')' +"</option>");
		}
		sbHtml.append("</select>");
		
		return sbHtml.toString();
	}
	
	// Get all information to display the screening add page.
	public Object getAddPageData() {
		if(BaseData.isOnline()) {
			this.get(RequestContext.SERVER_HOST + ScreeningsData.saveScreeningOnlineURL);
		} else {
			return retrieveDataAndConvertResultIntoHtml();
		}
		return false;
	}
	
	public Object getAddPageData(String id){
		if(BaseData.isOnline()){
			this.get(RequestContext.SERVER_HOST + this.saveScreeningOnlineURL + id + "/" );
		}
		else {
			this.form.toQueryString(id);
			return retrieveDataAndConvertResultIntoHtml();
		}
		return false;
	}

	
}
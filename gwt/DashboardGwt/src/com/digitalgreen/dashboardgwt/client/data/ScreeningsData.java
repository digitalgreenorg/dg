package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.ScreeningsData.Data;
import com.digitalgreen.dashboardgwt.client.data.ScreeningsData.Type;
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
		public final native FieldOfficersData.Type getFieldOfficer() /*-{ return this.fields.fieldofficer }-*/;
		public final native AnimatorsData.Type getCameraOperator() /*-{ return this.fields.animator}-*/;
		public final native PersonGroupsData.Type getFarmerGroupsTargeted () /*-{ return this.fields.farmer_groups_targeted  }-*/;
		public final native VideosData.Type getVideosScreened() /*-{ return this.fields.videoes_screened }-*/;
		public final native PersonMeetingAttendanceData.Type getFarmersAttendance () /*-{ return this.fields.farmers_attendance  }-*/;

		
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
	   	    
	    public Data() {
			super();
		}
		
		public Data(String id, String date) {
			super();
			this.id = id;
			this.date = date;
			this.location = location;
		}
		
		public Data(String id, String date ,String start_time, String end_time, String location, String target_person_attendance,
				String target_audience_interest, String target_adoptions, VillagesData.Data village, FieldOfficersData.Data fieldofficer,
				AnimatorsData.Data animator) {
			
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
			return this.start_time;
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
			return obj;
		}
		
		@Override
		public String getPrefixName() {
			return Data.COLLECTION_PREFIX;
		}
		
		@Override
		public void setObjValueFromString(String key, String val) {		
			super.setObjValueFromString(key, val);
			if(key.equals("date")) {
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
			} else {
				return;
			}
			this.addNameValueToQueryString(key, val);
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
		public String getTableId() {
			ScreeningsData screeningsDataDbApis = new ScreeningsData();
			return screeningsDataDbApis.tableID;
		}
	}
	
	protected static String tableID = "25";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `screening` " +
												"(id INTEGER PRIMARY KEY  NOT NULL ," +
												"DATE DATE  NOT NULL ," +
												"START_TIME TIME  NOT NULL ," +
												"END_TIME TIME  NOT NULL ," +
												"LOCATION VARCHAR(200)  NOT NULL ," +
												"TARGET_PERSON_ATTENDANCE INT  NULL DEFAULT NULL," +
												"TARGET_AUDIENCE_INTEREST INT  NULL DEFAULT NULL," +
												"TARGET_ADOPTIONS INT  NULL DEFAULT NULL," +
												"village_id INT  NOT NULL DEFAULT 0," +
												"fieldofficer_id INT  NULL DEFAULT NULL," +
												"animator_id INT  NOT NULL DEFAULT 0, " +
												"FOREIGN KEY(village_id) REFERENCES village(id), " +
												"FOREIGN KEY(fieldofficer_id) REFERENCES field_officer(id), " +
												"FOREIGN KEY(animator_id) REFERENCES animator(id));";
	
	protected static String selectScreenings = "SELECT sc.id, sc.DATE, sc.location FROM screening sc ORDER BY (sc.DATE);";
	protected static String listScreenings = "SELECT sc.id, sc.DATE, sc.start_time,sc.end_time, sc.location, sc.target_person_attendance," +
			"sc.target_audience_interest, sc.target_adoptions, sc.village_id,vil.village_name FROM screening sc JOIN village vil " +
			"ON sc.village_id = vil.id ORDER BY (-sc.id);";
	protected static String saveScreeningOnlineURL = "/dashboard/savescreeningonline/";
	protected static String getScreeningOnlineURL = "/dashboard/getscreeningsonline/";
	protected static String saveScreeningOfflineURL = "/dashboard/savescreeningoffline/";
	protected String table_name = "screening";
	protected String[] fields = {"id", "date", "START_TIME", "END_TIME", "LOCATION", "TARGET_PERSON_ATTENDANCE", "TARGET_AUDIENCE_INTEREST",
									"TARGET_ADOPTIONS","village_id", "fieldofficer_id", "animator_id"}; 
	
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
	protected String getTableName() {
		return this.table_name;
	}
	
	@Override
	protected String[] getFields() {
		return this.fields;
	}
	
	@Override
	public String getListingOnlineURL(){
		return ScreeningsData.getScreeningOnlineURL;
	}
	
	public final native JsArray<Type> asArrayOfData(String json) /*-{
		return eval(json);
	}-*/;
	
	public List serialize(JsArray<Type> screeningObjects){
		List screenings = new ArrayList();
		VillagesData village = new VillagesData();
		FieldOfficersData fieldofficer = new FieldOfficersData();
	    AnimatorsData animator = new AnimatorsData();
	    PersonGroupsData farmer_groups_targeted = new PersonGroupsData();
		for(int i = 0; i < screeningObjects.length(); i++){
			
			VillagesData.Data v = village.new Data(screeningObjects.get(i).getVillage().getPk(), 
										screeningObjects.get(i).getVillage().getVillageName());
			
			FieldOfficersData.Data f = null;
			
			if(screeningObjects.get(i).getFieldOfficer() != null) {
				
				f = fieldofficer.new Data(screeningObjects.get(i).getFieldOfficer().getPk(),
													screeningObjects.get(i).getFieldOfficer().getFieldOfficerName());
			} else {
				f = null;
			}
			
			AnimatorsData.Data a = animator.new Data(screeningObjects.get(i).getCameraOperator().getPk(),
													screeningObjects.get(i).getCameraOperator().getAnimatorName());
			
			Data screening = new Data(screeningObjects.get(i).getPk(),
									screeningObjects.get(i).getDate(),
									screeningObjects.get(i).getStartTime(),
									screeningObjects.get(i).getEndTime(),
									screeningObjects.get(i).getLocation(),
									screeningObjects.get(i).getTargetPersonAttendance(),
									screeningObjects.get(i).getTargetAudienceInterest(),
									screeningObjects.get(i).getTargetAdoptions(), v, f, a);
			
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
			this.save();
			return true;
		}
		return null;
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
		
		Window.alert("In retrieveDataAndConvertResultIntoHtml");
		
		VillagesData villageData = new VillagesData();
		List villages = villageData.getAllVillagesOffline();
		VillagesData.Data village;
		String html = "<select name=\"village\" id=\"id_village\">" + 
						"<option value='' selected='selected'>---------</option>";
		for(int i = 0; i < villages.size(); i++){
			village = (VillagesData.Data)villages.get(i);
			html = html + "<option value = \"" + village.getId() +"\">" + village.getVillageName() + "</option>";
		}
		html = html + "</select>";
		Window.alert("Village html:"+html);
		
		AnimatorsData animatorData = new AnimatorsData();
		List animators = animatorData.getAllAnimatorsOffline();
		AnimatorsData.Data animator;
		html = html+"<select name=\"animator\" id=\"id_animator\">" + 
				"<option value='' selected='selected'>---------</option>";
		for(int i = 0; i < animators.size(); i++){
			animator = (AnimatorsData.Data)animators.get(i);
			html = html + "<option value = \"" + animator.getId() +"\">" + animator.getAnimatorName() + "</option>";
		}
		html = html + "</select>";
		Window.alert("Village html,Animator html:"+html);
		
		VideosData videoData = new VideosData();
		List videos = videoData.getAllVideosOffline();
		VideosData.Data video;
		html = html+"<select name=\"videoes_screened\" id=\"id_videoes_screened\">" + 
				"<option value='' selected='selected'>---------</option>";
		for(int i = 0; i < videos.size(); i++){
			video = (VideosData.Data)videos.get(i);
			html = html + "<option value = \"" + video.getId() +"\">" + video.getTitle() + "</option>";
		}
		html = html + "</select>";
		Window.alert("Village html,Animator html,videos:"+html);
		
		FieldOfficersData fieldOfficerData = new FieldOfficersData();
		List fieldOfficers = fieldOfficerData.getAllFieldOfficersOffline();
		FieldOfficersData.Data fieldOfficer;
		html = html+"<select name=\"fieldofficer\" id=\"id_fieldofficer\">" + 
				"<option value='' selected='selected'>---------</option>";
		for(int i = 0; i < fieldOfficers.size(); i++){
			fieldOfficer = (FieldOfficersData.Data)fieldOfficers.get(i);
			html = html + "<option value = \"" + fieldOfficer.getId() +"\">" + fieldOfficer.getFieldOfficerName() + "</option>";
		}
		html = html + "</select>";
		Window.alert("Village html,Animator html,videos,fieldofficers:"+html);
		
		PersonGroupsData personGroupData = new PersonGroupsData();
		List personGroups = personGroupData.getAllPersonGroupsOffline();
		PersonGroupsData.Data personGroup;
		html = html + "<select name=\"farmer_groups_targeted\" id=\"id_farmer_groups_targeted\">" + 
				"<option value='' selected='selected'>---------</option>";
		for(int i = 0; i < personGroups.size(); i++){
			personGroup = (PersonGroupsData.Data)personGroups.get(i);
			html = html + "<option value = \"" + personGroup.getId() +"\">" + personGroup.getPersonGroupName() + "</option>";
		}
		html = html + "</select>";
		
		Window.alert("all html is: "+html);
		return html;
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
}
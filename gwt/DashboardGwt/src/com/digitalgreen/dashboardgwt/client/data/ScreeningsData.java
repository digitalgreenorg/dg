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
	    private PersonGroupsData.Data farmer_groups_targeted; 
	    private VideosData.Data videoes_screened;
	    private PersonMeetingAttendanceData.Data farmers_attendance;    
	    
	    public Data() {
			super();
		}
		
		public Data(String id, String date) {
			super();
			this.id = id;
			this.date = date;
		}
		

		public Data(String id, String date ,String start_time, String end_time, String location,String target_person_attendance,
				String target_audience_interest,VillagesData.Data village) {
			super();
			this.id = id;
			this.date = date;
			this.start_time = start_time;
			this.end_time = end_time;
			this.location = location;
			this.target_person_attendance = target_person_attendance;
			this.target_audience_interest = target_audience_interest;
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
		public VillagesData.Data getVillage(){
			return this.village;
		}
		
	
		public BaseData.Data clone() {
			Data obj = new Data();
			obj.id = this.id;
			obj.date = this.date;
			obj.start_time = this.start_time;
			obj.end_time = this.end_time;
			obj.location = this.location;
			obj.target_person_attendance = this.target_person_attendance;
			obj.target_audience_interest = this.target_audience_interest;
			obj.target_adoptions = this.target_adoptions;
			obj.village = this.village;
			obj.fieldofficer = this.fieldofficer;
			obj.animator = this.animator;
			obj.farmer_groups_targeted = this.farmer_groups_targeted;
			obj.videoes_screened = this.videoes_screened;
			obj.farmers_attendance = this.farmers_attendance;
			
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
			} else if(key.equals("farmer_groups_targeted")){
				PersonGroupsData farmer_groups_targeted = new PersonGroupsData();
				this.farmer_groups_targeted = farmer_groups_targeted.getNewData();
				this.farmer_groups_targeted.id = val;
			} else if(key.equals("videoes_screened")){
				VideosData videoes_screened = new VideosData();
				this.videoes_screened = videoes_screened.getNewData();
				this.videoes_screened.id = val;
			} else if(key.equals("farmers_attendance")) {
				PersonMeetingAttendanceData farmers_attendance = new PersonMeetingAttendanceData();
				this.farmers_attendance = farmers_attendance.getNewData();
				this.farmers_attendance.id = val;
			} 
			
			
		}
		
		
		@Override
		public void save() {
			
			ScreeningsData screeningsDataDbApis = new ScreeningsData();			
			if(this.id == null){
				this.id = screeningsDataDbApis.autoInsert(this.date, this.start_time,this.end_time, this.location,this.target_person_attendance, 
						this.target_audience_interest, this.target_adoptions,Integer.valueOf(this.village.getId()).toString(),
						Integer.valueOf(this.fieldofficer.getId()).toString(), Integer.valueOf(this.animator.getId()).toString(),
						Integer.valueOf(this.farmer_groups_targeted.getId()).toString(),Integer.valueOf(this.videoes_screened.getId()).toString(),
						Integer.valueOf(this.farmers_attendance.getId()).toString());
			}
			else{
				this.id = screeningsDataDbApis.autoInsert(Integer.valueOf(this.id).toString(), this.date, this.start_time,this.end_time, this.location,this.target_person_attendance, 
						this.target_audience_interest, this.target_adoptions,Integer.valueOf(this.village.getId()).toString(),
						Integer.valueOf(this.fieldofficer.getId()).toString(), Integer.valueOf(this.animator.getId()).toString(),
						Integer.valueOf(this.farmer_groups_targeted.getId()).toString(),Integer.valueOf(this.videoes_screened.getId()).toString(),
						Integer.valueOf(this.farmers_attendance.getId()).toString());
			}
			
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
	protected String[] fields = {"id", "date", "START_TIME", "END_TIME", "LOCATION", "TARGET_PERSON_ATTENDANCE", "TARGET_AUDIENCE_INTEREST"
			,"TARGET_ADOPTIONS","village_id", "fieldofficer_id", "animator_id"}; 
	
			
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
		for(int i = 0; i < screeningObjects.length(); i++){
			VillagesData.Data v = village.new Data(screeningObjects.get(i).getVillage().getPk(), screeningObjects.get(i).getVillage().getVillageName()) ;
			Data screening = new Data(screeningObjects.get(i).getPk(),
					screeningObjects.get(i).getDate(),
					screeningObjects.get(i).getStartTime(),
					screeningObjects.get(i).getEndTime(),
					screeningObjects.get(i).getLocation(),
					screeningObjects.get(i).getTargetPersonAttendance(),
					screeningObjects.get(i).getTargetAudienceInterest(),v);
			screenings.add(screening);
		}
		
		return screenings;
	}
	
	@Override
	public List getListingOnline(String json){
		return this.serialize(this.asArrayOfData(json));		
	}
	public Object postPageData() {
		return null;
	}
	
	// Get all information to display the screening add page.
	public Object getAddPageData() {
		if(this.isOnline()) {
			this.get("");
		} else {
			this.select("", null);
		}
		return null;
	}
	
	// Get all information/data to displayt he screening list page.
	public Object getListPageData() {
		if(this.isOnline()) {
			this.get("");
		} else {
			this.select("", null);
		}
		return null;		
	}
}
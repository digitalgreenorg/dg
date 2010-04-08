package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.data.PersonGroupsData.Type;
import com.digitalgreen.dashboardgwt.client.data.VillagesData.Data;
import com.google.gwt.core.client.JsArray;
import com.google.gwt.user.client.Window;

public class PersonGroupsData extends BaseData {

	public static class Type extends BaseData.Type{
		protected Type() {}
		public final native String getPersonGroupName() /*-{ return this.fields.group_name; }-*/;
		public final native String getDays() /*-{ return this.fields.days; }-*/;
		public final native String getTimings() /*-{ return this.fields.timings; }-*/;
		public final native String getTimeUpdated() /*-{ return this.fields.time_updated; }-*/;
		public final native VillagesData.Type getVillage() /*-{ return this.fields.village;}-*/;
	}
	
	public class Data extends BaseData.Data {		
		final private static String COLLECTION_PREFIX = "persongroups";
		
		private String group_name;
		private String days;
		private String timings;
		private String time_updated;
		private VillagesData.Data village;

		public Data() {
			super();
		}
		
		public Data(String id, String group_name){
			super();
			this.id = id;
			this.group_name = group_name;
		}
		
		public Data(String id, String group_name, String days, String timings,
				String time_updated, VillagesData.Data village){
			super();
			this.id = id;
			this.group_name = group_name;
			this.days = days;
			this.timings = timings;
			this.time_updated = time_updated;
			this.village = village;
		}
		
		@Override
		public BaseData.Data clone() {
			Data obj = new Data();
			obj.id = this.id;
			obj.group_name = this.group_name;
			obj.days = this.days;
			obj.timings = this.timings;
			obj.time_updated = this.time_updated;
			obj.village = this.village;
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
			} else if(key.equals("group_name")) {
				this.group_name = (String)val;
			} else if(key.equals("days")) {
				this.days = (String)val;
			} else if(key.equals("timings")) {
				this.timings = (String)val;
			} else if(key.equals("time_updated")) {
				this.time_updated = (String)val;
			} else if(key.equals("village")) {
				VillagesData village = new VillagesData();
				this.village = village.getNewData();
				this.village.id = val;
			}
		}
		
		@Override
		public void save() {
			AnimatorsData animatorsDataDbApis = new AnimatorsData();
<<<<<<< .mine
			this.id = animatorsDataDbApis.autoInsert(this.group_name, 
					this.days, 
					this.timings,
					this.time_updated, 
					this.village.getId());
=======
			if(this.id==0){
				this.id = animatorsDataDbApis.autoInsert(this.group_name, 
						this.days, 
						this.timings,
						this.time_updated, 
						Integer.valueOf(this.village.getId()).toString());
			}else{
				this.id = animatorsDataDbApis.autoInsert(Integer.valueOf(this.id).toString(),
						this.group_name, 
						this.days, 
						this.timings,
						this.time_updated, 
						Integer.valueOf(this.village.getId()).toString());
			}
			
>>>>>>> .r278
		}
	}
	
	protected static String tableID = "12";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `person_groups` " +
												"(id INTEGER PRIMARY KEY  NOT NULL ," +
												"GROUP_NAME VARCHAR(100)  NOT NULL ," +
												"DAYS VARCHAR(9) NOT NULL ," +
												"TIMINGS TIME  NULL DEFAULT NULL," +
												"TIME_UPDATED DATETIME  NOT NULL ," +
												"village_id INT  NOT NULL DEFAULT 0, " +
												"FOREIGN KEY(village_id) REFERENCES village(id));"; 
	
	protected static String selectPersonGroups = "SELECT id, GROUP_NAME FROM person_groups  ORDER BY (GROUP_NAME);";
	protected static String listPersonGroups = "SELECT * FROM person_groups pg JOIN village vil ON pg.village_id = vil.id ORDER BY (-pg.id);";
	protected static String savePersonGroupOfflineURL = "/dashboard/savepersongroupoffline/";
	protected static String savePersonGroupOnlineURL = "/dashboard/savepersongrouponline/";
	protected static String getPersonGroupOnlineURL = "/dashboard/getpersongroupsonline/";
	protected String table_name = "persongroup";
	protected String[] fields = {"id", "group_name","days", "timings", "time_updated", "village_id"};
		
	public PersonGroupsData() {
		super();
	}
	
	public PersonGroupsData(OnlineOfflineCallbacks callbacks) {
		super(callbacks);
	}
	
	public PersonGroupsData(OnlineOfflineCallbacks callbacks, Form form, String queryString) {
		super(callbacks, form, queryString);
	}
	@Override
	public Data getNewData() {
		return new Data();
	}
	
	@Override
	protected String getTableId() {
		return AnimatorsData.tableID;
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
		return PersonGroupsData.getPersonGroupOnlineURL;
	}
		
	
	public final native JsArray<Type> asArrayOfData(String json) /*-{
		return eval(json);
	}-*/;
	
	public List serialize(JsArray<Type> personGroupObjects){
		List personGroups = new ArrayList();
		VillagesData village = new VillagesData();
		for(int i = 0; i < personGroupObjects.length(); i++){
			VillagesData.Data vil = village.new Data(Integer.parseInt(personGroupObjects.get(i).getVillage().getPk()),
					personGroupObjects.get(i).getVillage().getVillageName());
						
			Data personGroup = new Data(Integer.parseInt(personGroupObjects.get(i).getPk()),
						personGroupObjects.get(i).getPersonGroupName(),
						personGroupObjects.get(i).getDays(),
						personGroupObjects.get(i).getTimings(),
						personGroupObjects.get(i).getTimeUpdated(),vil);
			personGroups.add(personGroup);
		}
		
		return personGroups;
	}
	
	@Override
	public List getListingOnline(String json){
		return this.serialize(this.asArrayOfData(json));		
	}
	
	
}
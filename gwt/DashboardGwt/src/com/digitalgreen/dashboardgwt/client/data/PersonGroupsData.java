package com.digitalgreen.dashboardgwt.client.data;

public class PersonGroupsData extends BaseData {

	public static class Type extends BaseData.Type{
		protected Type() {}
		public final native String getPersonGroupName() /*-{ return this.fields.group_name; }-*/;
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
		
		public Data(int id, String group_name){
			super();
			this.id = id;
			this.group_name = group_name;
		}
		
		public Data(int id, String group_name, String days, String timings,
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
			obj.village = (VillagesData.Data)this.village.clone();
			return obj;
		}
		
		@Override
		public void setObjValueFromString(String key, Object val) {
			if(key.equals("id")) {
				this.id = ((Integer)val).intValue();
			} else if(key.equals("group_name")) {
				this.group_name = (String)val;
			} else if(key.equals("days")) {
				this.days = (String)val;
			} else if(key.equals("timings")) {
				this.timings = (String)val;
			} else if(key.equals("time_updated")) {
				this.time_updated = (String)val;
			} else if(key.equals("village_id")) {
				VillagesData village = new VillagesData();
				this.village = village.getNewData();
				this.village.id = ((Integer)val).intValue();
			}
		}
		
		@Override
		public void save() {
			AnimatorsData animatorsDataDbApis = new AnimatorsData();
			this.id = animatorsDataDbApis.autoInsert(this.group_name, 
					this.days, 
					this.timings,
					this.time_updated, 
					Integer.valueOf(this.village.getId()).toString());
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
	
	protected static String savePersonGroupOfflineURL = "/dashboard/savepersongroupoffline/";
	
	public PersonGroupsData() {
		super();
	}
	
	@Override
	public Data getNewData() {
		return new Data();
	}
	
	@Override
	protected String getTableId() {
		return PersonGroupsData.tableID;
	}
}
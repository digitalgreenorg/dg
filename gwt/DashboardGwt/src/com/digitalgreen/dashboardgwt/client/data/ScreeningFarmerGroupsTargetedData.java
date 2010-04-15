package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.ScreeningFarmerGroupsTargetedData.Data;
import com.digitalgreen.dashboardgwt.client.data.ScreeningFarmerGroupsTargetedData.Type;
import com.google.gwt.core.client.JsArray;

public class ScreeningFarmerGroupsTargetedData extends BaseData {
	
	public static class Type extends BaseData.Type{
		protected Type(){}
		
		public final native String getScreening() /*-{ return this.fields.screening;}-*/;
		public final native String getPersonGroup() /*-{ return this.fields.persongroups;}-*/;		
	}
	
	public class Data extends BaseData.Data {
		final private static String COLLECTION_PREFIX = "screeningfarmergroupstargeted";
		
		private ScreeningsData.Data screening;// FK to the Screenings table
		private PersonGroupsData.Data group;
				
		public Data() {
			super();
		}
		
		public Data(String id, ScreeningsData.Data screening, PersonGroupsData.Data group) {
			this.id = id;
			this.screening = screening;
			this.group = group;
			}
		
		public Data(String id, PersonGroupsData.Data group){
			super();
			this.id = id;
			this.group = group;
		}
			
		public ScreeningsData.Data getScreening(){
			return this.screening;
		}
		
		public PersonGroupsData.Data getPersonGroup(){
			return this.group;
		}
		
		public BaseData.Data clone(){
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
			if(key.equals("screening")) {
				ScreeningsData screening = new ScreeningsData();
				this.screening = screening.getNewData();
				this.screening.id = val;
				
			} else if(key.equals("group")) {
				PersonGroupsData group = new PersonGroupsData();
				this.group = group.getNewData();
				this.group.id = val;
			} else {
				return;
			}
			this.addNameValueToQueryString(key, val);
		}
	

		@Override		
		public void save() {
			ScreeningFarmerGroupsTargetedData screeningFarmerGroupsTargetedsDataDbApis = new ScreeningFarmerGroupsTargetedData();
			this.id = screeningFarmerGroupsTargetedsDataDbApis.autoInsert(this.id,
					this.screening.getId(),
					this.group.getId());
			this.addNameValueToQueryString("id", this.id);
		}
		
		@Override
		public String getTableId() {
			ScreeningFarmerGroupsTargetedData screeningFarmerGroupsTargetedsDataDbApis = new ScreeningFarmerGroupsTargetedData();
			return screeningFarmerGroupsTargetedsDataDbApis.tableID;
		}
	}
	
	
	protected static String tableID = "26";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `screening_farmer_groups_targeted` " +
												"(id INTEGER PRIMARY KEY  NOT NULL ," +
												"screening_id INT  NOT NULL DEFAULT 0," +
												"persongroups_id INT  NOT NULL DEFAULT 0, " +
												"FOREIGN KEY(screening_id) REFERENCES screening(id), " +
												"FOREIGN KEY(persongroups_id) REFERENCES person_groups(id));" ;
	
	protected static String selectScreeningFarmerGroupsTargeted = "SELECT id FROM screening_farmer_groups_targeted ORDER BY (id);";
	protected static String listScreeningFarmerGroupsTargeted = "SELECT sfgt.id, pg.group_name FROM screening_farmer_groups_targeted sfgt" +
			",person_group pg WHERE sfgt.persongroups_id = pg.id ORDER BY (sfgt.id);";
	protected static String saveScreeningFarmerGroupsTargetedOfflineURL = "/dashboard/savescreeningfarmergroupstargetedoffline/";
	protected static String saveScreeningFarmerGroupsTargetedOnlineURL = "/dashboard/savescreeningfarmergroupstargetedonline/";
	protected static String getScreeningFarmerGroupsTargetedOnlineURL = "/dashboard/getscreeningfarmergroupstargetedsonline/";
	protected String table_name = "screening_farmer_groups_targeted";
	protected String[] fields = {"id", "screening_id","persongroups_id"};
		
	public ScreeningFarmerGroupsTargetedData() {
		super();
	}
	public ScreeningFarmerGroupsTargetedData(OnlineOfflineCallbacks callbacks) {
		super(callbacks);
	}
	
	public ScreeningFarmerGroupsTargetedData(OnlineOfflineCallbacks callbacks, Form form) {
		super(callbacks, form);
	}
	@Override
	public Data getNewData() {
		return new Data();
	}
	@Override
	protected String getTableId(){
		return ScreeningFarmerGroupsTargetedData.tableID;
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
		return ScreeningFarmerGroupsTargetedData.getScreeningFarmerGroupsTargetedOnlineURL;
	}

	@Override
	public String getSaveOfflineURL(){
		return ScreeningFarmerGroupsTargetedData.saveScreeningFarmerGroupsTargetedOfflineURL;
	}
	
	public final native JsArray<Type> asArrayOfData(String json) /*-{
		return eval(json);
	}-*/;
	
	public List serialize(JsArray<Type> screeningFarmerGroupsTargetedObjects){
		List screeningFarmerGroupsTargeteds = new ArrayList();
		ScreeningsData screening = new ScreeningsData();
		PersonGroupsData group = new PersonGroupsData();
		for(int i = 0; i < screeningFarmerGroupsTargetedObjects.length(); i++){
			ScreeningsData.Data sc = screening.new Data(screeningFarmerGroupsTargetedObjects.get(i).getScreening());
			PersonGroupsData.Data pg = group.new Data(screeningFarmerGroupsTargetedObjects.get(i).getPersonGroup());
			
			Data screeningFarmerGroupsTargeted = new Data(screeningFarmerGroupsTargetedObjects.get(i).getPk(),sc,pg);
			screeningFarmerGroupsTargeteds.add(screeningFarmerGroupsTargeted);
		}
		
		return screeningFarmerGroupsTargeteds;
	}
	
	@Override
	public List getListingOnline(String json){
		return this.serialize(this.asArrayOfData(json));		
	}
	
}

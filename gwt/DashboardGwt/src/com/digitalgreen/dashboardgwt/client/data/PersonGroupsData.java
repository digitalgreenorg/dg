package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Date;
import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.PersonGroupsData.Type;
import com.digitalgreen.dashboardgwt.client.data.VillagesData.Data;
import com.google.gwt.core.client.JsArray;
import com.google.gwt.gears.client.database.DatabaseException;
import com.google.gwt.user.client.Window;


public class PersonGroupsData extends BaseData {

	public static class Type extends BaseData.Type{
		protected Type() {}
		public final native String getPersonGroupName() /*-{ return $wnd.checkForNullValues(this.fields.group_name); }-*/;
		public final native String getDays() /*-{ return $wnd.checkForNullValues(this.fields.days); }-*/;
		public final native String getTimings() /*-{ return $wnd.checkForNullValues(this.fields.timings); }-*/;
		public final native String getTimeUpdated() /*-{ return $wnd.checkForNullValues(this.fields.time_updated); }-*/;
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
		
		public Data(String id){
			super();
			this.id = id;
		}
		
		public Data(String id, String group_name){
			super();
			this.id = id;
			this.group_name = group_name;
		}
		
		public Data(String id, String group_name, VillagesData.Data village){
			super();
			this.id = id;
			this.group_name = group_name;
			this.village = village;
		}
		
		public Data(String id, String group_name, String days, String timings,String time_updated, VillagesData.Data village){
			super();
			this.id = id;
			this.group_name = group_name;
			this.days = days;
			this.timings = timings;
			this.time_updated = time_updated;
			this.village = village;
		}
		
		public String getPersonGroupName(){
			return this.group_name;
		}
		
		public String getTimings(){
			return this.timings;
		}
		
		public String getTimeUpdated(){
			return this.time_updated;
		}
		
		public VillagesData.Data getVillage(){
			return this.village;
		}		
		
		@Override
		public BaseData.Data clone() {
			Data obj = new Data();
			obj.village = (new VillagesData()).new Data();
			return obj;
		}
	
		@Override
		public String getPrefixName() {
			return Data.COLLECTION_PREFIX;
		}
		
		@Override
		public void setObjValueFromString(String key, String val) {
			super.setObjValueFromString(key, val);
			if(key.equals("group_name")) {
				this.group_name = val;
			} else if(key.equals("days")) {
				this.days = val;
			} else if(key.equals("timings")) {
				this.timings = val;
			} else if(key.equals("time_updated")) {
				this.time_updated = (String)val;
			} else if(key.equals("village")) {
				VillagesData village = new VillagesData();
				this.village = village.getNewData();
				this.village.id = val;
			}else {
				return;
			}
			this.addNameValueToQueryString(key, val);
		}
		
		@Override
		public void save() {
			PersonGroupsData personGroupsDataDbApis = new PersonGroupsData();
			Date date = new Date();
			this.time_updated = date.getYear() + "-" + date.getMonth() +"-" + date.getDate() + " " + 
								date.getHours() + ":" + date.getMinutes() + ":" + date.getSeconds();
			this.id = personGroupsDataDbApis.autoInsert(this.id,
						this.group_name, 
						this.days, 
						this.timings,
						this.time_updated, 
						this.village.getId());
			this.addNameValueToQueryString("id", this.id);
		}
		
		@Override
		public void save(BaseData.Data foreignKey) {
			PersonGroupsData personGroupsDataDbApis = new PersonGroupsData();
			Date date = new Date();
			this.time_updated = date.getYear() + "-" + date.getMonth() +"-" + date.getDate() + " " + 
								date.getHours() + ":" + date.getMinutes() + ":" + date.getSeconds();
			this.id = personGroupsDataDbApis.autoInsert(this.id, 
					this.group_name, 
					this.days, 
					this.timings,
					this.time_updated, 
					foreignKey.getId());
			this.addNameValueToQueryString("id", this.id);
			this.addNameValueToQueryString("village", foreignKey.getId());
		}
		
		@Override
		public String getTableId() {
			PersonGroupsData personGroupsDataDbApis = new PersonGroupsData();
			return personGroupsDataDbApis.tableID;
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
	protected static String listPersonGroups = "SELECT pg.id,pg.GROUP_NAME, vil.id,vil.village_name FROM person_groups pg " +
			"JOIN village vil ON pg.village_id = vil.id ORDER BY (-pg.id);";
	protected static String savePersonGroupOfflineURL = "/dashboard/savepersongroupoffline/";
	protected static String savePersonGroupOnlineURL = "/dashboard/savepersongrouponline/";
	protected static String getPersonGroupOnlineURL = "/dashboard/getpersongroupsonline/";
	protected String table_name = "person_groups";
	protected String[] fields = {"id", "group_name","days", "timings", "time_updated", "village_id"};
		
	public PersonGroupsData() {
		super();
	}
	
	public PersonGroupsData(OnlineOfflineCallbacks callbacks) {
		super(callbacks);
	}
	
	public PersonGroupsData(OnlineOfflineCallbacks callbacks, Form form) {
		super(callbacks, form);
	}
	@Override
	public Data getNewData() {
		return new Data();
	}
	
	@Override
	protected String getTableId() {
		return PersonGroupsData.tableID;
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
		
	@Override
	public String getSaveOfflineURL(){
		return PersonGroupsData.savePersonGroupOfflineURL;
	}
	
	public final native JsArray<Type> asArrayOfData(String json) /*-{
		return eval(json);
	}-*/;
	
	public List serialize(JsArray<Type> personGroupObjects){
		List personGroups = new ArrayList();
		VillagesData village = new VillagesData();
		for(int i = 0; i < personGroupObjects.length(); i++){
			VillagesData.Data vil = village.new Data(personGroupObjects.get(i).getVillage().getPk(),
					personGroupObjects.get(i).getVillage().getVillageName());
						
			Data personGroup = new Data(personGroupObjects.get(i).getPk(),
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
	
	
	public List getPersonGroupsListingOffline(){
		BaseData.dbOpen();
		List personGroups = new ArrayList();
		VillagesData village = new VillagesData();
		this.select(listPersonGroups);
		if (this.getResultSet().isValidRow()){
			try {
				for (int i = 0; this.getResultSet().isValidRow(); ++i, this.getResultSet().next()) {
					VillagesData.Data v = village.new Data(this.getResultSet().getFieldAsString(2),  this.getResultSet().getFieldAsString(3)) ;
					Data personGroup = new Data(this.getResultSet().getFieldAsString(0), this.getResultSet().getFieldAsString(1),v);
					personGroups.add(personGroup);
	    	      }				
			} catch (DatabaseException e) {
				Window.alert("Database Exception  : " + e.toString());
				// TODO Auto-generated catch block
				BaseData.dbClose();
			}
			
		}
		BaseData.dbClose();
		return personGroups;
	}
	
	public List getAllPersonGroupsOffline(){
		BaseData.dbOpen();
		List personGroups = new ArrayList();
		this.select(selectPersonGroups);
		if (this.getResultSet().isValidRow()){
			try {
				for (int i = 0; this.getResultSet().isValidRow(); ++i, this.getResultSet().next()) {
					Data personGroup = new Data(this.getResultSet().getFieldAsString(0), this.getResultSet().getFieldAsString(1));
					personGroups.add(personGroup);
	    	      }				
			} catch (DatabaseException e) {
				Window.alert("Database Exception : " + e.toString());
				// TODO Auto-generated catch block
				BaseData.dbClose();
			}
			
		}
		BaseData.dbClose();
		return personGroups;
	}
	
	
	public Object postPageData() {
		if(BaseData.isOnline()){
			this.post(RequestContext.SERVER_HOST + PersonGroupsData.savePersonGroupOnlineURL, this.form.getQueryString());
		}
		else{
			this.save();
			return true;
		}
		
		return false;
	}
	
	public Object getListPageData(){
		if(BaseData.isOnline()){
			this.get(RequestContext.SERVER_HOST + PersonGroupsData.getPersonGroupOnlineURL);
		}
		else{
			return true;
		}
		return false;
	}	
	
	public String retrieveDataAndConvertResultIntoHtml(){
		VillagesData villageData = new VillagesData();
		List villages = villageData.getAllVillagesOffline();
		VillagesData.Data village;
		String html = "<select name=\"village\" id=\"id_village\">" 
			+ "<option selected='selected' value=''>---------</option>";
		for(int i=0; i< villages.size(); i++){
			village = (VillagesData.Data)villages.get(i);
			html = html + "<option value = \"" + village.getId() +"\">" + village.getVillageName() + "</option>";
		}
		html = html + "</select>";
		
		VillagesData villageData1 = new VillagesData();
		List villages1 = villageData.getAllVillagesOffline();
		VillagesData.Data village1;
		for(int inline = 0; inline < 30; inline++){
			html += "<select name=\"person_set-" + inline + "-village\" id=\"id_person_set-" + inline +"-village\">"+
			"<option selected='selected' value=''>---------</option>";
			for(int i=0; i< villages1.size(); i++){
				village1 = (VillagesData.Data)villages1.get(i);
				html = html + "<option value = \"" + village1.getId() +"\">" + village1.getVillageName() + "</option>";
			}
			html = html + "</select>";
		}
		
		return html;
	}
	
	public Object getAddPageData(){
		if(BaseData.isOnline()){
			this.get(RequestContext.SERVER_HOST + PersonGroupsData.savePersonGroupOnlineURL);
		}
		else{
			return retrieveDataAndConvertResultIntoHtml();
		}
		return false;
	}
	
}
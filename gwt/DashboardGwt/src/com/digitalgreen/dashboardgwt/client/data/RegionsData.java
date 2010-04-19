package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.validation.DateValidator;
import com.digitalgreen.dashboardgwt.client.data.validation.StringValidator;
import com.google.gwt.core.client.JsArray;
import com.google.gwt.gears.client.database.DatabaseException;
import com.google.gwt.user.client.Window;

public class RegionsData extends BaseData {
	
	public static class Type extends BaseData.Type{
		protected Type() {}
		public final native String getRegionName() /*-{ return $wnd.checkForNullValues(this.fields.region_name); }-*/;
		public final native String getStartDate() /*-{ return $wnd.checkForNullValues(this.fields.start_date);  }-*/;
	}

	public class Data extends BaseData.Data {
		
		final private static String COLLECTION_PREFIX = "region";
			
		private String region_name;
		private String start_date;
		
		public Data() {
			super();
		}
		
		public Data(String id, String region_name){
			super();
			this.id = id;
			this.region_name = region_name;
		}
		
		public Data(String id, String region_name, String start_date) {
			super();
			this.id = id;
			this.region_name = region_name;
			this.start_date = start_date;
		}
		
		public String getRegionName(){
			return this.region_name;
		}
		
		public String getStartDate(){
			return this.start_date;
		}
		
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
			if(key.equals("region_name")) {
				this.region_name = (String)val;
			} else if(key.equals("start_date")) {
				this.start_date = (String)val;
			} else {
				return;
			}
			this.addNameValueToQueryString(key, val);			
		}
		
		@Override
		public boolean validate(){
			StringValidator stringValidator = new StringValidator(this.region_name,false,false,0,50);
			DateValidator dateValidator = new DateValidator(this.start_date, true, true);
			return stringValidator.validate() && dateValidator.validate();
		}
		
		@Override
		public void save() {
			RegionsData regionsDataDbApis = new RegionsData();
			this.id = regionsDataDbApis.autoInsert(this.id,
					this.region_name, 
					this.start_date);
			this.addNameValueToQueryString("id", this.id);
		}		
		
		@Override
		public String getTableId() {
			RegionsData regionsDataDbApis = new RegionsData();
			return regionsDataDbApis.tableID;
		}
	}

	public static String tableID = "8";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `region` " +
												"(id INTEGER PRIMARY KEY NOT NULL," +
												"REGION_NAME VARCHAR(100) NOT NULL," +
												"START_DATE DATE NULL DEFAULT NULL);";
	protected static String dropTable = "DROP TABLE IF EXISTS `region`;";
	protected static String selectRegions = "SELECT id, region_name FROM region ORDER BY(region_name)";
	protected static String listRegions = "SELECT * FROM region ORDER BY(-id)";
	protected static String saveRegionOnlineURL = "/dashboard/saveregiononline/";
	protected static String getRegionOnlineURL = "/dashboard/getregionsonline/";
	protected static String saveRegionOfflineURL = "/dashboard/saveregionoffline/";
	protected String table_name = "region";
	protected String[] fields = {"id", "region_name", "start_date"};
	
	public RegionsData() {
		super();
	}
	
	public RegionsData(OnlineOfflineCallbacks callbacks) {
		super(callbacks);
	}
	
	public RegionsData(OnlineOfflineCallbacks callbacks, Form form) {
		super(callbacks, form);
	}

	@Override
	public Data getNewData() {
		return new Data();
	}
	
	@Override
	protected  String getTableId() {
		return RegionsData.tableID;
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
	protected String getCreateTableSql(){
		return this.createTable;
	}
	
	@Override
	protected String getDeleteTableSql(){
		return this.dropTable;
	}
	
	@Override
	public String getListingOnlineURL(){
		return RegionsData.getRegionOnlineURL;
	}
	
	@Override
	public String getSaveOfflineURL(){
		return RegionsData.saveRegionOfflineURL;
	}


	public final native JsArray<Type> asArrayOfData(String json) /*-{
		return eval(json);
	}-*/;
	
	
	public List serialize(JsArray<Type> regionObjects){
		List regions = new ArrayList();
		for(int i = 0; i < regionObjects.length(); i++){
			Data region = new Data(regionObjects.get(i).getPk(), regionObjects.get(i).getRegionName(), regionObjects.get(i).getStartDate());
			regions.add(region);
		}
		
		return regions;
	}
	
	@Override
	public List getListingOnline(String json){
		return this.serialize(this.asArrayOfData(json));		
	}
	
	public List getRegionsListingOffline(){
		BaseData.dbOpen();
		List regions = new ArrayList();
		this.select(listRegions);
		if (this.getResultSet().isValidRow()){
			try {
				for (int i = 0; this.getResultSet().isValidRow(); ++i, this.getResultSet().next()) {
					Data region = new Data(this.getResultSet().getFieldAsString(0), this.getResultSet().getFieldAsString(1), this.getResultSet().getFieldAsString(2));
					regions.add(region);
	    	      }				
			} catch (DatabaseException e) {
				Window.alert("Database Exception : " + e.toString());
				BaseData.dbClose();
			}
			
		}
		BaseData.dbClose();
		return regions;
	}

	public List getAllRegionsOffline(){
		BaseData.dbOpen();
		List regions = new ArrayList();
		this.select(selectRegions);
		if (this.getResultSet().isValidRow()){
			try {
				for (int i = 0; this.getResultSet().isValidRow(); ++i, this.getResultSet().next()) {
					Data region = new Data(this.getResultSet().getFieldAsString(0), this.getResultSet().getFieldAsString(1));
					regions.add(region);
	    	      }				
			} catch (DatabaseException e) {
				Window.alert("Database Exception : " + e.toString());
				BaseData.dbClose();
			}
			
		}
		BaseData.dbClose();
		return regions;
	}
	
	public Object postPageData() {
		if(BaseData.isOnline()){
			this.post(RequestContext.SERVER_HOST + RegionsData.saveRegionOnlineURL, this.form.getQueryString());
		}
		else{
			if(this.validate()){
				this.save();
				return true;
			}
		}
		
		return false;
	}
	
	public Object getPageData(){
		if(BaseData.isOnline()){
			this.get(RequestContext.SERVER_HOST + RegionsData.getRegionOnlineURL);
		}
		else{
			return true;
		}
		return false;
	}
	

}
package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.google.gwt.gears.client.database.DatabaseException;
import com.google.gwt.user.client.Window;

public class RegionsData extends BaseData {

	public class Data extends BaseData.Data {
		
		final private static String COLLECTION_PREFIX = "region";
			
		private String region_name;
		private String start_date;
		
		public Data(int id, String region_name, String start_date) {
			this.id = id;
			this.region_name = region_name;
			this.start_date = start_date;
		}
		
		public Object clone() {
			Data obj = (Data)super.clone();
			obj.region_name = this.region_name;
			obj.start_date = this.start_date;
			return obj;
		}

		@Override
		public String getPrefixName() {
			return Data.COLLECTION_PREFIX;
		}
		
		@Override
		public void setObjValueFromString(String key, Object val) {
			if(key.equals("id")) {
				this.id = ((Integer)val).intValue();
			} else if(key.equals("region_name")) {
				this.region_name = (String)val;
			} else if(key.equals("start_date")) {
				this.start_date = (String)val;
			}			
		}
		
		@Override
		public String[] getFormInsertValues() {
			return new String[]{this.region_name, this.start_date};
		}
	}

	protected static String tableID = "01";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `region` " +
												"(id INTEGER PRIMARY KEY NOT NULL," +
												"REGION_NAME VARCHAR(100) NOT NULL," +
												"START_DATE DATE NULL DEFAULT NULL);";  
	protected static String insertSql = "INSERT INTO region VALUES (?, ?, ?);";
	protected static String listRegions = "SELECT id, REGION_NAME FROM region ORDER BY(-id)";
	protected static String postURL = "/dashboard/saveregion/";
	protected String table_name = "region";
	protected String[] fields = {"region_name", "start_date"};
	
	public RegionsData() {
		super();
	}
	
	public RegionsData(OnlineOfflineCallbacks callbacks) {
		super(callbacks);
	}
	
	public void createRegion(String queryArg){
		HashMap form = Form.flatten(queryArg);
		String id = this.getNextRowId();
		this.insert(insertSql, id, (String)form.get("region_name"), (String)form.get("start_date") );
		FormQueueData formQueue = new FormQueueData();
		formQueue.saveQueryString(tableID, id, queryArg, "0", "A");
		this.updateLastInsertedID();
	}
	
	public List getRegions(){
		BaseData.dbOpen();
		List regions= new ArrayList();
		this.select(listRegions);
		if (this.getResultSet().isValidRow()){
			try {
				for (int i = 0; this.getResultSet().isValidRow(); ++i, this.getResultSet().next()) {
					ArrayList region = new ArrayList();
					region.add(this.getResultSet().getFieldAsInt(0));
					region.add(this.getResultSet().getFieldAsString(1));
					regions.add(region);
	    	      }				
			} catch (DatabaseException e) {
				Window.alert("Database Exception : " + e.toString());
				// TODO Auto-generated catch block
				BaseData.dbClose();
			}
			
		}else{
			Window.alert("No rows returned");
			
		}
		BaseData.dbClose();
		return regions;
	}
	
	public Object postPageData(String queryArg) {
		if(this.isOnline()){
			this.post(RequestContext.SERVER_HOST + this.postURL, queryArg);
		}
		else{
			this.createRegion(queryArg);
			return true;
		}
		
		return false;
	}
	

}
package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.validation.StringValidator;

import com.google.gwt.core.client.JsArray;
import com.google.gwt.gears.client.database.DatabaseException;
import com.google.gwt.user.client.Window;

public class PracticesData extends BaseData {
	
	public static class Type extends BaseData.Type{
		protected Type(){}
		public final native String getPracticeName() /*-{ return $wnd.checkForNullValues(this.fields.practice_name); }-*/;
		public final native String getSeasonality()/*-{ return $wnd.checkForNullValues(this.fields.seasonality); }-*/;
		public final native String getSummary() /*-{ return $wnd.checkForNullValues(this.fields.summary); }-*/;
	}
	
	public class Data extends BaseData.Data {
		
		final private static String COLLECTION_PREFIX = "practice";
		
		private String practice_name;
		private String seasonality;
		private String summary;
		
		public Data(){
			super();
		}
		
		public Data(String id){
			super();
			this.id = id;
		}
		
		public Data(String id, String practice_name){
			super();
			this.id = id;
			this.practice_name = practice_name;
		}
		
		public Data(String id, String practice_name, String seasonality, String summary){
			super();
			this.id = id;
			this.practice_name = practice_name;
			this.seasonality = seasonality;
			this.summary = summary;
		}
		
		public String getPracticeName(){
			return this.practice_name;
		}
		
		public String getSeasonality(){
			return this.seasonality;
		}
		
		public String getSummary(){
			return this.summary;
		}
		
		@Override
		public BaseData.Data clone(){
			Data obj = new Data();
			return obj;
		}
		
		@Override
		public String getPrefixName(){
			return Data.COLLECTION_PREFIX;
		}
		
		@Override
		public void setObjValueFromString(String key, String val){
			super.setObjValueFromString(key, val);
			if(key.equals("practice_name")){
				this.practice_name = (String)val;
			}
			else if(key.equals("seasonality")){
				this.seasonality = (String)val;
			}
			else if(key.equals("summary")){
				this.summary = (String)val;
			}
			else {
				return;
			}
			this.addNameValueToQueryString(key, val);
		}
		
		@Override
		public boolean validate(){
			StringValidator nameValidator = new StringValidator(this.practice_name, false, false, 1, 200);
			nameValidator.setError("Please make sure 'Name' NOT EMPTY and is less than 100 CHARACTERS.");
			StringValidator seasonalityValidator = new StringValidator(this.seasonality, false, false, 3, 3);
			seasonalityValidator.setError("Please make sure you choose a Season for 'Seasonality'.");
			StringValidator summaryValidator = new StringValidator(this.summary, true, false, 0, 1024);
			summaryValidator.setError("Please make sure 'Summary' is less than 1024 CHARACTERS.");
			ArrayList validatorList = new ArrayList();
			validatorList.add(nameValidator);
			validatorList.add(seasonalityValidator);
			validatorList.add(summaryValidator);
			return this.executeValidators(validatorList);
		}
		
		@Override
		public void save(){
			PracticesData practicesDataDbApis = new PracticesData();
			this.id = practicesDataDbApis.autoInsert(this.id, 
					this.practice_name, 
					this.seasonality, 
					this.summary);
			this.addNameValueToQueryString("id", this.id);
		}
		
		@Override
		public String getTableId() {
			PracticesData practicesDataDbApis = new PracticesData();
			return practicesDataDbApis.tableID;
		}
	}
	
	public static String tableID = "28";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `practices` " +
												"(id INTEGER PRIMARY KEY  NOT NULL ," +
												"PRACTICE_NAME VARCHAR(200)  NOT NULL ," +
												"SEASONALITY VARCHAR(3)  NOT NULL ," +
												"SUMMARY TEXT NULL DEFAULT NULL );";
	protected static String dropTable = "DROP TABLE IF EXISTS `practices`;";
	protected static String selectPractices = "SELECT id, practice_name FROM practices ORDER BY(practice_name)";
	protected static String listPractices = "SELECT * FROM practices ORDER BY(-id)";
	protected static String savePracticeOnlineURL = "/dashboard/savepracticeonline/";
	protected static String getPracticeOnlineURL = "/dashboard/getpracticesonline/";
	protected static String savePracticeOfflineURL = "/dashboard/savepracticeoffline/";
	protected String table_name = "practices";
	protected String[] fields = {"id", "practice_name", "seasonality", "summary"};
	
	public PracticesData(){
		super();
	}
	
	public PracticesData(OnlineOfflineCallbacks callbacks) {
		super(callbacks);
	}
	
	public PracticesData(OnlineOfflineCallbacks callbacks, Form form){
		super(callbacks, form);
	}
	
	@Override
	public Data getNewData(){
		return new Data();
	}
	
	@Override
	protected String getTableId(){
		return PracticesData.tableID;
	}
	
	@Override
	protected String getTableName(){
		return this.table_name;
	}
	
	@Override
	protected String[] getFields(){
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
		return PracticesData.getPracticeOnlineURL;
	}
	
	@Override
	public String getSaveOfflineURL(){
		return PracticesData.savePracticeOfflineURL;
	}
	
	public final native JsArray<Type> asArrayOfData(String json) /*-{
		return eval(json);
	}-*/;
	
	public List serialize(JsArray<Type> practiceObjects){
		List practices = new ArrayList();
		for(int i = 0; i < practiceObjects.length(); i++){
			Data practice = new Data(practiceObjects.get(i).getPk(), practiceObjects.get(i).getPracticeName(), 
					practiceObjects.get(i).getSeasonality(), practiceObjects.get(i).getSummary());
			practices.add(practice);
		}
		return practices;
	}
	
	@Override
	public List getListingOnline(String json){
		return this.serialize(this.asArrayOfData(json));
	}
	
	public List getPracticesListingOffline(){
		BaseData.dbOpen();
		List practices = new ArrayList();
		this.select(listPractices);
		if(this.getResultSet().isValidRow()){
			try {
				for(int i = 0; this.getResultSet().isValidRow(); ++i, this.getResultSet().next()){
					Data practice = new Data(this.getResultSet().getFieldAsString(0), this.getResultSet().getFieldAsString(1), 
							this.getResultSet().getFieldAsString(2), this.getResultSet().getFieldAsString(3));
					practices.add(practice);
				}
			}
			catch(DatabaseException e){
				Window.alert("Database Exception : " + e.toString());
				BaseData.dbClose();
			}
		}
		BaseData.dbClose();
		return practices;
	}
	
	public List getAllPracticesOffline(){
		BaseData.dbOpen();
		List practices = new ArrayList();
		this.select(selectPractices);
		if(this.getResultSet().isValidRow()){
			try {
				for(int i = 0; this.getResultSet().isValidRow(); ++i, this.getResultSet().next()){
					Data practice = new Data(this.getResultSet().getFieldAsString(0), this.getResultSet().getFieldAsString(1));
					practices.add(practice);
				}
			}
			catch(DatabaseException e){
				Window.alert("Database Exception : " + e.toString());
				BaseData.dbClose();
			}
		}
		BaseData.dbClose();
		return practices;
	}
	
	
	public Object postPageData(){
		if(BaseData.isOnline()){
			this.post(RequestContext.SERVER_HOST + this.savePracticeOnlineURL, this.form.getQueryString());
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
			this.get(RequestContext.SERVER_HOST + PracticesData.getPracticeOnlineURL);
		}
		else {
			return true;
		}
		return false;
	}
}
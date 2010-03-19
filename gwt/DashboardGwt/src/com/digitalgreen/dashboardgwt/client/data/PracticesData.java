package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;

import com.google.gwt.core.client.JsArray;
import com.google.gwt.gears.client.database.DatabaseException;
import com.google.gwt.user.client.Window;

public class PracticesData extends BaseData {
	
	public static class Type extends BaseData.Type{
		protected Type(){}
		public final native String getPracticeName() /*-{ return this.fields.practice_name; }-*/;
		public final native String getSeasonality()/*-{ return this.fields.seasonality; }-*/;
		public final native String getSummary() /*-{ return this.fields.summary; }-*/;
	}
	
	public class Data extends BaseData.Data {
		
		final private static String COLLECTION_PREFIX = "practices";
		
		private String practice_name;
		private String seasonality;
		private String summary;
		
		public Data(){
			super();
		}
		
		public Data(int id, String practice_name, String seasonality, String summary){
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
		public Object clone(){
			Data obj = new Data();
			obj.id = this.id;
			obj.practice_name = this.practice_name;
			obj.seasonality = this.seasonality;
			obj.summary = this.summary;
			return obj;
		}
		
		@Override
		public String getPrefixName(){
			return Data.COLLECTION_PREFIX;
		}
		
		@Override
		public void setObjValueFromString(String key, Object val){
			if(key.equals("id")){
				this.id = ((Integer)val).intValue();
			}
			else if(key.equals("practice_name")){
				this.practice_name = (String)val;
			}
			else if(key.equals("seasonality")){
				this.seasonality = (String)val;
			}
			else if(key.equals("summary")){
				this.summary = (String)val;
			}
		}
		
		@Override
		public void save(){
			PracticesData practicesDataDbApis = new PracticesData();
			this.id = practicesDataDbApis.autoInsert(this.practice_name, this.seasonality, this.summary);
		}
	}
	
	protected static String tableID = "21";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `practices` " +
												"(id INTEGER PRIMARY KEY  NOT NULL ," +
												"PRACTICE_NAME VARCHAR(200)  NOT NULL ," +
												"SEASONALITY VARCHAR(3)  NOT NULL ," +
												"SUMMARY TEXT NULL DEFAULT NULL );";  
	protected static String listPractices = "SELECT * FROM practices ORDER BY(-id)";
	protected static String savePracticeURL = "/dashboard/savepractice/";
	protected static String getPracticeURL = "/dashboard/getpractices/";
	protected String table_name = "practices";
	protected String[] fields = {"id", "practice_name", "seasonality", "summary"};
	
	public PracticesData(){
		super();
	}
	
	public PracticesData(OnlineOfflineCallbacks callbacks) {
		super(callbacks);
	}
	
	public PracticesData(OnlineOfflineCallbacks callbacks, Form form, String queryString){
		super(callbacks, form, queryString);
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
	
	public final native JsArray<Type> asArrayOfData(String json) /*-{
		return eval(json);
	}-*/;
	
	public List serialize(JsArray<Type> practiceObjects){
		List practices = new ArrayList();
		for(int i = 0; i < practiceObjects.length(); i++){
			Data practice = new Data(Integer.parseInt(practiceObjects.get(i).getPk()), practiceObjects.get(i).getPracticeName(), 
					practiceObjects.get(i).getSeasonality(), practiceObjects.get(i).getSummary());
			practices.add(practice);
		}
		return practices;
	}
	
	public List getPractices(String json){
		return this.serialize(this.asArrayOfData(json));
	}
	
	public List getPractices(){
		BaseData.dbOpen();
		List practices = new ArrayList();
		this.select(listPractices);
		if(this.getResultSet().isValidRow()){
			try {
				for(int i = 0; this.getResultSet().isValidRow(); ++i, this.getResultSet().next()){
					Data practice = new Data(this.getResultSet().getFieldAsInt(0), this.getResultSet().getFieldAsString(1), 
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
	
	public Object postPageData(){
		if(BaseData.isOnline()){
			this.post(RequestContext.SERVER_HOST + this.savePracticeURL, this.queryString);
		}
		else{
			this.save();
			return true;
		}
		return false;
	}
	
	public Object getPageData(){
		if(BaseData.isOnline()){
			this.get(RequestContext.SERVER_HOST + PracticesData.getPracticeURL);
		}
		else {
			return true;
		}
		return false;
	}
}
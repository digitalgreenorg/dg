package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.google.gwt.core.client.JsArray;
import com.google.gwt.gears.client.database.DatabaseException;
import com.google.gwt.user.client.Window;

public class LanguagesData extends BaseData {

	public static class Type extends BaseData.Type{
		protected Type() {}
		public final native String getLanguageName() /*-{ return this.fields.language_name; }-*/;
	}

	public class Data extends BaseData.Data {
		
		final private static String COLLECTION_PREFIX = "language";
			
		private String language_name;
		
		public Data() {
			super();
		}
		
		public Data(int id, String language_name) {
			super();
			this.id = id;
			this.language_name = language_name;
		}
		
		public String getLanguageName(){
			return this.language_name;
		}
		
		public BaseData.Data clone() {
			Data obj = new Data();
			obj.id = this.id;
			obj.language_name = this.language_name;
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
			} else if(key.equals("language_name")) {
				this.language_name = (String)val;
			}			
		}
		
		@Override
		public void save() {
			LanguagesData languagesDataDbApis = new LanguagesData();
			this.id = languagesDataDbApis.autoInsert(this.language_name);
		}
	}
	
	protected static String tableID = "20";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `language` " +
											"(id INTEGER PRIMARY KEY  NOT NULL ," +
											"language_name VARCHAR(100)  NOT NULL );";  
	protected static String selectLanguages = "SELECT * FROM language ORDER BY(language_name);";
	protected static String listLanguages = "SELECT * FROM language ORDER BY(-id)";
	protected static String saveLanguageOnlineURL = "/dashboard/savelanguageonline/";
	protected static String getLanguageOnlineURL = "/dashboard/getlanguagesonline/";
	protected static String saveLanguageOfflineURL = "/dashboard/savelanguageoffline/";
	protected String table_name = "language";
	protected String[] fields = {"id", "language_name"};
	
	public LanguagesData() {
		super();
	}
	
	public LanguagesData(OnlineOfflineCallbacks callbacks) {
		super(callbacks);
	}
	
	public LanguagesData(OnlineOfflineCallbacks callbacks, Form form, String queryString) {
		super(callbacks, form, queryString);
	}
	
	@Override
	public Data getNewData() {
		return new Data();
	}
	
	@Override
	protected String getTableId() {
		return LanguagesData.tableID;
	}
	
	protected String getTableName() {
		return this.table_name;
	}
	
	protected String[] getFields() {
		return this.fields;
	}
	
	protected static String getSaveOfflineURL(){
		return LanguagesData.saveLanguageOfflineURL;
	}
	
	
	public final native JsArray<Type> asArrayOfData(String json) /*-{
		return eval(json);
	}-*/;
	
	public List serialize(JsArray<Type> languageObjects){
		List languages = new ArrayList();
		for(int i = 0; i < languageObjects.length(); i++){
			Data language = new Data(Integer.parseInt(languageObjects.get(i).getPk()), languageObjects.get(i).getLanguageName());
			languages.add(language);
		}
		
		return languages;
	}
	
	public List getLanguagesListingOnline(String json){
		return this.serialize(this.asArrayOfData(json));		
	}
	
	public List getLanguagesListingOffline(){
		BaseData.dbOpen();
		List languages = new ArrayList();
		this.select(listLanguages);
		if (this.getResultSet().isValidRow()){
			try {
				for (int i = 0; this.getResultSet().isValidRow(); ++i, this.getResultSet().next()) {
					Data language = new Data(this.getResultSet().getFieldAsInt(0), this.getResultSet().getFieldAsString(1));
					languages.add(language);
	    	      }				
			} catch (DatabaseException e) {
				Window.alert("Database Exception : " + e.toString());
				// TODO Auto-generated catch block
				BaseData.dbClose();
			}
			
		}
		BaseData.dbClose();
		return languages;
	}
	
	public List getAllLanguagesOffline(){
		BaseData.dbOpen();
		List languages = new ArrayList();
		this.select(selectLanguages);
		if (this.getResultSet().isValidRow()){
			try {
				for (int i = 0; this.getResultSet().isValidRow(); ++i, this.getResultSet().next()) {
					Data language = new Data(this.getResultSet().getFieldAsInt(0), this.getResultSet().getFieldAsString(1));
					languages.add(language);
	    	      }				
			} catch (DatabaseException e) {
				Window.alert("Database Exception : " + e.toString());
				// TODO Auto-generated catch block
				BaseData.dbClose();
			}
			
		}
		BaseData.dbClose();
		return languages;
	}

	public Object postPageData() {
		if(BaseData.isOnline()){
			this.post(RequestContext.SERVER_HOST + LanguagesData.saveLanguageOnlineURL, this.queryString);
		}
		else{
			this.save();
			return true;
		}
		
		return false;
	}
	
	public Object getPageData(){
		if(BaseData.isOnline()){
			this.get(RequestContext.SERVER_HOST + LanguagesData.getLanguageOnlineURL);
		}
		else{
			return true;
		}
		return false;
	}	
}
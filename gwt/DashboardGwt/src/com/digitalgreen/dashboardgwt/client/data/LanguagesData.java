package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.validation.StringValidator;
import com.digitalgreen.dashboardgwt.client.data.validation.UniqueConstraintValidator;
import com.google.gwt.core.client.JsArray;
import com.google.gwt.gears.client.database.DatabaseException;
import com.google.gwt.user.client.Window;

public class LanguagesData extends BaseData {

	public static class Type extends BaseData.Type{
		protected Type() {}
		public final native String getLanguageName() /*-{ return $wnd.checkForNullValues(this.fields.language_name); }-*/;
	}

	public class Data extends BaseData.Data {
		
		final private static String COLLECTION_PREFIX = "language";
			
		private String language_name;
		
		public Data() {
			super();
		}
		
		public Data(String id) {
			super();
			this.id = id;
		}
		
		public Data(String id, String language_name) {
			super();
			this.id = id;
			this.language_name = language_name;
		}
		
		public String getLanguageName(){
			return this.language_name;
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
			if(key.equals("id")) {
				this.id = val;
			}else if(key.equals("language_name")) {
				this.language_name = (String)val;
			}
			else {
				return;
			}
			this.addNameValueToQueryString(key, val);
		}
		
		@Override
		public boolean validate() {
			StringValidator languageName = new StringValidator(this.language_name, false, false, 1, 100, true);
			languageName.setError("Please make sure that 'Language Name' is NOT EMPTY and not more than 100 characters.");
			ArrayList language_name = new ArrayList();
			language_name.add("language_name");
			language_name.add(this.language_name);
			ArrayList uniqueName = new ArrayList();
			uniqueName.add(language_name);
			UniqueConstraintValidator uniqueNameValidator = new UniqueConstraintValidator(uniqueName, new LanguagesData());
			uniqueNameValidator.setError("The Language is already in the system.  Please make sure it is unique.");
			uniqueNameValidator.setCheckId(this.getId());
			ArrayList validatorList = new ArrayList();
			validatorList.add(languageName);
			validatorList.add(uniqueNameValidator);
			return this.executeValidators(validatorList);
		}
		
		@Override
		public void save() {
			LanguagesData languagesDataDbApis = new LanguagesData();
			this.id = languagesDataDbApis.autoInsert(this.id, this.language_name);
			this.addNameValueToQueryString("id", this.id);
		}
		
		@Override
		public String toQueryString(String id) {
			LanguagesData languagesData = new LanguagesData();
			return this.rowToQueryString(languagesData.getTableName(), languagesData.getFields(), "id", id, "");
		}
		
		
		@Override
		public String getTableId() {
			LanguagesData languagesDataDbApis = new LanguagesData();
			return languagesDataDbApis.tableID;
		}
	}
	
	public static String tableID = "26";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `language` " +
											"(id INTEGER PRIMARY KEY  NOT NULL ," +
											"language_name VARCHAR(100) UNIQUE NOT NULL );";  
	protected static String dropTable = "DROP TABLE IF EXISTS `language`;";
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
	
	public LanguagesData(OnlineOfflineCallbacks callbacks, Form form) {
		super(callbacks, form);
	}
	
	@Override
	public Data getNewData() {
		return new Data();
	}
	
	@Override
	protected String getTableId() {
		return LanguagesData.tableID;
	}
	
	@Override
	public String getTableName() {
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
		return LanguagesData.getLanguageOnlineURL;
	}
	
	@Override
	public String getSaveOfflineURL(){
		return LanguagesData.saveLanguageOfflineURL;
	}
	
	@Override
	public String getSaveOnlineURL(){
		return LanguagesData.saveLanguageOnlineURL;
	}
	
	public final native JsArray<Type> asArrayOfData(String json) /*-{
		return eval(json);
	}-*/;
	
	public List serialize(JsArray<Type> languageObjects){
		List languages = new ArrayList();
		for(int i = 0; i < languageObjects.length(); i++){
			Data language = new Data(languageObjects.get(i).getPk(), languageObjects.get(i).getLanguageName());
			languages.add(language);
		}
		
		return languages;
	}
	
	@Override
	public List getListingOnline(String json){
		return this.serialize(this.asArrayOfData(json));		
	}
	
	
	
	public List getLanguagesListingOffline(String... pageNum){
		BaseData.dbOpen();
		List languages = new ArrayList();
		String listTemp;
		// Checking whether to return all villages or only limited number of villages
		if(pageNum.length == 0) {
			listTemp = listLanguages;
		}
		else {
			int offset = (Integer.parseInt(pageNum[0]) - 1)*pageSize;
			listTemp = listLanguages + " LIMIT "+ Integer.toString(offset) + " , "+Integer.toString(pageSize) +";";
		}
		this.select(listTemp);
		if (this.getResultSet().isValidRow()){
			try {
				for (int i = 0; this.getResultSet().isValidRow(); ++i, this.getResultSet().next()) {
					Data language = new Data(this.getResultSet().getFieldAsString(0), this.getResultSet().getFieldAsString(1));
					languages.add(language);
	    	      }				
			} catch (DatabaseException e) {
				Window.alert("Database Exception : " + e.toString());
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
					Data language = new Data(this.getResultSet().getFieldAsString(0), this.getResultSet().getFieldAsString(1));
					languages.add(language);
	    	      }				
			} catch (DatabaseException e) {
				Window.alert("Database Exception : " + e.toString());
				BaseData.dbClose();
			}
			
		}
		BaseData.dbClose();
		return languages;
	}

	public Object postPageData() {
		if(BaseData.isOnline()){
			this.post(RequestContext.SERVER_HOST + LanguagesData.saveLanguageOnlineURL, this.form.getQueryString());
		}
		else{
			if(this.validate()) {
				this.save();
				return true;
			}
		}
		
		return false;
	}
	
	public Object postPageData(String id) {
		if(BaseData.isOnline()){
			this.post(RequestContext.SERVER_HOST + this.saveLanguageOnlineURL + id + "/", this.form.getQueryString());
		}
		else{
			if(this.validate()) {
				this.save();
				return true;
			}
		}
		return false;
	}
	
	
	public Object getListPageData(String pageNum){
		if(BaseData.isOnline()){
			int offset = (Integer.parseInt(pageNum)-1)*pageSize;
			int limit = offset+pageSize;
			this.get(RequestContext.SERVER_HOST + LanguagesData.getLanguageOnlineURL+Integer.toString(offset)+"/"+Integer.toString(limit));
		}
		else{
			return true;
		}
		return false;
	}	
	
	public Object getAddPageData(){
		if(BaseData.isOnline()){
			this.get(RequestContext.SERVER_HOST + this.saveLanguageOnlineURL);
		}
		else{
			return "No add data required";
		}
		return false;
	}
	
	public Object getAddPageData(String id){
		if(BaseData.isOnline()){
			this.get(RequestContext.SERVER_HOST + this.saveLanguageOnlineURL + id + "/" );
		}
		else{
			this.form.toQueryString(id);
			return "No add data required";
		}
		return false;
	}
}
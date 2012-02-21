package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.validation.DateValidator;
import com.digitalgreen.dashboardgwt.client.data.validation.StringValidator;
import com.digitalgreen.dashboardgwt.client.data.validation.UniqueConstraintValidator;
import com.google.gwt.core.client.JsArray;
import com.google.gwt.gears.client.database.DatabaseException;
import com.google.gwt.user.client.Window;

public class CountriesData extends BaseData {
	
	public static class Type extends BaseData.Type{
		protected Type() {}
		public final native String getCountryName() /*-{ return $wnd.checkForNullValues(this.fields.country_name); }-*/;
		public final native String getStartDate() /*-{ return $wnd.checkForNullValues(this.fields.start_date);  }-*/;
	}

	public class Data extends BaseData.Data {
		
		final private static String COLLECTION_PREFIX = "country";
			
		private String country_name;
		private String start_date;
		
		public Data() {
			super();
		}
		
		public Data(String id, String country_name){
			super();
			this.id = id;
			this.country_name = country_name;
		}
		
		public Data(String id, String country_name, String start_date) {
			super();
			this.id = id;
			this.country_name = country_name;
			this.start_date = start_date;
		}
		
		public String getCountryName(){
			return this.country_name;
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
			if(key.equals("id")) {
				this.id = val;
			}else if(key.equals("country_name")) {
				this.country_name = (String)val;
			} else if(key.equals("start_date")) {
				this.start_date = (String)val;
			} else {
				return;
			}
			this.addNameValueToQueryString(key, val);			
		}
		
		@Override
		public boolean validate(){
			//Labels to print validation error messages
			String nameLabel = "Country Name";
			String dateLabel = "Start Date";
			StringValidator nameValidator = new StringValidator(nameLabel, this.country_name, false, false, 1, 100, true);
			DateValidator dateValidator = new DateValidator(dateLabel, this.start_date, true, false);
			ArrayList country_name = new ArrayList();
			country_name.add("country_name");
			country_name.add(this.country_name);
			ArrayList uniqueCountryName = new ArrayList();
			uniqueCountryName.add(country_name);
			ArrayList uniqueValidatorLabels = new ArrayList();
			uniqueValidatorLabels.add("Country Name");
			UniqueConstraintValidator countryName = new UniqueConstraintValidator(uniqueValidatorLabels, uniqueCountryName, new CountriesData());
			countryName.setCheckId(this.getId());
			ArrayList validatorList = new ArrayList();
			validatorList.add(nameValidator);
			validatorList.add(dateValidator);
			validatorList.add(countryName);
			return this.executeValidators(validatorList);
		}
		
		@Override
		public void save() {
			CountriesData countriesDataDbApis = new CountriesData();
			this.id = countriesDataDbApis.autoInsert(this.id,
					this.country_name, 
					this.start_date);
			this.addNameValueToQueryString("id", this.id);
		}		
		
		@Override
		public String toQueryString(String id) {
			CountriesData countriesData = new CountriesData();
			return this.rowToQueryString(countriesData.getTableName(), countriesData.getFields(), "id", id, "");
		}
		
		@Override
		public String getTableId() {
			CountriesData countriesDataDbApis = new CountriesData();
			return countriesDataDbApis.tableID;
		}
	}

	public static String tableID = "7";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `country` " +
												"(id BIGINT UNSIGNED PRIMARY KEY NOT NULL," +
												"COUNTRY_NAME VARCHAR(100) NOT NULL," +
												"START_DATE DATE NULL DEFAULT NULL);";
	protected static String dropTable = "DROP TABLE IF EXISTS `country`;";
	protected static String[] createIndexes = {"CREATE INDEX IF NOT EXISTS COUNTRY_PRIMARY ON country(id);"};
	protected static String selectCountries = "SELECT id, country_name FROM country ORDER BY(country_name)";
	protected static String listCountries = "SELECT * FROM country ORDER BY(-id)";
	protected static String saveCountryOnlineURL = "/dashboard/savecountryonline/";
	protected static String getCountryOnlineURL = "/dashboard/getcountriesonline/";
	protected static String saveCountryOfflineURL = "/dashboard/savecountryoffline/";
	protected String table_name = "country";
	protected String[] fields = {"id", "country_name", "start_date"};
	
	public CountriesData() {
		super();
	}
	
	public CountriesData(OnlineOfflineCallbacks callbacks) {
		super(callbacks);
	}
	
	public CountriesData(OnlineOfflineCallbacks callbacks, Form form) {
		super(callbacks, form);
	}

	@Override
	public Data getNewData() {
		return new Data();
	}
	
	@Override
	protected  String getTableId() {
		return CountriesData.tableID;
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
		return CountriesData.getCountryOnlineURL;
	}
	
	@Override
	public String getSaveOfflineURL(){
		return CountriesData.saveCountryOfflineURL;
	}
	
	@Override
	public String getSaveOnlineURL(){
		return CountriesData.saveCountryOnlineURL;
	}



	public final native JsArray<Type> asArrayOfData(String json) /*-{
		return eval(json);
	}-*/;
	
	
	public List serialize(JsArray<Type> countryObjects){
		List countries = new ArrayList();
		for(int i = 0; i < countryObjects.length(); i++){
			Data country = new Data(countryObjects.get(i).getPk(), countryObjects.get(i).getCountryName(), countryObjects.get(i).getStartDate());
			countries.add(country);
		}
		return countries;
	}
	
	@Override
	public List getListingOnline(String json){
		return this.serialize(this.asArrayOfData(json));		
	}
	
	public List getCountriesListingOffline(String... pageNum){
		BaseData.dbOpen();
		List countries = new ArrayList();
		String listTemp;
		// Checking whether to return all villages or only limited number of villages
		if(pageNum.length == 0) {
			listTemp = listCountries;
		}
		else {
			int offset = (Integer.parseInt(pageNum[0]) - 1)*pageSize;
			listTemp = listCountries + " LIMIT "+ Integer.toString(offset) + " , "+Integer.toString(pageSize) +";";
		}
		this.select(listTemp);
		if (this.getResultSet().isValidRow()){
			try {
				for (int i = 0; this.getResultSet().isValidRow(); ++i, this.getResultSet().next()) {
					Data country = new Data(this.getResultSet().getFieldAsString(0), this.getResultSet().getFieldAsString(1), this.getResultSet().getFieldAsString(2));
					countries.add(country);
	    	      }				
			} catch (DatabaseException e) {
				Window.alert("Database Exception : " + e.toString());
				BaseData.dbClose();
			}
		}
		BaseData.dbClose();
		return countries;
	}

	public List getAllCountriesOffline(){
		BaseData.dbOpen();
		List countries = new ArrayList();
		this.select(selectCountries);
		if (this.getResultSet().isValidRow()){
			try {
				for (int i = 0; this.getResultSet().isValidRow(); ++i, this.getResultSet().next()) {
					Data country = new Data(this.getResultSet().getFieldAsString(0), this.getResultSet().getFieldAsString(1));
					countries.add(country);
	    	      }				
			} catch (DatabaseException e) {
				Window.alert("Database Exception : " + e.toString());
				BaseData.dbClose();
			}	
		}
		BaseData.dbClose();
		return countries;
	}
	
	public Object postPageData() {
		if(BaseData.isOnline()){
			this.post(RequestContext.SERVER_HOST + CountriesData.saveCountryOnlineURL, this.form.getQueryString());
		}
		else{
			if(this.validate()){
				this.save();
				return true;
			}
		}		
		return false;
	}
	
	public Object postPageData(String id) {
		if(BaseData.isOnline()){
			this.post(RequestContext.SERVER_HOST + CountriesData.saveCountryOnlineURL + id + "/", this.form.getQueryString());
		}
		else{
			if(this.validate()){
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
			this.get(RequestContext.SERVER_HOST + CountriesData.getCountryOnlineURL+Integer.toString(offset)+"/"+Integer.toString(limit)+ "/");
		}
		else{
			return true;
		}
		return false;
	}
	
	public Object getAddPageData(){
		if(BaseData.isOnline()){
			this.get(RequestContext.SERVER_HOST + this.saveCountryOnlineURL);
		}
		else{
			return "No add data required";
		}
		return false;
	}
	
	public Object getAddPageData(String id){
		if(BaseData.isOnline()){
			this.get(RequestContext.SERVER_HOST + this.saveCountryOnlineURL + id + "/" );
		}
		else{
			this.form.toQueryString(id);
			return "No add data required";
		}
		return false;
	}

}

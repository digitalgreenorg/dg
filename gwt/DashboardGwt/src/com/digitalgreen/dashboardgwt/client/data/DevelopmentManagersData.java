package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;
import java.util.List;
import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.EquipmentHoldersData.Data;
import com.digitalgreen.dashboardgwt.client.data.validation.DateValidator;
import com.digitalgreen.dashboardgwt.client.data.validation.IntegerValidator;
import com.digitalgreen.dashboardgwt.client.data.validation.StringValidator;
import com.google.gwt.core.client.JsArray;
import com.google.gwt.gears.client.database.DatabaseException;
import com.google.gwt.user.client.Window;


public class DevelopmentManagersData extends BaseData {
	
	public static class Type extends BaseData.Type{
		protected Type() {}
		public final native String getName() /*-{ return $wnd.checkForNullValues(this.fields.name); }-*/;
		public final native String getAge() /*-{ return $wnd.checkForNullValues(this.fields.age); }-*/;
		public final native String getGender() /*-{ return $wnd.checkForNullValues(this.fields.gender); }-*/;
		public final native String getHireDate() /*-{ return $wnd.checkForNullValues(this.fields.hire_date); }-*/;
		public final native String getPhoneNo() /*-{ return $wnd.checkForNullValues(this.fields.phone_no); }-*/;
		public final native String getAddress() /*-{ return $wnd.checkForNullValues(this.fields.address); }-*/;
		public final native String getSpeciality() /*-{ return $wnd.checkForNullValues(this.fields.speciality); }-*/;
		public final native RegionsData.Type getRegion() /*-{ return this.fields.region }-*/;
		public final native String getStartDay() /*-{ return $wnd.checkForNullValues(this.fields.start_day); }-*/;
		public final native String getSalary() /*-{ return $wnd.checkForNullValues(this.fields.salary); }-*/;
				
	}
	
	public class Data extends BaseData.Data {
		
		final private static String COLLECTION_PREFIX = "developmentmanager";
			
		private String name;
		private String age;
		private String gender;
		private String hire_date;
		private String phone_no;
		private String address;
		private String speciality;
		private RegionsData.Data region;
		private String start_day;
		private String salary;
		
		
		
		public Data() {
			super();
		}
		
		public Data(String id) {
			super();
			this.id = id;
		}

		public Data(String id, String name,String age,String gender,String hire_date,String phone_no,String address,String speciality,
				RegionsData.Data region, String start_day, String salary ) {
			super();
			this.id = id;
			this.name = name;
			this.age = age;
			this.gender = gender;
			this.hire_date = hire_date;
			this.phone_no = phone_no;
			this.address = address;
			this.speciality = speciality;
			this.region = region;
			this.start_day = start_day;
			this.salary = salary;
		}
		
		public Data(String id, String name){
			super();
			this.id = id;
			this.name = name;
		}
				
		public String getName(){
			return this.name;
		}
		
		public String getAge(){
			return this.age;
		}
		
		public String getGender(){
			return this.gender;
		}
		
		public String getHireDate(){
			return this.hire_date;
		}
		
		public String getPhoneNo(){
			return this.phone_no;
		}
		
		public String getAddress(){
			return this.address;
		}
		
		public String getSpeciality(){
			return this.speciality;
		}
		
		public RegionsData.Data getRegion(){
			return this.region;
		}
		
		public String getStartDay(){
			return this.start_day;
		}
				
		
		public String getSalary(){
			return this.salary;
		}
				
		
		
		public BaseData.Data clone() {
			Data obj = new Data();
			obj.region = (new RegionsData()).new Data();
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
			}else if(key.equals("name")) {
				this.name = (String)val;
			} else if(key.equals("age")) {
				this.age = (String)val;
			} else if(key.equals("gender")) {
				this.gender = (String)val;
			} else if(key.equals("hire_date")) {
				this.hire_date = (String)val;
			}  else if(key.equals("phone_no")) {
				this.phone_no = (String)val;
			} else if(key.equals("address")) {
				this.address = (String)val;
			} else if(key.equals("speciality")) {
				this.speciality = (String)val;
			} else if(key.equals("region")) {
				// Have to Create an instance of RegionsData to create an instance of RegionsData.Data -- any better way of doing this??
				RegionsData region = new RegionsData();
				this.region = region.getNewData();
				this.region.id = val;
				//Never ever use this -- this.region.id = ((Integer)val).intValue();
			}  else if(key.equals("start_day")) {
				this.start_day = (String)val;
			}  else if(key.equals("salary")) {
				this.salary = val;
			} else {
				return;
			}
			this.addNameValueToQueryString(key, val);		
		}
		
		@Override
		public boolean validate(){
			//Labels to print validation error messages
			String nameLabel = "Name";
			String ageLabel = "Age";
			String genderLabel = "Gender";
			String hireDateLabel = "Hire Date";			
			String phoneNoLabel = "Phone Number";
			String addressLabel = "Address";
			String specialityLabel = "Speciality";
			String regionLabel = "Region";
			String startDateLabel = "Start Date";			
			StringValidator nameValidator = new StringValidator(nameLabel,this.name, false, false, 1, 100, true);
			IntegerValidator ageValidator = new IntegerValidator(ageLabel,this.age, true, true, 0, 100);
			StringValidator genderValidator = new StringValidator(genderLabel, this.gender, false, false, 1, 3);
			DateValidator hireDate = new DateValidator(hireDateLabel,this.hire_date, true, false);
			StringValidator phoneValidator = new StringValidator(phoneNoLabel,this.phone_no, true, false, 0, 100, true);
			StringValidator addressValidator = new StringValidator(addressLabel,this.address, true, false, 0, 500);
			StringValidator specialityValidator = new StringValidator(specialityLabel,this.speciality, true, false, 0, 500);
			StringValidator regionValidator = new StringValidator(regionLabel,this.region.getId(), false, false, 1, 100);
			DateValidator startDate = new DateValidator(startDateLabel,this.start_day, true, false);
			ArrayList validatorList = new ArrayList();
			validatorList.add(nameValidator);
			validatorList.add(ageValidator);
			validatorList.add(genderValidator);
			validatorList.add(hireDate);
			validatorList.add(phoneValidator);
			validatorList.add(addressValidator);
			validatorList.add(specialityValidator);
			validatorList.add(regionValidator);
			validatorList.add(startDate);
			return this.executeValidators(validatorList);
		}
		
		@Override		
		public void save() {
			DevelopmentManagersData developmentmanagersDataDbApis = new DevelopmentManagersData();
			this.id = developmentmanagersDataDbApis.autoInsert(this.id, 
						this.name,
						this.age,
						this.gender,
						this.hire_date,
						this.phone_no,
						this.address,
						this.speciality,
						this.region.getId(),
						this.start_day,
						this.salary);
			this.addNameValueToQueryString("id", this.id);
		}
		
		@Override
		public String toQueryString(String id) {
			DevelopmentManagersData developmentManagersData = new DevelopmentManagersData();
			return this.rowToQueryString(developmentManagersData.getTableName(), developmentManagersData.getFields(), "id", id, "");
		}
		
		
		@Override
		public String getTableId() {
			DevelopmentManagersData developmentmanagersDataDbApis = new DevelopmentManagersData();
			return developmentmanagersDataDbApis.tableID;
		}
	}
	
	public static String tableID = "11";
	protected static String createTable = "CREATE TABLE  IF NOT EXISTS `development_manager` " +
												"(id BIGINT UNSIGNED PRIMARY KEY  NOT NULL ," +
												"NAME VARCHAR(100)  NOT NULL ," +
												"AGE INT  NULL DEFAULT NULL," +
												"GENDER VARCHAR(1)  NOT NULL ," +
												"HIRE_DATE DATE  NULL DEFAULT NULL," +
												"PHONE_NO VARCHAR(100)  NULL DEFAULT NULL, " +
												"ADDRESS VARCHAR(500)  NULL DEFAULT NULL ," +
												"SPECIALITY TEXT  NULL DEFAULT NULL ," +
												"region_id BIGINT UNSIGNED  NOT NULL DEFAULT 0," +
												"START_DAY DATE  NULL DEFAULT NULL," +
												"SALARY FLOAT(0,0)  NULL DEFAULT NULL, " +
												"FOREIGN KEY(region_id) REFERENCES region(id));";
	protected static String dropTable = "DROP TABLE IF EXISTS `development_manager`;";
	protected static String selectDevelopmentManagers = "SELECT id, NAME FROM development_manager  ORDER BY (NAME);";
	protected static String getDevelopmentManagerByID = "SELECT id, NAME FROM development_manager WHERE id = ?;";
	protected static String listDevelopmentManagers = "SELECT d.id, d.NAME,d.AGE, d.GENDER, d.HIRE_DATE, d.PHONE_NO, d.ADDRESS,d.SPECIALITY, r.id, r.REGION_NAME , d.START_DAY, d.salary FROM development_manager d JOIN region r ON d.region_id = r.id ORDER BY (-d.id)";
	protected static String saveDevelopmentManagerOfflineURL = "/dashboard/savedevelopmentmanageroffline/";
	protected static String saveDevelopmentManagerOnlineURL = "/dashboard/savedevelopmentmanageronline/";
	protected static String getDevelopmentManagerOnlineURL = "/dashboard/getdevelopmentmanagersonline/";
	protected String table_name = "development_manager";
	protected String[] fields = {"id", "name", "age", "gender", "hire_date", "phone_no", "address", "speciality",
			"region_id", "start_day", "salary"};
	

	public DevelopmentManagersData() {
		super();
	}

	public DevelopmentManagersData(OnlineOfflineCallbacks callbacks) {
		super(callbacks);
	}
	
	public DevelopmentManagersData(OnlineOfflineCallbacks callbacks, Form form) {
		super(callbacks, form);
	}

	@Override
	public Data getNewData() {
		return new Data();
	}
	
	@Override
	protected String getTableId() {
		return DevelopmentManagersData.tableID;
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
		return DevelopmentManagersData.getDevelopmentManagerOnlineURL;
	}
	
	@Override
	public String getSaveOfflineURL(){
		return DevelopmentManagersData.saveDevelopmentManagerOfflineURL;
	}
	
	@Override
	public String getSaveOnlineURL(){
		return DevelopmentManagersData.saveDevelopmentManagerOnlineURL;
	}
	
	public final native JsArray<Type> asArrayOfData(String json) /*-{
		return eval(json);
	}-*/;
	
	public List serialize(JsArray<Type> developmentmanagerObjects){
		List developmentmanagers = new ArrayList();
		RegionsData region = new RegionsData();
		for(int i = 0; i < developmentmanagerObjects.length(); i++){
			RegionsData.Data r = region.new Data(developmentmanagerObjects.get(i).getRegion().getPk(), developmentmanagerObjects.get(i).getRegion().getRegionName(), developmentmanagerObjects.get(i).getRegion().getStartDate());
			Data developmentmanager = new Data(developmentmanagerObjects.get(i).getPk(),
						developmentmanagerObjects.get(i).getName(),
						developmentmanagerObjects.get(i).getAge(),
						developmentmanagerObjects.get(i).getGender(),
						developmentmanagerObjects.get(i).getHireDate(),
						developmentmanagerObjects.get(i).getPhoneNo(),
						developmentmanagerObjects.get(i).getAddress(),
						developmentmanagerObjects.get(i).getSpeciality(),r,
						developmentmanagerObjects.get(i).getStartDay(), 
						developmentmanagerObjects.get(i).getSalary());
			developmentmanagers.add(developmentmanager);
		}
		
		return developmentmanagers;
	}
	
	@Override
	public List getListingOnline(String json){
		return this.serialize(this.asArrayOfData(json));		
	}
	
	public List getDevelopmentManagersListingOffline(String... pageNum){
		BaseData.dbOpen();
		List developmentmanagers = new ArrayList();
		RegionsData region = new RegionsData();
		String listTemp;
		// Checking whether to return all villages or only limited number of villages
		if(pageNum.length == 0) {
			listTemp = listDevelopmentManagers;
		}
		else {
			int offset = (Integer.parseInt(pageNum[0]) - 1)*pageSize;
			listTemp = listDevelopmentManagers + " LIMIT "+ Integer.toString(offset) + " , "+Integer.toString(pageSize) +";";
		}
		this.select(listTemp);
		if (this.getResultSet().isValidRow()){
			try {
				for (int i = 0; this.getResultSet().isValidRow(); ++i, this.getResultSet().next()) {
					
					RegionsData.Data r = region.new Data(this.getResultSet().getFieldAsString(8),  this.getResultSet().getFieldAsString(9)) ;
					Data developmentmanager = new Data(this.getResultSet().getFieldAsString(0), 
							this.getResultSet().getFieldAsString(1),
							this.getResultSet().getFieldAsString(2),
							this.getResultSet().getFieldAsString(3),
							this.getResultSet().getFieldAsString(4),
							this.getResultSet().getFieldAsString(5),
							this.getResultSet().getFieldAsString(6),
							this.getResultSet().getFieldAsString(7),r,
							this.getResultSet().getFieldAsString(10), 
							this.getResultSet().getFieldAsString(11));
					developmentmanagers.add(developmentmanager);
				}				
			} catch (DatabaseException e) {
				Window.alert("Database Exception : " + e.toString());
				BaseData.dbClose();
			}
		}
		BaseData.dbClose();
		return developmentmanagers;
	}
	
	public List getAllDevelopmentManagersOffline(){
		BaseData.dbOpen();
		List developmentmanagers = new ArrayList();
		this.select(selectDevelopmentManagers);
		if (this.getResultSet().isValidRow()){
			try {
				for (int i = 0; this.getResultSet().isValidRow(); ++i, this.getResultSet().next()) {
					Data developmentmanager = new Data(this.getResultSet().getFieldAsString(0), this.getResultSet().getFieldAsString(1));
					developmentmanagers.add(developmentmanager);
				}				
			} catch (DatabaseException e) {
				Window.alert("Database Exception : " + e.toString());
				BaseData.dbClose();
			}
		}
		BaseData.dbClose();
		return developmentmanagers;
	}

	public Object postPageData() {
		if(BaseData.isOnline()){
			this.post(RequestContext.SERVER_HOST + DevelopmentManagersData.saveDevelopmentManagerOnlineURL, this.form.getQueryString());
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
			this.post(RequestContext.SERVER_HOST + this.saveDevelopmentManagerOnlineURL + id + "/", this.form.getQueryString());
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
			this.get(RequestContext.SERVER_HOST + DevelopmentManagersData.getDevelopmentManagerOnlineURL + Integer.toString(offset) + "/" + Integer.toString(limit)+ "/");
		}
		else{
			return true;
		}
		return false;
	}	
	
	public String retrieveDataAndConvertResultIntoHtml(){
		RegionsData regionData = new RegionsData();
		List regions = regionData.getAllRegionsOffline();
		RegionsData.Data region;
		String html = "<select name=\"region\" id=\"id_region\">" + 
					"<option value='' selected='selected'>---------</option>";
		
		for(int i=0; i< regions.size(); i++){
			region = (RegionsData.Data)regions.get(i);
			html = html + "<option value = \"" + region.getId() +"\">" + region.getRegionName() + "</option>";
		}
		html = html + "</select>";
		return html;
	}
	
	public Object getAddPageData(){
		if(BaseData.isOnline()){
			this.get(RequestContext.SERVER_HOST + DevelopmentManagersData.saveDevelopmentManagerOnlineURL);
		}
		else{
			return retrieveDataAndConvertResultIntoHtml();
		}
		return false;
	}
	
	public Object getAddPageData(String id){
		if(BaseData.isOnline()){
			this.get(RequestContext.SERVER_HOST + this.saveDevelopmentManagerOnlineURL + id + "/" );
		}
		else{
			this.form.toQueryString(id);
			return retrieveDataAndConvertResultIntoHtml();
		}
		return false;
	}
	
}
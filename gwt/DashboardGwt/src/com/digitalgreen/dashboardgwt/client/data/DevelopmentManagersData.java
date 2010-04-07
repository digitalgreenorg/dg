package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;
import java.util.List;
import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.google.gwt.core.client.JsArray;
import com.google.gwt.gears.client.database.DatabaseException;
import com.google.gwt.user.client.Window;


public class DevelopmentManagersData extends BaseData {
	
	public static class Type extends BaseData.Type{
		protected Type() {}
		public final native String getName() /*-{ return this.fields.name; }-*/;
		public final native String getAge() /*-{ return this.fields.age; }-*/;
		public final native String getGender() /*-{ return this.fields.gender; }-*/;
		public final native String getHireDate() /*-{ return this.fields.hire_date; }-*/;
		public final native String getPhoneNo() /*-{ return this.fields.phone_no; }-*/;
		public final native String getAddress() /*-{ return this.fields.address; }-*/;
		public final native String getSpeciality() /*-{ return this.fields.speciality; }-*/;
		public final native RegionsData.Type getRegion() /*-{ return this.fields.region }-*/;
		public final native String getStartDay() /*-{ return this.fields.start_day; }-*/;
		public final native int getEquipmentHolderId() /*-{ return this.fields.equipmentholder_id; }-*/;
		public final native float getSalary() /*-{ return this.fields.salary; }-*/;
				
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
		private int equipmentholder_id;
		private float salary;
		
		
		
		public Data() {
			super();
		}

		public Data(int id, String name,String age,String gender,String hire_date,String phone_no,String address,String speciality,
				RegionsData.Data region, String start_day,int equipmentholder_id,float salary ) {
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
			this.equipmentholder_id = equipmentholder_id;
			this.salary = salary;
		}
		
		public Data(int id, String name){
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
				
		public int getEquipmentHolderId(){
			return this.equipmentholder_id;
		}
		
		public float getSalary(){
			return this.salary;
		}
				
		
		
		public BaseData.Data clone() {
			Data obj = new Data();
			obj.id = this.id;
			obj.name = this.name;
			obj.age = this.age;
			obj.gender = this.gender;
			obj.hire_date = this.hire_date;
			obj.phone_no = this.phone_no;
			obj.address = this.address;
			obj.speciality = this.speciality;
			obj.region = (RegionsData.Data)this.region.clone();
			obj.start_day = this.start_day;
			obj.equipmentholder_id = this.equipmentholder_id;
			obj.salary = this.salary;
				
			return obj;
		}
		
		@Override
		public String getPrefixName() {
			return Data.COLLECTION_PREFIX;
		}
		
		@Override
		public void setObjValueFromString(String key, Object val) {		
			if(key.equals("id")) {
				this.id = Integer.parseInt((String)val);
			} else if(key.equals("name")) {
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
				this.region.id = Integer.parseInt((String)val);
				//Never ever use this -- this.region.id = ((Integer)val).intValue();
			}  else if(key.equals("start_day")) {
				this.start_day = (String)val;
			}  else if(key.equals("equipmentholder_id")) {
				this.equipmentholder_id = Integer.parseInt((String)val);
			} else if(key.equals("salary")) {
				this.salary = Float.parseFloat((String)val);
				}		
		}
		
		@Override
		
		public void save() {
			DevelopmentManagersData developmentmanagersDataDbApis = new DevelopmentManagersData();
			if(this.id == 0){
				this.id = developmentmanagersDataDbApis.autoInsert(this.name,this.age,this.gender,this.hire_date,
						this.phone_no,this.address,this.speciality,Integer.valueOf(this.region.getId()).toString(),this.start_day,
						Integer.valueOf(this.equipmentholder_id).toString(),Float.valueOf(this.salary).toString());
			}else{
				this.id = developmentmanagersDataDbApis.autoInsert(Integer.valueOf(this.id).toString(),this.name,this.age,this.gender,this.hire_date,
						this.phone_no,this.address,this.speciality,Integer.valueOf(this.region.getId()).toString(),this.start_day,
						Integer.valueOf(this.equipmentholder_id).toString(),Float.valueOf(this.salary).toString());
			}
			
			
		}
	}
	
	protected static String tableID = "4";
	protected static String createTable = "CREATE TABLE  IF NOT EXISTS `development_manager` " +
												"(id INTEGER PRIMARY KEY  NOT NULL ," +
												"NAME VARCHAR(100)  NOT NULL ," +
												"AGE INT  NULL DEFAULT NULL," +
												"GENDER VARCHAR(1)  NOT NULL ," +
												"HIRE_DATE DATE  NULL DEFAULT NULL," +
												"PHONE_NO VARCHAR(100)  NOT NULL, " +
												"ADDRESS VARCHAR(500)  NOT NULL ," +
												"SPECIALITY TEXT  NOT NULL ," +
												"region_id INT  NOT NULL DEFAULT 0," +
												"START_DAY DATE  NULL DEFAULT NULL," +
												"equipmentholder_id INT  NULL DEFAULT NULL," +
												"SALARY FLOAT(0,0)  NULL DEFAULT NULL, " +
												"FOREIGN KEY(region_id) REFERENCES region(id), " +
												"FOREIGN KEY(equipmentholder_id) REFERENCES equipment_holder(id));";
	protected static String selectDevelopmentManagers = "SELECT id, NAME FROM development_manager  ORDER BY (NAME);";
	protected static String listDevelopmentManagers = "SELECT d.id, d.NAME,d.AGE, d.GENDER, d.HIRE_DATE, d.PHONE_NO, d.ADDRESS,d.SPECIALITY, r.id, r.REGION_NAME , d.START_DAY, d.equipmentholder_id,d.salary FROM development_manager d JOIN region r ON d.region_id = r.id ORDER BY (-d.id);";
	protected static String saveDevelopmentManagerOfflineURL = "/dashboard/savedevelopmentmanageroffline/";
	protected static String saveDevelopmentManagerOnlineURL = "/dashboard/savedevelopmentmanageronline/";
	protected static String getDevelopmentManagerOnlineURL = "/dashboard/getdevelopmentmanagersonline/";
	protected String table_name = "development_manager";
	protected String[] fields = {"id", "name", "age", "gender", "hire_date", "phone_no", "address", "speciality",
			"region_id", "start_day", "equipmentholder_id", "salary"};
	

	public DevelopmentManagersData() {
		super();
	}

	public DevelopmentManagersData(OnlineOfflineCallbacks callbacks) {
		super(callbacks);
	}
	
	public DevelopmentManagersData(OnlineOfflineCallbacks callbacks, Form form, String queryString) {
		super(callbacks, form, queryString);
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
	protected String getTableName() {
		return this.table_name;
	}
	
	@Override
	protected String[] getFields() {
		return this.fields;
	}
	
	@Override
	public String getListingOnlineURL(){
		return DevelopmentManagersData.getDevelopmentManagerOnlineURL;
	}
	
	public final native JsArray<Type> asArrayOfData(String json) /*-{
		return eval(json);
	}-*/;
	
	public List serialize(JsArray<Type> developmentmanagerObjects){
		List developmentmanagers = new ArrayList();
		RegionsData region = new RegionsData();
		for(int i = 0; i < developmentmanagerObjects.length(); i++){
			RegionsData.Data r = region.new Data(Integer.parseInt(developmentmanagerObjects.get(i).getRegion().getPk()), developmentmanagerObjects.get(i).getRegion().getRegionName(), developmentmanagerObjects.get(i).getRegion().getStartDate());
			Data developmentmanager = new Data(Integer.parseInt(developmentmanagerObjects.get(i).getPk()),
						developmentmanagerObjects.get(i).getName(),
						developmentmanagerObjects.get(i).getAge(),
						developmentmanagerObjects.get(i).getGender(),
						developmentmanagerObjects.get(i).getHireDate(),
						developmentmanagerObjects.get(i).getPhoneNo(),
						developmentmanagerObjects.get(i).getAddress(),
						developmentmanagerObjects.get(i).getSpeciality(),r,
						developmentmanagerObjects.get(i).getStartDay(),
						developmentmanagerObjects.get(i).getEquipmentHolderId(),
						developmentmanagerObjects.get(i).getSalary());
			developmentmanagers.add(developmentmanager);
		}
		
		return developmentmanagers;
	}
	
	@Override
	public List getListingOnline(String json){
		return this.serialize(this.asArrayOfData(json));		
	}
	
	public List getDevelopmentManagersListingOffline(){
		BaseData.dbOpen();
		List developmentmanagers = new ArrayList();
		RegionsData region = new RegionsData();
		this.select(listDevelopmentManagers);
		if (this.getResultSet().isValidRow()){
			try {
				for (int i = 0; this.getResultSet().isValidRow(); ++i, this.getResultSet().next()) {
					RegionsData.Data r = region.new Data(this.getResultSet().getFieldAsInt(8),  this.getResultSet().getFieldAsString(9)) ;
					Data developmentmanager = new Data(this.getResultSet().getFieldAsInt(0), 
							this.getResultSet().getFieldAsString(1),
							this.getResultSet().getFieldAsString(2),
							this.getResultSet().getFieldAsString(3),
							this.getResultSet().getFieldAsString(4),
							this.getResultSet().getFieldAsString(5),
							this.getResultSet().getFieldAsString(6),
							this.getResultSet().getFieldAsString(7),r,
							this.getResultSet().getFieldAsString(10),
							this.getResultSet().getFieldAsInt(11),
							this.getResultSet().getFieldAsFloat(12));
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
					Data developmentmanager = new Data(this.getResultSet().getFieldAsInt(0), this.getResultSet().getFieldAsString(1));
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
			this.post(RequestContext.SERVER_HOST + DevelopmentManagersData.saveDevelopmentManagerOnlineURL, this.queryString);
		}
		else{
			this.save();
			return true;
		}
		
		return false;
	}
	
	public Object getListPageData(){
		if(BaseData.isOnline()){
			this.get(RequestContext.SERVER_HOST + DevelopmentManagersData.getDevelopmentManagerOnlineURL);
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
		String html = "<select name=\"region\" id=\"id_region\">";
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
	
}
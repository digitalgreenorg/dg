package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.LanguagesData.Data;
import com.google.gwt.core.client.JsArray;
import com.google.gwt.gears.client.database.DatabaseException;
import com.google.gwt.user.client.Window;

public class FieldOfficersData extends BaseData {
	
	public static class Type extends BaseData.Type{
		protected Type(){}
		
		public final native String getFieldOfficerName() /*-{ return this.fields.name; }-*/;
		public final native String getAge() /*-{ return this.fields.age; }-*/;
		public final native String getGender() /*-{ return this.fields.gender; }-*/;
		public final native String getHireDate() /*-{ return this.fields.hire_date; }-*/;
		public final native String getSalary() /*-{ return this.fields.salary; }-*/;
		public final native String getPhone() /*-{ return this.fields.phone_no; }-*/;
		public final native String getAddress() /*-{ return this.fields.address; }-*/;
		public final native ReviewersData.Type getReviewer() /*-{ return this.fields.reviewer; }-*/;
		public final native EquipmentHoldersData.Type getEquipmentHolder() /*-{ return this.fields.equipmentholder; }-*/;
	}
	
	public class Data extends BaseData.Data{
		
		final private static String COLLECTION_PREFIX = "fieldOfficers";
		
		private String name;
		private String age;
		private String gender;
		private String hire_date;
		private String salary;
		private String phone_no;
		private String address;
		private ReviewersData.Data reviewer;
		private EquipmentHoldersData.Data equipmentholder;
		
		public Data(){
			super();
		}
		
		public Data(String id, String name){
			super();
			this.id = id;
			this.name = name;
		}
		
		public Data(String id, String name, String age, String gender, String hire_date, 
				String salary, String phone_no, String address, ReviewersData.Data reviewer, EquipmentHoldersData.Data equipmentholder){
			super();
			this.id = id;
			this.name = name;
			this.age = age;
			this.gender = gender;
			this.hire_date = hire_date;
			this.salary = salary;
			this.phone_no = phone_no;
			this.address = address;
			this.reviewer = reviewer;
			this.equipmentholder = equipmentholder;
		}
		

		public String getFieldOfficerName(){
			return this.name;
		}
		
		public BaseData.Data clone(){
			Data obj = new Data();
			obj.id = this.id;
			obj.name = this.name;
			obj.age = this.age;
			obj.gender = this.gender;
			obj.hire_date = this.hire_date;
			obj.salary = this.salary;
			obj.phone_no = this.phone_no;
			obj.address = this.address;
			obj.reviewer = this.reviewer;
			obj.equipmentholder = this.equipmentholder;
			return obj;
		}

		@Override
		public String getPrefixName(){
			return Data.COLLECTION_PREFIX;
		}
		
		@Override
		public void setObjValueFromString(String key, String val){
			super.setObjValueFromString(key, val);
			if(key.equals("id")){
				this.id = val;
			} else if(key.equals("name")){
				this.name = (String)val;
			}
			else if(key.equals("age")){
				this.age = (String)val;
			}
			else if(key.equals("gender")){
				this.gender = (String)val;
			}
			else if(key.equals("hire_date")){
				this.hire_date = (String)val;
			}
			else if(key.equals("salary")){
				this.salary = val;
			}
			else if(key.equals("phone_no")){
				this.phone_no = (String)val;
			}
			else if(key.equals("address")){
				this.address = (String)val;
			}
			else if(key.equals("reviewer")) {
				ReviewersData reviewer = new ReviewersData();
				this.reviewer = reviewer.getNewData();
				 this.reviewer.id = val;
			}
			else if(key.equals("equipmentholder")) {
				EquipmentHoldersData equipmentholder = new EquipmentHoldersData();
				this.equipmentholder = equipmentholder.getNewData();
				this.equipmentholder.id = val;
			}
		}

		@Override
		public void save(){
			FieldOfficersData fieldOfficersDataDbApis = new FieldOfficersData();
			if(this.id == null){
				this.id = fieldOfficersDataDbApis.autoInsert(this.name, 
						this.age, 
						this.gender, 
						this.hire_date, 
						this.salary, 
						this.phone_no, 
						this.address, 
						this.reviewer.id, 
						this.equipmentholder.id);
			}
			else {
				this.id = fieldOfficersDataDbApis.autoInsert(this.id,
						this.name, 
						this.age, 
						this.gender, 
						this.hire_date, 
						this.salary, 
						this.phone_no, 
						this.address, 
						this.reviewer.getId(),
						this.equipmentholder.getId());
			}	
		}
	}
	
	protected static String tableID = "7";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `field_officer` " +
												"(id INTEGER PRIMARY KEY NOT NULL ," +
												"NAME VARCHAR(100) NOT NULL ," +
												"AGE INT NULL DEFAULT NULL," +
												"GENDER VARCHAR(1) NOT NULL ," +
												"HIRE_DATE DATE NULL DEFAULT NULL," +
												"SALARY FLOAT(0,0) NULL DEFAULT NULL," +
												"PHONE_NO VARCHAR(100) NOT NULL ," +
												"ADDRESS VARCHAR(500) NOT NULL ," +
												"reviewer_id INT NULL DEFAULT NULL," +
												"equipmentholder_id INT NULL DEFAULT NULL, " +
												"FOREIGN KEY(reviewer_id) REFERENCES reviewer(id), " +
												"FOREIGN KEY(equipmentholder_id) REFERENCES equipment_holder(id))";
	
	protected static String selectFieldOfficers = "SELECT id, name FROM field_officer ORDER BY(name);";
	protected static String listFieldOfficers = "SELECT * FROM field_officer ORDER BY (-id)";
	protected static String saveFieldOfficerOnlineURL = "/dashboard/savefieldofficeronline/";
	protected static String getFieldOfficersOnlineURL = "/dashboard/getfieldofficersonline/";
	protected static String saveFieldOfficerOfflineURL = "/dashboard/savefieldofficeroffline/";
	protected static String table_name = "field_officer";
	protected static String[] fields = {"id", "name", "age", "gender", "hire_date", "salary",  "phone_no", "address", "reviewer_id", "equipmentholder_id"};
	
	public FieldOfficersData(){
		super();
	}
	
	public FieldOfficersData(OnlineOfflineCallbacks callbacks){
		super(callbacks);
	}
	
	public FieldOfficersData(OnlineOfflineCallbacks callbacks, Form form, String queryString){
		super(callbacks, form, queryString);
	}
	
	@Override
	public Data getNewData() {
		return new Data();
	}
	
	@Override
	protected String getTableId() {
		return FieldOfficersData.tableID;
	}
	
	@Override
	protected String getTableName() {
		return FieldOfficersData.table_name;
	}
	
	@Override
	protected String[] getFields() {
		return FieldOfficersData.fields;
	}
	
	@Override
	public String getListingOnlineURL(){
		return FieldOfficersData.getFieldOfficersOnlineURL;
	}
	
	
	public final native JsArray<Type> asArrayOfData(String json) /*-{
		return eval(json);
	}-*/;
	
	public List serialize(JsArray<Type> fieldOfficerObjects){
		List fieldOfficers = new ArrayList();
		ReviewersData reviewer = new ReviewersData();
		EquipmentHoldersData equipmentholder = new EquipmentHoldersData();
		for(int i = 0; i < fieldOfficerObjects.length(); i++){
			ReviewersData.Data r = reviewer.new Data(fieldOfficerObjects.get(i).getReviewer().getPk());
			
			EquipmentHoldersData.Data eq = equipmentholder.new Data(fieldOfficerObjects.get(i).getEquipmentHolder().getPk());
			
			Data fieldOfficer = new Data(fieldOfficerObjects.get(i).getPk(), 
					fieldOfficerObjects.get(i).getFieldOfficerName(), 
					fieldOfficerObjects.get(i).getAge(), 
					fieldOfficerObjects.get(i).getGender(), 
					fieldOfficerObjects.get(i).getHireDate(), 
					fieldOfficerObjects.get(i).getSalary(), 
					fieldOfficerObjects.get(i).getPhone(), 
					fieldOfficerObjects.get(i).getAddress(), 
					r, eq);
			fieldOfficers.add(fieldOfficer);
		}
		return fieldOfficers;
	}
	
	@Override
	public List getListingOnline(String json){
		return this.serialize(this.asArrayOfData(json));
	}
	
	public List getFieldOfficersListingOffline(){
		BaseData.dbOpen();
		ReviewersData reviewer = new ReviewersData();
		EquipmentHoldersData equipmentholder = new EquipmentHoldersData();
		List fieldOfficers = new ArrayList();
		this.select(listFieldOfficers);
		if(this.getResultSet().isValidRow()){
			try {
				for(int i = 0; this.getResultSet().isValidRow(); ++i, this.getResultSet().next()){
					
					ReviewersData.Data r = reviewer.new Data(this.getResultSet().getFieldAsString(8));
					
					EquipmentHoldersData.Data eq = equipmentholder.new Data(this.getResultSet().getFieldAsString(9));
					
					Data fieldOfficer = new Data(this.getResultSet().getFieldAsString(0), this.getResultSet().getFieldAsString(1), 
							this.getResultSet().getFieldAsString(2), this.getResultSet().getFieldAsString(3), 
							this.getResultSet().getFieldAsString(4), this.getResultSet().getFieldAsString(5), 
							this.getResultSet().getFieldAsString(6), this.getResultSet().getFieldAsString(7), 
							r, eq);
					fieldOfficers.add(fieldOfficer);
				}
			} catch (DatabaseException e){
				Window.alert("Database Exception: " + e.toString());
				BaseData.dbClose();
			}
		}
		BaseData.dbClose();		
		return fieldOfficers;
	}

	
	public List getAllFieldOfficersOffline(){
		BaseData.dbOpen();

		List fieldofficers = new ArrayList();
		this.select(selectFieldOfficers);
		if (this.getResultSet().isValidRow()){
			try {
				for (int i = 0; this.getResultSet().isValidRow(); ++i, this.getResultSet().next()) {
					Data fieldofficer = new Data(this.getResultSet().getFieldAsString(0), this.getResultSet().getFieldAsString(1));
					fieldofficers.add(fieldofficer);
	    	      }				
			} catch (DatabaseException e) {
				Window.alert("Database Exception : " + e.toString());
				// TODO Auto-generated catch block
				BaseData.dbClose();
			}
			
		}
		BaseData.dbClose();
		return fieldofficers;
	}
	


	public Object postPageData() {
		if(BaseData.isOnline()){
			this.post(RequestContext.SERVER_HOST + this.saveFieldOfficerOnlineURL, this.queryString);
		}
		else {
			this.save();
			return true;
		}
		return false;
	}
	
	public Object getPageData(){
		if(BaseData.isOnline()){
			this.get(RequestContext.SERVER_HOST + FieldOfficersData.getFieldOfficersOnlineURL);
		}
		else{
			return true;
		}
		return false;
	}
}
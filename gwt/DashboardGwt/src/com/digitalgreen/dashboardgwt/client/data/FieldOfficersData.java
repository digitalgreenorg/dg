package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
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
		public final native float getSalary() /*-{ return this.fields.salary; }-*/;
		public final native String getPhone() /*-{ return this.fields.phone_no; }-*/;
		public final native String getAddress() /*-{ return this.fields.address; }-*/;
		public final native int getReviewerId() /*-{ return this.fields.reviewer_id; }-*/;
		public final native int getEquipmentHolderId() /*-{ return this.fields.equipmentholder_id; }-*/;
	}
	
	public class Data extends BaseData.Data{
		
		final private static String COLLECTION_PREFIX = "fieldOfficers";
		
		private String name;
		private String age;
		private String gender;
		private String hire_date;
		private float salary;
		private String phone_no;
		private String address;
		private int reviewer_id;
		private int equipmentholder_id;
		
		public Data(){
			super();
		}
		
		public Data(int id, String name, String age, String gender, String hire_date, 
				float salary, String phone_no, String address, int reviewer_id, int equipmentholder_id){
			super();
			this.id = id;
			this.name = name;
			this.age = age;
			this.gender = gender;
			this.hire_date = hire_date;
			this.salary = salary;
			this.phone_no = phone_no;
			this.address = address;
			this.reviewer_id = reviewer_id;
			this.equipmentholder_id = equipmentholder_id;
		}
		
		public String getFieldOfficerName(){
			return this.name;
		}
		
		public Object clone(){
			Data obj = new Data();
			obj.id = this.id;
			obj.name = this.name;
			obj.age = this.age;
			obj.gender = this.gender;
			obj.hire_date = this.hire_date;
			obj.salary = this.salary;
			obj.phone_no = this.phone_no;
			obj.address = this.address;
			obj.reviewer_id  =this.reviewer_id;
			obj.equipmentholder_id = this.equipmentholder_id;
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
				this.salary = ((Float)val).floatValue();
			}
			else if(key.equals("phone_no")){
				this.phone_no = (String)val;
			}
			else if(key.equals("address")){
				this.address = (String)val;
			}
			else if(key.equals("reviewer_id")) {
				 this.reviewer_id = ((Integer)val).intValue();
			}
			else if(key.equals("equipmentholder_id")) {
				this.equipmentholder_id = ((Integer)val).intValue();
			}
		}

		@Override
		public void save(){
			FieldOfficersData fieldOfficersDataDbApis = new FieldOfficersData();
			this.id = fieldOfficersDataDbApis.autoInsert(this.name, this.age, this.gender, this.hire_date, 
					Float.valueOf(this.salary).toString(), this.phone_no, this.address, Integer.valueOf(this.reviewer_id).toString(), 
					Integer.valueOf(this.equipmentholder_id).toString());
			
		}
	}
	
	protected static String tableID = "07";
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
	protected static String listFieldOfficers = "SELECT * FROM field_officer ORDER BY (-id)";
	protected static String saveFieldOfficerURL = "/dashboard/savefieldofficer/";
	protected static String getFieldOfficersURL = "/dashboard/getfieldofficers/";
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
	
	public final native JsArray<Type> asArrayOfData(String json) /*-{
		return eval(json);
	}-*/;
	
	public List serialize(JsArray<Type> fieldOfficerObjects){
		List fieldOfficers = new ArrayList();
		for(int i = 0; i < fieldOfficerObjects.length(); i++){
			Data fieldOfficer = new Data(Integer.parseInt(fieldOfficerObjects.get(i).getPk()), fieldOfficerObjects.get(i).getFieldOfficerName(), 
					fieldOfficerObjects.get(i).getAge(), fieldOfficerObjects.get(i).getGender(), fieldOfficerObjects.get(i).getHireDate(), 
					fieldOfficerObjects.get(i).getSalary() ,fieldOfficerObjects.get(i).getPhone(), fieldOfficerObjects.get(i).getAddress(), 
					fieldOfficerObjects.get(i).getReviewerId(), fieldOfficerObjects.get(i).getEquipmentHolderId());
			fieldOfficers.add(fieldOfficer);
		}
		return fieldOfficers;
	}
	
	public List getFieldOfficersOnline(String json){
		return this.serialize(this.asArrayOfData(json));
	}
	
	public List getFieldOfficersOffline(){
		BaseData.dbOpen();
		List fieldOfficers = new ArrayList();
		this.select(listFieldOfficers);
		if(this.getResultSet().isValidRow()){
			try {
				for(int i = 0; this.getResultSet().isValidRow(); ++i, this.getResultSet().next()){
					Data fieldOfficer = new Data(this.getResultSet().getFieldAsInt(0), this.getResultSet().getFieldAsString(1), 
							this.getResultSet().getFieldAsString(2), this.getResultSet().getFieldAsString(3), 
							this.getResultSet().getFieldAsString(4), this.getResultSet().getFieldAsFloat(5), 
							this.getResultSet().getFieldAsString(6), this.getResultSet().getFieldAsString(7), 
							this.getResultSet().getFieldAsInt(8), this.getResultSet().getFieldAsInt(9));
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

	public Object postPageData() {
		if(BaseData.isOnline()){
			this.post(RequestContext.SERVER_HOST + this.saveFieldOfficerURL, this.queryString);
		}
		else {
			this.save();
			return true;
		}
		return false;
	}
	
	public Object getPageData(){
		if(BaseData.isOnline()){
			this.get(RequestContext.SERVER_HOST + FieldOfficersData.getFieldOfficersURL);
		}
		else{
			return true;
		}
		return false;
	}
}
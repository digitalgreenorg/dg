package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.PersonAdoptPracticeData.Data;
import com.digitalgreen.dashboardgwt.client.data.PersonAdoptPracticeData.Type;
import com.google.gwt.core.client.JsArray;
import com.google.gwt.gears.client.database.DatabaseException;
import com.google.gwt.user.client.Window;

public class PersonAdoptPracticeData extends BaseData{
	
	public static class Type extends BaseData.Type{
		protected Type() {}
		public final native String getPerson() /*-{ return this.fields.person }-*/;
		public final native String getPractice() /*-{ return this.fields.practice }-*/;
		public final native String getPriorAdoptionFlag() /*-{ return $wnd.checkForNullValues(this.fields.prior_adoption_flag); }-*/;
		public final native String getDateOfAdoption() /*-{ return $wnd.checkForNullValues(this.fields.date_of_adoption); }-*/;
		public final native String getQuality() /*-{ return $wnd.checkForNullValues(this.fields.quality); }-*/;
		public final native String getQuantity() /*-{ return $wnd.checkForNullValues(this.fields.quantity); }-*/;
		public final native String getQuantityUnit() /*-{ return $wnd.checkForNullValues(this.fields.quantity_unit); }-*/;
	}
	
public class Data extends BaseData.Data {
		
		final private static String COLLECTION_PREFIX = "personadoptpractice";
			
		private PersonsData.Data person;
		private PracticesData.Data practice;
		private String prior_adoption_flag;
		private String date_of_adoption;
		private String quality;
		private String quantity;
		private String quantity_unit;		
		
		public Data() {
			super();
		}
		
		public Data(String id, String date_of_adoption) {
			super();
			this.id = id;
			this.date_of_adoption = date_of_adoption;
		}		

		public Data(String id,PersonsData.Data person, PracticesData.Data practice, String prior_adoption_flag,String date_of_adoption,
				String quality,String quantity,String quantity_unit) {
			super();
			this.id = id;
			this.person = person;
			this.practice = practice;
			this.prior_adoption_flag = prior_adoption_flag;
			this.date_of_adoption = date_of_adoption;
			this.quality = quality;
			this.quantity = quantity;
			this.quantity_unit = quantity_unit;
			
		}		
		
		public PersonsData.Data getPerson(){
			return this.person;
		}
		
		public PracticesData.Data getPractice(){
			return this.practice;
		}
		
		public String getPriorAdoptionFlag(){
			return this.prior_adoption_flag;
		}
		
		public String getDateOfAdoption(){
			return this.date_of_adoption;
		}
		
		public String getQuality(){
			return this.quality;
		}
		public String getQuantity(){
			return this.quantity;
		}
		public String getQuantityUnit(){
			return this.quantity_unit;
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
			if(key.equals("person")) {
				PersonsData person = new PersonsData();
				this.person = person.getNewData();
				this.person.id = val;
			} else if(key.equals("practice")) {
				PracticesData practice = new PracticesData();
				this.practice = practice.getNewData();
				this.practice.id = val;
			}  else if(key.equals("prior_adoption_flag")) {
				this.prior_adoption_flag = (String)val;
			}	else if(key.equals("date_of_adoption")) {
				this.date_of_adoption = (String)val;
			}	else if(key.equals("quality")) {
				this.quality = (String)val;
			}	else if(key.equals("quantity")) {
				this.quantity = (String)val;
			}	else if(key.equals("quantity_unit")) {
				this.quantity_unit = (String)val;
			}	else {
				return;
			}
			this.addNameValueToQueryString(key, val);	
		}
		
		@Override
		public void save() {
			PersonAdoptPracticeData personAdoptPracticesDataDbApis = new PersonAdoptPracticeData();
			this.id = personAdoptPracticesDataDbApis.autoInsert(this.id,
					this.person.getId(),
					this.practice.getId(),
					this.prior_adoption_flag,
					this.date_of_adoption,
					this.quality,
					this.quantity,
					this.quantity_unit);
			this.addNameValueToQueryString("id", this.id);
		}
		
		@Override
		public void save(BaseData.Data foreignKey) {
			PersonAdoptPracticeData personAdoptPracticesDataDbApis = new PersonAdoptPracticeData();
			this.id = personAdoptPracticesDataDbApis.autoInsert(this.id,
					foreignKey.getId(),
					this.practice.getId(),
					this.prior_adoption_flag,
					this.date_of_adoption,
					this.quality,
					this.quantity,
					this.quantity_unit);
			this.addNameValueToQueryString("id", this.id);
			this.addNameValueToQueryString("person", foreignKey.getId());
		}
		
		@Override
		public String getTableId() {
			PersonAdoptPracticeData personAdoptPracticesDataDbApis = new PersonAdoptPracticeData();
			return personAdoptPracticesDataDbApis.tableID;
		}
	}

	protected static String tableID = "29";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `person_adopt_practice` " +
												"(id INTEGER PRIMARY KEY  NOT NULL ," +
												"person_id INT  NOT NULL DEFAULT 0," +
												"practice_id INT  NOT NULL DEFAULT 0," +
												"PRIOR_ADOPTION_FLAG SMALLINT  NULL DEFAULT NULL," +
												"DATE_OF_ADOPTION DATE NOT NULL," +
												"QUALITY VARCHAR(200)  NULL DEFAULT NULL ," +
												"QUANTITY INT  NULL DEFAULT NULL," +
												"QUANTITY_UNIT VARCHAR(150)  NULL DEFAULT NULL, " +
												"FOREIGN KEY(person_id) REFERENCES person(id), " +
												"FOREIGN KEY(practice_id) REFERENCES practices(id));";

	protected static String selectPersonAdoptPractices = "SELECT id, date_of_adoption FROM person_adopt_practice ORDER BY (date_of_adoption);";
	protected static String listPersonAdoptPractices = "SELECT pap.id,p.id,p.person_name,pr.id,pr.practice_name, pap.DATE_OF_ADOPTION," +
			"pap.prior_adoption_flag,pap.quality, pap.quantity, pap.quantity_unit FROM " +
			"person_adopt_practice pap JOIN person p ON p.id = pap.person_id JOIN practices pr ON pr.id = pap.practice_id ORDER BY (-pap.id);";
	protected static String savePersonAdoptPracticeOnlineURL = "/dashboard/savepersonadoptpracticeonline/";
	protected static String getPersonAdoptPracticeOnlineURL = "/dashboard/getpersonadoptpracticesonline/";
	protected static String savePersonAdoptPracticeOfflineURL = "/dashboard/savepersonadoptpracticeoffline/";
	protected String table_name = "person_adopt_practice";
	protected String[] fields = {"id", "person_id", "practice_id", "prior_adoption_flag", 
			"date_of_adoption","quality","quantity","quantity_unit"};
		
	
	public PersonAdoptPracticeData(){
		super();
	}
	
	public PersonAdoptPracticeData(OnlineOfflineCallbacks callbacks) {
		super(callbacks);
	}
	
	public PersonAdoptPracticeData(OnlineOfflineCallbacks callbacks, Form form) {
		super(callbacks, form);
	}

	@Override
	public Data getNewData() {
		return new Data();
	}
	
	@Override
	protected String getTableId() {
		return PersonAdoptPracticeData.tableID;
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
		return PersonAdoptPracticeData.getPersonAdoptPracticeOnlineURL;
	}
	
	@Override
	public String getSaveOfflineURL(){
		return PersonAdoptPracticeData.savePersonAdoptPracticeOfflineURL;
	}
		
		
	public final native JsArray<Type> asArrayOfData(String json) /*-{
		return eval(json);
	}-*/;
	
	public List serialize(JsArray<Type> personAdoptPracticeObjects){
		List personAdoptPractices = new ArrayList();
		PersonsData person = new PersonsData();
		PracticesData practice = new PracticesData();
		for(int i = 0; i < personAdoptPracticeObjects.length(); i++){
			PersonsData.Data p = person.new Data(personAdoptPracticeObjects.get(i).getPerson());
			PracticesData.Data pr = practice.new Data(personAdoptPracticeObjects.get(i).getPractice());
			
			Data personAdoptPractice = new Data(personAdoptPracticeObjects.get(i).getPk(),p,pr, 
					personAdoptPracticeObjects.get(i).getPriorAdoptionFlag(), personAdoptPracticeObjects.get(i).getDateOfAdoption(),
					personAdoptPracticeObjects.get(i).getQuantity(),personAdoptPracticeObjects.get(i).getQuality(),
					personAdoptPracticeObjects.get(i).getQuantityUnit());
			personAdoptPractices.add(personAdoptPractice);
		}
		
		return personAdoptPractices;
	}
		
	public List getPersonAdoptPracticesListingOffline(){
		BaseData.dbOpen();
		List personAdoptPractices = new ArrayList();
		PersonsData person = new PersonsData();
		PracticesData practice = new PracticesData();
		this.select(listPersonAdoptPractices);
		if (this.getResultSet().isValidRow()){
			try {
				for (int i = 0; this.getResultSet().isValidRow(); ++i, this.getResultSet().next()) {
					PersonsData.Data p = person.new Data(this.getResultSet().getFieldAsString(1),  this.getResultSet().getFieldAsString(2));
					PracticesData.Data pr = practice.new Data(this.getResultSet().getFieldAsString(3),  this.getResultSet().getFieldAsString(4));
					Data personAdoptPractice = new Data(this.getResultSet().getFieldAsString(0), p,pr,this.getResultSet().getFieldAsString(5),
							this.getResultSet().getFieldAsString(6),this.getResultSet().getFieldAsString(7),this.getResultSet().getFieldAsString(8),
							this.getResultSet().getFieldAsString(9));
					personAdoptPractices.add(personAdoptPractice);
	    	      }				
			} catch (DatabaseException e) {
				Window.alert("Database Exception : " + e.toString());
				// TODO Auto-generated catch block
				BaseData.dbClose();
			}
			
		}
		BaseData.dbClose();
		return personAdoptPractices;
	}

	@Override
	public List getListingOnline(String json){
		return this.serialize(this.asArrayOfData(json));		
	}
	
	public List getAllPersonAdoptPracticesOffline(){
		BaseData.dbOpen();
		List personAdoptPractices = new ArrayList();
		this.select(selectPersonAdoptPractices);
		if (this.getResultSet().isValidRow()){
			try {
				for (int i = 0; this.getResultSet().isValidRow(); ++i, this.getResultSet().next()) {
					Data personAdoptPractice = new Data(this.getResultSet().getFieldAsString(0), this.getResultSet().getFieldAsString(1));
					personAdoptPractices.add(personAdoptPractice);
	    	      }				
			} catch (DatabaseException e) {
				Window.alert("Database Exception : " + e.toString());
				// TODO Auto-generated catch block
				BaseData.dbClose();
			}
			
		}
		BaseData.dbClose();
		return personAdoptPractices;
	}
	
	
	public Object postPageData() {
		if(BaseData.isOnline()){
			this.post(RequestContext.SERVER_HOST + PersonAdoptPracticeData.savePersonAdoptPracticeOnlineURL, this.form.getQueryString());
		}
		else{
			this.save();
			return true;
		}
		
		return false;
	}
	
	public Object getListPageData(){
		if(BaseData.isOnline()){
			this.get(RequestContext.SERVER_HOST + PersonAdoptPracticeData.getPersonAdoptPracticeOnlineURL);
		}
		else{
			return true;
		}
		return false;
	}	
	
	public Object getAddPageData(){
		if(BaseData.isOnline()){
			this.get(RequestContext.SERVER_HOST + PersonAdoptPracticeData.savePersonAdoptPracticeOnlineURL);
		}
		return false;
	}
}

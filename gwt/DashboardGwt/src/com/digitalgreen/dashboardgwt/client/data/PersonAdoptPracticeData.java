package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.PersonAdoptPracticeData.Data;
import com.digitalgreen.dashboardgwt.client.data.PersonAdoptPracticeData.Type;
import com.google.gwt.core.client.JsArray;

public class PersonAdoptPracticeData extends BaseData{
	
	public static class Type extends BaseData.Type{
		protected Type() {}
		public final native PersonsData.Type getPerson() /*-{ return this.fields.person }-*/;
		public final native PracticesData.Type getPractice() /*-{ return this.fields.practice }-*/;
		public final native String getPriorAdoptionFlag() /*-{ return this.fields.prior_adoption_flag; }-*/;
		public final native String getDateOfAdoption() /*-{ return this.fields.date_of_adoption; }-*/;
		public final native String getQuality() /*-{ return this.fields.quality; }-*/;
		public final native String getQuantity() /*-{ return this.fields.quantity; }-*/;
		public final native String getQuantityUnit() /*-{ return this.fields.quantity_unit; }-*/;
	}
	
public class Data extends BaseData.Data {
		
		final private static String COLLECTION_PREFIX = "personAdoptPractice";
			
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
		
		public Data(int id, String date_of_adoption) {
			super();
			this.id = id;
			this.date_of_adoption = date_of_adoption;
		}
		

		public Data(int id,PersonsData.Data person, PracticesData.Data practice, String prior_adoption_flag,String date_of_adoption,
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
			obj.id = this.id;
			obj.person = (PersonsData.Data)this.person.clone();
			obj.practice = (PracticesData.Data)this.practice.clone();
			obj.prior_adoption_flag = this.prior_adoption_flag;
			obj.date_of_adoption = this.date_of_adoption;
			obj.quality = this.quality;
			obj.quantity = this.quantity;
			obj.quantity_unit = this.quantity_unit;
			
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
			} else if(key.equals("person")) {
				PersonsData person = new PersonsData();
				this.person = person.getNewData();
				this.person.id = Integer.parseInt((String)val);
			} else if(key.equals("practice")) {
				PracticesData practice = new PracticesData();
				this.practice = practice.getNewData();
				this.practice.id = Integer.parseInt((String)val);
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
			}		
		}
		
		@Override
		public void save() {
			PersonAdoptPracticeData personAdoptPracticesDataDbApis = new PersonAdoptPracticeData();		
			if(this.id==0){
				this.id = personAdoptPracticesDataDbApis.autoInsert( Integer.valueOf(this.person.getId()).toString(),
						Integer.valueOf(this.practice.getId()).toString(), this.prior_adoption_flag,this.date_of_adoption,this.quality,
						this.quantity,this.quantity_unit);
			}else{
				this.id = personAdoptPracticesDataDbApis.autoInsert( Integer.valueOf(this.id).toString(), Integer.valueOf(this.person.getId()).toString(),
						Integer.valueOf(this.practice.getId()).toString(), this.prior_adoption_flag,this.date_of_adoption,this.quality,
						this.quantity,this.quantity_unit);
			}
			
		}
	}


	protected static String tableID = "29";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `person_adopt_practice` " +
												"(id INTEGER PRIMARY KEY  NOT NULL ," +
												"person_id INT  NOT NULL DEFAULT 0," +
												"practice_id INT  NOT NULL DEFAULT 0," +
												"PRIOR_ADOPTION_FLAG SMALLINT  NULL DEFAULT NULL," +
												"DATE_OF_ADOPTION DATE  NULL DEFAULT NULL," +
												"QUALITY VARCHAR(200)  NOT NULL ," +
												"QUANTITY INT  NULL DEFAULT NULL," +
												"QUANTITY_UNIT VARCHAR(150)  NOT NULL, " +
												"FOREIGN KEY(person_id) REFERENCES person(id), " +
												"FOREIGN KEY(practice_id) REFERENCES practices(id));";

	protected static String selectPersonAdoptPractices = "SELECT id, date_of_adoption FROM person_adopt_practice ORDER BY (date_of_adoption);";
	protected static String listPersonAdoptPractices = "SELECT * FROM person_adopt_practice pap JOIN person p ON p.id = pap.person_id" +
			"JOIN practice pr ON pr.id = pap.practice_id ORDER BY (-pap.id);";
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
	
	public PersonAdoptPracticeData(OnlineOfflineCallbacks callbacks, Form form, String queryString) {
		super(callbacks, form, queryString);
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
		
		
	public final native JsArray<Type> asArrayOfData(String json) /*-{
		return eval(json);
	}-*/;
	
	public List serialize(JsArray<Type> personAdoptPracticeObjects){
		List personAdoptPractices = new ArrayList();
		PersonsData person = new PersonsData();
		PracticesData practice = new PracticesData();
		for(int i = 0; i < personAdoptPracticeObjects.length(); i++){
			PersonsData.Data p = person.new Data(Integer.parseInt(personAdoptPracticeObjects.get(i).getPerson().getPk()),
					personAdoptPracticeObjects.get(i).getPerson().getPersonName());
			PracticesData.Data pr = practice.new Data(Integer.parseInt(personAdoptPracticeObjects.get(i).getPractice().getPk()),
					personAdoptPracticeObjects.get(i).getPractice().getPracticeName());
			
			Data personAdoptPractice = new Data(Integer.parseInt(personAdoptPracticeObjects.get(i).getPk()),p,pr, 
					personAdoptPracticeObjects.get(i).getPriorAdoptionFlag(), personAdoptPracticeObjects.get(i).getDateOfAdoption(),
					personAdoptPracticeObjects.get(i).getQuantity(),personAdoptPracticeObjects.get(i).getQuality(),
					personAdoptPracticeObjects.get(i).getQuantityUnit());
			personAdoptPractices.add(personAdoptPractice);
		}
		
		return personAdoptPractices;
	}
	
	@Override
	public List getListingOnline(String json){
		return this.serialize(this.asArrayOfData(json));		
	}
}

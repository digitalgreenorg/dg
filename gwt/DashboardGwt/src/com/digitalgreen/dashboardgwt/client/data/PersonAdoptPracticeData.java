package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.PersonAdoptPracticeData.Data;
import com.digitalgreen.dashboardgwt.client.data.PersonAdoptPracticeData.Type;
import com.digitalgreen.dashboardgwt.client.data.validation.DateValidator;
import com.digitalgreen.dashboardgwt.client.data.validation.IntegerValidator;
import com.digitalgreen.dashboardgwt.client.data.validation.StringValidator;
import com.digitalgreen.dashboardgwt.client.data.validation.UniqueConstraintValidator;
import com.digitalgreen.dashboardgwt.client.servlets.PersonAdoptPractices;
import com.google.gwt.core.client.JsArray;
import com.google.gwt.gears.client.database.DatabaseException;
import com.google.gwt.user.client.Window;
import com.google.web.bindery.event.shared.UmbrellaException;

public class PersonAdoptPracticeData extends BaseData{
	
	public static class Type extends BaseData.Type{
		protected Type() {}
		public final native PersonsData.Type getPerson() /*-{ return this.fields.person }-*/;
		public final native PracticesData.Type getPractice() /*-{ return this.fields.practice }-*/;
		public final native PersonGroupsData.Type getGroup() /*-{ return this.fields.person.fields.group }-*/;
		public final native VillagesData.Type getVillage() /*-{ return this.fields.person.fields.village }-*/;
		public final native String getPriorAdoptionFlag() /*-{ return $wnd.checkForNullValues(this.fields.prior_adoption_flag); }-*/;
		public final native String getDateOfAdoption() /*-{ return $wnd.checkForNullValues(this.fields.date_of_adoption); }-*/;
		public final native String getQuality() /*-{ return $wnd.checkForNullValues(this.fields.quality); }-*/;
		public final native String getQuantity() /*-{ return $wnd.checkForNullValues(this.fields.quantity); }-*/;
		public final native String getQuantityUnit() /*-{ return $wnd.checkForNullValues(this.fields.quantity_unit); }-*/;
	}
	
public class Data extends BaseData.Data {
		
		final private static String COLLECTION_PREFIX = "personadoptpractice";
		private PersonsData.Data person;
		private VillagesData.Data village;
		private PersonGroupsData.Data group;
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

		public Data(String id,PersonsData.Data person, PracticesData.Data practice,PersonGroupsData.Data group, VillagesData.Data village, 
				String prior_adoption_flag,String date_of_adoption,
				String quality,String quantity,String quantity_unit) {
			super();
			this.id = id;
			this.person = person;
			this.practice = practice;
			this.group = group;
			this.village = village;
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
		
		public VillagesData.Data getVillage(){
			return this.village;
		}
		public PersonGroupsData.Data getGroup(){
			return this.group;
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
			obj.person = (new PersonsData()).new Data();
			obj.practice = (new PracticesData()).new Data();
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
			}else if(key.equals("person")) {
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
		
		//This method is to check for multiple inlines with  same data.
		@Override
		public boolean compare(BaseData.Data other) {
			if(other instanceof PersonAdoptPracticeData.Data) {
				PersonAdoptPracticeData.Data obj = (PersonAdoptPracticeData.Data) other;
				if(this.date_of_adoption.equals(obj.getDateOfAdoption()) 
						&& this.practice.getId().equals(obj.getPractice().getId()) ) {
					errorStack.add("Person adopted two same practices on same date");
					return true;
				} else
					return false;
			} else
				return false;
		}
		@Override
		public boolean validate() {
			String personLabel = "Person";
			String practiceLabel = "Practice";
			String dateOfAdoptionLabel = "DateOfAdoption";
			String qualityLabel = "Quality";
			String quantityLabel = "Quantity";
			String quantityUnitLabel = "Quantity Unit";
			StringValidator personValidator = new StringValidator(personLabel,this.person.getId(), false, false, 1, 100);
			StringValidator practiceValidator = new StringValidator(practiceLabel, this.practice.getId(), false, false, 1, 100);
			DateValidator dateOfAdoption = new DateValidator(dateOfAdoptionLabel, this.date_of_adoption, false, false);
			StringValidator quality = new StringValidator(qualityLabel, this.quality, true, true, 0, 100, true);
			IntegerValidator quantity = new IntegerValidator(quantityLabel, this.quantity, true, true);
			StringValidator quantityUnit = new StringValidator(quantityUnitLabel,this.quantity_unit, true, true, 0, 100, true);

			//Unique constraint validator
			ArrayList unqPerson = new ArrayList();
			unqPerson.add("person_id");
			unqPerson.add(this.person.getId());			
			ArrayList unqPractice = new ArrayList();
			unqPractice.add("practice_id");
			unqPractice.add(this.practice.getId());			
			ArrayList unqDateOfAdoption = new ArrayList();
			unqDateOfAdoption.add("date_of_adoption");
			unqDateOfAdoption.add(this.date_of_adoption);			
			ArrayList uniqueTogether = new ArrayList();
			uniqueTogether.add(unqPerson);
			uniqueTogether.add(unqPractice);
			uniqueTogether.add(unqDateOfAdoption);
			ArrayList uniqueValidatorLabels = new ArrayList();
			uniqueValidatorLabels.add("Person");
			uniqueValidatorLabels.add("Practice");
			uniqueValidatorLabels.add("Date Of Adoption");
			UniqueConstraintValidator uniquePersonPractice = new UniqueConstraintValidator(uniqueValidatorLabels,
					uniqueTogether, new PersonAdoptPracticeData());
			uniquePersonPractice.setCheckId(this.getId());			
			ArrayList validatorList = new ArrayList();
			validatorList.add(personValidator);
			validatorList.add(practiceValidator);
			validatorList.add(dateOfAdoption);
			validatorList.add(quality);
			validatorList.add(quantity);
			validatorList.add(quantityUnit);
			validatorList.add(uniquePersonPractice);
			return this.executeValidators(validatorList);		
		}
		
		@Override
		public boolean validate(BaseData.Data foreignKey) {
			String practiceLabel = "Practice";
			String dateOfAdoptionLabel = "DateOfAdoption";
			String qualityLabel = "Quality";
			String quantityLabel = "Quantity";
			String quantityUnitLabel = "Quantity Unit";
			StringValidator practiceValidator = new StringValidator(practiceLabel, this.practice.getId(), false, false, 1, 100);
			DateValidator dateOfAdoption = new DateValidator(dateOfAdoptionLabel, this.date_of_adoption, false, false);
			StringValidator quality = new StringValidator(qualityLabel, this.quality, true, true, 0, 100, true);
			IntegerValidator quantity = new IntegerValidator(quantityLabel, this.quantity, true, true);
			StringValidator quantityUnit = new StringValidator(quantityUnitLabel, this.quantity_unit, true, true, 0, 100,true);
			ArrayList validatorList = new ArrayList();
			validatorList.add(practiceValidator);
			validatorList.add(dateOfAdoption);
			validatorList.add(quality);
			validatorList.add(quantity);
			validatorList.add(quantityUnit);
			return this.executeValidators(validatorList);
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
		public String toQueryString(String id) {
			PersonAdoptPracticeData personAdoptPracticeData = new PersonAdoptPracticeData();
			return this.rowToQueryString(personAdoptPracticeData.getTableName(), personAdoptPracticeData.getFields(), "id", id, "");
		}
		
		@Override
		public String toInlineQueryString(String id) {
			PersonAdoptPracticeData personAdoptPracticeData = new PersonAdoptPracticeData();
			return rowToQueryString(personAdoptPracticeData.getTableName(), personAdoptPracticeData.getFields(), 
					"person_id", id, this.COLLECTION_PREFIX + "_set");
		}
		
		@Override
		public String getTableId() {
			PersonAdoptPracticeData personAdoptPracticesDataDbApis = new PersonAdoptPracticeData();
			return personAdoptPracticesDataDbApis.tableID;
		}
	}

	public static String tableID = "31";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `person_adopt_practice` " +
												"(id BIGINT UNSIGNED PRIMARY KEY  NOT NULL ," +
												"person_id BIGINT UNSIGNED  NOT NULL DEFAULT 0," +
												"practice_id BIGINT UNSIGNED  NOT NULL DEFAULT 0," +
												"PRIOR_ADOPTION_FLAG SMALLINT  NULL DEFAULT NULL," +
												"DATE_OF_ADOPTION DATE NOT NULL," +
												"QUALITY VARCHAR(200)  NULL DEFAULT NULL ," +
												"QUANTITY INT  NULL DEFAULT NULL," +
												"QUANTITY_UNIT VARCHAR(150)  NULL DEFAULT NULL, " +
												"FOREIGN KEY(person_id) REFERENCES person(id), " +
												"FOREIGN KEY(practice_id) REFERENCES practices(id));";
	protected static String dropTable = "DROP TABLE IF EXISTS `person_adopt_practice`;";
	protected static String selectPersonAdoptPractices = "SELECT id, date_of_adoption FROM person_adopt_practice ORDER BY (date_of_adoption);";
	protected static String listPersonAdoptPractices = "SELECT pap.id, p.id, p.person_name," +
			"pr.id,pr.practice_name, pap.DATE_OF_ADOPTION,pap.prior_adoption_flag,pap.quality, pap.quantity, pap.quantity_unit," +
			" pg.id, pg.group_name, vil.id, vil.village_name " +
			"FROM person_adopt_practice pap JOIN person p ON p.id = pap.person_id JOIN village vil ON p.village_id = vil.id " +
			"LEFT JOIN person_groups pg on p.group_id = pg.id JOIN practices pr ON pr.id = pap.practice_id ORDER BY LOWER(p.PERSON_NAME) ";
	protected static String savePersonAdoptPracticeOnlineURL = "/dashboard/savepersonadoptpracticeonline/";
	protected static String getPersonAdoptPracticeOnlineURL = "/dashboard/getpersonadoptpracticesonline/";
	protected static String savePersonAdoptPracticeOfflineURL = "/dashboard/savepersonadoptpracticeoffline/";
	protected static String getPracticeSeenForPersonURL = "/dashboard/getpracticesseenforperson/";
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
		return PersonAdoptPracticeData.getPersonAdoptPracticeOnlineURL;
	}
	
	@Override
	public String getSaveOfflineURL(){
		return PersonAdoptPracticeData.savePersonAdoptPracticeOfflineURL;
	}
	
	@Override
	public String getSaveOnlineURL(){
		return PersonAdoptPracticeData.savePersonAdoptPracticeOnlineURL;
	}
		
		
	public final native JsArray<Type> asArrayOfData(String json) /*-{
		return eval(json);
	}-*/;
	
	public List serialize(JsArray<Type> personAdoptPracticeObjects){
		List personAdoptPractices = new ArrayList();
		PersonsData person = new PersonsData();
		VillagesData village = new VillagesData();
		PersonGroupsData group = new PersonGroupsData();
		PracticesData practice = new PracticesData();
		VillagesData.Data vil = null;
		for(int i = 0; i < personAdoptPracticeObjects.length(); i++){
			PersonGroupsData.Data pg = group.new Data();
			vil = village.new Data(personAdoptPracticeObjects.get(i).getVillage().getPk(),
					personAdoptPracticeObjects.get(i).getVillage().getVillageName());

			if (personAdoptPracticeObjects.get(i).getGroup() != null) {
				pg = group.new Data(personAdoptPracticeObjects.get(i).getGroup()
						.getPk(), personAdoptPracticeObjects.get(i).getGroup()
						.getPersonGroupName());
			}
			PersonsData.Data p=person.new Data(personAdoptPracticeObjects.get(i).getPerson().getPk(), 
					personAdoptPracticeObjects.get(i).getPerson().getPersonName());
			PracticesData.Data pr = practice.new Data(personAdoptPracticeObjects.get(i).getPractice().getPk(), 
					personAdoptPracticeObjects.get(i).getPractice().getPracticeName());
			Data personAdoptPractice = new Data(personAdoptPracticeObjects.get(i).getPk(),p,pr,pg,vil, 
					personAdoptPracticeObjects.get(i).getPriorAdoptionFlag(), personAdoptPracticeObjects.get(i).getDateOfAdoption(),
					personAdoptPracticeObjects.get(i).getQuantity(),personAdoptPracticeObjects.get(i).getQuality(),
					personAdoptPracticeObjects.get(i).getQuantityUnit());
			personAdoptPractices.add(personAdoptPractice);
		}		
		return personAdoptPractices;
	}
		
	public List getPersonAdoptPracticesListingOffline(String... pageNum){
		BaseData.dbOpen();
		List personAdoptPractices = new ArrayList();
		PersonsData person = new PersonsData();
		PersonGroupsData group = new PersonGroupsData();
		VillagesData vil = new VillagesData(); 
		PracticesData practice = new PracticesData();
		String listTemp;
		if(pageNum.length == 0) {
			listTemp = listPersonAdoptPractices;
		}
		else {
			int offset = (Integer.parseInt(pageNum[0]) - 1)*pageSize;
			if(pageNum.length == 1) {
				listTemp = listPersonAdoptPractices + " LIMIT "+ Integer.toString(offset) + " , "+Integer.toString(pageSize) +";";
			} else {
				listTemp = "SELECT pap.id, p.id, p.person_name," +
				"pr.id,pr.practice_name, pap.DATE_OF_ADOPTION,pap.prior_adoption_flag,pap.quality, pap.quantity, pap.quantity_unit," +
				" pg.id, pg.group_name, vil.id, vil.village_name " +
				"FROM person_adopt_practice pap JOIN person p ON p.id = pap.person_id JOIN village vil ON p.village_id = vil.id " +
				"LEFT JOIN person_groups pg on p.group_id = pg.id JOIN practices pr ON pr.id = pap.practice_id " +
				"WHERE (p.person_name LIKE '%"+pageNum[1]+"%' " +
									"OR pr.practice_name" +	" LIKE '%"+pageNum[1]+"%' "+"OR pg.group_name" +" LIKE '%"+pageNum[1]+"%' "+
									"OR vil.village_name" +	" LIKE '%"+pageNum[1]+"%') ORDER BY LOWER(p.PERSON_NAME) " 
							+ " LIMIT "+ Integer.toString(offset)+" , "+Integer.toString(pageSize)+ ";";
			}
		}
		this.select(listTemp);
		if (this.getResultSet().isValidRow()){
			try {
				for (int i = 0; this.getResultSet().isValidRow(); ++i, this.getResultSet().next()) {
					PersonsData.Data p = person.new Data(this.getResultSet().getFieldAsString(1),  this.getResultSet().getFieldAsString(2));
					PersonGroupsData.Data pg;
					if (this.getResultSet().getFieldAsString(4) == null) {
						pg = null;
					} else {
						pg = group.new Data(this.getResultSet()
								.getFieldAsString(10), this.getResultSet()
								.getFieldAsString(11));
					}
					VillagesData.Data v = vil.new Data(this.getResultSet()
							.getFieldAsString(12), this.getResultSet()
							.getFieldAsString(13));
					PracticesData.Data pr = practice.new Data(this.getResultSet().getFieldAsString(3),  this.getResultSet().getFieldAsString(4));
					Data personAdoptPractice = new Data(this.getResultSet().getFieldAsString(0), p,pr,pg,v,this.getResultSet().getFieldAsString(5),
							this.getResultSet().getFieldAsString(6),this.getResultSet().getFieldAsString(7),this.getResultSet().getFieldAsString(8),
							this.getResultSet().getFieldAsString(9));
					personAdoptPractices.add(personAdoptPractice);
	    	      }				
			} catch (DatabaseException e) {
				Window.alert("Database Exception : " + e.toString());
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
			if(this.validate()) {
				if(this.validate()) {
					this.save();
					return true;
				}
			}
		}		
		return false;
	}

	public Object postPageData(String id) {
		if(BaseData.isOnline()){
			this.post(RequestContext.SERVER_HOST + this.savePersonAdoptPracticeOnlineURL + id + "/", this.form.getQueryString());
		}
		else{
			if(this.validate()) {
				this.save();
				return true;
			}
		}
		return false;
	}
	
	public Object getListPageData(String...pageNum ){
		if(BaseData.isOnline()){
			int offset = (Integer.parseInt(pageNum[0])-1)*pageSize;
			int limit = offset+pageSize;
			if(pageNum.length > 1 ) {
				this.get(RequestContext.SERVER_HOST + PersonAdoptPracticeData.getPersonAdoptPracticeOnlineURL +
						Integer.toString(offset)+"/"+Integer.toString(limit)+"/" + "?searchText="+pageNum[1]);
			} else {
				this.get(RequestContext.SERVER_HOST + PersonAdoptPracticeData.getPersonAdoptPracticeOnlineURL 
						+ Integer.toString(offset) + "/" + Integer.toString(limit) + "/");
			}
		}
		else{
			return true;
		}
		return false;
	}	
	
	public String retrievePracticeSeenDataAndConvertToHtml(String person_id) {
		PracticesData practiceData = new PracticesData();
		List practices = practiceData.getPracticeSeenForPersonOffline(person_id);
		
		String htmlPractice = "<option value='' selected='selected'>---------</option>";
		
		for(Object practice : practices) {
			htmlPractice = htmlPractice + "<option value=\"" + ((PracticesData.Data)practice).getId() + "\">" + 
			((PracticesData.Data)practice).getPracticeName() + "</option>";
		}
		
		return htmlPractice;
	}
	
	public String retrieveDataAndConvertResultIntoHtml() {
		
		PersonsData personData = new PersonsData();
		List persons = personData.getAllPersonsOffline();
		PersonsData.Data person;
		String htmlPerson = "<select name=\"person\" id=\"id_person\"" + 
							"<option value='' selected='selected'>---------</option>";
		for ( int i = 0; i < persons.size(); i++ ) {
			person = (PersonsData.Data)persons.get(i);
			htmlPerson = htmlPerson + "<option value=\"" + person.getId() + "\">" + person.getPersonName() 
					+ " ("+ person.getVillage().getVillageName() +")" + "</option>";
			} 
		htmlPerson = htmlPerson + "</select>";
		
		PracticesData practiceData = new PracticesData();
		List practices = practiceData.getAllPracticesOffline();
		PracticesData.Data practice;
		String htmlPractice = "<select name=\"practice\" id=\"id_practice\""  + 
							"<option value='' selected='selected'>---------</option>";
		for(int i = 0; i < practices.size(); i++ ) {
			practice = (PracticesData.Data)practices.get(i);
			htmlPractice = htmlPractice + "<option value=\"" + practice.getId() + "\">" + practice.getPracticeName() + "</option>";
		}
		htmlPractice = htmlPractice + "</select>";
		
		return htmlPerson + htmlPractice;
	}
	
	public Object getAddPageData() {
		if(BaseData.isOnline()) {
			this.get(RequestContext.SERVER_HOST + PersonAdoptPracticeData.savePersonAdoptPracticeOnlineURL);
		}
		else{
			return retrieveDataAndConvertResultIntoHtml();
		}
		return false;
	}
	
	public Object getPracticesForPerson(String person_id) {
		if(BaseData.isOnline()) {
			this.get(RequestContext.SERVER_HOST + PersonAdoptPracticeData.getPracticeSeenForPersonURL + person_id + "/");
		}
		else {
			return retrievePracticeSeenDataAndConvertToHtml(person_id);
		}
		return false;
	}
	
	public Object getAddPageData(String id){
		if(BaseData.isOnline()){
			this.get(RequestContext.SERVER_HOST + this.savePersonAdoptPracticeOnlineURL + id + "/" );
		}
		else{
			this.form.toQueryString(id);
			return retrieveDataAndConvertResultIntoHtml();
		}
		return false;
	}	
	
	public String getCount(String searchText) {
		String count = "0";//stores number of rows in a resultset
		String countSql = "SELECT COUNT(*)" +
		"FROM person_adopt_practice pap JOIN person p ON p.id = pap.person_id JOIN village vil ON p.village_id = vil.id " +
		"LEFT JOIN person_groups pg on p.group_id = pg.id JOIN practices pr ON pr.id = pap.practice_id " +
		"WHERE (p.person_name LIKE '%"+searchText+"%' " +
							"OR pr.practice_name" +	" LIKE '%"+searchText+"%' "+"OR pg.group_name" +" LIKE '%"+searchText+"%' "+
							"OR vil.village_name" +	" LIKE '%"+searchText+"%') ;";
		BaseData.dbOpen();
		this.select(countSql);
		if(this.getResultSet().isValidRow()) {
			try {
				count = getResultSet().getFieldAsString(0);
			} catch (DatabaseException e) {
				// TODO Auto-generated catch block
				Window.alert("Database Exception"+e.toString());
			}
		}
		BaseData.dbClose();
		return count;
	}
}

package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.PersonRelationsData.Type;
import com.digitalgreen.dashboardgwt.client.data.PersonRelationsData.Data;
import com.google.gwt.core.client.JsArray;

public class PersonRelationsData extends BaseData {

	public static class Type extends BaseData.Type{
		protected Type() {}
		public final native String getPerson() /*-{ return this.fields.person }-*/;
		public final native String getRelative() /*-{ return this.fields.relative }-*/;
		public final native String getTypeOfRelationShip() /*-{ return $wnd.checkForNullValues(this.fields.type_of_relationship); }-*/;
	}
	
public class Data extends BaseData.Data {
		
		final private static String COLLECTION_PREFIX = "personrelation";
			
		private PersonsData.Data person;
		private PersonsData.Data relative;
		private String type_of_relationship;
				
		public Data() {
			super();
		}
		
		public Data(String id, String type_of_relationship) {
			super();
			this.id = id;
			this.type_of_relationship = type_of_relationship;
		}
		

		public Data(String id,PersonsData.Data person, PersonsData.Data relative, String type_of_relationship) {
			super();
			this.id = id;
			this.person = person;
			this.relative = relative;
			this.type_of_relationship = type_of_relationship;
		}		
		
		public PersonsData.Data getPerson(){
			return this.person;
		}
		
		public PersonsData.Data getRelative(){
			return this.relative;
		}
		
		public String getTypeOfRelationShip(){
			return this.type_of_relationship;
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
			}else if(key.equals("person")) {
				PersonsData person = new PersonsData();
				this.person = person.getNewData();
				this.person.id = val;
			} else if(key.equals("relative")) {
				PersonsData relative = new PersonsData();
				this.relative = relative.getNewData();
				this.relative.id = val;
			} else if(key.equals("type_of_relationship")) {
				this.type_of_relationship = (String)val;
			} else {
				return;
			}
			this.addNameValueToQueryString(key, val);
		}
		
		@Override
		public void save() {
			PersonRelationsData personRelationssDataDbApis = new PersonRelationsData();			
			this.id = personRelationssDataDbApis.autoInsert(this.id, this.person.getId(),
						this.relative.getId(), this.type_of_relationship);
			this.addNameValueToQueryString("id", this.id);
		}
		
		@Override
		public String toQueryString(String id) {
			PersonRelationsData personRelationsData = new PersonRelationsData();
			return this.rowToQueryString(personRelationsData.getTableName(), personRelationsData.getFields(), "id", id, "");
		}
		
		@Override
		public String getTableId() {
			PersonRelationsData personRelationssDataDbApis = new PersonRelationsData();
			return personRelationssDataDbApis.tableID;
		}
	}

	
	public static String tableID = "21";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `person_relations` " +
												"(id BIGINT UNSIGNED PRIMARY KEY  NOT NULL ," +
												"person_id BIGINT UNSIGNED  NOT NULL DEFAULT 0," +
												"relative_id BIGINT UNSIGNED  NOT NULL DEFAULT 0," +
												"TYPE_OF_RELATIONSHIP VARCHAR(100)  NOT NULL, " +
												"FOREIGN KEY(person_id) REFERENCES person(id), " +
												"FOREIGN KEY(relative_id) REFERENCES person(id));" ;
	protected static String dropTable = "DROP TABLE IF EXISTS `person_relations`;";
	protected static String selectPersonRelations = "SELECT id, type_of_relationship FROM person_relations ORDER BY (type_of_relationship);";
	protected static String listPersonRelations = "SELECT * FROM person_relations pr JOIN person p ON p.id = pr.person_id" +
			"ORDER BY (-pr.id);";
	protected static String savePersonRelationOnlineURL = "/dashboard/savepersonrelationonline/";
	protected static String getPersonRelationOnlineURL = "/dashboard/getpersonrelationsonline/";
	protected static String savePersonRelationOfflineURL = "/dashboard/savepersonrelationoffline/";
	protected String table_name = "person_relations";
	protected String[] fields = {"id", "person_id", "relative_id", "type_of_relationship"};
	
	
	public PersonRelationsData(){
		super();
	}
	
	public PersonRelationsData(OnlineOfflineCallbacks callbacks) {
		super(callbacks);
	}
	
	public PersonRelationsData(OnlineOfflineCallbacks callbacks, Form form) {
		super(callbacks, form);
	}

	@Override
	public Data getNewData() {
		return new Data();
	}
	
	@Override
	protected String getTableId() {
		return PersonRelationsData.tableID;
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
		return PersonRelationsData.getPersonRelationOnlineURL;
	}
	
	@Override
	public String getSaveOfflineURL(){
		return PersonRelationsData.savePersonRelationOfflineURL;
	}
	
	@Override
	public String getSaveOnlineURL(){
		return PersonRelationsData.savePersonRelationOnlineURL;
	}
	
	public final native JsArray<Type> asArrayOfData(String json) /*-{
		return eval(json);
	}-*/;
	
	public List serialize(JsArray<Type> personRelationObjects){
		List personRelations = new ArrayList();
		PersonsData person = new PersonsData();
		for(int i = 0; i < personRelationObjects.length(); i++){
			PersonsData.Data p = person.new Data(personRelationObjects.get(i).getPerson());
			PersonsData.Data relative = person.new Data(personRelationObjects.get(i).getRelative());
			Data personRelation = new Data(personRelationObjects.get(i).getPk(),p,relative, 
					personRelationObjects.get(i).getTypeOfRelationShip());
			personRelations.add(personRelation);
		}
		
		return personRelations;
	}
	
	@Override
	public List getListingOnline(String json){
		return this.serialize(this.asArrayOfData(json));		
	}
}

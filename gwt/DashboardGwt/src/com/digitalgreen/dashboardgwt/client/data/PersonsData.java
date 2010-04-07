package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.PersonsData.Type;
import com.digitalgreen.dashboardgwt.client.data.ScreeningsData.Data;
import com.google.gwt.core.client.JsArray;

public class PersonsData extends BaseData {
	
	public static class Type extends BaseData.Type{
		protected Type() {}
		public final native String getPersonName() /*-{ return this.fields.person_name; }-*/;
		public final native String getFatherName() /*-{ return this.fields.father_name; }-*/;
		public final native String getAge() /*-{ return this.fields.age; }-*/;
		public final native String getGender() /*-{ return this.fields.gender; }-*/;
		public final native String getPhoneNo() /*-{ return this.fields.phone_no; }-*/;
		public final native String getAddress() /*-{ return this.fields.address; }-*/;
		public final native String getLandHoldings() /*-{ return this.fields.land_holdings; }-*/;
		public final native VillagesData.Type getVillage() /*-{ return this.fields.village;}-*/;
		public final native PersonGroupsData.Type getPersonGroup() /*-{ return this.fields.group;}-*/;
		public final native int getEquipmentHolderId() /*-{ return this.fields.equipmentholder_id; }-*/;
		
	}
	
	public class Data extends BaseData.Data {
		
		final private static String COLLECTION_PREFIX = "person";
		
		private String person_name;
		private String father_name;
		private String age;
		private String gender;
		private String phone_no;
		private String address;
		private String land_holdings;
		private VillagesData.Data village;
		private PersonGroupsData.Data group;
		private int equipmentholder_id;
		private PersonRelationsData.Data relations;
		private PersonAdoptPracticeData.Data adopted_agricultural_practices;
		
		
		public Data() {
			super();
		}
		
		public Data(int id, String person_name,String father_name,String age,String gender,String phone_no,String address,String land_holdings,
				VillagesData.Data village,PersonGroupsData.Data group,int equipmentholder_id) {
			super();
			this.id = id;
			this.person_name = person_name;
			this.father_name = father_name;
			this.age = age;
			this.gender = gender;
			this.phone_no = phone_no;
			this.address = address;
			this.land_holdings = land_holdings;
			this.village = village;
			this.group = group;
			this.equipmentholder_id = equipmentholder_id;
		}
		
		public Data(int id, String person_name){
			super();
			this.id = id;
			this.person_name = person_name;
		}
				
		public String getPersonName(){
			return this.person_name;
		}
		
		public String getAge(){
			return this.age;
		}
		
		public String getGender(){
			return this.gender;
		}
				
		public String getPhoneNo(){
			return this.phone_no;
		}
		
		public String getAddress(){
			return this.address;
		}
		
		public String getLandHoldings(){
			return this.land_holdings;
		}
		
		public VillagesData.Data getVillage(){
			return this.village;
		}
		
		public PersonGroupsData.Data getGroup(){
			return this.group;
		}
						
		public int getEquipmentHolderId(){
			return this.equipmentholder_id;
		}
		
		public BaseData.Data clone() {
			Data obj = new Data();
			obj.id = this.id;
			obj.person_name = this.person_name;
			obj.father_name = this.father_name;
			obj.age = this.age;
			obj.gender = this.gender;
			obj.phone_no = this.phone_no;
			obj.address = this.address;
			obj.land_holdings = this.land_holdings;
			obj.village = (VillagesData.Data)this.village.clone();
			obj.group= (PersonGroupsData.Data)this.group.clone();
			obj.equipmentholder_id = this.equipmentholder_id;
			obj.relations = this.relations;
			obj.adopted_agricultural_practices = this.adopted_agricultural_practices;			
				
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
			} else if(key.equals("person_name")) {
				this.person_name = (String)val;
			} else if(key.equals("father_name")) {
				this.father_name = (String)val;
			} else if(key.equals("age")) {
				this.age = (String)val;
			} else if(key.equals("gender")) {
				this.gender = (String)val;
			} else if(key.equals("phone_no")) {
				this.phone_no = (String)val;
			} else if(key.equals("address")) {
				this.address = (String)val;
			} else if(key.equals("land_holdings")) {
				this.land_holdings = (String)val;
			} else if(key.equals("village")) {
				// Have to Create an instance of VillagesData to create an instance of VillagesData.Data -- any better way of doing this??
				VillagesData village = new VillagesData();
				this.village = village.getNewData();
				this.village.id = Integer.parseInt((String)val);
				//Never ever use this -- this.village.id = ((Integer)val).intValue();
			}  else if(key.equals("group")) {
				PersonGroupsData group = new PersonGroupsData();
				this.group = group.getNewData();
				this.group.id = Integer.parseInt((String)val);
				//Never ever use this -- this.group.id = ((Integer)val).intValue();
			}  else if(key.equals("equipmentholder_id")) {
				this.equipmentholder_id = Integer.parseInt((String)val);
			}  else if(key.equals("relations")) {
				PersonRelationsData relations = new PersonRelationsData();
				this.relations = relations.getNewData();
				this.relations.id = Integer.parseInt((String)val);
				//Never ever use this -- this.group.id = ((Integer)val).intValue();
			}  else if(key.equals("adopted_agricultural_practices")) {
				PersonAdoptPracticeData adopted_agricultural_practices = new PersonAdoptPracticeData();
				this.adopted_agricultural_practices = adopted_agricultural_practices.getNewData();
				this.adopted_agricultural_practices.id = Integer.parseInt((String)val);
				//Never ever use this -- this.group.id = ((Integer)val).intValue();
			}  	
		}
		
		@Override		
		public void save() {
			PersonsData personsDataDbApis = new PersonsData();		
			if(this.id==0){
				this.id = personsDataDbApis.autoInsert(this.person_name,this.father_name,this.age,this.gender,
						this.phone_no,this.address,this.land_holdings,Integer.valueOf(this.village.getId()).toString(),
						Integer.valueOf(this.group.getId()).toString(), Integer.valueOf(this.equipmentholder_id).toString(),
						Integer.valueOf(this.relations.getId()).toString(),Integer.valueOf(this.adopted_agricultural_practices.getId()).toString());
			}else{
				this.id = personsDataDbApis.autoInsert(Integer.valueOf(this.id).toString(),this.person_name,this.father_name,this.age,this.gender,
						this.phone_no,this.address,this.land_holdings,Integer.valueOf(this.village.getId()).toString(),
						Integer.valueOf(this.group.getId()).toString(), Integer.valueOf(this.equipmentholder_id).toString(),
						Integer.valueOf(this.relations.getId()).toString(),Integer.valueOf(this.adopted_agricultural_practices.getId()).toString());
			}
			
			}		
	}
	
	protected static String tableID = "13";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `person` " +
												"(id INTEGER PRIMARY KEY  NOT NULL ," +
												"PERSON_NAME VARCHAR(100)  NOT NULL ," +
												"FATHER_NAME VARCHAR(100)  NOT NULL ," +
												"AGE INT  NULL DEFAULT NULL," +
												"GENDER VARCHAR(1)  NOT NULL ," +
												"PHONE_NO VARCHAR(100)  NOT NULL ," +
												"ADDRESS VARCHAR(500)  NOT NULL ," +
												"LAND_HOLDINGS INT  NULL DEFAULT NULL," +
												"village_id INT  NOT NULL DEFAULT 0," +
												"group_id INT  NULL DEFAULT NULL," +
												"equipmentholder_id INT  NULL DEFAULT NULL, " +
												"FOREIGN KEY(village_id) REFERENCES village(id), " +
												"FOREIGN KEY(group_id) REFERENCES person_groups(id), " +
												"FOREIGN KEY(equipmentholder_id) REFERENCES equipment_holder(id) ); " ; 
	
	protected static String selectPersons = "SELECT id, PERSON_NAME FROM person  ORDER BY (PERSON_NAME);";
	protected static String listPersons = "SELECT p.id, p.PERSON_NAME,p.FATHER_NAME,p.AGE, p.GENDER,p.PHONE_NO,p.ADDRESS," +
			"vil.id, vil.village_name ,pg.id,pg.group_name FROM person p, village vil, person_group pg WHERE p.village_id = vil.id " +
			"and p.group_id = pg.id ORDER BY (-p.id);";
	protected static String savePersonOfflineURL = "/dashboard/savepersonoffline/";
	protected static String savePersonOnlineURL = "/dashboard/savepersononline/";
	protected static String getPersonOnlineURL = "/dashboard/getpersonsonline/";
	protected String table_name = "person";
	protected String[] fields = {"id", "person_name","father_name", "age", "gender", "phone_no", "address", "land_holder",
			"village_id", "group_id", "equipmentholder_id"};
	
	
	public PersonsData() {
		super();
	}
	public PersonsData(OnlineOfflineCallbacks callbacks) {
		super(callbacks);
	}
	
	public PersonsData(OnlineOfflineCallbacks callbacks, Form form, String queryString) {
		super(callbacks, form, queryString);
	}
	@Override
	public Data getNewData() {
		return new Data();
	}
	
	@Override
	protected String getTableId() {
		return PersonsData.tableID;
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
		return PersonsData.getPersonOnlineURL;
	}
		
	public final native JsArray<Type> asArrayOfData(String json) /*-{
		return eval(json);
	}-*/;
	
	public List serialize(JsArray<Type> personObjects){
		List persons = new ArrayList();
		VillagesData village = new VillagesData();
		PersonGroupsData group = new PersonGroupsData();
		for(int i = 0; i < personObjects.length(); i++){
			VillagesData.Data vil = village.new Data(Integer.parseInt(personObjects.get(i).getVillage().getPk()),
					personObjects.get(i).getVillage().getVillageName());
			PersonGroupsData.Data pg = group.new Data(Integer.parseInt(personObjects.get(i).getPersonGroup().getPk()),
					personObjects.get(i).getPersonGroup().getPersonGroupName());
			
			Data person = new Data(Integer.parseInt(personObjects.get(i).getPk()),
						personObjects.get(i).getPersonName(),
						personObjects.get(i).getFatherName(),
						personObjects.get(i).getAge(),
						personObjects.get(i).getGender(),
						personObjects.get(i).getPhoneNo(),
						personObjects.get(i).getAddress(),
						personObjects.get(i).getLandHoldings(),vil,pg,
						personObjects.get(i).getEquipmentHolderId());
			persons.add(person);
		}
		
		return persons;
	}
	
	@Override
	public List getListingOnline(String json){
		return this.serialize(this.asArrayOfData(json));		
	}
		
}
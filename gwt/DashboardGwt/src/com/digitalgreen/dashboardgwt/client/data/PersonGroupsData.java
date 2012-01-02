package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.validation.StringValidator;
import com.digitalgreen.dashboardgwt.client.data.validation.TimeValidator;
import com.digitalgreen.dashboardgwt.client.data.validation.UniqueConstraintValidator;
import com.google.gwt.core.client.JsArray;
import com.google.gwt.gears.client.database.DatabaseException;
import com.google.gwt.user.client.Window;

public class PersonGroupsData extends BaseData {

	public static class Type extends BaseData.Type {
		protected Type() {
		}

		public final native String getPersonGroupName() /*-{
			return $wnd.checkForNullValues(this.fields.group_name);
		}-*/;

		public final native String getDays() /*-{
			return $wnd.checkForNullValues(this.fields.days);
		}-*/;

		public final native String getTimings() /*-{
			return $wnd.checkForNullValues(this.fields.timings);
		}-*/;

		public final native String getTimeUpdated() /*-{
			return $wnd.checkForNullValues(this.fields.time_updated);
		}-*/;

		public final native VillagesData.Type getVillage() /*-{
			return this.fields.village;
		}-*/;
	}

	public class Data extends BaseData.Data {
		final private static String COLLECTION_PREFIX = "persongroups";

		private String group_name;
		private String days;
		private String timings;
		private String time_updated;
		private VillagesData.Data village;

		public Data() {
			super();
		}

		public Data(String id) {
			super();
			this.id = id;
		}

		public Data(String id, String group_name) {
			super();
			this.id = id;
			this.group_name = group_name;
		}

		public Data(String id, String group_name, VillagesData.Data village) {
			super();
			this.id = id;
			this.group_name = group_name;
			this.village = village;
		}

		public Data(String id, String group_name, String days, String timings,
				String time_updated, VillagesData.Data village) {
			super();
			this.id = id;
			this.group_name = group_name;
			this.days = days;
			this.timings = timings;
			this.time_updated = time_updated;
			this.village = village;
		}

		public String getPersonGroupName() {
			return this.group_name;
		}

		public String getTimings() {
			return this.timings;
		}

		public String getTimeUpdated() {
			return this.time_updated;
		}

		public VillagesData.Data getVillage() {
			return this.village;
		}

		@Override
		public BaseData.Data clone() {
			Data obj = new Data();
			obj.village = (new VillagesData()).new Data();
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
			} else if (key.equals("group_name")) {
				this.group_name = val;
			} else if (key.equals("days")) {
				this.days = val;
			} else if (key.equals("timings")) {
				this.timings = val;
			} else if (key.equals("time_updated")) {
				this.time_updated = (String) val;
			} else if (key.equals("village")) {
				VillagesData village = new VillagesData();
				this.village = village.getNewData();
				this.village.id = val;
			} else {
				return;
			}
			this.addNameValueToQueryString(key, val);
		}
		//This method is to check for multiple inlines with  same data. 
		@Override
		public boolean compare(BaseData.Data other) {
			if(other instanceof PersonGroupsData.Data) {
				PersonGroupsData.Data obj = (PersonGroupsData.Data) other;
				if(this.group_name.equals(obj.getPersonGroupName())) {
					errorStack.add(this.group_name+": Details entered twice");
					return true;
				} else
					return false;
			} else
				return false;
		}

		@Override
		public boolean validate() {
			//Labels to print validation error messages
			String nameLabel = "Group Name";
			String timeLabel = "Time";
			String villageLabel = "Village";
			StringValidator groupName = new StringValidator(nameLabel, this.group_name, false, false, 0, 100, true);
			TimeValidator timings = new TimeValidator(timeLabel, this.timings, true, true);
			StringValidator villageValidator = new StringValidator(villageLabel, this.village.getId(), false, false, 1, 100);
			ArrayList group_name = new ArrayList();
			group_name.add("group_name");
			group_name.add(this.group_name);
			ArrayList villageId = new ArrayList();
			villageId.add("village_id");
			villageId.add(this.village.getId());
			ArrayList groupVillageId = new ArrayList();
			groupVillageId.add(group_name);
			groupVillageId.add(villageId);
			ArrayList uniqueValidatorLabels = new ArrayList();
			uniqueValidatorLabels.add("Person Group");
			uniqueValidatorLabels.add("Village");			
			UniqueConstraintValidator uniqueGroupVillageId = new UniqueConstraintValidator(uniqueValidatorLabels,
					groupVillageId, new PersonGroupsData());
			uniqueGroupVillageId.setCheckId(this.getId());

			ArrayList validatorList = new ArrayList();
			validatorList.add(groupName);
			validatorList.add(timings);
			validatorList.add(villageValidator);
			validatorList.add(uniqueGroupVillageId);
			return this.executeValidators(validatorList);
		}

		@Override
		public boolean validate(BaseData.Data foreignKey) {
			//Labels to print validation error messages
			String nameLabel = "Group Name";
			String timeLabel = "Time";
			StringValidator groupName = new StringValidator(nameLabel,this.group_name, false, false, 0, 100, true);
			TimeValidator timings = new TimeValidator(timeLabel,this.timings, true, true);
			ArrayList validatorList = new ArrayList();
			validatorList.add(groupName);
			validatorList.add(timings);
			if(foreignKey.getId() != null) {
				ArrayList group_name = new ArrayList();
				group_name.add("group_name");
				group_name.add(this.group_name);
				ArrayList villageId = new ArrayList();
				villageId.add("village_id");
				villageId.add(foreignKey.getId());
				ArrayList groupVillageId = new ArrayList();
				groupVillageId.add(group_name);
				groupVillageId.add(villageId);
				ArrayList uniqueValidatorLabels = new ArrayList();
				uniqueValidatorLabels.add("Person Group");
				uniqueValidatorLabels.add("Village");			
				UniqueConstraintValidator uniqueGroupVillageId = new UniqueConstraintValidator(uniqueValidatorLabels,
						groupVillageId, new PersonGroupsData());
				uniqueGroupVillageId.setCheckId(this.getId());
				
				validatorList.add(uniqueGroupVillageId);
			}
			
			return this.executeValidators(validatorList);
		}

		@Override
		public void save() {
			PersonGroupsData personGroupsDataDbApis = new PersonGroupsData();
			Date date = new Date();
			if (this.id == null) {
				this.time_updated = BaseData.getCurrentDateAndTime();
			}
			this.id = personGroupsDataDbApis.autoInsert(this.id,
					this.group_name, this.days, this.timings,
					this.time_updated, this.village.getId());
			this.addNameValueToQueryString("id", this.id);
		}

		@Override
		public void save(BaseData.Data foreignKey) {
			PersonGroupsData personGroupsDataDbApis = new PersonGroupsData();
			Date date = new Date();
			this.time_updated = date.getYear() + "-" + date.getMonth() + "-"
					+ date.getDate() + " " + date.getHours() + ":"
					+ date.getMinutes() + ":" + date.getSeconds();
			this.id = personGroupsDataDbApis.autoInsert(this.id,
					this.group_name, this.days, this.timings,
					this.time_updated, foreignKey.getId());
			this.addNameValueToQueryString("id", this.id);
			this.addNameValueToQueryString("village", foreignKey.getId());
		}
		
		@Override
		public String toQueryString(String id) {
			PersonGroupsData personGroupsData = new PersonGroupsData();
			return rowToQueryString(personGroupsData.getTableName(), personGroupsData.getFields(), 
					"id", id, "");
		}

		@Override
		public String toInlineQueryString(String id) {
			PersonGroupsData personGroupsData = new PersonGroupsData();
			return rowToQueryString(personGroupsData.getTableName(), personGroupsData.getFields(), 
					"village_id", id, this.COLLECTION_PREFIX + "_set");
		}
		
		@Override
		public String getTableId() {
			PersonGroupsData personGroupsDataDbApis = new PersonGroupsData();
			return personGroupsDataDbApis.tableID;
		}
	}

	public static String tableID = "19";

	protected static String dropTable = "DROP TABLE IF EXISTS `person_groups`;";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `person_groups` "
			+ "(id BIGINT UNSIGNED PRIMARY KEY  NOT NULL ,"
			+ "GROUP_NAME VARCHAR(100)  NOT NULL ,"
			+ "DAYS VARCHAR(9) NULL DEFAULT NULL ,"
			+ "TIMINGS TIME  NULL DEFAULT NULL,"
			+ "TIME_UPDATED DATETIME  NULL DEFAULT NULL ,"
			+ "village_id BIGINT UNSIGNED  NOT NULL DEFAULT 0, "
			+ "FOREIGN KEY(village_id) REFERENCES village(id));";
	protected static String[] createIndexes = {"CREATE INDEX IF NOT EXISTS person_groups_PRIMARY ON person_groups(id);", 
	   										"CREATE INDEX IF NOT EXISTS person_groups_village_id ON person_groups(village_id);"};
	protected static String selectPersonGroups = "SELECT id, GROUP_NAME FROM person_groups  ORDER BY (GROUP_NAME);";
	protected static String selectPersonGroupsForVillage = "SELECT id, group_name FROM person_groups where village_id=%s ORDER BY group_name";
	protected static String selectPersonGroupsWithVillage = "SELECT person_groups.id, person_groups.GROUP_NAME, village.id, village.VILLAGE_NAME " +
			"FROM person_groups JOIN village ON person_groups.village_id = village.id ORDER BY (person_groups.GROUP_NAME)";
	protected static String listPersonGroups = "SELECT pg.id,pg.GROUP_NAME, vil.id,vil.village_name FROM person_groups pg "
			+ "JOIN village vil ON pg.village_id = vil.id ORDER BY LOWER(pg.GROUP_NAME)";
	protected static String savePersonGroupOfflineURL = "/dashboard/savepersongroupoffline/";
	protected static String savePersonGroupOnlineURL = "/dashboard/savepersongrouponline/";
	protected static String getPersonGroupOnlineURL = "/dashboard/getpersongroupsonline/";
	protected String table_name = "person_groups";
	protected String[] fields = { "id", "group_name", "days", "timings",
			"time_updated", "village_id" };

	public PersonGroupsData() {
		super();
	}

	public PersonGroupsData(OnlineOfflineCallbacks callbacks) {
		super(callbacks);
	}

	public PersonGroupsData(OnlineOfflineCallbacks callbacks, Form form) {
		super(callbacks, form);
	}

	@Override
	public Data getNewData() {
		return new Data();
	}

	@Override
	protected String getTableId() {
		return PersonGroupsData.tableID;
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
		return PersonGroupsData.getPersonGroupOnlineURL;
	}

	@Override
	public String getSaveOfflineURL() {
		return PersonGroupsData.savePersonGroupOfflineURL;
	}
	
	@Override
	public String getSaveOnlineURL() {
		return PersonGroupsData.savePersonGroupOnlineURL;
	}


	public final native JsArray<Type> asArrayOfData(String json) /*-{
		return eval(json);
	}-*/;

	public List serialize(JsArray<Type> personGroupObjects) {
		List personGroups = new ArrayList();
		VillagesData village = new VillagesData();
		for (int i = 0; i < personGroupObjects.length(); i++) {
			VillagesData.Data vil = village.new Data(personGroupObjects.get(i)
					.getVillage().getPk(), personGroupObjects.get(i)
					.getVillage().getVillageName());

			Data personGroup = new Data(personGroupObjects.get(i).getPk(),
					personGroupObjects.get(i).getPersonGroupName(),
					personGroupObjects.get(i).getDays(), personGroupObjects
							.get(i).getTimings(), personGroupObjects.get(i)
							.getTimeUpdated(), vil);
			personGroups.add(personGroup);
		}
		return personGroups;
	}

	@Override
	public List getListingOnline(String json) {
		return this.serialize(this.asArrayOfData(json));
	}

	public List getPersonGroupsListingOffline(String... pageNum) {
		BaseData.dbOpen();
		List personGroups = new ArrayList();
		VillagesData village = new VillagesData();
		String listTemp;
		// Checking whether to return all villages or only limited number of villages
		if(pageNum.length == 0) {
			listTemp = listPersonGroups;
		}
		else {
			int offset = (Integer.parseInt(pageNum[0]) - 1)*pageSize;
			if(pageNum.length == 1) {
				listTemp = listPersonGroups + " LIMIT "+ Integer.toString(offset) + " , "+Integer.toString(pageSize) +";";
			} else {
				listTemp = "SELECT pg.id,pg.group_name, vil.id,vil.village_name " +
				"FROM person_groups pg, village vil " +
				"WHERE pg.village_id = vil.id AND (pg.group_name LIKE '%"+pageNum[1]+"%' " +
									"OR vil.VILLAGE_NAME" +	" LIKE '%"+pageNum[1]+"%' )" +" ORDER BY(pg.group_name) " 
									+ " LIMIT "+ Integer.toString(offset)+" , "+Integer.toString(pageSize)+ ";";
			}
		}
		this.select(listTemp);
		if (this.getResultSet().isValidRow()) {
			try {
				for (int i = 0; this.getResultSet().isValidRow(); ++i, this
						.getResultSet().next()) {
					VillagesData.Data v = village.new Data(this.getResultSet()
							.getFieldAsString(2), this.getResultSet()
							.getFieldAsString(3));
					Data personGroup = new Data(this.getResultSet()
							.getFieldAsString(0), this.getResultSet()
							.getFieldAsString(1), v);
					personGroups.add(personGroup);
				}
			} catch (DatabaseException e) {
				Window.alert("Database Exception  : " + e.toString());
				BaseData.dbClose();
			}

		}
		BaseData.dbClose();
		return personGroups;
	}
	
	public List getAllPersonGroupsForVillageOffline(String village_id) {
		return fetchPersonGroupsForSql(selectPersonGroupsForVillage.replaceFirst("%s", village_id));
	}

	public List getAllPersonGroupsOffline() {
		return fetchPersonGroupsForSql(selectPersonGroups);
	}
		
	public List fetchPersonGroupsForSql(String sql) {
		BaseData.dbOpen();
		List personGroups = new ArrayList();
		this.select(sql);
		if (this.getResultSet().isValidRow()) {
			try {
				for (int i = 0; this.getResultSet().isValidRow(); ++i, this
						.getResultSet().next()) {
					Data personGroup = new Data(this.getResultSet()
							.getFieldAsString(0), this.getResultSet()
							.getFieldAsString(1));
					personGroups.add(personGroup);
				}
			} catch (DatabaseException e) {
				Window.alert("Database Exception : " + e.toString());
				BaseData.dbClose();
			}

		}
		BaseData.dbClose();
		return personGroups;
	}
	
	public List getAllPersonGroupsWithVillageOffline() {
		BaseData.dbOpen();
		List personGroups = new ArrayList();
		this.select(selectPersonGroupsWithVillage);
		if (this.getResultSet().isValidRow()) {
			try {
				VillagesData v = new VillagesData();
				for (int i = 0; this.getResultSet().isValidRow(); ++i, this
						.getResultSet().next()) {
					VillagesData.Data village = v.new Data(this.getResultSet().getFieldAsString(2), this.getResultSet().getFieldAsString(3));
					Data personGroup = new Data(this.getResultSet()
							.getFieldAsString(0), this.getResultSet()
							.getFieldAsString(1), village);
					personGroups.add(personGroup);
				}
			} catch (DatabaseException e) {
				Window.alert("Database Exception : " + e.toString());
				BaseData.dbClose();
			}

		}
		BaseData.dbClose();
		return personGroups;
	}

	public Object postPageData() {
		if (BaseData.isOnline()) {
			this.post(RequestContext.SERVER_HOST
					+ PersonGroupsData.savePersonGroupOnlineURL, this.form
					.getQueryString());
		} else {
			if (this.validate()) {
					this.save();
					return true;
				}
		}

		return false;
	}
	
	public Object postPageData(String id) {
		if(BaseData.isOnline()){
			this.post(RequestContext.SERVER_HOST + this.savePersonGroupOnlineURL + id + "/", this.form.getQueryString());
		}
		else{
			if(this.validate()) {
				this.save();
				return true;
			}
		}
		return false;
	}

	public Object getListPageData(String... pageNum) {
		if (BaseData.isOnline()) {
			int offset = (Integer.parseInt(pageNum[0])-1)*pageSize;
			int limit = offset+pageSize;
			if(pageNum.length > 1 ) {
				this.get(RequestContext.SERVER_HOST + PersonGroupsData.getPersonGroupOnlineURL +
						Integer.toString(offset)+"/"+Integer.toString(limit)+"/" + "?searchText="+pageNum[1]);
			} else {
				this.get(RequestContext.SERVER_HOST + PersonGroupsData.getPersonGroupOnlineURL + Integer.toString(offset) + "/" 
						+ Integer.toString(limit)+ "/");
			}
		} else {
			return true;
		}
		return false;
	}

	public String retrieveDataAndConvertResultIntoHtml() {
		VillagesData villageData = new VillagesData();
		List villages = villageData.getAllVillagesOffline();
		VillagesData.Data village;
		String html = "<select name=\"village\" id=\"id_village\">"
				+ "<option selected='selected' value=''>---------</option>";
		for (int i = 0; i < villages.size(); i++) {
			village = (VillagesData.Data) villages.get(i);
			html = html + "<option value = \"" + village.getId() + "\">"
					+ village.getVillageName() + "</option>";
		}
		html = html + "</select>";

		VillagesData villageData1 = new VillagesData();
		List villages1 = villageData.getAllVillagesOffline();
		VillagesData.Data village1;
		for (int inline = 0; inline < 30; inline++) {
			html += "<select name=\"person_set-" + inline
					+ "-village\" id=\"id_person_set-" + inline + "-village\">"
					+ "<option selected='selected' value=''>---------</option>";
			for (int i = 0; i < villages1.size(); i++) {
				village1 = (VillagesData.Data) villages1.get(i);
				html = html + "<option value = \"" + village1.getId() + "\">"
						+ village1.getVillageName() + "</option>";
			}
			html = html + "</select>";
		}

		return html;
	}

	public Object getAddPageData() {
		if (BaseData.isOnline()) {
			this.get(RequestContext.SERVER_HOST
					+ PersonGroupsData.savePersonGroupOnlineURL);
		} else {
			return retrieveDataAndConvertResultIntoHtml();
		}
		return false;
	}
	
	public Object getAddPageData(String id){
		if(BaseData.isOnline()){
			this.get(RequestContext.SERVER_HOST + this.savePersonGroupOnlineURL + id + "/" );
		}
		else{
			this.form.toQueryString(id);
			return retrieveDataAndConvertResultIntoHtml();
		}
		return false;
	}
	
	public String getCount(String searchText) {
		String count = "0";//stores number of rows in a resultset
		String countSql = "SELECT COUNT(*) " +
		"FROM person_groups pg, village vil " +
		"WHERE pg.village_id = vil.id AND (pg.group_name LIKE '%"+searchText+"%' " +
							"OR vil.VILLAGE_NAME" +	" LIKE '%"+searchText+"%' ) ;" ;
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
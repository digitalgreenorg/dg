package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.validation.DateValidator;
import com.digitalgreen.dashboardgwt.client.data.validation.IntegerValidator;
import com.digitalgreen.dashboardgwt.client.data.validation.StringValidator;
import com.digitalgreen.dashboardgwt.client.data.validation.UniqueConstraintValidator;
import com.google.gwt.core.client.JsArray;
import com.google.gwt.gears.client.database.DatabaseException;
import com.google.gwt.user.client.Window;

public class PersonAdoptPracticeData extends BaseData{
	
	public static class Type extends BaseData.Type{
		protected Type() {}
		public final native PersonsData.Type getPerson() /*-{ return this.fields.person }-*/;
		public final native VideosData.Type getVideo() /*-{ return this.fields.video }-*/;
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
		private VideosData.Data video;
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
		
		public Data(String id,PersonsData.Data person, VideosData.Data video, PersonGroupsData.Data group, VillagesData.Data village, 
				String prior_adoption_flag,String date_of_adoption,
				String quality,String quantity,String quantity_unit) {
			super();
			this.id = id;
			this.person = person;
			this.video = video;
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
		
		public VideosData.Data getVideo(){
			return this.video;
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
			obj.video = (new VideosData()).new Data();
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
			} else if(key.equals("video")) {
				VideosData video = new VideosData();
				this.video = video.getNewData();
				this.video.id = val;
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
						&& this.video.getId().equals(obj.getVideo().getId()) ) {
					errorStack.add("Person adopted two same video on same date");
					return true;
				} else
					return false;
			} else
				return false;
		}
		@Override
		public boolean validate() {
			String personLabel = "Person";
			String videoLabel = "Video";
			String dateOfAdoptionLabel = "DateOfAdoption";
			String qualityLabel = "Quality";
			String quantityLabel = "Quantity";
			String quantityUnitLabel = "Quantity Unit";
			StringValidator personValidator = new StringValidator(personLabel,this.person.getId(), false, false, 1, 100);
			StringValidator videoValidator = new StringValidator(videoLabel, this.video.getId(), false, false, 1, 100);
			DateValidator dateOfAdoption = new DateValidator(dateOfAdoptionLabel, this.date_of_adoption, false, false);
			StringValidator quality = new StringValidator(qualityLabel, this.quality, true, true, 0, 100, true);
			IntegerValidator quantity = new IntegerValidator(quantityLabel, this.quantity, true, true);
			StringValidator quantityUnit = new StringValidator(quantityUnitLabel,this.quantity_unit, true, true, 0, 100, true);

			//Unique constraint validator
			ArrayList unqPerson = new ArrayList();
			unqPerson.add("person_id");
			unqPerson.add(this.person.getId());			
			ArrayList unqVideo = new ArrayList();
			unqVideo.add("video_id");
			unqVideo.add(this.video.getId());			
			ArrayList unqDateOfAdoption = new ArrayList();
			unqDateOfAdoption.add("date_of_adoption");
			unqDateOfAdoption.add(this.date_of_adoption);			
			ArrayList uniqueTogether = new ArrayList();
			uniqueTogether.add(unqPerson);
			uniqueTogether.add(unqVideo);
			uniqueTogether.add(unqDateOfAdoption);
			ArrayList uniqueValidatorLabels = new ArrayList();
			uniqueValidatorLabels.add("Person");
			uniqueValidatorLabels.add("Video");
			uniqueValidatorLabels.add("Date Of Adoption");
			UniqueConstraintValidator uniquePersonPractice = new UniqueConstraintValidator(uniqueValidatorLabels,
					uniqueTogether, new PersonAdoptPracticeData());
			uniquePersonPractice.setCheckId(this.getId());			
			ArrayList validatorList = new ArrayList();
			validatorList.add(personValidator);
			validatorList.add(videoValidator);
			validatorList.add(dateOfAdoption);
			validatorList.add(quality);
			validatorList.add(quantity);
			validatorList.add(quantityUnit);
			validatorList.add(uniquePersonPractice);
			return this.executeValidators(validatorList);		
		}
		
		@Override
		public boolean validate(BaseData.Data foreignKey) {
			String videoLabel = "Video";
			String dateOfAdoptionLabel = "DateOfAdoption";
			String qualityLabel = "Quality";
			String quantityLabel = "Quantity";
			String quantityUnitLabel = "Quantity Unit";
			StringValidator videoValidator = new StringValidator(videoLabel, this.video.getId(), false, false, 1, 100);
			DateValidator dateOfAdoption = new DateValidator(dateOfAdoptionLabel, this.date_of_adoption, false, false);
			StringValidator quality = new StringValidator(qualityLabel, this.quality, true, true, 0, 100, true);
			IntegerValidator quantity = new IntegerValidator(quantityLabel, this.quantity, true, true);
			StringValidator quantityUnit = new StringValidator(quantityUnitLabel, this.quantity_unit, true, true, 0, 100,true);
			ArrayList validatorList = new ArrayList();
			validatorList.add(videoValidator);
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
					this.video.getId(),
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
					this.video.getId(),
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
												"video_id BIGINT UNSIGNED  NULL DEFAULT NULL," +
												"PRIOR_ADOPTION_FLAG SMALLINT  NULL DEFAULT NULL," +
												"DATE_OF_ADOPTION DATE NOT NULL," +
												"QUALITY VARCHAR(200)  NULL DEFAULT NULL ," +
												"QUANTITY INT  NULL DEFAULT NULL," +
												"QUANTITY_UNIT VARCHAR(150)  NULL DEFAULT NULL, " +
												"FOREIGN KEY(person_id) REFERENCES person(id), " +
												"FOREIGN KEY(video_id) REFERENCES video(id));";
	protected static String dropTable = "DROP TABLE IF EXISTS `person_adopt_practice`;";
	protected static String[] createIndexes = {"CREATE INDEX IF NOT EXISTS person_adopt_practice_PRIMARY ON person_adopt_practice(id);", 
	   "CREATE INDEX IF NOT EXISTS person_adopt_practice_person_id ON person_adopt_practice(person_id);",
	   "CREATE INDEX IF NOT EXISTS person_adopt_practice_video_id ON person_adopt_practice(video_id);"};
	protected static String selectPersonAdoptPractices = "SELECT id, date_of_adoption FROM person_adopt_practice ORDER BY (date_of_adoption);";
	protected static String listPersonAdoptPractices = "SELECT pap.id, p.id, p.person_name," +
			"pap.DATE_OF_ADOPTION,pap.prior_adoption_flag,pap.quality, pap.quantity, pap.quantity_unit," +
			" pg.id, pg.group_name, vil.id, vil.village_name, vid.id, vid.title " +
			"FROM person_adopt_practice pap " +
			"JOIN person p ON p.id = pap.person_id " +
			"JOIN village vil ON p.village_id = vil.id " +
			"LEFT JOIN person_groups pg on p.group_id = pg.id " +
			"LEFT JOIN video vid ON vid.id = pap.video_id  " +
			"ORDER BY pap.id DESC";
	protected static String savePersonAdoptPracticeOnlineURL = "/dashboard/savepersonadoptpracticeonline/";
	protected static String getPersonAdoptPracticeOnlineURL = "/dashboard/getpersonadoptpracticesonline/";
	protected static String savePersonAdoptPracticeOfflineURL = "/dashboard/savepersonadoptpracticeoffline/";
	protected static String getVideoSeenForPersonURL = "/dashboard/getvideosseenforperson/";
	protected static String getBlocksForDistrictURL = "/dashboard/getblocksfordistrictonline/";
	protected static String getVillagesForBlockURL = "/dashboard/getvillagesforblocksonline/";
	protected static String getPersonGroupsForVillageURL = "/dashboard/getpersongroupsforvillageonline/";
	protected static String getPersonForVillageAndNoPersonGroupURL = "/dashboard/getpersonforvillageandnopersongrouponline/";
	protected static String getPersonForPersonGroupsURL = "/dashboard/getpersonforpersongrouponline/";
	protected String table_name = "person_adopt_practice";
	protected String[] fields = {"id", "person_id", "video_id", "prior_adoption_flag", 
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
		VideosData video = new VideosData();
		VillagesData.Data vil = null;
		for(int i = 0; i < personAdoptPracticeObjects.length(); i++){
			PersonGroupsData.Data pg = group.new Data();
			VideosData.Data vid = video.new Data();
			vil = village.new Data(personAdoptPracticeObjects.get(i).getVillage().getPk(),
					personAdoptPracticeObjects.get(i).getVillage().getVillageName());

			if (personAdoptPracticeObjects.get(i).getGroup() != null) {
				pg = group.new Data(personAdoptPracticeObjects.get(i).getGroup()
						.getPk(), personAdoptPracticeObjects.get(i).getGroup()
						.getPersonGroupName());
			}
			if (personAdoptPracticeObjects.get(i).getVideo() != null) {
				vid = video.new Data(personAdoptPracticeObjects.get(i).getVideo().getPk(), personAdoptPracticeObjects.get(i).getVideo().getTitle());
			}
			
			PersonsData.Data p=person.new Data(personAdoptPracticeObjects.get(i).getPerson().getPk(), 
					personAdoptPracticeObjects.get(i).getPerson().getPersonName());
			Data personAdoptPractice = new Data(personAdoptPracticeObjects.get(i).getPk(), p, vid, pg, vil, 
					personAdoptPracticeObjects.get(i).getPriorAdoptionFlag(), personAdoptPracticeObjects.get(i).getDateOfAdoption(),
					personAdoptPracticeObjects.get(i).getQuality(),personAdoptPracticeObjects.get(i).getQuantity(),
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
		VideosData video = new VideosData();
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
				"pap.DATE_OF_ADOPTION,pap.prior_adoption_flag,pap.quality, pap.quantity, pap.quantity_unit," +
				" pg.id, pg.group_name, vil.id, vil.village_name, vid.id, vid.title " +
				"FROM person_adopt_practice pap " +
				"JOIN person p ON p.id = pap.person_id " +
				"JOIN village vil ON p.village_id = vil.id " +
				"LEFT JOIN person_groups pg on p.group_id = pg.id " +
				"LEFT JOIN video vid ON vid.id = pap.video_id " +
				"WHERE (p.person_name LIKE '%"+pageNum[1]+"%' " +
						"OR pg.group_name" +" LIKE '%"+pageNum[1]+"%' "+
						"OR vil.village_name" +	" LIKE '%"+pageNum[1]+"%') ORDER BY pap.id DESC" 
							+ " LIMIT "+ Integer.toString(offset)+" , "+Integer.toString(pageSize)+ ";";
			}
		}
		this.select(listTemp);
		if (this.getResultSet().isValidRow()){
			try {
				for (int i = 0; this.getResultSet().isValidRow(); ++i, this.getResultSet().next()) {
					PersonsData.Data p = person.new Data(this.getResultSet().getFieldAsString(1),  this.getResultSet().getFieldAsString(2));
					PersonGroupsData.Data pg;
					if (this.getResultSet().getFieldAsString(8) == null) {
						pg = null;
					} else {
						pg = group.new Data(this.getResultSet()
								.getFieldAsString(8), this.getResultSet()
								.getFieldAsString(9));
					}
					VillagesData.Data v = vil.new Data(this.getResultSet()
							.getFieldAsString(10), this.getResultSet()
							.getFieldAsString(11));
					VideosData.Data vid = video.new Data(this.getResultSet().getFieldAsString(12),  this.getResultSet().getFieldAsString(13));
					Data personAdoptPractice = new Data(this.getResultSet().getFieldAsString(0), p, vid, pg, v,this.getResultSet().getFieldAsString(3),
							this.getResultSet().getFieldAsString(4),this.getResultSet().getFieldAsString(5),this.getResultSet().getFieldAsString(6),
							this.getResultSet().getFieldAsString(7));
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
		else if(this.validate()) {
			this.save();
			return true;
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
		if(BaseData.isOnline()) {
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
		else {
			return true;
		}
		return false;
	}
	
	public String retrieveBlocksDataAndConvertToHtml(String district_id) {
		BlocksData blocksData = new BlocksData();
		List blocks = blocksData.getAllBlocksForDistrictOffline(district_id);		
		String htmlBlocks = "<option value='' selected='selected'>---------</option>";		
		for(Object block : blocks) {
			htmlBlocks = htmlBlocks + "<option value=\"" + ((BlocksData.Data)block).getId() + "\">" + 
			((BlocksData.Data)block).getBlockName() + "</option>";
		}		
		return htmlBlocks;		
	}
	
	public String retrieveVillagesDataAndConvertToHtml(String block_id) {
		VillagesData villagesData = new VillagesData();
		List villages = villagesData.getAllVillagesForBlockOffline(block_id);		
		String htmlVillages = "<option value='' selected='selected'>---------</option>";		
		for(Object village : villages) {
			htmlVillages = htmlVillages + "<option value=\"" + ((VillagesData.Data)village).getId() + "\">" + 
			((VillagesData.Data)village).getVillageName() + "</option>";
		}
		
		return htmlVillages;
	}
	
	public String retrievePersonsForPersonGroupDataAndConvertToHtml(String person_group_id) {
		PersonsData personsData = new PersonsData();
		List persons = personsData.getAllPersonsForPersonGroupOffline(person_group_id);
		
		String html = "<option value='' selected='selected'>---------</option>";
		
		for(Object person : persons) {
			html = html + "<option value=\"" + ((PersonsData.Data)person).getId() + "\">" + 
			((PersonsData.Data)person).getPersonName() + 
			(((PersonsData.Data)person).getFatherName() == "" ? "": (" (" + ((PersonsData.Data)person).getFatherName() + ")")) + 
					"</option>";
		}
		
		return html;
	}
	
	public String retrievePersonsForVillageDataAndConvertToHtml(String village_id) {
		PersonsData personsData = new PersonsData();
		List persons = personsData.getAllPersonsForVillageAndNoPersonGroupOffline(village_id);
		
		String html = "<option value='' selected='selected'>---------</option>";
		
		for(Object person : persons) {
			html = html + "<option value=\"" + ((PersonsData.Data)person).getId() + "\">" + 
			((PersonsData.Data)person).getPersonName() + 
			(((PersonsData.Data)person).getFatherName() == "" ? "": (" (" + ((PersonsData.Data)person).getFatherName() + ")")) + 
					"</option>";
		}
		
		return html;
	}
	
	public String retrievePersonGroupsDataAndConvertToHtml(String village_id) {
		PersonGroupsData personGroupsData = new PersonGroupsData();
		List personGroups = personGroupsData.getAllPersonGroupsForVillageOffline(village_id);
		
		String htmlPG = "<option value='' selected='selected'>---------</option><option value='null'>No Group</option>";
		
		for(Object personGroup : personGroups) {
			htmlPG = htmlPG + "<option value=\"" + ((PersonGroupsData.Data)personGroup).getId() + "\">" + 
			((PersonGroupsData.Data)personGroup).getPersonGroupName() + "</option>";
		}
		
		return htmlPG;
	}
	
	public String retrieveVideoSeenDataAndConvertToHtml(String person_id) {
		VideosData videosData = new VideosData();
		List videos = videosData.getVideoSeenForPersonOffline(person_id);
		
		String htmlVideo = "<option value='' selected='selected'>---------</option>";
		
		for(Object video : videos) {
			htmlVideo = htmlVideo + "<option value=\"" + ((VideosData.Data)video).getId() + "\">" + 
			((VideosData.Data)video).getTitle() + "</option>";
		}
		return htmlVideo;
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
		
		String htmlVideoOptions = null;
		//Fetch filtered videos if person is present in querystring
		if(this.form.getQueryString() != null) {
			HashMap map = Form.flatten(this.form.getQueryString());
			if(map.containsKey("person")) {
				htmlVideoOptions = retrieveVideoSeenDataAndConvertToHtml(map.get("person").toString());
			}
		}
		
		//person was not present in querystring. fetch all videos in the database
		if(htmlVideoOptions == null) {
			VideosData videoData = new VideosData();
			List videos = videoData.getAllVideosOffline();
			VideosData.Data video;
			htmlVideoOptions = "<option value='' selected='selected'>---------</option>";
			for(int i = 0; i < videos.size(); i++ ) {
				video = (VideosData.Data)videos.get(i);
				htmlVideoOptions = htmlVideoOptions + "<option value=\"" + video.getId() + "\">" + video.getTitle() + " ("+ video.getVillage().getVillageName() +")" 
				+ "</option>";
			}
		}
		String htmlVideo = "<select name=\"video\" id=\"id_video\""  + htmlVideoOptions + "</select>";
		
		return htmlPerson + htmlVideo;
	}
	
	public Object getBlocksForDistrict(String district_id) {
		if(BaseData.isOnline()) {
			this.get(RequestContext.SERVER_HOST + PersonAdoptPracticeData.getBlocksForDistrictURL + district_id + "/");
		}
		else {
			return retrieveBlocksDataAndConvertToHtml(district_id);
		}
		return false;
	}
	
	public Object getVillagesForBlock(String block_id) {
		if(BaseData.isOnline()) {
			this.get(RequestContext.SERVER_HOST + PersonAdoptPracticeData.getVillagesForBlockURL + block_id + "/");
		}
		else {
			return retrieveVillagesDataAndConvertToHtml(block_id);
		}
		return false;
	}
	
	public Object getPersonForVillageAndNoPersonGroup(String village_id) {
		if(BaseData.isOnline()) {
			this.get(RequestContext.SERVER_HOST + PersonAdoptPracticeData.getPersonForVillageAndNoPersonGroupURL + village_id + "/");
		}
		else {
			return retrievePersonsForVillageDataAndConvertToHtml(village_id);
		}
		return false;
	}
	
	public Object getPersonForPersonGroups(String person_group_id) {
		if(BaseData.isOnline()) {
			this.get(RequestContext.SERVER_HOST + PersonAdoptPracticeData.getPersonForPersonGroupsURL + person_group_id + "/");
		}
		else {
			return retrievePersonsForPersonGroupDataAndConvertToHtml(person_group_id);
		}
		return false;
	}
	
	public Object getPersonGroupsForVillage(String village_id) {
		if(BaseData.isOnline()) {
			this.get(RequestContext.SERVER_HOST + PersonAdoptPracticeData.getPersonGroupsForVillageURL + village_id + "/");
		}
		else {
			return retrievePersonGroupsDataAndConvertToHtml(village_id);
		}
		return false;
	}
	
	public Object getVideosForPerson(String person_id) {
		if(BaseData.isOnline()) {
			this.get(RequestContext.SERVER_HOST + PersonAdoptPracticeData.getVideoSeenForPersonURL + person_id + "/");
		}
		else {
			return retrieveVideoSeenDataAndConvertToHtml(person_id);
		}
		return false;
	}
	
	public Object getAddPageData(boolean hasFilters) {
		if(BaseData.isOnline()) {
			this.get(RequestContext.SERVER_HOST + PersonAdoptPracticeData.savePersonAdoptPracticeOnlineURL);
		}
		else{
			if(hasFilters) {
				BlocksData blockData = new BlocksData();
				return blockData.retrieveDataAndConvertResultIntoHtml();
			}
			else {
				return retrieveDataAndConvertResultIntoHtml();
			}
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
		"LEFT JOIN person_groups pg on p.group_id = pg.id LEFT JOIN video vid ON vid.id = pap.video_id " +
		"WHERE (p.person_name LIKE '%"+searchText+"%' " +
							"OR pg.group_name" +" LIKE '%"+searchText+"%' "+
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

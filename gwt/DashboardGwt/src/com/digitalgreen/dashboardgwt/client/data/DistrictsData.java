package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;
import java.util.List;
import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.validation.DateValidator;
import com.digitalgreen.dashboardgwt.client.data.validation.StringValidator;
import com.digitalgreen.dashboardgwt.client.data.validation.UniqueConstraintValidator;
import com.google.gwt.core.client.JsArray;
import com.google.gwt.gears.client.database.DatabaseException;
import com.google.gwt.user.client.Window;

public class DistrictsData extends BaseData {
	
	public static class Type extends BaseData.Type {
		protected Type() {}
		public final native String getDistrictName() /*-{ return $wnd.checkForNullValues(this.fields.district_name); }-*/;
		public final native String getStartDtae() /*-{ return $wnd.checkForNullValues(this.fields.start_date); }-*/ ;
		public final native StatesData.Type getState() /*-{ return this.fields.state; }-*/;
		public final native FieldOfficersData.Type getFieldOfficer() /*-{ return this.fields.fieldofficer; }-*/;
		public final native String getFieldOfficerStartDay() /*-{ return $wnd.checkForNullValues(this.fields.fieldofficer_startday); }-*/;
		public final native PartnersData.Type getPartner() /*-{ return this.fields.partner; }-*/;
	}

	public class Data extends BaseData.Data {
		
		final private String COLLECTION_PREFIX = "district";
		
		private String district_name;
		private String start_date;
		private StatesData.Data state;
		private FieldOfficersData.Data fieldofficer;
		private String fieldofficer_startday;
		private PartnersData.Data partner;
		
		public Data(){
			super();
		}
		
		public Data(String id, String district_name, String start_date, StatesData.Data state, FieldOfficersData.Data fieldofficer, String fieldofficer_startday, PartnersData.Data partner){
			super();
			this.id = id;
			this.district_name = district_name;
			this.start_date = start_date;
			this.state = state;
			this.fieldofficer = fieldofficer;
			this.fieldofficer_startday = fieldofficer_startday;
			this.partner = partner;
		}
		
		public Data(String id, String district_name){
			super();
			this.id = id;
			this.district_name = district_name;
		}
		
		public String getDistrictName(){
			return this.district_name;
		}
		
		public String getStartDate(){
			return this.start_date;
		}
		
		public StatesData.Data getState(){
			return this.state;
		}
		
		public FieldOfficersData.Data getFieldOfficer(){
			return this.fieldofficer;
		}
		
		public String getFieldOfficerStartDay(){
			return this.fieldofficer_startday;
		}
		
		public PartnersData.Data getPartner(){
			return this.partner;
		}
		
		@Override
		public BaseData.Data clone(){
			Data obj = new Data();
			obj.state = (new StatesData()).new Data();
			obj.fieldofficer = (new FieldOfficersData()).new Data();
			obj.partner = (new PartnersData()).new Data();
			return obj;
		}
		
		@Override
		public String getPrefixName(){
			return this.COLLECTION_PREFIX;
		}
		
		@Override
		public void setObjValueFromString(String key, String val) {
			super.setObjValueFromString(key, val);
			if(key.equals("id")) {
				this.id = val;
			}else if(key.equals("district_name")) {
				this.district_name = (String)val;
			} else if(key.equals("start_date")){
				this.start_date = (String)val;
			} else if(key.equals("state")){
				StatesData state1 = new StatesData();
				this.state = state1.getNewData();
				this.state.id = val;				
			} else if(key.equals("fieldofficer")){
				FieldOfficersData fieldofficer1 = new FieldOfficersData();
				this.fieldofficer = fieldofficer1.getNewData();
				this.fieldofficer.id = val;
			} else if(key.equals("fieldofficer_startday")){
				this.fieldofficer_startday = (String)val;
			} else if(key.equals("partner")){
				PartnersData partner1 = new PartnersData();
				this.partner = partner1.getNewData();
				this.partner.id = val;
			} else {
				return;
			}
			this.addNameValueToQueryString(key, val);
		}
		
		@Override
		public boolean validate() {
			//Labels to print validation error messages
			String districtNameLabel = "District Name";
			String startDateLabel = "Start Date";
			String stateLabel = "State";
			String fieldOfficerLabel = "Field officer";
			String fieldOfficerStartDateLabel = "Fieldofficer Start date";
			String partnerLabel = "Partner";
			
			StringValidator districtNameValidator = new StringValidator(districtNameLabel,this.district_name, false, false, 1, 100, true);
			DateValidator startDateValidator = new DateValidator(startDateLabel,this.start_date, true, true);
			StringValidator stateValidator = new  StringValidator(stateLabel,this.state.getId(), false, false, 1, 100);
			StringValidator fieldValidator = new StringValidator(fieldOfficerLabel, this.fieldofficer.getId(), false, false, 1, 100);
			DateValidator fieldOfficerStartDateValidator = new DateValidator(fieldOfficerStartDateLabel,this.fieldofficer_startday, true, true);
			StringValidator partnerValidator = new StringValidator(partnerLabel, this.partner.getId(), false, false, 1, 100);
			
			ArrayList district_name = new ArrayList();
			district_name.add("district_name");
			district_name.add(this.district_name);
			ArrayList uniqueName = new ArrayList();
			uniqueName.add(district_name);
			ArrayList uniqueValidatorLabels = new ArrayList();
			uniqueValidatorLabels.add("District");
			UniqueConstraintValidator uniqueNameValidator = new UniqueConstraintValidator(uniqueValidatorLabels,uniqueName, new DistrictsData());
			uniqueNameValidator.setCheckId(this.getId());
			ArrayList validatorList = new ArrayList();
			validatorList.add(districtNameValidator);
			validatorList.add(startDateValidator);
			validatorList.add(stateValidator);
			validatorList.add(fieldValidator);
			validatorList.add(fieldOfficerStartDateValidator);
			validatorList.add(partnerValidator);
			validatorList.add(uniqueNameValidator);
			return this.executeValidators(validatorList);
		}

		@Override
		public void save(){
			DistrictsData districtsDataDbApis = new DistrictsData();
			this.id = districtsDataDbApis.autoInsert(this.id,
						this.district_name, 
						this.start_date, 
						this.state.getId(), 
						this.fieldofficer.getId(), 
						this.fieldofficer_startday, 
						this.partner.getId());
			this.addNameValueToQueryString("id", this.id);
		}
		
		@Override
		public String toQueryString(String id) {
			DistrictsData districtsData = new DistrictsData();
			return this.rowToQueryString(districtsData.getTableName(), districtsData.getFields(), "id", id, "");
		}
		
		
		@Override
		public String getTableId() {
			DistrictsData districtsDataDbApis = new DistrictsData();
			return districtsDataDbApis.tableID;
		}
	}
	
	public static String tableID = "15";
	final protected static String createTable = "CREATE TABLE IF NOT EXISTS `district` " +
												"(id BIGINT UNSIGNED PRIMARY KEY  NOT NULL ," +
												"DISTRICT_NAME VARCHAR(100)  NOT NULL ," +
												"START_DATE DATE  NULL DEFAULT NULL," +
												"state_id BIGINT UNSIGNED  NOT NULL DEFAULT 0," +
												"fieldofficer_id BIGINT UNSIGNED  NOT NULL DEFAULT 0," +
												"FIELDOFFICER_STARTDAY DATE  NULL DEFAULT NULL," +
												"partner_id BIGINT UNSIGNED  NOT NULL DEFAULT 0, " +
												"FOREIGN KEY(state_id) REFERENCES state(id), " +
												"FOREIGN KEY(fieldofficer_id) REFERENCES field_officer(id), " +
												"FOREIGN KEY(partner_id) REFERENCES partners(id));";  
	protected static String dropTable = "DROP TABLE IF EXISTS `district`;";
	protected static String selectDistricts = "SELECT id, district_name FROM district ORDER BY (district_name)";
	protected static String listDistricts = "SELECT district.id, district.district_name, district.start_date, state.id , state.state_name, " +
			"field_officer.id , field_officer.name, district.fieldofficer_startday, partners.id, partners.partner_name " +
			"FROM district JOIN state ON district.state_id  = state.id JOIN field_officer ON district.fieldofficer_id = field_officer.id " +
			"JOIN partners ON partners.id  = district.partner_id ORDER BY LOWER(district.district_name)";
	protected static String saveDistrictOnlineURL = "/dashboard/savedistrictonline/";
	protected static String getDistrictsOnlineURL = "/dashboard/getdistrictsonline/";
	protected static String saveDistrictOfflineURL = "/dashboard/savedistrictoffline/";
	protected String table_name = "district";
	protected String[] fields = {"id", "district_name", "start_date", "state_id", "fieldofficer_id", "fieldofficer_startday", "partner_id"};
	
	public DistrictsData() {
		super();
	}
	
	public DistrictsData(OnlineOfflineCallbacks callbacks) {
		super(callbacks);
	}
	
	public DistrictsData(OnlineOfflineCallbacks callbacks, Form form) {
		super(callbacks, form);
	}

	@Override
	public Data getNewData() {
		return new Data();
	}
	
	@Override
	protected String getTableId() {
		return DistrictsData.tableID;
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
		return DistrictsData.getDistrictsOnlineURL;
	}
	
	@Override
	public String getSaveOfflineURL(){
		return DistrictsData.saveDistrictOfflineURL;
	}
	
	@Override
	public String getSaveOnlineURL(){
		return DistrictsData.saveDistrictOnlineURL;
	}
	
	public final native JsArray<Type> asArrayOfData(String json) /*-{
		return eval(json);
	}-*/;
	
	public List serialize(JsArray<Type> districtObjects) {
		List districts = new ArrayList();
		StatesData state = new StatesData();
		FieldOfficersData fieldofficer = new FieldOfficersData();
		PartnersData partner = new PartnersData();
		for(int i = 0; i < districtObjects.length(); i++){
			
			StatesData.Data s = state.new Data(districtObjects.get(i).getState().getPk(), districtObjects.get(i).getState().getStateName());
			
			FieldOfficersData.Data f = fieldofficer. new Data(districtObjects.get(i).getFieldOfficer().getPk(), 
					districtObjects.get(i).getFieldOfficer().getFieldOfficerName());
			
			PartnersData.Data p = partner.new Data(districtObjects.get(i).getPartner().getPk(), 
					districtObjects.get(i).getPartner().getPartnerName());
			
			Data district = new Data(districtObjects.get(i).getPk(), districtObjects.get(i).getDistrictName(), districtObjects.get(i).getStartDtae(), s, f, districtObjects.get(i).getFieldOfficerStartDay(), p);
			
			districts.add(district);
		}
		return districts;
	}
	
	@Override
	public List getListingOnline(String json){
		return this.serialize(this.asArrayOfData(json));
	}
	
	// for listing districts for district page
	public List getDistrictsListingsOffline(String... pageNum) {
		BaseData.dbOpen();
		List districts = new ArrayList();
		StatesData state = new StatesData();
		FieldOfficersData fieldofficer = new FieldOfficersData();
		PartnersData partner = new PartnersData();
		String listTemp;
		// Checking whether to return all villages or only limited number of villages
		if(pageNum.length == 0) {
			listTemp = listDistricts;
		}
		else {
			int offset = (Integer.parseInt(pageNum[0]) - 1)*pageSize;
			listTemp = listDistricts + " LIMIT "+ Integer.toString(offset) + " , "+Integer.toString(pageSize) +";";
		}
		this.select(listTemp);
		if(this.getResultSet().isValidRow()){
			try{
				
				for (int i = 0; this.getResultSet().isValidRow(); ++i, this.getResultSet().next()) {

					StatesData.Data s = state. new Data(this.getResultSet().getFieldAsString(3), this.getResultSet().getFieldAsString(4));

					FieldOfficersData.Data f = fieldofficer. new Data(this.getResultSet().getFieldAsString(5), this.getResultSet().getFieldAsString(6));
					
					PartnersData.Data  p = partner. new Data(this.getResultSet().getFieldAsString(8), this.getResultSet().getFieldAsString(9));
					
					Data district = new Data(this.getResultSet().getFieldAsString(0), this.getResultSet().getFieldAsString(1), 
							this.getResultSet().getFieldAsString(2), s, f, this.getResultSet().getFieldAsString(7), p);

					districts.add(district);
				}
			}
			catch (DatabaseException e) {
				Window.alert("Database Exception : " + e.toString());
				BaseData.dbClose();
			}
		}
		BaseData.dbClose();
		return districts;
	}
	
	// for listing all districts used by other forms
	public List getAllDistrictsOffline(){
		BaseData.dbOpen();
		List districts = new ArrayList();
		this.select(selectDistricts);
		if(this.getResultSet().isValidRow()){
			try {
				for (int i = 0; this.getResultSet().isValidRow(); ++i, this.getResultSet().next()) {
					Data district = new Data(this.getResultSet().getFieldAsString(0), this.getResultSet().getFieldAsString(1));
					districts.add(district);
				}
			}
			catch (DatabaseException e) {
				Window.alert("Database Exception : " + e.toString());
				BaseData.dbClose();
			}
		}
		BaseData.dbClose();
		return districts;
	}
	
	public List getTemplateDataOnline(String json){
		List relatedData = null;
		return relatedData;
	}
	
	public Object postPageData() {
		if(BaseData.isOnline()){
			this.post(RequestContext.SERVER_HOST + DistrictsData.saveDistrictOnlineURL, this.form.getQueryString());
		}
		else{
			if(this.validate()) {
				this.save();
				return true;
			}
		}
		
		return false;
	}
	
	public Object postPageData(String id) {
		if(BaseData.isOnline()){
			this.post(RequestContext.SERVER_HOST + this.saveDistrictOnlineURL + id + "/", this.form.getQueryString());
		}
		else{
			if(this.validate()) {
				this.save();
				return true;
			}
		}
		return false;
	}
	
	public Object getListPageData(String pageNum){
		if(BaseData.isOnline()){
			int offset = (Integer.parseInt(pageNum)-1)*pageSize;
			int limit = offset+pageSize;
			this.get(RequestContext.SERVER_HOST + DistrictsData.getDistrictsOnlineURL + Integer.toString(offset) + "/" + Integer.toString(limit)+ "/");
		}
		else{
			return true;
		}
		return false;
	}
		
	public String retrieveDataAndConvertResultIntoHtml() {
		StatesData stateData = new StatesData();
		List states = stateData.getAllStatesOffline();
		StatesData.Data state;
		String htmlState = "<select name=\"state\" id=\"id_state\"" + 
						"<option value='' selected='selected'>---------</option>";
		for(int i=0; i < states.size(); i++){
			state = (StatesData.Data)states.get(i);
			htmlState = htmlState + "<option value=\"" + state.getId() + "\">" + state.getStateName() + "</option>";
		}
		htmlState = htmlState + "</select>";
		
		FieldOfficersData fieldofficerData = new FieldOfficersData();
		List fieldofficers = fieldofficerData.getAllFieldOfficersOffline();
		FieldOfficersData.Data fieldofficer;
		String htmlFO = "<select name=\"fieldofficer\" id=\"id_fieldofficer\"" + 
						"<option value='' selected='selected'>---------</option>";
		for(int i=0; i < fieldofficers.size(); i++){
			fieldofficer = (FieldOfficersData.Data)fieldofficers.get(i);
			htmlFO = htmlFO + "<option value=\"" + fieldofficer.getId() + "\">" + fieldofficer.getFieldOfficerName() + "</option>";
		}
		htmlState = htmlState + "</select>";
		
		PartnersData partnerData = new PartnersData();
		List partners = partnerData.getAllPartnersOffline();
		PartnersData.Data partner;
		String htmlPartner = "<select name=\"partner\" id=\"id_partner\"" + 
							"<option value='' selected='selected'>---------</option>";
		for(int i = 0; i < partners.size(); i++){
			partner = (PartnersData.Data)partners.get(i);
			htmlPartner = htmlPartner + "<option value=\"" + partner.getId() + "\">" + partner.getPartnerName() + "</option>";
		}
		htmlPartner = htmlPartner + "</select>";
		
		return htmlState + htmlFO + htmlPartner;
	}
	
	public Object getAddPageData() {
		if(BaseData.isOnline()) {
			this.get(RequestContext.SERVER_HOST + DistrictsData.saveDistrictOnlineURL);
		}
		else{
			return retrieveDataAndConvertResultIntoHtml();
		}
		return false;
	}
	
	public Object getAddPageData(String id){
		if(BaseData.isOnline()){
			this.get(RequestContext.SERVER_HOST + this.saveDistrictOnlineURL + id + "/" );
		}
		else{
			this.form.toQueryString(id);
			return retrieveDataAndConvertResultIntoHtml();
		}
		return false;
	}
}
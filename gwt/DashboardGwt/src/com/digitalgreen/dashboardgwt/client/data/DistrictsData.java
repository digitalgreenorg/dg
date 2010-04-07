package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;
import java.util.List;
import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.google.gwt.core.client.JsArray;
import com.google.gwt.gears.client.database.DatabaseException;
import com.google.gwt.user.client.Window;

public class DistrictsData extends BaseData {
	
	public static class Type extends BaseData.Type {
		protected Type() {}
		public final native String getDistrictName() /*-{ return this.fields.district_name; }-*/;
		public final native String getStartDtae() /*-{ return this.fields.start_date; }-*/ ;
		public final native StatesData.Type getState() /*-{ return this.fields.state; }-*/;
		public final native FieldOfficersData.Type getFieldOfficer() /*-{ return this.fields.fieldofficer; }-*/;
		public final native String getFieldOfficerStartDay() /*-{ return this.fields.fieldofficer_startday; }-*/;
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
		
		public Data(int id, String district_name, String start_date, StatesData.Data state, FieldOfficersData.Data fieldofficer, String fieldofficer_startday, PartnersData.Data partner){
			super();
			this.id = id;
			this.district_name = district_name;
			this.start_date = start_date;
			this.state = state;
			this.fieldofficer = fieldofficer;
			this.fieldofficer_startday = fieldofficer_startday;
			this.partner = partner;
		}
		
		public Data(int id, String district_name){
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
			obj.id = this.id;
			obj.district_name = this.district_name;
			obj.start_date = this.start_date;
			obj.state = (StatesData.Data)this.state.clone();
			obj.fieldofficer = (FieldOfficersData.Data)this.fieldofficer.clone();
			obj.fieldofficer_startday = this.fieldofficer_startday;
			obj.partner = (PartnersData.Data)this.partner.clone();
			return obj;
		}
		
		@Override
		public String getPrefixName(){
			return this.COLLECTION_PREFIX;
		}
		
		@Override
		public void setObjValueFromString(String key, Object val) {
			if(key.equals("id")) {
				this.id = ((Integer)val).intValue();
			}
			else if(key.equals("district_name")) {
				this.district_name = (String)val;
			}
			else if(key.equals("start_date")){
				this.start_date = (String)val;
			}
			else if(key.equals("state")){
				StatesData state1 = new StatesData();
				this.state = state1.getNewData();
				this.state.id = Integer.parseInt((String)val);				
			}
			else if(key.equals("fieldofficer")){
				FieldOfficersData fieldofficer1 = new FieldOfficersData();
				this.fieldofficer = fieldofficer1.getNewData();
				this.fieldofficer.id = Integer.parseInt((String)val);
			}
			else if(key.equals("fieldofficer_startday")){
				this.fieldofficer_startday = (String)val;
			}
			else if(key.equals("partner")){
				PartnersData partner1 = new PartnersData();
				this.partner = partner1.getNewData();
				this.partner.id = Integer.parseInt((String)val);
			}
		}
		
		@Override
		public void save(){
			DistrictsData districtsDataDbApis = new DistrictsData();
			this.id = districtsDataDbApis.autoInsert(this.district_name, this.start_date, 
					Integer.valueOf(this.state.getId()).toString(), Integer.valueOf(this.fieldofficer.getId()).toString(), 
					this.fieldofficer_startday, Integer.valueOf(this.partner.getId()).toString());
		}
	}
	
	protected static String tableID = "8";
	final protected static String createTable = "CREATE TABLE IF NOT EXISTS `district` " +
												"(id INTEGER PRIMARY KEY  NOT NULL ," +
												"DISTRICT_NAME VARCHAR(100)  NOT NULL ," +
												"START_DATE DATE  NULL DEFAULT NULL," +
												"state_id INT  NOT NULL DEFAULT 0," +
												"fieldofficer_id INT  NOT NULL DEFAULT 0," +
												"FIELDOFFICER_STARTDAY DATE  NULL DEFAULT NULL," +
												"partner_id INT  NOT NULL DEFAULT 0, " +
												"FOREIGN KEY(state_id) REFERENCES state(id), " +
												"FOREIGN KEY(fieldofficer_id) REFERENCES field_officer(id), " +
												"FOREIGN KEY(partner_id) REFERENCES partners(id));";  
	protected static String selectDistricts = "SELECT id, district_name FROM district ORDER BY (district_name)";
	protected static String listDistricts = "SELECT district.id, district.district_name, district.start_date, state.id , state.state_name, field_officer.id , field_officer.name, district.fieldofficer_startday, partners.id, partners.partner_name FROM district JOIN state ON district.state_id  = state.id JOIN field_officer ON district.fieldofficer_id = field_officer.id JOIN partners ON partners.id  = district.partner_id ORDER BY (-district.id);";
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
	
	public DistrictsData(OnlineOfflineCallbacks callbacks, Form form, String queryString) {
		super(callbacks, form, queryString);
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
	protected String getTableName() {
		return this.table_name;
	}
	
	@Override 
	protected String[] getFields() {
		return this.fields;
	}
	
	protected static String getSaveOfflineURL(){
		return DistrictsData.saveDistrictOfflineURL;
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
			
			StatesData.Data s = state.new Data(Integer.parseInt(districtObjects.get(i).getState().getPk()), districtObjects.get(i).getState().getStateName());
			
			FieldOfficersData.Data f = fieldofficer. new Data(Integer.parseInt(districtObjects.get(i).getFieldOfficer().getPk()), 
					districtObjects.get(i).getFieldOfficer().getFieldOfficerName());
			
			PartnersData.Data p = partner.new Data(Integer.parseInt(districtObjects.get(i).getPartner().getPk()), 
					districtObjects.get(i).getPartner().getPartnerName());
			
			Data district = new Data(Integer.parseInt(districtObjects.get(i).getPk()), districtObjects.get(i).getDistrictName(), districtObjects.get(i).getStartDtae(), s, f, districtObjects.get(i).getFieldOfficerStartDay(), p);
			
			districts.add(district);
		}
		return districts;
	}
	
	public List getListingOnline(String json){
		return this.serialize(this.asArrayOfData(json));
	}
	
	// for listing districts for district page
	public List getDistrictsListingsOffline() {
		BaseData.dbOpen();
		List districts = new ArrayList();
		StatesData state = new StatesData();
		FieldOfficersData fieldofficer = new FieldOfficersData();
		PartnersData partner = new PartnersData();
		this.select(listDistricts);
		if(this.getResultSet().isValidRow()){
			try{
				
				for (int i = 0; this.getResultSet().isValidRow(); ++i, this.getResultSet().next()) {

					StatesData.Data s = state. new Data(this.getResultSet().getFieldAsInt(3), this.getResultSet().getFieldAsString(4));

					FieldOfficersData.Data f = fieldofficer. new Data(this.getResultSet().getFieldAsInt(5), this.getResultSet().getFieldAsString(6));
					
					PartnersData.Data  p = partner. new Data(this.getResultSet().getFieldAsInt(8), this.getResultSet().getFieldAsString(9));
					
					Data district = new Data(this.getResultSet().getFieldAsInt(0), this.getResultSet().getFieldAsString(1), 
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
					Data district = new Data(this.getResultSet().getFieldAsInt(0), this.getResultSet().getFieldAsString(1));
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
			this.post(RequestContext.SERVER_HOST + DistrictsData.saveDistrictOnlineURL, this.queryString);
		}
		else{
			this.save();
			return true;
		}
		
		return false;
	}
	
	public Object getListPageData(){
		if(BaseData.isOnline()){
			this.get(RequestContext.SERVER_HOST + DistrictsData.getDistrictsOnlineURL);
		}
		else{
			return true;
		}
		return false;
	}
	
	public String retrieveDataAndConvertResultIntoHtml() {
		StatesData stateData = new StatesData();
		List states = stateData.getStatesListingOffline();
		StatesData.Data state;
		String htmlState = "<select name=\"state\" id=\"id_state\"";
		for(int i=0; i < states.size(); i++){
			state = (StatesData.Data)states.get(i);
			htmlState = htmlState + "<option value=\"" + state.getId() + "\">" + state.getStateName() + "</option>";
		}
		htmlState = htmlState + "</select>";
		
		FieldOfficersData fieldofficerData = new FieldOfficersData();
		List fieldofficers = fieldofficerData.getFieldOfficersListingOffline();
		FieldOfficersData.Data fieldofficer;
		String htmlFO = "<select name=\"fieldofficer\" id=\"id_fieldofficer\"";
		for(int i=0; i < fieldofficers.size(); i++){
			fieldofficer = (FieldOfficersData.Data)fieldofficers.get(i);
			htmlFO = htmlFO + "<option value=\"" + fieldofficer.getId() + "\">" + fieldofficer.getFieldOfficerName() + "</option>";
		}
		htmlState = htmlState + "</select>";
		
		PartnersData partnerData = new PartnersData();
		List partners = partnerData.getPartnersListingOffline();
		PartnersData.Data partner;
		String htmlPartner = "<select name=\"partner\" id=\"id_partner\"";
		for(int i = 0; i < partners.size(); i++){
			partner = (PartnersData.Data)partners.get(i);
			htmlPartner = htmlPartner + "<option value=\"" + partner.getId() + "\">" + partner.getPartnerName() + "</option>";
		}
		
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
}
package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.ReviewersData.Data;
import com.digitalgreen.dashboardgwt.client.data.validation.DateValidator;
import com.digitalgreen.dashboardgwt.client.data.validation.IntegerValidator;
import com.digitalgreen.dashboardgwt.client.data.validation.StringValidator;
import com.google.gwt.core.client.JsArray;
import com.google.gwt.gears.client.database.DatabaseException;
import com.google.gwt.user.client.Window;

public class PartnersData extends BaseData {
	
	public static class Type extends BaseData.Type{
		protected Type() {}
		public final native String getPartnerName() /*-{ return $wnd.checkForNullValues(this.fields.partner_name); }-*/;
		public final native String getDateOfAssociation() /*-{ return $wnd.checkForNullValues(this.fields.date_of_association); }-*/;
		public final native String getPhoneNo() /*-{ return $wnd.checkForNullValues(this.fields.phone_no); }-*/;
		public final native String getAddress() /*-{ return $wnd.checkForNullValues(this.fields.address); }-*/;
	}
	
	public class Data extends BaseData.Data {
		
		final private static String COLLECTION_PREFIX = "partners";
			
		private String partner_name;
		private String date_of_association;
		private String phone_no;
		private String address;
		
		public Data() {
			super();
		}
		
		public Data(String id, String partner_name) {
			super();
			this.id = id;
			this.partner_name = partner_name;
		}
		
		public Data(String id, String partner_name, String date_of_association, String phone_no,
				String address) {
			super();
			this.id = id;
			this.partner_name = partner_name;
			this.date_of_association = date_of_association;
			this.phone_no = phone_no;
			this.address = address;
		}

		
		public String getPartnerName(){
			return this.partner_name;
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
			} 
			else if(key.equals("partner_name")) {
				this.partner_name = (String)val;
			} 
			else if(key.equals("date_of_association")) {
				 this.date_of_association = (String)val;
			} 
			else if(key.equals("phone_no")) {
				 this.phone_no = (String)val;
			} 
			else if(key.equals("address")) {
				 this.address = (String)val;
			} else {
				return;
			}
			this.addNameValueToQueryString(key, val);
		}
		
		public boolean validate(){
			StringValidator nameValidator = new StringValidator(this.partner_name, false, false, 1, 100, true);
			nameValidator.setError("Please make sure that 'Partner Name' is NOT EMPTY and not more than 100 characters.");
			DateValidator dateValidator = new DateValidator(this.date_of_association, true, false);
			dateValidator.setError("Please make sure 'Date of Association' is formatted as 'YYYY-MM-DD'.");
			StringValidator addressValidator = new StringValidator(this.phone_no, true, false, 0, 100);
			addressValidator.setError("Please make sure that 'Phone No' is not more than 100 CHARACTERS");
			StringValidator phoneValidator = new StringValidator(this.address, true, false, 0, 500);
			phoneValidator.setError("Please make sure that 'Phone No' is not more than 500 CHARACTERS");
			ArrayList validatorList = new ArrayList();
			validatorList.add(nameValidator);
			validatorList.add(dateValidator);
			validatorList.add(addressValidator);
			validatorList.add(phoneValidator);
			return this.executeValidators(validatorList);
		}

		@Override
		public void save() {
			PartnersData partnersDataDbApis = new PartnersData();
			this.id = partnersDataDbApis.autoInsert(this.id, 
						this.partner_name, 
						this.date_of_association,
						this.phone_no, 
						this.address);
			this.addNameValueToQueryString("id", this.id);
		}
		
		@Override
		public String toQueryString(String id) {
			PartnersData partnersData = new PartnersData();
			return this.rowToQueryString(partnersData.getTableName(), partnersData.getFields(), "id", id, "");
		}
		
		@Override
		public String getTableId() {
			PartnersData partnersDataDbApis = new PartnersData();
			return partnersDataDbApis.tableID;
		}
		
	}
	
	public static String tableID = "13";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `partners` " +
												"(id BIGINT UNSIGNED PRIMARY KEY  NOT NULL ," +
												"PARTNER_NAME VARCHAR(100)  NOT NULL ," +
												"DATE_OF_ASSOCIATION DATE  NULL DEFAULT NULL," +
												"PHONE_NO VARCHAR(100)  NULL DEFAULT NULL ," +
												"ADDRESS VARCHAR(500)  NULL DEFAULT NULL);"; 
	protected static String dropTable = "DROP TABLE IF EXISTS `partners`;";
	protected static String selectPartners = "SELECT id, partner_name FROM partners ORDER BY(partner_name)";
	protected static String getPartnerByID = "SELECT id, partner_name FROM partners WHERE id = ?";
	protected static String listPartners = "SELECT * FROM partners ORDER BY(-id)";
	protected static String savePartnerOnlineURL = "/dashboard/savepartneronline/";
	protected static String getPartnerOnlineURL = "/dashboard/getpartnersonline/";
	protected static String savePartnerOfflineURL = "/dashboard/savepartneroffline/";
	protected String table_name = "partners";
	protected String[] fields = {"id", "partner_name", "date_of_association", "phone_no", "address"};
	
	public PartnersData() {
		super();

	}
	
	public PartnersData(OnlineOfflineCallbacks callbacks) {
		super(callbacks);
	}
	
	public PartnersData(OnlineOfflineCallbacks callbacks, Form form) {
		super(callbacks, form);
	}

	@Override
	public Data getNewData() {
		return new Data();
	}
	
	@Override
	protected String getTableId() {
		return PartnersData.tableID;
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
		return PartnersData.getPartnerOnlineURL;
	}
	
	@Override
	public String getSaveOfflineURL(){
		return PartnersData.savePartnerOfflineURL;
	}
	
	@Override
	public String getSaveOnlineURL(){
		return PartnersData.savePartnerOnlineURL;
	}
		
	
	public final native JsArray<Type> asArrayOfData(String json) /*-{
		return eval(json);
	}-*/;
	
	public List serialize(JsArray<Type> partnerObjects){
		List partners = new ArrayList();
		
		for(int i = 0; i < partnerObjects.length(); i++){
			
			Data partner = new Data(partnerObjects.get(i).getPk(), partnerObjects.get(i).getPartnerName(),
					partnerObjects.get(i).getDateOfAssociation(), partnerObjects.get(i).getPhoneNo(),
					partnerObjects.get(i).getAddress());
			partners.add(partner);
		}
		return partners;
	}
	
	@Override
	public List getListingOnline(String json){
		return this.serialize(this.asArrayOfData(json));		
	}
	
	public List getPartnersListingOffline(String... pageNum){
		BaseData.dbOpen();
		List partners = new ArrayList();
		String listTemp;
		// Checking whether to return all villages or only limited number of villages
		if(pageNum.length == 0) {
			listTemp = listPartners;
		}
		else {
			int offset = (Integer.parseInt(pageNum[0]) - 1)*pageSize;
			listTemp = listPartners + " LIMIT "+ Integer.toString(offset) + " , "+Integer.toString(pageSize) +";";
		}
		this.select(listTemp);
		if (this.getResultSet().isValidRow()){
			try {
				for (int i = 0; this.getResultSet().isValidRow(); ++i, this.getResultSet().next()) {

					Data partner = new Data(this.getResultSet().getFieldAsString(0), 
							this.getResultSet().getFieldAsString(1),
							this.getResultSet().getFieldAsString(2),
							this.getResultSet().getFieldAsString(3),
							this.getResultSet().getFieldAsString(4));
					partners.add(partner);
	    	      }				
			} catch (DatabaseException e) {
				Window.alert("Database Exception : " + e.toString());
				BaseData.dbClose();
			}
		}
		BaseData.dbClose();
		return partners;
	}

	public List getAllPartnersOffline(){
		BaseData.dbOpen();
		List partners = new ArrayList();
		this.select(selectPartners);
		if (this.getResultSet().isValidRow()){
			try {
				for (int i = 0; this.getResultSet().isValidRow(); ++i, this.getResultSet().next()) {
					Data partner = new Data(this.getResultSet().getFieldAsString(0), this.getResultSet().getFieldAsString(1));
					partners.add(partner);
	    	      }				
			} catch (DatabaseException e) {
				Window.alert("Database Exception : " + e.toString());
				BaseData.dbClose();
			}
			
		}
		BaseData.dbClose();
		return partners;
	}


	public Object postPageData() {
		if(BaseData.isOnline()){
			this.post(RequestContext.SERVER_HOST + PartnersData.savePartnerOnlineURL, this.form.getQueryString());
		}
		else{
			if(this.validate()){
				this.save();
				return true;
			}
		}
		
		return false;
	}
	
	public Object postPageData(String id) {
		if(BaseData.isOnline()){
			this.post(RequestContext.SERVER_HOST + this.savePartnerOnlineURL + id + "/", this.form.getQueryString());
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
			this.get(RequestContext.SERVER_HOST + PartnersData.getPartnerOnlineURL+Integer.toString(offset)+"/"+Integer.toString(limit)+ "/");
		}
		else{
			return true;
		}
		return false;
	}
	
	public Object getAddPageData(){
		if(BaseData.isOnline()){
			this.get(RequestContext.SERVER_HOST + this.savePartnerOnlineURL);
		}
		else{
			return "No add data required";
		}
		return false;
	}
	
	public Object getAddPageData(String id){
		if(BaseData.isOnline()){
			this.get(RequestContext.SERVER_HOST + this.savePartnerOnlineURL + id + "/" );
		}
		else{
			this.form.toQueryString(id);
			return "No add data required";
		}
		return false;
	}
	
}
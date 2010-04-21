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
		public final native String getReviewer() /*-{ return this.fields.reviewer; }-*/;
		public final native String getEquipmentHolder() /*-{ return this.fields.equipmentholder; }-*/;
	}
	
	public class Data extends BaseData.Data {
		
		final private static String COLLECTION_PREFIX = "partners";
			
		private String partner_name;
		private String date_of_association;
		private String phone_no;
		private String address;
		private String reviewer;
		private String equipmentholder;
		
		public Data() {
			super();
		}
		
		public Data(String id, String partner_name) {
			super();
			this.id = id;
			this.partner_name = partner_name;
		}
		
		public Data(String id, String partner_name, String date_of_association, String phone_no,
				String address,String reviewer, String equipmentholder) {
			super();
			this.id = id;
			this.partner_name = partner_name;
			this.date_of_association = date_of_association;
			this.phone_no = phone_no;
			this.address = address;
			this.reviewer = reviewer;
			this.equipmentholder = equipmentholder;
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
			} 
			else if(key.equals("reviewer")) {
				 this.reviewer = val;
			} else if(key.equals("equipmentholder")) {
				this.equipmentholder = (String)val;
			}
		}
		public boolean validate(){
			StringValidator nameValidator = new StringValidator(this.partner_name, false, false, 1, 100);
			nameValidator.setError("Please make sure that 'Partner Name' is NOT EMPTY and not more than 100 CHARACTERS");
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
						this.address, 
						this.reviewer, 
						this.equipmentholder);
		}
	}
	
	public static String tableID = "13";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `partners` " +
												"(id INTEGER PRIMARY KEY  NOT NULL ," +
												"PARTNER_NAME VARCHAR(100)  NOT NULL ," +
												"DATE_OF_ASSOCIATION DATE  NULL DEFAULT NULL," +
												"PHONE_NO VARCHAR(100)  NULL DEFAULT NULL ," +
												"ADDRESS VARCHAR(500)  NULL DEFAULT NULL ," +
												"reviewer_id INT  NULL DEFAULT NULL," +
												"equipmentholder_id INT  NULL DEFAULT NULL, " +
												"FOREIGN KEY(reviewer_id) REFERENCES reviewer(id), " +
												"FOREIGN KEY(equipmentholder_id) REFERENCES equipment_holder(id) );"; 
	protected static String dropTable = "DROP TABLE IF EXISTS `partners`;";
	protected static String selectPartners = "SELECT id, partner_name FROM partners ORDER BY(partner_name)";
	protected static String getPartnerByID = "SELECT id, partner_name FROM partners WHERE id = ?";
	protected static String listPartners = "SELECT * FROM partners ORDER BY(-id)";
	protected static String savePartnerOnlineURL = "/dashboard/savepartneronline/";
	protected static String getPartnerOnlineURL = "/dashboard/getpartnersonline/";
	protected static String savePartnerOfflineURL = "/dashboard/savepartneroffline/";
	protected String table_name = "partners";
	protected String[] fields = {"id", "partner_name", "date_of_association", "phone_no", "address",
			"reviewer_id", "equipmentholder_id"};
	
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
		
	
	public final native JsArray<Type> asArrayOfData(String json) /*-{
		return eval(json);
	}-*/;
	
	public List serialize(JsArray<Type> partnerObjects){
		List partners = new ArrayList();
		ReviewersData reviewer = new ReviewersData();
		EquipmentHoldersData equipmentholder = new EquipmentHoldersData();
		
		for(int i = 0; i < partnerObjects.length(); i++){
			
			Data partner = new Data(partnerObjects.get(i).getPk(), partnerObjects.get(i).getPartnerName(),
					partnerObjects.get(i).getDateOfAssociation(), partnerObjects.get(i).getPhoneNo(),
					partnerObjects.get(i).getAddress(), partnerObjects.get(i).getReviewer(),
					partnerObjects.get(i).getEquipmentHolder());
			partners.add(partner);
		}
		return partners;
	}
	
	@Override
	public List getListingOnline(String json){
		return this.serialize(this.asArrayOfData(json));		
	}
	
	public List getPartnersListingOffline(){
		BaseData.dbOpen();
		ReviewersData reviewer = new ReviewersData();
		EquipmentHoldersData equipmentholder = new EquipmentHoldersData();
		List partners = new ArrayList();
		this.select(listPartners);
		if (this.getResultSet().isValidRow()){
			try {
				for (int i = 0; this.getResultSet().isValidRow(); ++i, this.getResultSet().next()) {

					Data partner = new Data(this.getResultSet().getFieldAsString(0), 
							this.getResultSet().getFieldAsString(1),
							this.getResultSet().getFieldAsString(2),
							this.getResultSet().getFieldAsString(3),
							this.getResultSet().getFieldAsString(4),
							this.getResultSet().getFieldAsString(5),
							this.getResultSet().getFieldAsString(6));
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
	
	public Object getPageData(){
		if(BaseData.isOnline()){
			this.get(RequestContext.SERVER_HOST + PartnersData.getPartnerOnlineURL);
		}
		else{
			return true;
		}
		return false;
	}
}
package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;

import com.google.gwt.core.client.JsArray;
import com.google.gwt.gears.client.database.DatabaseException;
import com.google.gwt.user.client.Window;

public class PartnersData extends BaseData {
	
	public static class Type extends BaseData.Type{
		protected Type() {}
		public final native String getPartnerName() /*-{ return this.fields.partner_name; }-*/;
		public final native String getDateOfAssociation() /*-{ return this.fields.date_of_association; }-*/;
		public final native String getPhoneNo() /*-{ return this.fields.phone_no; }-*/;
		public final native String getAddress() /*-{ return this.fields.address; }-*/;
		public final native int getReviewerId() /*-{ return this.fields.reviewer_id; }-*/;
		public final native int getEquipmentHolderId() /*-{ return this.fields.equipmentholder_id; }-*/;
	}
	
	public class Data extends BaseData.Data {
		
		final private static String COLLECTION_PREFIX = "partners";
			
		private String partner_name;
		private String date_of_association;
		private String phone_no;
		private String address;
		private int reviewer_id;
		private int equipmentholder_id;
		
		public Data() {
			super();
		}
		
		public Data(int id, String partner_name, String date_of_association, String phone_no,
				String address, int reviewer_id, int equipmentholder_id) {
			super();
			this.id = id;
			this.partner_name = partner_name;
			this.date_of_association = date_of_association;
			this.phone_no = phone_no;
			this.address = address;
			this.reviewer_id = reviewer_id;
			this.equipmentholder_id = equipmentholder_id;
		}
		
		public String getPartnerName(){
			return this.partner_name;
		}
		
		public Object clone() {
			Data obj = new Data();
			obj.id = this.id;
			obj.partner_name = this.partner_name;
			obj.date_of_association = this.date_of_association;
			obj.phone_no = this.phone_no;
			obj.address = this.address;
			obj.reviewer_id = this.reviewer_id;
			obj.equipmentholder_id = this.equipmentholder_id;
			return obj;
		}
		
		@Override
		public String getPrefixName() {
			return Data.COLLECTION_PREFIX;
		}
		
		@Override
		public void setObjValueFromString(String key, Object val) {
			if(key.equals("id")) {
				this.id = ((Integer)val).intValue();
			} else if(key.equals("partner_name")) {
				this.partner_name = (String)val;
			} else if(key.equals("date_of_association")) {
				 this.date_of_association = (String)val;
			} else if(key.equals("phone_no")) {
				 this.phone_no = (String)val;
			} else if(key.equals("address")) {
				 this.address = (String)val;
			} else if(key.equals("reviewer_id")) {
				 this.reviewer_id = ((Integer)val).intValue();
			} else if(key.equals("equipmentholder_id")) {
				this.equipmentholder_id = ((Integer)val).intValue();
			}
		}
		
		@Override
		public void save() {
			PartnersData partnersDataDbApis = new PartnersData();
			this.id = partnersDataDbApis.autoInsert(this.partner_name, this.date_of_association,
					this.phone_no, this.address, Integer.valueOf(this.reviewer_id).toString(), 
					Integer.valueOf(this.equipmentholder_id).toString());
		}
	}
	
	
	protected static String tableID = "06";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `partners` " +
												"(id INTEGER PRIMARY KEY  NOT NULL ," +
												"PARTNER_NAME VARCHAR(100)  NOT NULL ," +
												"DATE_OF_ASSOCIATION DATE  NULL DEFAULT NULL," +
												"PHONE_NO VARCHAR(100)  NOT NULL ," +
												"ADDRESS VARCHAR(500)  NOT NULL ," +
												"reviewer_id INT  NULL DEFAULT NULL," +
												"equipmentholder_id INT  NULL DEFAULT NULL, " +
												"FOREIGN KEY(reviewer_id) REFERENCES reviewer(id), " +
												"FOREIGN KEY(equipmentholder_id) REFERENCES equipment_holder(id) );"; 
	

	protected static String listPartners = "SELECT * FROM partners ORDER BY(-id)";
	protected static String savePartnerURL = "/dashboard/savepartner/";
	protected static String getPartnerURL = "/dashboard/getpartners/";
	protected String table_name = "partners";
	protected String[] fields = {"id", "partner_name", "date_of_association", "phone_no", "address",
			"reviewer_id", "equipmentholder_id"};
	
	public PartnersData() {
		super();

	}
	
	public PartnersData(OnlineOfflineCallbacks callbacks) {
		super(callbacks);
	}
	
	public PartnersData(OnlineOfflineCallbacks callbacks, Form form, String queryString) {
		super(callbacks, form, queryString);
	}

	@Override
	public Data getNewData() {
		return new Data();
	}
	
	@Override
	protected String getTableId() {
		return PartnersData.tableID;
	}
	
	protected String getTableName() {
		return this.table_name;
	}
	
	protected String[] getFields() {
		return this.fields;
	}
	
	public final native JsArray<Type> asArrayOfData(String json) /*-{
		return eval(json);
	}-*/;
	
	public List serialize(JsArray<Type> partnerObjects){
		List partners = new ArrayList();
		for(int i = 0; i < partnerObjects.length(); i++){
			Data partner = new Data(Integer.parseInt(partnerObjects.get(i).getPk()), partnerObjects.get(i).getPartnerName(),
					partnerObjects.get(i).getDateOfAssociation(), partnerObjects.get(i).getPhoneNo(),
					partnerObjects.get(i).getAddress(), partnerObjects.get(i).getReviewerId(),
					partnerObjects.get(i).getEquipmentHolderId());
			partners.add(partner);
		}
		
		return partners;
	}
	
	public List getPartnersOnline(String json){
		return this.serialize(this.asArrayOfData(json));		
	}
	
	public List getPartnersOffline(){
		BaseData.dbOpen();
		List partners = new ArrayList();
		this.select(listPartners);
		if (this.getResultSet().isValidRow()){
			try {
				for (int i = 0; this.getResultSet().isValidRow(); ++i, this.getResultSet().next()) {
					Data partner = new Data(this.getResultSet().getFieldAsInt(0), 
							this.getResultSet().getFieldAsString(1),
							this.getResultSet().getFieldAsString(2),
							this.getResultSet().getFieldAsString(3),
							this.getResultSet().getFieldAsString(4),
							this.getResultSet().getFieldAsInt(5),
							this.getResultSet().getFieldAsInt(6));
					partners.add(partner);
	    	      }				
			} catch (DatabaseException e) {
				Window.alert("Database Exception : " + e.toString());
				// TODO Auto-generated catch block
				BaseData.dbClose();
			}
			
		}
		BaseData.dbClose();
		return partners;
	}

	public Object postPageData() {
		if(BaseData.isOnline()){
			this.post(RequestContext.SERVER_HOST + this.savePartnerURL, this.queryString);
		}
		else{
			this.save();
			return true;
		}
		
		return false;
	}
	
	public Object getPageData(){
		if(BaseData.isOnline()){
			this.get(RequestContext.SERVER_HOST + PartnersData.getPartnerURL);
		}
		else{
			return true;
		}
		return false;
	}
}
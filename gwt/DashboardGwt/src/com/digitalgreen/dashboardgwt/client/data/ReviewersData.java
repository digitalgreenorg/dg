package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import com.digitalgreen.dashboardgwt.client.data.AnimatorsData.Data;
import com.digitalgreen.dashboardgwt.client.common.ApplicationConstants;
import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.google.gwt.core.client.JsArray;
import com.google.gwt.gears.client.database.DatabaseException;
import com.google.gwt.user.client.Window;
import com.digitalgreen.dashboardgwt.client.data.ReviewersData.Type;

public class ReviewersData extends BaseData {
	
	public static class Type extends BaseData.Type{
		protected Type() {}
		public final native String getContentType() /*-{ return $wnd.checkForNullValues(this.fields.content_type); }-*/;
		public final native String getObjectId() /*-{ return $wnd.checkForNullValues(this.fields.object_id); }-*/;
	}
	
	public class Data extends BaseData.Data {
		
		final private static String COLLECTION_PREFIX = "reviewer";
			
		private String content_type;
		private String object_id;
		private String reviewer_name; //This field doesn't exist in the Django Model. Made to take care of generic foreign key references.
		
		public Data() {
			super();
		}
		
		public Data(String id, String content_type, String object_id){
			super();
			this.id = id;
			this.content_type = content_type;
			this.object_id = object_id;
		}
		
		public Data(String id ) {
			super();
			this.id = id;
		}
		
		public Data(String id, String reviewer_name ) {
			super();
			this.id = id;
			this.reviewer_name = reviewer_name;
		}
		
		public String getContentType(){
			return this.content_type;
		}
		
		public String getObjectId(){
			return this.object_id;
		}
		
		public String getReviewerName(){
			return this.reviewer_name;
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
			if(key.equals("content_type")) {
				this.content_type = (String)val;
			} else if(key.equals("object_id")) {
				this.object_id = (String)val;
			} else {
				return;
			}
			this.addNameValueToQueryString(key, val);			
		}
		
		@Override
		public void save() {
			ReviewersData reviewersDataDbApis = new ReviewersData();
			this.id = reviewersDataDbApis.autoInsert(this.id, 
					this.content_type, 
					this.object_id);
			this.addNameValueToQueryString("id", this.id);
		}
		
		@Override
		public String getTableId() {
			ReviewersData reviewersDataDbApis = new ReviewersData();
			return reviewersDataDbApis.tableID;
		}
	}

	public static String tableID = "10";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `reviewer` " +
												"(id INTEGER PRIMARY KEY NOT NULL ," +
												"content_type_id INT NOT NULL DEFAULT 0," +
												"object_id INT NOT NULL DEFAULT 0);"; 
	protected static String selectReviewers = "SELECT * FROM reviewer ORDER BY(-id)";
	protected static String listReviewers = "SELECT * FROM reviewer ORDER BY(-id)";
	protected static String saveReviewerOnlineURL = "/dashboard/saverevieweronline/";
	protected static String getReviewerOnlineURL = "/dashboard/getreviewersonline/";
	protected static String saveReviewerOfflineURL = "/dashboard/saverevieweroffline/";
	protected String table_name = "reviewer";
	protected String[] fields = {"id", "content_type", "object_id"};
	
	
	public ReviewersData() {
		super();
	}
	
	public ReviewersData(OnlineOfflineCallbacks callbacks) {
		super(callbacks);
	}
	
	public ReviewersData(OnlineOfflineCallbacks callbacks, Form form) {
		super(callbacks, form);
	}

	@Override
	public Data getNewData() {
		return new Data();
	}
	
	@Override
	protected  String getTableId() {
		return ReviewersData.tableID;
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
		return ReviewersData.getReviewerOnlineURL;
	}
	
	@Override
	public String getSaveOfflineURL(){
		return ReviewersData.saveReviewerOfflineURL;
	}

	public final native JsArray<Type> asArrayOfData(String json) /*-{
		return eval(json);
	}-*/;
	
	public List serialize(JsArray<Type> reviewerObjects){
		List reviewers = new ArrayList();
		for(int i = 0; i < reviewerObjects.length(); i++){
			Data reviewer = new Data(reviewerObjects.get(i).getPk(), 
					reviewerObjects.get(i).getContentType(), 
					reviewerObjects.get(i).getObjectId());
			reviewers.add(reviewer);
		}
		return reviewers;
	}
	
	@Override
	public List getListingOnline(String json){
		return this.serialize(this.asArrayOfData(json));		
	}		
	
	public List getAllReviewersOffline(){
		BaseData.dbOpen();
		List reviewers = new ArrayList();
		this.select(selectReviewers);
		if(this.getResultSet().isValidRow()){
			try {
				String reviewerName = "";
				for(int i = 0; this.getResultSet().isValidRow(); ++i, this.getResultSet().next()){
					
					// Get the name of the reviewer (Generic Foreign Key to Development Manager, Field Officer and Partner)
					if(this.getResultSet().getFieldAsString(1) == DevelopmentManagersData.tableID){
						DevelopmentManagersData dm = (DevelopmentManagersData)ApplicationConstants.mappingBetweenTableIDAndDataObject.get(this.getResultSet().getFieldAsString(1));
						dm.select(dm.getDevelopmentManagerByID, this.getResultSet().getFieldAsString(2));
						reviewerName = dm.getResultSet().getFieldAsString(1);
					} else if(this.getResultSet().getFieldAsString(1) == FieldOfficersData.tableID){
						FieldOfficersData fo = (FieldOfficersData)ApplicationConstants.mappingBetweenTableIDAndDataObject.get(this.getResultSet().getFieldAsString(1));
						fo.select(fo.getFieldOfficerByID, this.getResultSet().getFieldAsString(2));
						reviewerName = fo.getResultSet().getFieldAsString(1);
					} else if(this.getResultSet().getFieldAsString(1) == PartnersData.tableID){
						PartnersData p = (PartnersData)ApplicationConstants.mappingBetweenTableIDAndDataObject.get(this.getResultSet().getFieldAsString(1));
						p.select(p.getPartnerByID, this.getResultSet().getFieldAsString(2));
						reviewerName = p.getResultSet().getFieldAsString(1);
					} 
					
					Data reviewer = new Data(this.getResultSet().getFieldAsString(0), reviewerName);
					reviewers.add(reviewer);
				}
			}
			catch(DatabaseException e){
				Window.alert("Database Exception : " + e.toString());
				BaseData.dbClose();
			}
		}
		BaseData.dbClose();
		return reviewers;
	}
}
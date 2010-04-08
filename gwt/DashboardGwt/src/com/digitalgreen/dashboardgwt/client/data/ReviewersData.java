package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import com.digitalgreen.dashboardgwt.client.data.AnimatorsData.Data;
import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.google.gwt.core.client.JsArray;
import com.google.gwt.gears.client.database.DatabaseException;
import com.google.gwt.user.client.Window;
import com.digitalgreen.dashboardgwt.client.data.ReviewersData.Type;

public class ReviewersData extends BaseData {
	
	public static class Type extends BaseData.Type{
		protected Type() {}
		public final native String getContentType() /*-{ return this.fields.content_type; }-*/;
		public final native String getObjectId() /*-{ return this.fields.object_id; }-*/;
	}
	
	public class Data extends BaseData.Data {
		
		final private static String COLLECTION_PREFIX = "reviewer";
			
		private String content_type;
		private String object_id;
		
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
		
		public String getContentType(){
			return this.content_type;
		}
		
		public String getObjectId(){
			return this.object_id;
		}
		
		public BaseData.Data clone() {
			Data obj = new Data();
			obj.id = this.id;
			obj.content_type = this.content_type;
			obj.object_id = this.object_id;
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
			} else if(key.equals("content_type")) {
				this.content_type = (String)val;
			} else if(key.equals("object_id")) {
				this.object_id = (String)val;
			}			
		}
		
		@Override
		public void save() {
			ReviewersData reviewersDataDbApis = new ReviewersData();
<<<<<<< .mine
			this.id = reviewersDataDbApis.autoInsert(this.content_type, this.object_id);
=======
			if(this.id==0){
				this.id = reviewersDataDbApis.autoInsert(Integer.valueOf(this.id).toString(), this.content_type, this.object_id);
			}
			else{
				this.id = reviewersDataDbApis.autoInsert( this.content_type, this.object_id);
			}
			
>>>>>>> .r278
		}
	}

	protected static String tableID = "3";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `reviewer` " +
												"(id INTEGER PRIMARY KEY NOT NULL ," +
												"content_type_id INT NOT NULL DEFAULT 0," +
												"object_id INT NOT NULL DEFAULT 0);"; 
	protected static String selectReviewers = "SELECT id FROM equipment_holder ORDER BY(-id)";
	protected static String listReviewers = "SELECT * FROM equipment_holder ORDER BY(-id)";
	protected static String saveReviewerOnlineURL = "/dashboard/saverevieweronline/";
	protected static String getReviewerOnlineURL = "/dashboard/getreviewersonline/";
	protected static String saveReviewerOfflineURL = "/dashboard/saverevieweroffline/";
	protected String table_name = "equipment_holder";
	protected String[] fields = {"id", "content_type", "object_id"};
	
	
	public ReviewersData() {
		super();
	}
	
	public ReviewersData(OnlineOfflineCallbacks callbacks) {
		super(callbacks);
	}
	
	public ReviewersData(OnlineOfflineCallbacks callbacks, Form form, String queryString) {
		super(callbacks, form, queryString);
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

	public final native JsArray<Type> asArrayOfData(String json) /*-{
		return eval(json);
	}-*/;
	
	public List serialize(JsArray<Type> reviewerObjects){
		List reviewers = new ArrayList();
		for(int i = 0; i < reviewerObjects.length(); i++){
			Data reviewer = new Data(Integer.parseInt(reviewerObjects.get(i).getPk()), 
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
}
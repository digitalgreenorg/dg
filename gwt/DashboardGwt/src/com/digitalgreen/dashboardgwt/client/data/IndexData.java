package com.digitalgreen.dashboardgwt.client.data;

import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.google.gwt.gears.client.database.ResultSet;

public class IndexData extends BaseData {
	
	protected static String postURL = "/dashboard/getkey/";
	protected static String indexDataURL = "/dashboard/getindexdata/";
	public final static int STATUS_READY = 0;
	public final static int STATUS_DB_NOT_OPEN = 1;
	public final static int STATUS_SCHEMA_NOT_READY = 2;
	
	
	public static class Type extends BaseData.Type{
		protected Type() {}
		public final native String getDashboardErrorCount() /*-{ return $wnd.checkForNullValues(this.dashboard_error_count); }-*/;
	}
	
	public class Data extends BaseData.Data {
		
		final private static String COLLECTION_PREFIX = "index";

		private String dashboardErrorCount;
		
		public Data() {
			super();
		}
		
		public Data(String dashboardErrorCount) {
			super();
			this.dashboardErrorCount = dashboardErrorCount;
		}
		
		public String getDashboardErrorCount(){
			return this.dashboardErrorCount;
		}
		
		public BaseData.Data clone() {
			Data obj = new Data();
			return obj;
		}
		
		@Override
		public String getPrefixName() {
			return Data.COLLECTION_PREFIX;
		}
		
	}
	
	public final native Type asArrayOfData(String json) /*-{
		return eval('('+json+')');
	}-*/;
	
	public Data serialize(Type indexData){
		if(indexData!=null)
			return  new Data(indexData.getDashboardErrorCount());
		else 
			return null;
	}

	public Data getIndexPageDataOnline(String json){
		return this.serialize(this.asArrayOfData(json));		
	}
	
	public Data getIndexPageDataOffline() {
		return new Data(null);
	}
	
	public Object getIndexPageData(){
		if(BaseData.isOnline()){
			this.get(RequestContext.SERVER_HOST + IndexData.indexDataURL);
		}
		else{
			return true;
		}
		return false;
	}
	
	public IndexData(OnlineOfflineCallbacks callbacks) {
		super(callbacks);
	}

	public IndexData() {
		super();
	}

	public static void createTables(){
		Schema.createSchema();
	}

	public Object getGlobalPrimaryKey(String username) {
		// Make a call to the Django view and get the primary key
		String postData = "username=" + username;
		this.post(RequestContext.SERVER_HOST + this.postURL, postData);
		return true;
	}
	
	public int checkIfOfflineReady(String username){
			if(!BaseData.dbOpen()) {
				return IndexData.STATUS_DB_NOT_OPEN;
			}
			this.select(LoginData.selectUser , username);
			ResultSet resultSet = this.getResultSet();
			if(this.isValidResultSet()) {		
				BaseData.dbClose();
				return IndexData.STATUS_READY;
			}
			else{
				BaseData.dbClose();
				return IndexData.STATUS_SCHEMA_NOT_READY;
			}
	}
}
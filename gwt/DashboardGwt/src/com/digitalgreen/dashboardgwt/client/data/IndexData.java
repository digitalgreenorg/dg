package com.digitalgreen.dashboardgwt.client.data;

import com.digitalgreen.dashboardgwt.client.common.ApplicationConstants;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.google.gwt.gears.client.database.DatabaseException;
import com.google.gwt.gears.client.database.ResultSet;

public class IndexData extends BaseData {
	
	protected static String postURL = "/dashboard/getkey/";
	protected static String indexDataURL = "/dashboard/getindexdata/";
	public final static int STATUS_READY = 0;
	public final static int STATUS_DB_NOT_OPEN = 1;
	public final static int STATUS_SCHEMA_NOT_READY = 2;
	public final static int STATUS_DB_NOT_COMPLETE = 3;
	protected static String getDashboardErrorCountSQL = "SELECT dashboard_error_count FROM user;";
	
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
		BaseData.dbOpen();
		this.select(this.getDashboardErrorCountSQL);
		ResultSet rs = this.getResultSet();
		String count = null;
		if(rs!=null && rs.isValidRow()) {
			try {
				count = new Integer(rs.getFieldAsInt(0)).toString();
			} catch (DatabaseException e) {
				BaseData.dbClose();
				e.printStackTrace();
			}
		}
		BaseData.dbClose();
		return new Data(count);
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
	
	public static native boolean isInternetConnected() /*-{
		return navigator.onLine;
	}-*/;
	
	/*public static native boolean isGearsAvailable() /*-{
		Window.alert("Window.Google " + window.google + " & " + "Google.gears " + google.gears);
		if (window.google!=null && google.gears!=null) {
			return true;
		}
		return false;
	}-*/;
	
	public boolean dbHasUnsyncedRows() {
		if(!BaseData.dbOpen()) {
			// if no DB, then no Unsynced rows :)
			return false;
		}
		this.select(FormQueueData.countUnsyncTableRow);
		ResultSet resultSet = this.getResultSet();
		if (resultSet!=null && resultSet.isValidRow()) {
			try {
				int totalUnsyncRows = resultSet.getFieldAsInt(0);
				if (totalUnsyncRows!=0) {
					BaseData.dbClose();
					return true;
				}
			} catch(DatabaseException e) {
				//Window.alert("Database Exception : " + e.toString());
				BaseData.dbClose();
			}
		}
		return false;
	}
	
	public int dbNotDownloaded(String username) throws DatabaseException {
		if(!BaseData.dbOpen()) {
			return IndexData.STATUS_DB_NOT_OPEN;
		}
		this.select(LoginData.selectUser , username);
		ResultSet resultSet = this.getResultSet();
		if(resultSet!=null && this.isValidResultSet()) {
			resultSet.close();
			this.select(LoginData.getSyncStatus, username);
			resultSet = this.getResultSet();
			if (resultSet.isValidRow()) {
				int last_table_index = resultSet.getFieldAsInt(1);
				if (last_table_index == ApplicationConstants.tableIDs.length) {
					BaseData.dbClose();
					return IndexData.STATUS_READY;
				}
			}
			
		}
		BaseData.dbClose();
		return IndexData.STATUS_SCHEMA_NOT_READY; // return 0
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
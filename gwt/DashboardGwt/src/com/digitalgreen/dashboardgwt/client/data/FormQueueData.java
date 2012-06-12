package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;
import java.util.Date;

import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.google.gwt.gears.client.database.DatabaseException;
import com.google.gwt.user.client.Window;

public class FormQueueData extends BaseData {

	public class Data extends BaseData.Data {
		
		final public static String ACTION_ADD = "A";
		final public static String ACTION_EDIT = "E";
		
		final public static String SYNC_READY = "0";
		final public static String SYNC_DONE = "1";
		
		private String table_id;
		private String global_pk_id;
		private String queryString;
		private String syncStatus;
		private String action;
		private long timestamp;

		public Data(String table_id, String global_pk_id, String queryString) {
			this.table_id = table_id;
			this.global_pk_id = global_pk_id;
			this.queryString = queryString;
			this.timestamp = (new Date()).getTime();
		}
		
		public void setAction(String action) {
			this.action = action;
		}
		
		public void setSyncStatus(String syncStatus) {
			this.syncStatus = syncStatus;
		}

		@Override
		public void save() {
			FormQueueData formQueueData = new FormQueueData();
			formQueueData.systemAutoIncrement = true;
			formQueueData.autoInsert(this.id,
					this.table_id,
					this.global_pk_id,
					this.queryString,
					this.syncStatus,
					this.action,
					String.valueOf(this.timestamp));
		}	
	}
	
	protected ArrayList formQueryStringList = null;
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `formqueue` " +
										  "(id INTEGER PRIMARY KEY, " +
										  "table_id INTEGER NOT NULL, " +
										  "global_pk_id BIGINT UNSIGNED NOT NULL, " +
										  "querystring VARCHAR NOT NULL, " +
										  "sync_status BOOLEAN, " +
										  "action CHAR(1) NOT NULL," +
										  "timestamp BIGINT UNSIGNED NOT NULL);";
	protected static String dropTable = "DROP TABLE IF EXISTS `formqueue`;";
	protected static String getUnsyncTableRow = "SELECT * FROM `formqueue` WHERE sync_status=0 ORDER BY id LIMIT 1";
	protected static String countUnsyncTableRow = "SELECT COUNT(1) FROM `formqueue` WHERE sync_status=0";
	protected static String updateSyncStatusOfARow = "UPDATE `formqueue` SET sync_status=1 WHERE id=?" ;
	protected static String getMaxGlobalPkId = "SELECT MAX(global_pk_id) FROM `formqueue`;";
	protected String table_name = "formqueue";
	protected String[] fields = {"id", "table_id", "global_pk_id", "querystring", "sync_status", "action", "timestamp"};
	
	public FormQueueData() {
		super();
		this.formQueryStringList = new ArrayList();
	}
	
	public FormQueueData(OnlineOfflineCallbacks callbacks) {
		super(callbacks);
		this.formQueryStringList = new ArrayList();
	}

	public FormQueueData.Data initFormQueueAdd(String table_id, String global_pk_id, 
			String queryString, String mode) {
		FormQueueData.Data formQueueData = new FormQueueData.Data(table_id, global_pk_id, queryString);
		formQueueData.setAction(mode);
		formQueueData.setSyncStatus(formQueueData.SYNC_READY);
		return formQueueData;
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
	
	public void addFormQueueData(FormQueueData.Data	formQueueData) {
		this.formQueryStringList.add(formQueueData);
	}
	
	public void save() {
		for(int i=0; i < this.formQueryStringList.size(); i++) {
			((BaseData.Data)this.formQueryStringList.get(i)).save();
		}
	}
	
	public int getUnsyncCount() {
		int totalUnsyncRows = 0;
		FormQueueData formQueueDbApi = new FormQueueData();
		BaseData.dbOpen();
		formQueueDbApi.select(FormQueueData.countUnsyncTableRow);
		if(formQueueDbApi.getResultSet().isValidRow()){
			try {
				totalUnsyncRows = formQueueDbApi.getResultSet().getFieldAsInt(0);
			} catch(DatabaseException e) {
				Window.alert("Database Exception : " + e.toString());
				BaseData.dbClose();
			}
		}
		return totalUnsyncRows;
	}
	
	public Object postPageData() {	
		return false;
	}
}
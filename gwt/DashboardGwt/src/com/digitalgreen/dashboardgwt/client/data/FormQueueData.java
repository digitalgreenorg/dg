package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;

import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;

public class FormQueueData extends BaseData {

	public class Data extends BaseData.Data {
		
		final public static String ACTION_ADD = "A";
		final public static String ACTION_EDIT = "E";
		final public static String ACTION_DELETE = "D";
		
		final public static String SYNC_READY = "0";
		final public static String SYNC_DONE = "1";
		
		private String table_id;
		private String global_pk_id;
		private String queryString;
		private String syncStatus;
		private String action;

		public Data(String table_id, String global_pk_id, String queryString) {
			this.table_id = table_id;
			this.global_pk_id = global_pk_id;
			this.queryString = queryString;
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
			formQueueData.autoInsert(this.table_id,
					this.global_pk_id,
					this.queryString,
					this.syncStatus,
					this.action);
		}	
	}
	
	protected ArrayList formQueryStringList = null;
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `formqueue` " +
										  "(table_id INTEGER NOT NULL, " +
										  "global_pk_id INTEGER NOT NULL PRIMARY KEY, " +
										  "querystring VARCHAR NOT NULL, " +
										  "sync_status BOOLEAN, " +
										  "action CHAR(1)); ";  
	protected static String dropTable = "DROP TABLE IF EXISTS `formqueue`;";
	protected static String getUnsyncTableRow = "SELECT * FROM `formqueue` WHERE sync_status=0 LIMIT 1";
	protected static String updateSyncStatusOfARow = "UPDATE `formqueue` SET sync_status=1 WHERE global_pk_id=?";
	protected String table_name = "formqueue";
	protected String[] fields = {"table_id", "global_pk_id", "querystring", "sync_status", "action"};
	
	
	public FormQueueData() {
		super();
		this.formQueryStringList = new ArrayList();
	}
	
	public FormQueueData(OnlineOfflineCallbacks callbacks) {
		super(callbacks);
		this.formQueryStringList = new ArrayList();	
	}

	public FormQueueData.Data initFormQueueAdd(String table_id, String global_pk_id, 
			String queryString) {
		FormQueueData.Data formQueueData = new FormQueueData.Data(table_id, global_pk_id, queryString);
		formQueueData.setAction(formQueueData.ACTION_ADD);
		formQueueData.setSyncStatus(formQueueData.SYNC_READY);
		return formQueueData;
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
	
	public Object postPageData() {	
		return false;
	}
}
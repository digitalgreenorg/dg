package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;

import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.google.gwt.gears.client.database.DatabaseException;
import com.google.gwt.gears.client.database.ResultSet;
import com.google.gwt.http.client.RequestException;
import com.google.gwt.user.client.Cookies;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.FormPanel;

public class LoginData extends BaseData {
	
	public class Data extends BaseData.Data {
		private int primaryKey;
		private String username;
		private String password;
		
		public Data() {
			super();
		}
		
		public Data(String username, String password, int key) {
			this.username = username;
			this.password = password;
			this.primaryKey = key;
		}
	}

	protected static String tableID = "31";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `user` " +
	  "(last_inserted_id INTEGER PRIMARY KEY NOT NULL, " +
	  "username VARCHAR(100)," +
	  " password VARCHAR(100)," +
	  " app_status CHAR(1)," +
	  " dirty_bit CHAR(1)," +
	  " last_sync_table_index INT);";

	protected static String dropTable = "DROP TABLE IF EXISTS `user`;";
	protected static String insertRow = "INSERT INTO user VALUES (?, ? , ?, ? , ?, ?);";
	protected static String authenticateUser = "SELECT username FROM user WHERE username=? AND password = ?";
	protected static String selectUser = "SELECT username FROM user WHERE username=?";
	protected static String updateUser = "UPDATE `user` SET last_inserted_id=?,app_status=?, dirty_bit=? WHERE username = ? AND password = ?";
	protected static String getSyncStatus = "SELECT dirty_bit, last_sync_table_index FROM `user` WHERE username = ?";
	protected static String updateSyncStatus = "UPDATE `user` SET dirty_bit=?, last_sync_table_index=? where username = ?;";
	protected static String postURL = "/dashboard/login/"; 
	
	public LoginData() {
		super();
	}

	public LoginData(OnlineOfflineCallbacks callbacks) {
		super(callbacks);
	}
	
	@Override
	protected String getTableId(){
		return LoginData.tableID;
	}
	
	@Override
	protected String getCreateTableSql(){
		return this.createTable;
	}
	
	@Override
	protected String getDeleteTableSql(){
		return this.dropTable;
	}

	public void create(){
		this.create(createTable);
	}
	
	public void delete(){
		this.delete(dropTable);
	}
	
	public void update(String primaryKey, String app_status, String dirty_bit, String username, String password ){
		this.update(updateUser,  primaryKey, app_status, dirty_bit, username, password);
	}
	
	public void updateSyncStatus(String dirty_bit, String last_sync_table_index, String username){
		this.update(updateSyncStatus, dirty_bit, last_sync_table_index, username);
	}
	
	public void insert(String primaryKey, String username, String password, String app_status, String dirty_bit, String last_sync_table_index) {
		this.insert(insertRow, primaryKey, username, password, app_status, dirty_bit, last_sync_table_index);
	}
	
	public Object authenticate(String username, String password) {
		if(this.isOnline()){
			String postData = "username=" + username + "&password=" + password;
			this.post(RequestContext.SERVER_HOST + LoginData.postURL, postData);
		} else {
			// Check if DB User row has the same username.
			try {
				LoginData.dbOpen();
				this.select(authenticateUser, username, password);
				ResultSet resultSet = this.getResultSet();
				if(resultSet.isValidRow()) {
					resultSet.close();
					LoginData.dbClose();
					return true;
				}
				else{
					LoginData.dbClose();
				}
			} catch (DatabaseException e) {
				LoginData.dbClose();
				Window.alert("Database Exception : " + e.toString());
			}
		}
		return false;
	}
	
	public ArrayList checkDirtyBitStatusInTheUserTable(String username){
		ArrayList<Integer> resultSet = new ArrayList<Integer>();
		BaseData.dbOpen();
		this.select(LoginData.getSyncStatus , username);
		ResultSet rs = this.getResultSet();
		if(rs.isValidRow()) {
			try {
				resultSet.add(rs.getFieldAsInt(0));
				resultSet.add(rs.getFieldAsInt(1));
			} catch (DatabaseException e) {
				BaseData.dbClose();
				e.printStackTrace();
				return resultSet;
			}
		}
		BaseData.dbClose();
		return resultSet;
	}
	
}
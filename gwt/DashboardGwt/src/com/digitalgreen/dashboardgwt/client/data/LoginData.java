package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;

import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.google.gwt.gears.client.database.DatabaseException;
import com.google.gwt.gears.client.database.ResultSet;
import com.google.gwt.user.client.Window;

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
	  "(last_inserted_id BIGINT UNSIGNED PRIMARY KEY NOT NULL, " +
	  " username VARCHAR(100)," +
	  " password VARCHAR(100)," +
	  " app_status CHAR(1)," +
	  " dirty_bit CHAR(1)," +
	  " last_sync_table_index INT," +
	  " user_role CHAR(1), " +
	  " dashboard_error_count INT);";

	protected static String dropTable = "DROP TABLE IF EXISTS `user`;";
	protected static String insertRow = "INSERT INTO user VALUES (?, ? , ?, ? , ?, ?, ?, ?);";
	protected static String authenticateUser = "SELECT username, user_role FROM user WHERE username=? AND password = ?";
	protected static String selectUser = "SELECT username FROM user WHERE username=?";
	protected static String updateUser = "UPDATE `user` SET last_inserted_id=? WHERE username = ? AND password = ?";
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
	
	public void update(String primaryKey, String username, String password ){
		this.update(updateUser,  primaryKey,  username, password);
	}
	
	public void updateSyncStatus(String dirty_bit, String last_sync_table_index, String username){
		this.update(updateSyncStatus, dirty_bit, last_sync_table_index, username);
	}
	
	public void insert(String primaryKey, String username, String password, String app_status, String dirty_bit, String last_sync_table_index, String user_role, String dashboard_errors) {
		this.insert(insertRow, primaryKey, username, password, app_status, dirty_bit, last_sync_table_index, user_role, dashboard_errors);
	}
	
	public Object authenticate(String username, String password) {
		if(BaseData.isOnline()){
			String postData = "username=" + username + "&password=" + password;
			this.post(RequestContext.SERVER_HOST + LoginData.postURL, postData);
		} else {
			// Check if DB User row has the same username.
			try {
				LoginData.dbOpen();
				this.select(authenticateUser, username, password);
				ResultSet resultSet = this.getResultSet();
				if(resultSet.isValidRow()) {
					String role = new String();
					role = resultSet.getFieldAsString(1);
					resultSet.close();
					LoginData.dbClose();
					return role;
				}
				else{
					LoginData.dbClose();
				}
			} catch (DatabaseException e) {
				LoginData.dbClose();
				Window.alert("Database Exception : " + e.toString());
			}
		}
		return "false";
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
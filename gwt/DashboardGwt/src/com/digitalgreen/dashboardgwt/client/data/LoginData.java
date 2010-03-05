package com.digitalgreen.dashboardgwt.client.data;

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
		}
		
		public Data(String username, String password, int key) {
			this.username = username;
			this.password = password;
			this.primaryKey = key;
		}
	}

	protected static String createTable = "CREATE TABLE IF NOT EXISTS `user` " +
	  "(last_inserted_id INTEGER PRIMARY KEY NOT NULL, " +
	  "username VARCHAR(100)," +
	  " password VARCHAR(100)," +
	  " app_status CHAR(1)," +
	  " dirty_bit CHAR(1));";

	protected static String deleteTable = "DROP TABLE IF EXISTS `user`;";
	
	protected static String insertRow = "INSERT INTO user VALUES (?, ? , ?, ? , ?);";
	
	protected static String selectUser = "SELECT username FROM user WHERE username=? AND password = ?";

	protected static String postURL = "/dashboard/login/"; 
	
	public LoginData() {
		super();
		this.data = new Data();
	}

	public LoginData(OnlineOfflineCallbacks callbacks) {
		super(callbacks);
	}

	public void create(){
		this.create(createTable);
	}
	
	public void delete(){
		this.delete(deleteTable);
	}
	
	public void insert(String primaryKey, String username, String password, String app_status, String dirty_bit) {
		this.insert(insertRow, primaryKey, username, password, app_status, dirty_bit);
	}
	
	public Object authenticate(String username, String password) {

		if(this.isOnline()){
			String postData = "username=" + username + "&password=" + password;
			this.post(RequestContext.SERVER_HOST + "postURL", postData);
			//String postData = "username=" + username + "&password=" + password;
			//this.post("http://127.0.0.1:8000/dashboard/login/", postData);
		} else {
			// Check if DB User row has the same username.
			try {
				this.dbOpen();
				this.select(selectUser, username, password);
				ResultSet resultSet = this.getResultSet();
				if(resultSet.isValidRow() && resultSet.getFieldAsString(0) == username) {
					resultSet.close();
					this.dbClose();
					return true;
				}
			} catch (DatabaseException e) {
				this.dbClose();
				Window.alert("Database Exception : " + e.toString());
				
			}
		}
		return false;
	}
	
	
}
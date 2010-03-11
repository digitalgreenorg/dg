package com.digitalgreen.dashboardgwt.client.data;

import com.digitalgreen.dashboardgwt.client.DashboardGwt;
import com.digitalgreen.dashboardgwt.client.common.ApplicationConstants;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.google.gwt.gears.client.Factory;
import com.google.gwt.gears.client.database.Database;
import com.google.gwt.gears.client.database.DatabaseException;
import com.google.gwt.gears.client.database.ResultSet;
import com.google.gwt.http.client.Request;
import com.google.gwt.http.client.RequestBuilder;
import com.google.gwt.http.client.RequestCallback;
import com.google.gwt.http.client.RequestException;
import com.google.gwt.http.client.Response;
import com.google.gwt.http.client.URL;
import com.google.gwt.user.client.Window;


public class BaseData implements OfflineDataInterface, OnlineDataInterface {
	private static Database db;
	private static String databaseName = ApplicationConstants.getDatabaseName();

	private String responseText = null;
	private int requestError = 0;
	protected BaseData.Data data;
	protected ResultSet lastResultSet;
	
	final static public int ERROR_RESPONSE = 1;
	final static public int ERROR_SERVER = 2;
	
	protected static String getLastInsertedID = "SELECT last_inserted_id FROM `user` WHERE username= ?;";
	protected static String updateLastInsertedID = "UPDATE `user` SET last_inserted_id = ? WHERE username = ?;";
	protected static String getApplicationStatus = "SELECT `app_status` FROM `user`;";
	protected static String updateApplicationStatus = "UPDATE `user` SET app_status=? WHERE username = ?;";
	protected static String userTableExists = "SELECT * FROM sqlite_master where type='table' and name = 'user';";
	
	protected OnlineOfflineCallbacks dataOnlineCallbacks;

	public class Data {
		public Data() {}
	}

	public BaseData() {}

	public BaseData(OnlineOfflineCallbacks callbacks) {
		this.dataOnlineCallbacks = callbacks;
	}
	
	public BaseData.Data getData() {
		return this.data;
	}
	
	protected static Database getDb() {
		return BaseData.db;
	}
	
	protected static boolean isOnline() {
		return ApplicationConstants.getCurrentOnlineStatus();
	}
	
	protected boolean isRequestError() {
		return this.requestError == BaseData.ERROR_RESPONSE || this.requestError == BaseData.ERROR_SERVER;
	}
	
	private void setResponseText(String responseText) {
		this.responseText = responseText;
	}

	private void setRequestError(int errorCode) {
		this.requestError = errorCode;
	}
	
	private void request(RequestBuilder.Method method, String url, String postData) {
		RequestBuilder builder = new RequestBuilder(method, URL.encode(url));
		try {
			if(method == RequestBuilder.POST) {
				builder.setHeader("Content-Type", "application/x-www-form-urlencoded");
			}
			Request request = builder.sendRequest(postData, new RequestCallback() {
			public void onResponseReceived(Request request, Response response) {
				if(response.getStatusCode() == 200) {
					dataOnlineCallbacks.onlineSuccessCallback(response.getText());
				}
			}
			public void onError(Request request, Throwable exception) {
				setRequestError(BaseData.ERROR_RESPONSE);
				dataOnlineCallbacks.onlineErrorCallback(BaseData.ERROR_RESPONSE);
			}		           
		});
		} catch (RequestException e) {
			// Couldn't connect to server
			setRequestError(BaseData.ERROR_SERVER);
			dataOnlineCallbacks.onlineErrorCallback(BaseData.ERROR_SERVER);
		}
	}
	
	public void get(String url) {
		this.request(RequestBuilder.GET, url, null);
	}
	
	public void post(String url, String postData) {
		this.request(RequestBuilder.POST, url, postData);
	}
	
	public static Boolean dbOpen() {
		try{
			BaseData.db = Factory.getInstance().createDatabase();
			db.open(BaseData.databaseName);
			return true;
		}catch (Exception e){
			return false;
		}
	}
	
	public static void dbClose() {
		try {
			BaseData.db.close();
		} catch (DatabaseException e) {
			Window.alert("Database close error: " + e.toString());
		}
	}

	public static void dbStartTransaction() throws DatabaseException {
		db.execute("BEGIN TRANSACTION;");
	}
	
	public static void dbCommit() throws DatabaseException {
		db.execute("COMMIT;");	
	}
	
	public void create(String createSql, String ...args){
		BaseData.dbOpen();
		this.execute(createSql, args);
		BaseData.dbClose();
	}
	
	public void delete(String deleteSql, String ...args) {
		BaseData.dbOpen();
		try {
			BaseData.dbStartTransaction();
			this.execute(deleteSql, args);
			BaseData.dbCommit();
			BaseData.dbClose();
		} catch (DatabaseException e) {
			// TODO Auto-generated catch block
			Window.alert("Database error: " + e.toString());
			BaseData.dbClose();
		}
	}

	public void insert(String insertSql, String ...args) {
		try {
			BaseData.dbOpen();
			BaseData.dbStartTransaction();
			this.execute(insertSql, args);
			BaseData.dbCommit();
			BaseData.dbClose();
		} catch (DatabaseException e) {
			Window.alert("Database error: " + e.toString());
			BaseData.dbClose();
		}
		
	}
	
	public void update(String updateSql, String ...args) {
		BaseData.dbOpen();
		try {
			BaseData.dbStartTransaction();
			this.execute(updateSql, args);
			BaseData.dbCommit();
			BaseData.dbClose();
		} catch (DatabaseException e) {
			// TODO Auto-generated catch block
			Window.alert("Database error: " + e.toString());
			BaseData.dbClose();
		}
	}

	/* Cannot close the database after a select statement. 
	 * Closing the database will delete the Result Set */
	public void select(String selectSql, String ...args) {
		this.execute(selectSql, args);
	}
	
	public String getNextRowId(){
		try {
			int id;
			BaseData.dbOpen();
			this.select(getLastInsertedID, ApplicationConstants.getUsernameCookie());
			if (this.getResultSet().isValidRow()){
				id = this.getResultSet().getFieldAsInt(0);
				id++;
				BaseData.dbClose();
				return id+"";
			} 
		}catch (DatabaseException e) {
				Window.alert("Database exception error : " +  e.toString());
				BaseData.dbClose();
		}
		return "error";
	}
	
	
	public void updateLastInsertedID(){
			String id = this.getNextRowId();
			this.update(updateLastInsertedID, id, ApplicationConstants.getUsernameCookie());
	}
	
	public boolean checkIfUserTableExists(){
		BaseData.dbOpen();
		this.select(userTableExists);
		if (this.getResultSet().isValidRow()){
			BaseData.dbClose();
			return true;
		}
		else{
			BaseData.dbClose();
			return false;
		}	
	}
	
	public int getApplicationStatus(){
		try{
			BaseData.dbOpen();
			this.select(getApplicationStatus);
			if (this.getResultSet().isValidRow()){
				int status = this.getResultSet().getFieldAsInt(0);
				return status;
			}
		} catch (DatabaseException e) {
			Window.alert("Database exception error : " +  e.toString());
		}finally {
			BaseData.dbClose();	
		}
		return -1;
	}
	

	public void updateAppStatus(String app_status, String username){
		this.update(updateApplicationStatus, app_status,username );
	}
	
	protected ResultSet getResultSet() {
		//if(this.lastResultSet != null && this.lastResultSet.isValidRow())
		return this.lastResultSet;
		//return null;
	}
	
	public void execute(String sql, String ...args) {
		this.lastResultSet = null;
		try {
			//BaseData.dbOpen();
			this.lastResultSet = BaseData.db.execute(sql, args);
			
		} catch (DatabaseException e) {
			Window.alert("Database execute error:" + e.toString());
		} /*finally {
			BaseData.dbClose();
			// Closing the database making the value of lastResultSet as null
		}*/
	}
	
	// Basically a wrapper around a core data function to execute
	// the offline callback.  The online callbacks get executed in request().
	public void apply(Object methodResponse) {
		if(!this.isOnline()) {
			this.dataOnlineCallbacks.offlineSuccessCallback(methodResponse);
		}
		//this.dataOnlineCallbacks.onlineSuccessCallback("1");
	}
}
package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.ApplicationConstants;
import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.data.RegionsData.Data;
import com.digitalgreen.dashboardgwt.client.data.RegionsData.Type;
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
import com.google.gwt.core.client.JavaScriptObject;
import com.google.gwt.core.client.JsArray;


public class BaseData implements OfflineDataInterface, OnlineDataInterface {
	
	public static class Type extends JavaScriptObject {
		protected Type() {}
		public final native String getPk() /*-{ return this.pk; }-*/; 
		public final native String getModel() /*-{ return this.model; }-*/;
		public final native Object getFields() /*-{ return this.fields ; }-*/;
	}
	
	public class Data implements Cloneable {
		
		protected String id = null;
		
		public Data() {}
		
		// Override this
		public BaseData.Data clone() {
			return null;
		}
		
		// Override this
		public String getPrefixName() {
			return null;
		}
		// Override this
		public void setObjValueFromString(String key, String val) {
			//Window.alert("The incoming key= " + key);
		}

		// Override this
		public void save() {}

		// Override this
		public void save(BaseData.Data withForeignKey) {}
		
		public String getId() {
			return this.id;
		}
	}
	
	private static Database db = null;
	private static String databaseName = ApplicationConstants.getDatabaseName();

	private int requestError = 0;
	
	protected Form form = null;
	protected String queryString = null;
	protected ResultSet lastResultSet;
	protected String table_name = "";
	protected String[] fields = {};
	
	final static public int ERROR_RESPONSE = 1;
	final static public int ERROR_SERVER = 2;
	
	protected static String getLastInsertedID = "SELECT last_inserted_id FROM `user` WHERE username= ?;";
	protected static String updateLastInsertedID = "UPDATE `user` SET last_inserted_id = ? WHERE username = ?;";
	protected static String getApplicationStatus = "SELECT `app_status` FROM `user`;";
	protected static String updateApplicationStatus = "UPDATE `user` SET app_status=? WHERE username = ?;";
	protected static String userTableExists = "SELECT * FROM sqlite_master where type='table' and name = 'user';";
	
	protected OnlineOfflineCallbacks dataOnlineCallbacks;

	public BaseData() {}

	public BaseData(OnlineOfflineCallbacks callbacks) {
		this.dataOnlineCallbacks = callbacks;
	}
	
	public BaseData(OnlineOfflineCallbacks callbacks, Form form, String queryString) {
		this.dataOnlineCallbacks = callbacks;
		this.form = form;
		this.queryString = queryString;
	}
	
	// Override this
	public Data getNewData() {
		return new Data();
	}
	
	// Override this
	protected String getTableId() {
		return "";
	}
	
	// Override this
	protected String getTableName() {
		return this.table_name;
	}
	
	// Override this
	protected String[] getFields() {
		return this.fields;
	}
	
	protected void save() {
		BaseData.dbOpen();
		try {
			BaseData.dbStartTransaction();
			this.form.save(this.queryString);
			FormQueueData formQueue = new FormQueueData();			 
			formQueue.saveQueryString(this.getTableId(), String.valueOf(this.form.getParent().getId()), this.queryString, "0", "A");
			BaseData.dbCommit();
		} catch (Exception e) {
			e.printStackTrace();
		}
		BaseData.dbClose();
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
	
	public void post(String url) {
		this.request(RequestBuilder.POST, url, null);
	}
	
	public static boolean dbOpen() {
		try{
			if(BaseData.db == null) {
				BaseData.db = Factory.getInstance().createDatabase();
				db.open(BaseData.databaseName);
			}
			return true;
		}catch (Exception e){
			return false;
		}
	}
	
	public static void dbClose() {
		try {
			if(BaseData.db != null) {
				BaseData.db.close();
			}
			BaseData.db = null;
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
		this.execute(deleteSql, args);
		BaseData.dbClose();
	}

	public void insert(String insertSql, String ...args) {
		BaseData.dbOpen();
		this.execute(insertSql, args);
		BaseData.dbClose();
	}

	public String autoInsert(String ...args) {
		String insertSql = "INSERT INTO " + this.getTableName() + " VALUES (";
		for(int i=0; i < this.getFields().length; i++) {
			if(i == this.getFields().length - 1) {
				insertSql += "?";
			} else {
				insertSql += "?, ";
			}
		}
		insertSql += ");";
		
		ArrayList tempList = new ArrayList();
		for(int i=0; i < args.length; i++) {
			tempList.add(args[i]);
		}
		String[] tempListString = new String[] {};
		if(this.getFields().length == args.length){
			for(int i=0; i < tempList.size(); i++) {
				tempListString[i] = (String)tempList.get(i);
			}
			this.insert(insertSql, tempListString);
			return args[0];
		} else{
			String newId = this.getNextRowId();
			if(!newId.equals("ERROR")) {
				tempList.add(0, newId);
				for(int i=0; i < tempList.size(); i++) {
					tempListString[i] = (String)tempList.get(i);
				}
				this.insert(insertSql, tempListString);
				this.updateLastInsertedID(newId);
				return newId;
			}
		}
		return "-1";
	}
	
	public void update(String updateSql, String ...args) {
		BaseData.dbOpen();
		this.execute(updateSql, args);
		BaseData.dbClose();
	}

	/* Cannot close the database after a select statement. 
	 * Closing the database will delete the Result Set */
	public void select(String selectSql, String ...args) {
		this.execute(selectSql, args);
	}
	
	public String getNextRowId(){
		try {
			BaseData.dbOpen();
			this.select(getLastInsertedID, ApplicationConstants.getUsernameCookie());
			if (this.getResultSet().isValidRow()){
				int id = this.getResultSet().getFieldAsInt(0);
				BaseData.dbClose();
				return (new Integer(++id)).toString();
			} 
		} catch (DatabaseException e) {
				Window.alert("Database exception error : " +  e.toString());
				BaseData.dbClose();
		}
		return "ERROR";
	}
		
	public void updateLastInsertedID() {
			String id = this.getNextRowId();
			this.update(updateLastInsertedID, id, ApplicationConstants.getUsernameCookie());
	}
	
	// To avoid another select to get the global id
	public void updateLastInsertedID(String id) {
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
		return this.lastResultSet;
	}
	
	public void execute(String sql, String ...args) {
		this.lastResultSet = null;
		try {
			this.lastResultSet = BaseData.db.execute(sql, args);	
		} catch (DatabaseException e) {
			Window.alert("Database execute error:" + e.toString());
		}
	}
	
	//Override this
	public List getListingOnline(String json){
		return null;		
	}
	
	//Override this
	public  String getListingOnlineURL(){
		return null;
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
package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Date;

import com.digitalgreen.dashboardgwt.client.common.ApplicationConstants;
import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.data.BlocksData.Data;
import com.digitalgreen.dashboardgwt.client.data.validation.BaseValidator;
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


public class BaseData implements OfflineDataInterface, OnlineDataInterface {
	
	public static class Type extends JavaScriptObject {
		protected Type() {}
		public final native String getPk() /*-{ return $wnd.checkForNullValues(this.pk); }-*/; 
		public final native String getModel() /*-{ return $wnd.checkForNullValues(this.model); }-*/;
		public final native Object getFields() /*-{ return this.fields ; }-*/;
	}
	
	public class Data implements Cloneable {
		protected String id = null;
		protected String queryString = null;
		protected HashMap manyToManyRelationshipMap = null;
		protected boolean hasManyToManyRelationships = false;
		protected boolean isManyToManyDependent = false;
		protected ArrayList errorStack = null;
		protected String mode = null;
		
		public Data() {
			this.manyToManyRelationshipMap = new HashMap();
			this.errorStack = new ArrayList();
			this.mode = FormQueueData.Data.ACTION_ADD;
		}
		
		// Override this
		public BaseData.Data clone() {
			return null;
		}
		
		// Override this
		public String getPrefixName() {
			return null;
		}
		
		public String getMode() {
			return this.mode;
		}
		
		public void setMode(String mode) {
			this.mode = mode;
		}
		
		public void setAsManyToManyDependent() {
			this.isManyToManyDependent = true;
		}
		
		public boolean isManyToManyDependent() {
			return this.isManyToManyDependent;
		}
		
		// Override this
		public void setObjValueFromString(String key, String val) {}

		// Override this
		public void save() {}

		// Override this
		public void save(BaseData.Data withForeignKey) {}
		
		// Override this
		public String toQueryString(String id) {
			return "";
		}
		
		// Override this
		public String toInlineQueryString(String id) {
			return "";
		}
		
		private String rowToQueryStringForManyToMany(String id) {
			String queryString = "";
			if(!this.hasManyToManyRelationships) {
				return "";
			}
			
			Object []keys = (Object[])this.manyToManyRelationshipMap.keySet().toArray();
			for(int i=0; i < keys.length; i++) {
				String queryStringPart = "";
				ManyToManyRelationship manyToManyRelationship = (ManyToManyRelationship)this.manyToManyRelationshipMap.get(keys[i]);
				BaseData dbApi = new BaseData();
				String query = "SELECT * FROM " + manyToManyRelationship.getToTable().getTableName() + " WHERE " +
					this.getPrefixName() + "_id=" + id;
				BaseData.dbOpen();
				dbApi.select(query);
				if (dbApi.getResultSet().isValidRow()) {
					for (int j=0; dbApi.getResultSet().isValidRow(); ++j, dbApi.getResultSet().next()) {
						try {
							queryStringPart += manyToManyRelationship.getAttributeCollectionName() + "=" + 
								dbApi.getResultSet().getFieldAsString(2) + "&";
						} catch (DatabaseException e) {
							e.printStackTrace();
						}
					}
					if(queryStringPart.endsWith("&")) {
						queryStringPart = queryStringPart.substring(0, queryStringPart.length() - 1);
					}
				}
				queryString += queryStringPart;
				if(i != keys.length - 1 && !queryString.endsWith("&")) {
					queryString += "&";
				}
			}
			BaseData.dbClose();
			return queryString;
		}
		
		protected String rowToQueryString(String tableName, String []fields,
				String predicateLValue, String predicateRValue, String prefix) {
			String queryString = "";
			BaseData dbApi = new BaseData();
			String query = "SELECT * FROM " + tableName + " WHERE " + predicateLValue + "=" +
				predicateRValue + ";";
			BaseData.dbOpen();
			dbApi.select(query);
			if (dbApi.getResultSet().isValidRow()) {
				for (int i=0; dbApi.getResultSet().isValidRow(); ++i, dbApi.getResultSet().next()) {
					String queryStringPart = "";
					for(int j=0; j < fields.length; j++) {
						try {
							String value = dbApi.getResultSet().getFieldAsString(j);
							String name = fields[j];
							if(fields[j].endsWith("_id")) {
								name = fields[j].substring(0, fields[j].length() - 3);
							}
							if(!prefix.equals("")) {
								name = prefix.endsWith("_set") ? prefix + "-" + i + "-" + name :
									prefix + "-" + name;
							}
							queryStringPart += value != null ? name + "=" + value : name + "=";
							if(fields.length != j-1) {
								queryStringPart += "&";
							}
						} catch (DatabaseException e) {
							e.printStackTrace();
						}
					}
					queryString += queryStringPart + "&";
				}
			}
			// dirty
			if(queryString.endsWith("&")) {
				queryString = queryString.substring(0, queryString.length() - 1 - 1);
			}
			BaseData.dbClose();
			return queryString + "&" + this.rowToQueryStringForManyToMany(predicateRValue);
		}
		
		public String getId() {
			return this.id;
		}
		
		public void addManyToManyRelationship(String fieldName,
				BaseData toTableBaseData,
				String attributeCollectionName) {
			ManyToManyRelationship manyToManyRelationship = new ManyToManyRelationship(fieldName,
					toTableBaseData, attributeCollectionName);
			this.manyToManyRelationshipMap.put((String)attributeCollectionName, manyToManyRelationship);
			this.hasManyToManyRelationships = true;
		}
		
		public HashMap getManyToManyRelationships() {
			return this.manyToManyRelationshipMap;
		}
		
		public boolean hasManyToManyRelationships() {
			return this.hasManyToManyRelationships;
		}
		
		public void deleteManyToManyDependents(String id) {
			if(!this.hasManyToManyRelationships) {
				return;
			}
			Object []keys = (Object[])this.manyToManyRelationshipMap.keySet().toArray();
			for(int i=0; i < keys.length; i++) {
				ManyToManyRelationship manyToManyRelationship = (ManyToManyRelationship)this.manyToManyRelationshipMap.get(keys[i]);
				BaseData dbApi = new BaseData();
				String dml = "DELETE FROM " + manyToManyRelationship.getToTable().getTableName() + " WHERE " +
					this.getPrefixName() + "_id=" + id +";";
				dbApi.delete(dml);
			}
		}
		
		public void addNameValueToQueryString(String name, String value) {
			String nameValuePair = name + "=" + value;
			if(this.queryString == null) {
				this.queryString = nameValuePair;
			} else {
				this.queryString += "&" + nameValuePair;
			}
		}
		
		public String getQueryString() {
			return this.queryString;
		}
		
		// Override this
		public String getTableId() {
			return "";
		}
		
		// Override this
		public boolean validate() {
			return true;
		}
		
		// Override this
		public boolean validate(BaseData.Data foreignKey) {
			return true;
		}
		
		protected boolean executeValidators(ArrayList validators) {
			boolean isValid = true;
			for(int i=0; i < validators.size(); i++) {
				if(!((BaseValidator)validators.get(i)).validate()) {
					errorStack.add(((BaseValidator)validators.get(i)).getError());
					isValid = false;
				}
			}
			return isValid;
		}
		
		public ArrayList getErrorStack() {
			return this.errorStack;
		}
	}
	
	public class ManyToManyRelationship {
		
		private String field;
		private BaseData toTable;
		private String attributeCollectionName;
	
		public ManyToManyRelationship(String field, BaseData toTable,
				String attributeCollectionName) {
			this.field = field;
			this.toTable = toTable;
			this.attributeCollectionName = attributeCollectionName;
		}
		
		public String getAttributeCollectionName() {
			return this.attributeCollectionName;
		}
		
		public BaseData getToTable() {
			return this.toTable;
		}
		
		public String getField() {
			return this.field;
		}
	}
	
	private static Database db = null;
	private static String databaseName = ApplicationConstants.getDatabaseName();
	
	protected Form form = null;
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
	protected static String createTable = "";
	protected static String dropTable = "";
	
	protected OnlineOfflineCallbacks dataOnlineCallbacks;

	public BaseData() {}

	public BaseData(OnlineOfflineCallbacks callbacks) {
		this.dataOnlineCallbacks = callbacks;
	}
	
	public BaseData(OnlineOfflineCallbacks callbacks, Form form) {
		this.dataOnlineCallbacks = callbacks;
		this.form = form;
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
	public String getTableName() {
		return this.table_name;
	}
	
	// Override this
	protected String[] getFields() {
		return this.fields;
	}
	
	//Override this
	protected String getCreateTableSql(){
		return this.createTable;
	}
	
	//Override this
	protected String getDeleteTableSql(){
		return this.dropTable;
	}
	
	protected boolean validate() {
		return this.form.validate();
	}
	
	protected void save() {
		try {
			BaseData.dbStartTransaction();
			this.form.save();
			this.form.getFormQueue().save();
			BaseData.dbCommit();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	protected static Database getDb() {
		return BaseData.db;
	}
	
	protected static boolean isOnline() {
		return ApplicationConstants.getCurrentOnlineStatus();
	}
	
	private void request(RequestBuilder.Method method, String url, String postData) {
		RequestBuilder builder = new RequestBuilder(method, URL.encode(url));
		try {
			if(method == RequestBuilder.POST) {
				builder.setHeader("Content-Type", "application/x-www-form-urlencoded");
			}
			Request request = builder.sendRequest(postData, new RequestCallback() {
			public void onResponseReceived(Request request, Response response) {
				if(response.getStatusCode() == 200 || response.getStatusCode() == 201) {
					dataOnlineCallbacks.setStatusCode(response.getStatusCode());
					dataOnlineCallbacks.onlineSuccessCallback(response.getText());
				}
			}
			public void onError(Request request, Throwable exception) {
				dataOnlineCallbacks.onlineErrorCallback(BaseData.ERROR_RESPONSE);
			}		           
		});
		} catch (RequestException e) {
			// Couldn't connect to server
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
				BaseData.db = null;
			}
		} catch (DatabaseException e) {
			Window.alert("Database close error: " + e.toString());
		}
	}
	
	public static boolean dbDelete(){
		try{
			if(BaseData.db != null) {
				BaseData.db.remove();
			}
			BaseData.db = null;
			return true;
		}catch (Exception e){
			Window.alert("exception here");
			return false;
		}
	}

	public static void dbStartTransaction() throws DatabaseException {
		BaseData.dbOpen();
		db.execute("BEGIN TRANSACTION;");
		BaseData.dbClose();
	}
	
	public static void dbCommit() throws DatabaseException {
		BaseData.dbOpen();
		db.execute("COMMIT;");
		BaseData.dbClose();
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
		for(int i=0; i < this.getFields().length; i++) {
			if(i == 0 && args[i] == null) {
				continue;
			}
			tempList.add(args[i]);
		}
		
		String[] tempListString = new String[] {};
		// This client passed in a value for id
		if(args[0] != null || !this.getFields()[0].equals("id")){
			for(int i=0; i < tempList.size(); i++) {
				tempListString[i] = tempList.get(i) == null ? (String)tempList.get(i) : "" + tempList.get(i);
			}
			try {
				BaseData.dbOpen();
				this.lastResultSet = BaseData.db.execute(insertSql, tempListString);
				BaseData.dbClose();
			// Assuming duplicate exception (yuck), but no other way to tell.
			} catch (DatabaseException e) {
				BaseData.dbClose();
				String updateSql = "UPDATE " + this.getTableName() + " SET ";
				String[] fields = this.getFields();
				for(int i= 0; i < fields.length; i++) {
					if(i == fields.length - 1) {
						updateSql += fields[i] + "=?";
					} else {
						updateSql += fields[i] + "=?, ";
					}
				}
				updateSql += " WHERE " + this.getFields()[0] + "=" + args[0] + ";";
				this.update(updateSql, tempListString);
			}
			return args[0];
		}
		// Get an autoincremented id
		else{
			String newId = this.getNextRowId();
			if(!newId.equals("ERROR")) {
				tempList.add(0, newId);
				for(int i=0; i < tempList.size(); i++) {
					if(tempList.get(i) == null) 
						tempListString[i] = (String)tempList.get(i);
					else
						tempListString[i] = "" + tempList.get(i);
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
	
	public ResultSet getResultSet() {
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
	
	// Override this
	public String getSaveOfflineURL(){
		return null;
	}
	
	// Override this
	public String getSaveOnlineURL(){
		return null;
	}

	
	public static String getCurrentDateAndTime(){
		Date date = new Date();
		return date.getYear() + 1900 + "-" + date.getMonth() +"-" + date.getDate() + " " + date.getHours() + ":" + date.getMinutes() + ":" + date.getSeconds();
	}

	// Basically a wrapper around a core data function to execute
	// the offline callback.  The online callbacks get executed in request().
	public void apply(Object methodResponse) {
		if(!this.isOnline()) {
			this.dataOnlineCallbacks.offlineSuccessCallback(methodResponse);
		}
	}

}
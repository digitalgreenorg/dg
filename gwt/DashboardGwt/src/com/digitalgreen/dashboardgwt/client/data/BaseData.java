package com.digitalgreen.dashboardgwt.client.data;

import com.digitalgreen.dashboardgwt.client.DashboardGwt;
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
	private static String databaseName = DashboardGwt.getDatabaseName();

	private String responseText = null;
	private int requestError = 0;
	protected BaseData.Data data;
	protected ResultSet lastResultSet;
	
	final static private int ERROR_RESPONSE = 1;
	final static private int ERROR_SERVER = 2;

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
		return DashboardGwt.getCurrentOnlineStatus();
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
				Window.alert("HEY RESPONSE = " + response.getStatusCode() + " AND text = " + response.getText());
				if (response.getStatusCode() == 200) {
					Window.alert("COMING IN SUCCESS?");
					dataOnlineCallbacks.onlineSuccessCallback(response.getText());
				}
			}
			public void onError(Request request, Throwable exception) {
				Window.alert("COMING INTO ERROR?");
				setRequestError(BaseData.ERROR_RESPONSE);
				dataOnlineCallbacks.onlineErrorCallback();
			}		           
		});
		} catch (RequestException e) {
			// Couldn't connect to server
			Window.alert("GOT A MASSIVE SERVER ERROR");
			setRequestError(BaseData.ERROR_SERVER);
		}
	}
	
	public void get(String url) {
		this.request(RequestBuilder.GET, url, null);
	}
	
	public void post(String url, String postData) {
		this.request(RequestBuilder.POST, url, postData);
	}
	
	public static void dbOpen() {
		BaseData.db = Factory.getInstance().createDatabase();
        db.open(BaseData.databaseName);
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
	
	public void delete(String deleteSql, String ...args) {
		this.execute(deleteSql, args);	
	}

	public void insert(String insertSql, String ...args) {
		this.execute(insertSql, args);
	}

	public void select(String selectSql, String ...args) {
		this.execute(selectSql, args);
	}

	public void update(String updateSql, String ...args) {
		this.execute(updateSql, args);
	}

	public int getLastInsertRowId() {
		return BaseData.db.getLastInsertRowId();
	}
	
	protected ResultSet getResultSet() {
		if(this.lastResultSet != null && this.lastResultSet.isValidRow())
			return this.lastResultSet;
		return null;
	}
	
	public void execute(String sql, String ...args) {
		this.lastResultSet = null;
		try {
			BaseData.dbOpen();
			this.lastResultSet = BaseData.db.execute(sql, args);
		} catch (DatabaseException e) {
			Window.alert("Database execute error: " + e.toString());
		} finally {
			BaseData.dbClose();
		}
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
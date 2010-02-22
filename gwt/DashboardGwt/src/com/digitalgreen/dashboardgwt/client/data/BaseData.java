package com.digitalgreen.dashboardgwt.client.data;

import com.digitalgreen.dashboardgwt.client.DashboardGwt;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
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
import com.google.gwt.user.client.ui.FormPanel;

public class BaseData implements OfflineDataInterface, OnlineDataInterface {
	private static Database db;
	private static String databaseName = DashboardGwt.getDatabaseName();

	private ResultSet lastResultSet;
	private String responseText = null;
	private int requestError = 0;
	
	final static private int ERROR_RESPONSE = 1;
	final static private int ERROR_SERVER = 2;

	public class Data {}
	
	protected boolean isOnline() {
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
	
	private void request(RequestBuilder.Method method, String url) {
		RequestBuilder builder = new RequestBuilder(method, URL.encode(url));
		try {
			Request request = builder.sendRequest(null, new RequestCallback() {
			public void onResponseReceived(Request request, Response response) {
				if (response.getStatusCode() == 200) {
					setResponseText(response.getText());
				}
			}
			public void onError(Request request, Throwable exception) {
				setRequestError(BaseData.ERROR_RESPONSE);
			}		           
		});
		} catch (RequestException e) {
			// Couldn't connect to server
			setRequestError(BaseData.ERROR_SERVER);
		}
	}
	
	public void get(String url) {
		this.request(RequestBuilder.GET, url);
	}
	
	public void post(String url) {
		this.request(RequestBuilder.GET, url);
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

	public void dbStartTransaction() {
		this.execute("BEGIN TRANSACTION;");
	}
	
	public void dbCommit() {
		this.execute("COMMIT;");	
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
	
	private void execute(String sql, String ...args) {
		this.lastResultSet = null;
		try {
			this.lastResultSet = BaseData.db.execute(sql, args);
		} catch (DatabaseException e) {
			Window.alert("Database execute error: " + e.toString());
		}
	}
}
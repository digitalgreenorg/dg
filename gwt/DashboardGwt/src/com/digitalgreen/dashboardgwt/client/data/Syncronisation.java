package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.ApplicationConstants;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.servlets.BaseServlet;
import com.digitalgreen.dashboardgwt.client.servlets.Index;
import com.google.gwt.gears.client.database.DatabaseException;
import com.google.gwt.user.client.Window;
import com.digitalgreen.dashboardgwt.client.common.events.EventBus;
import com.digitalgreen.dashboardgwt.client.common.events.ProgressEvent;

public class Syncronisation {
	
	public Syncronisation() {	
	}
	
	private FormQueueData formQueue;
	private int totalRowsToSync = 0;
	private LoginData loginData;
	private int lastSyncedId;
	private int currentIndex = 0;
	private String setGlobalKeyURL = "/dashboard/setkey/";
	private BaseServlet servlet;
	private int offset = 0;
	
	public void syncFromLocalToMain(BaseServlet servlet) {
		this.servlet = servlet;
		formQueue = new FormQueueData(new OnlineOfflineCallbacks(servlet) {
			public void onlineSuccessCallback(String results) {
				if(results.equals("1")) {
					currentIndex++;
					EventBus.get().fireEvent(new ProgressEvent((int)(((float)currentIndex / totalRowsToSync) * 100)));
					updateSyncStatusOfLastSyncedRowInFormQueueTable();
					if(!postRowOfFormQueueTable()) {
						updateGlobalPkIDOnMainServer();
					}
				} else if(results.equals("0")) {
					RequestContext requestContext = new RequestContext();
					requestContext.setErrorMessage("Validation Error.  Please contact support.");
					getServlet().redirectTo(new Index(requestContext));
				} else if(results.equals("synced")) {
					setGlobalIDInLocalUserTable();
				} else{
					Window.alert("Unkown Error.  Please contact support.");
				}
			}

			public void onlineErrorCallback(int errorCode) {
				RequestContext requestContext = new RequestContext();
				if (errorCode == BaseData.ERROR_RESPONSE) {
					requestContext.setErrorMessage("You may be experiencing server/bandwidth problems.  Please try again, or contact support.");
				} else if (errorCode == BaseData.ERROR_SERVER) {
					requestContext.setErrorMessage("Problem in the connection with the server.");
				} else {
					requestContext.setErrorMessage("Unknown error.  Please contact support.");
				}
				getServlet().redirectTo(new Index(requestContext));	
			}
		});
		
		this.totalRowsToSync = formQueue.getUnsyncCount();
		if(!postRowOfFormQueueTable()){
			RequestContext requestContext = new RequestContext();
			requestContext.setMessage("Local database is in sync with the main server ");
			servlet.redirectTo(new Index(requestContext));
		}
	}
	
	public void syncFromMainToLocal(BaseServlet servlet){
		loginData = new LoginData();
		IndexData indexData = new IndexData(new OnlineOfflineCallbacks(servlet) {
			public void onlineSuccessCallback(String results) {
				if(!results.equals("0")) {
					LoginData user = new LoginData();
					user.insert(results, ApplicationConstants.getUsernameCookie(), ApplicationConstants.getPasswordCookie(), "1", "1", "0");
					formQueue.get(RequestContext.SERVER_HOST + ((BaseData)ApplicationConstants.mappingBetweenTableIDAndDataObject.get(ApplicationConstants.tableIDs[currentIndex])).getListingOnlineURL()+ offset+ "/" + ApplicationConstants.PAGESIZE + "/");
				} else {
					RequestContext requestContext = new RequestContext();
					requestContext.setErrorMessage("You do not have a valid account.  Please contact support. ");
					getServlet().redirectTo(new Index(requestContext));				
				}
			}
			
			public void onlineErrorCallback(int errorCode) {
				RequestContext requestContext = new RequestContext();
				if (errorCode == BaseData.ERROR_RESPONSE)
					requestContext.setErrorMessage("You may be experiencing server/bandwidth problems.  Please try again, or contact support.");
				else if (errorCode == BaseData.ERROR_SERVER)
					requestContext.setErrorMessage("Problem in the connection with the server.");
				else
					requestContext.setErrorMessage("Unknown error.  Please contact support.");
				getServlet().redirectTo(new Index(requestContext));	
			}
			
		});
		
		formQueue = new FormQueueData(new OnlineOfflineCallbacks(servlet) {
			public void onlineSuccessCallback(String results) {
				if(results != null) {
					EventBus.get().fireEvent(new ProgressEvent((int)(((float)currentIndex / ApplicationConstants.tableIDs.length) * 100)));
					if(!results.equals("EOF")) {
						List objects = ((BaseData)ApplicationConstants.mappingBetweenTableIDAndDataObject.get(ApplicationConstants.tableIDs[currentIndex])).getListingOnline(results);
						BaseData.Data object;
						for (int i = 0; i < objects.size(); ++i) {
							object = (BaseData.Data) objects.get(i);
							object.save();
						}
						offset = offset + ApplicationConstants.PAGESIZE;
						formQueue.get(RequestContext.SERVER_HOST + ((BaseData)ApplicationConstants.mappingBetweenTableIDAndDataObject.get(ApplicationConstants.tableIDs[currentIndex])).getListingOnlineURL()+offset+"/"+(offset+ApplicationConstants.PAGESIZE)+"/");
					} else {
						currentIndex++;
						offset = 0;
						if(currentIndex == ApplicationConstants.tableIDs.length){
							updateSyncStatusInUserTable("0", "0");
							RequestContext requestContext = new RequestContext();
							requestContext.setMessage("Local database is in sync with the main server");
							getServlet().redirectTo(new Index(requestContext));	
						}else{
							updateSyncStatusInUserTable("1", ""+currentIndex);
							formQueue.get(RequestContext.SERVER_HOST + ((BaseData)ApplicationConstants.mappingBetweenTableIDAndDataObject.get(ApplicationConstants.tableIDs[currentIndex])).getListingOnlineURL()+offset+"/"+(offset+ApplicationConstants.PAGESIZE)+"/");
						}
					}
				}
			}
			
			public void onlineErrorCallback(int errorCode) {
				RequestContext requestContext = new RequestContext();
				if (errorCode == BaseData.ERROR_RESPONSE)
					requestContext.setErrorMessage("You may be experiencing server/bandwidth problems.  Please try again, or contact support.");
				else if (errorCode == BaseData.ERROR_SERVER)
					requestContext.setErrorMessage("Problem in the connection with the server.");
				else
					requestContext.setErrorMessage("Unknown error.  Please contact support.");
				getServlet().redirectTo(new Index(requestContext));	
			}
		});
		
		
		this.servlet = servlet;
		BaseData instance = new BaseData();
		ArrayList<Integer> resultSet = new ArrayList<Integer>();
		
		if(instance.checkIfUserTableExists()) {
			resultSet = loginData.checkDirtyBitStatusInTheUserTable(ApplicationConstants.getUsernameCookie());
		}
		if(instance.checkIfUserTableExists() && !resultSet.isEmpty() && resultSet.get(0) == 1){
			// Case 1 : Download has been interrupted in between. Resume the download
			this.currentIndex = resultSet.get(1);
			BaseData baseData = (BaseData)ApplicationConstants.mappingBetweenTableIDAndDataObject.get(ApplicationConstants.tableIDs[currentIndex]);
			// Delete the table on which the sync got interrupted.
			baseData.delete(baseData.getDeleteTableSql());
			baseData.create(baseData.getCreateTableSql());
			formQueue.get(RequestContext.SERVER_HOST + ((BaseData)ApplicationConstants.mappingBetweenTableIDAndDataObject.get(ApplicationConstants.tableIDs[currentIndex])).getListingOnlineURL()+offset+"/"+(offset+ApplicationConstants.PAGESIZE)+"/");
		}else{
			//Delete the complete schema
			Schema.dropSchema();
			Schema.createSchema();
			this.currentIndex = 0;
			indexData.apply(indexData.getGlobalPrimaryKey(ApplicationConstants.getUsernameCookie()));
		}
	}
	
	public Boolean postRowOfFormQueueTable(){
		BaseData.dbOpen();
		formQueue.select(FormQueueData.getUnsyncTableRow);
		if(formQueue.getResultSet().isValidRow()){
			try {
				if(formQueue.getResultSet().getFieldAsInt(4) == 0) {
					String queryString = formQueue.getResultSet().getFieldAsString(3);
					if(formQueue.getResultSet().getFieldAsChar(5) == 'A'){
						lastSyncedId  = formQueue.getResultSet().getFieldAsInt(0);
						formQueue.post(RequestContext.SERVER_HOST + 
								(String)((BaseData)ApplicationConstants.mappingBetweenTableIDAndDataObject.get(formQueue.getResultSet().getFieldAsString(1))).getSaveOfflineURL(), 
								queryString);
						BaseData.dbClose();
					}
					else if(formQueue.getResultSet().getFieldAsChar(5) == 'E'){
						lastSyncedId  = formQueue.getResultSet().getFieldAsInt(0);
						formQueue.post(RequestContext.SERVER_HOST + 
								(String)((BaseData)ApplicationConstants.mappingBetweenTableIDAndDataObject.get(formQueue.getResultSet().getFieldAsString(1))).getSaveOfflineURL() + formQueue.getResultSet().getFieldAsString(2) +"/" , 
								queryString);
						BaseData.dbClose();
					}
						
				}
			} catch(DatabaseException e){
				Window.alert("Database Exception : " + e.toString());
				BaseData.dbClose();
			}
			return true;
		}
		else{
			return false;
		}
	}
	
	public void updateSyncStatusInUserTable(String dirtyBit, String tableIndex){
		loginData.updateSyncStatus(dirtyBit, tableIndex , ApplicationConstants.getUsernameCookie());
	}
	
	public void updateSyncStatusOfLastSyncedRowInFormQueueTable(){
		formQueue.update(FormQueueData.updateSyncStatusOfARow, ""+lastSyncedId);
	}
	
	public void updateGlobalPkIDOnMainServer(){
		BaseData.dbOpen();
		formQueue.select(FormQueueData.getMaxGlobalPkId);
		if(formQueue.getResultSet().isValidRow()){
			String queryString;
			try {
				queryString = "id="+formQueue.getResultSet().getFieldAsInt(0)+"&username="+ApplicationConstants.getUsernameCookie();
				formQueue.post(this.setGlobalKeyURL, queryString);
			} catch (DatabaseException e) {
				Window.alert("Database Exception : " + e.toString());
				BaseData.dbClose();
			}
		}
		else{
			Window.alert("Caught unexpected error in the local database.");
		}
		BaseData.dbClose();
	}
	
	private void setGlobalIDInLocalUserTable(){
		IndexData indexData = new IndexData(new OnlineOfflineCallbacks(this.servlet) {
			public void onlineSuccessCallback(String results) {
				if(results != "0") {
					LoginData user = new LoginData();
					user.update(results, ApplicationConstants.getUsernameCookie(), ApplicationConstants.getPasswordCookie());
					RequestContext requestContext = new RequestContext();
					requestContext.setMessage("Local database is in sync with the main server");
					getServlet().redirectTo(new Index(requestContext));
				} else {
					RequestContext requestContext = new RequestContext();
					requestContext.setErrorMessage("You do not have a valid account.Please contact support. ");
					getServlet().redirectTo(new Index(requestContext));				
				}
			}
			
			public void onlineErrorCallback(int errorCode) {
				RequestContext requestContext = new RequestContext();
				if (errorCode == BaseData.ERROR_RESPONSE)
					requestContext.setErrorMessage("You may be experiencing server/bandwidth problems.  Please try again, or contact support.");
				else if (errorCode == BaseData.ERROR_SERVER)
					requestContext.setErrorMessage("Problem in the connection with the server.");
				else
					requestContext.setErrorMessage("Unknown error.  Please contact support.");
				getServlet().redirectTo(new Index(requestContext));	
			}
			
		});
		
		indexData.apply(indexData.getGlobalPrimaryKey(ApplicationConstants.getUsernameCookie()));

	}
	

}
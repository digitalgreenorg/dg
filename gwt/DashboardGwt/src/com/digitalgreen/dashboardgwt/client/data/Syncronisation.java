package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.ApplicationConstants;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.servlets.BaseServlet;
import com.digitalgreen.dashboardgwt.client.servlets.Index;
import com.google.gwt.gears.client.database.DatabaseException;
import com.google.gwt.gears.client.database.ResultSet;
import com.google.gwt.user.client.Window;

public class Syncronisation {
	
	public Syncronisation(){	
	}
	
	private FormQueueData formQueue;
	private LoginData loginData;
	private int lastSyncedId;
	private int currentIndex;
	private String setGlobalKeyURL = "/dashboard/setkey/";
	private BaseServlet servlet;
	private int offset = 0;
	
	public void syncFromLocalToMain(BaseServlet servlet){
		this.servlet = servlet;
		formQueue = new FormQueueData(new OnlineOfflineCallbacks(servlet) {
			public void onlineSuccessCallback(String results) {
				if(results == "1") {
						updateSyncStatusOfLastSyncedRowInFormQueueTable();
						if(!postRowOfFormQueueTable()){
								updateGlobalPkIDOnMainServer();
						}
				} else if(results =="0") {
					RequestContext requestContext = new RequestContext();
					requestContext.setMessageString("Validation Error : Form cannot be verified on the main server");
					getServlet().redirectTo(new Index(requestContext));		
				}else if(results=="synced"){
					setGlobalIDInLocalUserTable();
				}
				else{
					Window.alert("Unkown Error!");
				}
			}
			
			public void onlineErrorCallback(int errorCode) {
				Window.alert("GOT AN ERROR connecting to server");
				RequestContext requestContext = new RequestContext();
				if (errorCode == BaseData.ERROR_RESPONSE)
					requestContext.setMessageString("Unresponsive Server.  Please contact support.");
				else if (errorCode == BaseData.ERROR_SERVER)
					requestContext.setMessageString("Problem in the connection with the server.");
				else
					requestContext.setMessageString("Unknown error.  Please contact support.");
				getServlet().redirectTo(new Index(requestContext));	
			}
		});
		
		if(!postRowOfFormQueueTable()){
			RequestContext requestContext = new RequestContext();
			requestContext.setMessageString("Local database is in sync with the main server ");
			servlet.redirectTo(new Index(requestContext));
		}
	}
	
	public void syncFromMainToLocal(BaseServlet servlet){
		loginData = new LoginData();
		IndexData indexData = new IndexData(new OnlineOfflineCallbacks(servlet) {
			public void onlineSuccessCallback(String results) {
				if(results != "0") {
					LoginData user = new LoginData();
					user.insert(results, ApplicationConstants.getUsernameCookie(), ApplicationConstants.getPasswordCookie(), "1", "1", "0");
					formQueue.get(RequestContext.SERVER_HOST + ((BaseData)ApplicationConstants.mappingBetweenTableIDAndDataObject.get(ApplicationConstants.tableIDs[currentIndex])).getListingOnlineURL()+ offset+ "/" + ApplicationConstants.PAGESIZE + "/");
				} else {
					RequestContext requestContext = new RequestContext();
					requestContext.setMessageString("You do not have a valid account.Please contact support. ");
					getServlet().redirectTo(new Index(requestContext));				
				}
			}
			
			public void onlineErrorCallback(int errorCode) {
				Window.alert("GOT AN ERROR connecting to server");
				RequestContext requestContext = new RequestContext();
				if (errorCode == BaseData.ERROR_RESPONSE)
					requestContext.setMessageString("Unresponsive Server.  Please contact support.");
				else if (errorCode == BaseData.ERROR_SERVER)
					requestContext.setMessageString("Problem in the connection with the server.");
				else
					requestContext.setMessageString("Unknown error.  Please contact support.");
				getServlet().redirectTo(new Index(requestContext));	
			}
			
		});
		
		formQueue = new FormQueueData(new OnlineOfflineCallbacks(servlet) {
			public void onlineSuccessCallback(String results) {
				if(results != null) {
					if(!results.equals("EOF")){
						List objects = ((BaseData)ApplicationConstants.mappingBetweenTableIDAndDataObject.get(ApplicationConstants.tableIDs[currentIndex])).getListingOnline(results);
						BaseData.Data object;
						for (int i = 0; i < objects.size(); ++i) {
							object = (BaseData.Data) objects.get(i);
							object.save();
						}
						offset = offset + ApplicationConstants.PAGESIZE;
						formQueue.get(RequestContext.SERVER_HOST + ((BaseData)ApplicationConstants.mappingBetweenTableIDAndDataObject.get(ApplicationConstants.tableIDs[currentIndex])).getListingOnlineURL()+offset+"/"+(offset+ApplicationConstants.PAGESIZE)+"/");
					}else{
						currentIndex++;
						offset = 0;
						if(currentIndex == ApplicationConstants.tableIDs.length){
							updateSyncStatusInUserTable("0", "0");
							RequestContext requestContext = new RequestContext();
							requestContext.setMessageString("Local database is in sync with the main server");
							getServlet().redirectTo(new Index(requestContext));	
						}else{
							updateSyncStatusInUserTable("1", ""+currentIndex);
							formQueue.get(RequestContext.SERVER_HOST + ((BaseData)ApplicationConstants.mappingBetweenTableIDAndDataObject.get(ApplicationConstants.tableIDs[currentIndex])).getListingOnlineURL()+offset+"/"+(offset+ApplicationConstants.PAGESIZE)+"/");
						}
					}
				}
			}
			
			public void onlineErrorCallback(int errorCode) {
				Window.alert("GOT AN ERROR connecting to server");
				RequestContext requestContext = new RequestContext();
				if (errorCode == BaseData.ERROR_RESPONSE)
					requestContext.setMessageString("Unresponsive Server.  Please contact support.");
				else if (errorCode == BaseData.ERROR_SERVER)
					requestContext.setMessageString("Problem in the connection with the server.");
				else
					requestContext.setMessageString("Unknown error.  Please contact support.");
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
				if(formQueue.getResultSet().getFieldAsInt(3) == 0){
					String queryString = "id="+formQueue.getResultSet().getFieldAsString(1)+"&"+formQueue.getResultSet().getFieldAsString(2);
					if(formQueue.getResultSet().getFieldAsChar(4) == 'A'){
						lastSyncedId  = formQueue.getResultSet().getFieldAsInt(1);
						formQueue.post(RequestContext.SERVER_HOST + (String)((BaseData)ApplicationConstants.mappingBetweenTableIDAndDataObject.get(formQueue.getResultSet().getFieldAsString(0))).getSaveOfflineURL(), queryString);
						BaseData.dbClose();
					}
					else{
						// Take care of edit case
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
		String queryString = "id="+this.lastSyncedId+"&username="+ApplicationConstants.getUsernameCookie();
		formQueue.post(this.setGlobalKeyURL, queryString);
	}
	
	private void setGlobalIDInLocalUserTable(){
		IndexData indexData = new IndexData(new OnlineOfflineCallbacks(this.servlet) {
			public void onlineSuccessCallback(String results) {
				if(results != "0") {
					LoginData user = new LoginData();
					user.update(results, "1", "0", ApplicationConstants.getUsernameCookie(), ApplicationConstants.getPasswordCookie());
					RequestContext requestContext = new RequestContext();
					requestContext.setMessageString("Local database is in sync with the main server");
					getServlet().redirectTo(new Index(requestContext));
				} else {
					RequestContext requestContext = new RequestContext();
					requestContext.setMessageString("You do not have a valid account.Please contact support. ");
					getServlet().redirectTo(new Index(requestContext));				
				}
			}
			
			public void onlineErrorCallback(int errorCode) {
				Window.alert("GOT AN ERROR connecting to server");
				RequestContext requestContext = new RequestContext();
				if (errorCode == BaseData.ERROR_RESPONSE)
					requestContext.setMessageString("Unresponsive Server.  Please contact support.");
				else if (errorCode == BaseData.ERROR_SERVER)
					requestContext.setMessageString("Problem in the connection with the server.");
				else
					requestContext.setMessageString("Unknown error.  Please contact support.");
				getServlet().redirectTo(new Index(requestContext));	
			}
			
		});
		
		indexData.apply(indexData.getGlobalPrimaryKey(ApplicationConstants.getUsernameCookie()));

	}
	

}
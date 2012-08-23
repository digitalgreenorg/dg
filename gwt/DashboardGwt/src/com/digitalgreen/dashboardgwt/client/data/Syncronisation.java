package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.ApplicationConstants;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.servlets.BaseServlet;
import com.digitalgreen.dashboardgwt.client.servlets.Index;
import com.google.gwt.gears.client.database.DatabaseException;
import com.google.gwt.json.client.JSONObject;
import com.google.gwt.json.client.JSONParser;
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
	private int offset = 0;
		
	public void syncFromLocalToMain(BaseServlet servlet) {
		formQueue = new FormQueueData(new OnlineOfflineCallbacks(servlet) {
			
			protected void uploadNextRow() {
				this.setUploadInterrupted(ApplicationConstants.uploadNotInterrupted);
				currentIndex++;
				EventBus.get().fireEvent(new ProgressEvent((int)(((float)currentIndex / totalRowsToSync) * 100)));
				updateSyncStatusOfLastSyncedRowInFormQueueTable();
				if(!postRowOfFormQueueTable()) {
					updateGlobalPkIDOnMainServer();
				}
			}
			
			public void setUploadInterrupted(String value) {
				LoginData user = new LoginData();
		    	user.setUploadInterrupted(value, ApplicationConstants.getUsernameCookie());
			}
			
			public String getUploadInterrupted() {
				LoginData user=new LoginData();
				String value = user.getUploadInterrupted(ApplicationConstants.getUsernameCookie());
		        return value;
		    }
			
			public void onlineSuccessCallback(String results) {
				if(results.equals("1")) {
					this.uploadNextRow();
				} else if(results.equals("0")) {
					if (this.getUploadInterrupted().equals(ApplicationConstants.uploadInterrupted)) {
						/* Nandini Sync Status Error: Sometimes upload is successful but network is interrupted.
						 * Here, sync status may be 0 but the row has already been uploaded to the server.
						 */
						this.uploadNextRow(); // if upload was interrupted 
					}
					else {
						RequestContext requestContext = new RequestContext();
						requestContext.setErrorMessage("Validation Error.  Please contact support.");
						getServlet().redirectTo(new Index(requestContext));
					}
				} else if(results.equals("synced")) {
					EventBus.get().fireEvent(new ProgressEvent(100));
					RequestContext requestContext = new RequestContext();
					requestContext.setMessage("Local database is in sync with the main server.");
					getServlet().redirectTo(new Index(requestContext));
					//setGlobalIDInLocalUserTable();
				} else{
					Window.alert("Unkown Error.  Please contact support.");
				}
			}

			public void onlineErrorCallback(int errorCode) {
				RequestContext requestContext = new RequestContext();
				this.setUploadInterrupted(ApplicationConstants.uploadInterrupted);
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
		EventBus.get().fireEvent(new ProgressEvent(0));
		if(!postRowOfFormQueueTable()){
			updateGlobalPkIDOnMainServer();
			RequestContext requestContext = new RequestContext();
			requestContext.setMessage("Your data has been uploaded.  Local database is in sync with the main server.");
			servlet.redirectTo(new Index(requestContext));
		}
	}
	
	public void syncFromMainToLocal(BaseServlet servlet){
		loginData = new LoginData();
		IndexData indexData = new IndexData(new OnlineOfflineCallbacks(servlet) {
			public void onlineSuccessCallback(String results) {
				if(!results.equals("0")) {
					LoginData user = new LoginData();
					JSONObject resultObj = JSONParser.parse(results).isObject();
					String err_count = resultObj.get("dashboard_error_count").toString();
					String last_id = resultObj.get("last_id").toString();
					user.insert(last_id, ApplicationConstants.getUsernameCookie(), ApplicationConstants.getPasswordCookie(), ApplicationConstants.getCurrentOnlineStatus()? "1":"0", "1", "0", ApplicationConstants.getUserRoleCookie(),ApplicationConstants.uploadNotInterrupted, err_count);
					/*
					 * Testing Upload Interrupted Getter and Setter
					//user.setUploadInterrupted(ApplicationConstants.uploadInterrupted, ApplicationConstants.getUsernameCookie());
					//String uploadInterrupted = user.getUploadInterrupted(ApplicationConstants.getUsernameCookie());
					//Window.alert("Upload Interrupted " + uploadInterrupted);
					 */
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
					if(!results.equals("EOF")) {
						BaseData.dbOpen();
						try {
							BaseData.dbStartTransaction();
						} catch (DatabaseException e) {
							// TODO Auto-generated catch block
							Window.alert("Database transaction exception");
						}
						
						List objects = ((BaseData)ApplicationConstants.mappingBetweenTableIDAndDataObject.get(ApplicationConstants.tableIDs[currentIndex])).getListingOnline(results);
						BaseData.Data object;
						for (int i = 0; i < objects.size(); ++i) {
							object = (BaseData.Data) objects.get(i);
							object.save();
						}
						try {
							BaseData.dbCommit();
						} catch (DatabaseException e) {
							// TODO Auto-generated catch block
							Window.alert("BaseData commit exception"+e.toString());
						}
						BaseData.dbClose();						
						offset = offset + ApplicationConstants.PAGESIZE;
						formQueue.get(RequestContext.SERVER_HOST + ((BaseData)ApplicationConstants.mappingBetweenTableIDAndDataObject.get(ApplicationConstants.tableIDs[currentIndex])).getListingOnlineURL()+offset+"/"+(offset+ApplicationConstants.PAGESIZE)+"/");
					} else {
						currentIndex++;
						EventBus.get().fireEvent(new ProgressEvent((int)(((float)currentIndex / ApplicationConstants.tableIDs.length) * 100)));
						offset = 0;
						if(currentIndex == ApplicationConstants.tableIDs.length){
							updateSyncStatusInUserTable("0", "" + ApplicationConstants.tableIDs.length);
							Schema.createIndexes();
							RequestContext requestContext = new RequestContext();
							requestContext.setMessage("Your data has been downloaded.  Local database is in sync with the main server.");
							// This is to clear out anything left over in the progress bar the next time the operation is run.
							EventBus.get().fireEvent(new ProgressEvent(0));
							getServlet().redirectTo(new Index(requestContext));
							
						}else{
							updateSyncStatusInUserTable("1", "" + currentIndex);
							formQueue.get(RequestContext.SERVER_HOST + ((BaseData)ApplicationConstants.mappingBetweenTableIDAndDataObject.
									get(ApplicationConstants.tableIDs[currentIndex])).getListingOnlineURL()+offset+"/"+(offset+ApplicationConstants.PAGESIZE)+"/");
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
			offset = Integer.parseInt(baseData.getCount());
			//baseData.delete(baseData.getDeleteTableSql());
			//baseData.create(baseData.getCreateTableSql());
			EventBus.get().fireEvent(new ProgressEvent((int)(((float)currentIndex / ApplicationConstants.tableIDs.length) * 100)));
			formQueue.get(RequestContext.SERVER_HOST + ((BaseData)ApplicationConstants.mappingBetweenTableIDAndDataObject.
					get(ApplicationConstants.tableIDs[currentIndex])).getListingOnlineURL()+offset+"/"+(offset+ApplicationConstants.PAGESIZE)+"/");
			
		}else{
			//Delete the complete schema
			Schema.dropSchema();
			Schema.createSchema();
			this.currentIndex = 0;
			EventBus.get().fireEvent(new ProgressEvent(0));
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
								(String)((BaseData)ApplicationConstants.mappingBetweenTableIDAndDataObject.get(formQueue.getResultSet().getFieldAsString(1))).getSaveOfflineURL()
								+ formQueue.getResultSet().getFieldAsString(2) +"/" , 
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
		formQueue.select(FormQueueData.getLastInsertedID, ApplicationConstants.getUsernameCookie());
		if(formQueue.getResultSet().isValidRow()){
			String queryString;
			try {
				queryString = "id=" + formQueue.getResultSet().getFieldAsLong(0) + "&username=" + ApplicationConstants.getUsernameCookie();
				formQueue.post(RequestContext.SERVER_HOST + this.setGlobalKeyURL, queryString);
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
	

}
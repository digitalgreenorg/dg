package com.digitalgreen.dashboardgwt.client.data;

import java.util.HashMap;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.ApplicationConstants;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.servlets.BaseServlet;
import com.digitalgreen.dashboardgwt.client.servlets.Index;
import com.google.gwt.gears.client.database.DatabaseException;
import com.google.gwt.user.client.Window;

public class Syncronisation {
	
	public Syncronisation(){	
	}
	
	private FormQueueData formQueue;
	private int lastSyncedId;
	private int currentIndex=0;
	private String setGlobalKeyURL = "/dashboard/setkey/";
	private BaseServlet servlet;
	
	public void syncFromLocalToMain(BaseServlet servlet){
		this.servlet = servlet;
		formQueue = new FormQueueData(new OnlineOfflineCallbacks(servlet) {
			public void onlineSuccessCallback(String results) {
				if(results == "1") {
						updateSyncStatusOfLastSyncedRow();
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
		this.servlet = servlet;
		formQueue = new FormQueueData(new OnlineOfflineCallbacks(servlet) {
			public void onlineSuccessCallback(String results) {
				if(results != null) {
					List objects = ((BaseData)ApplicationConstants.mappingBetweenTableIDAndDataObject.get(ApplicationConstants.tableIDs[currentIndex])).getListingOnline(results);
					BaseData.Data object;
					for (int i = 0; i < objects.size(); ++i) {
						object = (BaseData.Data) objects.get(i);
						object.save();
					}
					currentIndex++;
					if(currentIndex == ApplicationConstants.tableIDs.length){
						RequestContext requestContext = new RequestContext();
						requestContext.setMessageString("Local database is in sync with the main server");
						getServlet().redirectTo(new Index(requestContext));	
					}else{
						formQueue.get(RequestContext.SERVER_HOST + ((BaseData)ApplicationConstants.mappingBetweenTableIDAndDataObject.get(ApplicationConstants.tableIDs[currentIndex])).getListingOnlineURL());
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

		formQueue.get(RequestContext.SERVER_HOST + ((BaseData)ApplicationConstants.mappingBetweenTableIDAndDataObject.get(ApplicationConstants.tableIDs[currentIndex])).getListingOnlineURL());
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
	
	public void updateSyncStatusOfLastSyncedRow(){
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
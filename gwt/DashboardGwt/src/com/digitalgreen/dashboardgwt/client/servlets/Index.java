package com.digitalgreen.dashboardgwt.client.servlets;

import com.digitalgreen.dashboardgwt.client.common.ApplicationConstants;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.DashboardGwt;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import java.util.HashMap;

import com.digitalgreen.dashboardgwt.client.data.BaseData;
import com.digitalgreen.dashboardgwt.client.data.FormQueueData;
import com.digitalgreen.dashboardgwt.client.data.Syncronisation;
import com.digitalgreen.dashboardgwt.client.data.UsersData;
import com.digitalgreen.dashboardgwt.client.data.IndexData;
import com.digitalgreen.dashboardgwt.client.data.LoginData;
import com.digitalgreen.dashboardgwt.client.servlets.BaseServlet;
import com.digitalgreen.dashboardgwt.client.templates.BaseTemplate;
import com.digitalgreen.dashboardgwt.client.templates.IndexTemplate;
import com.google.gwt.gears.client.Factory;
import com.google.gwt.gears.client.GearsException;
import com.google.gwt.gears.client.database.ResultSet;
import com.google.gwt.gears.client.localserver.LocalServer;
import com.google.gwt.gears.client.localserver.ManagedResourceStore;
import com.google.gwt.gears.client.localserver.ManagedResourceStoreCompleteHandler;
import com.google.gwt.gears.client.localserver.ManagedResourceStoreErrorHandler;
import com.google.gwt.gears.offline.client.Offline;
import com.google.gwt.user.client.Cookies;
import com.google.gwt.user.client.Timer;
import com.google.gwt.user.client.Window;

public class Index extends BaseServlet {
	public final static String pluginNotInstalled = "This browser does not have the Gears plugin. " +
		" Please <a href=\"http://gears.google.com/\" target=\"_blank\">install Gears</a> " +
		"and reload the application.";
	
	public final static String unsyncedRowsMessage = "You have unsynced rows that are pending " +
			"upload to the main server.  Please click on the 'Upload' button to start the upload.";
	
	public Index() {
		super();
	}
	
	public Index(RequestContext requestContext) {
		super(requestContext);
	}
	
	private boolean createManagedResourceStore() {
		try {
			final RequestContext requestContext = new RequestContext();
			final BaseServlet servlet = this;
			ManagedResourceStore managedResourceStore = Offline.getManagedResourceStore();
			managedResourceStore.setOnCompleteHandler(new ManagedResourceStoreCompleteHandler() {
				public void onComplete(ManagedResourceStoreCompleteHandler.ManagedResourceStoreCompleteEvent event) {
					requestContext.setMessage("Donwloaded all offline contents successfully.  You can now proceed with any offline activities.");
					servlet.redirectTo(new Index(requestContext));
				}
			});
			managedResourceStore.setOnErrorHandler(new ManagedResourceStoreErrorHandler() {
				public void onError(ManagedResourceStoreErrorHandler.ManagedResourceStoreErrorEvent error) {
					requestContext.setMessage("There was an error while downloading some offline contents.  " +
							"Please either try again by refreshing your page and clicking 'Go Offline, or contact support.");
					servlet.redirectTo(new Index(requestContext));
				}
			});
	    } catch (GearsException e) {
	    	return false;
	    }
	    return true;
	}
	
	@Override
	public void response () {
		super.response();
		String method = this.getMethodTypeCtx();
		
		if (!this.isLoggedIn()) {
			super.redirectTo(new Login());
		} 
		else {
			IndexData indexData = new IndexData();
			int offlineReadyState = indexData.checkIfOfflineReady(ApplicationConstants.getUsernameCookie());
			if(method.equals(RequestContext.METHOD_POST)) {
				HashMap queryArgs = (HashMap)this.requestContext.getArgs();
				String queryArg = (String)queryArgs.get("action");
				if(queryArg.equals("gooffline")) {
					RequestContext requestContext = new RequestContext();
					if(offlineReadyState == IndexData.STATUS_DB_NOT_OPEN) {
						requestContext.setErrorMessage(Index.pluginNotInstalled);
					} else if(offlineReadyState == IndexData.STATUS_SCHEMA_NOT_READY) {
						requestContext.setErrorMessage("We did not detect a database on your browser.  " +
								"Please click on the 'Download' button before going offline");
					} else {
						LocalServer server = Factory.getInstance().createLocalServer();
				    	if(!createManagedResourceStore()) {
				    		requestContext.setErrorMessage("Downloading of manifest file and static contents failed.");
				    	} else {
				    		LoginData user = new LoginData();
							user.updateAppStatus("0",ApplicationConstants.getUsernameCookie());
							ApplicationConstants.toggleConnection(false);
				    	}
					}
					this.redirectTo(new Index(requestContext));
				}
				else if (queryArg.equals("goonline")) {
					if(offlineReadyState == IndexData.STATUS_READY) {
						LoginData user = new LoginData();
						user.updateAppStatus("1", ApplicationConstants.getUsernameCookie());
					}
					ApplicationConstants.toggleConnection(true);
					RequestContext requestContext = new RequestContext();
					this.redirectTo(new Index(requestContext));
				}
				else if (queryArg.equals("sync")){
					RequestContext requestContext = new RequestContext();
					if(offlineReadyState == IndexData.STATUS_DB_NOT_OPEN) {
						requestContext.setErrorMessage(Index.pluginNotInstalled);
						this.redirectTo(new Index(requestContext));
					} else if(offlineReadyState == IndexData.STATUS_SCHEMA_NOT_READY) {
						requestContext.setErrorMessage("We did not detect a database on your browser.  " +
								"Please click on the 'Download' button before going offline");
						this.redirectTo(new Index(requestContext));
					} else {
						Syncronisation syncronisation = new Syncronisation();
						syncronisation.syncFromLocalToMain(this);
					}
				}
				else if (queryArg.equals("resync")) {
					RequestContext requestContext = new RequestContext();
					if(offlineReadyState == IndexData.STATUS_DB_NOT_OPEN) {
						requestContext.setErrorMessage(Index.pluginNotInstalled);
						this.redirectTo(new Index(requestContext));
					} else {
						FormQueueData formQueueDataDbApi = new FormQueueData();
						if(offlineReadyState == IndexData.STATUS_READY && formQueueDataDbApi.getUnsyncCount() > 0) {
							requestContext.setErrorMessage(Index.unsyncedRowsMessage);
							this.redirectTo(new Index(requestContext));
						} else {
							Syncronisation syncronisation = new Syncronisation();
							syncronisation.syncFromMainToLocal(this);
						}
					}
				}
			}
			else {
				BaseTemplate operationUi = new BaseTemplate();
				operationUi.hideGlassDoorMessage();
				this.requestContext.getArgs().put("showOfflineReady", offlineReadyState == IndexData.STATUS_READY);
				this.fillTemplate(new IndexTemplate(this.requestContext));
			}
		}
	}
}
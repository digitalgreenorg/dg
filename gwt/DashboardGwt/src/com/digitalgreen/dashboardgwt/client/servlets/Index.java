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
import com.google.gwt.gears.offline.client.Offline;
import com.google.gwt.user.client.Cookies;
import com.google.gwt.user.client.Timer;
import com.google.gwt.user.client.Window;

public class Index extends BaseServlet {
	public final static String pluginNotInstalled = "This browser does not have the Gears plugin. " +
		" Please <a href=\"http://gears.google.com/\" target=\"_blank\">install Gears</a> " +
		"and reload the application.";
	
	public Index(){
		super();
	}
	
	public Index(RequestContext requestContext) {
		super(requestContext);
	}
	
	private boolean createManagedResourceStore() {
		try {
			final ManagedResourceStore managedResourceStore = Offline.getManagedResourceStore();

			new Timer() {
				final String oldVersion = managedResourceStore.getCurrentVersion();
				String transferringData = "Transferring data";

				@Override
				public void run() {
					switch (managedResourceStore.getUpdateStatus()) {
					case ManagedResourceStore.UPDATE_OK:
						break;
					case ManagedResourceStore.UPDATE_CHECKING:
					case ManagedResourceStore.UPDATE_DOWNLOADING:
						transferringData += ".";
						schedule(500);
						break;
					case ManagedResourceStore.UPDATE_FAILED:
						break;
					}
				}
			}.schedule(500);
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
						Syncronisation syncronisation = new Syncronisation();
						syncronisation.syncFromMainToLocal(this);
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
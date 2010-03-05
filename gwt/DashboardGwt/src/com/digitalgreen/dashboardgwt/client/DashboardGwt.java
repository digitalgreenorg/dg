package com.digitalgreen.dashboardgwt.client;

import com.google.gwt.core.client.EntryPoint;
import com.digitalgreen.dashboardgwt.client.servlets.Index;
import com.digitalgreen.dashboardgwt.client.common.ApplicationConstants;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.BaseData;
import com.digitalgreen.dashboardgwt.client.data.LoginData;
import com.google.gwt.gears.client.database.ResultSet;
import com.google.gwt.http.client.*;
import com.google.gwt.user.client.Cookies;
import com.google.gwt.user.client.Timer;
import com.google.gwt.user.client.Window;

public class DashboardGwt implements EntryPoint {
	// Some globals
	
	final static private int timerDelayFactor = 2;
	final static private int timerDelayDefault = 5000;
	private Timer timer;
	private int timeDelay;

	public void onModuleLoad() {
		setup();
		Index index  = new Index();
		index.response();
		/*
		this.timer = new Timer() {
			@Override
			public void run() {
				checkServerConnection();
			}
		};
		this.timer.schedule(this.timeDelay);
		*/
	}
		
	/* Sets the status of the application as online / offline
	 * This function is called every time the application is refreshed */ 
	private void setup(){
		BaseData instance = new BaseData();
		if(instance.checkIfUserTableExists()){
			int status = instance.getApplicationStatus();
			if(status == 0){
				ApplicationConstants.toggleConnection(false);
			}
			else{
				ApplicationConstants.toggleConnection(true);
			}	
		}
		else{
			ApplicationConstants.toggleConnection(true);
		}
	}

	
	private void checkServerConnection() {
		String url = RequestContext.getServerUrl();
		RequestBuilder builder = new RequestBuilder(RequestBuilder.GET, URL.encode(url));
		try {
			Request request = builder.sendRequest(null, new RequestCallback() {
			public void onResponseReceived(Request request, Response response) {
				if (response.getStatusCode() == 200) {
					ApplicationConstants.toggleConnection(true);
					computeTimerDelay();
				}
			}
			public void onError(Request request, Throwable exception) {
				ApplicationConstants.toggleConnection(false);
				computeTimerDelay();
			}		           
		});
		} catch (RequestException e) {
			// Couldn't connect to server
			ApplicationConstants.toggleConnection(false);
			computeTimerDelay();
		}
	}

	private void computeTimerDelay() {
		this.timeDelay *= DashboardGwt.timerDelayFactor;
		// 30 mins
		if(this.timeDelay > 1000 * 60 * 30) {
			this.timeDelay = DashboardGwt.timerDelayDefault;
		}
		this.timer.schedule(this.timeDelay);
	}
	
	
}

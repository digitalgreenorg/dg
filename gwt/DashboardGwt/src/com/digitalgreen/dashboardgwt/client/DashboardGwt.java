package com.digitalgreen.dashboardgwt.client;

import java.util.HashMap;

import com.google.gwt.core.client.EntryPoint;
import com.google.gwt.dev.shell.BrowserChannel;
import com.google.gwt.event.logical.shared.ValueChangeEvent;
import com.google.gwt.event.logical.shared.ValueChangeHandler;
import com.digitalgreen.dashboardgwt.client.servlets.Index;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.google.gwt.http.client.*;
import com.google.gwt.user.client.History;
import com.google.gwt.user.client.HistoryListener;
import com.google.gwt.user.client.Timer;

public class DashboardGwt implements EntryPoint, HistoryListener{
	// Some globals
	private static boolean isOnline = true;
	
	final static private String digitalgreenDatabaseName = "digitalgreen";
	final static private int timerDelayFactor = 2;
	final static private int timerDelayDefault = 5000;
	private Timer timer;
	private int timeDelay;
	public static final String INIT_STATE = null;
	
	public void onModuleLoad() {
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
		History.addHistoryListener(this);
		initHistoryState();
	}
	
	public void initHistoryState(){
		
//		Get the history token. You can use History.getToken() throughout your
//		web application to determine what state your application should be in. 
		
		String token = History.getToken();
		
//		determine if there is a token in the history stack, and if there is not a token then you 
//		can pass through any string you want, denoting that your web application is in its initial state.
		if(token.length() == 0){
			onHistoryChanged(INIT_STATE);
		}else{
			onHistoryChanged(token);
		}
	}
	
	String oldToken = null;
	
	public void onHistoryChanged(String historyToken){
		 if(historyToken.equals(INIT_STATE)){
			 
		 }
	}

	private void checkServerConnection() {
		String url = RequestContext.getServerUrl();
		RequestBuilder builder = new RequestBuilder(RequestBuilder.GET, URL.encode(url));
		try {
			Request request = builder.sendRequest(null, new RequestCallback() {
			public void onResponseReceived(Request request, Response response) {
				if (response.getStatusCode() == 200) {
					DashboardGwt.toggleConnection(true);
					computeTimerDelay();
				}
			}
			public void onError(Request request, Throwable exception) {
				DashboardGwt.toggleConnection(false);
				computeTimerDelay();
			}		           
		});
		} catch (RequestException e) {
			// Couldn't connect to server
			DashboardGwt.toggleConnection(false);
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
	
	public static void toggleConnection(boolean isOnline) {
		DashboardGwt.isOnline = isOnline;
	}
	
	public static boolean getCurrentOnlineStatus() {
		return DashboardGwt.isOnline;
	}
	
	public static String getDatabaseName() {
		return DashboardGwt.digitalgreenDatabaseName;
	}
}

package com.digitalgreen.dashboardgwt.client;

import com.google.gwt.core.client.EntryPoint;
import com.google.gwt.event.logical.shared.ValueChangeEvent;
import com.google.gwt.event.logical.shared.ValueChangeHandler;
import com.digitalgreen.dashboardgwt.client.servlets.Index;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.google.gwt.http.client.*;
import com.google.gwt.user.client.History;
import com.google.gwt.user.client.Timer;
import com.google.gwt.user.client.Window;

public class DashboardGwt implements EntryPoint {
	// Some globals
	private static boolean isOnline = true;
	
	final static private String digitalgreenDatabaseName = "digitalgreen";
	final static private int timerDelayFactor = 2;
	final static private int timerDelayDefault = 5000;
	private Timer timer;
	private int timeDelay;
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
		installNavigationListener();
	}

	public static int doWork() {
		//Window.alert("IN DO WORK?");
		//Index index = new Index();
		//index.response();
		return 1;
	}
	public static native void installNavigationListener() /*-{
		$wnd.globalFunction = $entry(@com.digitalgreen.dashboardgwt.client.DashboardGwt::doWork()());
		//alert("COMING HERE AT LEAST");
	}-*/;

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
	
	private static void toggleConnection(boolean isOnline) {
		DashboardGwt.isOnline = isOnline;
	}
	
	public static boolean getCurrentOnlineStatus() {
		return DashboardGwt.isOnline;
	}
	
	public static String getDatabaseName() {
		return DashboardGwt.digitalgreenDatabaseName;
	}
}

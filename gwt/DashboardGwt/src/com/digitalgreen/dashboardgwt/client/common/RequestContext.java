package com.digitalgreen.dashboardgwt.client.common;

import java.util.HashMap;

// Emulating a marshalled HTTP request object
public class RequestContext {
	static public String METHOD_GET = "GET";
	static public String METHOD_POST = "POST";
	static public String SERVER_HOST = "http://174.129.13.106";
	
	private String methodTypeCtx = null;
	private String formAction = null;
	private HashMap args = null;
	private String messageString = null;
	private String queryString = null;
	private Form formTemplate = null;
	
	public RequestContext() {
		this.methodTypeCtx = METHOD_GET;
		this.args = new HashMap();
	}
	
	public RequestContext(String method) {
		this.methodTypeCtx = method;
		this.args = new HashMap();
	}

	public void setQueryString(String queryString) {
		this.queryString = queryString;
	}
	
	// TODO:  check for a form template after Form class in common is implemented
	public boolean hasQueryString() {
		return (queryString != null);
	}
	
	public String getQueryString() {
		return this.queryString;
	}

	public boolean hasMessages() {
		return this.messageString != null;
	}
	
	public void setMessageString(String messageString) {
		this.messageString = messageString;
	}
	
	public String getMessageString() {
		return this.messageString;
	}
	
	public String getMethodTypeCtx() {
		return this.methodTypeCtx;
	}

	public String getFormAction() {
		return this.formAction;
	}
	
	public void setFormAction(String action) {
		this.formAction = action;
	}
	
	public HashMap getArgs() {
		return this.args;
	}
	
	public void setArgs(HashMap args) {
		this.args = args;
	}
	
	public static String getServerUrl() {
		return "http://" + SERVER_HOST + "/";
	}
}
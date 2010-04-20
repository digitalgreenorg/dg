package com.digitalgreen.dashboardgwt.client.common;

import java.util.HashMap;

// Emulating a marshalled HTTP request object
public class RequestContext {
	final static private String DEFAULT_USERNAME_ARG_NAME = "loggedin_user";
	
	static public String METHOD_GET = "GET";
	static public String METHOD_POST = "POST";
	static public String SERVER_HOST = "http://127.0.0.1:8000";
	
	private String methodTypeCtx = null;
	private String formAction = null;
	private HashMap args = null;
	private String messageString = null;
	private Form form = null;
	
	public RequestContext() {
		this.methodTypeCtx = METHOD_GET;
		this.args = new HashMap();
		this.form = new Form();
	}
	
	public RequestContext(String method) {
		this.methodTypeCtx = method;
		this.args = new HashMap();
		this.form = new Form();
	}
	
	public Form getForm() {
		return this.form;
	}
	
	public void setForm(Form form) {
		this.form = form;
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
	
	public void setMethodTypeCtx(String methodTypeCtx) {
		this.methodTypeCtx = methodTypeCtx;
	}

	public boolean hasFormErrors() {
		return !this.form.isValid();
	}
	
	public String getFormErrorString() {
		return this.form.printFormErrors();
	}
}
package com.digitalgreen.dashboardgwt.client.common;

import java.util.HashMap;

// Emulating a marshalled HTTP request object
public class RequestContext {
	static public String METHOD_GET = "GET";
	static public String METHOD_POST = "POST";
	static public String SERVER_HOST = "http://www.digitalgreen.org/technology";
	
	private String methodTypeCtx = null;
	private String formAction = null;
	private HashMap args = null;
	private String message = null;
	private String errorMessage = null;
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
		return this.message != null;
	}
	
	public void setMessage(String message) {
		this.message = message;
	}
	
	public String getMessage() {
		return this.message;
	}
	
	public void setErrorMessage(String errorMessage) {
		this.errorMessage = errorMessage;
	}
	
	public String getErrorMessage() {
		return this.errorMessage;
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

	public boolean hasErrorMessages(){
		return this.errorMessage != null;
	}

}
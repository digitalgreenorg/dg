package com.digitalgreen.dashboardgwt.client.common;

import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.FormPanel;
import java.util.HashMap;

// Emulating a marshalled HTTP request object
public class RequestContext {
	static public String METHOD_GET = "GET";
	static public String METHOD_POST = "POST";
	static public String SERVER_HOST = "174.129.13.106";
	
	private String methodTypeCtx = null;
	private String formAction = null;
	private FormPanel data = null;
	private HashMap args = null;
	
	public RequestContext() {
		this.methodTypeCtx = METHOD_GET;
		this.args = new HashMap();
	}
	
	// method is most likely POST
	public RequestContext(String method, FormPanel postForm) {
		this.methodTypeCtx = method;
		this.data = postForm;
		this.args = new HashMap();
	}
	
	public String getMethodTypeCtx() {
		return this.methodTypeCtx;
	}
	
	public FormPanel getFormPanelCtx() {
		return this.data;
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
package com.digitalgreen.dashboardgwt.client.common;

import java.util.ArrayList;
import java.util.HashMap;

import com.digitalgreen.dashboardgwt.client.data.BaseData;

// TODO: FINISH THIS FOR NEXT REVISION
public class Form {
	private BaseData.Data parent;
	private Object[] dependents = null;
	private String queryString = null;
	
	public Form(BaseData.Data parent) {
		this.parent = parent;
	}
	
	public Form(BaseData.Data parent, Object[] dependents) {
		this.parent = parent;
		this.dependents = dependents;
	}
	
	public void save() {}

	public void populate() {}

	public static HashMap flatten(String queryString) {
		HashMap formHashMap = new HashMap();
		String[] queryStringList = queryString.split("&");
		for(int i=0; i < queryStringList.length; i++) {
			String[] nameValueList = queryStringList[i].split("=");
			formHashMap.put(nameValueList[0], nameValueList[1]);
		}
		return formHashMap;
	}
	
	// Return a tree data representation of the parsed query string.
	public void parseQueryString(String queryString) {
		String[] queryStringList = queryString.split("&");
		for(int i=0; i < queryStringList.length; i++) {
			String[] nameValueList = queryStringList[0].split("=");
			for(int j=0; j < this.dependents.length; j++) {
				if(this.dependents[j] instanceof ArrayList) {	
				} else if (this.dependents[j] instanceof BaseData.Data) {
				}
			}
		}
	}

	public void toQueryString() {}	
}
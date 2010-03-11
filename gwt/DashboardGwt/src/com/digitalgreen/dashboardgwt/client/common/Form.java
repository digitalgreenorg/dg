package com.digitalgreen.dashboardgwt.client.common;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Set;

import com.digitalgreen.dashboardgwt.client.data.BaseData;
import com.digitalgreen.dashboardgwt.client.data.BaseData.Data;

public class Form {
	private BaseData.Data parent;
	private Object[] dependents = null;
	private String queryString = null;
	private HashMap dataFormat = null;
	
	public Form(BaseData.Data parent) {
		this.parent = parent;
	}
	
	public Form(BaseData.Data parent, Object[] dependents) {
		this.parent = parent;
		this.dependents = dependents;
	}
	
	public HashMap getDataFormat() {
		return this.dataFormat;
	}

	// Save the dataFormat representation of the Form.  Transaction details
	// are left up to the caller.
	public void save() {
		// Save the parent first to get a FK for its dependents
		this.parent.save();
		String[] dataFormatKeys = (String[])dataFormat.keySet().toArray();
		for(String key : dataFormatKeys) {
			Object value = dataFormat.get(key);
			if(value instanceof ArrayList) {
				for(int i=0; i < ((ArrayList)value).size(); i++) {
					((BaseData.Data)((ArrayList)value).get(i)).save(this.parent);
				}
			} else {
				((BaseData.Data)value).save(this.parent);
			}
		}
	}

	public void fetch() {}

	public static HashMap flatten(String queryString) {
		HashMap formHashMap = new HashMap();
		String[] queryStringList = queryString.split("&");
		for(int i=0; i < queryStringList.length; i++) {
			String[] nameValueList = queryStringList[i].split("=");
			formHashMap.put(nameValueList[0], nameValueList[1]);
		}
		return formHashMap;
	}
	
	private String getCollectionNameFromArray(ArrayList dependentList) {
		BaseData.Data data = (BaseData.Data)dependentList.get(0);
		return data.getPrefixName();
	}
	
	private void setDataObjectField(BaseData.Data dataObj, String key, Object val) {
			dataObj.setObjValueFromString(key, val);
	}
	
	// This method collects name/value pairs from a flattened source hashmap into
	// an array of objects using this format: personmeetingattendance_set-0-expressed_question
	// queryString -> flattened hashmap -> array of populated BaseData.Data objects
	private void collectDependencies(ArrayList dependentList, HashMap sourceDict) {
		HashMap firstPassDict = new HashMap();
		String prefixName = getCollectionNameFromArray(dependentList);
		Object[] sourceKeys = sourceDict.keySet().toArray();
		for(int i=0; i < sourceKeys.length; i++) {
			String[] splitSourceKey = ((String)sourceKeys[i]).split("-");
			if(splitSourceKey[0].equalsIgnoreCase(prefixName + "_set")) {
				String dataObjKey = splitSourceKey[0] + "-" + splitSourceKey[1];
				BaseData.Data dataObj = (BaseData.Data)firstPassDict.get(dataObjKey);
				if(dataObj == null) {
					BaseData.Data newDataObj = (BaseData.Data)((BaseData.Data)dependentList.get(0)).clone();
					setDataObjectField(newDataObj, splitSourceKey[2], sourceDict.get(sourceKeys[i]));
					firstPassDict.put(dataObjKey, newDataObj);
				} else {
					setDataObjectField(dataObj, splitSourceKey[2], sourceDict.get(sourceKeys[i]));
				}
			}
		}
	
		// Finally add the collected list of objects as an array in our output hashmap.  
		dataFormat.put(prefixName, new ArrayList(firstPassDict.values()));
	}
	
	// Similar to the list case but using format: personmeetingattendance_expressed_question
	private void collectDependency(BaseData.Data dependent, HashMap sourceDict) {
		String prefixName = dependent.getPrefixName();
		Object[] sourceKeys = sourceDict.keySet().toArray();
		BaseData.Data newDataObj = (BaseData.Data)dependent.clone();
		for(int i=0; i < sourceKeys.length; i++) {
			String prefixSrc = ((String)sourceKeys[i]).substring(0, prefixName.length() - 1);
			if(prefixSrc.equalsIgnoreCase(prefixName)) {
				String attributeName = ((String)sourceKeys[i]).substring(prefixName.length() + 1);
				setDataObjectField(newDataObj, attributeName, sourceDict.get(sourceKeys[i]));
			}
		}
		// This is for a single object in the Form tree
		dataFormat.put(prefixName, newDataObj);
	}
	
	// Return a tree data representation of a parsed query string.
	public void parseQueryString(String queryString) {
		HashMap sourceDict = Form.flatten(queryString);
		for(int j=0; j < this.dependents.length; j++) {
			Object dataFormatted = null;
			if(this.dependents[j] instanceof ArrayList) {
				collectDependencies((ArrayList)this.dependents[j], sourceDict);
			} else if (this.dependents[j] instanceof BaseData.Data) {
				collectDependency((BaseData.Data)this.dependents[j], sourceDict);
			}
			
		}
	}
}
package com.digitalgreen.dashboardgwt.client.common;

import java.util.ArrayList;
import java.util.HashMap;
import com.digitalgreen.dashboardgwt.client.data.BaseData;
import com.digitalgreen.dashboardgwt.client.data.FormQueueData;
import com.digitalgreen.dashboardgwt.client.templates.BaseTemplate;
import com.google.gwt.http.client.URL;

public class Form {
	private BaseData.Data parent = null;
	private Object[] dependents = null;
	private HashMap dataFormat = null;
	private String queryString = null;
	private FormQueueData formQueue = null;
	private ArrayList baseDataErrorStack = null;
	private String id = null;
	
	public Form() {}
	
	public Form(BaseData.Data parent) {
		this.parent = parent;
		this.dependents = new Object[] {};
		this.dataFormat = new HashMap();
		this.formQueue = new FormQueueData();
		this.baseDataErrorStack = new ArrayList();
	}
	
	public Form(BaseData.Data parent, Object[] dependents) {
		this.parent = parent;
		this.dependents = dependents;
		this.dataFormat = new HashMap();
		this.formQueue = new FormQueueData();
		this.baseDataErrorStack = new ArrayList();
	}
	
	public String getQueryString() {
		return this.queryString;
	}

	public FormQueueData getFormQueue() {
		return this.formQueue;
	}
	
	public void setQueryString(String queryString) {
		this.queryString = URL.decodeComponent(queryString, true);
	}
	
	public boolean isValid() {
		return this.baseDataErrorStack != null && this.baseDataErrorStack.isEmpty();
	}
	
	public void setId(String id) {
		this.id = id;
	}
	
	public String getId() {
		return this.id;
	}
	
	public boolean validate() {
		boolean hasErrors = false;
		this.parseQueryString(this.queryString);
		if(!this.parent.validate()) {
			this.baseDataErrorStack.add(this.parent);
			hasErrors = true;
		}
		Object[] dataFormatKeys = dataFormat.keySet().toArray();
		for(int i=0; i < dataFormatKeys.length; i++) {
			// We already saved the parent so don't bother going over it again
			if(dataFormatKeys[i].equals(this.parent.getPrefixName()) ||
					dataFormatKeys[i].equals(this.parent.getPrefixName() + "_set")) {
				continue;
			}
			Object value = dataFormat.get(dataFormatKeys[i]);
			if(value instanceof ArrayList) {
				for(int j=0; j < ((ArrayList)value).size(); j++) {
					BaseData.Data dependentData = (BaseData.Data)((ArrayList)value).get(j);
					if(!dependentData.validate(this.parent)) {
						this.baseDataErrorStack.add(dependentData);
						hasErrors = true;
					}
					//Code to handle if user enters same data in two or more inlines
					else {
						//Comparing inline objects with previous objects
						for(int k=j-1; k>=0; k--) {
							BaseData.Data other = (BaseData.Data)((ArrayList)value).get(k);
							//Return true if new object details are same as any previous object details for inlines
							if(dependentData.compare(other)) {
								this.baseDataErrorStack.add(dependentData);
								hasErrors = true;
							}
						}
					}
				}
			} else {
				if(!((BaseData.Data)value).validate(this.parent)) {
					this.baseDataErrorStack.add(((BaseData.Data)value));
					hasErrors = true;
				}
			}
		}
		return !hasErrors;
	}
	
	public void toQueryString(String id) {
		String queryString = this.parent.toQueryString(id);
		for(int i=0; i < this.dependents.length; i++) {
			if(this.dependents[i] instanceof ArrayList) {
				queryString += "&" + ((BaseData.Data)((ArrayList)this.dependents[i]).get(0)).toInlineQueryString(id);
			} else {
				queryString += "&" + ((BaseData.Data)this.dependents[i]).toInlineQueryString(id);
			}
		}
		
		// This fixes the validation error issue where, on validation error, we want
		// to preserve the user inputted fields that caused the error.  Fix for now.
		if(this.queryString == null) {
			this.queryString = queryString;
		}
	}
	
	// Save the dataFormat representation of the Form.  Transaction details
	// are left up to the caller.
	public void save() {
		this.parseQueryString(this.queryString);
		// Prepare the save first in case it's a many to many, we may need to
		// delete rows in corresponding m2m tables.
		if(this.id != null && this.parent.hasManyToManyRelationships()) {
			this.parent.deleteManyToManyDependents(this.id);
		}
		// Save the parent first to get a FK for its dependents
		this.parent.save();
		FormQueueData.Data formQueueAdd = this.formQueue.initFormQueueAdd(this.parent.getTableId(), 
				this.parent.getId(), this.parent.getQueryString(), this.parent.getMode());
		this.formQueue.addFormQueueData(formQueueAdd);
		Object[] dataFormatKeys = dataFormat.keySet().toArray();
		for(int i=0; i < dataFormatKeys.length; i++) {
			// We already saved the parent so don't bother going over it again
			if(dataFormatKeys[i].equals(this.parent.getPrefixName()) ||
					dataFormatKeys[i].equals(this.parent.getPrefixName() + "_set")) {
				continue;
			}
			Object value = dataFormat.get(dataFormatKeys[i]);
			if(value instanceof ArrayList) {
				for(int j=0; j < ((ArrayList)value).size(); j++) {
					BaseData.Data dependentData = (BaseData.Data)((ArrayList)value).get(j);
					dependentData.save(this.parent);
					if(!dependentData.isManyToManyDependent()) {
						formQueueAdd = this.formQueue.initFormQueueAdd(dependentData.getTableId(), 
								dependentData.getId(), dependentData.getQueryString(), 
								dependentData.getMode());
						this.formQueue.addFormQueueData(formQueueAdd);
					}
				}
			} else {
				((BaseData.Data)value).save(this.parent);
				if(!((BaseData.Data)value).isManyToManyDependent()) {
					formQueueAdd = this.formQueue.initFormQueueAdd(((BaseData.Data)value).getTableId(), 
							((BaseData.Data)value).getId(), ((BaseData.Data)value).getQueryString(), 
							((BaseData.Data)value).getMode());
					this.formQueue.addFormQueueData(formQueueAdd);
				}
			}
		}
	}

	public static HashMap flatten(String queryString) {
		HashMap formHashMap = new HashMap();
		String[] queryStringList = queryString.split("&");
		for(int i=0; i < queryStringList.length; i++) {
			String[] nameValueList = queryStringList[i].split("=");
			// Discard null query params.  No value inputted by user.
			if(nameValueList[1] != null) {
				Object value = formHashMap.get(nameValueList[0]);
				if (value == null) {
					formHashMap.put(nameValueList[0], nameValueList[1]);
				} else if (value instanceof ArrayList) {
					((ArrayList)value).add(nameValueList[1]);
				} else {
					ArrayList arrayValue = new ArrayList();
					arrayValue.add(value);
					arrayValue.add(nameValueList[1]);
					formHashMap.remove(nameValueList[0]);
					formHashMap.put(nameValueList[0], arrayValue);
				}
			}
		}
		return formHashMap;
	}
	
	private String getCollectionNameFromArray(ArrayList dependentList) {
		BaseData.Data dependentType = (BaseData.Data)dependentList.get(0);
		return dependentType.getPrefixName();
	}
	
	private void setDataObjectField(BaseData.Data dataObj, String key, Object val) {
		if(val != null && val instanceof String) {
			dataObj.setObjValueFromString(key, (String)val);
			if(key.equals("id")) {
				dataObj.setMode(FormQueueData.Data.ACTION_EDIT);
			}
		}
	}
	
	private static boolean isInteger(String integer) {
		try {
			int i = Integer.parseInt(integer);
			return true;
		} catch (NumberFormatException e) {
			return false;
		}
	}
	
	// This method collects name/value pairs from a flattened source hashmap into
	// an array of objects using this format: personmeetingattendance_set-0-expressed_question
	// queryString -> flattened hashmap -> array of populated BaseData.Data objects
	private void collectDependencies(ArrayList dependentList, HashMap sourceDict) {
		HashMap firstPassDict = new HashMap();
		String prefixName = getCollectionNameFromArray(dependentList);
		Object[] sourceKeys = sourceDict.keySet().toArray();
		String[] splitSourceKey = null;
		for(int i=0; i < sourceKeys.length; i++) {
			splitSourceKey = ((String)sourceKeys[i]).split("-");
			// Case 1:  persongroups_set
			// Case 2:  home_village (no set included for whatever reason
			// And check if persongroups_set-1 (that 1 is an integer.  Sometimes
			// there's junk there.
			if((splitSourceKey[0].equalsIgnoreCase(prefixName + "_set") ||
					splitSourceKey[0].equalsIgnoreCase(prefixName)) &&
					Form.isInteger(splitSourceKey[1])) {
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
	
	private void createManyToManyRelationships(BaseData.Data parent, HashMap sourceDict) {
		if(!parent.hasManyToManyRelationships()) {
			return;
		}
		Object[] sourceKeys = sourceDict.keySet().toArray();
		for(int i=0; i < sourceKeys.length; i++) {
			Object value = sourceDict.get(sourceKeys[i]);
			HashMap manyToManyRelationshipMap = parent.getManyToManyRelationships();
			BaseData.ManyToManyRelationship manyToManyRelationship = (BaseData.ManyToManyRelationship)manyToManyRelationshipMap.get((String)sourceKeys[i]);
			if(manyToManyRelationship != null) {
				ArrayList listBaseData = new ArrayList();
				if(!(value instanceof ArrayList)) {
					BaseData.Data baseData = ((manyToManyRelationship.getToTable()).getNewData()).clone();
					baseData.setAsManyToManyDependent();
					setDataObjectField(baseData, manyToManyRelationship.getField(), value);
					listBaseData.add(baseData);
				} else {
					ArrayList srcValue = (ArrayList)value;
					for(int j=0; j < srcValue.size(); j++) {
						BaseData.Data baseData = ((manyToManyRelationship.getToTable()).getNewData()).clone();
						baseData.setAsManyToManyDependent();
						setDataObjectField(baseData, manyToManyRelationship.getField(), srcValue.get(j));
						listBaseData.add(baseData);
					}
				}
				dataFormat.put(manyToManyRelationship.getAttributeCollectionName(), listBaseData);
			}
		}
	}
	
	private void collectParent(BaseData.Data parent, HashMap sourceDict) {
		Object[] sourceKeys = sourceDict.keySet().toArray();
		this.parent = parent.clone();
		for(int i=0; i < sourceKeys.length; i++) {
			if(sourceDict.get(sourceKeys[i]) instanceof ArrayList) {
				for(int j=0; j < ((ArrayList)sourceDict.get(sourceKeys[i])).size(); j++) {
					setDataObjectField(this.parent, (String)sourceKeys[i], ((ArrayList)sourceDict.get(sourceKeys[i])).get(j));
				}
			} else {
				setDataObjectField(this.parent, (String)sourceKeys[i], sourceDict.get(sourceKeys[i]));
			}
		}
		dataFormat.put((String)parent.getPrefixName(), this.parent);
		this.createManyToManyRelationships(this.parent, sourceDict);
	}

	// Return a tree data representation of a parsed query string.
	public void parseQueryString(String queryString) {
		if(!this.dataFormat.isEmpty()) {
			return;
		}
		HashMap sourceDict = Form.flatten(queryString);
		// Add the special edit id in case we have one
		if(this.id != null) {
			sourceDict.put("id", this.id);
		}
		collectParent(this.parent, sourceDict);
		for(int j=0; j < this.dependents.length; j++) {
			if(this.dependents[j] instanceof ArrayList) {
				collectDependencies((ArrayList)this.dependents[j], sourceDict);
			} else if (this.dependents[j] instanceof BaseData.Data) {
				collectDependency((BaseData.Data)this.dependents[j], sourceDict);
			}	
		}
	}
	
	public static String retriveQueryStringFromHTMLString(String html){
		return BaseTemplate.createEditQueryString(html);
	}
	
	public String printFormErrors() {
		String outputErrors = "";
		for(int i=0; i < this.baseDataErrorStack.size(); i++) {
			BaseData.Data baseData = (BaseData.Data)this.baseDataErrorStack.get(i);
			outputErrors += "For " + baseData.getPrefixName() + ":</br>";
			for(int j=0; j < baseData.getErrorStack().size(); j++) {
				ArrayList errorList = baseData.getErrorStack();
				outputErrors += "&nbsp;&nbsp;&nbsp;&nbsp;" + (String)errorList.get(j) + "</br>"; 
			}
		}
		return outputErrors;
	}
}
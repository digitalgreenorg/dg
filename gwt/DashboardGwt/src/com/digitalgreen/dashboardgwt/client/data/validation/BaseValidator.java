package com.digitalgreen.dashboardgwt.client.data.validation;

public class BaseValidator {
	private boolean nullable = true;
	private boolean blank = true;
	private Object value = null;
	private String errorString = "Invalid field.";
	
	public BaseValidator(Object value) {
		this.value = value;
	}
	
	public BaseValidator(Object value, boolean nullable) {
		this.value = value;
		this.nullable = nullable;
	}
	
	public BaseValidator(Object value, boolean nullable, boolean blank) {
		this.value = value;
		this.nullable = nullable;
		this.blank = blank;
	}

	public boolean isNullable() {
		return this.nullable;
	}
	
	public boolean isBlankable() {
		return this.blank;
	}
	
	public boolean isNotEmpty() {
		String valueTrim = new String((String)value);
		return !valueTrim.isEmpty();
	}
	
	public Object getValue() {
		return this.value;
	}
	
	// Override this
	public boolean validate() {
		if(!nullable && value == null) {
			return false;
		}
		if(value != null && value instanceof String) {
			String valueTrim = new String((String)value);
			if(!blank && valueTrim.isEmpty()){
				return false;
			}
		}
		return true;
	}

	public void setError(String errorString) {
		this.errorString = errorString;
	}
	
	public String getError() {
		return this.errorString;
	}
}
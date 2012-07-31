package com.digitalgreen.dashboardgwt.client.data.validation;

public class BaseValidator {
	protected boolean nullable = true;
	protected boolean blank = true;
	protected Object value = null;
	protected String childLabel = null;
	protected String errorString = "Invalid field entries : ";
	//Validation Error Messages format
	protected final String requiredFieldErrorMessage = "Is a required field";
	protected final String maximumCharactersErrorMessage = "Maximum number of characters allowed are ";
	protected final String specialCharactersErrorMessage = "Should not contain any special characters ";
	protected final String dateFormatErrorMessage = "Should be formatted as 'YYYY-MM-DD'.";
	protected final String timeFormatErrorMessage = "Should be formatted as 'Hours:Minutes:Seconds (e.g: 07:30:00)'.";
	protected final String integerErrorMessage = "Requires a valid integer ";
	protected final String integerMaxMinErrorMessage = "Value should be between ";
	protected final String uniqueValidatorErrorMessage = " Already in system. Please make sure it is unique";
	protected final String floatFormatErrorMessage = " Is not valid. ";
	protected final String manyToManyErrorMessage = " Enter atleast one value. ";	
	
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
	
	public BaseValidator(String childLabel, Object value, boolean nullable, boolean blank) {
		this.value = value;
		this.nullable = nullable;
		this.blank = blank;
		this.childLabel = childLabel;
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
		errorString = childLabel+" : ";
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
package com.digitalgreen.dashboardgwt.client.data.validation;

import java.util.HashMap;

import com.google.gwt.user.client.Window;

public class StringValidator extends BaseValidator {
	
	final static protected String strictChars = "[a-zA-Z0-9._, ]+";
	protected int minValue = Integer.MIN_VALUE;
	protected int maxValue = Integer.MAX_VALUE;
	protected HashMap choices = null;
	protected boolean strictCharSet = false;
	
	public StringValidator(String value) {
		super(value);
	}
	
	public StringValidator(String childLabel, String value, boolean nullable, boolean blank) {
		super(value, nullable, blank);
		this.childLabel = childLabel;
	}
	
	public StringValidator(String childLabel, String value, boolean nullable, boolean blank, 
			int minValue, int maxValue) {
		super(value, nullable, blank);
		this.minValue = minValue;
		this.maxValue = maxValue;
		this.childLabel = childLabel;
	}
	
	public StringValidator(String childLabel, String value, boolean nullable, boolean blank, 
			int minValue, int maxValue, boolean strictCharSet) {
		super(childLabel,value, nullable, blank);
		this.minValue = minValue;
		this.maxValue = maxValue;
		this.strictCharSet = strictCharSet;
		this.childLabel = childLabel;
	}
	
	@Override
	public boolean validate() {
		if(!super.validate()){
			errorString += requiredFieldErrorMessage; 
			return false;
		} else if(this.getValue() == null){
			return true;
		} else if(!(((String)this.getValue()).length() >= this.minValue && 
				((String)this.getValue()).length() <= this.maxValue)) {
			errorString += maximumCharactersErrorMessage+Integer.toString(this.maxValue);
			return false;
		}		
		
		if(this.getValue() != null && this.isNotEmpty() && this.strictCharSet && 
				!validateUniCodeChars((String)this.getValue())) {
			errorString += specialCharactersErrorMessage;
			return false;
		}
		return true;
	}
	
	private boolean validateUniCodeChars(String value) {
		String strictUniCodeChars = ".*[^\\x20-\\x7E].*";
		if(value.matches(StringValidator.strictChars)) {
			return true;
		} 
		if(value.matches(strictUniCodeChars)) {
			return true;
		} else {
			return false;
		}
	}
}
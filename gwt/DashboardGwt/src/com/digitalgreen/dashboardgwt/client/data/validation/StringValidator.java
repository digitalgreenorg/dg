package com.digitalgreen.dashboardgwt.client.data.validation;

import java.util.HashMap;

import com.google.gwt.user.client.Window;

public class StringValidator extends BaseValidator {
	
	final static private String strictChars = "[a-zA-Z0-9][a-zA-Z0-9 ]*";
	private int minValue = Integer.MIN_VALUE;
	private int maxValue = Integer.MAX_VALUE;
	private HashMap choices = null;
	private boolean strictCharSet = false;
	
	public StringValidator(String value) {
		super(value);
	}
	
	public StringValidator(String value, boolean nullable, boolean blank) {
		super(value, nullable, blank);
	}
	
	public StringValidator(String value, boolean nullable, boolean blank, 
			int minValue, int maxValue) {
		super(value, nullable, blank);
		this.minValue = minValue;
		this.maxValue = maxValue;
	}
	
	public StringValidator(String value, boolean nullable, boolean blank, 
			int minValue, int maxValue, boolean strictCharSet) {
		super(value, nullable, blank);
		this.minValue = minValue;
		this.maxValue = maxValue;
		this.strictCharSet = strictCharSet;
	}
	
	@Override
	public boolean validate() {
		if(!super.validate()){ 
			return false;
		} else if(this.getValue() == null){
			return true;
		} else if(!(((String)this.getValue()).length() >= this.minValue && 
				((String)this.getValue()).length() <= this.maxValue)) {
			return false;
		}		
		if(this.getValue() != null && this.isNotEmpty() && this.strictCharSet && 
				!((String)this.getValue()).matches(StringValidator.strictChars)) {
			return false;
		}
		return true;
	}
}
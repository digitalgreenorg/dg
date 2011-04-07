package com.digitalgreen.dashboardgwt.client.data.validation;

import com.google.gwt.user.client.Window;

public class TimeValidator extends BaseValidator {

	public TimeValidator(String value) {
		super(value);
	}
	
	public TimeValidator(String childLabel, String value, boolean nullable, boolean blank) {		
		super(value, nullable, blank);
		this.childLabel = childLabel;
	}

	private boolean validateHour(String hour) {
		if(hour.length() == 2){
			int valueInt = 0;
			try {
				valueInt = Integer.parseInt(hour);
			} catch(Exception e) {
				return false;
			}
			
			return valueInt >= 0 && valueInt <= 24;
		}
		else {
			return false;
		}
		
	}
	
	private boolean validateMinute(String minute) {
		if(minute.length() == 2) {
			int valueInt = 0;
			try {
				valueInt = Integer.parseInt(minute);
			} catch(Exception e) {
				return false;
			}
			return valueInt >= 0 && valueInt <= 60;
		}
		else {
			return false;
		}
		
	}
	
	private boolean validateSecond(String second) {
		if (second.length() == 2) {
			int valueInt = 0;
			try {
				valueInt = Integer.parseInt(second);
			} catch(Exception e) {
				return false;
			}
			return valueInt >= 0 && valueInt <= 60;
		}
		else {
			return false;
		}
		
	}
	
	@Override
	public boolean validate() {
		if(!super.validate()) {
			errorString += reqiuredFieldErrorMessage;
			return false;
		} else if(this.getValue() == null){
			return true;
		}
		if(((String)this.getValue()).length() > 8) {
			errorString += timeFormatErrorMessage;
			return false;
		}
		String[] hourMinuteSecond = ((String)this.getValue()).split(":");
		if (this.validateHour(hourMinuteSecond[0]) &&
			this.validateMinute(hourMinuteSecond[1]) &&
			this.validateSecond(hourMinuteSecond[2])) 
			return true;
		else {
			errorString += timeFormatErrorMessage;
			return false;
		}
	}
}
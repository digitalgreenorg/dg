package com.digitalgreen.dashboardgwt.client.data.validation;

public class TimeValidator extends BaseValidator {

	public TimeValidator(String value) {
		super(value);
	}
	
	public TimeValidator(String value, boolean nullable, boolean blank) {
		super(value, nullable, blank);
	}

	private boolean validateHour(String hour) {
		int valueInt = 0;
		try {
			valueInt = Integer.parseInt(hour);
		} catch(Exception e) {
			return false;
		}
		
		return valueInt >= 0 && valueInt <= 24;
	}
	
	private boolean validateMinute(String minute) {
		int valueInt = 0;
		try {
			valueInt = Integer.parseInt(minute);
		} catch(Exception e) {
			return false;
		}
		return valueInt >= 0 && valueInt <= 60;
	}
	
	private boolean validateSecond(String second) {
		int valueInt = 0;
		try {
			valueInt = Integer.parseInt(second);
		} catch(Exception e) {
			return false;
		}
		return valueInt >= 0 && valueInt <= 60;
	}
	
	@Override
	public boolean validate() {
		if(!super.validate()) {
			return false;
		} else if(this.getValue() == null){
			return true;
		}
		String[] dateTime = this.getValue().split(" ");
		DateValidator dateValidator = new DateValidator(dateTime[0]);
		if(!dateValidator.validate()) {
			return false;
		}
		String[] hourMinuteSecond = dateTime[1].split(":");
		return this.validateHour(hourMinuteSecond[0]) &&
			this.validateMinute(hourMinuteSecond[1]) &&
			this.validateSecond(hourMinuteSecond[2]);
	}
}
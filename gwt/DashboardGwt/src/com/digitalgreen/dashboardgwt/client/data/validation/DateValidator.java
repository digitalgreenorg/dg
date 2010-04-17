package com.digitalgreen.dashboardgwt.client.data.validation;

import com.google.gwt.user.client.Window;

public class DateValidator extends BaseValidator {

	public DateValidator(String value) {
		super(value);
	}

	public DateValidator(String value, boolean nullable, boolean blank) {
		super(value, nullable, blank);
	}

	private boolean validateYear(String year) {
			try {
				int valueInt = Integer.parseInt(year);
			} catch (Exception e) {
				return false;
			}
			return year != null && year.length() == 4;		
	}

	private boolean validateMonth(String month) {
		int valueInt = 0;
		try {
				valueInt = Integer.parseInt(month);
		} 
		catch (Exception e) {
				return false;
		}
		return month != null && month.length() == 2 && valueInt >= 1 && valueInt <= 12;	
	}

	private boolean validateDay(String day) {
		int valueInt = 0;
		try {
			valueInt = Integer.parseInt(day);
		} 
		catch (Exception e) {
				return false;
		}
		return day != null && day.length() == 2 && valueInt >= 1 && valueInt <= 31;		
	}

	@Override
	public boolean validate() {
		if (!super.validate()) {
			return false;
		} else if(this.getValue() == null){
			return true;
		}		
		String[] yearMonthDay = this.getValue().split("-");
		return this.validateYear(yearMonthDay[0])
				&& this.validateMonth(yearMonthDay[1])
				&& this.validateDay(yearMonthDay[2]);
	}
}
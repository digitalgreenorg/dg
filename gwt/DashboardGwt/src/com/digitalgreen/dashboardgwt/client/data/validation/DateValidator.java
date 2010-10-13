package com.digitalgreen.dashboardgwt.client.data.validation;


import java.util.Date;

import com.google.gwt.i18n.client.DateTimeFormat;
import com.google.gwt.user.client.Window;

public class DateValidator extends BaseValidator {

	public DateValidator(String value) {
		super(value);
	}

	public DateValidator(String childLabel, String value, boolean nullable, boolean blank) {
		super(value, nullable, blank);
		this.childLabel = childLabel;
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
			errorString += reqiuredFieldErrorMessage;
			return false;
		} else if(this.getValue() == null){
			return true;
		}
		try {
			//Using GWT API for validating date.
			Date date = DateTimeFormat.getFormat("yyyy-MM-dd").parseStrict((String)this.getValue());
		} catch (IllegalArgumentException e) {
			errorString += dateFormatErrorMessage;
			return false;
		}
		return true;
		//Code do not work for illegal dates like 2010-30-30
		/*String[] yearMonthDay = ((String)this.getValue()).split("-");
		if(this.validateYear(yearMonthDay[0])
				&& this.validateMonth(yearMonthDay[1])
				&& this.validateDay(yearMonthDay[2])) {
			return true;			
		} else {
			errorString += dateFormatErrorMessage;
			return false;
		}*/
	}
}
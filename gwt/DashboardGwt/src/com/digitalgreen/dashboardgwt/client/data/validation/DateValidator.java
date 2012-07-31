package com.digitalgreen.dashboardgwt.client.data.validation;


import java.util.Date;
import com.google.gwt.i18n.client.DateTimeFormat;

public class DateValidator extends BaseValidator {
	
	String key;
	
	public DateValidator(String value) {
		super(value);
	}

	public DateValidator(String childLabel, String value, boolean nullable, boolean blank) {
		super(value, nullable, blank);
		this.childLabel = childLabel;
	}
	
	@Override
	public boolean validate() {
		if (!super.validate()) {
			errorString += requiredFieldErrorMessage;
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
	}
}
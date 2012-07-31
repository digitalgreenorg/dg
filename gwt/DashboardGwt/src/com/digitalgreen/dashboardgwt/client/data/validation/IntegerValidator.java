package com.digitalgreen.dashboardgwt.client.data.validation;

import com.google.gwt.user.client.Window;

public class IntegerValidator extends BaseValidator {

	protected Integer minValue = null;
	protected Integer maxValue = null;
	protected int valueInt;

	public IntegerValidator(String value) {
		super(value);
	}

	public IntegerValidator(String childLabel, String value, boolean nullable, boolean blank) {
		super(value, nullable, blank);
		this.childLabel = childLabel;
	}

	public IntegerValidator(String childLabel, String value, boolean nullable, boolean blank,
			int minValue, int maxValue) {
		super(value, nullable, blank);
		this.maxValue = maxValue;
		this.minValue = minValue;
		this.childLabel = childLabel;
	}

	public int getValueInt() {
		return this.valueInt;
	}

	@Override
	public boolean validate() {
		if (!super.validate()) {
			errorString += requiredFieldErrorMessage;
			return false;
		} else if (this.getValue() == null) {
			return true;
		} else {
			try {
				this.valueInt = Integer.parseInt((String)this.getValue());
			} catch (NumberFormatException e) {
				errorString += integerErrorMessage;
				return false;
			}
			if ((this.minValue != null ? this.getValueInt() >= this.minValue: true) && (this.maxValue != null ? this.getValueInt() <= this.maxValue: true)) {
				return true;				
			} else {
				errorString += integerMaxMinErrorMessage+this.minValue+" and "+this.maxValue;
				return false;		
			}
		}
	}
}
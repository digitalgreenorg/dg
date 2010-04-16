package com.digitalgreen.dashboardgwt.client.data.validation;

public class PositiveIntegerValidator extends IntegerValidator {
	
	public PositiveIntegerValidator(String value) {
		super(value);
	}
	
	public PositiveIntegerValidator(String value, boolean nullable, boolean blank) {
		super(value, nullable, blank);
	}
	
	public PositiveIntegerValidator(String value, boolean nullable, boolean blank,
			int minValue, int maxValue) {
		super(value, nullable, blank, minValue, maxValue);
	}
	
	@Override
	public boolean validate() {
		return super.validate() && this.getValueInt() >= 0;
	}
}
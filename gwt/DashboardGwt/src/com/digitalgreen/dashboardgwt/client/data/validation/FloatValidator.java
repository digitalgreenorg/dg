package com.digitalgreen.dashboardgwt.client.data.validation;

public class FloatValidator extends BaseValidator {

	public FloatValidator(String value) {
		super(value);
	}
	
	public FloatValidator(String value, boolean nullable, boolean blank) {
		super(value, nullable, blank);
	}
	
	@Override
	public boolean validate() {
		try {
			float checkFormat = Float.parseFloat(this.getValue());
		} catch (NumberFormatException e) {
			return false;
		}
		return super.validate();
	}
}
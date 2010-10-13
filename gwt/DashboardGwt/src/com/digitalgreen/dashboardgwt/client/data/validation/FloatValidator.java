package com.digitalgreen.dashboardgwt.client.data.validation;


public class FloatValidator extends BaseValidator {

	public FloatValidator(String value) {
		super(value);
	}

	public FloatValidator(String childLabel, String value, boolean nullable, boolean blank) {
		super(value, nullable, blank);
		this.childLabel = childLabel;
	}

	@Override
	public boolean validate() {
		if(!super.validate()){
			errorString += reqiuredFieldErrorMessage; 
			return false;
		} else if (this.getValue() == null) {
			return true;
		} else {
			try {
				float checkFormat = Float.parseFloat((String)this.getValue());
			} catch (NumberFormatException e) {
				errorString += floatFormatErrorMessage ;
				return false;
			}
			return true;
		}
	}
}
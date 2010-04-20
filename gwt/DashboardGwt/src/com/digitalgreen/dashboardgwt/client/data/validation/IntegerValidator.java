package com.digitalgreen.dashboardgwt.client.data.validation;

import com.google.gwt.user.client.Window;

public class IntegerValidator extends BaseValidator {

	private Integer minValue = null;
	private Integer maxValue = null;
	private int valueInt;

	public IntegerValidator(String value) {
		super(value);
	}

	public IntegerValidator(String value, boolean nullable, boolean blank) {
		super(value, nullable, blank);
	}

	public IntegerValidator(String value, boolean nullable, boolean blank,
			int minValue, int maxValue) {
		super(value, nullable, blank);
	}

	public int getValueInt() {
		return this.valueInt;
	}

	@Override
	public boolean validate() {
		if (!super.validate()) {
			Window.alert("exp valueInt: " + valueInt);
			return false;
		} else if (this.getValue() == null) {
			return true;
		} else {
			try {
				this.valueInt = Integer.parseInt((String)this.getValue());
			} catch (NumberFormatException e) {
				return false;
			}

			return (this.minValue != null ? ((String)this.getValue()).length() >= this.minValue.toString().length(): true 
					&& this.maxValue != null ? ((String)this.getValue()).length() <= this.maxValue.toString().length(): true);
		}
	}
}
package com.digitalgreen.dashboardgwt.client.data.validation;

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
		try {
			this.valueInt = Integer.parseInt(this.getValue());
		} catch(NumberFormatException e) {
			return false;
		}
		
		return (super.validate() && 
				this.minValue != null ? this.getValue().length() >= this.minValue.toString().length() : true && 
				this.maxValue != null ? this.getValue().length() <= this.maxValue.toString().length() : true);
	}
	
}
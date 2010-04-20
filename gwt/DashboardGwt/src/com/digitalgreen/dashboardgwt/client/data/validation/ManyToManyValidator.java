package com.digitalgreen.dashboardgwt.client.data.validation;

import java.util.ArrayList;

public class ManyToManyValidator extends BaseValidator {
	
	// Override this
	public ManyToManyValidator(ArrayList value) {
		super(value);
	}

	public ManyToManyValidator(ArrayList value, boolean nullable) {
		super(value, nullable);
	}
	
	@Override
	public boolean validate() {
		if(!this.isNullable() && (this.getValue() == null || 
				(this.getValue() instanceof ArrayList && 
				((ArrayList)this.getValue()).isEmpty()))) {
			return false;
		}
		return true;
	}
}
package com.digitalgreen.dashboardgwt.client.data.validation;

import org.junit.Test;

import com.google.gwt.junit.client.GWTTestCase;

public class DateValidatorTest extends GWTTestCase {

	@Test
	public void test() {
		DateValidator dateValidator = new DateValidator("2012-12-06");
		assertEquals(dateValidator.validate(), true);
		// Correct Date, Zeros missing - should parse.
		dateValidator = new DateValidator("2012-04-6");
		assertEquals(dateValidator.validate(), true);
		dateValidator = new DateValidator("2012-4-06");
		assertEquals(dateValidator.validate(), true);
		// Spaces
		dateValidator = new DateValidator("2011-11- 26");
		assertEquals(dateValidator.validate(), true);
		
		// Month Incorrect
		dateValidator = new DateValidator("2012-14-06");
		assertEquals(dateValidator.validate(), false);
		// Year Incorrect
		dateValidator = new DateValidator("2012-12-36");
		assertEquals(dateValidator.validate(), false);
		// Format incorrect
		dateValidator = new DateValidator("7-4-2012");
		assertEquals(dateValidator.validate(), false);
		// Semi-colon added
		dateValidator = new DateValidator("2012-04-06;");
		assertEquals(dateValidator.validate(), false);

	}

	@Override
	public String getModuleName() {
		return "com.digitalgreen.dashboardgwt.DashboardGwt";
	}

}

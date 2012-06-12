package com.digitalgreen.dashboardgwt.client.data.validation;

import org.junit.Test;

import com.google.gwt.junit.client.GWTTestCase;

public class TimeValidatorTest extends GWTTestCase {

	@Test
	public void test() {
		TimeValidator timeValidator = new TimeValidator("12:23:12");
		assertEquals(timeValidator.validate(), true);
		timeValidator = new TimeValidator("16:60:00");
		assertEquals(timeValidator.validate(), false);
	}

	@Override
	public String getModuleName() {
		return "com.digitalgreen.dashboardgwt.DashboardGwt";
	}

}

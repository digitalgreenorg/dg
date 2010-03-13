package com.digitalgreen.dashboardgwt.client.common;

import com.google.gwt.user.client.Cookies;

public class ApplicationConstants {
	
	private static boolean isOnline = true;
	
	public static String digitalgreenDatabaseName = "digitalgreen";
	
	public static String getUsernameCookie() {
		return Cookies.getCookie("username");
	}
	
	public static void setUsernameCookie(String username) {
		Cookies.setCookie("username", username);
	}
	
	public static String getPasswordCookie() {
		return Cookies.getCookie("password");
	}
	
	public static void setPasswordCookie(String password) {
		Cookies.setCookie("password", password);
	}
	
	public static void deleteCookies() {
		Cookies.removeCookie("username");
		Cookies.removeCookie("password");
	}
	
	public static void setLoginCookies(String username, String password) {
		ApplicationConstants.setUsernameCookie(username);
		ApplicationConstants.setPasswordCookie(password);
	}
	
	public static void toggleConnection(boolean isOnline) {
		ApplicationConstants.isOnline = isOnline;
	}
	
	public static boolean getCurrentOnlineStatus() {
		return ApplicationConstants.isOnline;
	}
	
	public static String getDatabaseName() {
		return ApplicationConstants.digitalgreenDatabaseName;
	}
}
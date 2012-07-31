package com.digitalgreen.dashboardgwt.client.common;

import java.util.HashMap;

import com.digitalgreen.dashboardgwt.client.data.AnimatorAssignedVillagesData;
import com.digitalgreen.dashboardgwt.client.data.AnimatorSalaryPerMonthData;
import com.digitalgreen.dashboardgwt.client.data.AnimatorsData;
import com.digitalgreen.dashboardgwt.client.data.BlocksData;
import com.digitalgreen.dashboardgwt.client.data.CountriesData;
import com.digitalgreen.dashboardgwt.client.data.DevelopmentManagersData;
import com.digitalgreen.dashboardgwt.client.data.DistrictsData;
import com.digitalgreen.dashboardgwt.client.data.EquipmentHoldersData;
import com.digitalgreen.dashboardgwt.client.data.EquipmentsData;
import com.digitalgreen.dashboardgwt.client.data.FieldOfficersData;
import com.digitalgreen.dashboardgwt.client.data.LanguagesData;
import com.digitalgreen.dashboardgwt.client.data.MonthlyCostPerVillageData;
import com.digitalgreen.dashboardgwt.client.data.PartnersData;
import com.digitalgreen.dashboardgwt.client.data.PersonAdoptPracticeData;
import com.digitalgreen.dashboardgwt.client.data.PersonGroupsData;
import com.digitalgreen.dashboardgwt.client.data.PersonMeetingAttendanceData;
import com.digitalgreen.dashboardgwt.client.data.PersonRelationsData;
import com.digitalgreen.dashboardgwt.client.data.PersonsData;
import com.digitalgreen.dashboardgwt.client.data.PracticesData;
import com.digitalgreen.dashboardgwt.client.data.RegionsData;
import com.digitalgreen.dashboardgwt.client.data.ReviewersData;
import com.digitalgreen.dashboardgwt.client.data.ScreeningFarmerGroupsTargetedData;
import com.digitalgreen.dashboardgwt.client.data.ScreeningVideosScreenedData;
import com.digitalgreen.dashboardgwt.client.data.ScreeningsData;
import com.digitalgreen.dashboardgwt.client.data.StatesData;
import com.digitalgreen.dashboardgwt.client.data.TargetsData;
import com.digitalgreen.dashboardgwt.client.data.TrainingAnimatorsTrainedData;
import com.digitalgreen.dashboardgwt.client.data.TrainingsData;
import com.digitalgreen.dashboardgwt.client.data.VideoFarmersShownData;
import com.digitalgreen.dashboardgwt.client.data.VideoRelatedAgriculturalPracticesData;
import com.digitalgreen.dashboardgwt.client.data.VideosData;
import com.digitalgreen.dashboardgwt.client.data.VillagesData;
import com.google.gwt.user.client.Cookies;

public class ApplicationConstants {
	
	private static boolean isOnline = true;
	
	public static String digitalgreenDatabaseName = "digitalgreendatabase";
	
	public static String[] tableIDs = {	"7","8","9","10","11","12","13",
										"14","15","16", "17","18", "19","20","21",
										"22","23","37","24", "25","26", "28","27",
										"38","39","29","40","41","30","31","34","42"};

	public static HashMap mappingBetweenTableIDAndDataObject;
	
	public final static int PAGESIZE = 3000;
	
	//Below Constants and their getter methods are for pagination
	public final static int pageSize = 100;
	//Maximum number of pages in single horizontal row is 49
	public final static int maxPagesToDisplayPerRow = 49;
	
	public static int getPageSize() {
		return ApplicationConstants.pageSize;
	}
	
	public static int getMaxPagesToDisplayPerRow() {
		return ApplicationConstants.maxPagesToDisplayPerRow;
	}
	
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
	
	public static String getUserRoleCookie() {
		return Cookies.getCookie("userrole");
	}
	
	public static void setUserRoleCookie(String userrole) {
		Cookies.setCookie("userrole", userrole);
	}
	
	public static void deleteCookies() {
		Cookies.removeCookie("username");
		Cookies.removeCookie("password");
		Cookies.removeCookie("userrole");
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
	
	@SuppressWarnings("unchecked")
	public static void createMappingBetweenTableIDAndDataObject(){
		mappingBetweenTableIDAndDataObject = new HashMap();
		CountriesData countriesData  = new CountriesData();
		mappingBetweenTableIDAndDataObject.put(CountriesData.tableID, countriesData);
		RegionsData regionsData  = new RegionsData();
		mappingBetweenTableIDAndDataObject.put(RegionsData.tableID, regionsData);
		EquipmentHoldersData equipmentHoldersData= new EquipmentHoldersData();
		mappingBetweenTableIDAndDataObject.put(EquipmentHoldersData.tableID, equipmentHoldersData);
		ReviewersData reviewersData = new ReviewersData();
		mappingBetweenTableIDAndDataObject.put(ReviewersData.tableID, reviewersData);
		DevelopmentManagersData developmentManagersData = new DevelopmentManagersData();
		mappingBetweenTableIDAndDataObject.put(DevelopmentManagersData.tableID, developmentManagersData);
		StatesData statesData = new StatesData();
		mappingBetweenTableIDAndDataObject.put(StatesData.tableID, statesData);
		PartnersData partnersData = new PartnersData();
		mappingBetweenTableIDAndDataObject.put(PartnersData.tableID, partnersData);
		FieldOfficersData fieldOfficersData = new FieldOfficersData();
		mappingBetweenTableIDAndDataObject.put(FieldOfficersData.tableID, fieldOfficersData);
		DistrictsData districtsData = new DistrictsData();
		mappingBetweenTableIDAndDataObject.put(DistrictsData.tableID, districtsData);
		BlocksData blocksData = new BlocksData();
		mappingBetweenTableIDAndDataObject.put(BlocksData.tableID, blocksData);
		VillagesData villagesData = new VillagesData();
		mappingBetweenTableIDAndDataObject.put(VillagesData.tableID, villagesData);
		MonthlyCostPerVillageData monthlyCostPerVillageData = new MonthlyCostPerVillageData();
		mappingBetweenTableIDAndDataObject.put(MonthlyCostPerVillageData.tableID, monthlyCostPerVillageData);
		PersonGroupsData personGroupsData = new PersonGroupsData();
		mappingBetweenTableIDAndDataObject.put(PersonGroupsData.tableID, personGroupsData);
		PersonsData personsData = new PersonsData();
		mappingBetweenTableIDAndDataObject.put(PersonsData.tableID, personsData);
		PersonRelationsData personRelationsData = new PersonRelationsData();
		mappingBetweenTableIDAndDataObject.put(PersonRelationsData.tableID, personRelationsData);
		AnimatorsData animatorsData = new AnimatorsData();
		mappingBetweenTableIDAndDataObject.put(AnimatorsData.tableID, animatorsData);
		TrainingsData trainingsData = new TrainingsData();
		mappingBetweenTableIDAndDataObject.put(TrainingsData.tableID, trainingsData);
		TrainingAnimatorsTrainedData trainingAnimatorsTrainedData = new TrainingAnimatorsTrainedData();
		mappingBetweenTableIDAndDataObject.put(TrainingAnimatorsTrainedData.tableID, trainingAnimatorsTrainedData);
		AnimatorAssignedVillagesData animatorAssignedVillagesData = new AnimatorAssignedVillagesData();
		mappingBetweenTableIDAndDataObject.put(AnimatorAssignedVillagesData.tableID, animatorAssignedVillagesData);
		AnimatorSalaryPerMonthData animatorSalaryPerMonthData = new AnimatorSalaryPerMonthData();
		mappingBetweenTableIDAndDataObject.put(AnimatorSalaryPerMonthData.tableID, animatorSalaryPerMonthData);
		LanguagesData languagesData = new LanguagesData();
		mappingBetweenTableIDAndDataObject.put(LanguagesData.tableID, languagesData);
		PracticesData practicesData = new PracticesData();
		mappingBetweenTableIDAndDataObject.put(PracticesData.tableID, practicesData);
		VideosData videosData = new VideosData();
		mappingBetweenTableIDAndDataObject.put(VideosData.tableID, videosData);
		VideoRelatedAgriculturalPracticesData videoRelatedAgriculturalPracticesData = new VideoRelatedAgriculturalPracticesData();
		mappingBetweenTableIDAndDataObject.put(VideoRelatedAgriculturalPracticesData.tableID, videoRelatedAgriculturalPracticesData);
		VideoFarmersShownData videoFarmersShownData = new VideoFarmersShownData();
		mappingBetweenTableIDAndDataObject.put(VideoFarmersShownData.tableID, videoFarmersShownData);
		ScreeningsData screeningsData = new ScreeningsData();
		mappingBetweenTableIDAndDataObject.put(ScreeningsData.tableID, screeningsData);
		ScreeningFarmerGroupsTargetedData screeningFarmerGroupsTargetedData = new ScreeningFarmerGroupsTargetedData();
		mappingBetweenTableIDAndDataObject.put(ScreeningFarmerGroupsTargetedData.tableID, screeningFarmerGroupsTargetedData);
		ScreeningVideosScreenedData screeningVideosScreenedData = new ScreeningVideosScreenedData();
		mappingBetweenTableIDAndDataObject.put(ScreeningVideosScreenedData.tableID, screeningVideosScreenedData);
		PersonMeetingAttendanceData personMeetingAttendanceData = new PersonMeetingAttendanceData();
		mappingBetweenTableIDAndDataObject.put(PersonMeetingAttendanceData.tableID, personMeetingAttendanceData);
		PersonAdoptPracticeData personAdoptPracticeData = new PersonAdoptPracticeData();
		mappingBetweenTableIDAndDataObject.put(PersonAdoptPracticeData.tableID, personAdoptPracticeData);
		EquipmentsData equipmentsData = new EquipmentsData();
		mappingBetweenTableIDAndDataObject.put(EquipmentsData.tableID, equipmentsData);
		TargetsData targetsData = new TargetsData();
		mappingBetweenTableIDAndDataObject.put(TargetsData.tableID, targetsData);
	}
		
}
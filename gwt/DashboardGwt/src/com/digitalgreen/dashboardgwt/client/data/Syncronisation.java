package com.digitalgreen.dashboardgwt.client.data;

import java.util.HashMap;

import com.digitalgreen.dashboardgwt.client.common.ApplicationConstants;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.servlets.BaseServlet;
import com.digitalgreen.dashboardgwt.client.servlets.Index;
import com.google.gwt.gears.client.database.DatabaseException;
import com.google.gwt.user.client.Window;

public class Syncronisation {
	
	public Syncronisation(){	
	}
	
	@SuppressWarnings("unchecked")
	protected HashMap mapping;
	private FormQueueData formQueue;
	private int lastSyncedId;
	private String setGlobalKeyURL = "/dashboard/setkey/";
	private BaseServlet servlet;
	
	public void syncFromLocalToMain(BaseServlet servlet){
		this.servlet = servlet;
		createMappingBetweenTableAndTableID();
		formQueue = new FormQueueData(new OnlineOfflineCallbacks(servlet) {
			public void onlineSuccessCallback(String results) {
				if(results == "1") {
						updateSyncStatusOfLastSyncedRow();
						if(!postRowOfFormQueueTable()){
								updateGlobalPkIDOnMainServer();
						}
				} else if(results =="0") {
					RequestContext requestContext = new RequestContext();
					requestContext.setMessageString("Validation Error : Form cannot be verified on the main server");
					getServlet().redirectTo(new Index(requestContext));		
				}else if(results=="synced"){
					setGlobalIDInLocalUserTable();
				}
				else{
					Window.alert("Unkown Error!");
				}
			}
			
			public void onlineErrorCallback(int errorCode) {
				Window.alert("GOT AN ERROR connecting to server");
				RequestContext requestContext = new RequestContext();
				if (errorCode == BaseData.ERROR_RESPONSE)
					requestContext.setMessageString("Unresponsive Server.  Please contact support.");
				else if (errorCode == BaseData.ERROR_SERVER)
					requestContext.setMessageString("Problem in the connection with the server.");
				else
					requestContext.setMessageString("Unknown error.  Please contact support.");
				getServlet().redirectTo(new Index(requestContext));	
			}
		});
		
		if(!postRowOfFormQueueTable()){
			RequestContext requestContext = new RequestContext();
			requestContext.setMessageString("Local database is in sync with the main server ");
			servlet.redirectTo(new Index(requestContext));
		}
	}
	
	public Boolean postRowOfFormQueueTable(){
		BaseData.dbOpen();
		formQueue.select(FormQueueData.getUnsyncTableRow);
		if(formQueue.getResultSet().isValidRow()){
			try {
				if(formQueue.getResultSet().getFieldAsInt(3) == 0){
					String queryString = "id="+formQueue.getResultSet().getFieldAsString(1)+"&"+formQueue.getResultSet().getFieldAsString(2);
					if(formQueue.getResultSet().getFieldAsChar(4) == 'A'){
						lastSyncedId  = formQueue.getResultSet().getFieldAsInt(1);
						formQueue.post(RequestContext.SERVER_HOST + (String)mapping.get(formQueue.getResultSet().getFieldAsString(0)), queryString);
						BaseData.dbClose();
					}
					else{
						// Take care of edit case
					}
						
				}
			} catch(DatabaseException e){
				Window.alert("Database Exception : " + e.toString());
				BaseData.dbClose();
			}
			return true;
		}
		else{
			return false;
		}
	}
	
	public void updateSyncStatusOfLastSyncedRow(){
		formQueue.update(FormQueueData.updateSyncStatusOfARow, ""+lastSyncedId);
	}
	
	public void updateGlobalPkIDOnMainServer(){
		String queryString = "id="+this.lastSyncedId+"&username="+ApplicationConstants.getUsernameCookie();
		formQueue.post(this.setGlobalKeyURL, queryString);
	}
	
	private void setGlobalIDInLocalUserTable(){
		IndexData indexData = new IndexData(new OnlineOfflineCallbacks(this.servlet) {
			public void onlineSuccessCallback(String results) {
				if(results != "0") {
					LoginData user = new LoginData();
					user.update(results, "1", "0", ApplicationConstants.getUsernameCookie(), ApplicationConstants.getPasswordCookie());
					RequestContext requestContext = new RequestContext();
					requestContext.setMessageString("Local database is in sync with the main server");
					getServlet().redirectTo(new Index(requestContext));
				} else {
					RequestContext requestContext = new RequestContext();
					requestContext.setMessageString("You do not have a valid account.Please contact support. ");
					getServlet().redirectTo(new Index(requestContext));				
				}
			}
			
			public void onlineErrorCallback(int errorCode) {
				Window.alert("GOT AN ERROR connecting to server");
				RequestContext requestContext = new RequestContext();
				if (errorCode == BaseData.ERROR_RESPONSE)
					requestContext.setMessageString("Unresponsive Server.  Please contact support.");
				else if (errorCode == BaseData.ERROR_SERVER)
					requestContext.setMessageString("Problem in the connection with the server.");
				else
					requestContext.setMessageString("Unknown error.  Please contact support.");
				getServlet().redirectTo(new Index(requestContext));	
			}
			
		});
		
		indexData.apply(indexData.getGlobalPrimaryKey(ApplicationConstants.getUsernameCookie()));
		
	}
	@SuppressWarnings("unchecked")
	public void createMappingBetweenTableAndTableID(){
		mapping = new HashMap();
		mapping.put(RegionsData.tableID, RegionsData.saveRegionOfflineURL); 
		mapping.put(EquipmentHoldersData.tableID, EquipmentHoldersData.saveEquipmentHolderOfflineURL);
		mapping.put(ReviewersData.tableID, ReviewersData.saveReviewerOfflineURL);
		mapping.put(DevelopmentManagersData.tableID, DevelopmentManagersData.saveDevelopmentManagerOfflineURL);
		mapping.put(StatesData.tableID, StatesData.saveStateOfflineURL);
		mapping.put(PartnersData.tableID, PartnersData.savePartnerOfflineURL);
		mapping.put(FieldOfficersData.tableID, FieldOfficersData.saveFieldOfficerOfflineURL);
		mapping.put(DistrictsData.tableID, DistrictsData.saveDistrictOfflineURL);
		mapping.put(BlocksData.tableID, BlocksData.saveBlockOfflineURL);
		mapping.put(VillagesData.tableID, VillagesData.saveVillageOfflineURL);
		mapping.put(MonthlyCostPerVillageData.tableID, MonthlyCostPerVillageData.saveMonthlyCostPerVillageOfflineURL);
		mapping.put(PersonGroupsData.tableID, PersonGroupsData.savePersonGroupOfflineURL);
		mapping.put(PersonsData.tableID, PersonsData.savePersonOfflineURL);
		mapping.put(PersonRelationsData.tableID, PersonRelationsData.savePersonRelationOfflineURL);
		mapping.put(AnimatorsData.tableID, AnimatorsData.saveAnimatorOfflineURL);
		mapping.put(TrainingsData.tableID, TrainingsData.saveTrainingOfflineURL);
		mapping.put(TrainingAnimatorsTrainedData.tableID, TrainingAnimatorsTrainedData.saveTrainingAnimatorsTrainedOfflineURL);
		mapping.put(AnimatorAssignedVillagesData.tableID, AnimatorAssignedVillagesData.saveAnimatorAssignedVillageOfflineURL);
		mapping.put(AnimatorSalaryPerMonthData.tableID, AnimatorSalaryPerMonthData.saveAnimatorSalaryPerMonthOfflineURL);
		mapping.put(LanguagesData.tableID, LanguagesData.saveLanguageOfflineURL);
		mapping.put(PracticesData.tableID, PracticesData.savePracticeOfflineURL);
		mapping.put(VideosData.tableID, VideosData.saveVideoOfflineURL);
		mapping.put(VideoRelatedAgriculturalPracticesData.tableID, VideoRelatedAgriculturalPracticesData.saveVideoRelatedAgriculturalPracticeOfflineURL);
		mapping.put(VideoFarmersShownData.tableID, VideoFarmersShownData.saveVideoFarmerOfflineURL);
		mapping.put(ScreeningsData.tableID, ScreeningsData.saveScreeningOfflineURL);
		mapping.put(ScreeningFarmerGroupsTargetedData.tableID, ScreeningFarmerGroupsTargetedData.saveScreeningFarmerGroupsTargetedOfflineURL);
		mapping.put(ScreeningVideosScreenedData.tableID, ScreeningVideosScreenedData.saveScreeningVideosScreenedOfflineURL);
		mapping.put(PersonMeetingAttendanceData.tableID, PersonMeetingAttendanceData.savePersonMeetingAttendanceOfflineURL);
		mapping.put(PersonAdoptPracticeData.tableID, PersonAdoptPracticeData.savePersonAdoptPracticeOfflineURL);
		mapping.put(EquipmentsData.tableID, EquipmentsData.saveEquipmentOfflineURL);
	}
}
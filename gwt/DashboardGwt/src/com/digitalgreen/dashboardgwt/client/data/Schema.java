package com.digitalgreen.dashboardgwt.client.data;

import com.google.gwt.gears.client.database.DatabaseException;
import com.google.gwt.user.client.Window;

public class Schema {
	
	
	
	public static void createSchema() {
		try {
			
			BaseData.dbOpen();
			BaseData.dbStartTransaction();
			BaseData.getDb().execute(RegionsData.createTable);
			BaseData.getDb().execute(EquipmentHoldersData.createTable);
			BaseData.getDb().execute(ReviewersData.createTable);
			BaseData.getDb().execute(DevelopmentManagersData.createTable);
			BaseData.getDb().execute(StatesData.createTable);
			BaseData.getDb().execute(PartnersData.createTable);
			BaseData.getDb().execute(FieldOfficersData.createTable);
			BaseData.getDb().execute(DistrictsData.createTable);
			BaseData.getDb().execute(BlocksData.createTable);
			BaseData.getDb().execute(VillagesData.createTable);
			BaseData.getDb().execute(MonthlyCostPerVillageData.createTable);
			BaseData.getDb().execute(PersonGroupsData.createTable);
			BaseData.getDb().execute(PersonsData.createTable);
			BaseData.getDb().execute(PersonRelationsData.createTable);
			BaseData.getDb().execute(AnimatorsData.createTable);
			BaseData.getDb().execute(TrainingsData.createTable);
			BaseData.getDb().execute(TrainingAnimatorsTrainedData.createTable);
			BaseData.getDb().execute(AnimatorAssignedVillagesData.createTable);
			BaseData.getDb().execute(AnimatorSalaryPerMonthData.createTable);
			BaseData.getDb().execute(LanguagesData.createTable);
			BaseData.getDb().execute(PracticesData.createTable);
			BaseData.getDb().execute(VideosData.createTable);
			BaseData.getDb().execute(VideoRelatedAgriculturalPracticesData.createTable);
			BaseData.getDb().execute(VideoFarmersShownData.createTable);
			BaseData.getDb().execute(ScreeningsData.createTable);
			BaseData.getDb().execute(ScreeningFarmerGroupsTargetedData.createTable);
			BaseData.getDb().execute(ScreeningVideosScreenedData.createTable);
			BaseData.getDb().execute(PersonMeetingAttendanceData.createTable);
			BaseData.getDb().execute(PersonAdoptPracticeData.createTable);
			BaseData.getDb().execute(EquipmentsData.createTable);
			BaseData.getDb().execute(LoginData.createTable);
			BaseData.getDb().execute(FormQueueData.createTable);
			BaseData.dbCommit();
			BaseData.dbClose();
		} catch (DatabaseException e) {
			Window.alert("Database Exception : Error in creating the tables");
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	public static void dropSchema() {}
}
package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;
import java.util.List;
import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.google.gwt.core.client.JsArray;
import com.google.gwt.gears.client.database.DatabaseException;
import com.google.gwt.user.client.Window;

public class TrainingsData extends BaseData {
	
	public static class Type extends BaseData.Type {
		protected Type() {}
		public final native String getTrainigPurpose() /*-{ return $wnd.checkForNullValues(this.fields.trainig_purpose); }-*/;
		public final native String getTrainingOutcome() /*-{ return $wnd.checkForNullValues(this.fields.training_outcome); }-*/;
		public final native String getTrainingStartDate() /*-{ return $wnd.checkForNullValues(this.fields.trainig_start_date); }-*/;
		public final native String getTrainingEndDate() /*-{ return $wnd.checkForNullValues(this.fields.trainig_end_date); }-*/;
		public final native VillagesData.Type getVillage() /*-{ return this.fields.village; }-*/;
		public final native DevelopmentManagersData.Type getDevelopmentManager() /*-{ return this.fields.developmentmanager }-*/;
		public final native FieldOfficersData.Type getFieldOfficer() /*-{ return this.fields.fieldofficer; }-*/;
	}
	
	public class Data extends BaseData.Data {
		
		final private String COLLECTION_PREFIX = "training";
		
		private String training_purpose;
		private String training_outcome;
		private String training_start_date;
		private String training_end_date;
		private VillagesData.Data village;
		private DevelopmentManagersData.Data developmentmanager;
		private FieldOfficersData.Data fieldofficer;
		
		public Data(){
			super();
		}
		
		public Data(String id, String training_purpose, String training_outcome, String training_start_date, String training_end_date, 
				VillagesData.Data village, DevelopmentManagersData.Data developmentmanager, FieldOfficersData.Data fieldofficer ){
			super();
			this.id = id;
			this.training_purpose = training_purpose;
			this.training_outcome = training_outcome;
			this.training_start_date = training_start_date;
			this.training_end_date = training_end_date;
			this.village = village;
			this.developmentmanager = developmentmanager;
			this.fieldofficer = fieldofficer;
		}
		
		public Data(String id, String training_purpose, String training_outcome){
			super();
			this.id = id;
			this.training_purpose = training_purpose;
			this.training_outcome = training_outcome;
		}
		
		public String getTrainigPurpose() { 
			return this.training_purpose; 
		}
		
		public String getTrainingOutcome() { 
			return this.training_outcome; 
		}
		
		public String getTrainingStartDate() { 
			return this.training_start_date; 
		}
		
		public String getTrainingEndDate() { 
			return this.training_end_date; 
		}
		
		public VillagesData.Data getVillage(){
			return this.village;
		}
		
		public DevelopmentManagersData.Data getDevelopmentManager(){
			return this.developmentmanager;
		}
		
		public FieldOfficersData.Data getFieldOfficer(){
			return this.fieldofficer;
		}
		
		@Override
		public BaseData.Data clone(){
			Data obj = new Data();
			obj.id = this.id;
			obj.training_purpose = this.training_purpose;
			obj.training_outcome = this.training_outcome;
			obj.training_start_date = this.training_start_date;
			obj.training_end_date = this.training_end_date;
			obj.village = (VillagesData.Data)this.village.clone();
			obj.developmentmanager = (DevelopmentManagersData.Data)this.developmentmanager.clone();
			obj.fieldofficer = (FieldOfficersData.Data)this.fieldofficer.clone();
			return obj;
		}
		
		@Override
		public String getPrefixName(){
			return this.COLLECTION_PREFIX;
		}
		
		@Override
		public void setObjValueFromString(String key, String val) {
			super.setObjValueFromString(key, val);
			if(key.equals("id")) {
				this.id = val;
			}
			else if(key.equals("training_purpose")){
				this.training_purpose = (String)val;
			}
			else if(key.equals("training_outcome")){
				this.training_outcome = (String)val;
			}
			else if(key.equals("training_start_date")){
				this.training_start_date = (String)val;
			}
			else if(key.equals("training_end_date")){
				this.training_end_date = (String)val;
			}
			else if(key.equals("village")){
				VillagesData village1 = new VillagesData();
				this.village = village1.getNewData();
				this.village.id = val;
			}
			else if(key.equals("developmentmanager")){
				DevelopmentManagersData developmentmanager1 = new DevelopmentManagersData();
				this.developmentmanager = developmentmanager1.getNewData();
				this.developmentmanager.id = val;
			}
			else if(key.equals("fieldofficer")){
				FieldOfficersData fieldofficer1 = new FieldOfficersData();
				this.fieldofficer = fieldofficer1.getNewData();
				this.fieldofficer.id = val;
			}
		}
		
		@Override
		public void save(){
			TrainingsData trainingsDataDbApis = new TrainingsData();
			if(this.id == null){
				this.id = trainingsDataDbApis.autoInsert(this.training_purpose, this.training_outcome, this.training_start_date, 
						this.training_end_date, Integer.valueOf(this.village.getId()).toString(),
						Integer.valueOf(this.developmentmanager.getId()).toString(), Integer.valueOf(this.fieldofficer.getId()).toString());
			}else{
				this.id = trainingsDataDbApis.autoInsert(Integer.valueOf(this.id).toString(), this.training_purpose, this.training_outcome, this.training_start_date, 
						this.training_end_date, Integer.valueOf(this.village.getId()).toString(),
						Integer.valueOf(this.developmentmanager.getId()).toString(), Integer.valueOf(this.fieldofficer.getId()).toString());
			}
			
		}
	}

	protected static String tableID = "16";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `training` " +
												"(id INTEGER PRIMARY KEY  NOT NULL ," +
												"TRAINING_PURPOSE TEXT  NOT NULL ," +
												"TRAINING_OUTCOME TEXT  NOT NULL ," +
												"TRAINING_START_DATE DATE  NULL DEFAULT NULL," +
												"TRAINING_END_DATE DATE  NULL DEFAULT NULL," +
												"village_id INT  NOT NULL DEFAULT 0," +
												"dm_id INT  NOT NULL DEFAULT 0," +
												"fieldofficer_id INT  NOT NULL DEFAULT 0, " +
												"FOREIGN KEY(village_id) REFERENCES village(id), " +
												"FOREIGN KEY(dm_id) REFERENCES development_manager(id), " +
												"FOREIGN KEY(fieldofficer_id) REFERENCES field_officer(id));" ;  
	protected static String selectTrainings = "SELECT id, TRAINING_PURPOSE, TRAINING_OUTCOME, TRAINING_START_DATE, TRAINING_END_DATE FROM training ORDER BY (id)";
	protected static String listTrainings = "SELECT training.id, training.training_purpose, training.training_outcome, training.training_start_date, training.training_end_date, village.id, village.village_name, development_manager.id, development_manager.name, field_officer.id, field_officer.name FROM training JOIN village ON training.village_id = village.id JOIN development_manager ON training.dm_id = development_manager.id JOIN field_officer ON training.fieldofficer_id = field_officer.id ORDER BY (training.id);";
	protected static String saveTrainingOnlineURL = "/dashboard/savetrainingonline/";
	protected static String getTrainingsOnlineURL = "/dashboard/gettrainingsonline/";
	protected static String saveTrainingOfflineURL = "/dashboard/savetrainingoffline/";
	protected String table_name = "training";
	protected String[] fields = {"id", "training_purpose", "training_outcome", "training_start_dat", "training_end_date", "village_id", "dm_id", "fieldofficer_id"};
	
	public TrainingsData() {
		super();
	}
	
	public TrainingsData(OnlineOfflineCallbacks callbacks) {
		super(callbacks);
	}
	
	public TrainingsData(OnlineOfflineCallbacks callbacks, Form form, String queryString) {
		super(callbacks, form, queryString);
	}
	
	@Override
	public Data getNewData() {
		return new Data();
	}
	
	@Override
	protected String getTableId() {
		return TrainingsData.tableID;
	}
	
	@Override
	protected String getTableName() {
		return this.table_name;
	}
	
	@Override 
	protected String[] getFields() {
		return this.fields;
	}
	
	@Override
	public String getListingOnlineURL(){
		return TrainingsData.getTrainingsOnlineURL;
	}

	
	public final native JsArray<Type> asArrayOfData(String json) /*-{
		return eval(json);
	}-*/;
	
	public List serialize(JsArray<Type> trainingObjects) {
		List trainings = new ArrayList();
		VillagesData village = new VillagesData();
		DevelopmentManagersData developmentmanager = new DevelopmentManagersData();
		FieldOfficersData fieldofficer = new FieldOfficersData();
		for(int i = 0; i < trainingObjects.length(); i++){
			
			VillagesData.Data v = village. new Data(trainingObjects.get(i).getVillage().getPk(), trainingObjects.get(i).getVillage().getVillageName());
			
			DevelopmentManagersData.Data dm = developmentmanager. new Data(trainingObjects.get(i).getDevelopmentManager().getPk(), trainingObjects.get(i).getDevelopmentManager().getName());
			
			FieldOfficersData.Data f = fieldofficer. new Data(trainingObjects.get(i).getFieldOfficer().getPk(), 
					trainingObjects.get(i).getFieldOfficer().getFieldOfficerName());
			
			Data training = new Data(trainingObjects.get(i).getPk(), trainingObjects.get(i).getTrainigPurpose(), 
					trainingObjects.get(i).getTrainingOutcome(), trainingObjects.get(i).getTrainingStartDate(), 
					trainingObjects.get(i).getTrainingEndDate(), v, dm, f);
			
			trainings.add(training);
		}
		return trainings;
	}
	
	@Override
	public List getListingOnline(String json){
		return this.serialize(this.asArrayOfData(json));
	}
	
	public List getTrainingsListingsOffline() {
		BaseData.dbOpen();
		List trainings = new ArrayList();
		VillagesData village = new VillagesData();
		DevelopmentManagersData developmentmanager = new DevelopmentManagersData();
		FieldOfficersData fieldofficer = new FieldOfficersData();
		this.select(listTrainings);
		if(this.getResultSet().isValidRow()){
			try {
				for (int i = 0; this.getResultSet().isValidRow(); ++i, this.getResultSet().next()) {
					
					VillagesData.Data v = village. new Data(this.getResultSet().getFieldAsString(5), this.getResultSet().getFieldAsString(6));
					
					DevelopmentManagersData.Data dm = developmentmanager. new Data(this.getResultSet().getFieldAsString(7), this.getResultSet().getFieldAsString(8));
					
					FieldOfficersData.Data f = fieldofficer. new Data(this.getResultSet().getFieldAsString(9), this.getResultSet().getFieldAsString(10));
					
					Data training = new Data(this.getResultSet().getFieldAsString(0), this.getResultSet().getFieldAsString(1), 
							this.getResultSet().getFieldAsString(2), this.getResultSet().getFieldAsString(3), 
							this.getResultSet().getFieldAsString(4), v, dm, f);
					
					trainings.add(training);					
				}
			}
			catch (DatabaseException e) {
				Window.alert("Database Exception : " + e.toString());
				BaseData.dbClose();
			}
		}
		BaseData.dbClose();
		return trainings;
	}
	
	public List getAllTrainingsOffline(){
		BaseData.dbOpen();
		List trainings = new ArrayList();
		this.select(selectTrainings);
		if(this.getResultSet().isValidRow()){
			try {
				for (int i = 0; this.getResultSet().isValidRow(); ++i, this.getResultSet().next()) {
					Data training = new Data(this.getResultSet().getFieldAsString(0), this.getResultSet().getFieldAsString(1), 
							this.getResultSet().getFieldAsString(2));
					trainings.add(training);
				}
			}
			catch (DatabaseException e) {
				Window.alert("Database Exception : " + e.toString());
				BaseData.dbClose();
			}
		}
		BaseData.dbClose();
		return trainings;
	}
	
	public List getTemplateDataOnline(String json){
		List relatedData = null;
		return relatedData;
	}
	
	public Object postPageData() {
		if(BaseData.isOnline()){
			this.post(RequestContext.SERVER_HOST + TrainingsData.saveTrainingOnlineURL, this.queryString);
		}
		else{
			this.save();
			return true;
		}
		return false;
	}
	
	public Object getListPageData(){
		if(BaseData.isOnline()){
			this.get(RequestContext.SERVER_HOST + TrainingsData.getTrainingsOnlineURL);
		}
		else{
			return true;
		}
		return false;
	}
	
	public String retrieveDataAndConvertResultIntoHtml() {
		VillagesData villageData = new VillagesData();
		List villages = villageData.getVillagesListingOffline();
		VillagesData.Data village;
		String htmlVillage = "<select name=\"state\" id=\"id_state\"";
		for(int i=0; i < villages.size(); i++){
			village = (VillagesData.Data)villages.get(i);
			htmlVillage = htmlVillage + "<option value=\"" + village.getId() + "\">" + village.getVillageName() + "</option>";
		}
		htmlVillage = htmlVillage + "</select>";
		
		DevelopmentManagersData developmentmanagerData = new DevelopmentManagersData();
		List developmentmanagers = developmentmanagerData.getDevelopmentManagersListingOffline();
		DevelopmentManagersData.Data developmentmanager;
		String htmlDevelopmentManager = "<select name=\"partner\" id=\"id_partner\"";
		for(int i = 0; i < developmentmanagers.size(); i++){
			developmentmanager = (DevelopmentManagersData.Data)developmentmanagers.get(i);
			htmlDevelopmentManager = htmlDevelopmentManager + "<option value=\"" + developmentmanager.getId() + "\">" + developmentmanager.getName() + "</option>";
		}

		FieldOfficersData fieldofficerData = new FieldOfficersData();
		List fieldofficers = fieldofficerData.getFieldOfficersListingOffline();
		FieldOfficersData.Data fieldofficer;
		String htmlFO = "<select name=\"fieldofficer\" id=\"id_fieldofficer\"";
		for(int i=0; i < fieldofficers.size(); i++){
			fieldofficer = (FieldOfficersData.Data)fieldofficers.get(i);
			htmlFO = htmlFO + "<option value=\"" + fieldofficer.getId() + "\">" + fieldofficer.getFieldOfficerName() + "</option>";
		}
		htmlFO = htmlFO + "</select>";

		return htmlVillage + htmlDevelopmentManager + htmlFO;
	}
	
	public Object getAddPageData() {
		if(BaseData.isOnline()) {
			this.get(RequestContext.SERVER_HOST + TrainingsData.saveTrainingOnlineURL);
		}
		else{
			return retrieveDataAndConvertResultIntoHtml();
		}
		return false;
	}
}
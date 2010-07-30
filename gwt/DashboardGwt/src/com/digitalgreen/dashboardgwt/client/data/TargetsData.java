package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.TrainingAnimatorsTrainedData.Data;
import com.digitalgreen.dashboardgwt.client.data.validation.DateValidator;
import com.digitalgreen.dashboardgwt.client.data.validation.IntegerValidator;
import com.digitalgreen.dashboardgwt.client.data.validation.ManyToManyValidator;
import com.digitalgreen.dashboardgwt.client.data.validation.StringValidator;
import com.digitalgreen.dashboardgwt.client.data.validation.UniqueConstraintValidator;
import com.google.gwt.core.client.JsArray;
import com.google.gwt.gears.client.database.DatabaseException;
import com.google.gwt.user.client.Window;

public class TargetsData extends BaseData {

	public static class Type extends BaseData.Type{
		protected Type() {}
		public final native DistrictsData.Type getDistrict() /*-{ return this.fields.district }-*/;
		public final native String getMonthYear() /*-{ return $wnd.checkForNullValues(this.fields.month_year); }-*/;
		public final native String getClustersIdentification() /*-{ return $wnd.checkForNullValues(this.fields.clusters_identification);}-*/;
		public final native String getDgConceptSharing() /*-{ return $wnd.checkForNullValues(this.fields.dg_concept_sharing); }-*/;
		public final native String getCspIdentification() /*-{ return this.fields.csp_identification; }-*/;
		public final native String getDisseminationSetDeployment() /*-{ return $wnd.checkForNullValues(this.fields.dissemination_set_deployment); }-*/;
		public final native String getVillageOperationalization()/*-{ return  $wnd.checkForNullValues(this.fields.village_operationalization); }-*/;
		public final native String getVideoUploading()/*-{ return  $wnd.checkForNullValues(this.fields.video_uploading); }-*/;
		public final native String getVideoProduction()/*-{ return  $wnd.checkForNullValues(this.fields.video_production); }-*/;
		public final native String getStoryboardPreparation()/*-{ return  $wnd.checkForNullValues(this.fields.storyboard_preparation); }-*/;
		public final native String getVideoShooting()/*-{ return  $wnd.checkForNullValues(this.fields.video_shooting); }-*/;
		public final native String getVideoEditing()/*-{ return  $wnd.checkForNullValues(this.fields.video_editing); }-*/;
		public final native String getVideoQualityChecking() /*-{ return $wnd.checkForNullValues(this.fields.video_quality_checking); }-*/;
		public final native String getDisseminations() /*-{ return $wnd.checkForNullValues(this.fields.disseminations); }-*/;
		public final native String getAvgAttendancePerDissemination()/*-{ return  $wnd.checkForNullValues(this.fields.avg_attendance_per_dissemination); }-*/;
		public final native String getExpInterestPerDissemination()/*-{ return  $wnd.checkForNullValues(this.fields.exp_interest_per_dissemination); }-*/;
		public final native String getAdoptionPerDissemination()/*-{ return  $wnd.checkForNullValues(this.fields.adoption_per_dissemination); }-*/;
		public final native String getCrpTraining()/*-{ return  $wnd.checkForNullValues(this.fields.crp_training); }-*/;
		public final native String getCrpRefresherTraining()/*-{ return  $wnd.checkForNullValues(this.fields.crp_refresher_training); }-*/;
		public final native String getCspTraining()/*-{ return  $wnd.checkForNullValues(this.fields.csp_training); }-*/;
		public final native String getCspRefresherTraining()/*-{ return  $wnd.checkForNullValues(this.fields.csp_refresher_training); }-*/;
		public final native String getEditorTraining()/*-{ return  $wnd.checkForNullValues(this.fields.editor_training); }-*/;
		public final native String getEditorRefresherTraining()/*-{ return  $wnd.checkForNullValues(this.fields.editor_refresher_training); }-*/;
		public final native String getVillagesCertification()/*-{ return  $wnd.checkForNullValues(this.fields.villages_certification); }-*/;
		public final native String getWhatWentWell()/*-{ return  $wnd.checkForNullValues(this.fields.what_went_well); }-*/;
		public final native String getWhatNotWentWell()/*-{ return  $wnd.checkForNullValues(this.fields.what_not_went_well); }-*/;
		public final native String getChallenges()/*-{ return  $wnd.checkForNullValues(this.fields.challenges); }-*/;
		public final native String getSupportRequested()/*-{ return  $wnd.checkForNullValues(this.fields.support_requested); }-*/;
		public final native String getLastModified()/*-{ return  $wnd.checkForNullValues(this.fields.last_modified); }-*/;
	}
	
	public class Data extends BaseData.Data {
				
		final private static String COLLECTION_PREFIX = "target";
		
		private DistrictsData.Data district; 
		private String month_year;   		
		private String clusters_identification;
	    private String dg_concept_sharing; 	    
	    private String csp_identification; 
	    private String dissemination_set_deployment; 
	    private String village_operationalization;
	    private String video_uploading;
	    private String video_production;
	    private String storyboard_preparation;
	    private String video_shooting; 
	    private String video_editing; 
		private String video_quality_checking; 
	    private String disseminations;
	    private String avg_attendance_per_dissemination;
	    private String exp_interest_per_dissemination; 
	    private String adoption_per_dissemination;
	    private String crp_training;
	    private String crp_refresher_training;
	    private String csp_training; 
	    private String csp_refresher_training;
	    private String editor_training; 
	    private String editor_refresher_training;
	    private String villages_certification;
	    private String what_went_well;
	    private String what_not_went_well;
	    private String challenges;
	    private String support_requested;
	    private String last_modified;
	    		
		public Data() {
			super();
			}
		
		public Data(String id) {
			super();
			this.id = id;
		}
		
		public Data(String id, String monthYear) {
			super();
			this.id = id;
			this.month_year = monthYear;
		}
		
		public Data(String id, String monthYear, DistrictsData.Data district) {
			super();
			this.id = id;
			this.month_year = monthYear;
			this.district = district;
		}
		
		public Data(String id,DistrictsData.Data district, String month_year, String clusters_identification, String dg_concept_sharing, 
				String csp_identification, String dissemination_set_deployment, String village_operationalization, String video_uploading, 
				String video_production, String storyboard_preparation, String video_shooting, String video_editing, 
				String video_quality_checking, String disseminations, String avg_attendance_per_dissemination, 
				String exp_interest_per_dissemination, String adoption_per_dissemination, String crp_training, 
				String crp_refresher_training, String csp_training, String csp_refresher_training, 
				String editor_training, String editor_refresher_training, String villages_certification, String what_went_well, 
				String what_not_went_well, String challenges, String support_requested, String last_modified){
			
			super();
			this.id = id;
			this.district = district;
			this.month_year = month_year;
			this.clusters_identification = clusters_identification;
			this.dg_concept_sharing = dg_concept_sharing;
			this.csp_identification = csp_identification;
			this.dissemination_set_deployment = dissemination_set_deployment;
			this.village_operationalization = village_operationalization;
			this.video_uploading = video_uploading;
			this.video_production = video_production;
			this.storyboard_preparation = storyboard_preparation;
			this.video_shooting = video_shooting;
			this.video_editing = video_editing;
			this.video_quality_checking = video_quality_checking;
			this.disseminations = disseminations;
			this.avg_attendance_per_dissemination = avg_attendance_per_dissemination;
			this.exp_interest_per_dissemination = exp_interest_per_dissemination;
			this.adoption_per_dissemination = adoption_per_dissemination;
			this.crp_training = crp_training;
			this.crp_refresher_training = crp_refresher_training;
			this.csp_training = csp_training;
			this.csp_refresher_training = csp_refresher_training;
			this.editor_training = editor_training;
			this.editor_refresher_training = editor_refresher_training;
			this.villages_certification = villages_certification;
			this.what_went_well = what_went_well;
			this.what_not_went_well = what_not_went_well;
			this.challenges = challenges;
			this.support_requested = support_requested;
			this.last_modified = last_modified;
		}
		
		public String getMonthYear(){
			return this.month_year;
		}
				
		public DistrictsData.Data getDistrict(){
			return this.district;
		}
		
		public BaseData.Data clone() {
			Data obj = new Data();
			obj.district = (new DistrictsData()).new Data();
			return obj;
		}
		
		@Override
		public String getPrefixName() {
			return Data.COLLECTION_PREFIX;
		}
		
		@Override
		public void setObjValueFromString(String key, String val) {
			super.setObjValueFromString(key, val);
			if(key.equals("id")) {
				this.id = val;
			} else if(key.equals("district")) {
				DistrictsData district = new DistrictsData();
				this.district = district.getNewData();
				this.district.id = val;
			} else if(key.equals("month_year")) {
				this.month_year = (String)val;
			} else if(key.equals("clusters_identification")){
				this.clusters_identification = (String)val;
			} else if(key.equals("dg_concept_sharing")){
				this.dg_concept_sharing = (String)val;	
			} else if (key.equals("csp_identification")) {
				this.csp_identification = (String)val;
			} else if (key.equals("dissemination_set_deployment")){
				this.dissemination_set_deployment = (String)val;
			} else if(key.equals("village_operationalization")){
				this.village_operationalization = (String)val;
			} else if(key.equals("video_uploading")){
				this.video_uploading = (String)val;
			} else if(key.equals("video_production")){
				this.video_production = (String)val;
			} else if(key.equals("storyboard_preparation")){
				this.storyboard_preparation = (String)val;
			} else if(key.equals("video_shooting")){
				this.video_shooting = (String)val;
			} else if(key.equals("video_editing")){
				this.video_editing = (String)val;
			} else if(key.equals("video_quality_checking")) {
				this.video_quality_checking = (String)val;
			} else if (key.equals("disseminations")) {
				this.disseminations = (String)val;
			} else if (key.equals("avg_attendance_per_dissemination")){
				this.avg_attendance_per_dissemination = val;
			} else if(key.equals("exp_interest_per_dissemination")) {
				this.exp_interest_per_dissemination = (String)val;;
			} else if(key.equals("adoption_per_dissemination")) {
				this.adoption_per_dissemination = (String)val;;
			} else if(key.equals("crp_training")) {
				this.crp_training = (String)val;;
			} else if(key.equals("crp_refresher_training")) {
				this.crp_refresher_training = (String)val;;
			} else if(key.equals("csp_training")){
				this.csp_training = (String)val;
			} else if(key.equals("csp_refresher_training")) {
				this.csp_refresher_training = (String)val;;
			} else if(key.equals("editor_training")) {
				this.editor_training = (String)val;
			} else if(key.equals("editor_refresher_training")) {
				this.editor_refresher_training = (String)val;
			} else if(key.equals("villages_certification")) {
				this.villages_certification = (String)val;
			} else if(key.equals("what_went_well")){
				this.what_went_well= (String)val;
			} else if(key.equals("what_not_went_well")){
				this.what_not_went_well= (String)val;
			} else if(key.equals("challenges")){
				this.challenges= (String)val;
			} else if(key.equals("support_requested")){
				this.support_requested= (String)val;
			} else if(key.equals("last_modified")){
				this.last_modified= (String)val;
			} else {
				return;
			}
			this.addNameValueToQueryString(key, val);			
		}
		
		@Override
		public boolean validate() {
			IntegerValidator clusters_identification = new IntegerValidator(this.clusters_identification, true, true);
			clusters_identification.setError("Please enter a valid clustersIdentification");
			IntegerValidator dg_concept_sharing = new IntegerValidator(this.dg_concept_sharing, true, true);
			dg_concept_sharing.setError("Please enter a valid DgConceptSharing");
			IntegerValidator csp_identification = new IntegerValidator(this.csp_identification, true, true);
			csp_identification.setError("Please enter a valid csp_identification");
			IntegerValidator dissemination_set_deployment = new IntegerValidator(this.dissemination_set_deployment, true, true);
			dissemination_set_deployment.setError("Please enter a valid dissemination_set_deployment");
			IntegerValidator village_operationalization = new IntegerValidator(this.village_operationalization, true, true);
			village_operationalization.setError("Please enter a valid village_operationalization");
			IntegerValidator video_uploading = new IntegerValidator(this.video_uploading, true, true);
			video_uploading.setError("Please enter a valid video_uploading");
			IntegerValidator video_production = new IntegerValidator(this.video_production, true, true);
			video_production.setError("Please enter a valid video_production");
			IntegerValidator storyboard_preparation = new IntegerValidator(this.storyboard_preparation, true, true);
			storyboard_preparation.setError("Please enter a valid storyboard_preparation");
			IntegerValidator video_shooting = new IntegerValidator(this.video_shooting, true, true);
			video_shooting.setError("Please enter a valid video_shooting");
			IntegerValidator video_editing = new IntegerValidator(this.video_editing, true, true);
			video_editing.setError("Please enter a valid video_editing");
			IntegerValidator video_quality_checking = new IntegerValidator(this.video_quality_checking, true, true);
			video_quality_checking.setError("Please enter a valid video_quality_checking");
			IntegerValidator disseminations = new IntegerValidator(this.disseminations, true, true);
			disseminations.setError("Please enter a valid disseminations");
			IntegerValidator avg_attendance_per_dissemination = new IntegerValidator(this.avg_attendance_per_dissemination, true, true);
			avg_attendance_per_dissemination.setError("Please enter a valid avg_attendance_per_dissemination");
			IntegerValidator exp_interest_per_dissemination = new IntegerValidator(this.exp_interest_per_dissemination, true, true);
			exp_interest_per_dissemination.setError("Please enter a valid exp_interest_per_dissemination");
			IntegerValidator adoption_per_dissemination = new IntegerValidator(this.adoption_per_dissemination, true, true);
			adoption_per_dissemination.setError("Please enter a valid adoption_per_dissemination");
			IntegerValidator crp_training = new IntegerValidator(this.crp_training, true, true);
			crp_training.setError("Please enter a valid crp_training");
			IntegerValidator crp_refresher_training = new IntegerValidator(this.crp_refresher_training, true, true);
			crp_refresher_training.setError("Please enter a valid crp_refresher_training");
			IntegerValidator csp_training = new IntegerValidator(this.csp_training, true, true);
			csp_training.setError("Please enter a valid csp_training");
			IntegerValidator csp_refresher_training = new IntegerValidator(this.csp_refresher_training, true, true);
			csp_refresher_training.setError("Please enter a valid csp_refresher_training");
			IntegerValidator editor_training = new IntegerValidator(this.editor_training, true, true);
			editor_training.setError("Please enter a valid editor_training");
			IntegerValidator editor_refresher_training = new IntegerValidator(this.editor_refresher_training, true, true);
			editor_refresher_training.setError("Please enter a valid editor_refresher_training");
			IntegerValidator villages_certification = new IntegerValidator(this.villages_certification, true, true);
			villages_certification.setError("Please enter a valid villages_certification");
			StringValidator what_went_well = new StringValidator(this.what_went_well, true, true, 1, 300);;
			what_went_well.setError("Please make sure you choose a  valid what_went_well.");
			StringValidator what_not_went_well = new StringValidator(this.what_not_went_well, true, true, 1, 300);;
			what_not_went_well.setError("Please make sure you choose a  valid what_not_went_well.");
			StringValidator challenges = new StringValidator(this.challenges, true, true, 1, 300);;
			challenges.setError("Please make sure you choose a  valid challenges.");
			StringValidator support_requested = new StringValidator(this.support_requested, true, true, 1, 300);;
			support_requested.setError("Please make sure you choose a  valid support_requested.");
			
			ArrayList validatorList = new ArrayList();
			validatorList.add(clusters_identification);
			validatorList.add(dg_concept_sharing);
			validatorList.add(csp_identification);
			validatorList.add(dissemination_set_deployment);
			validatorList.add(village_operationalization);
			validatorList.add(video_uploading);
			validatorList.add(video_production);
			validatorList.add(storyboard_preparation);
			validatorList.add(video_shooting);
			validatorList.add(video_editing);
			validatorList.add(video_quality_checking);
			validatorList.add(disseminations);
			validatorList.add(avg_attendance_per_dissemination);
			validatorList.add(exp_interest_per_dissemination);
			validatorList.add(adoption_per_dissemination);
			validatorList.add(crp_training);
			validatorList.add(crp_refresher_training);
			validatorList.add(csp_training);
			validatorList.add(csp_refresher_training);
			validatorList.add(editor_training);
			validatorList.add(editor_refresher_training);
			validatorList.add(villages_certification);
			validatorList.add(what_went_well);
			validatorList.add(what_not_went_well);
			validatorList.add(challenges);
			validatorList.add(support_requested);
			return this.executeValidators(validatorList);
		}
		
		@Override
		public void save() {
			TargetsData targetsDataDbApis = new TargetsData();		
			this.id = targetsDataDbApis.autoInsert(this.id,
						this.district.getId(),
						this.month_year, 
						this.clusters_identification, 
						this.dg_concept_sharing, 
						this.csp_identification, 
						this.dissemination_set_deployment, 
						this.village_operationalization,
						this.video_uploading, 
						this.video_production, 
						this.storyboard_preparation, 
						this.video_shooting,
						this.video_editing, 
						this.video_quality_checking, 
						this.disseminations, 
						this.avg_attendance_per_dissemination, 
						this.exp_interest_per_dissemination, 
						this.adoption_per_dissemination, 
						this.crp_training, 
						this.crp_refresher_training, 
						this.csp_training,
						this.csp_refresher_training, 
						this.editor_training,
						this.editor_refresher_training, 
						this.villages_certification, 
						this.what_went_well,
						this.what_not_went_well, 
						this.challenges, 
						this.support_requested, 
						this.last_modified);
			this.addNameValueToQueryString("id", this.id);
		}
		
		@Override
		public String toQueryString(String id) {
			TargetsData targetsData = new TargetsData();
			return this.rowToQueryString(targetsData.getTableName(), targetsData.getFields(), "id", id, "");
		}
		
		@Override
		public String getTableId() {
			TargetsData targetsDataDbApis = new TargetsData();
			return targetsDataDbApis.tableID;
		}
	}
	
	public static String tableID = "42";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `dashboard_target` " +
												"(id BIGINT UNSIGNED PRIMARY KEY  NOT NULL , " +
												"district_id BIGINT UNSIGNED NOT NULL," +
												"month_year DATE NOT NULL," +
												"clusters_identification INT  NULL DEFAULT NULL," +
												"dg_concept_sharing INT  NULL DEFAULT NULL," +
												"csp_identification INT  NULL DEFAULT NULL," +
												"dissemination_set_deployment INT  NULL DEFAULT NULL," +
												"village_operationalization INT  NULL DEFAULT NULL," +
												"video_uploading INT  NULL DEFAULT NULL," +
												"video_production INT  NULL DEFAULT NULL," +
												"storyboard_preparation INT  NULL DEFAULT NULL," +
												"video_shooting INT  NULL DEFAULT NULL," +
												"video_editing INT  NULL DEFAULT NULL," +
												"video_quality_checking INT  NULL DEFAULT NULL," +
												"disseminations INT  NULL DEFAULT NULL," +
												"avg_attendance_per_dissemination INT  NULL DEFAULT NULL," +
												"exp_interest_per_dissemination INT  NULL DEFAULT NULL," +
												"adoption_per_dissemination INT  NULL DEFAULT NULL," +
												"crp_training INT  NULL DEFAULT NULL," +
												"crp_refresher_training INT  NULL DEFAULT NULL," +
												"csp_training INT  NULL DEFAULT NULL," +
												"csp_refresher_training INT  NULL DEFAULT NULL," +
												"editor_training INT  NULL DEFAULT NULL," +
												"editor_refresher_training INT  NULL DEFAULT NULL," +
												"villages_certification INT  NULL DEFAULT NULL," +
												"what_went_well TEXT NULL DEFAULT NULL,"+
												"what_not_went_well TEXT NULL DEFAULT NULL ,"+
												"challenges TEXT  NULL DEFAULT NULL ," +
												"support_requested TEXT  NULL DEFAULT NULL ," +
												"last_modified DATETIME  NOT NULL," +
												"FOREIGN KEY(district_id) REFERENCES district(id));";
	protected static String dropTable = "DROP TABLE IF EXISTS `dashboard_target`;";
	protected static String selectTargets = "SELECT t.id, t.month_year, t.district_id, d.district_name " +
										   "FROM dashboard_target t, district d WHERE t.district_id = d.id ORDER BY (-t.month_year);";
	protected static String listTargets = "SELECT t.id, t.month_year, t.district_id, d.district_name " +
										 "FROM dashboard_target t, district d WHERE t.district_id = d.id ORDER BY (-t.id);";
	protected static String saveTargetOnlineURL = "/dashboard/savetargetonline/";
	protected static String getTargetOnlineURL = "/dashboard/gettargetsonline/";
	protected static String saveTargetOfflineURL = "/dashboard/savetargetoffline/";
	protected String table_name = "dashboard_target";
	protected String[] fields = {"id", "district_id", "month_year", "clusters_identification", "dg_concept_sharing", "csp_identification", 
								"dissemination_set_deployment","village_operationalization",
								"video_uploading", "video_production", "storyboard_preparation", "video_shooting", "video_editing", 
								"video_quality_checking", "disseminations","avg_attendance_per_dissemination", "exp_interest_per_dissemination",
								"adoption_per_dissemination",
								"crp_training", "crp_refresher_training", "csp_training", "csp_refresher_training", "editor_training", 
								"editor_refresher_training", "villages_certification",
								"what_went_well", "what_not_went_well","challenges","support_requested", "last_modified"}; 		
	
	public TargetsData() {
		super();
	}
	
	public TargetsData(OnlineOfflineCallbacks callbacks) {
		super(callbacks);
	}
	
	public TargetsData(OnlineOfflineCallbacks callbacks, Form form) {
		super(callbacks, form);
	}

	@Override
	public Data getNewData() {
		return new Data();
	}
	
	@Override
	protected String getTableId() {
		return TargetsData.tableID;
	}
	
	@Override
	public String getTableName() {
		return this.table_name;
	}
	
	@Override
	protected String[] getFields() {
		return this.fields;
	}
	
	@Override
	protected String getCreateTableSql(){
		return this.createTable;
	}
	
	@Override
	protected String getDeleteTableSql(){
		return this.dropTable;
	}
	
	@Override
	public String getListingOnlineURL(){
		return TargetsData.getTargetOnlineURL;
	}
	
	@Override
	public String getSaveOfflineURL(){
		return TargetsData.saveTargetOfflineURL;
	}
	
	@Override
	public String getSaveOnlineURL(){
		return TargetsData.saveTargetOnlineURL;
	}
	
	public final native JsArray<Type> asArrayOfData(String json) /*-{
		return eval(json);
	}-*/;
	
	public List serialize(JsArray<Type> targetObjects){
		List targets = new ArrayList();
		DistrictsData district = new DistrictsData();
		for(int i = 0; i < targetObjects.length(); i++){
			DistrictsData.Data d = district.new Data(targetObjects.get(i).getDistrict().getPk(), 
					targetObjects.get(i).getDistrict().getDistrictName()) ;
			Data target = new Data(targetObjects.get(i).getPk(),d, 
									targetObjects.get(i).getMonthYear(),
									targetObjects.get(i).getClustersIdentification(),
									targetObjects.get(i).getDgConceptSharing(), 
									targetObjects.get(i).getCspIdentification(),
									targetObjects.get(i).getDisseminationSetDeployment(),
									targetObjects.get(i).getVillageOperationalization(),
									targetObjects.get(i).getVideoUploading(),
									targetObjects.get(i).getVideoProduction(),
									targetObjects.get(i).getStoryboardPreparation(),
									targetObjects.get(i).getVideoShooting(),
									targetObjects.get(i).getVideoEditing(), 
									targetObjects.get(i).getVideoQualityChecking(), 
									targetObjects.get(i).getDisseminations(),
									targetObjects.get(i).getAvgAttendancePerDissemination(),
									targetObjects.get(i).getExpInterestPerDissemination(),
									targetObjects.get(i).getAdoptionPerDissemination(),
									targetObjects.get(i).getCrpTraining(),
									targetObjects.get(i).getCrpRefresherTraining(),
									targetObjects.get(i).getCspTraining(),
									targetObjects.get(i).getCspRefresherTraining(),
									targetObjects.get(i).getEditorTraining(),
									targetObjects.get(i).getEditorRefresherTraining(),
									targetObjects.get(i).getVillagesCertification(),
									targetObjects.get(i).getWhatWentWell(),
									targetObjects.get(i).getWhatNotWentWell(),
									targetObjects.get(i).getChallenges(),
									targetObjects.get(i).getSupportRequested(),
									targetObjects.get(i).getLastModified());

			targets.add(target);
		}
		return targets;
	}
	
	@Override
	public List getListingOnline(String json){
		return this.serialize(this.asArrayOfData(json));		
	}
	
	public List getTargetsListingOffline(String... pageNum){
		BaseData.dbOpen();
		List targets = new ArrayList();
		DistrictsData district = new DistrictsData();
		String listTemp;
		if(pageNum.length == 0) {
			listTemp = listTargets;
		}
		else {
			int offset = (Integer.parseInt(pageNum[0]) - 1)*pageSize;
			listTemp = listTargets + " LIMIT "+ Integer.toString(offset) + " , "+Integer.toString(pageSize) +";";
		}
		this.select(listTemp);
		if (this.getResultSet().isValidRow()){
			try {
				for (int i = 0; this.getResultSet().isValidRow(); ++i, this.getResultSet().next()) {
					DistrictsData.Data d = district.new Data(this.getResultSet().getFieldAsString(2),  this.getResultSet().getFieldAsString(3)) ;
					Data target = new Data(this.getResultSet().getFieldAsString(0), this.getResultSet().getFieldAsString(1), d);
					targets.add(target);
	    	      }				
			} catch (DatabaseException e) {
				Window.alert("Database Exception : " + e.toString());
				BaseData.dbClose();
			}
		}
		BaseData.dbClose();
		return targets;
	}
	
	public List getAllTargetsOffline(){
		BaseData.dbOpen();
		List targets = new ArrayList();
		this.select(selectTargets);
		if (this.getResultSet().isValidRow()){
			try {
				DistrictsData districtsData = new DistrictsData();
				DistrictsData.Data district;
				for (int i = 0; this.getResultSet().isValidRow(); ++i, this.getResultSet().next()) {
					district = districtsData.new Data(this.getResultSet().getFieldAsString(2), this.getResultSet().getFieldAsString(3));
					Data target = new Data(this.getResultSet().getFieldAsString(0), this.getResultSet().getFieldAsString(1), district);
					targets.add(target);
	    	      }				
			} catch (DatabaseException e) {
				Window.alert("Database Exception : " + e.toString());
				BaseData.dbClose();
			}
		}
		BaseData.dbClose();
		return targets;
	}
	
	public Object postPageData() {
		if(BaseData.isOnline()){
			this.post(RequestContext.SERVER_HOST + TargetsData.saveTargetOnlineURL, this.form.getQueryString());
		}
		else{
			if(this.validate()) {
				this.save();
				return true;
			}
		}
		
		return false;
	}
	
	public Object postPageData(String id) {
		if(BaseData.isOnline()){
			this.post(RequestContext.SERVER_HOST + this.saveTargetOnlineURL + id + "/", this.form.getQueryString());
		}
		else{
			if(this.validate()) {
				this.save();
				return true;
			}
		}
		return false;
	}
	
	public Object getListPageData(String pageNum){
		if(BaseData.isOnline()){
			int offset = (Integer.parseInt(pageNum)-1)*pageSize;
			int limit = offset+pageSize;
			this.get(RequestContext.SERVER_HOST + TargetsData.getTargetOnlineURL+Integer.toString(offset)+"/"+Integer.toString(limit)+ "/");
		}
		else{
			return true;
		}
		return false;
	}	
	
	
	public String retrieveDataAndConvertResultIntoHtml(){
		DistrictsData districtData = new DistrictsData();
		List districts = districtData.getAllDistrictsOffline();
		DistrictsData.Data district;
		String html = "<select name=\"district\" id=\"id_district\">" + 
			"<option value='' selected='selected'>---------</option>";
		for(int i =0; i< districts.size(); i++){
			district = (DistrictsData.Data)districts.get(i);
			html = html + "<option value = \"" + district.getId() + "\">" + district.getDistrictName() + "</option>";
		}
		html = html + "</select>";
		return html;
	}
	
	public Object getAddPageData(){
		if(BaseData.isOnline()){
			this.get(RequestContext.SERVER_HOST + TargetsData.saveTargetOnlineURL);
		}
		else{
			return retrieveDataAndConvertResultIntoHtml();
		}
		return false;
	}
	
	public Object getAddPageData(String id){
		if(BaseData.isOnline()){
			this.get(RequestContext.SERVER_HOST + this.saveTargetOnlineURL + id + "/" );
		}
		else {
			this.form.toQueryString(id);
			return retrieveDataAndConvertResultIntoHtml();
		}
		return false;
	}
}
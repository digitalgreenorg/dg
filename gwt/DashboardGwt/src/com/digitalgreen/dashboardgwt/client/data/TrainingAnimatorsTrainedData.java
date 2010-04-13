package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;
import java.util.List;
import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.google.gwt.core.client.JsArray;
import com.google.gwt.gears.client.database.DatabaseException;
import com.google.gwt.user.client.Window;

public class TrainingAnimatorsTrainedData extends BaseData {
	
	public static class Type extends BaseData.Type {
		protected Type() {}
		public final native TrainingsData.Type getTraining() /*-{ return this.fields.training; }-*/;
		public final native AnimatorsData.Type getAnimator() /*-{ return this.fields.animator; }-*/;
	}
	
	public class Data extends BaseData.Data {
		
		final private String COLLECTION_PREFIX = "trainingAnimatorsTrained";
		
		private TrainingsData.Data training;
		private AnimatorsData.Data animator;
		
		public Data(){
			super();
		}
		
		public Data(String id){
			super();
			this.id = id;
		}
		
		public Data(String id, TrainingsData.Data training, AnimatorsData.Data animator){
			super();
			this.id = id;
			this.training = training;
			this.animator = animator;
		}
		
		public TrainingsData.Data getTraining(){
			return this.training;
		}
		
		public AnimatorsData.Data getAnimator(){
			return this.animator;
		}
		
		@Override
		public BaseData.Data clone() {
			Data obj = new Data();
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
			else if(key.equals("training")){
				TrainingsData training1 = new TrainingsData();
				this.training = training1.getNewData();
				this.training.id = val;
			}
			else if(key.equals("animator")){
				AnimatorsData animator1 = new AnimatorsData();
				this.animator = animator1.getNewData();
				this.animator.id = val;
			}
		}
		
		@Override
		public void save(){
			TrainingAnimatorsTrainedData trainingAnimatorsTrainedDataDbApis = new TrainingAnimatorsTrainedData();
			this.id = trainingAnimatorsTrainedDataDbApis.autoInsert(Integer.valueOf(this.id).toString(),
					this.training.getId(), 
					this.animator.getId());
		}
	}
	
	protected static String tableID = "17";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `training_animators_trained` " +
												"(id INTEGER PRIMARY KEY  NOT NULL ," +
												"training_id INT  NOT NULL DEFAULT 0," +
												"animator_id INT  NOT NULL DEFAULT 0, " +
												"FOREIGN KEY(training_id) REFERENCES training(id), " +
												"FOREIGN KEY(animator_id) REFERENCES animator(id));";
	protected static String selectTrainingAnimatorsTrained = "SELECT id FROM training_animators_trained ORDER BY (id)";
	protected static String listTrainingAnimatorsTrained = "SELECT training_animators_trained.id, training.id, training.training_purpose, training.training_outcome, animator.id, animator.name FROM training_animators_trained JOIN training ON training_animators_trained.training_id = training.id JOIN animator ON training_animators_trained.animator_id = animator.id ORDER BY (training_animators_trained.id);";
	protected static String saveTrainingAnimatorsTrainedOnlineURL = "/dashboard/savetraininganimatorstrainedonline/";
	protected static String getTrainingAnimatorsTrainedOnlineURL = "/dashboard/gettraininganimatorstrainedonline/";
	protected static String saveTrainingAnimatorsTrainedOfflineURL = "/dashboard/savetraininganimatorstrainedoffline/";
	protected String table_name = "training_animators_trained";
	protected String[] fields = {"id", "training_id", "animator_id"};
	
	public TrainingAnimatorsTrainedData(){
		super();
	}
	
	public TrainingAnimatorsTrainedData(OnlineOfflineCallbacks callbacks) {
		super(callbacks);
	}
	
	public TrainingAnimatorsTrainedData(OnlineOfflineCallbacks callbacks, Form form, String queryString) {
		super(callbacks, form);
	}

	@Override
	public Data getNewData() {
		return new Data();
	}
	
	@Override
	protected String getTableId() {
		return TrainingAnimatorsTrainedData.tableID;
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
		return TrainingAnimatorsTrainedData.getTrainingAnimatorsTrainedOnlineURL;
	}
	
	public final native JsArray<Type> asArrayOfData(String json) /*-{
		return eval(json);
	}-*/;
	
	public List serialize(JsArray<Type> trainingAnimatorsTrainedObjects) {
		List trainingAnimatorsTrained = new ArrayList();
		TrainingsData training = new TrainingsData();
		AnimatorsData animator = new AnimatorsData();
		for(int i = 0; i < trainingAnimatorsTrainedObjects.length(); i++) {
			TrainingsData.Data t = training. new Data(trainingAnimatorsTrainedObjects.get(i).getPk(), 
					trainingAnimatorsTrainedObjects.get(i).getTraining().getTrainingPurpose());
			
			AnimatorsData.Data a = animator. new Data(trainingAnimatorsTrainedObjects.get(i).getAnimator().getPk(),
									trainingAnimatorsTrainedObjects.get(i).getAnimator().getAnimatorName());
			
			Data traininganimatorstrained = new Data(trainingAnimatorsTrainedObjects.get(i).getPk(), t, a);
			
			trainingAnimatorsTrained.add(traininganimatorstrained);			
		}
		
		return trainingAnimatorsTrained;
	}
	
	@Override
	public List getListingOnline(String json){
		return this.serialize(this.asArrayOfData(json));
	}
	
	public List getTrainingAnimatorsTrainedListingsOffline() {
		BaseData.dbOpen();
		List trainingAnimatorsTrained = new ArrayList();
		TrainingsData training = new TrainingsData();
		AnimatorsData animator = new AnimatorsData();
		this.select(listTrainingAnimatorsTrained);
		if(this.getResultSet().isValidRow()){
			try {
				for (int i = 0; this.getResultSet().isValidRow(); ++i, this.getResultSet().next()) {
					
					TrainingsData.Data t = training. new Data(this.getResultSet().getFieldAsString(1), this.getResultSet().getFieldAsString(2));
					
					AnimatorsData.Data a = animator. new Data(this.getResultSet().getFieldAsString(4), this.getResultSet().getFieldAsString(5));
					
					Data traininganimatorstrained = new Data(this.getResultSet().getFieldAsString(0), t, a);
					
					trainingAnimatorsTrained.add(traininganimatorstrained);
				}
				
			}
			catch (DatabaseException e) {
				Window.alert("Database Exception : " + e.toString());
				BaseData.dbClose();
			}
		}
		BaseData.dbClose();
		return trainingAnimatorsTrained;
	}
	
	public List getAllTrainingAnimatorsTrainedOffline(){
		BaseData.dbOpen();
		List trainingAnimatorsTrained = new ArrayList();
		this.select(selectTrainingAnimatorsTrained);
		if(this.getResultSet().isValidRow()){
			try {
				for (int i = 0; this.getResultSet().isValidRow(); ++i, this.getResultSet().next()) {
					Data traininganimatorstrained = new Data(this.getResultSet().getFieldAsString(0));
					trainingAnimatorsTrained.add(traininganimatorstrained);
				}
			}
			catch (DatabaseException e) {
				Window.alert("Database Exception : " + e.toString());
				BaseData.dbClose();
			}
		}
		BaseData.dbClose();
		return trainingAnimatorsTrained;
	}
	
	public List getTemplateDataOnline(String json){
		List relatedData = null;
		return relatedData;
	}

	public Object postPageData() {
		if(BaseData.isOnline()){
			this.post(RequestContext.SERVER_HOST + TrainingAnimatorsTrainedData.saveTrainingAnimatorsTrainedOnlineURL, this.form.getQueryString());
		}
		else{
			this.save();
			return true;
		}
		return false;
	}
	
	public Object getListPageData(){
		if(BaseData.isOnline()){
			this.get(RequestContext.SERVER_HOST + DistrictsData.getDistrictsOnlineURL);
		}
		else{
			return true;
		}
		return false;
	}
	
	public Object getAddPageData() {
		if(BaseData.isOnline()) {
			this.get(RequestContext.SERVER_HOST + TrainingAnimatorsTrainedData.saveTrainingAnimatorsTrainedOnlineURL);
		}
		else{
			return true;
		}
		return false;
	}
	
	
}

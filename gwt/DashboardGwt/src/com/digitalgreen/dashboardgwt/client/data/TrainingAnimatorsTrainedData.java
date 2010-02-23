package com.digitalgreen.dashboardgwt.client.data;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;

public class TrainingAnimatorsTrainedData extends BaseData {
	
	final protected static String createTable = "CREATE TABLE IF NOT EXISTS `training_animators_trained` " +
												"(id INTEGER PRIMARY KEY  NOT NULL ," +
												"training_id INT  NOT NULL DEFAULT 0," +
												"animator_id INT  NOT NULL DEFAULT 0, " +
												"FOREIGN KEY(training_id) REFERENCES training(id), " +
												"FOREIGN KEY(animator_id) REFERENCES animator(id));";
	
	public TrainingAnimatorsTrainedData(RequestContext requestContext){
		super();
	}

}

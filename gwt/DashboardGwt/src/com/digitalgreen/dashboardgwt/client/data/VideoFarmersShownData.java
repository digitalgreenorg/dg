package com.digitalgreen.dashboardgwt.client.data;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;

public class VideoFarmersShownData extends BaseData {

	final protected static String createTable = "CREATE TABLE IF NOT EXISTS `video_farmers_shown` " +
												"(id INTEGER PRIMARY KEY  NOT NULL ," +
												"video_id INT  NOT NULL DEFAULT 0," +
												"person_id INT  NOT NULL DEFAULT 0, " +
												"FOREIGN KEY(video_id) REFERENCES video(id), " +
												"FOREIGN KEY(person_id) REFERENCES person(id));";
	
	public VideoFarmersShownData(RequestContext requestContext){
		super();
	}

}

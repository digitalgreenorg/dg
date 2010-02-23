package com.digitalgreen.dashboardgwt.client.data;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;

public class ScreeningVideosScreenedData extends BaseData {
	
	final protected static String createTable = "CREATE TABLE IF NOT EXISTS `screening_videos_screened` " +
												"(id INTEGER PRIMARY KEY  NOT NULL ," +
												"screening_id INT  NOT NULL DEFAULT 0," +
												"video_id INT  NOT NULL DEFAULT 0,  " +
												"FOREIGN KEY(screening_id) REFERENCES screening(id), " +
												"FOREIGN KEY(video_id) REFERENCES video(id));";
	
	public ScreeningVideosScreenedData(RequestContext requestContext){
		super();
	}
}

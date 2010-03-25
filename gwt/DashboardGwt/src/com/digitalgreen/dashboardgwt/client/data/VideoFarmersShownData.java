package com.digitalgreen.dashboardgwt.client.data;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;

public class VideoFarmersShownData extends BaseData {

	protected static String tableID = "24";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `video_farmers_shown` " +
												"(id INTEGER PRIMARY KEY  NOT NULL ," +
												"video_id INT  NOT NULL DEFAULT 0," +
												"person_id INT  NOT NULL DEFAULT 0, " +
												"FOREIGN KEY(video_id) REFERENCES video(id), " +
												"FOREIGN KEY(person_id) REFERENCES person(id));";
	
	protected static String saveVideoFarmerOfflineURL = "/dashboard/savevideofarmeroffline/";
	
	public VideoFarmersShownData(){
		super();
	}

	@Override
	protected String getTableId(){
		return VideoFarmersShownData.tableID;
	}
}

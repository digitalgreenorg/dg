package com.digitalgreen.dashboardgwt.client.data;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;

public class VideoRelatedAgriculturalPracticesData extends BaseData {
	
	protected static String tableID = "23";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `video_related_agricultural_practices` " +
												"(id INTEGER PRIMARY KEY  NOT NULL ," +
												"video_id INT  NOT NULL DEFAULT 0," +
												"practices_id INT  NOT NULL DEFAULT 0, " +
												"FOREIGN KEY(video_id) REFERENCES video(id),  " +
												"FOREIGN KEY(practices_id) REFERENCES practices(id) );";
	
	protected static String saveVideoRelatedAgriculturalPracticeOfflineURL = "/dashboard/savevideorelatedagriculturalpracticeoffline/";
	
	public VideoRelatedAgriculturalPracticesData(){
		super();
	}
	
	@Override
	protected String getTableId(){
		return VideoRelatedAgriculturalPracticesData.tableID;
	}

}

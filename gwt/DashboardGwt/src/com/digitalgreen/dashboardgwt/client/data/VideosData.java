package com.digitalgreen.dashboardgwt.client.data;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;

public class VideosData extends BaseData {

	protected static String tableID = "22";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `video` " +
												"(id INTEGER PRIMARY KEY  NOT NULL ," +
												"TITLE VARCHAR(200)  NOT NULL ," +
												"VIDEO_TYPE INT  NOT NULL DEFAULT 0," +
												"DURATION TIME  NULL DEFAULT NULL," +
												"language_id INT  NOT NULL DEFAULT 0," +
												"SUMMARY TEXT  NOT NULL ," +
												"PICTURE_QUALITY VARCHAR(200)  NOT NULL ," +
												"AUDIO_QUALITY VARCHAR(200)  NOT NULL ," +
												"EDITING_QUALITY VARCHAR(200)  NOT NULL ," +
												"EDIT_START_DATE DATE  NULL DEFAULT NULL," +
												"EDIT_FINISH_DATE DATE  NULL DEFAULT NULL," +
												"THEMATIC_QUALITY VARCHAR(200)  NOT NULL ," +
												"VIDEO_PRODUCTION_START_DATE DATE  NOT NULL ," +
												"VIDEO_PRODUCTION_END_DATE DATE  NOT NULL ," +
												"STORYBASE INT  NOT NULL DEFAULT 0," +
												"STORYBOARD_FILENAME VARCHAR(100)  NOT NULL ," +
												"RAW_FILENAME VARCHAR(100)  NOT NULL ," +
												"MOVIE_MAKER_PROJECT_FILENAME VARCHAR(100)  NOT NULL ," +
												"FINAL_EDITED_FILENAME VARCHAR(100)  NOT NULL ," +
												"village_id INT NOT NULL DEFAULT 0," +
												"facilitator_id INT  NOT NULL DEFAULT 0," +
												"cameraoperator_id INT  NOT NULL DEFAULT 0," +
												"reviewer_id INT  NULL DEFAULT NULL," +
												"APPROVAL_DATE DATE  NULL DEFAULT NULL," +
												"supplementary_video_produced_id INT  NULL DEFAULT NULL," +
												"VIDEO_SUITABLE_FOR INT  NOT NULL DEFAULT 0," +
												"REMARKS TEXT  NOT NULL ," +
												"ACTORS VARCHAR(1)  NOT NULL ," +
												"last_modified DATETIME  NOT NULL, " +
												"FOREIGN KEY(village_id) REFERENCES village(id), " +
												"FOREIGN KEY(facilitator_id) REFERENCES animator(id), " +
												"FOREIGN KEY(cameraoperator_id) REFERENCES animator(id), " +
												"FOREIGN KEY(reviewer_id) REFERENCES reviewer(id), " +
												"FOREIGN KEY(language_id) REFERENCES language(id) );";  
	
	protected static String saveVideoOfflineURL = "/dashboard/savevideooffline/";
	
	public VideosData() {
		super();
	}
	
	@Override
	protected String getTableId(){
		return VideosData.tableID;
	}
}
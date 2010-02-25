package com.digitalgreen.dashboardgwt.client.data;

import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;

public class ScreeningsData extends BaseData {

	final protected static String createTable = "CREATE TABLE IF NOT EXISTS `screening` " +
												"(id INTEGER PRIMARY KEY  NOT NULL ," +
												"DATE DATE  NOT NULL ," +
												"START_TIME TIME  NOT NULL ," +
												"END_TIME TIME  NOT NULL ," +
												"LOCATION VARCHAR(200)  NOT NULL ," +
												"TARGET_PERSON_ATTENDANCE INT  NULL DEFAULT NULL," +
												"TARGET_AUDIENCE_INTEREST INT  NULL DEFAULT NULL," +
												"TARGET_ADOPTIONS INT  NULL DEFAULT NULL," +
												"village_id INT  NOT NULL DEFAULT 0," +
												"fieldofficer_id INT  NULL DEFAULT NULL," +
												"animator_id INT  NOT NULL DEFAULT 0, " +
												"FOREIGN KEY(village_id) REFERENCES village(id), " +
												"FOREIGN KEY(fieldofficer_id) REFERENCES field_officer(id), " +
												"FOREIGN KEY(animator_id) REFERENCES animator(id));";
	
	public class Data extends BaseData.Data {
	}

	public ScreeningsData(OnlineOfflineCallbacks callbacks) {
		super(callbacks);
	}

	// Get all information to display the screening add page.
	public Object getAddPageData() {
		if(this.isOnline()) {
			this.get("");
		} else {
			this.select("", null);
		}
		return null;
	}
	
	// Get all information/data to displayt he screening list page.
	public Object getListPageData() {
		if(this.isOnline()) {
			this.get("");
		} else {
			this.select("", null);
		}
		return null;		
	}
}
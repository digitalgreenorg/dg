package com.digitalgreen.dashboardgwt.client.data;

public class BlocksData extends BaseData {

	public static class Type extends BaseData.Type{
		protected Type() {}
		public final native String getBlockName() /*-{ return this.fields.block_name; }-*/;
		public final native String getStartDate() /*-{ return this.fields.start_date; }-*/;
		public final native String getDistrictId() /*-{ return this.fields.district_id; }-*/;
	}
	
	final protected static String createTable = "CREATE TABLE IF NOT EXISTS `block` " +
												"(id INTEGER PRIMARY KEY  NOT NULL ," +
												"BLOCK_NAME VARCHAR(100)  NOT NULL ," +
												"START_DATE DATE  NULL DEFAULT NULL," +
												"district_id INT  NOT NULL DEFAULT 0, " +
												"FOREIGN KEY(district_id) REFERENCES district(id));";
	
}
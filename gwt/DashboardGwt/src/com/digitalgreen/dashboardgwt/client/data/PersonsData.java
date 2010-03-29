package com.digitalgreen.dashboardgwt.client.data;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.ScreeningsData.Data;

public class PersonsData extends BaseData {
	
	public static class Type extends BaseData.Type{
		protected Type() {}
	}
	
	public class Data extends BaseData.Data {
		
		final private static String COLLECTION_PREFIX = "person";
		
		public Data() {
			super();
		}

		@Override
		public String getPrefixName() {
			return Data.COLLECTION_PREFIX;
		}
	}
	
	protected static String tableID = "13";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `person` " +
												"(id INTEGER PRIMARY KEY  NOT NULL ," +
												"PERSON_NAME VARCHAR(100)  NOT NULL ," +
												"FATHER_NAME VARCHAR(100)  NOT NULL ," +
												"AGE INT  NULL DEFAULT NULL," +
												"GENDER VARCHAR(1)  NOT NULL ," +
												"PHONE_NO VARCHAR(100)  NOT NULL ," +
												"ADDRESS VARCHAR(500)  NOT NULL ," +
												"LAND_HOLDINGS INT  NULL DEFAULT NULL," +
												"village_id INT  NOT NULL DEFAULT 0," +
												"group_id INT  NULL DEFAULT NULL," +
												"equipmentholder_id INT  NULL DEFAULT NULL, " +
												"FOREIGN KEY(village_id) REFERENCES village(id), " +
												"FOREIGN KEY(group_id) REFERENCES person_groups(id), " +
												"FOREIGN KEY(equipmentholder_id) REFERENCES equipment_holder(id) ); " ; 
	
	protected static String savePersonOfflineURL = "/dashboard/savepersonoffline/";
	
	public PersonsData() {
		super();
	}
	
	@Override
	public Data getNewData() {
		return new Data();
	}
	
	@Override
	protected String getTableId() {
		return AnimatorsData.tableID;
	}
	
	protected String getTableName() {
		return this.table_name;
	}
}
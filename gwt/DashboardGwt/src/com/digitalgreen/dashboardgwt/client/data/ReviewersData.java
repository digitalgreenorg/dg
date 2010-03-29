package com.digitalgreen.dashboardgwt.client.data;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.AnimatorsData.Data;

public class ReviewersData extends BaseData {
	
	public static class Type extends BaseData.Type{
		protected Type() {}
	}
	
	public class Data extends BaseData.Data {
		
		final private static String COLLECTION_PREFIX = "reviewer";
		
		public Data() {
			super();
		}

		@Override
		public String getPrefixName() {
			return Data.COLLECTION_PREFIX;
		}
	}

	protected static String tableID = "3";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `reviewer` " +
												"(id INTEGER PRIMARY KEY NOT NULL ," +
												"content_type_id INT NOT NULL DEFAULT 0," +
												"object_id INT NOT NULL DEFAULT 0);"; 
	protected static String saveReviewerOfflineURL = "/dashboard/saverevieweroffline/";
	
	public ReviewersData() {
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
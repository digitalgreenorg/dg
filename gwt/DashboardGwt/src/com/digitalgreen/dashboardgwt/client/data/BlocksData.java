package com.digitalgreen.dashboardgwt.client.data;

import java.util.List;

import com.digitalgreen.dashboardgwt.client.data.VillagesData.Data;

public class BlocksData extends BaseData {

	public static class Type extends BaseData.Type{
		protected Type() {}
		public final native String getBlockName() /*-{ return this.fields.block_name; }-*/;
		public final native String getStartDate() /*-{ return this.fields.start_date; }-*/;
		public final native String getDistrictId() /*-{ return this.fields.district_id; }-*/;
	}
	
	public class Data extends BaseData.Data {
		
		final private static String COLLECTION_PREFIX = "block";
			
		private String block_name;
		private String start_date;
		private DistrictsData.Data district;
		
		public Data() {
			super();
		}
		
		public Data(int id, String block_name){
			super();
			this.id = id;
			this.block_name = block_name;
		}
		
		public Data(int id, String block_name, String start_date, DistrictsData.Data district){
			super();
			this.id = id;
			this.block_name = block_name;
			this.start_date = start_date;
			this.district = district;
		}
		
		public String getBlockName() {
			return this.block_name;
		}
	}
	
	protected static String tableID = "9";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `block` " +
												"(id INTEGER PRIMARY KEY  NOT NULL ," +
												"BLOCK_NAME VARCHAR(100)  NOT NULL ," +
												"START_DATE DATE  NULL DEFAULT NULL," +
												"district_id INT  NOT NULL DEFAULT 0, " +
												"FOREIGN KEY(district_id) REFERENCES district(id));";
	
	protected static String saveBlockOfflineURL = "/dashboard/saveblockoffline/";
	
	public BlocksData() {
		super();
	}
	
	@Override
	public Data getNewData() {
		return new Data();
	}
	
	@Override
	protected String getTableId() {
		return BlocksData.tableID;
	}
	
	public List getAllBlocksOffline() {
		return null;
	}	
}
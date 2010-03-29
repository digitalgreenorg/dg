package com.digitalgreen.dashboardgwt.client.data;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;

public class VillagesData extends BaseData {

	public static class Type extends BaseData.Type{
		protected Type() {}
		public final native String getVillageName() /*-{ return this.fields.village_name; }-*/;
		public final native BlocksData.Type getBlock() /*-{ return this.fields.block }-*/;
	}
	
	public class Data extends BaseData.Data {
		
		final private static String COLLECTION_PREFIX = "village";
		
		private String village_name;
	    private BlocksData.Data block; 
	    private int no_of_households;
	    private int population;
	    private String road_connectivity;
	    private String control; 
	    private String start_date; 
		
		public Data() {
			super();
		}
		
		public Data(int id, String village_name) {
			super();
			this.id = id;
			this.village_name = village_name;		
		}

		public Data(int id, String village_name , BlocksData.Data block) {
			super();
			this.id = id;
			this.village_name = village_name;
			this.block = block;
		}
		
		
		public String getVillageName(){
			return this.village_name;
		}
		
		public BlocksData.Data getBlock(){
			return this.block;
		}
		
		public BaseData.Data clone() {
			Data obj = new Data();
			obj.id = this.id;
			obj.village_name = this.village_name;
			obj.block = this.block;
			return obj;
		}
		
		@Override
		public String getPrefixName() {
			return Data.COLLECTION_PREFIX;
		}
	}

	
	protected static String tableID = "10";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `village` " +
												"(id INTEGER PRIMARY KEY  NOT NULL ," +
												"VILLAGE_NAME VARCHAR(100)  NOT NULL ," +
												"block_id INT  NOT NULL DEFAULT 0," +
												"NO_OF_HOUSEHOLDS INT  NULL DEFAULT NULL," +
												"POPULATION INT  NULL DEFAULT NULL," +
												"ROAD_CONNECTIVITY VARCHAR(100)  NOT NULL ," +
												"CONTROL SMALLINT  NULL DEFAULT NULL," +
												"START_DATE DATE  NULL DEFAULT NULL, " +
												"FOREIGN KEY(block_id) REFERENCES block(id)); ";  
	
	protected static String saveVillageOfflineURL = "/dashboard/savevillageoffline/";
	protected String table_name = "village";
	
	public VillagesData() {
		super();
	}
	
	public VillagesData(OnlineOfflineCallbacks callbacks) {
		super(callbacks);
	}
	
	public VillagesData(OnlineOfflineCallbacks callbacks, Form form, String queryString) {
		super(callbacks, form, queryString);
	}

	@Override
	public Data getNewData() {
		return new Data();
	}
	
	@Override
	protected String getTableId() {
		return VillagesData.tableID;
	}
	
	protected String getTableName() {
		return this.table_name;
	}
}
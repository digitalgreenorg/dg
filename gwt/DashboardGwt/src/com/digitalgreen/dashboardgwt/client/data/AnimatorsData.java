package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.VillagesData.Data;
import com.google.gwt.gears.client.database.DatabaseException;
import com.google.gwt.user.client.Window;

public class AnimatorsData extends BaseData {

	public static class Type extends BaseData.Type{
		protected Type() {}
	}
	
	public class Data extends BaseData.Data {
		
		final private static String COLLECTION_PREFIX = "animator";
		
		private String name;
		
		public Data() {
			super();
		}
		
		public Data(int id, String name){
			super();
			this.id = id;
			this.name = name;
		}

		public String getAnimatorNamer(){
			return this.name;
		}
		
		@Override
		public String getPrefixName() {
			return Data.COLLECTION_PREFIX;
		}
	}

	
	protected static String tableID = "15";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `animator` " +
												"(id INTEGER PRIMARY KEY  NOT NULL ," +
												"NAME VARCHAR(100)  NOT NULL ," +
												"AGE INT  NULL DEFAULT NULL," +
												"GENDER VARCHAR(1)  NOT NULL ," +
												"CSP_FLAG SMALLINT  NULL DEFAULT NULL," +
												"CAMERA_OPERATOR_FLAG SMALLINT  NULL DEFAULT NULL," +
												"FACILITATOR_FLAG SMALLINT  NULL DEFAULT NULL," +
												"PHONE_NO VARCHAR(100)  NOT NULL ," +
												"ADDRESS VARCHAR(500)  NOT NULL ," +
												"partner_id INT  NOT NULL DEFAULT 0," +
												"home_village_id INT  NOT NULL DEFAULT 0," +
												"equipmentholder_id INT  NULL DEFAULT NULL, " +
												"FOREIGN KEY(partner_id) REFERENCES partners(id), " +
												"FOREIGN KEY(home_village_id) REFERENCES village(id), " +
												"FOREIGN KEY(equipmentholder_id) REFERENCES equipment_holder(id) );";
	
	protected static String selectAllAnimators = "SELECT id, name FROM animator;";
	protected static String saveAnimatorOfflineURL = "/dashboard/saveanimatoroffline/";
	
	public AnimatorsData() {
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
	
	public List getAllAnimatorsOffline(){
		BaseData.dbOpen();
		List animators = new ArrayList();
		this.select(selectAllAnimators);
		if (this.getResultSet().isValidRow()){
			try {
				for (int i = 0; this.getResultSet().isValidRow(); ++i, this.getResultSet().next()) {
					Data animator = new Data(this.getResultSet().getFieldAsInt(0), this.getResultSet().getFieldAsString(1));
					animators.add(animator);
	    	      }				
			} catch (DatabaseException e) {
				Window.alert("Database Exception : " + e.toString());
				// TODO Auto-generated catch block
				BaseData.dbClose();
			}
			
		}
		BaseData.dbClose();
		return animators;
	}
	
	
}
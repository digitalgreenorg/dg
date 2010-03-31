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
		final private static String COLLECTION_PREFIX = "home_village";
		
		private String name;
		private int age;
		private String gender;
		private int csp_flag;
		private int camera_operator_flag;
		private int facilitator_flag;
		private String phone_no;
		private String address;
		private PartnersData.Data partner;
		private VillagesData.Data village;
		private EquipmentHoldersData.Data equipment_holder;

		public Data() {
			super();
		}
		
		public Data(int id, String name){
			super();
			this.id = id;
			this.name = name;
		}
		
		public Data(int id, String name, int age, String gender, int csp_flag, int camera_operator_flag,
				int facilitator_flag, String phone_no, String address, PartnersData.Data partner,
				VillagesData.Data village, EquipmentHoldersData.Data equipment_holder){
			super();
			this.id = id;
			this.name = name;
			this.age = age;
			this.gender = gender;
			this.csp_flag = csp_flag;
			this.camera_operator_flag = camera_operator_flag;
			this.facilitator_flag = facilitator_flag;
			this.phone_no = phone_no;
			this.address = address;
			this.partner = partner;
			this.village = village;
			this.equipment_holder = equipment_holder;
		}

		public String getAnimatorName(){
			return this.name;
		}
		
		@Override
		public String getPrefixName() {
			return Data.COLLECTION_PREFIX;
		}
		
		@Override
		public BaseData.Data clone() {
			Data obj = new Data();
			obj.id = this.id;
			obj.name = this.name;
			obj.age = this.age;
			obj.gender = this.gender;
			obj.csp_flag = this.csp_flag;
			obj.camera_operator_flag = this.camera_operator_flag;
			obj.facilitator_flag = this.facilitator_flag;
			obj.phone_no = this.phone_no;
			obj.address = this.address;
			obj.partner = (PartnersData.Data)this.partner.clone();
			obj.village = (VillagesData.Data)this.village.clone();
			obj.equipment_holder = (EquipmentHoldersData.Data)this.equipment_holder.clone();
			return obj;
		}
		
		@Override
		public void setObjValueFromString(String key, Object val) {
			if(key.equals("id")) {
				this.id = ((Integer)val).intValue();
			} else if(key.equals("name")) {
				this.name = (String)val;
			} else if(key.equals("age")) {
				this.age = ((Integer)val).intValue();
			} else if(key.equals("gender")) {
				this.gender = (String)val;
			} else if(key.equals("csp_flag")) {
				this.csp_flag = ((Integer)val).intValue();
			} else if(key.equals("camera_operator_flag")) {
				this.camera_operator_flag = ((Integer)val).intValue();
			} else if(key.equals("facilitator_flag")) {
				this.facilitator_flag = ((Integer)val).intValue();
			} else if(key.equals("phone_no")) {
				this.phone_no = (String)val;
			} else if(key.equals("address")) {
				this.address = (String)val;
			} else if(key.equals("partner_id")) {
				PartnersData partner = new PartnersData();
				this.partner = partner.getNewData();
				this.partner.id = ((Integer)val).intValue();
			} else if(key.equals("home_village_id")) {
				VillagesData village = new VillagesData();
				this.village = village.getNewData();
				this.village.id = ((Integer)val).intValue();
			} else if(key.equals("equipmentholder_id")) {
				EquipmentHoldersData equipmentHolders = new EquipmentHoldersData();
				this.equipment_holder = equipmentHolders.getNewData();
				this.equipment_holder.id = ((Integer)val).intValue();;
			}
		}
		
		@Override
		public void save() {
			AnimatorsData animatorsDataDbApis = new AnimatorsData();
			this.id = animatorsDataDbApis.autoInsert(this.name, 
					Integer.valueOf(this.age).toString(), 
					this.gender, Integer.valueOf(this.csp_flag).toString(),
					Integer.valueOf(this.camera_operator_flag).toString(), 
					Integer.valueOf(this.facilitator_flag).toString(), 
					this.phone_no, this.address,
					Integer.valueOf(this.partner.getId()).toString(), 
					Integer.valueOf(this.village.getId()).toString(), 
					Integer.valueOf(this.equipment_holder.getId()).toString());
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
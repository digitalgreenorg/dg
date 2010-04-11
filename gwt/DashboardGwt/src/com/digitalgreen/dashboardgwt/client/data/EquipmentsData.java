package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;
import java.util.List;
import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.EquipmentHoldersData.Data;
import com.google.gwt.core.client.JsArray;
import com.google.gwt.gears.client.database.DatabaseException;
import com.google.gwt.user.client.Window;


public class EquipmentsData extends BaseData {
	
	public static class Type extends BaseData.Type{
		protected Type() {}
		public final native String getEquipmentType() /*-{ return $wnd.checkForNullValues(this.fields.equipment_type); }-*/;
		public final native String getModelNo() /*-{ return $wnd.checkForNullValues(this.fields.model_no); }-*/;
		public final native String getSerialNo() /*-{ return $wnd.checkForNullValues(this.fields.serial_no); }-*/;
		public final native String getCost() /*-{ return $wnd.checkForNullValues(this.fields.cost); }-*/;
		public final native String getProcurementDate() /*-{ return $wnd.checkForNullValues(this.fields.procurement_date); }-*/;
		public final native String getWarrantyExpirationDate() /*-{ return $wnd.checkForNullValues(this.fields.warranty_expiration_date); }-*/;
		public final native String getEquipmentHolderId() /*-{ return this.fields.equipmentholder_id; }-*/;
	
	}
	
	public class Data extends BaseData.Data {
		
		final private static String COLLECTION_PREFIX = "equipments";
			
		private String equipment_type;
		private String model_no;
		private String serial_no;
		private String cost;
		private String procurement_date;
		private String warranty_expiration_date;
		private String equipmentholder_id;
		
		
		public Data() {
			super();
		}

		public Data(String id, String equipment_type,String model_no,String serial_no,String cost,String procurement_date,
				String warranty_expiration_date, String equipmentholder_id) {
			super();
			this.id = id;
			this.equipment_type = equipment_type;
			this.model_no = model_no;
			this.serial_no = serial_no;
			this.cost = cost;
			this.procurement_date = procurement_date;
			this.warranty_expiration_date = warranty_expiration_date;
			this.equipmentholder_id = equipmentholder_id;
		}
		
		public Data(String id, String equipment_type){
			super();
			this.id = id;
			this.equipment_type = equipment_type;
		}
				
		public String getEquipmentType(){
			return this.equipment_type;
		}
		
		public String getModelNo(){
			return this.model_no;
		}
		
		public String getSerialNo(){
			return this.serial_no;
		}
		
		public String getCost(){
			return this.cost;
		}
		
		public String getProcurementDate(){
			return this.procurement_date;
		}
		
		public String getWarrantyExpirationDate(){
			return this.warranty_expiration_date;
		}
		
		public String getEquipmentHolderId(){
			return this.equipmentholder_id;
		}
		
		public BaseData.Data clone() {
			Data obj = new Data();
			return obj;
		}
		
		@Override
		public String getPrefixName() {
			return Data.COLLECTION_PREFIX;
		}
		
		@Override
		public void setObjValueFromString(String key, String val) {
			super.setObjValueFromString(key, val);
			if(key.equals("id")) {
				this.id = val;
			} else if(key.equals("equipment_type")) {
				this.equipment_type = (String)val;
			} else if(key.equals("model_no")) {
				this.model_no = (String)val;
			} else if(key.equals("serial_no")) {
				this.serial_no = (String)val;
			} else if(key.equals("cost")) {
				this.cost = (String)val;
			}  else if(key.equals("procurement_date")) {
				this.procurement_date = (String)val;
			} else if(key.equals("warranty_expiration_date")) {
				this.warranty_expiration_date = (String)val;
			} else if(key.equals("equipmentholder")) {
				this.equipmentholder_id = val;
			} 	 	
		}
		
		@Override
		
		public void save() {
			EquipmentsData equipmentsDataDbApis = new EquipmentsData();			
			this.id = equipmentsDataDbApis.autoInsert(this.id,
						this.equipment_type,
						this.model_no,
						this.serial_no,
						this.cost,
						this.procurement_date,
						this.warranty_expiration_date,
						this.equipmentholder_id);
		}
	}
	
	protected static String tableID = "30";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `equipment_id` " +
												"(id INTEGER PRIMARY KEY  NOT NULL ," +
												"EQUIPMENT_TYPE VARCHAR(300)  NOT NULL ," +
												"MODEL_NO VARCHAR(300)  NOT NULL ," +
												"SERIAL_NO VARCHAR(300)  NOT NULL ," +
												"COST FLOAT(0,0)  NULL DEFAULT NULL," +
												"PROCUREMENT_DATE DATE NULL DEFAULT NULL," +
												"WARRANTY_EXPIRATION_DATE DATE  NULL DEFAULT NULL," +
												"equipmentholder_id INT  NULL DEFAULT NULL, " +
												"FOREIGN KEY(equipmentholder_id) REFERENCES equipment_holder(id));";
	
	protected static String selectEquipments = "SELECT id, EQUIPMENT_TYPE FROM equipment_id  ORDER BY (EQUIPMENT_TYPE);";
	protected static String listEquipments = "SELECT * FROM equipment_id ORDER BY (-id);";
	protected static String saveEquipmentOfflineURL = "/dashboard/saveequipmentoffline/";
	protected static String saveEquipmentOnlineURL = "/dashboard/saveequipmentonline/";
	protected static String getEquipmentOnlineURL = "/dashboard/getequipmentsonline/";
	protected String table_name = "equipment_id";
	protected String[] fields = {"id", "equipment_type", "model_no", "serial_no", "cost", "procurement_date", "warranty_expiration_date",
			"equipmentholder_id"};
	
	
	public EquipmentsData() {
		super();
	}
	
	public EquipmentsData(OnlineOfflineCallbacks callbacks) {
		super(callbacks);
	}
	
	public EquipmentsData(OnlineOfflineCallbacks callbacks, Form form) {
		super(callbacks, form);
	}
	
	@Override
	public Data getNewData() {
		return new Data();
	}
	
	@Override
	protected String getTableId(){
		return EquipmentsData.tableID;
	}
	
	@Override
	protected String getTableName() {
		return this.table_name;
	}
	
	@Override
	protected String[] getFields() {
		return this.fields;
	}
	
	@Override
	public String getListingOnlineURL(){
		return EquipmentsData.getEquipmentOnlineURL;
	}
	
	public final native JsArray<Type> asArrayOfData(String json) /*-{
		return eval(json);
	}-*/;
	
	public List serialize(JsArray<Type> equipmentObjects){
		List equipments = new ArrayList();
		EquipmentHoldersData equipmentholder = new EquipmentHoldersData();
		for(int i = 0; i < equipmentObjects.length(); i++){
			
			Data equipment = new Data(equipmentObjects.get(i).getPk(), equipmentObjects.get(i).getEquipmentType(), 
					equipmentObjects.get(i).getModelNo(),equipmentObjects.get(i).getSerialNo(), 
					equipmentObjects.get(i).getCost(),equipmentObjects.get(i).getProcurementDate(),
					equipmentObjects.get(i).getWarrantyExpirationDate(),equipmentObjects.get(i).getEquipmentHolderId());
			equipments.add(equipment);
		}
		
		return equipments;
	}
	
	@Override
	public List getListingOnline(String json){
		return this.serialize(this.asArrayOfData(json));		
	}
	
	public List getEquipmentsListingOffline(){
		BaseData.dbOpen();
		EquipmentHoldersData equipmentholder = new EquipmentHoldersData();
		List equipments = new ArrayList();
		this.select(listEquipments);
		if (this.getResultSet().isValidRow()){
			try {
				for (int i = 0; this.getResultSet().isValidRow(); ++i, this.getResultSet().next()) {
					Data equipment = new Data(this.getResultSet().getFieldAsString(0), 
							this.getResultSet().getFieldAsString(1),
							this.getResultSet().getFieldAsString(2),
							this.getResultSet().getFieldAsString(3),
							this.getResultSet().getFieldAsString(4),
							this.getResultSet().getFieldAsString(5),
							this.getResultSet().getFieldAsString(6),
							this.getResultSet().getFieldAsString(7));
					equipments.add(equipment);
				}				
			} catch (DatabaseException e) {
				Window.alert("Database Exception : " + e.toString());
				BaseData.dbClose();
			}
		}
		BaseData.dbClose();
		return equipments;
	}
	
	public List getAllEquipmentsOffline(){
		BaseData.dbOpen();
		List equipments = new ArrayList();
		this.select(selectEquipments);
		if (this.getResultSet().isValidRow()){
			try {
				for (int i = 0; this.getResultSet().isValidRow(); ++i, this.getResultSet().next()) {
					Data equipment = new Data(this.getResultSet().getFieldAsString(0), this.getResultSet().getFieldAsString(1));
					equipments.add(equipment);
				}				
			} catch (DatabaseException e) {
				Window.alert("Database Exception : " + e.toString());
				BaseData.dbClose();
			}
		}
		BaseData.dbClose();
		return equipments;
	}

	public Object postPageData() {
		if(BaseData.isOnline()){
			this.post(RequestContext.SERVER_HOST + EquipmentsData.saveEquipmentOnlineURL, this.form.getQueryString());
		}
		else{
			this.save();
			return true;
		}
		
		return false;
	}
			
	public Object getPageData(){
		if(BaseData.isOnline()){
			this.get(RequestContext.SERVER_HOST + EquipmentsData.getEquipmentOnlineURL);
		}
		else{
			return true;
		}
		return false;
	}

}
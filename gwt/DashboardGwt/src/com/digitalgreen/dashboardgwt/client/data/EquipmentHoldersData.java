package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.ApplicationConstants;
import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.data.EquipmentHoldersData.Data;
import com.digitalgreen.dashboardgwt.client.data.EquipmentHoldersData.Type;
import com.google.gwt.core.client.JsArray;
import com.google.gwt.gears.client.database.DatabaseException;
import com.google.gwt.user.client.Window;

public class EquipmentHoldersData extends BaseData {
	
	public static class Type extends BaseData.Type{
		protected Type() {}
		public final native String getContentType() /*-{ return $wnd.checkForNullValues(this.fields.content_type); }-*/;
		public final native String getObjectId() /*-{ return $wnd.checkForNullValues(this.fields.object_id); }-*/;
	}
	
	public class Data extends BaseData.Data {
		
		final private static String COLLECTION_PREFIX = "equipmentholder";
			
		private String content_type;
		private String object_id;
		private String equipmentHolderName; //This field doesn't exist in the Django Model. Made to take care of generic foreign key references.
		
		public Data() {
			super();
		}
		
		public Data(String id, String content_type, String object_id){
			super();
			this.id = id;
			this.content_type = content_type;
			this.object_id = object_id;
		}
		
		public Data(String id) {
			super();
			this.id = id;
		}
		
		public Data(String id, String equipmentHolderName ) {
			super();
			this.id = id;
			this.equipmentHolderName = equipmentHolderName;
		}
		
		public String getContentType(){
			return this.content_type;
		}
		
		public String getObjectId(){
			return this.object_id;
		}
		
		public String getEquipmentHolderName(){
			return this.equipmentHolderName;
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
			}else if(key.equals("content_type")) {
				this.content_type = (String)val;
			} else if(key.equals("object_id")) {
				this.object_id = (String)val;
			} else {
				return;
			}
			this.addNameValueToQueryString(key, val);			
		}
		
		@Override
		public void save() {
			EquipmentHoldersData equipmentholdersDataDbApis = new EquipmentHoldersData();
			this.id = equipmentholdersDataDbApis.autoInsert(this.id,
					this.content_type,
					this.object_id);
			this.addNameValueToQueryString("id", this.id);
		}
		
		@Override
		public String toQueryString(String id) {
			EquipmentHoldersData equipmentHoldersData = new EquipmentHoldersData();
			return this.rowToQueryString(equipmentHoldersData.getTableName(), equipmentHoldersData.getFields(), "id", id, "");
		}
		
		
		@Override
		public String getTableId() {
			EquipmentHoldersData equipmentholdersDataDbApis = new EquipmentHoldersData();
			return equipmentholdersDataDbApis.tableID;
		}
	}
	
	
	public static String tableID = "9";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `equipment_holder` " +
												"(id BIGINT UNSIGNED PRIMARY KEY NOT NULL ," +
												"content_type_id INT NOT NULL DEFAULT 0," +
												"object_id BIGINT UNSIGNED NOT NULL DEFAULT 0);"; 
	protected static String dropTable = "DROP TABLE IF EXISTS `equipment_holder`;";
	protected static String createIndexes = "CREATE INDEX IF NOT EXISTS equipment_holder_PRIMARY ON equipment_holder(id);";
	protected static String selectEquipmentHolders = "SELECT * FROM equipment_holder ORDER BY(-id)";
	protected static String listEquipmentHolders = "SELECT * FROM equipment_holder ORDER BY(-id)";
	protected static String saveEquipmentHolderOnlineURL = "/dashboard/saveequipmentholderonline/";
	protected static String getEquipmentHolderOnlineURL = "/dashboard/getequipmentholdersonline/";
	protected static String saveEquipmentHolderOfflineURL = "/dashboard/saveequipmentholderoffline/";
	protected String table_name = "equipment_holder";
	protected String[] fields = {"id", "content_type", "object_id"};

	
	
	public EquipmentHoldersData() {
		super();
	}
	
	public EquipmentHoldersData(OnlineOfflineCallbacks callbacks) {
		super(callbacks);
	}
	
	public EquipmentHoldersData(OnlineOfflineCallbacks callbacks, Form form) {
		super(callbacks, form);
	}

	@Override
	public Data getNewData() {
		return new Data();
	}
	
	@Override
	protected  String getTableId() {
		return EquipmentHoldersData.tableID;
	}
	
	@Override
	public String getTableName() {
		return this.table_name;
	}
	
	@Override
	protected String[] getFields() {
		return this.fields;
	}
	
	@Override
	protected String getCreateTableSql(){
		return this.createTable;
	}
	
	@Override
	protected String getDeleteTableSql(){
		return this.dropTable;
	}
	
	@Override
	public String getListingOnlineURL(){
		return EquipmentHoldersData.getEquipmentHolderOnlineURL;
	}
	
	@Override
	public String getSaveOfflineURL(){
		return EquipmentHoldersData.saveEquipmentHolderOfflineURL;
	}
	
	@Override
	public String getSaveOnlineURL(){
		return EquipmentHoldersData.saveEquipmentHolderOnlineURL;
	}

	public final native JsArray<Type> asArrayOfData(String json) /*-{
		return eval(json);
	}-*/;
	
	public List serialize(JsArray<Type> equipmentholderObjects){
		List equipmentholders = new ArrayList();
		for(int i = 0; i < equipmentholderObjects.length(); i++){
			Data equipmentholder = new Data(equipmentholderObjects.get(i).getPk(), 
					equipmentholderObjects.get(i).getContentType(), 
					equipmentholderObjects.get(i).getObjectId());
			equipmentholders.add(equipmentholder);
		}
		return equipmentholders;
	}
	
	@Override
	public List getListingOnline(String json){
		return this.serialize(this.asArrayOfData(json));		
	}

	public List getAllEquipmentHoldersOffline(){
		BaseData.dbOpen();
		List equipmentHolders = new ArrayList();
		this.select(selectEquipmentHolders);
		if(this.getResultSet().isValidRow()){
			try {
				String equipmentHolderName = "";
				for(int i = 0; this.getResultSet().isValidRow(); ++i, this.getResultSet().next()){
					
					// Get the name of the reviewer (Generic Foreign Key to Development Manager, Field Officer and Partner)
					if(this.getResultSet().getFieldAsString(1) == DevelopmentManagersData.tableID){
						DevelopmentManagersData dm = (DevelopmentManagersData)ApplicationConstants.mappingBetweenTableIDAndDataObject.get(this.getResultSet().getFieldAsString(1));
						dm.select(dm.getDevelopmentManagerByID, this.getResultSet().getFieldAsString(2));
						equipmentHolderName = dm.getResultSet().getFieldAsString(1);
					} else if(this.getResultSet().getFieldAsString(1) == FieldOfficersData.tableID){
						FieldOfficersData fo = (FieldOfficersData)ApplicationConstants.mappingBetweenTableIDAndDataObject.get(this.getResultSet().getFieldAsString(1));
						fo.select(fo.getFieldOfficerByID, this.getResultSet().getFieldAsString(2));
						equipmentHolderName = fo.getResultSet().getFieldAsString(1);
					} else if(this.getResultSet().getFieldAsString(1) == PartnersData.tableID){
						PartnersData p = (PartnersData)ApplicationConstants.mappingBetweenTableIDAndDataObject.get(this.getResultSet().getFieldAsString(1));
						p.select(p.getPartnerByID, this.getResultSet().getFieldAsString(2));
						equipmentHolderName = p.getResultSet().getFieldAsString(1);
					} 
					
					Data equipmentHolder = new Data(this.getResultSet().getFieldAsString(0), equipmentHolderName);
					equipmentHolders.add(equipmentHolder);
				}
			}
			catch(DatabaseException e){
				Window.alert("Database Exception : " + e.toString());
				BaseData.dbClose();
			}
		}
		BaseData.dbClose();
		return equipmentHolders;
	}
		
}
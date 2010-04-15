package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.data.EquipmentHoldersData.Data;
import com.digitalgreen.dashboardgwt.client.data.EquipmentHoldersData.Type;
import com.google.gwt.core.client.JsArray;
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
		
		public String getContentType(){
			return this.content_type;
		}
		
		public String getObjectId(){
			return this.object_id;
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
			if(key.equals("content_type")) {
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
		public String getTableId() {
			EquipmentHoldersData equipmentholdersDataDbApis = new EquipmentHoldersData();
			return equipmentholdersDataDbApis.tableID;
		}
	}
	
	
	protected static String tableID = "2";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `equipment_holder` " +
												"(id INTEGER PRIMARY KEY NOT NULL ," +
												"content_type_id INT NOT NULL DEFAULT 0," +
												"object_id INT NOT NULL DEFAULT 0);"; 
	
	protected static String selectEquipmentHolders = "SELECT id FROM equipment_holder ORDER BY(-id)";
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
	protected String getTableName() {
		return this.table_name;
	}
	
	@Override
	protected String[] getFields() {
		return this.fields;
	}
	
	@Override
	public String getListingOnlineURL(){
		return EquipmentHoldersData.getEquipmentHolderOnlineURL;
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
		
}
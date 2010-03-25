package com.digitalgreen.dashboardgwt.client.data;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;

public class EquipmentHoldersData extends BaseData {

	protected static String tableID = "2";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `equipment_holder` " +
												"(id INTEGER PRIMARY KEY NOT NULL ," +
												"content_type_id INT NOT NULL DEFAULT 0," +
												"object_id INT NOT NULL DEFAULT 0);"; 
	
	protected static String saveEquipmentHolderOfflineURL = "/dashboard/saveequipmentholderoffline/";
	
	public EquipmentHoldersData() {
		super();
	}
	
	@Override
	protected String getTableId() {
		return EquipmentHoldersData.tableID;
	}

	
}
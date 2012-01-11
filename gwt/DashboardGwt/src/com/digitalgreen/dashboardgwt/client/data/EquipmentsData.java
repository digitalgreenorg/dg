package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;
import java.util.List;
import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.EquipmentHoldersData.Data;
import com.digitalgreen.dashboardgwt.client.data.validation.DateValidator;
import com.digitalgreen.dashboardgwt.client.data.validation.FloatValidator;
import com.digitalgreen.dashboardgwt.client.data.validation.StringValidator;
import com.google.gwt.core.client.JsArray;
import com.google.gwt.gears.client.database.DatabaseException;
import com.google.gwt.user.client.Window;


public class EquipmentsData extends BaseData {
	
	public static class Type extends BaseData.Type{
		protected Type() {}
		public final native String getEquipmentType() /*-{ return $wnd.checkForNullValues(this.fields.equipment_type); }-*/;
		public final native String getOtherEquipment() /*-{ return $wnd.checkForNullValues(this.fields.other_equipment); }-*/;
		public final native String getInvoiceNo() /*-{ return $wnd.checkForNullValues(this.fields.invoice_no); }-*/;
		public final native String getModelNo() /*-{ return $wnd.checkForNullValues(this.fields.model_no); }-*/;
		public final native String getSerialNo() /*-{ return $wnd.checkForNullValues(this.fields.serial_no); }-*/;
		public final native String getCost() /*-{ return $wnd.checkForNullValues(this.fields.cost); }-*/;
		public final native String getPurpose() /*-{ return $wnd.checkForNullValues(this.fields.purpose); }-*/;
		public final native String getAdditionalAccessories() /*-{ return $wnd.checkForNullValues(this.fields.additional_accessories); }-*/;
		public final native String getIsReserve() /*-{ return $wnd.checkForNullValues(this.fields.is_reserve); }-*/;
		public final native String getProcurementDate() /*-{ return $wnd.checkForNullValues(this.fields.procurement_date); }-*/;
		public final native String getTransferDate() /*-{ return $wnd.checkForNullValues(this.fields.transfer_date); }-*/;
		public final native String getInstallationDate() /*-{ return $wnd.checkForNullValues(this.fields.installation_date); }-*/;
		public final native String getWarrantyExpirationDate() /*-{ return $wnd.checkForNullValues(this.fields.warranty_expiration_date); }-*/;
		public final native VillagesData.Type getVillage() /*-{ return this.fields.village; }-*/;
		public final native EquipmentHoldersData.Type getEquipmentHolder() /*-{ return this.fields.equipmentholder; }-*/;
		public final native String getRemarks() /*-{ return $wnd.checkForNullValues(this.fields.remarks); }-*/;
		
	
	}
	
	public class Data extends BaseData.Data {
		
		final private static String COLLECTION_PREFIX = "equipments";
			
		private String equipment_type;
		private String other_equipment;
		private String model_no;
		private String serial_no;
		private String cost;
		private String purpose;
		private String additional_accessories;
		private String is_reserve;
		private String procurement_date;
		private String transfer_date;
		private String installation_date;
		private String warranty_expiration_date;
		private VillagesData.Data village;
		private EquipmentHoldersData.Data equipmentholder;
		private String remarks;
		private String invoice_no;
		
		public Data() {
			super();
		}

		public Data(String id, String equipment_type, String other_equipment,  String invoice_no, String model_no, String serial_no, String cost,
				String purpose, String additional_accessories, String is_reserve, String procurement_date, String transfer_date,
				String installation_date, String warranty_expiration_date, VillagesData.Data village,
				EquipmentHoldersData.Data equipmentholder, String remarks) {
			super();
			this.id = id;
			this.equipment_type = equipment_type;
			this.other_equipment = other_equipment;
			this.model_no = model_no;
			this.serial_no = serial_no;
			this.cost = cost;
			this.purpose = purpose;
			this.additional_accessories = additional_accessories;
			this.is_reserve = is_reserve;
			this.procurement_date = procurement_date;
			this.transfer_date = transfer_date;
			this.installation_date = installation_date; 
			this.warranty_expiration_date = warranty_expiration_date;
			this.village = village;
			this.equipmentholder = equipmentholder;
			this.remarks = remarks;
			this.invoice_no = invoice_no;
		}
		
		public Data(String id, String equipment_type){
			super();
			this.id = id;
			this.equipment_type = equipment_type;
		}
		
		public Data(String id, String equipment_type, String model_no, String invoice_no, VillagesData.Data village, String procurement_date, String remarks){
			super();
			this.id = id;
			this.equipment_type = equipment_type; 
			this.model_no = model_no;
			this.invoice_no = invoice_no;
			this.village = village;
			this.procurement_date = procurement_date;
			this.remarks = remarks;
		}
		
		public Data(String id, String equipment_type, String model_no, String serial_no){
			super();
			this.id = id;
			this.equipment_type = equipment_type; 
			this.model_no = model_no;
			this.serial_no = serial_no;
		}
				
		public String getEquipmentType(){
			return this.equipment_type;
		}
		
		public String getOtherEquipment(){
			return this.other_equipment;
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
		
		public String getPurpose(){
			return this.purpose;
		}
		
		public String getAdditionalAccessories(){
			return this.additional_accessories;
		}
		
		public String getIsReserve(){
			return this.is_reserve;
		}
		
		public String getProcurementDate(){
			return this.procurement_date;
		}
		
		public String getTransferDate(){
			return this.transfer_date;
		}
		
		public String getInstallationDate(){
			return this.installation_date;
		}
		
		public String getWarrantyExpirationDate(){
			return this.warranty_expiration_date;
		}
		
		public VillagesData.Data getVillage(){
			return this.village;
		}
		
		public EquipmentHoldersData.Data getEquipmentHolder(){
			return this.equipmentholder;
		}
		
		public String getRemarks(){
			return this.remarks;
		}
		
		public String getInvoiceNo(){
			return this.invoice_no;
		}
		
		public BaseData.Data clone() {
			Data obj = new Data();
			obj.equipmentholder = (new EquipmentHoldersData()).new Data();
			obj.village = (new VillagesData()).new Data();
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
			} else if(key.equals("invoice_no")) {
				this.invoice_no = (String)val;
			} else if(key.equals("other_equipment")) {
				this.other_equipment = (String)val;
			} else if(key.equals("model_no")) {
				this.model_no = (String)val;
			} else if(key.equals("serial_no")) {
				this.serial_no = (String)val;
			} else if(key.equals("cost")) {
				this.cost = (String)val;
			} else if(key.equals("purpose")) {
				this.purpose = (String)val;
			} else if(key.equals("additional_accessories")) {
				this.additional_accessories = (String)val;
			} else if(key.equals("is_reserve")){
				this.is_reserve = (String)val;
			} else if(key.equals("procurement_date")) {
				this.procurement_date = (String)val;
			} else if(key.equals("transfer_date")){
				this.transfer_date = (String)val;
			} else if(key.equals("installation_date")){
				this.installation_date = (String)val;
			} else if(key.equals("warranty_expiration_date")) {
				this.warranty_expiration_date = (String)val;
			} else if(key.equals("village")) {
				VillagesData villageData = new VillagesData();
				this.village = villageData.getNewData();
				this.village.id = val;
			} else if(key.equals("equipmentholder")) {
				EquipmentHoldersData equipmentHolderData = new EquipmentHoldersData();
				this.equipmentholder = equipmentHolderData.getNewData();
				this.equipmentholder.id = val;
			} else if(key.equals("remarks")) {
				this.remarks = (String)val;
			} else {
				return;
			}
			this.addNameValueToQueryString(key, val);	 	
		}
		
		@Override
		public boolean validate() {
			//Labels to print validation error messages
			String equipmentTypeLabel = "Equipment Type";
			String otherEquipmentTypeLabel = "Other Equipment Type";
			String modelNoLabel = "Make / Model No";
			String serialNoLabel = "Serial No";
			String costLabel = "Cost";
			String additionalAccessoriesLabel = "Additional Accessories Supplied" ;
			String procurementDateLabel = "Procurement Date";
			String transferDateLabel = "Transfer from DG to Partner Date";
			String installationDateLabel = "Field Installation Date";
			String warrantyExpirationDateLabel = "Warranty Expiration Date";
			String remarksLabel = "Remarks";
			String invoiceNoLabel = "Invoice Number";
			
			StringValidator equipmentType = new StringValidator(equipmentTypeLabel,this.equipment_type, false, false);
			StringValidator otherEquipmentType = new StringValidator(otherEquipmentTypeLabel, this.other_equipment, true, false, 0, 100,true);
			StringValidator invoiceNo = new StringValidator(invoiceNoLabel, this.invoice_no, false, false, 0, 100,true);
			StringValidator ModelNo = new StringValidator(modelNoLabel, this.model_no, true, false, 0, 100,true);
			StringValidator serialNo = new StringValidator(serialNoLabel, this.serial_no, true, false, 0, 100,true);
			FloatValidator cost = new FloatValidator(costLabel, this.cost, true, true);
			StringValidator additionalAccessories = new StringValidator(additionalAccessoriesLabel,this.additional_accessories, true, false, 0, 100,true);
			DateValidator procurementDate = new DateValidator(procurementDateLabel,this.procurement_date, true, true);
			DateValidator transferDate = new DateValidator(transferDateLabel,this.transfer_date, true, true);
			DateValidator installationDate = new DateValidator(installationDateLabel,this.installation_date, true, true);
			DateValidator warrantyExpirationDate = new DateValidator(warrantyExpirationDateLabel,this.warranty_expiration_date, true, true);
			StringValidator remarks = new StringValidator(remarksLabel,this.remarks, true, false, 0, 100,true);
			ArrayList validatorList = new ArrayList();
			validatorList.add(equipmentType);
			validatorList.add(otherEquipmentType);
			validatorList.add(invoiceNo);
			validatorList.add(ModelNo);
			validatorList.add(serialNo);
			validatorList.add(cost);
			validatorList.add(additionalAccessories);
			validatorList.add(procurementDate);
			validatorList.add(transferDate);
			validatorList.add(installationDate);
			validatorList.add(warrantyExpirationDate);
			validatorList.add(remarks);
			return this.executeValidators(validatorList);
		}
		
		@Override		
		public void save() {
			EquipmentsData equipmentsDataDbApis = new EquipmentsData();
			this.id = equipmentsDataDbApis.autoInsert(this.id,
						this.equipment_type,
						this.other_equipment,
						this.invoice_no,						
						this.model_no,
						this.serial_no,
						this.cost,
						this.purpose,
						this.additional_accessories,
						this.is_reserve,
						this.procurement_date,
						this.transfer_date,
						this.installation_date,
						this.warranty_expiration_date,
						this.village.getId(),
						this.equipmentholder.getId(),
						this.remarks
						);
			this.addNameValueToQueryString("id", this.id);
		}
		
		@Override
		public String toQueryString(String id) {
			EquipmentsData equipmentsData = new EquipmentsData();
			return this.rowToQueryString(equipmentsData.getTableName(), equipmentsData.getFields(), "id", id, "");
		}
		
		
		@Override
		public String getTableId() {
			EquipmentsData equipmentsDataDbApis = new EquipmentsData();
			return equipmentsDataDbApis.tableID;
		}
	}
	
	public static String tableID = "34";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `equipment_id` " +
												"(id BIGINT UNSIGNED PRIMARY KEY  NOT NULL ," +
												"EQUIPMENT_TYPE INT  NOT NULL ," +
												"OTHER_EQUIPMENT VARCHAR(300) DEFAULT NULL," +
												"INVOICE_NO varchar(300) NOT NULL,"+
												"MODEL_NO VARCHAR(300)  NULL DEFAULT NULL ," +
												"SERIAL_NO VARCHAR(300)  NULL DEFAULT NULL ," +
												"COST FLOAT(0,0)  NULL DEFAULT NULL," +
												"PURPOSE INT DEFAULT NULL," +
												"ADDITIONAL_ACCESSORIES VARCHAR(500) NULL DEFAULT NULL," +
												"IS_RESERVE INT NULL DEFAULT 0," +
												"PROCUREMENT_DATE DATE NULL DEFAULT NULL," +
												"TRANSFER_DATE DATE NULL DEFAULT NULL," +
												"INSTALLATION_DATE NULL DEFAULT NULL," +
												"WARRANTY_EXPIRATION_DATE DATE  NULL DEFAULT NULL," +
												"VILLAGE_ID BIGINT UNSIGNED NULL DEFAULT NULL," + 
												"EQUIPMENTHOLDER_ID BIGINT UNSIGNED  NULL DEFAULT NULL, " +
												"REMARKS TEXT  NULL DEFAULT NULL, " +
												"FOREIGN KEY(VILLAGE_ID) REFERENCES village(id)," +
												"FOREIGN KEY(EQUIPMENTHOLDER_ID) REFERENCES equipment_holder(id));";
	protected static String dropTable = "DROP TABLE IF EXISTS `equipment_id`;";
	protected static String[] createIndexes = {"CREATE INDEX IF NOT EXISTS equipment_id_PRIMARY ON equipment_id(id);", 
	   "CREATE INDEX IF NOT EXISTS equipment_id_VILLAGE_ID ON equipment_id(VILLAGE_ID);",
	   "CREATE INDEX IF NOT EXISTS equipment_id_EQUIPMENTHOLDER_ID ON equipment_id(EQUIPMENTHOLDER_ID);"};
	protected static String selectEquipments = "SELECT id, EQUIPMENT_TYPE, model_no, serial_no FROM equipment_id  ORDER BY (EQUIPMENT_TYPE);";
	protected static String listEquipments = "SELECT e.id, e.equipment_type, e.model_no, e.invoice_no, v.id, v.village_name, e.procurement_date, e.remarks " +
			"FROM equipment_id e LEFT JOIN village v ON e.village_id = v.id ORDER BY (v.village_name) DESC";
	protected static String saveEquipmentOfflineURL = "/dashboard/saveequipmentoffline/";
	protected static String saveEquipmentOnlineURL = "/dashboard/saveequipmentonline/";
	protected static String getEquipmentOnlineURL = "/dashboard/getequipmentsonline/";
	protected String table_name = "equipment_id";
	protected String[] fields = {"id", "equipment_type", "other_equipment", "invoice_no","model_no", 
			"serial_no", "cost", "purpose", "additional_accessories", "is_reserve",
			"procurement_date", "transfer_date", "installation_date", "warranty_expiration_date",
			"village_id", "equipmentholder_id", "remarks"};
	
	
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
		return EquipmentsData.getEquipmentOnlineURL;
	}
	
	@Override
	public String getSaveOfflineURL(){
		return EquipmentsData.saveEquipmentOfflineURL;
	}
	
	@Override
	public String getSaveOnlineURL(){
		return EquipmentsData.saveEquipmentOnlineURL;
	}
	
	public final native JsArray<Type> asArrayOfData(String json) /*-{
		return eval(json);
	}-*/;
	
	public List serialize(JsArray<Type> equipmentObjects){
		List equipments = new ArrayList();
		EquipmentHoldersData equipmentholder = new EquipmentHoldersData();
		VillagesData village = new VillagesData();
		for(int i = 0; i < equipmentObjects.length(); i++){
			EquipmentHoldersData.Data e = equipmentholder.new Data();
			VillagesData.Data v = village.new Data();
			if(equipmentObjects.get(i).getEquipmentHolder() != null){
				e = equipmentholder.new Data(equipmentObjects.get(i).getEquipmentHolder().getPk());
			}
			if(equipmentObjects.get(i).getVillage() != null){
				v = village.new Data(equipmentObjects.get(i).getVillage().getPk(),
						equipmentObjects.get(i).getVillage().getVillageName());
			}

			Data equipment = new Data(equipmentObjects.get(i).getPk(), equipmentObjects.get(i).getEquipmentType(),
					equipmentObjects.get(i).getOtherEquipment(), equipmentObjects.get(i).getInvoiceNo(), equipmentObjects.get(i).getModelNo(),
					equipmentObjects.get(i).getSerialNo(), equipmentObjects.get(i).getCost(),
					equipmentObjects.get(i).getPurpose(), equipmentObjects.get(i).getAdditionalAccessories(),
					equipmentObjects.get(i).getIsReserve(), equipmentObjects.get(i).getProcurementDate(), 
					equipmentObjects.get(i).getTransferDate(), equipmentObjects.get(i).getInstallationDate(), 
					equipmentObjects.get(i).getWarrantyExpirationDate(),v,e,
					equipmentObjects.get(i).getRemarks());

			equipments.add(equipment);
		}
		
		return equipments;
	}
	
	@Override
	public List getListingOnline(String json){
		return this.serialize(this.asArrayOfData(json));		
	}
	
	public List getEquipmentsListingOffline(String... pageNum){
		BaseData.dbOpen();
		VillagesData village = new VillagesData();
		List equipments = new ArrayList();
		String listTemp;
		// Checking whether to return all villages or only limited number of villages
		if(pageNum.length == 0) {
			listTemp = listEquipments;
		}
		else {
			int offset = (Integer.parseInt(pageNum[0]) - 1)* pageSize;
			listTemp = listEquipments + " LIMIT "+ Integer.toString(offset) + " , "+Integer.toString(pageSize) +";";
			
			if(pageNum.length == 1) {
				listTemp = listEquipments + " LIMIT "+ Integer.toString(offset) + " , "+Integer.toString(pageSize) +";";
			} else {
				listTemp = "SELECT e.id, e.equipment_type, e.model_no, e.invoice_no, e.village_id, vil.village_name, e.procurement_date, e.remarks " +
						"FROM equipment_id e LEFT JOIN village vil  ON  vil.id= e.village_id WHERE e.equipment_type LIKE '%"+pageNum[1]+"%' " + 
									" OR e.invoice_no LIKE '%"+pageNum[1]+"%' " + 
									" OR e.procurement_date LIKE '%"+pageNum[1]+"%' " + " OR e.remarks LIKE '%"+pageNum[1]+"%' " +
									"OR vil.VILLAGE_NAME" +	" LIKE '%"+pageNum[1]+"%'" +" ORDER BY(vil.village_name) " 
									+ " LIMIT "+ Integer.toString(offset)+" , "+Integer.toString(pageSize)+ ";";
			}			
		}
		this.select(listTemp);
		if (this.getResultSet().isValidRow()){
			try {
				for (int i = 0; this.getResultSet().isValidRow(); ++i, this.getResultSet().next()) {
					VillagesData.Data v = village.new Data(this.getResultSet().getFieldAsString(4), this.getResultSet().getFieldAsString(5));
					Data equipment = new Data(this.getResultSet().getFieldAsString(0), 
							this.getResultSet().getFieldAsString(1),
							this.getResultSet().getFieldAsString(2),
							this.getResultSet().getFieldAsString(3),
							v, this.getResultSet().getFieldAsString(6), this.getResultSet().getFieldAsString(7));
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
					Data equipment = new Data(this.getResultSet().getFieldAsString(0), this.getResultSet().getFieldAsString(1),
							this.getResultSet().getFieldAsString(2), this.getResultSet().getFieldAsString(3));
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
			if(this.validate()) {
				this.save();
				return true;
			}
		}
		
		return false;
	}
	
	public Object postPageData(String id) {
		if(BaseData.isOnline()){
			this.post(RequestContext.SERVER_HOST + this.saveEquipmentOnlineURL + id + "/", this.form.getQueryString());
		}
		else{
			if(this.validate()) {
				this.save();
				return true;
			}
		}
		return false;
	}
	
	public Object getListPageData(String... pageNum){
		if(BaseData.isOnline()){
			int offset = (Integer.parseInt(pageNum[0])-1)*pageSize;
			int limit = offset+pageSize;
			if(pageNum.length > 1 ) {
				this.get(RequestContext.SERVER_HOST + EquipmentsData.getEquipmentOnlineURL +
						Integer.toString(offset)+"/"+Integer.toString(limit)+"/" + "?searchText="+pageNum[1]);
			} else {
				this.get(RequestContext.SERVER_HOST + EquipmentsData.getEquipmentOnlineURL + Integer.toString(offset)+ "/"+ Integer.toString(limit) +"/");
			}
		}
		else{
			return true;
		}
		return false;
	}	
	
	public String retrieveDataAndConvertResultIntoHtml(){
		EquipmentHoldersData equipmentHoldersData = new EquipmentHoldersData();
		List equipmentHolders = equipmentHoldersData.getAllEquipmentHoldersOffline();
		EquipmentHoldersData.Data equipmentHolder;
		String html = "<select id='id_equipmentholder' name='equipmentholder'>" +
				" <option selected='selected' value=''>---------</option>";
		
		for(int i =0; i< equipmentHolders.size(); i++){
			equipmentHolder = (EquipmentHoldersData.Data) equipmentHolders.get(i);
			html = html + "<option value = \"" + equipmentHolder.getId() + "\">" + equipmentHolder.getEquipmentHolderName() +  "</option>";
		}
		html = html + "</select>";
		
		VillagesData  villagesData = new VillagesData();
		List villages = villagesData.getAllVillagesOffline();
		VillagesData.Data village;
		html = html + "<select id='id_village' name='village'>" +
		"<option selected='selected' value=''>---------</option>";
		
		for(int i =0; i< villages.size(); i++){
			village = (VillagesData.Data)villages.get(i);
			html = html + "<option value = \"" + village.getId() + "\">" + village.getVillageName() + "</option>";
		}
		html = html + "</select>";
		
		return html;
	}

	public Object getAddPageData(){
		if(BaseData.isOnline()){
			this.get(RequestContext.SERVER_HOST + this.saveEquipmentOnlineURL);
		}
		else{
			return retrieveDataAndConvertResultIntoHtml();
		}
		return false;
	}
	
	public Object getAddPageData(String id){
		if(BaseData.isOnline()){
			this.get(RequestContext.SERVER_HOST + this.saveEquipmentOnlineURL + id + "/" );
		}
		else{
			this.form.toQueryString(id);
			return retrieveDataAndConvertResultIntoHtml();
		}
		return false;
	}
	
	public String getCount(String searchText) {
		String count = "0";//stores number of rows in a resultset
		String countSql = "SELECT COUNT(*) " +
				"FROM equipment_id e LEFT JOIN village vil  ON  vil.id= e.village_id " +
				"WHERE  (e.village_id = vil.id OR e.village_id is null) AND (e.equipment_type LIKE '%"+searchText+"%' " + 
									" OR e.invoice_no LIKE '%"+searchText+"%' " + 
									" OR e.procurement_date LIKE '%"+searchText+"%' " + " OR e.remarks LIKE '%"+searchText+"%' " +
									"OR vil.VILLAGE_NAME" +	" LIKE '%"+searchText+"%' );" ;
		BaseData.dbOpen();
		this.select(countSql);
		if(this.getResultSet().isValidRow()) {
			try {
				count = getResultSet().getFieldAsString(0);
			} catch (DatabaseException e) {
				Window.alert("Database Exception"+e.toString());
			}
		}
		BaseData.dbClose();
		return count;
	}
	

}
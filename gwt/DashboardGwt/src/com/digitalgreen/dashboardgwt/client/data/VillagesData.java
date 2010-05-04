package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.VideosData.Data;
import com.digitalgreen.dashboardgwt.client.data.validation.DateValidator;
import com.digitalgreen.dashboardgwt.client.data.validation.IntegerValidator;
import com.digitalgreen.dashboardgwt.client.data.validation.StringValidator;
import com.digitalgreen.dashboardgwt.client.data.validation.UniqueConstraintValidator;
import com.google.gwt.core.client.JsArray;
import com.google.gwt.gears.client.database.DatabaseException;
import com.google.gwt.user.client.Window;

public class VillagesData extends BaseData {

	public static class Type extends BaseData.Type{
		protected Type() {}
		public final native String getVillageName() /*-{ return $wnd.checkForNullValues(this.fields.village_name); }-*/;
		public final native BlocksData.Type getBlock() /*-{ return this.fields.block }-*/;
		public final native String getNoOfHouseholds() /*-{ return this.fields.no_of_households }-*/;
		public final native String getPopulation() /*-{ return this.fields.population }-*/;
		public final native String getRoadConnectivity() /*-{ return this.fields.road_connectivity }-*/;
		public final native String getControl() /*-{ return $wnd.checkForNullValues(this.fields.control); }-*/;
		public final native String getStartDate() /*-{ return $wnd.checkForNullValues(this.fields.start_date);}-*/;
	}
	
	public class Data extends BaseData.Data {
		
		final private static String COLLECTION_PREFIX = "village";
		
		private String village_name;
	    private BlocksData.Data block; 
	    private String no_of_households;
	    private String population;
	    private String road_connectivity;
	    private String control; 
	    private String start_date; 
		
		public Data() {
			super();
		}

		public Data(String id, String village_name) {
			super();
			this.id = id;
			this.village_name = village_name;
		}

		public Data(String id, String village_name, BlocksData.Data block) {
			super();
			this.id = id;
			this.village_name = village_name;
			this.block = block;
		}
		
		public Data(String id, String village_name , BlocksData.Data block, 
				String no_of_households, String population, String road_connectivity, 
				String control, String start_date) {
			super();
			this.id = id;
			this.village_name = village_name;
			this.block = block;
			this.no_of_households = no_of_households;
			this.population = population;
			this.road_connectivity = road_connectivity;
			this.control = control;
			this.start_date = start_date;
		}
		
		public String getVillageName(){
			return this.village_name;
		}
		
		public BlocksData.Data getBlock(){
			return this.block;
		}
		
		@Override
		public BaseData.Data clone() {
			Data obj = new Data();
			obj.block = (new BlocksData()).new Data();
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
			} else if(key.equals("village_name")) {
				this.village_name = val;
			} else if(key.equals("block")) {
				BlocksData block = new BlocksData();
				this.block = block.getNewData();
				this.block.id = val;
			} else if(key.equals("no_of_households")) {
				this.no_of_households = val;
			} else if(key.equals("population")) {
				this.population = val;
			} else if(key.equals("road_connectivity")) {
				this.road_connectivity = val;
			} else if(key.equals("control")) {
				this.control = val;
			} else if(key.equals("start_date")) {
				this.start_date = val;
			} else {
				return;
			}
			this.addNameValueToQueryString(key, val);
		}
		
		@Override
		public boolean validate(){
			StringValidator villageName = new StringValidator(this.village_name,false,false,0,100);
			villageName.setError("Village Name is a required field and is less than 100 characters.");
			StringValidator blockValidator = new StringValidator(this.block.getId(), false, false, 1, 100);
			blockValidator.setError("Please make sure you choose a block for 'Block'.");
			IntegerValidator noOfHouseHolds = new IntegerValidator(this.no_of_households,true,true);
			noOfHouseHolds.setError("Please enter integer for No Of Households");
			IntegerValidator population = new IntegerValidator(this.population,true,true);
			population.setError("Please enter integer for population");
			StringValidator roadConnectivity = new StringValidator(this.road_connectivity,true,true,0,100);
			roadConnectivity.setError("Please make sure that road connectivity is less than 100 characters.");
			DateValidator startDate = new DateValidator(this.start_date, true, true);
			startDate.setError("Please make sure 'Start date' is formatted as YYYY-MM-DD.");
			ArrayList village_name = new ArrayList();
			village_name.add("village_name");
			village_name.add(this.village_name);
			ArrayList blockID = new ArrayList();
			blockID.add("block_id");
			blockID.add(this.block.getId());
			ArrayList uniqueVillage = new ArrayList();
			uniqueVillage.add(village_name);
			ArrayList villageBllockID = new ArrayList();
			villageBllockID.add(village_name);
			villageBllockID.add(blockID);
			UniqueConstraintValidator uniqueVillageBlockID = new UniqueConstraintValidator(villageBllockID, new VillagesData());
			uniqueVillageBlockID.setError("The Village and Block pair is already in the system.  Please make sure it is unique.");
			uniqueVillageBlockID.setCheckId(this.getId());
			
			ArrayList validatorList = new ArrayList();
			validatorList.add(villageName);
			validatorList.add(blockValidator);
			validatorList.add(noOfHouseHolds);
			validatorList.add(population);
			validatorList.add(roadConnectivity);
			validatorList.add(startDate);
			validatorList.add(uniqueVillageBlockID);
			return this.executeValidators(validatorList);
		}
		
		@Override
		public void save() {
			VillagesData villagesDataDbApis = new VillagesData();
			this.id = villagesDataDbApis.autoInsert(this.id,
					this.village_name, 
					this.block.getId(),  
					this.no_of_households,  
					this.population, 
					this.road_connectivity, 
					this.control, 
					this.start_date);
			this.addNameValueToQueryString("id", this.id);
		}
		
		@Override
		public String toQueryString(String id) {
			VillagesData villageData = new VillagesData();
			return this.rowToQueryString(villageData.getTableName(), villageData.getFields(), "id", id, "");
		}
		
		@Override
		public String getTableId() {
			VillagesData villagesDataDbApis = new VillagesData();
			return villagesDataDbApis.tableID;
		}
	}
	
	public static String tableID = "17";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `village` " +
												"(id INTEGER PRIMARY KEY  NOT NULL ," +
												"VILLAGE_NAME VARCHAR(100)  NOT NULL ," +
												"block_id INT  NOT NULL DEFAULT 0," +
												"NO_OF_HOUSEHOLDS INT  NULL DEFAULT NULL," +
												"POPULATION INT  NULL DEFAULT NULL," +
												"ROAD_CONNECTIVITY VARCHAR(100)  NULL ," +
												"CONTROL SMALLINT  NULL DEFAULT NULL," +
												"START_DATE DATE  NULL DEFAULT NULL, " +
												"FOREIGN KEY(block_id) REFERENCES block(id)); ";  
	protected static String dropTable = "DROP TABLE IF EXISTS `village`;";
	protected static String selectVillages = "SELECT id, village_name FROM village ORDER BY(village_name)";
	protected static String listVillages = "SELECT village.id, village.village_name, block.id, block.block_name FROM village JOIN block ON village.block_id = block.id ORDER BY(-village.id)";
	protected static String saveVillageOnlineURL = "/dashboard/savevillageonline/";
	protected static String getVillageOnlineURL = "/dashboard/getvillagesonline/";
	protected static String saveVillageOfflineURL = "/dashboard/savevillageoffline/";
	protected String[] fields = {"id", "village_name", "block_id", "no_of_households", "population",
			"road_connectivity", "control", "start_date"};
	protected String table_name = "village";
	
	public VillagesData() {
		super();
	}
	
	public VillagesData(OnlineOfflineCallbacks callbacks) {
		super(callbacks);
	}
	
	public VillagesData(OnlineOfflineCallbacks callbacks, Form form) {
		super(callbacks, form);
	}

	@Override
	public Data getNewData() {
		return new Data();
	}
	
	@Override
	protected String getTableId() {
		return VillagesData.tableID;
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
		return VillagesData.getVillageOnlineURL;
	}
	
	@Override
	public String getSaveOfflineURL(){
		return VillagesData.saveVillageOfflineURL;
	}
	
	@Override
	public String getSaveOnlineURL(){
		return VillagesData.saveVillageOnlineURL;
	}

	public final native JsArray<Type> asArrayOfData(String json) /*-{
		return eval(json);
	}-*/;

	
	public List serialize(JsArray<Type> villageObjects){
        List villages = new ArrayList();
        BlocksData block = new BlocksData();
        for(int i = 0; i < villageObjects.length(); i++){
                BlocksData.Data b = block.new Data(villageObjects.get(i).getBlock().getPk(),
                                villageObjects.get(i).getBlock().getBlockName());
                VillagesData.Data village = new Data(villageObjects.get(i).getPk(),
                                villageObjects.get(i).getVillageName(), b,
                                villageObjects.get(i).getNoOfHouseholds(),
                                villageObjects.get(i).getPopulation(),
                                villageObjects.get(i).getRoadConnectivity(),
                                villageObjects.get(i).getControl(),
                                villageObjects.get(i).getStartDate());
                villages.add(village);
        }
        return villages;
	}


	@Override
	public List getListingOnline(String json){
		return this.serialize(this.asArrayOfData(json));		
	}

	public List getVillagesListingOffline(){
		BaseData.dbOpen();
		List villages = new ArrayList();
		BlocksData block = new BlocksData();
		this.select(listVillages);
		if (this.getResultSet().isValidRow()){
			try {
				for (int i = 0; this.getResultSet().isValidRow(); ++i, this.getResultSet().next()) {
					BlocksData.Data b = block.new Data(this.getResultSet().getFieldAsString(2), this.getResultSet().getFieldAsString(3));
					Data village = new Data(this.getResultSet().getFieldAsString(0), this.getResultSet().getFieldAsString(1), b);
					villages.add(village);
				}				
			} catch (DatabaseException e) {
				Window.alert("Database Exception : " + e.toString());
				// TODO Auto-generated catch block
				BaseData.dbClose();
			}
		}
		BaseData.dbClose();
		return villages;
	}
	
	public List getAllVillagesOffline(){
		BaseData.dbOpen();
		List villages = new ArrayList();
		this.select(selectVillages);
		if (this.getResultSet().isValidRow()){
			try {
				for (int i = 0; this.getResultSet().isValidRow(); ++i, this.getResultSet().next()) {
					Data village = new Data(this.getResultSet().getFieldAsString(0), this.getResultSet().getFieldAsString(1));
					villages.add(village);
				}				
			} catch (DatabaseException e) {
				Window.alert("Database Exception : " + e.toString());
				// TODO Auto-generated catch block
				BaseData.dbClose();
			}
		}
		BaseData.dbClose();
		return villages;
	}

	public Object postPageData() {
		if(BaseData.isOnline()){
			this.post(RequestContext.SERVER_HOST + this.saveVillageOnlineURL, this.form.getQueryString());
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
			this.post(RequestContext.SERVER_HOST + this.saveVillageOnlineURL + id + "/", this.form.getQueryString());
		}
		else{
			if(this.validate()) {
				this.save();
				return true;
			}
		}
		return false;
	}
	
	public Object getListPageData(){
		if(BaseData.isOnline()){
			this.get(RequestContext.SERVER_HOST + this.getVillageOnlineURL);
		}
		else{
			return true;
		}
		return false;
	}
	
	public Object getAddPageData(String id){
		if(BaseData.isOnline()){
			this.get(RequestContext.SERVER_HOST + this.saveVillageOnlineURL + id + "/" );
		}
		else {
			this.form.toQueryString(id);
			return retrieveDataAndConvertResultIntoHtml();
		}
		return false;
	}

	public String retrieveDataAndConvertResultIntoHtml(){
		BlocksData blockData = new BlocksData();
		List blocks = blockData.getAllBlocksOffline();
		BlocksData.Data block;
		String html = "<select name=\"block\" id=\"id_block\">" + 
					"<option value='' selected='selected'>---------</option>";
		for(int i=0; i< blocks.size(); i++){
			block = (BlocksData.Data)blocks.get(i);
			html = html + "<option value = \"" + block.getId() +"\">" + block.getBlockName() + "</option>";
		}
		html = html + "</select>";
		
		PartnersData partnerData = new PartnersData();
		List partners = partnerData.getAllPartnersOffline();
		PartnersData.Data partner;
		for(int inline = 0; inline < 5; inline++){
			html += "<select name=\"animator_set-" + inline + "-partner\" id=\"id_animator_set-" + inline +"-partner\">";
			html += "<option value = \"\">" + "---------" + "</option>";
			for(int i=0; i< partners.size(); i++){
				partner = (PartnersData.Data)partners.get(i);
				html = html + "<option value = \"" + partner.getId() +"\">" + partner.getPartnerName() + "</option>";
			}
			html = html + "</select>";
		}
		return html;
	}
	
	public Object getAddPageData(){
		if(BaseData.isOnline()){
			this.get(RequestContext.SERVER_HOST + this.saveVillageOnlineURL);
		}
		else{
			return retrieveDataAndConvertResultIntoHtml();
		}
		return false;
	}
}
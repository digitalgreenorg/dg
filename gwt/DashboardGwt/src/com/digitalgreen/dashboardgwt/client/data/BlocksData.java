package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;
import java.util.List;
import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.validation.DateValidator;
import com.digitalgreen.dashboardgwt.client.data.validation.StringValidator;
import com.google.gwt.core.client.JsArray;
import com.google.gwt.gears.client.database.DatabaseException;
import com.google.gwt.user.client.Window;

public class BlocksData extends BaseData {

	public static class Type extends BaseData.Type {
		protected Type() {
		}

		public final native String getBlockName() /*-{
			return $wnd.checkForNullValues(this.fields.block_name);
		}-*/;

		public final native String getStartDate() /*-{
			return $wnd.checkForNullValues(this.fields.start_date);
		}-*/;

		public final native DistrictsData.Type getDistrict() /*-{
			return this.fields.district;
		}-*/;
	}

	public class Data extends BaseData.Data {

		final protected static String COLLECTION_PREFIX = "block";

		private String block_name;
		private String start_date;
		private DistrictsData.Data district;

		public Data() {
			super();
		}

		public Data(String id, String block_name, String start_date,
				DistrictsData.Data district) {
			super();
			this.id = id;
			this.block_name = block_name;
			this.start_date = start_date;
			this.district = district;
		}

		public Data(String id, String block_name) {
			super();
			this.id = id;
			this.block_name = block_name;
		}

		public String getBlockName() {
			return this.block_name;
		}

		public String getStartDate() {
			return this.start_date;
		}

		public DistrictsData.Data getDistrict() {
			return this.district;
		}

		@Override
		public BaseData.Data clone() {
			Data obj = new Data();
			obj.district = (new DistrictsData()).new Data();
			return obj;
		}

		@Override
		public String getPrefixName() {
			return Data.COLLECTION_PREFIX;
		}

		@Override
		public void setObjValueFromString(String key, String val) {
			super.setObjValueFromString(key, val);
			if (key.equals("block_name")) {
				this.block_name = (String) val;
			} else if (key.equals("start_date")) {
				this.start_date = (String) val;
			} else if (key.equals("district")) {
				DistrictsData district1 = new DistrictsData();
				this.district = district1.getNewData();
				this.district.id = val;
			} else {
				return;
			}
			this.addNameValueToQueryString(key, val);
		}

		@Override
		public boolean validate() {
			StringValidator blockName = new StringValidator(this.block_name, false, false, 1, 100);
			blockName.setError("Please make sure that 'Block Name' is NOT EMPTY and not more then 100 CHARACTERS");
			DateValidator startDate = new DateValidator(this.start_date, true, true);
			startDate.setError("Please make sure 'Start date' is formatted as 'YYYY-MM-DD'.");
			StringValidator districtValidator = new StringValidator(this.district.getId(), false, false, 1, 100);
			districtValidator.setError("Please make sure you choose a village for 'District'.");
			ArrayList validatorList = new ArrayList();
			validatorList.add(blockName);
			validatorList.add(startDate);
			validatorList.add(districtValidator);
			return this.executeValidators(validatorList);
		}

		@Override
		public void save() {
			BlocksData blocksDataDbApis = new BlocksData();
			this.id = blocksDataDbApis.autoInsert(this.id, this.block_name,
					this.start_date, this.district.getId());
			this.addNameValueToQueryString("id", this.id);
		}

		@Override
		public String getTableId() {
			BlocksData blocksDataDbApis = new BlocksData();
			return blocksDataDbApis.tableID;
		}
	}

	public static String tableID = "16";
	final protected static String createTable = "CREATE TABLE IF NOT EXISTS `block` "
			+ "(id INTEGER PRIMARY KEY  NOT NULL ,"
			+ "BLOCK_NAME VARCHAR(100)  NOT NULL ,"
			+ "START_DATE DATE  NULL DEFAULT NULL,"
			+ "district_id INT  NOT NULL DEFAULT 0, "
			+ "FOREIGN KEY(district_id) REFERENCES district(id));";
	protected static String dropTable = "DROP TABLE IF EXISTS `block`;";
	protected static String selectBlocks = "SELECT id, BLOCK_NAME FROM block ORDER BY (block_name);";
	protected static String listBlocks = "SELECT block.id, block.BLOCK_NAME, block.START_DATE, district.id, district.DISTRICT_NAME FROM block JOIN district ON block.district_id = district.id ORDER BY (-block.id);";
	protected static String saveBlockOnlineURL = "/dashboard/saveblockonline/";
	protected static String getBlockOnlineURL = "/dashboard/getblocksonline/";
	protected static String saveBlockOfflineURL = "/dashboard/saveblockoffline/";
	protected String table_name = "block";
	protected String[] fields = { "id", "block_name", "start_date",
			"district_id" };

	public BlocksData() {
		super();
	}

	public BlocksData(OnlineOfflineCallbacks callbacks) {
		super(callbacks);
	}

	public BlocksData(OnlineOfflineCallbacks callbacks, Form form) {
		super(callbacks, form);
	}

	@Override
	public Data getNewData() {
		return new Data();
	}

	@Override
	protected String getTableId() {
		return BlocksData.tableID;
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
	protected String getCreateTableSql(){
		return this.createTable;
	}
	
	@Override
	protected String getDeleteTableSql(){
		return this.dropTable;
	}
	
	@Override
	public String getListingOnlineURL() {
		return BlocksData.getBlockOnlineURL;
	}

	@Override
	public String getSaveOfflineURL() {
		return BlocksData.saveBlockOfflineURL;
	}

	public final native JsArray<Type> asArrayOfData(String json) /*-{
		return eval(json);
	}-*/;

	public List serialize(JsArray<Type> blockObjects) {
		List blocks = new ArrayList();
		DistrictsData district = new DistrictsData();

		for (int i = 0; i < blockObjects.length(); i++) {

			DistrictsData.Data d = district.new Data(blockObjects.get(i)
					.getDistrict().getPk(), blockObjects.get(i).getDistrict()
					.getDistrictName());

			Data block = new Data(blockObjects.get(i).getPk(), blockObjects
					.get(i).getBlockName(), blockObjects.get(i).getStartDate(),
					d);

			blocks.add(block);
		}
		return blocks;
	}

	public List getListingOnline(String json) {
		return this.serialize(this.asArrayOfData(json));
	}

	public List getBlocksListingOffline() {
		BaseData.dbOpen();
		List blocks = new ArrayList();
		DistrictsData district = new DistrictsData();
		this.select(listBlocks);
		if (this.getResultSet().isValidRow()) {
			try {
				for (int i = 0; this.getResultSet().isValidRow(); ++i, this
						.getResultSet().next()) {

					DistrictsData.Data d = district.new Data(this
							.getResultSet().getFieldAsString(3), this
							.getResultSet().getFieldAsString(4));

					Data block = new Data(this.getResultSet().getFieldAsString(
							0), this.getResultSet().getFieldAsString(1), this
							.getResultSet().getFieldAsString(2), d);

					blocks.add(block);
				}
			} catch (DatabaseException e) {
				Window.alert("Database Exception : " + e.toString());
				BaseData.dbClose();
			}
		}
		BaseData.dbClose();
		return blocks;
	}

	public List getAllBlocksOffline() {
		BaseData.dbOpen();
		List blocks = new ArrayList();
		this.select(selectBlocks);
		if (this.getResultSet().isValidRow()) {
			try {
				for (int i = 0; this.getResultSet().isValidRow(); ++i, this
						.getResultSet().next()) {
					Data block = new Data(this.getResultSet().getFieldAsString(
							0), this.getResultSet().getFieldAsString(1));
					blocks.add(block);
				}
			} catch (DatabaseException e) {
				Window.alert("Database Exception : " + e.toString());
				BaseData.dbClose();
			}
		}
		BaseData.dbClose();
		return blocks;
	}

	public Object postPageData() {
		if (BaseData.isOnline()) {
			this
					.post(RequestContext.SERVER_HOST
							+ BlocksData.saveBlockOnlineURL, this.form
							.getQueryString());
		} else {
			if (this.validate()) {
				this.save();
				return true;
			}
		}
		return false;
	}

	public Object getListPageData() {
		if (BaseData.isOnline()) {
			this.get(RequestContext.SERVER_HOST + BlocksData.getBlockOnlineURL);
		} else {
			return true;
		}
		return false;
	}

	public String retrieveDataAndConvertResultIntoHtml() {
		DistrictsData districtData = new DistrictsData();
		List districts = districtData.getAllDistrictsOffline();
		DistrictsData.Data district;
		String html = "<select name=\"district\" id=\"id_district\">"
				+ "<option value='' selected='selected'>---------</option>";
		for (int i = 0; i < districts.size(); i++) {
			district = (DistrictsData.Data) districts.get(i);
			html = html + "<option value = \"" + district.getId() + "\">"
					+ district.getDistrictName() + "</option>";
		}
		html = html + "</select>";
		return html;
	}

	public Object getAddPageData() {
		if (BaseData.isOnline()) {
			this
					.get(RequestContext.SERVER_HOST
							+ BlocksData.saveBlockOnlineURL);
		} else {
			return retrieveDataAndConvertResultIntoHtml();
		}
		return false;
	}
}
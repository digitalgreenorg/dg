package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;
import java.util.List;
import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.validation.DateValidator;
import com.digitalgreen.dashboardgwt.client.data.validation.IntegerValidator;
import com.digitalgreen.dashboardgwt.client.data.validation.StringValidator;
import com.digitalgreen.dashboardgwt.client.data.validation.UniqueConstraintValidator;
import com.google.gwt.core.client.JsArray;
import com.google.gwt.gears.client.database.DatabaseException;
import com.google.gwt.user.client.Window;

public class AnimatorsData extends BaseData {

	public static class Type extends BaseData.Type {
		protected Type() {
		}

		public final native String getAnimatorName() /*-{
			return $wnd.checkForNullValues(this.fields.name);
		}-*/;

		public final native String getAge() /*-{
			return $wnd.checkForNullValues(this.fields.age);
		}-*/;

		public final native String getGender() /*-{
			return $wnd.checkForNullValues(this.fields.gender);
		}-*/;

		public final native String getCSPFlags() /*-{
			return $wnd.checkForNullValues(this.fields.csp_flag);
		}-*/;

		public final native String getCameraOperatorFlag() /*-{
			return $wnd.checkForNullValues(this.fields.camera_operator_flag);
		}-*/;

		public final native String getFacilitatorFlag() /*-{
			return $wnd.checkForNullValues(this.fields.facilitator_flag);
		}-*/;

		public final native String getPhoneNo() /*-{
			return $wnd.checkForNullValues(this.fields.phone_no);
		}-*/;

		public final native String getAddress() /*-{
			return $wnd.checkForNullValues(this.fields.address);
		}-*/;

		public final native PartnersData.Type getPartner() /*-{
			return this.fields.partner;
		}-*/;

		public final native VillagesData.Type getVillage() /*-{
			return this.fields.village;
		}-*/;


	}

	public class Data extends BaseData.Data {

		final private static String COLLECTION_PREFIX = "animator";

		private String name;
		private String age;
		private String gender;
		private String csp_flag;
		private String camera_operator_flag;
		private String facilitator_flag;
		private String phone_no;
		private String address;
		private PartnersData.Data partner;
		private VillagesData.Data village;

		public Data() {
			super();
		}

		public Data(String id) {
			super();
			this.id = id;
		}

		public Data(String id, String name) {
			super();
			this.id = id;
			this.name = name;
		}
		
		public Data(String id, String name, VillagesData.Data village) {
			super();
			this.id = id;
			this.name = name;
			this.village = village;
		}

		public Data(String id, String name, PartnersData.Data partner,
				VillagesData.Data village) {
			super();
			this.id = id;
			this.name = name;
			this.partner = partner;
			this.village = village;
		}

		public Data(String id, String name, String age, String gender,
				String csp_flag, String camera_operator_flag,
				String facilitator_flag, String phone_no, String address,
				PartnersData.Data partner, VillagesData.Data village) {
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
		}

		public String getAnimatorName() {
			return this.name;
		}

		public String getAge() {
			return this.age;
		}

		public String getGender() {
			return this.gender;
		}

		public String getCSPFlag() {
			return this.csp_flag;
		}

		public String getCameraOperatorFlag() {
			return this.camera_operator_flag;
		}

		public String getFacilitatorFlag() {
			return this.facilitator_flag;
		}

		public String getPhoneNo() {
			return this.phone_no;
		}

		public String getAddress() {
			return this.address;
		}

		public PartnersData.Data getPartner() {
			return this.partner;
		}

		public VillagesData.Data getVillage() {
			return this.village;
		}


		@Override
		public String getPrefixName() {
			return Data.COLLECTION_PREFIX;
		}

		@Override
		public BaseData.Data clone() {
			Data obj = new Data();
			obj.partner = (new PartnersData()).new Data();
			obj.village = (new VillagesData()).new Data();
			return obj;
		}

		@Override
		public void setObjValueFromString(String key, String val) {
			super.setObjValueFromString(key, val);
			if (key.equals("id")) {
				this.id = val;
			} else if (key.equals("name")) {
				this.name = val;
			} else if (key.equals("age")) {
				this.age = val;
			} else if (key.equals("gender")) {
				this.gender = val;
			} else if (key.equals("csp_flag")) {
				this.csp_flag = val;
			} else if (key.equals("camera_operator_flag")) {
				this.camera_operator_flag = val;
			} else if (key.equals("facilitator_flag")) {
				this.facilitator_flag = val;
			} else if (key.equals("phone_no")) {
				this.phone_no = val;
			} else if (key.equals("address")) {
				this.address = val;
			} else if (key.equals("partner")) {
				PartnersData partner = new PartnersData();
				this.partner = partner.getNewData();
				this.partner.id = val;
			} else if (key.equals("village")) {
				VillagesData village = new VillagesData();
				this.village = village.getNewData();
				this.village.id = val;
			} else {
				return;
			}
			this.addNameValueToQueryString(key, val);
		}

		@Override
		public boolean validate() {
			StringValidator name = new StringValidator(this.name, false, false,	0, 100, true);
			name.setError("Name is a required field and please make sure 'name' is less than 100 characters and does not contain special characters.");
			IntegerValidator age = new IntegerValidator(this.age, true, true, 0, 100);
			age.setError("Please enter a valid age");
			StringValidator gender = new StringValidator(this.gender, false, false, 0, 10);
			gender.setError("Please select gender");
			StringValidator phoneNo = new StringValidator(this.phone_no, true, true, 0, 100, true);
			phoneNo.setError("Please make sure that phone number is valid and does not contain special characters.");
			StringValidator address = new StringValidator(this.address, true, true, 0, 500);
			address.setError("Please make sure that 'address' is less than 500 characters");
			StringValidator villageValidator = new StringValidator(this.village.getId(), false, false, 1, 100);
			villageValidator.setError("Please make sure you choose a village for 'Village'.");
			StringValidator partnerValidator = new StringValidator(this.partner.getId(), false, false, 1, 100);
			partnerValidator.setError("Please make sure you choose a partner for 'Partner'.");
			
			ArrayList unqName = new ArrayList();
			unqName.add("name");
			unqName.add(this.name);
			ArrayList unqGender = new ArrayList();
			unqGender.add("gender");
			unqGender.add(this.gender);
			ArrayList unqPartner = new ArrayList();
			unqPartner.add("partner_id");
			unqPartner.add(this.partner.getId());
			ArrayList unqVillage = new ArrayList();
			unqVillage.add("village_id");
			unqVillage.add(this.village.getId());
			
			ArrayList uniqueTogether = new ArrayList();
			uniqueTogether.add(unqName);
			uniqueTogether.add(unqGender);
			uniqueTogether.add(unqPartner);
			uniqueTogether.add(unqVillage);
			
			UniqueConstraintValidator uniqueNameGenderPartnerVillage = new UniqueConstraintValidator(uniqueTogether, new AnimatorsData());
			uniqueNameGenderPartnerVillage.setError("The Name, Gender, Partner and Home Village are already in the system.  Please make sure they are unique.");
			uniqueNameGenderPartnerVillage.setCheckId(this.getId());
			
			ArrayList validatorList = new ArrayList();
			validatorList.add(name);
			validatorList.add(age);
			validatorList.add(gender);
			validatorList.add(phoneNo);
			validatorList.add(address);
			validatorList.add(villageValidator);
			validatorList.add(partnerValidator);
			validatorList.add(uniqueNameGenderPartnerVillage);
			return this.executeValidators(validatorList);
		}

		@Override
		public boolean validate(BaseData.Data foreignkey) {
			StringValidator name = new StringValidator(this.name, false, false,	0, 100);
			name.setError("Name is a required field and please make sure 'name' is less than 100 characters.");
			IntegerValidator age = new IntegerValidator(this.age, true, true, 0, 100);
			age.setError("Please enter a valid age");
			StringValidator gender = new StringValidator(this.gender, false, false, 0, 10);
			gender.setError("Please select gender");
			StringValidator phoneNo = new StringValidator(this.phone_no, true, true, 0, 100);
			phoneNo.setError("Please make sure that phone number is valid");
			StringValidator address = new StringValidator(this.address, true, true, 0, 500);
			address.setError("Please make sure that 'address' is less than 500 characters");
			StringValidator partnerValidator = new StringValidator(this.partner.getId(), false, false, 1, 100);
			partnerValidator.setError("Please make sure you choose a partner for 'Partner'.");
			
			ArrayList unqName = new ArrayList();
			unqName.add("name");
			unqName.add(this.name);
			ArrayList unqGender = new ArrayList();
			unqGender.add("gender");
			unqGender.add(this.gender);
			ArrayList unqPartner = new ArrayList();
			unqPartner.add("partner_id");
			unqPartner.add(this.partner.getId());
			ArrayList unqVillage = new ArrayList();

			ArrayList uniqueTogether = new ArrayList();
			uniqueTogether.add(unqName);
			uniqueTogether.add(unqGender);
			uniqueTogether.add(unqPartner);
			
			UniqueConstraintValidator uniqueNameGenderPartnerVillage = new UniqueConstraintValidator(uniqueTogether, new AnimatorsData());
			uniqueNameGenderPartnerVillage.setError("The Name, Gender, Partner and Home Village are already in the system.  Please make sure they are unique.");
			uniqueNameGenderPartnerVillage.setCheckId(this.getId());
			
			ArrayList validatorList = new ArrayList();
			validatorList.add(name);
			validatorList.add(age);
			validatorList.add(gender);
			validatorList.add(phoneNo);
			validatorList.add(address);
			validatorList.add(partnerValidator);
			validatorList.add(uniqueNameGenderPartnerVillage);
			return this.executeValidators(validatorList);
		}

		@Override
		public void save() {
			AnimatorsData animatorsDataDbApis = new AnimatorsData();
			this.id = animatorsDataDbApis.autoInsert(this.id, this.name,
					this.age, this.gender, this.csp_flag,
					this.camera_operator_flag, this.facilitator_flag,
					this.phone_no, this.address, this.partner.getId(),
					this.village.getId());
			this.addNameValueToQueryString("id", this.id);
		}

		@Override
		public void save(BaseData.Data foreignKey) {
			AnimatorsData animatorsDataDbApis = new AnimatorsData();
			this.id = animatorsDataDbApis.autoInsert(this.id, this.name,
					this.age, this.gender, this.csp_flag,
					this.camera_operator_flag, this.facilitator_flag,
					this.phone_no, this.address, this.partner.getId(),
					foreignKey.getId());
			this.addNameValueToQueryString("id", this.id);
			this.addNameValueToQueryString("village", foreignKey.getId());
		}

		@Override
		public String toQueryString(String id) {
			AnimatorsData animatorsData = new AnimatorsData();
			return rowToQueryString(animatorsData.getTableName(), animatorsData.getFields(), 
					"id", id, "");
		}

		@Override
		public String toInlineQueryString(String id) {
			AnimatorsData animatorsData = new AnimatorsData();
			return rowToQueryString(animatorsData.getTableName(), animatorsData.getFields(), 
					"village_id", id, this.COLLECTION_PREFIX + "_set");
		}
		
		@Override
		public String getTableId() {
			AnimatorsData animatorsDataDbApis = new AnimatorsData();
			return animatorsDataDbApis.tableID;
		}
	}

	public static String tableID = "22";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `animator` " +
											"(id BIGINT UNSIGNED PRIMARY KEY  NOT NULL ," +
											"NAME VARCHAR(100)  NOT NULL ," +
											"AGE INT  NULL DEFAULT NULL," +
											"GENDER VARCHAR(1)  NOT NULL ," +
											"CSP_FLAG SMALLINT  NULL DEFAULT NULL," +
											"CAMERA_OPERATOR_FLAG SMALLINT  NULL DEFAULT NULL," +
											"FACILITATOR_FLAG SMALLINT  NULL DEFAULT NULL," +
											"PHONE_NO VARCHAR(100) NULL DEFAULT NULL," +
											"ADDRESS VARCHAR(500)  NULL DEFAULT NULL," +
											"partner_id BIGINT UNSIGNED  NOT NULL DEFAULT 0," +
											"village_id BIGINT UNSIGNED  NOT NULL DEFAULT 0," +
											"FOREIGN KEY(partner_id) REFERENCES partners(id), " +
											"FOREIGN KEY(village_id) REFERENCES village(id));";
	protected static String dropTable = "DROP TABLE IF EXISTS `animator`;";
	protected static String selectAnimators = "SELECT animator.id, animator.name FROM animator ORDER BY (animator.NAME);";
	protected static String selectAnimatorsWithVillage = "SELECT animator.id, animator.NAME, village.id, village.VILLAGE_NAME " +
			"FROM animator JOIN village ON animator.village_id = village.id ORDER BY (animator.NAME);";
	protected static String listAnimators = "SELECT a.id, a.name,p.id,p.partner_name,vil.id,vil.village_name "
			+ "FROM animator a,partners p,village vil WHERE  a.partner_id = p.id and a.village_id = vil.id ORDER BY LOWER(a.name)";
	protected static String saveAnimatorOnlineURL = "/dashboard/saveanimatoronline/";
	protected static String saveAnimatorOfflineURL = "/dashboard/saveanimatoroffline/";
	protected static String getAnimatorsOnlineURL = "/dashboard/getanimatorsonline/";
	protected String table_name = "animator";
	protected String[] fields = { "id", "name", "age", "gender", "csp_flag",
			"camera_operator_flag", "facilitator_flag", "phone_no", "address",
			"partner_id", "village_id" };

	public AnimatorsData() {
		super();
	}

	public AnimatorsData(OnlineOfflineCallbacks callbacks) {
		super(callbacks);
	}

	public AnimatorsData(OnlineOfflineCallbacks callbacks, Form form) {
		super(callbacks, form);
	}

	@Override
	public Data getNewData() {
		return new Data();
	}

	@Override
	protected String getTableId() {
		return AnimatorsData.tableID;
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
	public String getListingOnlineURL() {
		return AnimatorsData.getAnimatorsOnlineURL;
	}

	@Override
	public String getSaveOfflineURL() {
		return AnimatorsData.saveAnimatorOfflineURL;
	}
	
	@Override
	public String getSaveOnlineURL() {
		return AnimatorsData.saveAnimatorOnlineURL;
	}

	public final native JsArray<Type> asArrayOfData(String json) /*-{
		return eval(json);
	}-*/;

	public List serialize(JsArray<Type> animatorObjects) {
		List animators = new ArrayList();
		PartnersData partner = new PartnersData();
		VillagesData village = new VillagesData();
		for (int i = 0; i < animatorObjects.length(); i++) {
			PartnersData.Data p = partner.new Data(animatorObjects.get(i)
					.getPartner().getPk(), animatorObjects.get(i).getPartner()
					.getPartnerName());
			VillagesData.Data v = village.new Data(animatorObjects.get(i)
					.getVillage().getPk(), animatorObjects.get(i).getVillage()
					.getVillageName());
			Data animator = new Data(animatorObjects.get(i).getPk(),
					animatorObjects.get(i).getAnimatorName(), animatorObjects
							.get(i).getAge(), animatorObjects.get(i)
							.getGender(), animatorObjects.get(i).getCSPFlags(),
					animatorObjects.get(i).getCameraOperatorFlag(),
					animatorObjects.get(i).getFacilitatorFlag(),
					animatorObjects.get(i).getPhoneNo(), animatorObjects.get(i)
							.getAddress(), p, v);

			animators.add(animator);
		}
		return animators;
	}

	@Override
	public List getListingOnline(String json) {
		return this.serialize(this.asArrayOfData(json));
	}

	public List getAnimatorsListingOffline(String... pageNum) {
		BaseData.dbOpen();
		List animators = new ArrayList();
		PartnersData partner = new PartnersData();
		VillagesData village = new VillagesData();
		String listTemp;
		// Checking whether to return all villages or only limited number of villages
		if(pageNum.length == 0) {
			listTemp = listAnimators;
		}
		else {
			int offset = (Integer.parseInt(pageNum[0]) - 1)*pageSize;
			if(pageNum.length == 1) {
				listTemp = listAnimators + " LIMIT "+ Integer.toString(offset) + " , "+Integer.toString(pageSize) +";";
			} else {
				listTemp = "SELECT a.id, a.name,p.id,p.partner_name,vil.id,vil.village_name " +
							"FROM animator a,partners p,village vil " +
							"WHERE  a.partner_id = p.id and a.village_id = vil.id AND (a.name LIKE '%"+pageNum[1]+"%' " +
									"OR vil.VILLAGE_NAME" +	" LIKE '%"+pageNum[1]+"%' OR p.partner_name LIKE '%"+pageNum[1]+"%')" +" ORDER BY(a.name) " 
									+ " LIMIT "+ Integer.toString(offset)+" , "+Integer.toString(pageSize)+ ";";
			}
		}
		this.select(listTemp);
		if (this.getResultSet().isValidRow()) {
			try {
				for (int i = 0; this.getResultSet().isValidRow(); ++i, this
						.getResultSet().next()) {

					PartnersData.Data p = partner.new Data(this.getResultSet()
							.getFieldAsString(2), this.getResultSet()
							.getFieldAsString(3));

					VillagesData.Data v = village.new Data(this.getResultSet()
							.getFieldAsString(4), this.getResultSet()
							.getFieldAsString(5));

					Data animator = new Data(this.getResultSet()
							.getFieldAsString(0), this.getResultSet()
							.getFieldAsString(1), p, v);

					animators.add(animator);
				}

			} catch (DatabaseException e) {
				Window.alert("Database Exception : " + e.toString());
				BaseData.dbClose();
			}
		}
		BaseData.dbClose();
		return animators;
	}

	public List getAllAnimatorsOffline() {
		BaseData.dbOpen();
		List animators = new ArrayList();
		this.select(selectAnimators);
		if (this.getResultSet().isValidRow()) {
			try {
				for (int i = 0; this.getResultSet().isValidRow(); ++i, this.getResultSet().next()) {
					Data animator = new Data(this.getResultSet().getFieldAsString(0), 
							this.getResultSet().getFieldAsString(1));
					animators.add(animator);
				}
			} catch (DatabaseException e) {
				Window.alert("Database Exception : " + e.toString());
				BaseData.dbClose();
			}
		}
		BaseData.dbClose();
		return animators;
	}
	
	public List getAllAnimatorsWithVillageOffline() {
		BaseData.dbOpen();
		List animators = new ArrayList();
		this.select(selectAnimatorsWithVillage);
		if (this.getResultSet().isValidRow()) {
			try {
				VillagesData v = new VillagesData();
				for (int i = 0; this.getResultSet().isValidRow(); ++i, this.getResultSet().next()) {
					VillagesData.Data village = v.new Data(this.getResultSet().getFieldAsString(2), this.getResultSet().getFieldAsString(3));
					Data animator = new Data(this.getResultSet().getFieldAsString(0), this.getResultSet().getFieldAsString(1), village);
					animators.add(animator);
				}
			} catch (DatabaseException e) {
				Window.alert("Database Exception : " + e.toString());
				BaseData.dbClose();
			}
		}
		BaseData.dbClose();
		return animators;
	}

	public Object postPageData() {
		if (BaseData.isOnline()) {
			this.post(RequestContext.SERVER_HOST
					+ AnimatorsData.saveAnimatorOnlineURL, this.form
					.getQueryString());
		} else {
			if (this.validate()) {
				this.save();
				return true;
			}
		}
		return false;
	}
	
	public Object postPageData(String id) {
		if(BaseData.isOnline()){
			this.post(RequestContext.SERVER_HOST + this.saveAnimatorOnlineURL + id + "/", this.form.getQueryString());
		}
		else{
			if(this.validate()) {
				this.save();
				return true;
			}
		}
		return false;
	}

	public Object getListPageData(String... pageNum) {
		if (BaseData.isOnline()) {
			int offset = (Integer.parseInt(pageNum[0])-1)*pageSize;
			int limit = offset+pageSize;
			if(pageNum.length > 1 ) {
				this.get(RequestContext.SERVER_HOST + AnimatorsData.getAnimatorsOnlineURL +
						Integer.toString(offset)+"/"+Integer.toString(limit)+"/" + "?searchText="+pageNum[1]);
			} else {
				this.get(RequestContext.SERVER_HOST + AnimatorsData.getAnimatorsOnlineURL + Integer.toString(offset) + "/" 
						+ Integer.toString(limit)+ "/");
			}					
		} else {
			return true;
		}
		return false;
	}

	public String retrieveDataAndConvertResultIntoHtml() {
		PartnersData partnerData = new PartnersData();
		List partners = partnerData.getAllPartnersOffline();
		PartnersData.Data partner;
		String htmlPartner = "<select name=\"partner\" id=\"id_partner\""
				+ "<option selected='selected' value=''>---------</option>";
		for (int i = 0; i < partners.size(); i++) {
			partner = (PartnersData.Data) partners.get(i);
			htmlPartner = htmlPartner + "<option value=\"" + partner.getId()
					+ "\">" + partner.getPartnerName() + "</option>";
		}
		htmlPartner = htmlPartner + "</select>";
		VillagesData villageData = new VillagesData();
		List villages = villageData.getAllVillagesOffline();
		VillagesData.Data village;
		String htmlVillage = "<select name=\"village\" id=\"id_village\""
				+ "<option selected='selected' value=''>---------</option>";
		for (int i = 0; i < villages.size(); i++) {
			village = (VillagesData.Data) villages.get(i);
			htmlVillage = htmlVillage + "<option value=\"" + village.getId()
					+ "\">" + village.getVillageName() + "</option>";
		}
		htmlVillage = htmlVillage + "</select>";
		
		VillagesData villageData1 = new VillagesData();
		List villages1 = villageData1.getAllVillagesOffline();
		VillagesData.Data village1;
		String html = "";
		for (int inline = 0; inline < 3; inline++) {
			html += "<select name=\"animatorassignedvillage_set-" + inline
					+ "-village\" id=\"id_animatorassignedvillage_set-"
					+ inline + "-village\">"
					+ "<option selected='selected' value=''>---------</option>";
			for (int i = 0; i < villages1.size(); i++) {
				village1 = (VillagesData.Data) villages1.get(i);
				html = html + "<option value = \"" + village1.getId() + "\">"
						+ village1.getVillageName() + "</option>";
			}
			html = html + "</select>";
		}
		return htmlPartner + htmlVillage + html;
	}

	public Object getAddPageData() {
		if (BaseData.isOnline()) {
			this.get(RequestContext.SERVER_HOST
					+ AnimatorsData.saveAnimatorOnlineURL);
		} else {
			return retrieveDataAndConvertResultIntoHtml();
		}
		return false;
	}
	
	public Object getAddPageData(String id){
		if(BaseData.isOnline()){
			this.get(RequestContext.SERVER_HOST + this.saveAnimatorOnlineURL + id + "/" );
		}
		else{
			this.form.toQueryString(id);
			return retrieveDataAndConvertResultIntoHtml();
		}
		return false;
	}
	
	public String getCount(String searchText) {
		String count = "0";//stores number of rows in a resultset
		String countSql = "SELECT COUNT(*) FROM animator a,partners p,village vil " +
			"WHERE  a.partner_id = p.id and a.village_id = vil.id AND (a.name LIKE '%"+searchText+"%' " +
			"OR vil.VILLAGE_NAME" +	" LIKE '%"+searchText+"%' OR p.partner_name LIKE '%"+searchText+"%');" ;
		BaseData.dbOpen();
		this.select(countSql);
		if(this.getResultSet().isValidRow()) {
			try {
				count = getResultSet().getFieldAsString(0);
			} catch (DatabaseException e) {
				// TODO Auto-generated catch block
				Window.alert("Database Exception"+e.toString());
			}
		}
		BaseData.dbClose();
		return count;
	}
}
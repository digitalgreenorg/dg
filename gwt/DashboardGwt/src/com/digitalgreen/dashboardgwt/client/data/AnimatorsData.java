package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;
import java.util.List;
import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.google.gwt.core.client.JsArray;
import com.google.gwt.gears.client.database.DatabaseException;
import com.google.gwt.user.client.Window;

public class AnimatorsData extends BaseData {
	
	public static class Type extends BaseData.Type {
		protected Type() {}
		public final native String getAnimatorName() /*-{ return this.fields.name + ""; }-*/;
		public final native String getAge() /*-{ return this.fields.age + ""; }-*/;
		public final native String getGender() /*-{ return this.fields.gender + ""; }-*/;
		public final native String getCSPFlags() /*-{ return this.fields.csp_flags + ""; }-*/;
		public final native String getCameraOperatorFlag() /*-{ return this.fields.camera_operator_flag + ""; }-*/;
		public final native String getFacilitatorFlag() /*-{ return this.fields.facilitator_flag + ""; }-*/;
		public final native String getPhoneNo() /*-{ return this.fields.phone_no + ""; }-*/;
		public final native String getAddress() /*-{ return this.fields.address + ""; }-*/;
		public final native PartnersData.Data getPartner() /*-{ return this.fields.partner; }-*/;
		public final native VillagesData.Data getVillage() /*-{ return this.fields.village; }-*/;
		public final native String getEquipmentHolder() /*-{ return this.fields.equipment_holder; }-*/;

	}
	
	public class Data extends BaseData.Data {
		
		final private static String COLLECTION_PREFIX = "home_village";
		
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
		private String equipment_holder_id;

		public Data() {
			super();
		}
		
		public Data(String id, String name){
			super();
			this.id = id;
			this.name = name;
		}
		
		public Data(String id, String name, String age, String gender, String csp_flag, String camera_operator_flag,
				String facilitator_flag, String phone_no, String address, PartnersData.Data partner,
				VillagesData.Data village, String equipment_holder_id){
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
			this.equipment_holder_id = equipment_holder_id;
		}

		public String getAnimatorName(){
			return this.name;
		}
		
		public String getAge(){
			return this.age;
		}
		
		public String getGender(){
			return this.gender;
		}
		
		public String getCSPFlag(){
			return this.csp_flag;
		}
		
		public String getCameraOperatorFlag(){
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
		
		public PartnersData.Data getPartner(){
			return this.partner;
		}
		
		public VillagesData.Data getVillage(){
			return this.village;
		}
		
		public String getEquipmentHolder(){
			return this.equipment_holder_id;
		}
		
		@Override
		public String getPrefixName() {
			return Data.COLLECTION_PREFIX;
		}
		
		@Override
		public BaseData.Data clone() {
			Data obj = new Data();
			return obj;
		}
		
		@Override
		public void setObjValueFromString(String key, String val) {
			super.setObjValueFromString(key, val);
			if(key.equals("id")) {
				this.id = val;
			} else if(key.equals("name")) {
				this.name = val;
			} else if(key.equals("age")) {
				this.age = val;
			} else if(key.equals("gender")) {
				this.gender = val;
			} else if(key.equals("csp_flag")) {
				this.csp_flag = val;
			} else if(key.equals("camera_operator_flag")) {
				this.camera_operator_flag = val;
			} else if(key.equals("facilitator_flag")) {
				this.facilitator_flag = val;
			} else if(key.equals("phone_no")) {
				this.phone_no = val;
			} else if(key.equals("address")) {
				this.address = val;
			} else if(key.equals("partner")) {
				PartnersData partner = new PartnersData();
				this.partner = partner.getNewData();
				this.partner.id = val;
			} else if(key.equals("home_village")) {
				VillagesData village = new VillagesData();
				this.village = village.getNewData();
				this.village.id = val;
			} else if(key.equals("equipmentholder")) {
				this.equipment_holder_id = val;
			}
		}
		
		@Override
		public void save() {
			AnimatorsData animatorsDataDbApis = new AnimatorsData();
			if(this.id == null){
				this.id = animatorsDataDbApis.autoInsert(this.name, 
						this.age, 
						this.gender, 
						this.csp_flag, 
						this.camera_operator_flag, 
						this.facilitator_flag, 
						this.phone_no, 
						this.address, 
						this.partner.getId(), 
						this.village.getId(), 
						this.equipment_holder_id);
			} else {
				this.id = animatorsDataDbApis.autoInsert(this.id, 
						this.name, 
						this.age, 
						this.gender, 
						this.csp_flag, 
						this.camera_operator_flag, 
						this.facilitator_flag, 
						this.phone_no, 
						this.address, 
						this.partner.getId(), 
						this.village.getId(), 
						this.equipment_holder_id);
			}
		}
		
		@Override
		public void save(BaseData.Data foreignKey) {
			AnimatorsData animatorsDataDbApis = new AnimatorsData();
			this.id = animatorsDataDbApis.autoInsert(this.name, 
					this.age, 
					this.gender, 
					this.csp_flag, 
					this.camera_operator_flag, 
					this.facilitator_flag, 
					this.phone_no, 
					this.address, 
					this.partner.getId(), 
					foreignKey.getId(), 
					this.equipment_holder_id);
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
	protected static String selectAnimators = "SELECT animator.id, animator.name FROM animator ORDER BY (animator.name);";
	protected static String listAnimators = "SELECT animator.id, animator.name, animator.age, animator.gender, animator.csp_flag, animator.camera_operator_flag, animator.facilitator_flag, animator.phone_no, animator.address, partners.id, partners.partner_name, village.id, village.village_name, equipment_holder.id FROM animator JOIN partners ON animator.partner_id = partners.id JOIN village ON animator.home_village_id = village.id JOIN equipment_holder ON animator.equipmentholder_id = equipment_holder.id;";
	protected static String saveAnimatorOnlineURL = "/dashboard/saveanimatoronline/";
	protected static String saveAnimatorOfflineURL = "/dashboard/saveanimatoroffline/";
	protected static String getAnimatorsOnlineURL = "/dashboard/getanimatorsonline/";
	protected String table_name = "animator";
	protected String[] fields = {"id", "name", "age", "gender", "csp_flag", "camera_operator_flag", "facilitator_flag", "phone_no", "address", "partner_id", "home_village_id", "equipmentholder_id"};
	
	public AnimatorsData() {
		super();
	}
	
	public AnimatorsData(OnlineOfflineCallbacks callbacks) {
		super(callbacks);
	}
	
	public AnimatorsData(OnlineOfflineCallbacks callbacks, Form form, String queryString) {
		super(callbacks, form, queryString);
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
	protected String getTableName() {
		return this.table_name;
	}
	
	@Override 
	protected String[] getFields() {
		return this.fields;
	}

	@Override
	public String getListingOnlineURL(){
		return AnimatorsData.getAnimatorsOnlineURL;
	}
	
	public final native JsArray<Type> asArrayOfData(String json) /*-{
		return eval(json);
	}-*/;
	
	public List serialize(JsArray<Type> animatorObjects) {
		List animators = new ArrayList();
		PartnersData partner = new PartnersData();
		VillagesData village = new VillagesData();
		for(int i = 0; i < animatorObjects.length(); i++) {
			
			PartnersData.Data p = partner. new Data(animatorObjects.get(i).getPartner().getId(), animatorObjects.get(i).getPartner().getPartnerName());
			
			VillagesData.Data v = village. new Data(animatorObjects.get(i).getVillage().getId(), animatorObjects.get(i).getVillage().getVillageName());
			
			Data animator = new Data(animatorObjects.get(i).getPk(), animatorObjects.get(i).getAnimatorName(),
							animatorObjects.get(i).getAge(), animatorObjects.get(i).getGender(), animatorObjects.get(i).getCSPFlags(),
							animatorObjects.get(i).getCameraOperatorFlag(), animatorObjects.get(i).getFacilitatorFlag(),
							animatorObjects.get(i).getPhoneNo(), animatorObjects.get(i).getAddress(), p, v, 
							animatorObjects.get(i).getEquipmentHolder());
		}
		
		return animators;
	}
	
	@Override
	public List getListingOnline(String json){
		return this.serialize(this.asArrayOfData(json));
	}
	
	public List getAnimatorsListingOffline(){
		BaseData.dbOpen();
		List animators = new ArrayList();
		PartnersData partner = new PartnersData();
		VillagesData village = new VillagesData();
		this.select(listAnimators);
		if(this.getResultSet().isValidRow()){
			try{
				Window.alert("resultse count: " + this.getResultSet().getFieldCount());
				for (int i = 0; this.getResultSet().isValidRow(); ++i, this.getResultSet().next()) {
					
					PartnersData.Data  p = partner. new Data(this.getResultSet().getFieldAsString(9), this.getResultSet().getFieldAsString(10));
					
					VillagesData.Data v = village. new Data(this.getResultSet().getFieldAsString(11), this.getResultSet().getFieldAsString(12));
					
					Data animator = new Data(this.getResultSet().getFieldAsString(0), this.getResultSet().getFieldAsString(1),
							 this.getResultSet().getFieldAsString(2), this.getResultSet().getFieldAsString(3), 
							 this.getResultSet().getFieldAsString(4), this.getResultSet().getFieldAsString(5),
							 this.getResultSet().getFieldAsString(6), this.getResultSet().getFieldAsString(7), 
							 this.getResultSet().getFieldAsString(8), p, v, 
							 this.getResultSet().getFieldAsString(13));
					
					animators.add(animator);
				}
				
			}
			catch (DatabaseException e) {
				Window.alert("Database Exception : " + e.toString());
				BaseData.dbClose();
			}
		}
		BaseData.dbClose();
		return animators;
	}
	
	public List getAllAnimatorsOffline(){
		BaseData.dbOpen();
		List animators = new ArrayList();
		this.select(selectAnimators);
		if (this.getResultSet().isValidRow()){
			try {
				for (int i = 0; this.getResultSet().isValidRow(); ++i, this.getResultSet().next()) {
					Data animator = new Data(this.getResultSet().getFieldAsString(0), this.getResultSet().getFieldAsString(1));
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
		if(BaseData.isOnline()){
			this.post(RequestContext.SERVER_HOST + AnimatorsData.saveAnimatorOnlineURL, this.queryString);
		}
		else{
			this.save();
			return true;
		}
		return false;
	}
	
	public Object getListPageData(){
		if(BaseData.isOnline()){
			this.get(RequestContext.SERVER_HOST + AnimatorsData.getAnimatorsOnlineURL);
		}
		else{
			return true;
		}
		return false;
	}
	
	public String retrieveDataAndConvertResultIntoHtml() {
		PartnersData partnerData = new PartnersData();
		List partners = partnerData.getPartnersListingOffline();
		PartnersData.Data partner;
		String htmlPartner = "<select name=\"partner\" id=\"id_partner\"";
		for(int i = 0; i < partners.size(); i++){
			partner = (PartnersData.Data)partners.get(i);
			htmlPartner = htmlPartner + "<option value=\"" + partner.getId() + "\">" + partner.getPartnerName() + "</option>";
		}
		
		VillagesData villageData = new VillagesData();
		List villages = villageData.getVillagesListingOffline();
		VillagesData.Data village;
		String htmlVillage = "<select name=\"village\" id=\"id_village\"";
		for(int i = 0; i < villages.size(); i++){
			village = (VillagesData.Data)villages.get(i);
			htmlVillage = htmlVillage + "<option value=\"" + village.getId() + "\">" + village.getVillageName() + "</option>";
		}
		
		VillagesData villageData1 = new VillagesData();
		List villages1 = villageData1.getVillagesListingOffline();
		VillagesData.Data village1;
		String html = "";
		for(int inline = 0; inline < 3; inline++){
			html += "<select name=\"animatorassignedvillage_set-" + inline + "-village\" id=\"id_animatorassignedvillage_set-" + inline + "-village\">";
			for ( int i = 0; i < villages1.size(); i++ ) {
				village1 = (VillagesData.Data)villages1.get(i);
				html = html + "<option value = \"" + village1.getId() + "\">" + village1.getVillageName() + "</option>";
				Window.alert(html);
			}
			html = html + "</select>";
		}
		
		return htmlPartner + htmlVillage + html;
	}
	
	public Object getAddPageData() {
		if(BaseData.isOnline()) {
			this.get(RequestContext.SERVER_HOST + AnimatorsData.saveAnimatorOnlineURL);
		}
		else{
			return retrieveDataAndConvertResultIntoHtml();
		}
		return false;
	}
}
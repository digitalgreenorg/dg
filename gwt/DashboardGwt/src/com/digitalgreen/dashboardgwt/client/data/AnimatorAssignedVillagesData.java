package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.ApplicationConstants;
import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.validation.DateValidator;
import com.digitalgreen.dashboardgwt.client.data.validation.StringValidator;
import com.digitalgreen.dashboardgwt.client.servlets.AnimatorAssignedVillages;
import com.google.gwt.core.client.JsArray;
import com.google.gwt.gears.client.database.DatabaseException;
import com.google.gwt.user.client.Window;

public class AnimatorAssignedVillagesData extends BaseData{
	
	public static class Type extends BaseData.Type {
		protected Type() {}
		public final native AnimatorsData.Type getAnimator() /*-{ return this.fields.animator; }-*/ ;
		public final native VillagesData.Type getVillage() /*-{ return this.fields.village; }-*/ ;
		public final native String getStartDate() /*-{ return $wnd.checkForNullValues(this.fields.start_date); }-*/;
	}
	
	public class Data extends BaseData.Data {
		
		final private static String COLLECTION_PREFIX = "animatorassignedvillage";
		
		private AnimatorsData.Data animator;
		private VillagesData.Data village;
		private String start_date;
		
		public Data() {
			super();
		}
		
		public Data(String id, String start_date){
			super();
			this.id = id;
			this.start_date = start_date;
		}
		
		public Data(String id, AnimatorsData.Data animator, VillagesData.Data village, String start_date){
			super();
			this.id = id;
			this.animator = animator;
			this.village = village;
			this.start_date = start_date;
		}
		
		public String getStartDate(){
			return this.start_date;
		}
		
		public AnimatorsData.Data getAnimator(){
			return this.animator;
		}
		
		public VillagesData.Data getVillage(){
			return this.village;
		}
		
		@Override
		public BaseData.Data clone(){
			Data obj = new Data();
			obj.animator = (new AnimatorsData()).new Data();
			obj.village = (new VillagesData()).new Data();
			return obj;
		}
		
		@Override
		public String getPrefixName(){
			return this.COLLECTION_PREFIX;
		}
		
		@Override
		public void setObjValueFromString(String key, String val){
			super.setObjValueFromString(key, val);
			if(key.equals("id")) {
				this.id = val;
			}else if(key.equals("animator")) {
				AnimatorsData animator1 = new AnimatorsData();
				this.animator = animator1.getNewData();
				this.animator.id = val;
			}
			else if(key.equals("village")){
				VillagesData village1 = new VillagesData();
				this.village = village1.getNewData();
				this.village.id = val;
			}
			else if(key.equals("start_date")) {
				this.start_date = (String)val;
			} else {
				return;
			}
			this.addNameValueToQueryString(key, val);
		}
		
		@Override
		public boolean validate(){
			StringValidator animatorValidator = new StringValidator(this.animator.getId(), false, false, 1, 100);
			animatorValidator.setError("Please make sure you choose a animator for 'Animator'.");
			StringValidator villageValidator = new StringValidator(this.village.getId(), false, false, 1, 100);
			villageValidator.setError("Please make sure you choose a village for 'Village'.");
			DateValidator startDate = new DateValidator(this.start_date, true, true);
			startDate.setError("Please make sure 'Start date' is formatted as YYYY-MM-DD.");
			ArrayList validatorList = new ArrayList();
			validatorList.add(animatorValidator);
			validatorList.add(villageValidator);
			validatorList.add(startDate);
			return this.executeValidators(validatorList);
		}
		
		@Override
		public boolean validate(BaseData.Data foreignKey){
			StringValidator villageValidator = new StringValidator(this.village.getId(), false, false, 1, 100);
			villageValidator.setError("Please make sure you choose a village for 'Village'.");
			DateValidator startDate = new DateValidator(this.start_date, true, true);
			startDate.setError("Please make sure 'Start date' is formatted as YYYY-MM-DD.");
			ArrayList validatorList = new ArrayList();
			validatorList.add(villageValidator);
			validatorList.add(startDate);
			return this.executeValidators(validatorList);
		}
		
		@Override
		public void save(){
			AnimatorAssignedVillagesData animatorAssignedVillagesDataDbApis = new AnimatorAssignedVillagesData();
			this.id = animatorAssignedVillagesDataDbApis.autoInsert(this.id, 
					this.animator.getId(), 
					this.village.getId(), 
					this.start_date);
			this.addNameValueToQueryString("id", this.id);
		}
		
		@Override
		public void save(BaseData.Data foreignKey) {
			AnimatorAssignedVillagesData animatorAssignedVillagesDataDbApis = new AnimatorAssignedVillagesData();
			this.id = animatorAssignedVillagesDataDbApis.autoInsert(this.id,
					foreignKey.getId(), 
					this.village.getId(), 
					this.start_date);
			this.addNameValueToQueryString("id", this.id);
			this.addNameValueToQueryString("animator", foreignKey.getId());
		}
		
		@Override
		public String toQueryString(String id) {
			AnimatorAssignedVillagesData animatorAssignedVillagesData = new AnimatorAssignedVillagesData();
			return this.rowToQueryString(animatorAssignedVillagesData.getTableName(), animatorAssignedVillagesData.getFields(), "id", id, "");
		}
		
		@Override
		public String toInlineQueryString(String id) {
			AnimatorAssignedVillagesData animatorAssignedVillagesData = new AnimatorAssignedVillagesData();
			return rowToQueryString(animatorAssignedVillagesData.getTableName(), animatorAssignedVillagesData.getFields(), 
					"animator_id", id, this.COLLECTION_PREFIX + "_set");
		}
		
		@Override
		public String getTableId() {
			AnimatorAssignedVillagesData animatorAssignedVillagesDataDbApis = new AnimatorAssignedVillagesData();
			return animatorAssignedVillagesDataDbApis.tableID;
		}
	}
	
	public static String tableID = "24";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `animator_assigned_village` " +
												"(id BIGINT UNSIGNED PRIMARY KEY NOT NULL ," +
												"animator_id BIGINT UNSIGNED  NOT NULL DEFAULT 0," +
												"village_id BIGINT UNSIGNED  NOT NULL DEFAULT 0," +
												"START_DATE DATE  NULL DEFAULT NULL, " +
												"FOREIGN KEY(animator_id) REFERENCES animator(id), " +
												"FOREIGN KEY(village_id) REFERENCES village(id));";
	protected static String dropTable = "DROP TABLE IF EXISTS `animator_assigned_village`;";
	protected static String selectAnimatorsAssignedVillages = "SELECT id, start_date from animator_assigned_village ORDER BY(id);";
	protected static String listAnimatorsAssignedVillages = "SELECT aav.id, a.id, a.name, vil.id,vil.VILLAGE_NAME,aav.start_date" +
			" FROM animator_assigned_village aav,animator a,village vil WHERE aav.animator_id = a.id and aav.village_id = vil.id ORDER BY LOWER(a.name)";
	protected static String saveAnimatorAssignedVillageOnlineURL = "/dashboard/saveanimatorassignedvillageonline/";
	protected static String getAnimatorAssignedVillageOnlineURL = "/dashboard/getanimatorassignedvillagesonline/";
	protected static String saveAnimatorAssignedVillageOfflineURL = "/dashboard/saveanimatorassignedvillageoffline/";
	protected String table_name = "animator_assigned_village";
	protected String[] fields = {"id", "animator_id", "village_id", "start_date"};
	
	public AnimatorAssignedVillagesData(){
		super();
	}
	
	public AnimatorAssignedVillagesData(OnlineOfflineCallbacks callbacks){
		super(callbacks);
	}
	
	public AnimatorAssignedVillagesData(OnlineOfflineCallbacks callbacks, Form form){
		super(callbacks, form);
	}
	
	@Override
	public Data getNewData(){
		return new Data();
	}
	
	@Override
	protected String getTableId(){
		return AnimatorAssignedVillagesData.tableID;
	}
	
	@Override
	public String getTableName(){
		return this.table_name;
	}
	
	@Override
	protected String[] getFields(){
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
		return AnimatorAssignedVillagesData.getAnimatorAssignedVillageOnlineURL;
	}
	
	@Override
	public String getSaveOfflineURL(){
		return AnimatorAssignedVillagesData.saveAnimatorAssignedVillageOfflineURL;
	}
	
	@Override
	public String getSaveOnlineURL(){
		return AnimatorAssignedVillagesData.saveAnimatorAssignedVillageOnlineURL;
	}
	

	public final native JsArray<Type> asArrayOfData(String json) /*-{
		return eval(json);
	}-*/;
	
	public List serialize(JsArray<Type> animatorAssignedVillageObjects){
		List animatorAssignedVillages = new ArrayList();
		AnimatorsData animator = new AnimatorsData();
		VillagesData village = new VillagesData();
		for ( int i = 0; i < animatorAssignedVillageObjects.length(); i++ ) {
			
			AnimatorsData.Data a = animator. new Data(animatorAssignedVillageObjects.get(i).getAnimator().getPk(), 
					animatorAssignedVillageObjects.get(i).getAnimator().getAnimatorName());
			
			VillagesData.Data v = village. new Data(animatorAssignedVillageObjects.get(i).getVillage().getPk(), animatorAssignedVillageObjects.get(i).getVillage().getVillageName());
			
			Data animatorassignedvillage = new Data(animatorAssignedVillageObjects.get(i).getPk(), a, v, animatorAssignedVillageObjects.get(i).getStartDate());
			
			animatorAssignedVillages.add(animatorassignedvillage);
		}
		return animatorAssignedVillages;
	}
	
	@Override
	public List getListingOnline(String json){
		return this.serialize(this.asArrayOfData(json));		
	}
	
	public List getAnimatorsAssignedVillagesListingOffline(String... pageNum){
		BaseData.dbOpen();
		List animatorsAssignedVillages = new ArrayList();
		AnimatorsData animator = new AnimatorsData();
		VillagesData village = new VillagesData();
		String listTemp;
		// Checking whether to return all villages or only limited number of villages
		if(pageNum.length == 0) {
			listTemp = listAnimatorsAssignedVillages;
		}
		else {
			int offset = (Integer.parseInt(pageNum[0]) - 1)*pageSize;
			if(pageNum.length == 1) {
				listTemp = listAnimatorsAssignedVillages + " LIMIT "+ Integer.toString(offset) + " , "+Integer.toString(pageSize) +";";
			} else {
				listTemp = "SELECT aav.id, a.id, a.name, vil.id,vil.VILLAGE_NAME,aav.start_date" +
							" FROM animator_assigned_village aav,animator a,village vil " +
							"WHERE aav.animator_id = a.id AND aav.village_id = vil.id AND (a.name LIKE '%"+pageNum[1]+"%' " +
									"OR vil.VILLAGE_NAME" +	" LIKE '%"+pageNum[1]+"%')" +" ORDER BY(a.name) " 
									+ " LIMIT "+ Integer.toString(offset)+" , "+Integer.toString(pageSize)+ ";";
			}
		}
		this.select(listTemp);
		if(this.getResultSet().isValidRow()){
			try{				
				for (int i = 0; this.getResultSet().isValidRow(); ++i, this.getResultSet().next()) {					
					AnimatorsData.Data a = animator. new Data(this.getResultSet().getFieldAsString(1), this.getResultSet().getFieldAsString(2));					
					VillagesData.Data v = village. new Data(this.getResultSet().getFieldAsString(3), this.getResultSet().getFieldAsString(4));					
					Data animatorassignedvillage = new Data(this.getResultSet().getFieldAsString(0),a,v, this.getResultSet().getFieldAsString(5));					
					animatorsAssignedVillages.add(animatorassignedvillage);					
				}
			}
			catch (DatabaseException e) {
				Window.alert("Database Exception : " + e.toString());
				BaseData.dbClose();
			}
		}
		BaseData.dbClose();
		return animatorsAssignedVillages;
	}
	
	public List getAllAnimatorsAssignedVillagesOnline(){
		BaseData.dbOpen();
		List animatorsAssignedVillages = new ArrayList();
		this.select(selectAnimatorsAssignedVillages);
		if(this.getResultSet().isValidRow()){
			try {
				for (int i = 0; this.getResultSet().isValidRow(); ++i, this.getResultSet().next()) {				
					Data animatorassignedvillage = new Data(this.getResultSet().getFieldAsString(0), this.getResultSet().getFieldAsString(1));					
					animatorsAssignedVillages.add(animatorassignedvillage);
				}
			}
			catch (DatabaseException e) {
				Window.alert("Database Exception : " + e.toString());
				BaseData.dbClose();
			}
		}
		
		BaseData.dbClose();
		return animatorsAssignedVillages;
	}
	
	public Object postPageData() {
		if(BaseData.isOnline()){
			this.post(RequestContext.SERVER_HOST + AnimatorAssignedVillagesData.saveAnimatorAssignedVillageOnlineURL, this.form.getQueryString());
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
			this.post(RequestContext.SERVER_HOST + this.saveAnimatorAssignedVillageOnlineURL + id + "/", this.form.getQueryString());
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
				this.get(RequestContext.SERVER_HOST + AnimatorAssignedVillagesData.getAnimatorAssignedVillageOnlineURL +
						Integer.toString(offset)+"/"+Integer.toString(limit)+"/" + "?searchText="+pageNum[1]);
			} else {
				this.get(RequestContext.SERVER_HOST + AnimatorAssignedVillagesData.getAnimatorAssignedVillageOnlineURL 
						+ Integer.toString(offset) + "/" + Integer.toString(limit) + "/");
			}					
		} else {
			return true;
		}
		return false;
	}

	public String retrieveDataAndConvertResultIntoHtml() {
		AnimatorsData animatorData = new AnimatorsData();
		List animators = animatorData.getAllAnimatorsOffline();
		AnimatorsData.Data animator;
		String htmlAnimator = "<select name=\"animator\" id=\"id_animator\"" + 
							"<option value='' selected='selected'>---------</option>";
		for ( int i = 0; i < animators.size(); i++ ) {
			animator = (AnimatorsData.Data)animators.get(i);
			htmlAnimator = htmlAnimator + "<option value=\"" + animator.getId() + "\">" + animator.getAnimatorName() + "</option>";
		}
		htmlAnimator = htmlAnimator + "</select>";
		
		VillagesData villageData = new VillagesData();
		List villages = villageData.getAllVillagesOffline();
		VillagesData.Data village;
		String htmlVillage = "<select name=\"village\" id=\"id_village\""  + 
							"<option value='' selected='selected'>---------</option>";
		for(int i = 0; i < villages.size(); i++ ) {
			village = (VillagesData.Data)villages.get(i);
			htmlVillage = htmlVillage + "<option value=\"" + village.getId() + "\">" + village.getVillageName() + "</option>";
		}
		htmlVillage = htmlVillage + "</select>";
		
		return htmlAnimator + htmlVillage;
	}
	
	public Object getAddPageData() {
		if(BaseData.isOnline()) {
			this.get(RequestContext.SERVER_HOST + AnimatorAssignedVillagesData.saveAnimatorAssignedVillageOnlineURL);
		}
		else{
			return retrieveDataAndConvertResultIntoHtml();
		}
		return false;
	}
	
	public Object getAddPageData(String id){
		if(BaseData.isOnline()){
			this.get(RequestContext.SERVER_HOST + this.saveAnimatorAssignedVillageOnlineURL + id + "/" );
		}
		else{
			this.form.toQueryString(id);
			return retrieveDataAndConvertResultIntoHtml();
		}
		return false;
	}
	
	public String getCount(String searchText) {
		String count = "0";//stores number of rows in a resultset
		String countSql = "SELECT COUNT(*)" +
						" FROM animator_assigned_village aav,animator a,village vil " +
						"WHERE aav.animator_id = a.id AND aav.village_id = vil.id AND (a.name LIKE '%"+searchText+"%' " +
						"OR vil.VILLAGE_NAME" +	" LIKE '%"+searchText+"%');";
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
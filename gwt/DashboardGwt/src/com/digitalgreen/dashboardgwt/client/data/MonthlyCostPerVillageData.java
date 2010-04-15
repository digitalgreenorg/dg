package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.MonthlyCostPerVillageData.Data;
import com.digitalgreen.dashboardgwt.client.data.MonthlyCostPerVillageData.Type;
import com.google.gwt.core.client.JsArray;

public class MonthlyCostPerVillageData extends BaseData {
	
	public static class Type extends BaseData.Type{
		protected Type() {}
		public final native VillagesData.Type getVillage() /*-{ return this.fields.village }-*/;
		public final native String getDate() /*-{ return $wnd.checkForNullValues(this.fields.date); }-*/;
		public final native String getLaborCost() /*-{ return $wnd.checkForNullValues(this.fields.labor_cost); }-*/;
		public final native String getEquipmentCost() /*-{ return $wnd.checkForNullValues(this.fields.equipment_cost); }-*/;
		public final native String getTransportationCost() /*-{ return $wnd.checkForNullValues(this.fields.transportation_cost); }-*/;
		public final native String getMiscellaneousCost() /*-{ return $wnd.checkForNullValues(this.fields.miscellaneous_cost); }-*/;
		public final native String getTotalCost() /*-{ return $wnd.checkForNullValues(this.fields.total_cost); }-*/;
		public final native String getPartnersCost() /*-{ return $wnd.checkForNullValues(this.fields.partners_cost); }-*/;
		public final native String getDigitalGreenCost() /*-{ return $wnd.checkForNullValues(this.fields.digitalgreen_cost); }-*/;
		public final native String getCommunityCost() /*-{ return $wnd.checkForNullValues(this.fields.community_cost); }-*/;
		
	}
	
public class Data extends BaseData.Data {
		
		final private static String COLLECTION_PREFIX = "monthlycostpervillage";
			
		private VillagesData.Data village;
		private String date;
		private String labor_cost;
		private String equipment_cost;
		private String transportation_cost;
		private String miscellaneous_cost;
		private String total_cost;
		private String partners_cost;
		private String digitalgreen_cost;
		private String community_cost;
				
				
		public Data() {
			super();
		}
		
		public Data(String id, VillagesData.Data village) {
			super();
			this.id = id;
			this.village = village;
		}
		

		public Data(String id, VillagesData.Data village, String date, String labor_cost,String equipment_cost,String transportation_cost,
				String miscellaneous_cost,String total_cost,String partners_cost,String digitalgreen_cost,String community_cost) {
			super();
			this.id = id;
			this.village = village;
			this.date = date;
			this.labor_cost = labor_cost;
			this.equipment_cost = equipment_cost;
			this.transportation_cost = transportation_cost;
			this.miscellaneous_cost = miscellaneous_cost;
			this.total_cost = total_cost;
			this.partners_cost = partners_cost;
			this.digitalgreen_cost = digitalgreen_cost;
			this.community_cost = community_cost;
					
		}
				
		public VillagesData.Data getVillage(){
			return this.village;
		}
		
		public String getDate(){
			return this.date;
		}
		
		public String getLaborCost(){
			return this.labor_cost;
		}
		
		public String getEquipmentCost(){
			return this.equipment_cost;
		}
		public String getTransportationCost(){
			return this.transportation_cost;
		}
		public String getMiscellaneousCost(){
			return this.miscellaneous_cost;
		}
		public String getTotalCost(){
			return this.total_cost;
		}
		public String getPartnersCost(){
			return this.partners_cost;
		}
		public String getDigitalGreenCost(){
			return this.digitalgreen_cost;
		}
		public String getCommunityCost(){
			return this.community_cost;
		}
		
		
		public BaseData.Data clone() {
			Data obj = new Data();
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
			if(key.equals("village")) {
				// Have to Create an instance of VillagesData to create an instance of VillagesData.Data -- any better way of doing this??
				VillagesData village = new VillagesData();
				this.village = village.getNewData();
				this.village.id = val;
				//Never ever use this -- this.village.id = ((Integer)val).intValue();
			}  else if(key.equals("date")) {
				this.date = (String)val;
			}	else if(key.equals("labor_cost")) {
				this.labor_cost = (String)val;
			}	else if(key.equals("equipment_cost")) {
				this.equipment_cost = (String)val;
			}	else if(key.equals("transportation_cost")) {
				this.transportation_cost = (String)val;
			}	else if(key.equals("miscellaneous_cost")) {
				this.miscellaneous_cost = (String)val;
			}	else if(key.equals("total_cost")) {
				this.total_cost = (String)val;
			}	else if(key.equals("partners_cost")) {
				this.partners_cost = (String)val;
			}	else if(key.equals("digitalgreen_cost")) {
				this.digitalgreen_cost = (String)val;
			}	else if(key.equals("community_cost")) {
				this.community_cost = (String)val;
			}	else {
				return;
			}
			this.addNameValueToQueryString(key, val);	
		}
		
		@Override
		public void save() {
			MonthlyCostPerVillageData monthlycostpervillagesDataDbApis = new MonthlyCostPerVillageData();	
			this.id = monthlycostpervillagesDataDbApis.autoInsert(this.id,
						this.village.getId(),
						this.date,
						this.labor_cost,
						this.equipment_cost,
						this.transportation_cost,
						this.miscellaneous_cost,
						this.total_cost,
						this.partners_cost,
						this.digitalgreen_cost,
						this.community_cost);
			this.addNameValueToQueryString("id", this.id);
		}
		
		@Override
		public String getTableId() {
			MonthlyCostPerVillageData monthlycostpervillagesDataDbApis = new MonthlyCostPerVillageData();
			return monthlycostpervillagesDataDbApis.tableID;
		}
	}
	
	protected static String tableID = "11";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `monthly_cost_per_village` " +
												"(id INTEGER PRIMARY KEY  NOT NULL ," +
												"village_id INT  NOT NULL DEFAULT 0," +
												"DATE DATE  NOT NULL ," +
												"LABOR_COST FLOAT(0,0)  NULL DEFAULT NULL," +
												"EQUIPMENT_COST FLOAT(0,0)  NULL DEFAULT NULL," +
												"TRANSPORTATION_COST FLOAT(0,0)  NULL DEFAULT NULL," +
												"MISCELLANEOUS_COST FLOAT(0,0)  NULL DEFAULT NULL," +
												"TOTAL_COST FLOAT(0,0)  NULL DEFAULT NULL," +
												"PARTNERS_COST FLOAT(0,0)  NULL DEFAULT NULL," +
												"DIGITALGREEN_COST FLOAT(0,0)  NULL DEFAULT NULL," +
												"COMMUNITY_COST FLOAT(0,0)  NULL DEFAULT NULL, " +
												"FOREIGN KEY(village_id) REFERENCES village(id));";
	
	protected static String selectMonthlyCostPerVillages = "SELECT id, vil.village_name FROM monthly_cost_per_village mcpv, village vil WHERE" +
			" mcpv.village_id = vil.id ORDER BY (vil.village_name);";
	protected static String listMonthlyCostPerVillages = "SELECT * FROM monthly_cost_per_village mcps JOIN vllage vil ON mcps.village_id = vil.id ORDER BY (-mcps.id);";
	protected static String saveMonthlyCostPerVillageOnlineURL = "/dashboard/savemonthlycostpervillageonline/";
	protected static String getMonthlyCostPerVillageOnlineURL = "/dashboard/getmonthlycostpervillagesonline/";
	protected static String saveMonthlyCostPerVillageOfflineURL = "/dashboard/savemonthlycostpervillageoffline/";
	protected String table_name = "monthly_cost_per_village";
	protected String[] fields = {"id", "village_id", "date", "labor_cost","equipment_cost","transportation_cost","miscellaneous_cost","total_cost",
			"partners_cost","digitalgreen_cost","community_cost"};
	
	
	public MonthlyCostPerVillageData(){
		super();
	}
	
	public MonthlyCostPerVillageData(OnlineOfflineCallbacks callbacks) {
		super(callbacks);
	}
	
	public MonthlyCostPerVillageData(OnlineOfflineCallbacks callbacks, Form form) {
		super(callbacks, form);
	}

	@Override
	public Data getNewData() {
		return new Data();
	}
	@Override
	protected String getTableId() {
		return MonthlyCostPerVillageData.tableID;
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
		return MonthlyCostPerVillageData.getMonthlyCostPerVillageOnlineURL;
	}
	
	@Override
	public String getSaveOfflineURL(){
		return MonthlyCostPerVillageData.saveMonthlyCostPerVillageOfflineURL;
	}
	
	public final native JsArray<Type> asArrayOfData(String json) /*-{
		return eval(json);
	}-*/;
	
	public List serialize(JsArray<Type> monthlycostpervillageObjects){
		List monthlycostpervillages = new ArrayList();
		VillagesData village = new VillagesData();
		for(int i = 0; i < monthlycostpervillageObjects.length(); i++){
			VillagesData.Data vil = village.new Data(monthlycostpervillageObjects.get(i).getVillage().getPk(), 
					monthlycostpervillageObjects.get(i).getVillage().getVillageName());
			
			Data monthlycostpervillage = new Data(monthlycostpervillageObjects.get(i).getPk(), vil,
											monthlycostpervillageObjects.get(i).getDate(), 
											monthlycostpervillageObjects.get(i).getLaborCost(),
											monthlycostpervillageObjects.get(i).getEquipmentCost(), 
											monthlycostpervillageObjects.get(i).getTransportationCost(),
											monthlycostpervillageObjects.get(i).getMiscellaneousCost(), 
											monthlycostpervillageObjects.get(i).getTotalCost(),
											monthlycostpervillageObjects.get(i).getPartnersCost(), 
											monthlycostpervillageObjects.get(i).getDigitalGreenCost(),
											monthlycostpervillageObjects.get(i).getCommunityCost());
			monthlycostpervillages.add(monthlycostpervillage);
		}
		
		return monthlycostpervillages;
	}
	
	@Override
	public List getListingOnline(String json){
		return this.serialize(this.asArrayOfData(json));		
	}
}

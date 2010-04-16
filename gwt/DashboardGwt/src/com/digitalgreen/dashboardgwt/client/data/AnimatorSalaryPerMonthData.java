package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.AnimatorSalaryPerMonthData.Type;
import com.digitalgreen.dashboardgwt.client.data.AnimatorSalaryPerMonthData.Data;
import com.google.gwt.core.client.JsArray;

public class AnimatorSalaryPerMonthData extends BaseData{
	
	public static class Type extends BaseData.Type{
		protected Type() {}
		public final native AnimatorsData.Type getAnimator() /*-{ return this.fields.animator; }-*/;
		public final native String getDate() /*-{ return $wnd.checkForNullValues(this.fields.date); }-*/;
		public final native String getTotalSalary() /*-{ return $wnd.checkForNullValues(this.fields.total_salary); }-*/;
		public final native String getPayDate() /*-{ return $wnd.checkForNullValues(this.fields.pay_date); }-*/;
	}
	
	public class Data extends BaseData.Data {
		
		final private static String COLLECTION_PREFIX = "animatorsalarypermonth";
			
		private AnimatorsData.Data animator;
		private String date;
		private String total_salary;
		private String pay_date;
		
				
		public Data() {
			super();
		}
		
		public Data(String id, AnimatorsData.Data animator) {
			super();
			this.id = id;
			this.animator = animator;
		}
		

		public Data(String id, AnimatorsData.Data animator,String date, String total_salary, String pay_date) {
			super();
			this.id = id;
			this.animator = animator;
			this.date = date;
			this.total_salary = total_salary;
			this.pay_date = pay_date;
			
		}
				
		public AnimatorsData.Data getAnimator(){
			return this.animator;
		}
		
		public String getDate(){
			return this.date;
		}
		
		public String getTotalSalary(){
			return this.total_salary;
		}
		
		public String getPayDate(){
			return this.pay_date;
		}
		
		
		public BaseData.Data clone() {
			Data obj = new Data();
			obj.animator = (new AnimatorsData()).new Data();
			return obj;
		}
		
		@Override
		public String getPrefixName() {
			return Data.COLLECTION_PREFIX;
		}
		
		@Override
		public void setObjValueFromString(String key, String val) {
			super.setObjValueFromString(key, val);
			if(key.equals("animator")) {
				// Have to Create an instance of AnimatorsData to create an instance of AnimatorsData.Data -- any better way of doing this??
				AnimatorsData animator = new AnimatorsData();
				this.animator = animator.getNewData();
				this.animator.id = val;
				//Never ever use this -- this.region.id = ((Integer)val).intValue();
			}  else if(key.equals("date")) {
				this.date = (String)val;
			}	 else if(key.equals("total_salary")) {
				this.total_salary = (String)val;
			}	 else if(key.equals("pay_date")) {
				this.pay_date = (String)val;
			}	else {
				return;
			}
			this.addNameValueToQueryString(key, val);	
		}
		
		@Override
		public void save() {
			AnimatorSalaryPerMonthData animatorsalarypermonthsDataDbApis = new AnimatorSalaryPerMonthData();		
			this.id = animatorsalarypermonthsDataDbApis.autoInsert(this.id,
						this.animator.getId(),
						this.date,
						this.total_salary, 
						this.pay_date);
			this.addNameValueToQueryString("id", this.id);
		}
		

		@Override
		public String getTableId() {
			AnimatorSalaryPerMonthData animatorsalarypermonthsDataDbApis = new AnimatorSalaryPerMonthData();
			return animatorsalarypermonthsDataDbApis.tableID;
		}
		
	}

	public static String tableID = "25";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `animator_salary_per_month` " +
												"(id INTEGER PRIMARY KEY NOT NULL ," +
												"animator_id INT  NOT NULL DEFAULT 0," +
												"DATE DATE  NOT NULL ," +
												"TOTAL_SALARY FLOAT(0,0)  NULL DEFAULT NULL," +
												"PAY_DATE DATE  NULL DEFAULT NULL, " +
												"FOREIGN KEY(animator_id) REFERENCES animator(id));";
	
	protected static String selectAnimatorSalaryPerMonths = "SELECT asp.id, a.NAME  FROM animator_salary_per_month asp, animator a " +
			"WHERE asp.animator_id = a.id ORDER BY (NAME);";
	protected static String listAnimatorSalaryPerMonths = "SELECT * FROM animator_salary_per_month aav JOIN animator a ON aav.animator_id = a.id " +
			"ORDER BY (-aav.id);";
	protected static String saveAnimatorSalaryPerMonthOnlineURL = "/dashboard/saveanimatorsalarypermonthonline/";
	protected static String getAnimatorSalaryPerMonthOnlineURL = "/dashboard/getanimatorsalarypermonthsonline/";
	protected static String saveAnimatorSalaryPerMonthOfflineURL = "/dashboard/saveanimatorsalarypermonthoffline/";
	protected String table_name = "animator_salary_per_month";
	protected String[] fields = {"id", "animator_id", "date", "total_salary", "pay_date"};
	
	
	public AnimatorSalaryPerMonthData(){
		super();
	}
	
	public AnimatorSalaryPerMonthData(OnlineOfflineCallbacks callbacks) {
		super(callbacks);
	}
	
	public AnimatorSalaryPerMonthData(OnlineOfflineCallbacks callbacks, Form form) {
		super(callbacks, form);
	}

	@Override
	public Data getNewData() {
		return new Data();
	}
	
	@Override
	protected String getTableId() {
		return AnimatorSalaryPerMonthData.tableID;
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
		return AnimatorSalaryPerMonthData.getAnimatorSalaryPerMonthOnlineURL;
	}
	
	@Override
	public String getSaveOfflineURL(){
		return AnimatorSalaryPerMonthData.saveAnimatorSalaryPerMonthOfflineURL;
	}
	
	
	public final native JsArray<Type> asArrayOfData(String json) /*-{
		return eval(json);
	}-*/;
	
	public List serialize(JsArray<Type> animatorsalarypermonthObjects){
		List animatorsalarypermonths = new ArrayList();
		AnimatorsData animator = new AnimatorsData();
		for(int i = 0; i < animatorsalarypermonthObjects.length(); i++){
			AnimatorsData.Data a = animator.new Data(animatorsalarypermonthObjects.get(i).getAnimator().getPk(), 
					animatorsalarypermonthObjects.get(i).getAnimator().getAnimatorName());
			Data animatorsalarypermonth = new Data(animatorsalarypermonthObjects.get(i).getPk(),
					 a,animatorsalarypermonthObjects.get(i).getDate(),
					 animatorsalarypermonthObjects.get(i).getTotalSalary(),
					 animatorsalarypermonthObjects.get(i).getPayDate());
			animatorsalarypermonths.add(animatorsalarypermonth);
		}
		
		return animatorsalarypermonths;
	}
	
	@Override
	public List getListingOnline(String json){
		return this.serialize(this.asArrayOfData(json));		
	}
}
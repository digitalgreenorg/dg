package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.google.gwt.core.client.JsArray;

public class DashboardErrorData extends BaseData {
	
	public static class Type extends BaseData.Type{
		protected Type() {}
		public final native String getErrorMsg() /*-{ return $wnd.checkForNullValues(this.fields.rule.fields.error_msg); }-*/;
		public final native String getObjectId1() /*-{ return $wnd.checkForNullValues(this.fields.object_id1); }-*/;
		public final native String getObjectId2() /*-{ return $wnd.checkForNullValues(this.fields.object_id2); }-*/;
		public final native String isError() /*-{ return $wnd.checkForNullValues(this.fields.notanerror); }-*/;
		public final native String getContentType1() /*-{ return (this.fields.content_type1)?$wnd.checkForNullValues(this.fields.content_type1.fields.name):null; }-*/;
		public final native String getContentType2() /*-{ return (this.fields.content_type2)?$wnd.checkForNullValues(this.fields.content_type2.fields.name):null; }-*/;
		
	}
	
	public class Data extends BaseData.Data {
		
		final private static String COLLECTION_PREFIX = "dashboard errors";
			
		private String error_msg;
		private String object1;
		private String object2;
		private String notanerror;
		private String content_type1;
		private String content_type2;
		
		
		public Data() {
			super();
		}

		public Data(String id, String error_msg,String object1, String object2, String notanerror, String content_type1, String content_type2) {
			super();
			this.id = id;
			this.error_msg = error_msg;
			this.object1 = object1;
			this.object2 = object2;
			this.notanerror = notanerror;
			this.content_type1 = content_type1;
			this.content_type2 = content_type2;
		}
		
		
		public String getErrorMsg(){
			return this.error_msg;
		}
		
		public String getObjectId1(){
			return this.object1;
		}
		
		public String getObjectId2(){
			return this.object2;
		}
		
		public boolean isError(){
			if(this.notanerror!=null && this.notanerror!="0")
				return true;
			else 
				return false;
		}
		
		public String getContentType1(){
			return this.content_type1;
		}
		
		public String getContentType2(){
			return this.content_type2;
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
		public String getTableId() {
			return DashboardErrorData.tableID;
		}
	}

	public static String tableID = "44";
	
	protected static String getDashboardErrorOnlineURL = "/dashboard/geterrorsonline/";
	protected static String markNotAnErrorURL = "/dashboard/notanerror/";
	
	public DashboardErrorData() {
		super();
	}
	
	public DashboardErrorData(OnlineOfflineCallbacks callbacks) {
		super(callbacks);
	}
	
	public DashboardErrorData(OnlineOfflineCallbacks callbacks, Form form) {
		super(callbacks, form);
	}

	@Override
	public Data getNewData() {
		return new Data();
	}
	
	@Override
	protected String getTableId() {
		return DashboardErrorData.tableID;
	}
	
	@Override
	public String getListingOnlineURL(){
		return DashboardErrorData.getDashboardErrorOnlineURL;
	}
	
	public final native JsArray<Type> asArrayOfData(String json) /*-{
		return eval(json);
	}-*/;
	
	public List serialize(JsArray<Type> errorObjects){
		List errors = new ArrayList();
		for(int i = 0; i < errorObjects.length(); i++){
			Data error = new Data(errorObjects.get(i).getPk(), errorObjects.get(i).getErrorMsg(), errorObjects.get(i).getObjectId1(), errorObjects.get(i).getObjectId2(), errorObjects.get(i).isError(), errorObjects.get(i).getContentType1(), errorObjects.get(i).getContentType2());
			errors.add(error);
		}
		return errors;
	}
	
	@Override
	public List getListingOnline(String json){
		return this.serialize(this.asArrayOfData(json));		
	}
	
	public Object getListPageData(String pageNum){
		if(BaseData.isOnline()){
			int offset = (Integer.parseInt(pageNum)-1)*pageSize;
			int limit = offset+pageSize;
			this.get(RequestContext.SERVER_HOST + DashboardErrorData.getDashboardErrorOnlineURL+Integer.toString(offset)+"/"+Integer.toString(limit)+ "/");
			return false;
		}
		else{
			return true;
		}
	}
	
	public Object postPageData() {
		if(BaseData.isOnline()){
			this.post(RequestContext.SERVER_HOST + DashboardErrorData.markNotAnErrorURL, this.form.getQueryString());
		}
		//else
			//Offline is disabled for Dashboard Errors
		
		return false;
	}
}
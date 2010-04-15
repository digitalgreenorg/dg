package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.ScreeningVideosScreenedData.Type;
import com.digitalgreen.dashboardgwt.client.data.ScreeningVideosScreenedData.Data;
import com.google.gwt.core.client.JsArray;

public class ScreeningVideosScreenedData extends BaseData {
	
	public static class Type extends BaseData.Type{
		protected Type(){}
		
		public final native ScreeningsData.Type getScreening() /*-{ return this.fields.screening;}-*/;
		public final native VideosData.Type getVideo() /*-{ return this.fields.video;}-*/;		
	}
	
	public class Data extends BaseData.Data {
		final private static String COLLECTION_PREFIX = "screeningvideosscreened";
		
		private ScreeningsData.Data screening;// FK to the Screenings table
		private VideosData.Data video;
				
		public Data() {
			super();
		}
		
		public Data(String id, ScreeningsData.Data screening, VideosData.Data video) {
			this.id = id;
			this.screening = screening;
			this.video = video;
			}
		
		public Data(String id, VideosData.Data video){
			super();
			this.id = id;
			this.video = video;
		}
			
		public ScreeningsData.Data getScreening(){
			return this.screening;
		}
		
		public VideosData.Data getVideo(){
			return this.video;
		}
		
		public BaseData.Data clone(){
			Data obj = new Data();
			return obj;
		}
		
		@Override
		public String getPrefixName() {
			return Data.COLLECTION_PREFIX;
		}
		
		@Override
		public void setObjValueFromString(String key, String val) {
			super.setObjValueFromString(key, val);
			if(key.equals("screening")) {
				ScreeningsData screening = new ScreeningsData();
				this.screening = screening.getNewData();
				this.screening.id = val;
				
			} else if(key.equals("video")) {
				VideosData video = new VideosData();
				this.video = video.getNewData();
				this.video.id = val;
			} else {
				return;
			}
			this.addNameValueToQueryString(key, val);
		}
	

		@Override		
		public void save() {
			ScreeningVideosScreenedData screeningVideosScreenedsDataDbApis = new ScreeningVideosScreenedData();		
			this.id = screeningVideosScreenedsDataDbApis.autoInsert(this.id,
					this.screening.getId(),
					this.video.getId());
			this.addNameValueToQueryString("id", this.id);
		}
		
		@Override
		public String getTableId() {
			ScreeningVideosScreenedData screeningVideosScreenedsDataDbApis = new ScreeningVideosScreenedData();
			return screeningVideosScreenedsDataDbApis.tableID;
		}	
	}
	
		
	protected static String tableID = "27";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `screening_videos_screened` " +
												"(id INTEGER PRIMARY KEY  NOT NULL ," +
												"screening_id INT  NOT NULL DEFAULT 0," +
												"video_id INT  NOT NULL DEFAULT 0,  " +
												"FOREIGN KEY(screening_id) REFERENCES screening(id), " +
												"FOREIGN KEY(video_id) REFERENCES video(id));";
	
	
	protected static String selectScreeningVideosScreened = "SELECT svs.id, vid.TITLE FROM screening_videos_screened svs, video vid" +
	"WHERE svs.video_id = vid.id ORDER BY (vid.TITLE);";
	protected static String listScreeningVideosScreened = "SELECT svs.id, vid.TITLE FROM screening_videos_screened svs, video vid" +
	"WHERE svs.video_id = vid.id ORDER BY (svs.id);";
	protected static String saveScreeningVideosScreenedOfflineURL = "/dashboard/savescreeningvideosscreenedoffline/";
	protected static String saveScreeningVideosScreenedOnlineURL = "/dashboard/savescreeningvideosscreenedonline/";
	protected static String getScreeningVideosScreenedOnlineURL = "/dashboard/getscreeningvideosscreenedsonline/";
	protected String table_name = "screening_videos_screened";
	protected String[] fields = {"id", "screening_id","video_id"};
		
	public ScreeningVideosScreenedData() {
		super();
	}
	public ScreeningVideosScreenedData(OnlineOfflineCallbacks callbacks) {
		super(callbacks);
	}
	
	public ScreeningVideosScreenedData(OnlineOfflineCallbacks callbacks, Form form) {
		super(callbacks, form);
	}
	@Override
	public Data getNewData() {
		return new Data();
	}
	@Override
	protected String getTableId(){
		return ScreeningVideosScreenedData.tableID;
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
		return ScreeningVideosScreenedData.getScreeningVideosScreenedOnlineURL;
	}
	
	
	public final native JsArray<Type> asArrayOfData(String json) /*-{
		return eval(json);
	}-*/;
	
	public List serialize(JsArray<Type> screeningVideosScreenedObjects){
		List screeningVideosScreeneds = new ArrayList();
		ScreeningsData screening = new ScreeningsData();
		VideosData video = new VideosData();
		PracticesData practice = new PracticesData();
		for(int i = 0; i < screeningVideosScreenedObjects.length(); i++){
			ScreeningsData.Data sc = screening.new Data(screeningVideosScreenedObjects.get(i).getScreening().getPk(),
					screeningVideosScreenedObjects.get(i).getScreening().getDate());
			VideosData.Data vid = video.new Data(screeningVideosScreenedObjects.get(i).getVideo().getPk(),
					screeningVideosScreenedObjects.get(i).getVideo().getTitle());
			
			Data screeningVideosScreened = new Data(screeningVideosScreenedObjects.get(i).getPk(),sc,vid);
			screeningVideosScreeneds.add(screeningVideosScreened);
		}
		
		return screeningVideosScreeneds;
	}
	
	@Override
	public List getListingOnline(String json){
		return this.serialize(this.asArrayOfData(json));		
	}

	
}

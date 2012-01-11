package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.ScreeningVideosScreenedData.Type;
import com.digitalgreen.dashboardgwt.client.data.ScreeningVideosScreenedData.Data;
import com.google.gwt.core.client.JsArray;
import com.google.gwt.user.client.Window;

public class ScreeningVideosScreenedData extends BaseData {
	
	public static class Type extends BaseData.Type{
		protected Type(){}
		
		public final native String getScreening() /*-{ return this.fields.screening;}-*/;
		public final native String getVideo() /*-{ return this.fields.video;}-*/;		
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
			obj.screening = (new ScreeningsData()).new Data();
			obj.video = (new VideosData()).new Data();
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
			}else if(key.equals("screening")) {
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
		public void save(BaseData.Data foreignKey){
			ScreeningVideosScreenedData screeningVideosScreenedsDataDbApis = new ScreeningVideosScreenedData();
			this.id = screeningVideosScreenedsDataDbApis.autoInsert(this.id,
					foreignKey.getId(), 
					this.video.getId());
			this.addNameValueToQueryString("id", this.id);
			this.addNameValueToQueryString("screening", foreignKey.getId());
		}
		
		@Override
		public String toQueryString(String id) {
			ScreeningVideosScreenedData screeningVideosScreenedData = new ScreeningVideosScreenedData();
			return this.rowToQueryString(screeningVideosScreenedData.getTableName(), screeningVideosScreenedData.getFields(), "id", id, "");
		}
		
		@Override
		public String getTableId() {
			ScreeningVideosScreenedData screeningVideosScreenedsDataDbApis = new ScreeningVideosScreenedData();
			return screeningVideosScreenedsDataDbApis.tableID;
		}	
	}
	
		
	public static String tableID = "41";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `screening_videos_screened` " +
												"(id BIGINT UNSIGNED PRIMARY KEY  NOT NULL ," +
												"screening_id BIGINT UNSIGNED  NOT NULL DEFAULT 0," +
												"video_id BIGINT UNSIGNED  NOT NULL DEFAULT 0,  " +
												"FOREIGN KEY(screening_id) REFERENCES screening(id), " +
												"FOREIGN KEY(video_id) REFERENCES video(id));";
	protected static String dropTable = "DROP TABLE IF EXISTS `screening_videos_screened`;";
	protected static String[] createIndexes = {"CREATE INDEX IF NOT EXISTS screening_videos_screened_PRIMARY ON screening_videos_screened(id);", 
								   "CREATE INDEX IF NOT EXISTS screening_videos_screened_screening_id ON screening_videos_screened(screening_id);",
								   "CREATE INDEX IF NOT EXISTS screening_videos_screened_video_id ON screening_videos_screened(video_id);"};
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
		return ScreeningVideosScreenedData.getScreeningVideosScreenedOnlineURL;
	}
	
	@Override
	public String getSaveOfflineURL(){
		return ScreeningVideosScreenedData.saveScreeningVideosScreenedOfflineURL;
	}
	
	@Override
	public String getSaveOnlineURL(){
		return ScreeningVideosScreenedData.saveScreeningVideosScreenedOnlineURL;
	}
	
	public final native JsArray<Type> asArrayOfData(String json) /*-{
		return eval(json);
	}-*/;
	
	public List serialize(JsArray<Type> screeningVideosScreenedObjects){
		List screeningVideosScreeneds = new ArrayList();
		ScreeningsData screening = new ScreeningsData();
		VideosData video = new VideosData();
		for(int i = 0; i < screeningVideosScreenedObjects.length(); i++){
			ScreeningsData.Data sc = screening.new Data(screeningVideosScreenedObjects.get(i).getScreening());
			VideosData.Data vid = video.new Data(screeningVideosScreenedObjects.get(i).getVideo());
			
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

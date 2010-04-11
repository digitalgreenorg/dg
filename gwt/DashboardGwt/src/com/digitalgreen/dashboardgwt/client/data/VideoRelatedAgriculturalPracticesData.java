package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.VideoRelatedAgriculturalPracticesData.Type;
import com.digitalgreen.dashboardgwt.client.data.VideoRelatedAgriculturalPracticesData.Data;
import com.google.gwt.core.client.JsArray;

public class VideoRelatedAgriculturalPracticesData extends BaseData {
	
	public static class Type extends BaseData.Type{
		protected Type(){}
		
		public final native VideosData.Type getVideo() /*-{ return this.fields.video;}-*/;
		public final native PracticesData.Type getPractice() /*-{ return this.fields.practice;}-*/;
	}
	
	public class Data extends BaseData.Data {
		final private static String COLLECTION_PREFIX = "videorelatedagriculturalpractices";
		
		private PracticesData.Data practice;// FK to the Screenings table
		private VideosData.Data video;
				
		public Data() {
			super();
		}
		
		public Data(String id, VideosData.Data video,PracticesData.Data practice) {
			this.id = id;
			this.video = video;
			this.practice = practice;
			}
		
		public Data(String id, VideosData.Data video){
			super();
			this.id = id;
			this.video = video;
		}
			
		public VideosData.Data getVideo(){
			return this.video;
		}
		public PracticesData.Data getPractice(){
			return this.practice;
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
			if(key.equals("id")) {
				this.id = val;
			} else if(key.equals("video")) {
				VideosData video = new VideosData();
				this.video = video.getNewData();
				this.video.id = val;
			} else if(key.equals("practice")) {
				PracticesData practice = new PracticesData();
				this.practice = practice.getNewData();
				this.practice.id = val;				
			} 
		}
	
		@Override		
		public void save() {
			VideoRelatedAgriculturalPracticesData videoRelatedAgriculturalPracticessDataDbApis = new VideoRelatedAgriculturalPracticesData();
			this.id = videoRelatedAgriculturalPracticessDataDbApis.autoInsert(this.id,
						this.video.getId(),
						this.practice.getId());
		}	
	}
	
	
	protected static String tableID = "23";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `video_related_agricultural_practices` " +
												"(id INTEGER PRIMARY KEY  NOT NULL ," +
												"video_id INT  NOT NULL DEFAULT 0," +
												"practices_id INT  NOT NULL DEFAULT 0, " +
												"FOREIGN KEY(video_id) REFERENCES video(id),  " +
												"FOREIGN KEY(practices_id) REFERENCES practices(id) );";
	
	protected static String selectVideoRelatedAgriculturalPracticeShown = "SELECT vrap.id, vid.TITLE FROM video_related_agricultural_practices vrap, video vid" +
	"WHERE vrap.video_id = vid.id ORDER BY (vid.TITLE);";
	protected static String listVideoRelatedAgriculturalPracticeShown = "SELECT vrap.id, vid.TITLE, pr.practice_name FROM" +
			" video_related_agricultural_practices vrap,video vid, practice pr WHERE vrap.video_id = vid.id AND vrap.practices_id = pr.id " +
			"ORDER BY (vrap.id);";
	protected static String saveVideoRelatedAgriculturalPracticeOfflineURL = "/dashboard/savevideorelatedagriculturalpracticeoffline/";
	protected static String saveVideoRelatedAgriculturalPracticeOnlineURL = "/dashboard/savevideorelatedagriculturalpracticeonline/";
	protected static String getVideoRelatedAgriculturalPracticeOnlineURL = "/dashboard/getvideorelatedagriculturalpracticesonline/";
	protected String table_name = "video_related_agricultural_practices";
	protected String[] fields = {"id", "video_id","practices_id"};
	
	public VideoRelatedAgriculturalPracticesData(){
		super();
	}
	
	public VideoRelatedAgriculturalPracticesData(OnlineOfflineCallbacks callbacks) {
		super(callbacks);
	}
	
	public VideoRelatedAgriculturalPracticesData(OnlineOfflineCallbacks callbacks, Form form) {
		super(callbacks, form);
	}
	@Override
	public Data getNewData() {
		return new Data();
	}
	@Override
	protected String getTableId(){
		return VideoRelatedAgriculturalPracticesData.tableID;
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
		return VideoRelatedAgriculturalPracticesData.getVideoRelatedAgriculturalPracticeOnlineURL;
	}

	
	public final native JsArray<Type> asArrayOfData(String json) /*-{
		return eval(json);
	}-*/;
	
	public List serialize(JsArray<Type> videoFarmersShownObjects){
		List videoFarmersShowns = new ArrayList();
		PracticesData practice = new PracticesData();
		VideosData video = new VideosData();
		for(int i = 0; i < videoFarmersShownObjects.length(); i++){
			PracticesData.Data p = practice.new Data(videoFarmersShownObjects.get(i).getPractice().getPk(),
					videoFarmersShownObjects.get(i).getPractice().getPracticeName());
			VideosData.Data vid = video.new Data(videoFarmersShownObjects.get(i).getVideo().getPk(),
					videoFarmersShownObjects.get(i).getVideo().getTitle());
			
			Data videoFarmersShown = new Data(videoFarmersShownObjects.get(i).getPk(),vid,p);
			videoFarmersShowns.add(videoFarmersShown);
		}
		
		return videoFarmersShowns;
	}
	
	@Override
	public List getListingOnline(String json){
		return this.serialize(this.asArrayOfData(json));		
	}


}

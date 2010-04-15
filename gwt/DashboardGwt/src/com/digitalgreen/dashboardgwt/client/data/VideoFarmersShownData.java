package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.VideoFarmersShownData.Type;
import com.digitalgreen.dashboardgwt.client.data.VideoFarmersShownData.Data;
import com.google.gwt.core.client.JsArray;

public class VideoFarmersShownData extends BaseData {
	
	public static class Type extends BaseData.Type{
		protected Type(){}
		
		public final native String getVideo() /*-{ return this.fields.video;}-*/;
		public final native String getPerson() /*-{ return this.fields.person;}-*/;
	}
	
	public class Data extends BaseData.Data {
		final private static String COLLECTION_PREFIX = "videofarmersshown";
		
		private PersonsData.Data person;// FK to the Screenings table
		private VideosData.Data video;
				
		public Data() {
			super();
		}
		
		public Data(String id, VideosData.Data video,PersonsData.Data person) {
			this.id = id;
			this.video = video;
			this.person = person;
			}
		
		public Data(String id, VideosData.Data video){
			super();
			this.id = id;
			this.video = video;
		}
			
		public VideosData.Data getVideo(){
			return this.video;
		}
		public PersonsData.Data getPerson(){
			return this.person;
		}
		
		public BaseData.Data clone(){
			Data obj = new Data();
			obj.video = (new VideosData()).new Data();
			obj.person = (new PersonsData()).new Data();
			return obj;
		}
		
		@Override
		public String getPrefixName() {
			return Data.COLLECTION_PREFIX;
		}
		
		@Override
		public void setObjValueFromString(String key, String val) {
			super.setObjValueFromString(key, val);
			if(key.equals("video")) {
				VideosData video = new VideosData();
				this.video = video.getNewData();
				this.video.id = val;
			} else if(key.equals("person")) {
				PersonsData person = new PersonsData();
				this.person = person.getNewData();
				this.person.id = val;				
			} else {
				return;
			}
			this.addNameValueToQueryString(key, val);
		}
	
		@Override		
		public void save() {
			VideoFarmersShownData videoFarmersShownsDataDbApis = new VideoFarmersShownData();		
			this.id = videoFarmersShownsDataDbApis.autoInsert(this.id,
						this.video.getId(),
						this.person.getId());
			this.addNameValueToQueryString("id", this.id);
		}	
		
		@Override
		public String getTableId() {
			VideoFarmersShownData videoFarmersShownsDataDbApis = new VideoFarmersShownData();
			return videoFarmersShownsDataDbApis.tableID;
		}
	}
	

	protected static String tableID = "24";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `video_farmers_shown` " +
												"(id INTEGER PRIMARY KEY  NOT NULL ," +
												"video_id INT  NOT NULL DEFAULT 0," +
												"person_id INT  NOT NULL DEFAULT 0, " +
												"FOREIGN KEY(video_id) REFERENCES video(id), " +
												"FOREIGN KEY(person_id) REFERENCES person(id));";
	
	protected static String selectVideoFarmerShown = "SELECT vfs.id, vid.TITLE FROM video_farmers_shown vfs, video vid" +
	"WHERE vfs.video_id = vid.id ORDER BY (vid.TITLE);";
	protected static String listVideoFarmerShown = "SELECT vfs.id, vid.TITLE, p.person_name FROM video_farmers_shown vfs, video vid, person p" +
	"WHERE vfs.video_id = vid.id AND vfs.person_id = p.id ORDER BY (vfs.id);";
	protected static String saveVideoFarmerOfflineURL = "/dashboard/savevideofarmeroffline/";
	protected static String saveVideoFarmerOnlineURL = "/dashboard/savevideofarmeronline/";
	protected static String getVideoFarmerOnlineURL = "/dashboard/getvideofarmersonline/";
	protected String table_name = "video_farmers_shown";
	protected String[] fields = {"id", "video_id","person_id"};
	
	public VideoFarmersShownData(){
		super();
	}

	public VideoFarmersShownData(OnlineOfflineCallbacks callbacks) {
		super(callbacks);
	}
	
	public VideoFarmersShownData(OnlineOfflineCallbacks callbacks, Form form) {
		super(callbacks, form);
	}
	@Override
	public Data getNewData() {
		return new Data();
	}
	@Override
	protected String getTableId(){
		return VideoFarmersShownData.tableID;
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
		return VideoFarmersShownData.getVideoFarmerOnlineURL;
	}
	
	@Override
	public String getSaveOfflineURL(){
		return VideoFarmersShownData.saveVideoFarmerOfflineURL;
	}

	
	public final native JsArray<Type> asArrayOfData(String json) /*-{
		return eval(json);
	}-*/;
	
	public List serialize(JsArray<Type> videoFarmersShownObjects){
		List videoFarmersShowns = new ArrayList();
		PersonsData person = new PersonsData();
		VideosData video = new VideosData();
		for(int i = 0; i < videoFarmersShownObjects.length(); i++){
			PersonsData.Data p = person.new Data(videoFarmersShownObjects.get(i).getPerson());
			VideosData.Data vid = video.new Data(videoFarmersShownObjects.get(i).getVideo());
			
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

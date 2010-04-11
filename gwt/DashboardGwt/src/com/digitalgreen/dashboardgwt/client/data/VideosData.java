package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.google.gwt.core.client.JsArray;
import com.google.gwt.gears.client.database.DatabaseException;
import com.google.gwt.user.client.Window;

public class VideosData extends BaseData {

	public static class Type extends BaseData.Type{
		protected Type() {}
		public final native String getTitle() /*-{ return $wnd.checkForNullValues(this.fields.title); }-*/;
		public final native String getVideoType() /*-{ return $wnd.checkForNullValues(this.fields.video_type);}-*/;
		public final native String getDuration() /*-{ return $wnd.checkForNullValues(this.fields.duration); }-*/;
		public final native String getSummary() /*-{ return $wnd.checkForNullValues(this.fields.summary); }-*/;
		public final native String getVideoProductionStartDate() /*-{ return $wnd.checkForNullValues(this.fields.video_production_start_date); }-*/;
		public final native String getVideoProductionEndDate() /*-{ return $wnd.checkForNullValues(this.fields.video_production_end_date); }-*/;
		public final native VillagesData.Type getVillage() /*-{ return this.fields.village }-*/;
		public final native AnimatorsData.Type getFacilitator() /*-{ return this.fields.facilitator }-*/;
		public final native AnimatorsData.Type getCameraOperator() /*-{ return this.fields.cameraoperator }-*/;
	}
	
	public class Data extends BaseData.Data {
				
		final private static String COLLECTION_PREFIX = "video";
		
		private String title;   		
		private String video_type;
	    private String duration; 
	    private LanguagesData.Data language; 
	    private String summary; 
	    private String picture_quality; 
	    private String audio_quality;
	    private String editing_quality;
	    private String edit_start_date;
	    private String edit_finish_date;
	    private String thematic_quality; 
	    private String video_production_start_date; 
		private String video_production_end_date; 
	    private String storybase;
	    private String storyboard_filename;
	    private String raw_filename; 
	    private String movie_maker_project_filename;
	    private String final_edited_filename;
	    private VillagesData.Data village;
	    private AnimatorsData.Data facilitator; 
	    private AnimatorsData.Data cameraoperator;
	    private ReviewersData.Data reviewer; 
	    private String approval_date;
	    private VideosData.Data supplementary_video_produced;
	    private String video_suitable_for;
	    private String remarks;
	    private PracticesData.Data related_agricultural_practices;    
	    private PersonsData.Data farmers_shown;
	    private String actors;
	    private String last_modified; 
		
		public Data() {
			super();
		}
		
		public Data(String id, String title) {
			super();
			this.id = id;
			this.title = title;
		}
		

		public Data(String id, String title ,String video_production_start_date, String video_production_end_date,  VillagesData.Data village) {
			super();
			this.id = id;
			this.title = title;
			this.video_production_start_date = video_production_start_date;
			this.video_production_end_date = video_production_end_date;
			this.village = village;
		}
		
		
		public String getTitle(){
			return this.title;
		}
		
		public String getVideoProductionStartDate(){
			return this.video_production_start_date;
		}
		
		public String getVideoProductionEndDate(){
			return this.video_production_end_date;
		}
		
		public VillagesData.Data getVillage(){
			return this.village;
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
		public void setObjValueFromString(String key, String val) {
			super.setObjValueFromString(key, val);
			if(key.equals("id")) {
				this.id = val;
			} else if(key.equals("title")) {
				this.title = (String)val;
			} else if(key.equals("video_type")){
				this.video_type = val;
			} else if(key.equals("video_production_start_date")) {
				this.video_production_start_date = (String)val;
			} else if (key.equals("video_production_end_date")) {
				this.video_production_end_date = (String)val;
			} else if (key.equals("language")) {
				LanguagesData language = new LanguagesData();
				this.language = language.getNewData();
				this.language.id = val;
			} else if (key.equals("storybase")){
				this.storybase = val;
			} else if (key.equals("summary")){
				this.summary = (String)val;
			} else if(key.equals("village")) {
				VillagesData village = new VillagesData();
				this.village = village.getNewData();
				this.village.id = val;
			} else if(key.equals("facilitator")){
				AnimatorsData facilitator = new AnimatorsData();
				this.facilitator = facilitator.getNewData();
				this.facilitator.id = val;
			} else if(key.equals("cameraoperator")){
				AnimatorsData cameraoperator = new AnimatorsData();
				this.cameraoperator = cameraoperator.getNewData();
				this.cameraoperator.id = val;
			} else if(key.equals("related_agricultural_practices")){
				PracticesData practices = new PracticesData();
				this.related_agricultural_practices = practices.getNewData();
				this.related_agricultural_practices.id = val;
			} else if(key.equals("farmers_shown")) {
				PersonsData person = new PersonsData();
				this.farmers_shown = person.getNewData();
				this.farmers_shown.id = val;
			} else if(key.equals("actors")) {
				this.actors = (String)val;
			} else if(key.equals("picture_quality")){
				this.picture_quality = (String)val;
			} else if(key.equals("audio_quality")){
				this.audio_quality = (String)val;
			} else if(key.equals("editing_quality")){
				this.editing_quality = (String)val;
			} else if(key.equals("edit_start_date")){
				this.edit_start_date = (String)val;
			} else if(key.equals("edit_finish_date")){
				this.edit_finish_date = (String)val;
			} else if(key.equals("thematic_quality")){
				this.thematic_quality = (String)val;
			} else if(key.equals("reviewer")){
				ReviewersData reviewer = new ReviewersData();
				this.reviewer = reviewer.getNewData();
				this.reviewer.id = val;
			} else if(key.equals("approval_date")){
				this.approval_date = (String)val;
			} else if(key.equals("supplementary_video_produced")){
				VideosData video = new VideosData();
				this.supplementary_video_produced = video.getNewData();
				this.supplementary_video_produced.id = val;
			}
			
			
		}
		
		
		@Override
		public void save() {
			Date date = new Date();
			this.last_modified = date.getYear() + "-" + date.getMonth() +"-" + date.getDate() + " " + date.getHours() + ":" + date.getMinutes() + ":" + date.getSeconds();
			VideosData videosDataDbApis = new VideosData();		
			this.id = videosDataDbApis.autoInsert(this.id,
						this.title, 
						this.video_type, 
						this.duration, 
						this.language.getId(), 
						this.summary, 
						this.picture_quality,
						this.audio_quality, 
						this.editing_quality, 
						this.edit_start_date, 
						this.edit_finish_date,
						this.thematic_quality, 
						this.video_production_start_date, 
						this.video_production_end_date, 
						this.storybase, 
						this.storyboard_filename, 
						this.raw_filename, 
						this.movie_maker_project_filename, 
						this.final_edited_filename, 
						this.village.getId(),
						this.facilitator.getId(), 
						this.cameraoperator.getId(),
						this.reviewer.getId(), 
						this.approval_date, 
						this.supplementary_video_produced.getId(),
						this.video_suitable_for, 
						this.remarks, 
						this.actors, 
						this.last_modified);
		}
	}
	
	protected static String tableID = "22";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `video` " +
												"(id INTEGER PRIMARY KEY  NOT NULL ," +
												"TITLE VARCHAR(200)  NOT NULL ," +
												"VIDEO_TYPE INT  NOT NULL DEFAULT 0," +
												"DURATION TIME  NULL DEFAULT NULL," +
												"language_id INT  NOT NULL DEFAULT 0," +
												"SUMMARY TEXT  NOT NULL ," +
												"PICTURE_QUALITY VARCHAR(200)  NOT NULL ," +
												"AUDIO_QUALITY VARCHAR(200)  NOT NULL ," +
												"EDITING_QUALITY VARCHAR(200)  NOT NULL ," +
												"EDIT_START_DATE DATE  NULL DEFAULT NULL," +
												"EDIT_FINISH_DATE DATE  NULL DEFAULT NULL," +
												"THEMATIC_QUALITY VARCHAR(200)  NOT NULL ," +
												"VIDEO_PRODUCTION_START_DATE DATE  NOT NULL ," +
												"VIDEO_PRODUCTION_END_DATE DATE  NOT NULL ," +
												"STORYBASE INT  NOT NULL DEFAULT 0," +
												"STORYBOARD_FILENAME VARCHAR(100)  NOT NULL ," +
												"RAW_FILENAME VARCHAR(100)  NOT NULL ," +
												"MOVIE_MAKER_PROJECT_FILENAME VARCHAR(100)  NOT NULL ," +
												"FINAL_EDITED_FILENAME VARCHAR(100)  NOT NULL ," +
												"village_id INT NOT NULL DEFAULT 0," +
												"facilitator_id INT  NOT NULL DEFAULT 0," +
												"cameraoperator_id INT  NOT NULL DEFAULT 0," +
												"reviewer_id INT  NULL DEFAULT NULL," +
												"APPROVAL_DATE DATE  NULL DEFAULT NULL," +
												"supplementary_video_produced_id INT  NULL DEFAULT NULL," +
												"VIDEO_SUITABLE_FOR INT  NOT NULL DEFAULT 0," +
												"REMARKS TEXT  NOT NULL ," +
												"ACTORS VARCHAR(1)  NOT NULL ," +
												"last_modified DATETIME  NOT NULL, " +
												"FOREIGN KEY(village_id) REFERENCES village(id), " +
												"FOREIGN KEY(facilitator_id) REFERENCES animator(id), " +
												"FOREIGN KEY(cameraoperator_id) REFERENCES animator(id), " +
												"FOREIGN KEY(reviewer_id) REFERENCES reviewer(id), " +
												"FOREIGN KEY(language_id) REFERENCES language(id) );";  

	protected static String selectVideos = "SELECT video.id, video.title FROM video ORDER BY (video.title);";
	protected static String listVideos = "SELECT video.id, video.title, video.video_production_start_date, " +
										 "video.video_production_end_date, video.village_id, village.village_name " +
										 "FROM video JOIN village ON video.village_id = village.id ORDER BY (-video.id);";
	protected static String saveVideoOnlineURL = "/dashboard/savevideoonline/";
	protected static String getVideoOnlineURL = "/dashboard/getvideosonline/";
	protected static String saveVideoOfflineURL = "/dashboard/savevideooffline/";
	protected String table_name = "video";
	protected String[] fields = {"id", "title", "video_type", "duration", "language", "summary", "picture_quality","audio_quality",
								"editing_quality", "edit_start_date", "edit_finish_date", "thematic_quality", "video_production_start_date", 
								"video_production_end_date", "storybase","storyboard_filename", "raw_filename", "movie_maker_project_filename",
								"final_edited_filename", "village", "facilitator", "cameraoperator", "reviewer", "approval_date", "supplementary_video_produced",
								"video_suitable_for", "remarks", "related_agricultural_practices","farmers_shown","actors", "last_modified"}; 		
	
	public VideosData() {
		super();
	}
	
	public VideosData(OnlineOfflineCallbacks callbacks) {
		super(callbacks);
	}
	
	public VideosData(OnlineOfflineCallbacks callbacks, Form form) {
		super(callbacks, form);
	}
	

	@Override
	public Data getNewData() {
		return new Data();
	}
	
	@Override
	protected String getTableId() {
		return VideosData.tableID;
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
		return VideosData.getVideoOnlineURL;
	}

	
	public final native JsArray<Type> asArrayOfData(String json) /*-{
		return eval(json);
	}-*/;
	
	public List serialize(JsArray<Type> videoObjects){
		List videos = new ArrayList();
		VillagesData village = new VillagesData();
		for(int i = 0; i < videoObjects.length(); i++){
			VillagesData.Data v = village.new Data(videoObjects.get(i).getVillage().getPk(), videoObjects.get(i).getVillage().getVillageName()) ;
			Data video = new Data(videoObjects.get(i).getPk(), videoObjects.get(i).getTitle(), videoObjects.get(i).getVideoProductionStartDate(), videoObjects.get(i).getVideoProductionEndDate(), v);
			videos.add(video);
		}
		
		return videos;
	}
	
	@Override
	public List getListingOnline(String json){
		return this.serialize(this.asArrayOfData(json));		
	}
	
	public List getVideosListingOffline(){
		BaseData.dbOpen();
		List videos = new ArrayList();
		VillagesData village = new VillagesData();
		this.select(listVideos);
		if (this.getResultSet().isValidRow()){
			try {
				for (int i = 0; this.getResultSet().isValidRow(); ++i, this.getResultSet().next()) {
					VillagesData.Data v = village.new Data(this.getResultSet().getFieldAsString(4),  this.getResultSet().getFieldAsString(5)) ;
					Data video = new Data(this.getResultSet().getFieldAsString(0), this.getResultSet().getFieldAsString(1), this.getResultSet().getFieldAsString(2),this.getResultSet().getFieldAsString(3), v);
					videos.add(video);
	    	      }				
			} catch (DatabaseException e) {
				Window.alert("Database Exception : " + e.toString());
				// TODO Auto-generated catch block
				BaseData.dbClose();
			}
			
		}
		BaseData.dbClose();
		return videos;
	}
	
	public List getAllVideosOffline(){
		BaseData.dbOpen();
		List videos = new ArrayList();
		this.select(selectVideos);
		if (this.getResultSet().isValidRow()){
			try {
				for (int i = 0; this.getResultSet().isValidRow(); ++i, this.getResultSet().next()) {
					Data video = new Data(this.getResultSet().getFieldAsString(0), this.getResultSet().getFieldAsString(1));
					videos.add(video);
	    	      }				
			} catch (DatabaseException e) {
				Window.alert("Database Exception : " + e.toString());
				// TODO Auto-generated catch block
				BaseData.dbClose();
			}
			
		}
		BaseData.dbClose();
		return videos;
	}
	
	
	public Object postPageData() {
		if(BaseData.isOnline()){
			this.post(RequestContext.SERVER_HOST + VideosData.saveVideoOnlineURL, this.form.getQueryString());
		}
		else{
			this.save();
			return true;
		}
		
		return false;
	}
	
	public Object getListPageData(){
		if(BaseData.isOnline()){
			this.get(RequestContext.SERVER_HOST + VideosData.getVideoOnlineURL);
		}
		else{
			return true;
		}
		return false;
	}	
	
	public String retrieveDataAndConvertResultIntoHtml(){
		LanguagesData languageData = new LanguagesData();
		List languages = languageData.getAllLanguagesOffline();
		LanguagesData.Data language;
		String html = "<select name=\"language\" id=\"id_language\">";
		for(int i=0; i< languages.size(); i++){
			language = (LanguagesData.Data)languages.get(i);
			html = html + "<option value = \"" + language.getId() +"\">" + language.getLanguageName() + "</option>";
		}
		html = html + "</select>";
		
		AnimatorsData animatorData = new AnimatorsData();
		List facilitators = animatorData.getAllAnimatorsOffline();
		AnimatorsData.Data facilitator;
		html = html + "<select name=\"facilitator\" id=\"id_facilitator\">";
		for(int i=0; i< facilitators.size(); i++){
			facilitator = (AnimatorsData.Data)facilitators.get(i);
			html = html + "<option value = \"" + facilitator.getId() +"\">" + facilitator.getAnimatorName() + "</option>";
		}
		html = html + "</select>";
		
		List cameraoperators = animatorData.getAllAnimatorsOffline();
		AnimatorsData.Data cameraoperator;
		html = html + "<select name=\"cameraoperator\" id=\"id_cameraoperator\">";
		for(int i=0; i< cameraoperators.size(); i++){
			cameraoperator = (AnimatorsData.Data)cameraoperators.get(i);
			html = html + "<option value = \"" + cameraoperator.getId() +"\">" + cameraoperator.getAnimatorName() + "</option>";
		}
		html = html + "</select>";
		
		return html;
	}
	
	public Object getAddPageData(){
		if(BaseData.isOnline()){
			this.get(RequestContext.SERVER_HOST + VideosData.saveVideoOnlineURL);
		}
		else{
			return retrieveDataAndConvertResultIntoHtml();
		}
		return false;
	}
	

}
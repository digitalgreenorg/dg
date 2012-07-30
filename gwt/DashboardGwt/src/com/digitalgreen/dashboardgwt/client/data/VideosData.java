package com.digitalgreen.dashboardgwt.client.data;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.TrainingAnimatorsTrainedData.Data;
import com.digitalgreen.dashboardgwt.client.data.validation.DateValidator;
import com.digitalgreen.dashboardgwt.client.data.validation.ManyToManyValidator;
import com.digitalgreen.dashboardgwt.client.data.validation.StringValidator;
import com.digitalgreen.dashboardgwt.client.data.validation.UniqueConstraintValidator;
import com.google.gwt.core.client.JsArray;
import com.google.gwt.gears.client.database.DatabaseException;
import com.google.gwt.user.client.Window;

public class VideosData extends BaseData {

	public static class Type extends BaseData.Type{
		protected Type() {}
		public final native String getTitle() /*-{ return $wnd.checkForNullValues(this.fields.title); }-*/;
		public final native String getVideoType() /*-{ return $wnd.checkForNullValues(this.fields.video_type);}-*/;
		public final native String getDuration() /*-{ return $wnd.checkForNullValues(this.fields.duration); }-*/;
		public final native String getLanguage() /*-{ return this.fields.language; }-*/;
		public final native String getSummary() /*-{ return $wnd.checkForNullValues(this.fields.summary); }-*/;
		public final native String getPictureQuality()/*-{ return  $wnd.checkForNullValues(this.fields.picture_quality); }-*/;
		public final native String getAudioQuality()/*-{ return  $wnd.checkForNullValues(this.fields.audio_quality); }-*/;
		public final native String getEditingQuality()/*-{ return  $wnd.checkForNullValues(this.fields.editing_quality); }-*/;
		public final native String getEditStartDate()/*-{ return  $wnd.checkForNullValues(this.fields.edit_start_date); }-*/;
		public final native String getEditFinishDate()/*-{ return  $wnd.checkForNullValues(this.fields.edit_finish_date); }-*/;
		public final native String getThematicQuality()/*-{ return  $wnd.checkForNullValues(this.fields.thematic_quality); }-*/;
		public final native String getVideoProductionStartDate() /*-{ return $wnd.checkForNullValues(this.fields.video_production_start_date); }-*/;
		public final native String getVideoProductionEndDate() /*-{ return $wnd.checkForNullValues(this.fields.video_production_end_date); }-*/;
		public final native String getStorybase()/*-{ return  $wnd.checkForNullValues(this.fields.storybase); }-*/;
		public final native String getStoryboardFilename()/*-{ return  $wnd.checkForNullValues(this.fields.storyboard_filename); }-*/;
		public final native String getRawFilename()/*-{ return  $wnd.checkForNullValues(this.fields.raw_filename); }-*/;
		public final native String getMovieMakerProjectFilename()/*-{ return  $wnd.checkForNullValues(this.fields.movie_maker_project_filename); }-*/;
		public final native String getFinalEditedFilename()/*-{ return  $wnd.checkForNullValues(this.fields.final_edited_filename); }-*/;
		public final native VillagesData.Type getVillage() /*-{ return this.fields.village }-*/;
		public final native String getFacilitator() /*-{ return this.fields.facilitator }-*/;
		public final native String getCameraOperator() /*-{ return this.fields.cameraoperator }-*/;
		public final native String getReviewer() /*-{ return this.fields.reviewer; }-*/;
		public final native String getApprovalDate()/*-{ return  $wnd.checkForNullValues(this.fields.approval_date); }-*/;
		public final native String getSupplementaryVideoProduced()/*-{ return  this.fields.supplementary_video_produced; }-*/;
		public final native String getVideoSuitableFor()/*-{ return  $wnd.checkForNullValues(this.fields.video_suitable_for); }-*/;
		public final native String getRemarks()/*-{ return  $wnd.checkForNullValues(this.fields.remarks); }-*/;
		public final native String getActors()/*-{ return  $wnd.checkForNullValues(this.fields.actors); }-*/;
		public final native String getLastModified()/*-{ return  $wnd.checkForNullValues(this.fields.last_modified); }-*/;
		public final native String getYouTubeId()/*-{ return  $wnd.checkForNullValues(this.fields.youtubeid); }-*/;
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
	    private String actors;
	    private String last_modified;
	    private ArrayList related_agricultural_practices;
	    private ArrayList farmers_shown;
	    private String youtubeid;
		
		public Data() {
			super();
			this.related_agricultural_practices = new ArrayList();
			this.farmers_shown = new ArrayList();
			this.addManyToManyRelationship("person", 
					(new VideoFarmersShownData()), 
					"farmers_shown");
		}
		
		public Data(String id) {
			super();
			this.id = id;
		}
		
		public Data(String id, String title) {
			super();
			this.id = id;
			this.title = title;
		}
		
		public Data(String id, String title, VillagesData.Data village) {
			super();
			this.id = id;
			this.title = title;
			this.village = village;
		}

		public Data(String id, String title ,String video_production_start_date, String video_production_end_date,  VillagesData.Data village) {
			super();
			this.id = id;
			this.title = title;
			this.video_production_start_date = video_production_start_date;
			this.video_production_end_date = video_production_end_date;
			this.village = village;
		}
		
		public Data(String id,String title, String video_type, String duration, LanguagesData.Data language, String summary, 
				String picture_quality, String audio_quality, String editing_quality, String edit_start_date, String edit_finish_date, 
				String thematic_quality, String video_production_start_date, String video_production_end_date, String storybase, 
				String storyboard_filename, String raw_filename, String movie_maker_project_filename, String final_edited_filename, 
				VillagesData.Data village, AnimatorsData.Data facilitator, AnimatorsData.Data cameraoperator, ReviewersData.Data reviewer, 
				String approval_date, VideosData.Data supplementary_video_produced, String video_suitable_for, String remarks, 
				String actors, String last_modified, String youtubeid){
			
			super();
			this.id = id;
			this.title = title;
			this.video_type = video_type;
			this.duration = duration;
			this.language = language;
			this.summary = summary;
			this.picture_quality = picture_quality;
			this.audio_quality = audio_quality;
			this.editing_quality = editing_quality;
			this.edit_start_date = edit_start_date;
			this.edit_finish_date = edit_finish_date;
			this.thematic_quality = thematic_quality;
			this.video_production_start_date = video_production_start_date;
			this.video_production_end_date = video_production_end_date;
			this.storybase = storybase;
			this.storyboard_filename = storyboard_filename;
			this.raw_filename = raw_filename;
			this.movie_maker_project_filename = movie_maker_project_filename;
			this.final_edited_filename = final_edited_filename;
			this.village = village;
			this.facilitator = facilitator;
			this.cameraoperator = cameraoperator;
			this.reviewer = reviewer;
			this.approval_date = approval_date;
			this.supplementary_video_produced = supplementary_video_produced;
			this.video_suitable_for = video_suitable_for;
			this.remarks = remarks;
			this.actors = actors;
			this.last_modified = last_modified;
			this.youtubeid = youtubeid;
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
			obj.language = (new LanguagesData()).new Data();
			obj.village = (new VillagesData()).new Data();
			obj.cameraoperator = (new AnimatorsData()).new Data();
			obj.facilitator = (new AnimatorsData()).new Data();
			obj.reviewer = (new ReviewersData()).new Data();
			obj.supplementary_video_produced = (new VideosData()).new Data();
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
			}else if(key.equals("title")) {
				this.title = (String)val;
			} else if(key.equals("video_type")){
				this.video_type = val;
			} else if(key.equals("duration")){
				this.duration = val;	
			} else if (key.equals("language")) {
				LanguagesData language = new LanguagesData();
				this.language = language.getNewData();
				this.language.id = val;
			} else if (key.equals("summary")){
				this.summary = (String)val;
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
			} else if(key.equals("video_production_start_date")) {
				this.video_production_start_date = (String)val;
			} else if (key.equals("video_production_end_date")) {
				this.video_production_end_date = (String)val;
			} else if (key.equals("storybase")){
				this.storybase = val;
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
			} else if(key.equals("video_suitable_for")) {
				this.video_suitable_for = (String)val;
			} else if(key.equals("remarks")) {
				this.remarks = (String)val;
			} else if(key.equals("actors")) {
				this.actors = (String)val;
			} else if(key.equals("related_agricultural_practices")){
				this.related_agricultural_practices.add(val);
			} else if(key.equals("farmers_shown")){
				this.farmers_shown.add(val);
			} else if(key.equals("youtubeid")){
				this.youtubeid = (String)val;
			} else {
				return;
			}
			this.addNameValueToQueryString(key, val);		
		}
		
		@Override
		public boolean validate() {
			//Labels to print error messages
			String titleLabel = "Title";
			String videoTypeLabel = "Video Type";
			String videoProductionStartDateLabel = "Video Production Start Date";
			String videoProductionEndDateLabel = "Video Production End Date";
			String languageLabel = "Language";
			String storybaseLabel = "Story Base";
			String summaryLabel = "Summary";
			String villageLabel = "Village";
			String facilitatorLabel = "Facilitator";
			String cameraOperatorLabel = "Camera Operator";
			String relatedAgriculturalPracticesLabel = "Related Agricultural Practices";
			String farmersShownLabel = "Farmers Shown";
			String actorsLabel = "Actors";
			String pictureQualityLabel = "Picture Quality";
			String audioQualityLabel = "Audio Quality";
			String editingQualityLabel = "Editing Quality";
			String editStartDateLabel = "Edit Start Date";
			String editFinishDateLabel = "Edit FInish Date";
			String thematic_qualityLabel = "Thematic Quality";
			String approvalDateLabel = "Approval Date";
			String videoSuitableForLabel = "Video Suitable For";
			String remarksLabel = "Remarks";
			String youtubeIdLabel = "YouTubeId";
						
			StringValidator title = new StringValidator(titleLabel, this.title, false, false, 1, 200, true);
			StringValidator videoType = new StringValidator(videoTypeLabel, this.video_type, false, false, 1, 1);
			DateValidator videoProductionStartDate = new DateValidator(videoProductionStartDateLabel, this.video_production_start_date, 
					false, false);
			DateValidator videoProductionEndDate = new DateValidator(videoProductionEndDateLabel, this.video_production_end_date, false, false);
			StringValidator language = new StringValidator(languageLabel, this.language.getId(), false, false, 1, 100);
			StringValidator storybase = new StringValidator(storybaseLabel, this.storybase, false, false, 1, 1);
			StringValidator summary = new StringValidator(summaryLabel, this.summary, true, false, 0, 1024);
			StringValidator village = new StringValidator(villageLabel, this.facilitator.getId(), false, false, 1, 100);
			StringValidator facilitator = new StringValidator(facilitatorLabel, this.village.getId(), false, false, 1, 100);
			StringValidator cameraOperator = new StringValidator(cameraOperatorLabel, this.cameraoperator.getId(), false, false, 1, 100);
			ManyToManyValidator relatedAgriculturalPractices = new ManyToManyValidator(relatedAgriculturalPracticesLabel,
					this.related_agricultural_practices, true);
			ManyToManyValidator farmersShown = new ManyToManyValidator(farmersShownLabel, this.farmers_shown, false);
			StringValidator actors = new StringValidator(actorsLabel, this.actors, false, false, 1, 1);
			StringValidator pictureQuality = new StringValidator( pictureQualityLabel, this.picture_quality, true, false, 0, 200,true);
			StringValidator audioQuality = new StringValidator(audioQualityLabel, this.audio_quality, true, true, 0, 200,true);
			StringValidator editingQuality = new StringValidator(editingQualityLabel, this.editing_quality, true, true, 0, 200,true);
			DateValidator editStartDate = new DateValidator(editStartDateLabel, this.edit_start_date, true, true);
			DateValidator editFinishDate = new DateValidator(editFinishDateLabel, this.edit_finish_date, true, true);
			StringValidator thematic_quality = new StringValidator(thematic_qualityLabel, this.thematic_quality, true, true, 0, 200,true);
			DateValidator approvalDate = new DateValidator(approvalDateLabel, this.approval_date, true, true);
			StringValidator videoSuitableFor = new StringValidator(videoSuitableForLabel, this.video_suitable_for, false, false, 1, 1);
			StringValidator remarks = new StringValidator(remarksLabel, this.remarks, true, true, 0, 500);
			StringValidator youtubeid = new StringValidator(youtubeIdLabel, this.youtubeid, true, true, 0, 20);
			youtubeid.setError("Please make sure 'Youtubeid' is less than 20 CHARACTERS.");
			
			ArrayList uniqueTitle = new ArrayList();
			uniqueTitle.add("TITLE");
			uniqueTitle.add(this.title);
			
			ArrayList uniqueVideoProductionStartDate = new ArrayList();
			uniqueVideoProductionStartDate.add("VIDEO_PRODUCTION_START_DATE");
			uniqueVideoProductionStartDate.add(this.video_production_start_date);
			
			ArrayList uniqueVideoProductionEndDate = new ArrayList();
			uniqueVideoProductionEndDate.add("VIDEO_PRODUCTION_END_DATE");
			uniqueVideoProductionEndDate.add(this.video_production_end_date);
			
			ArrayList uniqueVillage = new ArrayList();
			uniqueVillage.add("village_id");
			uniqueVillage.add(this.village.getId());
			
			ArrayList uniqueTogether = new ArrayList();
			uniqueTogether.add(uniqueTitle);
			uniqueTogether.add(uniqueVideoProductionStartDate);
			uniqueTogether.add(uniqueVideoProductionEndDate);
			uniqueTogether.add(uniqueVillage);
			
			ArrayList uniqueValidatorLabels = new ArrayList();
			uniqueValidatorLabels.add("Title");
			uniqueValidatorLabels.add("Video Production Start Date");
			uniqueValidatorLabels.add("Video Production End Date");
			uniqueValidatorLabels.add("Village");
			UniqueConstraintValidator uniqueTitleStartEndDateVillageID = new UniqueConstraintValidator(uniqueValidatorLabels,
					uniqueTogether, new VideosData());
			uniqueTitleStartEndDateVillageID.setCheckId(this.getId());
			ArrayList validatorList = new ArrayList();
			validatorList.add(title);
			validatorList.add(videoType);
			validatorList.add(videoProductionStartDate);
			validatorList.add(videoProductionEndDate);
			validatorList.add(language);
			validatorList.add(storybase);
			validatorList.add(summary);
			validatorList.add(village);
			validatorList.add(facilitator);
			validatorList.add(cameraOperator);
			validatorList.add(relatedAgriculturalPractices);
			validatorList.add(farmersShown);
			validatorList.add(actors);
			validatorList.add(pictureQuality);
			validatorList.add(audioQuality);
			validatorList.add(editingQuality);
			validatorList.add(editStartDate);
			validatorList.add(editFinishDate);
			validatorList.add(thematic_quality);
			validatorList.add(approvalDate);
			validatorList.add(videoSuitableFor);
			validatorList.add(remarks);
			validatorList.add(youtubeid);
			validatorList.add(uniqueTitleStartEndDateVillageID);
			return this.executeValidators(validatorList);
		}
		
		@Override
		public void save() {
			this.last_modified = BaseData.getCurrentDateAndTime();
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
						this.last_modified,
						this.youtubeid);
			this.addNameValueToQueryString("id", this.id);
		}
		
		@Override
		public String toQueryString(String id) {
			VideosData videosData = new VideosData();
			return this.rowToQueryString(videosData.getTableName(), videosData.getFields(), "id", id, "");
		}
		
		@Override
		public String getTableId() {
			VideosData videosDataDbApis = new VideosData();
			return videosDataDbApis.tableID;
		}
	}
	
	public static String tableID = "27";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `video` " +
												"(id BIGINT UNSIGNED PRIMARY KEY  NOT NULL ," +
												"TITLE VARCHAR(200)  NOT NULL ," +
												"VIDEO_TYPE INT  NOT NULL," +
												"DURATION TIME  NULL DEFAULT NULL," +
												"language_id BIGINT UNSIGNED  NOT NULL ," +
												"SUMMARY TEXT  NULL DEFAULT NULL ," +
												"PICTURE_QUALITY VARCHAR(200) NULL DEFAULT NULL," +
												"AUDIO_QUALITY VARCHAR(200)  NULL DEFAULT NULL," +
												"EDITING_QUALITY VARCHAR(200)  NULL DEFAULT NULL," +
												"EDIT_START_DATE DATE  NULL DEFAULT NULL," +
												"EDIT_FINISH_DATE DATE  NULL DEFAULT NULL," +
												"THEMATIC_QUALITY VARCHAR(200)  NULL DEFAULT NULL ," +
												"VIDEO_PRODUCTION_START_DATE DATE  NOT NULL ," +
												"VIDEO_PRODUCTION_END_DATE DATE  NOT NULL ," +
												"STORYBASE INT  NOT NULL," +
												"STORYBOARD_FILENAME VARCHAR(100)  NULL DEFAULT NULL ," +
												"RAW_FILENAME VARCHAR(100)  NULL DEFAULT NULL," +
												"MOVIE_MAKER_PROJECT_FILENAME VARCHAR(100)  NULL DEFAULT NULL," +
												"FINAL_EDITED_FILENAME VARCHAR(100)  NULL DEFAULT NULL," +
												"village_id BIGINT UNSIGNED NOT NULL," +
												"facilitator_id BIGINT UNSIGNED  NOT NULL," +
												"cameraoperator_id BIGINT UNSIGNED  NOT NULL," +
												"reviewer_id BIGINT UNSIGNED  NULL DEFAULT NULL," +
												"APPROVAL_DATE DATE  NULL DEFAULT NULL," +
												"supplementary_video_produced_id BIGINT UNSIGNED  NULL DEFAULT NULL," +
												"VIDEO_SUITABLE_FOR INT NOT NULL," +
												"REMARKS TEXT  NULL DEFAULT NULL," +
												"ACTORS VARCHAR(1)  NOT NULL ," +
												"last_modified DATETIME  NOT NULL, " +
												"youtubeid VARCHAR(20)  NULL DEFAULT NULL ," +
												"FOREIGN KEY(village_id) REFERENCES village(id), " +
												"FOREIGN KEY(facilitator_id) REFERENCES animator(id), " +
												"FOREIGN KEY(cameraoperator_id) REFERENCES animator(id), " +
												"FOREIGN KEY(reviewer_id) REFERENCES reviewer(id), " +
												"FOREIGN KEY(language_id) REFERENCES language(id) );";
	protected static String dropTable = "DROP TABLE IF EXISTS `video`;";
	protected static String[] createIndexes = {"CREATE INDEX IF NOT EXISTS video_PRIMARY ON video(id);", 
											"CREATE INDEX IF NOT EXISTS video_village_id ON video(village_id);",
											"CREATE INDEX IF NOT EXISTS video_facilitator_id ON video(facilitator_id);",
											"CREATE INDEX IF NOT EXISTS video_cameraoperator_id ON video(cameraoperator_id);",
											"CREATE INDEX IF NOT EXISTS video_reviewer_id ON video(reviewer_id);",
											"CREATE INDEX IF NOT EXISTS video_language_id ON video(language_id);"};
	protected static String selectVideos = "SELECT video.id, video.title, village.id, village.village_name " +
										   "FROM video JOIN village ON video.village_id = village.id" +
										   " ORDER BY (video.title);";
	protected static String listVideos = "SELECT video.id, video.title, video.video_production_start_date, " +
										 "video.video_production_end_date, video.village_id, village.village_name " +
										 "FROM video JOIN village ON video.village_id = village.id ORDER BY LOWER(video.title);";
	protected static String selectVideosSeenForPerson = "SELECT DISTINCT vid.id, vid.title FROM video vid " +
		"JOIN screening_videos_screened svs ON svs.video_id = vid.id " +
		"JOIN person_meeting_attendance pma ON pma.screening_id = svs.screening_id " +
		"WHERE person_id = ";
	protected static String saveVideoOnlineURL = "/dashboard/savevideoonline/";
	protected static String getVideoOnlineURL = "/dashboard/getvideosonline/";
	protected static String saveVideoOfflineURL = "/dashboard/savevideooffline/";
	protected String table_name = "video";
	protected String[] fields = {"id", "title", "video_type", "duration", "language_id", "summary", "picture_quality","audio_quality",
								"editing_quality", "edit_start_date", "edit_finish_date", "thematic_quality", "video_production_start_date", 
								"video_production_end_date", "storybase","storyboard_filename", "raw_filename", "movie_maker_project_filename",
								"final_edited_filename", "village_id", "facilitator_id", "cameraoperator_id", "reviewer_id", "approval_date", "supplementary_video_produced_id",
								"video_suitable_for", "remarks","actors", "last_modified", "youtubeid"}; 		
	
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
		return VideosData.getVideoOnlineURL;
	}
	
	@Override
	public String getSaveOfflineURL(){
		return VideosData.saveVideoOfflineURL;
	}
	
	@Override
	public String getSaveOnlineURL(){
		return VideosData.saveVideoOnlineURL;
	}
	
	public final native JsArray<Type> asArrayOfData(String json) /*-{
		return eval(json);
	}-*/;
	
	public List serialize(JsArray<Type> videoObjects){
		List videos = new ArrayList();
		LanguagesData language = new LanguagesData();
		VillagesData village = new VillagesData();
		AnimatorsData facilitator = new AnimatorsData();
		AnimatorsData cameraoperator = new AnimatorsData();
		ReviewersData reviewer = new ReviewersData();
		VideosData video1 = new VideosData();
		PersonsData person = new PersonsData();
		
		for(int i = 0; i < videoObjects.length(); i++){
			ReviewersData.Data r = reviewer.new Data();
			VideosData.Data vd1 = video1.new Data();
			
			LanguagesData.Data l = language.new Data(videoObjects.get(i).getLanguage());
			
			VillagesData.Data vl = village.new Data(videoObjects.get(i).getVillage().getPk(), 
													videoObjects.get(i).getVillage().getVillageName()) ;
			
			AnimatorsData.Data f = facilitator.new Data(videoObjects.get(i).getFacilitator());
			
			AnimatorsData.Data c = cameraoperator.new Data(videoObjects.get(i).getCameraOperator());
			
			if(videoObjects.get(i).getReviewer() != null){
				r = reviewer.new Data(videoObjects.get(i).getReviewer());
			}
			
			if(videoObjects.get(i).getSupplementaryVideoProduced() != null){
				vd1 = video1.new Data(videoObjects.get(i).getSupplementaryVideoProduced());
			}
					
			Data video = new Data(videoObjects.get(i).getPk(), 
									videoObjects.get(i).getTitle(),
									videoObjects.get(i).getVideoType(),
									videoObjects.get(i).getDuration(), l,
									videoObjects.get(i).getSummary(),
									videoObjects.get(i).getPictureQuality(),
									videoObjects.get(i).getAudioQuality(),
									videoObjects.get(i).getEditingQuality(),
									videoObjects.get(i).getEditStartDate(),
									videoObjects.get(i).getEditFinishDate(),
									videoObjects.get(i).getThematicQuality(),
									videoObjects.get(i).getVideoProductionStartDate(), 
									videoObjects.get(i).getVideoProductionEndDate(), 
									videoObjects.get(i).getStorybase(),
									videoObjects.get(i).getStoryboardFilename(),
									videoObjects.get(i).getRawFilename(),
									videoObjects.get(i).getMovieMakerProjectFilename(),
									videoObjects.get(i).getFinalEditedFilename(), vl, f, c, r,
									videoObjects.get(i).getApprovalDate(), vd1,
									videoObjects.get(i).getVideoSuitableFor(),
									videoObjects.get(i).getRemarks(),
									videoObjects.get(i).getActors(),
									videoObjects.get(i).getLastModified(),
									videoObjects.get(i).getYouTubeId());

			videos.add(video);
		}
		return videos;
	}
	
	@Override
	public List getListingOnline(String json){
		return this.serialize(this.asArrayOfData(json));		
	}
	
	public List getVideosListingOffline(String... pageNum){
		BaseData.dbOpen();
		List videos = new ArrayList();
		VillagesData village = new VillagesData();
		String listTemp;
		if(pageNum.length == 0) {
			listTemp = listVideos;
		}
		else {
			int offset = (Integer.parseInt(pageNum[0]) - 1)*pageSize;
			if(pageNum.length == 1) {
				listTemp = listVideos + " LIMIT "+ Integer.toString(offset) + " , "+Integer.toString(pageSize) +";";
			} else {
				listTemp = "SELECT vid.id, vid.title, vid.video_production_start_date, " +
				 				"vid.video_production_end_date, vid.village_id, vil.village_name " +
							"FROM video vid, village vil " +
							"WHERE  vid.village_id = vil.id AND ( vid.video_production_start_date LIKE '%"+pageNum[1]+"%' " + 
									" OR vid.video_production_end_date LIKE '%"+pageNum[1]+"%' " + " OR vid.id LIKE '%"+pageNum[1]+"%' " +
									" OR vid.title LIKE '%"+pageNum[1]+"%' " +
									"OR vil.VILLAGE_NAME" +	" LIKE '%"+pageNum[1]+"%' )" +" ORDER BY(vid.title) " 
									+ " LIMIT "+ Integer.toString(offset)+" , "+Integer.toString(pageSize)+ ";";
			}		
		}
		this.select(listTemp);
		if (this.getResultSet().isValidRow()){
			try {
				for (int i = 0; this.getResultSet().isValidRow(); ++i, this.getResultSet().next()) {
					VillagesData.Data v = village.new Data(this.getResultSet().getFieldAsString(4),  this.getResultSet().getFieldAsString(5)) ;
					Data video = new Data(this.getResultSet().getFieldAsString(0), this.getResultSet().getFieldAsString(1), this.getResultSet().getFieldAsString(2),this.getResultSet().getFieldAsString(3), v);
					videos.add(video);
	    	      }				
			} catch (DatabaseException e) {
				Window.alert("Database Exception : " + e.toString());
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
				VillagesData villagesData = new VillagesData();
				VillagesData.Data village;
				for (int i = 0; this.getResultSet().isValidRow(); ++i, this.getResultSet().next()) {
					village = villagesData.new Data(this.getResultSet().getFieldAsString(2), this.getResultSet().getFieldAsString(3));
					Data video = new Data(this.getResultSet().getFieldAsString(0), this.getResultSet().getFieldAsString(1), village);
					videos.add(video);
	    	      }				
			} catch (DatabaseException e) {
				Window.alert("Database Exception : " + e.toString());
				BaseData.dbClose();
			}
		}
		BaseData.dbClose();
		return videos;
	}
	
	public List getVideoSeenForPersonOffline(String person_id) {
		BaseData.dbOpen();
		List videos = new ArrayList();
		this.select(selectVideosSeenForPerson + person_id);
		if(this.getResultSet().isValidRow()){
			try {
				for(int i = 0; this.getResultSet().isValidRow(); ++i, this.getResultSet().next()){
					Data video = new Data(this.getResultSet().getFieldAsString(0), this.getResultSet().getFieldAsString(1));
					videos.add(video);
				}
			}
			catch(DatabaseException e){
				Window.alert("Database Exception : " + e.toString());
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
			if(this.validate()) {
				this.save();
				return true;
			}
		}
		
		return false;
	}
	
	public Object postPageData(String id) {
		if(BaseData.isOnline()){
			this.post(RequestContext.SERVER_HOST + this.saveVideoOnlineURL + id + "/", this.form.getQueryString());
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
				this.get(RequestContext.SERVER_HOST + VideosData.getVideoOnlineURL +
						Integer.toString(offset)+"/"+Integer.toString(limit)+"/" + "?searchText="+pageNum[1]);
			} else {
				this.get(RequestContext.SERVER_HOST + VideosData.getVideoOnlineURL + Integer.toString(offset) + "/" 
						+ Integer.toString(limit)+ "/");
			}
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
		String html = "<select name=\"language\" id=\"id_language\">" + 
					"<option value='' selected='selected'>---------</option>";
		for(int i=0; i< languages.size(); i++){
			language = (LanguagesData.Data)languages.get(i);
			html = html + "<option value = \"" + language.getId() +"\">" + language.getLanguageName() + "</option>";
		}
		html = html + "</select>";
		
		VillagesData villageData = new VillagesData();
		List villages = villageData.getAllVillagesOffline();
		VillagesData.Data village;
		html = html + "<select name=\"village\" id=\"id_village\">" + 
			"<option value='' selected='selected'>---------</option>";
		for(int i =0; i< villages.size(); i++){
			village = (VillagesData.Data)villages.get(i);
			html = html + "<option value = \"" + village.getId() + "\">" + village.getVillageName() + "</option>";
		}
		html = html + "</select>";
		
		AnimatorsData animatorData = new AnimatorsData();
		List facilitators = animatorData.getAllAnimatorsOffline();
		AnimatorsData.Data facilitator;
		html = html + "<select name=\"facilitator\" id=\"id_facilitator\">" + 
				"<option value='' selected='selected'>---------</option>";
		for(int i=0; i< facilitators.size(); i++){
			facilitator = (AnimatorsData.Data)facilitators.get(i);
			html = html + "<option value = \"" + facilitator.getId() +"\">" + facilitator.getAnimatorName() + "</option>";
		}
		html = html + "</select>";
		
		List cameraoperators = animatorData.getAllAnimatorsOffline();
		AnimatorsData.Data cameraoperator;
		html = html + "<select name=\"cameraoperator\" id=\"id_cameraoperator\">" + 
					"<option value='' selected='selected'>---------</option>";
		for(int i=0; i< cameraoperators.size(); i++){
			cameraoperator = (AnimatorsData.Data)cameraoperators.get(i);
			html = html + "<option value = \"" + cameraoperator.getId() +"\">" + cameraoperator.getAnimatorName() + "</option>";
		}
		html = html + "</select>";
		
		PersonsData personsData = new PersonsData();
		List persons = personsData.getAllPersonsOffline();
		PersonsData.Data person;
		html = html + "<select id='id_farmers_shown' name='farmers_shown' multiple='multiple'>";
		for(int i=0; i<persons.size(); i++ ){
			person = (PersonsData.Data)persons.get(i);
			html = html + "<option value = \"" + person.getId() + "\">" + person.getPersonName() + "(" + person.getVillage().getVillageName() +")" + "</option>";
		}
		html = html + "</select>";

		ReviewersData reviewersData = new ReviewersData();
		List reviewers = reviewersData.getAllReviewersOffline();
		ReviewersData.Data reviewer;
		html = html + "<select id='id_reviewer' name='reviewer'>" +
				" <option selected='selected' value=''>---------</option>";
		
		for(int i =0; i< reviewers.size(); i++){
			reviewer = (ReviewersData.Data) reviewers.get(i);
			html = html + "<option value = \"" + reviewer.getId() + "\">" + reviewer.getReviewerName() +  "</option>";
		}
		html = html + "</select>";
		
		VideosData videosData = new VideosData();
		List videos = videosData.getAllVideosOffline();
		VideosData.Data video;
		html = html + "<select id='id_supplementary_video_produced' name='supplementary_video_produced'>" +
		" <option selected='selected' value=''>---------</option>";
		for(int i= 0; i< videos.size(); i++){
			video = (VideosData.Data) videos.get(i);
			html = html + "<option value = \"" + video.getId() + "\">" + video.getTitle() + "(" + video.getVillage().getVillageName() + ")" + "</option>";
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
	
	public Object getAddPageData(String id){
		if(BaseData.isOnline()){
			this.get(RequestContext.SERVER_HOST + this.saveVideoOnlineURL + id + "/" );
		}
		else {
			this.form.toQueryString(id);
			return retrieveDataAndConvertResultIntoHtml();
		}
		return false;
	}
	
	public String getCount(String searchText) {
		String count = "0";//stores number of rows in a resultset
		String countSql = "SELECT COUNT(*) " +
				"FROM video vid, village vil " +
				"WHERE  vid.village_id = vil.id AND (vid.video_production_start_date LIKE '%"+searchText+"%' " + 
									" OR vid.video_production_end_date LIKE '%"+searchText+"%' " + 
									" OR vid.id LIKE '%"+searchText+"%' " + " OR vid.title LIKE '%"+searchText+"%' " +
									"OR vil.VILLAGE_NAME" +	" LIKE '%"+searchText+"%' );" ;
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
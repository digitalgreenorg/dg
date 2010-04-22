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
		
		public Data() {
			super();
			this.related_agricultural_practices = new ArrayList();
			this.farmers_shown = new ArrayList();
			this.addManyToManyRelationship("practice", 
					(new VideoRelatedAgriculturalPracticesData()).new Data(), 
					"related_agricultural_practices");
			this.addManyToManyRelationship("person", 
					(new VideoFarmersShownData()).new Data(), 
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
				String actors, String last_modified){
			
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
			if(key.equals("title")) {
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
			} else {
				return;
			}
			this.addNameValueToQueryString(key, val);			
		}
		
		@Override
		public boolean validate() {
			StringValidator title = new StringValidator(this.title, false, false, 1, 200);
			title.setError("Please make sure that 'Title' is NOT EMPTY and not more than 200 characters.");
			StringValidator videoType = new StringValidator(this.video_type, false, false, 1, 1);;
			videoType.setError("Please make sure you choose a video type for 'Video type'.");
			DateValidator videoProductionStartDate = new DateValidator(this.video_production_start_date, false, false);
			videoProductionStartDate.setError("Please make sure 'Video production start date' is NOT EMPTY and id formatted as 'YYYY-MM-DD'.");
			DateValidator videoProductionEndDate = new DateValidator(this.video_production_end_date, false, false);
			videoProductionEndDate.setError("Please make sure 'Video production end date' is NOT EMPTY and id formatted as 'YYYY-MM-DD'.");
			StringValidator language = new StringValidator(this.language.getId(), false, false, 1, 100);
			language.setError("Please make sure you choose a language for 'Language'.");
			StringValidator storybase = new StringValidator(this.storybase, false, false, 1, 1);
			storybase.setError("Please make sure you choose a storybase type for 'Storybase'.");
			StringValidator summary = new StringValidator(this.summary, true, false, 0, 1024);
			summary.setError("Please make sure that 'Title' is not more than 1024 CHARACTERS");
			StringValidator village = new StringValidator(this.facilitator.getId(), false, false, 1, 100);
			village.setError("Please make sure you choose a village for 'Village'.");
			StringValidator facilitator = new StringValidator(this.village.getId(), false, false, 1, 100);
			facilitator.setError("Please make sure you choose a facilitator for 'Facilitator'.");
			StringValidator cameraOperator = new StringValidator(this.cameraoperator.getId(), false, false, 1, 100);
			cameraOperator.setError("Please make sure you choose a camera operator for 'Camera Operator'.");
			ManyToManyValidator relatedAgriculturalPractices = new ManyToManyValidator(this.related_agricultural_practices, false);
			relatedAgriculturalPractices.setError("Please make sure you add some practices for 'Related agricultural practices'");
			ManyToManyValidator farmersShown = new ManyToManyValidator(this.related_agricultural_practices, false);
			farmersShown.setError("Please make sure you add some farmers for 'Farmers shown'");
			StringValidator actors = new StringValidator(this.actors, false, false, 1, 1);
			actors.setError("Please make sure you choose a actor for 'Actors'.");
			StringValidator pictureQuality = new StringValidator( this.picture_quality, true, false, 0, 200);
			pictureQuality.setError("Please make sure 'Picture quality' is less than 200 CHARACTERS.");
			StringValidator audioQuality = new StringValidator(this.audio_quality, true, true, 0, 200);
			audioQuality.setError("Please make sure 'Audio quality' is less than 200 CHARACTERS.");
			StringValidator editingQuality = new StringValidator(this.editing_quality, true, true, 0, 200);
			editingQuality.setError("Please make sure 'Editing quality' is less than 200 CHARACTERS.");
			DateValidator editStartDate = new DateValidator(this.edit_start_date, true, true);
			editStartDate.setError("Please make sure 'Edit start date' is formatted as YYYY-MM-DD.");
			DateValidator editFinishDate = new DateValidator(this.edit_finish_date, true, true);
			editFinishDate.setError("Please make sure 'Edit finish date' is formatted as YYYY-MM-DD.");
			StringValidator thematic_quality = new StringValidator(this.thematic_quality, true, true, 0, 200);
			thematic_quality.setError("Please make sure 'Thematic quality' is less than 200 CHARACTERS.");
			DateValidator approvalDate = new DateValidator(this.approval_date, true, true);
			approvalDate.setError("Please make sure 'Approval date' is formatted as YYYY-MM-DD.");
			StringValidator videoSuitableFor = new StringValidator(this.video_suitable_for, false, false, 1, 1);
			videoSuitableFor.setError("Please make sure you choose a video suitable for 'Video suitable for'.");
			StringValidator remarks = new StringValidator(this.remarks, true, true, 0, 500);
			remarks.setError("Please make sure 'Remarks' is less than 500 CHARACTERS.");
			
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
			
			UniqueConstraintValidator uniqueTitleStartEndDateVillageID = new UniqueConstraintValidator(uniqueTogether, new VideosData());
			uniqueTitleStartEndDateVillageID.setError("The Title, video production start date, video production end date, and village are already in the system.  Please make sure they are unique.");

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
			validatorList.add(uniqueTitleStartEndDateVillageID);
			return this.executeValidators(validatorList);
		}
		
		@Override
		public void save() {
			
			if(this.id == null){
				this.last_modified = BaseData.getCurrentDateAndTime();
			}
				
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
			this.addNameValueToQueryString("id", this.id);
		}
		
		@Override
		public String getTableId() {
			VideosData videosDataDbApis = new VideosData();
			return videosDataDbApis.tableID;
		}
	}
	
	public static String tableID = "27";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `video` " +
												"(id INTEGER PRIMARY KEY  NOT NULL ," +
												"TITLE VARCHAR(200)  NOT NULL ," +
												"VIDEO_TYPE INT  NOT NULL DEFAULT 0," +
												"DURATION TIME  NULL DEFAULT NULL," +
												"language_id INT  NOT NULL DEFAULT 0," +
												"SUMMARY TEXT  NULL ," +
												"PICTURE_QUALITY VARCHAR(200) NULL DEFAULT NULL," +
												"AUDIO_QUALITY VARCHAR(200)  NULL DEFAULT NULL," +
												"EDITING_QUALITY VARCHAR(200)  NULL DEFAULT NULL," +
												"EDIT_START_DATE DATE  NULL DEFAULT NULL," +
												"EDIT_FINISH_DATE DATE  NULL DEFAULT NULL," +
												"THEMATIC_QUALITY VARCHAR(200)  NULL DEFAULT NULL ," +
												"VIDEO_PRODUCTION_START_DATE DATE  NOT NULL ," +
												"VIDEO_PRODUCTION_END_DATE DATE  NOT NULL ," +
												"STORYBASE INT  NOT NULL DEFAULT 0," +
												"STORYBOARD_FILENAME VARCHAR(100)  NULL DEFAULT NULL ," +
												"RAW_FILENAME VARCHAR(100)  NULL DEFAULT NULL," +
												"MOVIE_MAKER_PROJECT_FILENAME VARCHAR(100)  NULL DEFAULT NULL," +
												"FINAL_EDITED_FILENAME VARCHAR(100)  NULL DEFAULT NULL," +
												"village_id INT NOT NULL DEFAULT 0," +
												"facilitator_id INT  NOT NULL DEFAULT 0," +
												"cameraoperator_id INT  NOT NULL DEFAULT 0," +
												"reviewer_id INT  NULL DEFAULT NULL," +
												"APPROVAL_DATE DATE  NULL DEFAULT NULL," +
												"supplementary_video_produced_id INT  NULL DEFAULT NULL," +
												"VIDEO_SUITABLE_FOR INT NOT NULL DEFAULT 0," +
												"REMARKS TEXT  NULL DEFAULT NULL," +
												"ACTORS VARCHAR(1)  NOT NULL ," +
												"last_modified DATETIME  NOT NULL, " +
												"FOREIGN KEY(village_id) REFERENCES village(id), " +
												"FOREIGN KEY(facilitator_id) REFERENCES animator(id), " +
												"FOREIGN KEY(cameraoperator_id) REFERENCES animator(id), " +
												"FOREIGN KEY(reviewer_id) REFERENCES reviewer(id), " +
												"FOREIGN KEY(language_id) REFERENCES language(id) );";  
	protected static String dropTable = "DROP TABLE IF EXISTS `video`;";
	protected static String selectVideos = "SELECT video.id, video.title, village.id, village.village_name " +
										   "FROM video JOIN village ON video.village_id = village.id" +
										   " ORDER BY (video.title);";
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
								"video_suitable_for", "remarks","actors", "last_modified"}; 		
	
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
		ReviewersData.Data r = reviewer.new Data();
		VideosData video1 = new VideosData();
		VideosData.Data vd1 = video1.new Data();
		PracticesData practice = new PracticesData();
		PersonsData person = new PersonsData();
		
		for(int i = 0; i < videoObjects.length(); i++){
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
									videoObjects.get(i).getLastModified());

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
		
		PracticesData practicesData = new PracticesData();
		List practices = practicesData.getAllPracticesOffline();
		PracticesData.Data practice;
		html = html+ "<select id='id_related_agricultural_practices' name='related_agricultural_practices' multiple='multiple'>";
		for(int i=0; i<practices.size(); i++){
			practice = (PracticesData.Data)practices.get(i);
			html = html+ "<option value = \"" + practice.getId() + "\">" + practice.getPracticeName() + "</option>";
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
}
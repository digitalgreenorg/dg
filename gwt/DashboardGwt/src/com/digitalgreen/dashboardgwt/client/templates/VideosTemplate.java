package com.digitalgreen.dashboardgwt.client.templates;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.VideosData;
import com.digitalgreen.dashboardgwt.client.servlets.Videos;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.Hyperlink;

public class VideosTemplate extends BaseTemplate {
	
	public VideosTemplate(RequestContext requestContext) {
		super(requestContext);
		this.formTemplate = new Form((new VideosData()).getNewData());;
	}
	
	@Override
	public void fill() {
		String templateType = "Video";
		String templatePlainType = "dashboard/video/add/";
		RequestContext requestContext = new RequestContext();
		HashMap args = new HashMap();
		args.put("action", "add");
		requestContext.setArgs(args);
		requestContext.setForm(this.formTemplate);
		Videos addVideosServlet = new Videos(requestContext);
		RequestContext saveRequestContext = new RequestContext(RequestContext.METHOD_POST);
		Form saveForm = new Form((new VideosData()).getNewData());
		saveRequestContext.setForm(this.formTemplate);
		Videos saveVideo = new Videos(saveRequestContext);
		// Draw the content of the template depending on the request type (GET/POST)
		super.fillDGTemplate(templateType, videosListHtml, videosAddHtml, addDataToElementID);
		// Add it to the rootpanel
		super.fill();
		//Now add listings
		List<Hyperlink> links =  this.fillListings();
		// Now add hyperlinks
		super.fillDgListPage(templatePlainType, templateType, videosListFormHtml, addVideosServlet, links);
		this.displayCalendar();
		// Now add any submit control buttons
		super.fillDgFormPage(saveVideo);
	}
	
	protected List<Hyperlink> fillListings() {
		HashMap queryArgs = this.getRequestContext().getArgs();
		String queryArg = (String)queryArgs.get("action");
		List<Hyperlink> links = new ArrayList<Hyperlink>();
		// If we're unsure, just default to list view
		if(queryArg.equals("list")) {
			// 	Add Listings
			List videos = (List)queryArgs.get("listing");			
			if(videos  != null){
				String tableRows ="";
				String style;
				VideosData.Data video;
				RequestContext requestContext = null;
				for (int row = 0; row <videos.size(); ++row) {
					if(row%2==0)
						style= "row2";
					else
						style = "row1";
					video = (VideosData.Data) videos.get(row);
					requestContext = new RequestContext();
					requestContext.getArgs().put("action", "edit");
					requestContext.getArgs().put("id", video.getId());
					requestContext.setForm(this.formTemplate);
					links.add(this.createHyperlink("<a href='#dashboard/video/" + video.getId() + "/'>" + 
							video.getId() + "</a>",
							"dashboard/video/" + video.getId() + "/",
							new Videos(requestContext)));
					tableRows += "<tr class='" +style+ "'>" +
								  "<td><input type='checkbox' class='action-select' value='"+ video.getId() + "' name='_selected_action' /></td>" +
								  "<th id = 'row" + row + "'></th>"+ 
									"<td>"+ video.getTitle()+"</td>" +
									"<td>"+ video.getVillage().getVillageName() + "</td>"+
									"<td>"+ video.getVideoProductionStartDate() + "</td>" +
									"<td>"+ video.getVideoProductionEndDate() + "</td>" +
								"</tr>";
				}
				videosListFormHtml = videosListFormHtml + tableRows + "</tbody></table>";
			}
		}
		return links;
	}
	//Loading javascript for displaying calendar in Google chrome browser
	public static native void displayCalendar() /*-{
		$wnd.DateTimeShortcuts.init();		
	}-*/;
	final private String addDataToElementID[] = {"id_language", "id_village", "id_facilitator", "id_cameraoperator", "id_farmers_shown", "id_reviewer", "id_supplementary_video_produced"};
	
	private String videosListFormHtml = "<div class = 'toolbar'><label for='searchbar'>" +
									"<img alt='Search' src='/media/img/admin/icon_searchbox.png'></label>" +
									"<input type='text' id='searchbar' value='' name='q' size='40'>" +
									"<input id='search' type='button' value='Search'>" +
								"</div>"+
								"<div class='actions'>" +
    							"<label>Action: <select name='action'>" +
    								"<option value='' selected='selected'>---------</option>" +
    								"<option value='delete_selected'>Delete selected videos</option>" +
    								"</select>" +
    							"</label>" +
    							"<button type='submit' class='button' title='Run the selected action' name='index' value='0'>Go</button>" +
    						"</div>" +    
    						"<table cellspacing='0'>" +
    							"<thead>" +
    								"<tr>" +
    									"<th>" +
    										"<input type='checkbox' id='action-toggle' />" +
    									"</th>" +
    									"<th class='sorted descending'>" +
    										"<a href='?ot=asc&amp;o=1'>" +
    											"ID" +
    										"</a>" +
    									"</th>" +
    									"<th>" +
    										"<a href='?ot=asc&amp;o=2'>" +
    											"Title" +
    										"</a>" +
    									"</th>" +
    									"<th>" +
    										"<a href='?ot=asc&amp;o=3'>" +
    											"Village" +
    										"</a>" +
    									"</th>" +
    									"<th>" +
    										"<a href='?ot=asc&amp;o=4'>" +
    											"Video production start date" +
    										"</a>" +
    									"</th>" +
    									"<th>" +
    										"<a href='?ot=asc&amp;o=5'>" +
    											"Video production end date" +
    										"</a>" +
    									"</th>" +
    								"</tr>" +
    							"</thead>" +
    							"<tbody>" ;
	
	final private String videosListHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
								"<div id='content' class='flex'>" +
									"<h1>Select Video to change</h1>" +
									"<div id='content-main'>" +
										"<ul class='object-tools'>" +
											"<li id='add-link'>" +                // Insert add link here
											"</li>" +
										"</ul>" +
										"<div class='module' id='changelist'>" +
											"<form action='' method='post'>" +
												"<div id='listing-form-body'>" +  // Insert form data here
												"</div>" +
											"</form>" +
										"</div>" +
									"</div>" +
								"</div>";
	
	final private String videosAddHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
    							"<div id='content' class='colM'>" +
    								"<h1>Add video</h1>" +
    								"<div id='content-main'>" +
    									//"<form enctype='multipart/form-data' action='' method='post' id='video_form'>" +
    										//"<div>" +
    											"<fieldset class='module aligned '>" +
    												"<div class='form-row title  '>" +
    													"<div>" +
    														"<label for='id_title' class='required'>Title:</label><input id='id_title' type='text' class='vTextField' name='title' maxlength='200' />" +
    													"</div>" +
    												"</div>" +
    												"<div class='form-row video_type  '>" +
    													"<div>" +
    														"<label for='id_video_type' class='required'>Video type:</label><select name='video_type' id='id_video_type'>" +
    															"<option value='' selected='selected'>---------</option>" +
    															"<option value='1'>Demonstration</option>"+
    															"<option value='2'>Success story/ Testimonial</option>"+
    															"<option value='3'>Activity Introduction</option>"+
    															"<option value='4'>Discussion</option>"+
    															"<option value='5'>General Awareness</option>"+
    														"</select>" +
    													"</div>" +
    												"</div>" +
    												"<div class='form-row video_production_start_date  '>" +
    													"<div>" +
    														"<label for='id_video_production_start_date' class='required'>Video production start date:</label><input id='id_video_production_start_date' type='text' class='vDateField' name='video_production_start_date' size='10' />" +
    													"</div>" +
    												"</div>" +
    												"<div class='form-row video_production_end_date  '>" +
    													"<div>" +
    														"<label for='id_video_production_end_date' class='required'>Video production end date:</label><input id='id_video_production_end_date' type='text' class='vDateField' name='video_production_end_date' size='10' />" +
    													"</div>" +
    												"</div>" +
    												"<div class='form-row language  '>" +
    													"<div>" +
    														"<label for='id_language' class='required'>Language:</label><select name='language' id='id_language'>" +
    															"<option value='' selected='selected'>---------</option>" +
    														"</select>" +
    													"</div>" +
    												"</div>" +
    												"<div class='form-row storybase  '>" +
    													"<div>" +
    														"<label for='id_storybase' class='required'>Storybase:</label><select name='storybase' id='id_storybase'>" +
    															"<option value='' selected='selected'>---------</option>" +
    															"<option value='1'>Agricultural</option>"+
    															"<option value='2'>Institutional</option>"+

    														"</select>" +
    													"</div>" +
    												"</div>" +
    												"<div class='form-row summary  '>" +
    													"<div>" +
    														"<label for='id_summary'>Summary:</label><textarea id='id_summary' rows='10' cols='40' name='summary' class='vLargeTextField'></textarea>" +
    													"</div>" +
    												"</div>" +
    											"</fieldset>" +
    											"<fieldset class='module aligned '>" +
    												"<h2>Upload Files</h2>" +
    												"<div class='form-row storyboard_filename  '>" +
    													"<div>" +
    														"<label for='id_storyboard_filename'>Storyboard filename:</label><input type='file' name='storyboard_filename' id='id_storyboard_filename' />" +
    													"</div>" +
    												"</div>" +
    												"<div class='form-row raw_filename  '>" +
    													"<div>" +
    														"<label for='id_raw_filename'>Raw filename:</label><input type='file' name='raw_filename' id='id_raw_filename' />" +
    													"</div>" +
    												"</div>" +
    												"<div class='form-row movie_maker_project_filename  '>" +
    													"<div>" +
    														"<label for='id_movie_maker_project_filename'>Movie maker project filename:</label><input type='file' name='movie_maker_project_filename' id='id_movie_maker_project_filename' />" +
    													"</div>" +
    												"</div>" +
    												"<div class='form-row final_edited_filename  '>" +
    													"<div>" +
    														"<label for='id_final_edited_filename'>Final edited filename:</label><input type='file' name='final_edited_filename' id='id_final_edited_filename' />" +
    													"</div>" +
    												"</div>" +
    											"</fieldset>" +
    											"<fieldset class='module aligned '>" +
    												"<div class='form-row village  '>" +
    													"<div>" +
    														"<label for='id_village' class='required'>Village:</label>" +
    														"<select name='village' id='id_village'>"+
    														"<option value='' selected='selected'>---------</option>"+
    														"</select>" + 
    														/*Uncomment the below lines for enable auto complete feature in the village field*/
    														/*"<input type='hidden' name='village' id='id_village' />" +
    														"<style type='text/css' media='screen'>" +
													            "#lookup_village {" +
													                "padding-right:16px;" +
													                "background: url(" +
													                    "/media/img/admin/selector-search.gif" +
													                ") no-repeat right;" +
													            "}" +
													            "#del_village {" +
													                "display: none;" +
													            "}" +
													        "</style>" +
													        "<input type='text' id='lookup_village' value='' />" +
													        "<a href='#' id='del_village'>" +
													        	"<img src='/media/img/admin/icon_deletelink.gif' />" +
													        "</a>" +
													        "<script type='text/javascript' src='/media/js/jquery.autocomplete.js'></script>"+
													        "<script type='text/javascript'>" +
														        "if ($('#lookup_village').val()) {" +
														            "$('#del_village').show()" +
														        "}" +
														        "$('#lookup_village').autocomplete('/dashboard/search/', {" +
														            "extraParams: {" +
														                "search_fields: 'village_name'," +
														                "app_label: 'dashboard'," +
														                "model_name: 'village'," +
														            "}," +
														        "}).result(function(event, data, formatted) {" +
														            "if (data) {" +
														                "$('#id_village').val(data[1]);" +
														                "$('#del_village').show();" +
														            "}" +
														        "});" +
														        "$('#del_village').click(function(ele, event) {" +
														            "$('#id_village').val('');" +
														            "$('#del_village').hide();" +
														            "$('#lookup_village').val('');" +
														        "});" +
													        "</script>" +*/
													    "</div>" +
												    "</div>" +
												    "<div class='form-row facilitator  '>" +
												    	"<div>" +
												    		"<label for='id_facilitator' class='required'>Facilitator:</label><select name='facilitator' id='id_facilitator'>" +
												    			"<option value='' selected='selected'>---------</option>" +
												    		"</select>" +
												    	"</div>" +
												    "</div>" +
												    "<div class='form-row cameraoperator  '>" +
												    	"<div>" +
												    		"<label for='id_cameraoperator' class='required'>Camera Operator:</label><select name='cameraoperator' id='id_cameraoperator'>" +
												    			"<option value='' selected='selected'>---------</option>" +
												    		"</select>" +
												    	"</div>" +
												    "</div>" +
											        "<div class='form-row farmers_shown  '>" +
												    	"<div>" +
												    		"<label for='id_farmers_shown' class='required'>Farmers shown:</label><select multiple='multiple' name='farmers_shown' id='id_farmers_shown'>" +
												    		"</select>" +
												    		//"<script type='text/javascript' src='/media/js/SelectFilter2.js'></script>"+
												    		//"<script type='text/javascript'>SelectFilter.init('id_farmers_shown', 'farmers shown', 0, '/media/');</script>"+
												    		"<p class='help'> Hold down 'Control', or 'Command' on a Mac, to select more than one.</p>" +
												    	"</div>" +
												    "</div>" +
												    "<div class='form-row actors  '>" +
												    	"<div>" +
												    		"<label for='id_actors' class='required'>Actors:</label><select name='actors' id='id_actors'>" +
												    			"<option value='' selected='selected'>---------</option>" +
												    			"<option value='I'>Individual</option>"+
												    			"<option value='F'>Family</option>"+
												    			"<option value='G'>Group</option>"+
												    		"</select>" +
												    	"</div>" +
												    "</div>" +
												"</fieldset>" +
												"<fieldset class='module aligned '>" +
													"<h2>Video Quality</h2>" +
													"<div class='form-row picture_quality  '>" +
														"<div>" +
															"<label for='id_picture_quality'>Picture quality:</label><input id='id_picture_quality' type='text' class='vTextField' name='picture_quality' maxlength='200' />" +
														"</div>" +
													"</div>" +
													"<div class='form-row audio_quality  '>" +
														"<div>" +
															"<label for='id_audio_quality'>Audio quality:</label><input id='id_audio_quality' type='text' class='vTextField' name='audio_quality' maxlength='200' />" +
														"</div>" +
													"</div>" +
													"<div class='form-row editing_quality  '>" +
														"<div>" +
															"<label for='id_editing_quality'>Editing quality:</label><input id='id_editing_quality' type='text' class='vTextField' name='editing_quality' maxlength='200' />" +
														"</div>" +
													"</div>" +
													"<div class='form-row edit_start_date  '>" +
														"<div>" +
															"<label for='id_edit_start_date'>Edit start date:</label><input id='id_edit_start_date' type='text' class='vDateField' name='edit_start_date' size='10' />" +
														"</div>" +
													"</div>" +
													"<div class='form-row edit_finish_date  '>" +
														"<div>" +
															"<label for='id_edit_finish_date'>Edit finish date:</label><input id='id_edit_finish_date' type='text' class='vDateField' name='edit_finish_date' size='10' />" +
														"</div>" +
													"</div>" +
													"<div class='form-row thematic_quality  '>" +
														"<div>" +
															"<label for='id_thematic_quality'>Thematic quality:</label><input id='id_thematic_quality' type='text' class='vTextField' name='thematic_quality' maxlength='200' />" +
														"</div>" +
													"</div>" +
												"</fieldset>" +
												"<fieldset class='module aligned '>" +
													"<h2>Review</h2>" +
													"<div class='form-row reviewer  '>" +
														"<div>" +
															"<label for='id_reviewer'>Reviewer:</label><select name='reviewer' id='id_reviewer'>" +
																"<option value='' selected='selected'>---------</option>" +
															"</select>" +
														"</div>" +
													"</div>" +
													"<div class='form-row approval_date  '>" +
														"<div>" +
															"<label for='id_approval_date'>Approval date:</label><input id='id_approval_date' type='text' class='vDateField' name='approval_date' size='10' />" +
														"</div>" +
													"</div>" +
													"<div class='form-row supplementary_video_produced  '>" +
														"<div>" +
															"<label for='id_supplementary_video_produced'>Supplementary video produced:</label><select name='supplementary_video_produced' id='id_supplementary_video_produced'>" +
																"<option value='' selected='selected'>---------</option>" +
															"</select>" +
														"</div>" +
													"</div>" +
													"<div class='form-row video_suitable_for  '>" +
														"<div>" +
															"<label for='id_video_suitable_for' class='required'>Video suitable for:</label><select name='video_suitable_for' id='id_video_suitable_for'>" +
																"<option value='' selected='selected'>---------</option>" +
																"<option value='1'>Dissemination</option>"+
																"<option value='2'>Video Production Training</option>"+
																"<option value='3'>Dissemination Training</option>"+
																"<option value='4'>Nothing</option>"+
																"<option value='5'>Pending for Approval</option>"+
															"</select>" +
														"</div>" +
													"</div>" +
													"<div class='form-row remarks  '>" +
														"<div>" +
															"<label for='id_remarks'>Remarks:</label><textarea id='id_remarks' rows='10' cols='40' name='remarks' class='vLargeTextField'></textarea>" +
														"</div>" +
													"</div>" +
													"<div class='form-row youtubeid'>" +
														"<div>" +
															"<label for='id_youtubeid'>Youtubeid:</label>" +
															"<input type='text' maxlength='20' name='youtubeid' class='vTextField' id='id_youtubeid'>" +
														"</div>" +
													"</div>"+
												"</fieldset>" +
												"<div class='submit-row' >" +
													"<input id='save' type='button' value='Save' class='default' name='_save' />" +
												"</div>" +
												"<script type='text/javascript'>document.getElementById('id_title').focus();</script>" +
												"<script type='text/javascript'>" +
												"</script>" +
											//"</div>" +
										//"</form>" +
									"</div>" +
									"<br class='clear' />" +
								"</div>"; 
}

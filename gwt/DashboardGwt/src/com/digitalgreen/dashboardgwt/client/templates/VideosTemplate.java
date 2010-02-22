package com.digitalgreen.dashboardgwt.client.templates;

import java.util.HashMap;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.servlets.Videos;

public class VideosTemplate extends BaseTemplate {
	public VideosTemplate(RequestContext requestContext) {
		super(requestContext);
	}
	
	@Override
	public void fill() {
		String templateType = "Video";
		String templatePlainType = "dashboard/video/add/";
		RequestContext requestContext = new RequestContext();
		HashMap args = new HashMap();
		args.put("action", "add");
		requestContext.setArgs(args);
		Videos addVideosServlet = new Videos(requestContext);
		Videos video = new Videos(BaseTemplate.setupDgPostContext(this.getDgFormId()));
		// Draw the content of the template depending on the request type (GET/POST)
		super.fillDGTemplate(templateType, videosListHtml, videosAddHtml);
		// Add it to the rootpanel
		super.fill();
		// Now add hyperlinks
		super.fillDGLinkControls(templatePlainType, templateType, videosListFormHtml, addVideosServlet);
		// Now add any submit control buttons
		super.fillDGSubmitControls(video);
	}
	
	final static private String videosListFormHtml = "<div class='actions'>" +
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
    							"<tbody>" +
    								"<div id='data-rows'" +       // Insert data rows here
    								"</div>" +
    							"</tbody>" +
    						"</table>";
;
	
	final static private String videosListHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
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
	
	final static private String videosAddHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
    							"<div id='content' class='colM'>" +
    								"<h1>Add video</h1>" +
    								"<div id='content-main'>" +
    									"<form enctype='multipart/form-data' action='' method='post' id='video_form'>" +
    										"<div>" +
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
    														"</select><a href='/admin/dashboard/language/add/' class='add-another' id='add_id_language' onclick='return showAddAnotherPopup(this);'> <img src='/media/img/admin/icon_addlink.gif' width='10' height='10' alt='Add Another'/></a>" +
    													"</div>" +
    												"</div>" +
    												"<div class='form-row storybase  '>" +
    													"<div>" +
    														"<label for='id_storybase' class='required'>Storybase:</label><select name='storybase' id='id_storybase'>" +
    															"<option value='' selected='selected'>---------</option>" +
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
    														"<label for='id_village' class='required'>Village:</label><input type='hidden' name='village' id='id_village' />" +
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
													        "<script type='text/javascript'>" +
														        "if ($('#lookup_village').val()) {" +
														            "$('#del_village').show()" +
														        "}" +
														        "$('#lookup_village').autocomplete('../search/', {" +
														            "extraParams: {" +
														                "search_fields: 'village_name'," +
														                "app_label: 'dashboard'," +
														                "model_name: 'village'," +
														            "}," +
														        "}).result(function(event, data, formatted) {" +
														            "if (data) {" +
														                "$('#id_village').val(data[1]);" +
														                "$('#del_village').show();" +
															    "filter();" +
														            "}" +
														        "});" +
														        "$('#del_village').click(function(ele, event) {" +
														            "$('#id_village').val('');" +
														            "$('#del_village').hide();" +
														            "$('#lookup_village').val('');" +
														        "});" +
													        "</script>" +
													        "<a href='/admin/dashboard/village/add/' class='add-another' id='add_id_village' onclick='return showAddAnotherPopup(this);'> <img src='/media/img/admin/icon_addlink.gif' width='10' height='10' alt='Add Another'/></a>" +
													    "</div>" +
												    "</div>" +
												    "<div class='form-row facilitator  '>" +
												    	"<div>" +
												    		"<label for='id_facilitator' class='required'>Facilitator:</label><select disabled='true' name='facilitator' id='id_facilitator'>" +
												    			"<option value='' selected='selected'>---------</option>" +
												    		"</select>" +
												    	"</div>" +
												    "</div>" +
												    "<div class='form-row cameraoperator  '>" +
												    	"<div>" +
												    		"<label for='id_cameraoperator' class='required'>Cameraoperator:</label><select disabled='true' name='cameraoperator' id='id_cameraoperator'>" +
												    			"<option value='' selected='selected'>---------</option>" +
												    		"</select>" +
												    	"</div>" +
												    "</div>" +
												    "<div class='form-row related_agricultural_practices  '>" +
												    	"<div>" +
												    		"<label for='id_related_agricultural_practices' class='required'>Related agricultural practices:</label><select multiple='multiple' name='related_agricultural_practices' id='id_related_agricultural_practices'>" +
												    		"</select><script type='text/javascript'>addEvent(window, 'load', function(e) {SelectFilter.init('id_related_agricultural_practices', 'related agricultural practices', 0, '/media/'); });</script>" +
												    		"<a href='/admin/dashboard/practices/add/' class='add-another' id='add_id_related_agricultural_practices' onclick='return showAddAnotherPopup(this);'> <img src='/media/img/admin/icon_addlink.gif' width='10' height='10' alt='Add Another'/></a>" +
												    		"<p class='help'> Hold down 'Control', or 'Command' on a Mac, to select more than one.</p>" +
												    	"</div>" +
												    "</div>" +
												    "<div class='form-row farmers_shown  '>" +
												    	"<div>" +
												    		"<label for='id_farmers_shown' class='required'>Farmers shown:</label><select multiple='multiple' name='farmers_shown' id='id_farmers_shown'>" +
												    		"</select><script type='text/javascript'>addEvent(window, 'load', function(e) {SelectFilter.init('id_farmers_shown', 'farmers shown', 0, '/media/'); });</script>" +
												    		"<a href='/admin/dashboard/person/add/' class='add-another' id='add_id_farmers_shown' onclick='return showAddAnotherPopup(this);'> <img src='/media/img/admin/icon_addlink.gif' width='10' height='10' alt='Add Another'/></a>" +
												    		"<p class='help'> Hold down 'Control', or 'Command' on a Mac, to select more than one.</p>" +
												    	"</div>" +
												    "</div>" +
												    "<div class='form-row actors  '>" +
												    	"<div>" +
												    		"<label for='id_actors' class='required'>Actors:</label><select name='actors' id='id_actors'>" +
												    			"<option value='' selected='selected'>---------</option>" +
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
															"</select><a href='/admin/dashboard/video/add/' class='add-another' id='add_id_supplementary_video_produced' onclick='return showAddAnotherPopup(this);'> <img src='/media/img/admin/icon_addlink.gif' width='10' height='10' alt='Add Another'/></a>" +
														"</div>" +
													"</div>" +
													"<div class='form-row video_suitable_for  '>" +
														"<div>" +
															"<label for='id_video_suitable_for' class='required'>Video suitable for:</label><select name='video_suitable_for' id='id_video_suitable_for'>" +
																"<option value='' selected='selected'>---------</option>" +
															"</select>" +
														"</div>" +
													"</div>" +
													"<div class='form-row remarks  '>" +
														"<div>" +
															"<label for='id_remarks'>Remarks:</label><textarea id='id_remarks' rows='10' cols='40' name='remarks' class='vLargeTextField'></textarea>" +
														"</div>" +
													"</div>" +
												"</fieldset>" +
												"<div class='submit-row' >" +
													"<input type='submit' value='Save' class='default' name='_save' />" +
												"</div>" +
												"<script type='text/javascript'>document.getElementById('id_title').focus();</script>" +
												"<script type='text/javascript'>" +
												"</script>" +
											"</div>" +
										"</form>" +
									"</div>" +
									"<br class='clear' />" +
								"</div>";

} 
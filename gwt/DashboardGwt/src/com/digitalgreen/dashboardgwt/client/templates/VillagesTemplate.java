package com.digitalgreen.dashboardgwt.client.templates;

import java.util.HashMap;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.servlets.Villages;

public class VillagesTemplate extends BaseTemplate {
	public VillagesTemplate(RequestContext requestContext) {
		super(requestContext);
	}
	
	@Override
	public void fill() {
		String templateType = "Village";
		String templatePlainType = "dashboard/village/add/";
		RequestContext requestContext = new RequestContext();
		HashMap args = new HashMap();
		args.put("action", "add");
		requestContext.setArgs(args);
		Villages addVillagesServlet = new Villages(requestContext);
		Villages region = new Villages(new RequestContext(RequestContext.METHOD_POST, 
				getPostForm()));
		// Draw the content of the template depending on the request type (GET/POST)
		super.fillDGTemplate(templateType, villagesListHtml, villagesAddHtml);
		// Add it to the rootpanel
		super.fill();
		// Now add hyperlinks
		super.fillDGLinkControls(templatePlainType, templateType, villagesListFormHtml, addVillagesServlet);
		// Now add any submit control buttons
		super.fillDGSubmitControls(region);
	}
	
	final static private String villagesListFormHtml = "<div class='actions'>" +
								"<label>Action: <select name='action'>" +
									"<option value='' selected='selected'>---------</option>" +
									"<option value='delete_selected'>Delete selected villages</option>" +
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
										"<th>" +
											"<a href='?ot=asc&amp;o=1'>" +
												"Village name" +
											"</a>" +
										"</th>" +
										"<th>" +
											"<a href='?ot=asc&amp;o=2'>" +
												"Block" +
											"</a>" +
										"</th>" +
									"</tr>" +
								"</thead>" +
								"<tbody>" +
									"<div id='data-rows'" +       // Insert data rows here
									"</div>" +
								"</tbody>" +
							"</table>";
	
	final static private String villagesListHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
								"<div id='content' class='flex'>" +
									"<h1>Select screening to change</h1>" +
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
	
	final static private String villagesAddHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
								"<div id='content' class='colM'>" +
									"<h1>Add village</h1>" +
										"<div id='content-main'>" +
											"<form enctype='multipart/form-data' action='' method='post' id='village_form'>" +
												"<div>" +
													"<fieldset class='module aligned '>" +
														"<div class='form-row village_name  '>" +
															"<div>" +
																"<label for='id_village_name' class='required'>Village name:</label><input id='id_village_name' type='text' class='vTextField' name='village_name' maxlength='100' />" +
															"</div>" +
														"</div>" +
														"<div class='form-row block  '>" +
															"<div>" +
																"<label for='id_block' class='required'>Block:</label><select name='block' id='id_block'>" +
																	"<option value='' selected='selected'>---------</option>" +
																"</select><a href='/admin/dashboard/block/add/' class='add-another' id='add_id_block' onclick='return showAddAnotherPopup(this);'> <img src='/media/img/admin/icon_addlink.gif' width='10' height='10' alt='Add Another'/></a>" +
															"</div>" +
														"</div>" +
														"<div class='form-row no_of_households  '>" +
															"<div>" +
																"<label for='id_no_of_households'>No of households:</label><input id='id_no_of_households' type='text' class='vIntegerField' name='no_of_households' />" +
															"</div>" +
														"</div>" +
														"<div class='form-row population  '>" +
															"<div>" +
																"<label for='id_population'>Population:</label><input id='id_population' type='text' class='vIntegerField' name='population' />" +
															"</div>" +
														"</div>" +
														"<div class='form-row road_connectivity  '>" +
															"<div>" +
																"<label for='id_road_connectivity'>Road connectivity:</label><input id='id_road_connectivity' type='text' class='vTextField' name='road_connectivity' maxlength='100' />" +
															"</div>" +
														"</div>" +
														"<div class='form-row control  '>" +
															"<div>" +
																"<label for='id_control'>Control:</label><select name='control' id='id_control'>" +
																	"<option value='1' selected='selected'>Unknown</option>" +
																	"<option value='2'>Yes</option>" +
																	"<option value='3'>No</option>" +
																"</select>" +
															"</div>" +
														"</div>" +
														"<div class='form-row start_date  '>" +
															"<div>" +
																"<label for='id_start_date'>Start date:</label><input id='id_start_date' type='text' class='vDateField' name='start_date' size='10' />" +
															"</div>" +
														"</div>" +
													"</fieldset>" +
													"<div class='inline-group'>" +
														"<div class='tabular inline-related '>" +
															"<input type='hidden' name='persongroups_set-TOTAL_FORMS' value='5' id='id_persongroups_set-TOTAL_FORMS' /><input type='hidden' name='persongroups_set-INITIAL_FORMS' value='0' id='id_persongroups_set-INITIAL_FORMS' />" +
																"<fieldset class='module'>" +
																	"<h2>Person groups</h2>" +
																	"<table>" +
																		"<thead>" +
																			"<tr>" +
																				"<th colspan='2'>Group name</th>" +
																				"<th >Days</th>" +
																				"<th >Timings</th>" +
																				"<th>Delete?</th>" +
																			"</tr>" +
																		"</thead>" +
																		"<tr class='row1 '>" +
																			"<td class='original'>" +
																				"<input type='hidden' name='persongroups_set-0-id' id='id_persongroups_set-0-id' />" +
																				"<input type='hidden' name='persongroups_set-0-village' id='id_persongroups_set-0-village' />" +
																			"</td>" +
																			"<td class='group_name'>" +
																				"<input id='id_persongroups_set-0-group_name' type='text' class='vTextField' name='persongroups_set-0-group_name' maxlength='100' />" +
																			"</td>" +
																			"<td class='days'>" +
																				"<select name='persongroups_set-0-days' id='id_persongroups_set-0-days'>" +
																					"<option value='' selected='selected'>---------</option>" +
																					"<option value='Monday'>Monday</option>" +
																					"<option value='Tuesday'>Tuesday</option>" +
																					"<option value='Wednesday'>Wednesday</option>" +
																					"<option value='Thursday'>Thursday</option>" +
																					"<option value='Friday'>Friday</option>" +
																					"<option value='Saturday'>Saturday</option>" +
																					"<option value='Sunday'>Sunday</option>" +
																				"</select>" +
																			"</td>" +
																			"<td class='timings'>" +
																				"<input id='id_persongroups_set-0-timings' type='text' class='vTimeField' name='persongroups_set-0-timings' size='8' />" +
																			"</td>" +
																			"<td class='delete'></td>" +
																		"</tr>" +
																		"<tr class='row2 '>" +
																			"<td class='original'>" +
																				"<input type='hidden' name='persongroups_set-1-id' id='id_persongroups_set-1-id' />" +
																				"<input type='hidden' name='persongroups_set-1-village' id='id_persongroups_set-1-village' />" +
																			"</td>" +
																			"<td class='group_name'>" +
																				"<input id='id_persongroups_set-1-group_name' type='text' class='vTextField' name='persongroups_set-1-group_name' maxlength='100' />" +
																			"</td>" +
																			"<td class='days'>" +
																				"<select name='persongroups_set-1-days' id='id_persongroups_set-1-days'>" +
																					"<option value='' selected='selected'>---------</option>" +
																					"<option value='Monday'>Monday</option>" +
																					"<option value='Tuesday'>Tuesday</option>" +
																					"<option value='Wednesday'>Wednesday</option>" +
																					"<option value='Thursday'>Thursday</option>" +
																					"<option value='Friday'>Friday</option>" +
																					"<option value='Saturday'>Saturday</option>" +
																					"<option value='Sunday'>Sunday</option>" +
																				"</select>" +
																			"</td>" +
																			"<td class='timings'>" +
																				"<input id='id_persongroups_set-1-timings' type='text' class='vTimeField' name='persongroups_set-1-timings' size='8' />" +
																			"</td>" +
																			"<td class='delete'></td>" +
																		"</tr>" +
																		"<tr class='row1 '>" +
																			"<td class='original'>" +
																				"<input type='hidden' name='persongroups_set-2-id' id='id_persongroups_set-2-id' />" +
																				"<input type='hidden' name='persongroups_set-2-village' id='id_persongroups_set-2-village' />" +
																			"</td>" +
																			"<td class='group_name'>" +
																				"<input id='id_persongroups_set-2-group_name' type='text' class='vTextField' name='persongroups_set-2-group_name' maxlength='100' />" +
																			"</td>" +
																			"<td class='days'>" +
																				"<select name='persongroups_set-2-days' id='id_persongroups_set-2-days'>" +
																					"<option value='' selected='selected'>---------</option>" +
																					"<option value='Monday'>Monday</option>" +
																					"<option value='Tuesday'>Tuesday</option>" +
																					"<option value='Wednesday'>Wednesday</option>" +
																					"<option value='Thursday'>Thursday</option>" +
																					"<option value='Friday'>Friday</option>" +
																					"<option value='Saturday'>Saturday</option>" +
																					"<option value='Sunday'>Sunday</option>" +
																				"</select>" +
																			"</td>" +
																			"<td class='timings'>" +
																				"<input id='id_persongroups_set-2-timings' type='text' class='vTimeField' name='persongroups_set-2-timings' size='8' />" +
																			"</td>" +
																			"<td class='delete'></td>" +
																		"</tr>" +
																		"<tr class='row2 '>" +
																			"<td class='original'>" +
																				"<input type='hidden' name='persongroups_set-3-id' id='id_persongroups_set-3-id' />" +
																				"<input type='hidden' name='persongroups_set-3-village' id='id_persongroups_set-3-village' />" +
																			"</td>" +
																			"<td class='group_name'>" +
																				"<input id='id_persongroups_set-3-group_name' type='text' class='vTextField' name='persongroups_set-3-group_name' maxlength='100' />" +
																			"</td>" +
																			"<td class='days'>" +
																				"<select name='persongroups_set-3-days' id='id_persongroups_set-3-days'>" +
																					"<option value='' selected='selected'>---------</option>" +
																					"<option value='Monday'>Monday</option>" +
																					"<option value='Tuesday'>Tuesday</option>" +
																					"<option value='Wednesday'>Wednesday</option>" +
																					"<option value='Thursday'>Thursday</option>" +
																					"<option value='Friday'>Friday</option>" +
																					"<option value='Saturday'>Saturday</option>" +
																					"<option value='Sunday'>Sunday</option>" +
																				"</select>" +
																			"</td>" +
																			"<td class='timings'>" +
																				"<input id='id_persongroups_set-3-timings' type='text' class='vTimeField' name='persongroups_set-3-timings' size='8' />" +
																			"</td>" +
																			"<td class='delete'></td>" +
																		"</tr>" +
																		"<tr class='row1 '>" +
																			"<td class='original'>" +
																				"<input type='hidden' name='persongroups_set-4-id' id='id_persongroups_set-4-id' />" +
																				"<input type='hidden' name='persongroups_set-4-village' id='id_persongroups_set-4-village' />" +
																			"</td>" +
																			"<td class='group_name'>" +
																				"<input id='id_persongroups_set-4-group_name' type='text' class='vTextField' name='persongroups_set-4-group_name' maxlength='100' />" +
																			"</td>" +
																			"<td class='days'>" +
																				"<select name='persongroups_set-4-days' id='id_persongroups_set-4-days'>" +
																					"<option value='' selected='selected'>---------</option>" +
																					"<option value='Monday'>Monday</option>" +
																					"<option value='Tuesday'>Tuesday</option>" +
																					"<option value='Wednesday'>Wednesday</option>" +
																					"<option value='Thursday'>Thursday</option>" +
																					"<option value='Friday'>Friday</option>" +
																					"<option value='Saturday'>Saturday</option>" +
																					"<option value='Sunday'>Sunday</option>" +
																				"</select>" +
																			"</td>" +
																			"<td class='timings'>" +
																				"<input id='id_persongroups_set-4-timings' type='text' class='vTimeField' name='persongroups_set-4-timings' size='8' />" +
																			"</td>" +
																			"<td class='delete'></td>" +
																		"</tr>" +
																	"</table>" +
																"</fieldset>" +
															"</div>" +
														"</div>" +
														"<div class='inline-group'>" +
															"<div class='tabular inline-related last-related'>" +
																"<input type='hidden' name='home_village-TOTAL_FORMS' value='5' id='id_home_village-TOTAL_FORMS' /><input type='hidden' name='home_village-INITIAL_FORMS' value='0' id='id_home_village-INITIAL_FORMS' />" +
																"<fieldset class='module'>" +
																	"<h2>Animators</h2>" +
																	"<table>" +
																		"<thead>" +
																			"<tr>" +
																				"<th colspan='2'>Name</th>" +
																				"<th >Age</th>" +
																				"<th >Gender</th>" +
																				"<th >Csp flag</th>" +
																				"<th >Camera operator flag</th>" +
																				"<th >Facilitator flag</th>" +
																				"<th >Phone no</th>" +
																				"<th >Address</th>" +
																				"<th >Partner</th>" +
																				"<th>Delete?</th>" +
																			"</tr>" +
																		"</thead>" +
																		"<tr class='row1 '>" +
																			"<td class='original'>" +
																				"<input type='hidden' name='home_village-0-id' id='id_home_village-0-id' />" +
																				"<input type='hidden' name='home_village-0-home_village' id='id_home_village-0-home_village' />" +
																			"</td>" +
																			"<td class='name'>" +
																				"<input id='id_home_village-0-name' type='text' class='vTextField' name='home_village-0-name' maxlength='100' />" +
																			"</td>" +
																			"<td class='age'>" +
																				"<input id='id_home_village-0-age' type='text' class='vIntegerField' name='home_village-0-age' />" +
																			"</td>" +
																			"<td class='gender'>" +
																				"<select name='home_village-0-gender' id='id_home_village-0-gender'>" +
																					"<option value='' selected='selected'>---------</option>" +
																					"<option value='M'>Male</option>" +
																					"<option value='F'>Female</option>" +
																				"</select>" +
																			"</td>" +
																			"<td class='csp_flag'>" +
																				"<select name='home_village-0-csp_flag' id='id_home_village-0-csp_flag'>" +
																					"<option value='1' selected='selected'>Unknown</option>" +
																					"<option value='2'>Yes</option>" +
																					"<option value='3'>No</option>" +
																				"</select>" +
																			"</td>" +
																			"<td class='camera_operator_flag'>" +
																				"<select name='home_village-0-camera_operator_flag' id='id_home_village-0-camera_operator_flag'>" +
																					"<option value='1' selected='selected'>Unknown</option>" +
																					"<option value='2'>Yes</option>" +
																					"<option value='3'>No</option>" +
																				"</select>" +
																			"</td>" +
																			"<td class='facilitator_flag'>" +
																				"<select name='home_village-0-facilitator_flag' id='id_home_village-0-facilitator_flag'>" +
																					"<option value='1' selected='selected'>Unknown</option>" +
																					"<option value='2'>Yes</option>" +
																					"<option value='3'>No</option>" +
																				"</select>" +
																			"</td>" +
																			"<td class='phone_no'>" +
																				"<input id='id_home_village-0-phone_no' type='text' class='vTextField' name='home_village-0-phone_no' maxlength='100' />" +
																			"</td>" +
																			"<td class='address'>" +
																				"<input id='id_home_village-0-address' type='text' class='vTextField' name='home_village-0-address' maxlength='500' />" +
																			"</td>" +
																			"<td class='partner'>" +
																				"<select name='home_village-0-partner' id='id_home_village-0-partner'>" +
																					"<option value='' selected='selected'>---------</option>" +
																				"</select><a href='/admin/dashboard/partners/add/' class='add-another' id='add_id_home_village-0-partner' onclick='return showAddAnotherPopup(this);'> <img src='/media/img/admin/icon_addlink.gif' width='10' height='10' alt='Add Another'/></a>" +
																			"</td>" +
																			"<td class='delete'></td>" +
																		"</tr>" +
																		"<tr class='row2 '>" +
																			"<td class='original'>" +
																				"<input type='hidden' name='home_village-1-id' id='id_home_village-1-id' />" +
																				"<input type='hidden' name='home_village-1-home_village' id='id_home_village-1-home_village' />" +
																			"</td>" +
																			"<td class='name'>" +
																				"<input id='id_home_village-1-name' type='text' class='vTextField' name='home_village-1-name' maxlength='100' />" +
																			"</td>" +
																			"<td class='age'>" +
																				"<input id='id_home_village-1-age' type='text' class='vIntegerField' name='home_village-1-age' />" +
																			"</td>" +
																			"<td class='gender'>" +
																				"<select name='home_village-1-gender' id='id_home_village-1-gender'>" +
																					"<option value='' selected='selected'>---------</option>" +
																					"<option value='M'>Male</option>" +
																					"<option value='F'>Female</option>" +
																				"</select>" +
																			"</td>" +
																			"<td class='csp_flag'>" +
																				"<select name='home_village-1-csp_flag' id='id_home_village-1-csp_flag'>" +
																					"<option value='1' selected='selected'>Unknown</option>" +
																					"<option value='2'>Yes</option>" +
																					"<option value='3'>No</option>" +
																				"</select>" +
																			"</td>" +
																			"<td class='camera_operator_flag'>" +
																				"<select name='home_village-1-camera_operator_flag' id='id_home_village-1-camera_operator_flag'>" +
																					"<option value='1' selected='selected'>Unknown</option>" +
																					"<option value='2'>Yes</option>" +
																					"<option value='3'>No</option>" +
																				"</select>" +
																			"</td>" +
																			"<td class='facilitator_flag'>" +
																				"<select name='home_village-1-facilitator_flag' id='id_home_village-1-facilitator_flag'>" +
																					"<option value='1' selected='selected'>Unknown</option>" +
																					"<option value='2'>Yes</option>" +
																					"<option value='3'>No</option>" +
																				"</select>" +
																			"</td>" +
																			"<td class='phone_no'>" +
																				"<input id='id_home_village-1-phone_no' type='text' class='vTextField' name='home_village-1-phone_no' maxlength='100' />" +
																			"</td>" +
																			"<td class='address'>" +
																				"<input id='id_home_village-1-address' type='text' class='vTextField' name='home_village-1-address' maxlength='500' />" +
																			"</td>" +
																			"<td class='partner'>" +
																				"<select name='home_village-1-partner' id='id_home_village-1-partner'>" +
																					"<option value='' selected='selected'>---------</option>" +
																				"</select><a href='/admin/dashboard/partners/add/' class='add-another' id='add_id_home_village-1-partner' onclick='return showAddAnotherPopup(this);'> <img src='/media/img/admin/icon_addlink.gif' width='10' height='10' alt='Add Another'/></a>" +
																			"</td>" +
																			"<td class='delete'></td>" +
																		"</tr>" +
																		"<tr class='row1 '>" +
																			"<td class='original'>" +
																				"<input type='hidden' name='home_village-2-id' id='id_home_village-2-id' />" +
																				"<input type='hidden' name='home_village-2-home_village' id='id_home_village-2-home_village' />" +
																			"</td>" +
																		"<td class='name'>" +
																			"<input id='id_home_village-2-name' type='text' class='vTextField' name='home_village-2-name' maxlength='100' />" +
																		"</td>" +
																		"<td class='age'>" +
																			"<input id='id_home_village-2-age' type='text' class='vIntegerField' name='home_village-2-age' />" +
																		"</td>" +
																		"<td class='gender'>" +
																			"<select name='home_village-2-gender' id='id_home_village-2-gender'>" +
																				"<option value='' selected='selected'>---------</option>" +
																				"<option value='M'>Male</option>" +
																				"<option value='F'>Female</option>" +
																			"</select>" +
																		"</td>" +
																		"<td class='csp_flag'>" +
																			"<select name='home_village-2-csp_flag' id='id_home_village-2-csp_flag'>" +
																				"<option value='1' selected='selected'>Unknown</option>" +
																				"<option value='2'>Yes</option>" +
																				"<option value='3'>No</option>" +
																			"</select>" +
																		"</td>" +
																		"<td class='camera_operator_flag'>" +
																			"<select name='home_village-2-camera_operator_flag' id='id_home_village-2-camera_operator_flag'>" +
																				"<option value='1' selected='selected'>Unknown</option>" +
																				"<option value='2'>Yes</option>" +
																				"<option value='3'>No</option>" +
																			"</select>" +
																		"</td>" +
																		"<td class='facilitator_flag'>" +
																			"<select name='home_village-2-facilitator_flag' id='id_home_village-2-facilitator_flag'>" +
																				"<option value='1' selected='selected'>Unknown</option>" +
																				"<option value='2'>Yes</option>" +
																				"<option value='3'>No</option>" +
																			"</select>" +
																		"</td>" +
																		"<td class='phone_no'>" +
																			"<input id='id_home_village-2-phone_no' type='text' class='vTextField' name='home_village-2-phone_no' maxlength='100' />" +
																		"</td>" +
																		"<td class='address'>" +
																			"<input id='id_home_village-2-address' type='text' class='vTextField' name='home_village-2-address' maxlength='500' />" +
																		"</td>" +
																		"<td class='partner'>" +
																			"<select name='home_village-2-partner' id='id_home_village-2-partner'>" +
																				"<option value='' selected='selected'>---------</option>" +
																			"</select><a href='/admin/dashboard/partners/add/' class='add-another' id='add_id_home_village-2-partner' onclick='return showAddAnotherPopup(this);'> <img src='/media/img/admin/icon_addlink.gif' width='10' height='10' alt='Add Another'/></a>" +
																		"</td>" +
																		"<td class='delete'></td>" +
																	"</tr>" +
																	"<tr class='row2 '>" +
																		"<td class='original'>" +
																			"<input type='hidden' name='home_village-3-id' id='id_home_village-3-id' />" +
																			"<input type='hidden' name='home_village-3-home_village' id='id_home_village-3-home_village' />" +
																		"</td>" +
																	"<td class='name'>" +
																		"<input id='id_home_village-3-name' type='text' class='vTextField' name='home_village-3-name' maxlength='100' />" +
																	"</td>" +
																	"<td class='age'>" +
																		"<input id='id_home_village-3-age' type='text' class='vIntegerField' name='home_village-3-age' />" +
																	"</td>" +
																	"<td class='gender'>" +
																		"<select name='home_village-3-gender' id='id_home_village-3-gender'>" +
																			"<option value='' selected='selected'>---------</option>" +
																			"<option value='M'>Male</option>" +
																			"<option value='F'>Female</option>" +
																		"</select>" +
																	"</td>" +
																	"<td class='csp_flag'>" +
																		"<select name='home_village-3-csp_flag' id='id_home_village-3-csp_flag'>" +
																			"<option value='1' selected='selected'>Unknown</option>" +
																			"<option value='2'>Yes</option>" +
																			"<option value='3'>No</option>" +
																		"</select>" +
																	"</td>" +
																	"<td class='camera_operator_flag'>" +
																		"<select name='home_village-3-camera_operator_flag' id='id_home_village-3-camera_operator_flag'>" +
																			"<option value='1' selected='selected'>Unknown</option>" +
																			"<option value='2'>Yes</option>" +
																			"<option value='3'>No</option>" +
																		"</select>" +
																	"</td>" +
																	"<td class='facilitator_flag'>" +
																		"<select name='home_village-3-facilitator_flag' id='id_home_village-3-facilitator_flag'>" +
																			"<option value='1' selected='selected'>Unknown</option>" +
																			"<option value='2'>Yes</option>" +
																			"<option value='3'>No</option>" +
																		"</select>" +
																	"</td>" +
																	"<td class='phone_no'>" +
																		"<input id='id_home_village-3-phone_no' type='text' class='vTextField' name='home_village-3-phone_no' maxlength='100' />" +
																	"</td>" +
																	"<td class='address'>" +
																		"<input id='id_home_village-3-address' type='text' class='vTextField' name='home_village-3-address' maxlength='500' />" +
																	"</td>" +
																	"<td class='partner'>" +
																		"<select name='home_village-3-partner' id='id_home_village-3-partner'>" +
																			"<option value='' selected='selected'>---------</option>" +
																		"</select><a href='/admin/dashboard/partners/add/' class='add-another' id='add_id_home_village-3-partner' onclick='return showAddAnotherPopup(this);'> <img src='/media/img/admin/icon_addlink.gif' width='10' height='10' alt='Add Another'/></a>" +
																	"</td>" +
																	"<td class='delete'></td>" +
																"</tr>" +
																"<tr class='row1 '>" +
																	"<td class='original'>" +
																		"<input type='hidden' name='home_village-4-id' id='id_home_village-4-id' />" +
																		"<input type='hidden' name='home_village-4-home_village' id='id_home_village-4-home_village' />" +
																	"</td>" +
																	"<td class='name'>" +
																		"<input id='id_home_village-4-name' type='text' class='vTextField' name='home_village-4-name' maxlength='100' />" +
																	"</td>" +
																	"<td class='age'>" +
																		"<input id='id_home_village-4-age' type='text' class='vIntegerField' name='home_village-4-age' />" +
																	"</td>" +
																	"<td class='gender'>" +
																		"<select name='home_village-4-gender' id='id_home_village-4-gender'>" +
																			"<option value='' selected='selected'>---------</option>" +
																			"<option value='M'>Male</option>" +
																			"<option value='F'>Female</option>" +
																		"</select>" +
																	"</td>" +
																	"<td class='csp_flag'>" +
																		"<select name='home_village-4-csp_flag' id='id_home_village-4-csp_flag'>" +
																			"<option value='1' selected='selected'>Unknown</option>" +
																			"<option value='2'>Yes</option>" +
																			"<option value='3'>No</option>" +
																		"</select>" +
																	"</td>" +
																	"<td class='camera_operator_flag'>" +
																		"<select name='home_village-4-camera_operator_flag' id='id_home_village-4-camera_operator_flag'>" +
																			"<option value='1' selected='selected'>Unknown</option>" +
																			"<option value='2'>Yes</option>" +
																			"<option value='3'>No</option>" +
																		"</select>" +
																	"</td>" +
																	"<td class='facilitator_flag'>" +
																		"<select name='home_village-4-facilitator_flag' id='id_home_village-4-facilitator_flag'>" +
																			"<option value='1' selected='selected'>Unknown</option>" +
																			"<option value='2'>Yes</option>" +
																			"<option value='3'>No</option>" +
																		"</select>" +
																	"</td>" +
																	"<td class='phone_no'>" +
																		"<input id='id_home_village-4-phone_no' type='text' class='vTextField' name='home_village-4-phone_no' maxlength='100' />" +
																	"</td>" +
																	"<td class='address'>" +
																		"<input id='id_home_village-4-address' type='text' class='vTextField' name='home_village-4-address' maxlength='500' />" +
																	"</td>" +
																	"<td class='partner'>" +
																		"<select name='home_village-4-partner' id='id_home_village-4-partner'>" +
																			"<option value='' selected='selected'>---------</option>" +
																		"</select><a href='/admin/dashboard/partners/add/' class='add-another' id='add_id_home_village-4-partner' onclick='return showAddAnotherPopup(this);'> <img src='/media/img/admin/icon_addlink.gif' width='10' height='10' alt='Add Another'/></a>" +
																	"</td>" +
																	"<td class='delete'></td>" +
																"</tr>" +
															"</table>" +
														"</fieldset>" +
													"</div>" +
												"</div>" +	
												"<div class='submit-row' >" +
													"<input type='submit' value='Save' class='default' name='_save' />" +
												"</div>" +
												"<script type='text/javascript'>document.getElementById('id_village_name').focus();</script>" +
												"<script type='text/javascript'>" +
												"</script>" +
											"</div>" +
										"</form>" +
									"</div>" +
									"<br class='clear' />" +
								"</div>";

}
package com.digitalgreen.dashboardgwt.client.templates;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.AnimatorsData;
import com.digitalgreen.dashboardgwt.client.data.PersonGroupsData;
import com.digitalgreen.dashboardgwt.client.data.RegionsData;
import com.digitalgreen.dashboardgwt.client.data.VillagesData;
import com.digitalgreen.dashboardgwt.client.servlets.Regions;
import com.digitalgreen.dashboardgwt.client.servlets.Villages;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.Hyperlink;

public class VillagesTemplate extends BaseTemplate {
	public VillagesTemplate(RequestContext requestContext) {
		super(requestContext);
		ArrayList personGroupData = new ArrayList();
		personGroupData.add((new PersonGroupsData()).getNewData());
		ArrayList animatorsData = new ArrayList();
		animatorsData.add((new AnimatorsData()).getNewData());
		this.formTemplate = new Form((new VillagesData()).getNewData(), 
				new Object[] {personGroupData, animatorsData});
	}
	
	@Override
	public void fill() {
		String templateType = "Village";
		String templatePlainType = "dashboard/village/add/";
		RequestContext requestContext = new RequestContext();
		HashMap args = new HashMap();
		args.put("action", "add");
		requestContext.setArgs(args);
		requestContext.setForm(this.formTemplate);
		Villages addVillagesServlet = new Villages(requestContext);
		RequestContext saveRequestContext = new RequestContext(RequestContext.METHOD_POST);
		saveRequestContext.setForm(this.formTemplate);
		Villages saveVillage = new Villages(saveRequestContext);
		// Draw the content of the template depending on the request type (GET/POST)
		super.fillDGTemplate(templateType, villagesListHtml, villagesAddHtml, addDataToElementID);
		// Add it to the rootpanel
		super.fill();
		//Now add listings
		List<Hyperlink> links =  this.fillListings();
		// Now add hyperlinks
		super.fillDgListPage(templatePlainType, templateType, villagesListFormHtml, addVillagesServlet, links);
		// Now add any submit control buttons
		super.fillDgFormPage(saveVillage);
	}

	protected List<Hyperlink> fillListings() {
		HashMap queryArgs = this.getRequestContext().getArgs();
		String queryArg = (String)queryArgs.get("action");
		List<Hyperlink> links = new ArrayList<Hyperlink>();
		if(queryArg.equals("list")) {
			// 	Add Listings
			List villages = (List)queryArgs.get("listing");			
			if(villages != null){
				String tableRows ="";
				String style;
				VillagesData.Data village;
				RequestContext requestContext = null;
				for (int row = 0; row < villages.size(); ++row) {
					if(row%2==0)
						style= "row2";
					else
						style = "row1";
					village = (VillagesData.Data)villages.get(row);
					requestContext = new RequestContext();
					requestContext.getArgs().put("action", "edit");
					requestContext.getArgs().put("id", village.getId());
					requestContext.setForm(this.formTemplate);
					links.add(this.createHyperlink("<a href='#dashboard/village/"+ village.getId() +"/'>" +
							village.getVillageName()+"</a>",
							"dashboard/village/"+ village.getId() +"/",
							new Villages(requestContext)));
					tableRows += "<tr class='" +style+ "'>" +
					  "<td><input type='checkbox' class='action-select' value='"+ village.getId() + "' name='_selected_action' /></td>" +
						"<th id = 'row" + row + "'></th>" +
						"<td>"+ village.getBlock().getBlockName() + "</td>" + 
					"</tr>";
				}
				villagesListFormHtml = villagesListFormHtml + tableRows + "</tbody></table>";
			}
		}
		return links;
	}
	
	// A list of Element IDs that need to receive the data before the template is loaded.
	final private String addDataToElementID[] = {"id_block", "id_animator_set-0-partner", "id_animator_set-1-partner", 
			"id_animator_set-2-partner", "id_animator_set-3-partner", "id_animator_set-4-partner"};
	
	private String villagesListFormHtml = "<div class='actions'>" +
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
								"<tbody>";
	
	final private String villagesListHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
								"<div id='content' class='flex'>" +
									"<h1>Select Village to change</h1>" +
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
	
	final private String villagesAddHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
								"<div id='content' class='colM'>" +
									"<h1>Add village</h1>" +
										"<div id='content-main'>" +
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
																"</select>" +
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
															"<input type='hidden' name='persongroups_set-TOTAL_FORMS' value='5' id='id_persongroups_set-TOTAL_FORMS' />" +
															"<input type='hidden' name='persongroups_set-INITIAL_FORMS' value='0' id='id_persongroups_set-INITIAL_FORMS' />" +
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
																"<input type='hidden' name='animator_set-TOTAL_FORMS' value='5' id='id_animator_set-TOTAL_FORMS' />" +
																"<input type='hidden' name='animator_set-INITIAL_FORMS' value='0' id='id_animator_set-INITIAL_FORMS' />" +
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
																				"<input type='hidden' name='animator_set-0-id' id='id_animator_set-0-id' />" +
																				"<input type='hidden' name='animator_set-0-village' id='id_animator_set-0-village' />" +
																			"</td>" +
																			"<td class='name'>" +
																				"<input id='id_animator_set-0-name' type='text' class='vTextField' name='animator_set-0-name' maxlength='100' />" +
																			"</td>" +
																			"<td class='age'>" +
																				"<input id='id_animator_set-0-age' type='text' class='vIntegerField' name='animator_set-0-age' />" +
																			"</td>" +
																			"<td class='gender'>" +
																				"<select name='animator_set-0-gender' id='id_animator_set-0-gender'>" +
																					"<option value='' selected='selected'>---------</option>" +
																					"<option value='M'>Male</option>" +
																					"<option value='F'>Female</option>" +
																				"</select>" +
																			"</td>" +
																			"<td class='csp_flag'>" +
																				"<select name='animator_set-0-csp_flag' id='id_animator_set-0-csp_flag'>" +
																					"<option value='' selected='selected'>---------</option>" +
																					"<option value='1'>Unknown</option>" +
																					"<option value='2'>Yes</option>" +
																					"<option value='3'>No</option>" +
																				"</select>" +
																			"</td>" +
																			"<td class='camera_operator_flag'>" +
																				"<select name='animator_set-0-camera_operator_flag' id='id_animator_set-0-camera_operator_flag'>" +
																					"<option value='' selected='selected'>---------</option>" +
																					"<option value='1'>Unknown</option>" +
																					"<option value='2'>Yes</option>" +
																					"<option value='3'>No</option>" +
																				"</select>" +
																			"</td>" +
																			"<td class='facilitator_flag'>" +
																				"<select name='animator_set-0-facilitator_flag' id='id_animator_set-0-facilitator_flag'>" +
																					"<option value='' selected='selected'>---------</option>" +
																					"<option value='1'>Unknown</option>" +
																					"<option value='2'>Yes</option>" +
																					"<option value='3'>No</option>" +
																				"</select>" +
																			"</td>" +
																			"<td class='phone_no'>" +
																				"<input id='id_animator_set-0-phone_no' type='text' class='vTextField' name='animator_set-0-phone_no' maxlength='100' />" +
																			"</td>" +
																			"<td class='address'>" +
																				"<input id='id_animator_set-0-address' type='text' class='vTextField' name='animator_set-0-address' maxlength='500' />" +
																			"</td>" +
																			"<td class='partner'>" +
																				"<select name='animator_set-0-partner' id='id_animator_set-0-partner'>" +
																					"<option value='' selected='selected'>---------</option>" +
																				"</select>" +
																			"</td>" +
																			"<td class='delete'></td>" +
																		"</tr>" +
																		"<tr class='row2 '>" +
																			"<td class='original'>" +
																				"<input type='hidden' name='animator_set-1-id' id='id_animator_set-1-id' />" +
																				"<input type='hidden' name='animator_set-1-village' id='id_animator_set-1-village' />" +
																			"</td>" +
																			"<td class='name'>" +
																				"<input id='id_animator_set-1-name' type='text' class='vTextField' name='animator_set-1-name' maxlength='100' />" +
																			"</td>" +
																			"<td class='age'>" +
																				"<input id='id_animator_set-1-age' type='text' class='vIntegerField' name='animator_set-1-age' />" +
																			"</td>" +
																			"<td class='gender'>" +
																				"<select name='animator_set-1-gender' id='id_animator_set-1-gender'>" +
																					"<option value='' selected='selected'>---------</option>" +
																					"<option value='M'>Male</option>" +
																					"<option value='F'>Female</option>" +
																				"</select>" +
																			"</td>" +
																			"<td class='csp_flag'>" +
																				"<select name='animator_set-1-csp_flag' id='id_animator_set-1-csp_flag'>" +
																					"<option value='' selected='selected'>---------</option>" +
																					"<option value='1'>Unknown</option>" +
																					"<option value='2'>Yes</option>" +
																					"<option value='3'>No</option>" +
																				"</select>" +
																			"</td>" +
																			"<td class='camera_operator_flag'>" +
																				"<select name='animator_set-1-camera_operator_flag' id='id_animator_set-1-camera_operator_flag'>" +
																					"<option value='' selected='selected'>---------</option>" +
																					"<option value='1'>Unknown</option>" +
																					"<option value='2'>Yes</option>" +
																					"<option value='3'>No</option>" +
																				"</select>" +
																			"</td>" +
																			"<td class='facilitator_flag'>" +
																				"<select name='animator_set-1-facilitator_flag' id='id_animator_set-1-facilitator_flag'>" +
																					"<option value='' selected='selected'>---------</option>" +
																					"<option value='1'>Unknown</option>" +
																					"<option value='2'>Yes</option>" +
																					"<option value='3'>No</option>" +
																				"</select>" +
																			"</td>" +
																			"<td class='phone_no'>" +
																				"<input id='id_animator_set-1-phone_no' type='text' class='vTextField' name='animator_set-1-phone_no' maxlength='100' />" +
																			"</td>" +
																			"<td class='address'>" +
																				"<input id='id_animator_set-1-address' type='text' class='vTextField' name='animator_set-1-address' maxlength='500' />" +
																			"</td>" +
																			"<td class='partner'>" +
																				"<select name='animator_set-1-partner' id='id_animator_set-1-partner'>" +
																					"<option value='' selected='selected'>---------</option>" +
																				"</select>" +
																			"</td>" +
																			"<td class='delete'></td>" +
																		"</tr>" +
																		"<tr class='row1 '>" +
																			"<td class='original'>" +
																				"<input type='hidden' name='animator_set-2-id' id='id_animator_set-2-id' />" +
																				"<input type='hidden' name='animator_set-2-village' id='id_animator_set-2-village' />" +
																			"</td>" +
																		"<td class='name'>" +
																			"<input id='id_animator_set-2-name' type='text' class='vTextField' name='animator_set-2-name' maxlength='100' />" +
																		"</td>" +
																		"<td class='age'>" +
																			"<input id='id_animator_set-2-age' type='text' class='vIntegerField' name='animator_set-2-age' />" +
																		"</td>" +
																		"<td class='gender'>" +
																			"<select name='animator_set-2-gender' id='id_animator_set-2-gender'>" +
																				"<option value='' selected='selected'>---------</option>" +
																				"<option value='M'>Male</option>" +
																				"<option value='F'>Female</option>" +
																			"</select>" +
																		"</td>" +
																		"<td class='csp_flag'>" +
																			"<select name='animator_set-2-csp_flag' id='id_animator_set-2-csp_flag'>" +
																				"<option value='' selected='selected'>---------</option>" +
																				"<option value='1'>Unknown</option>" +
																				"<option value='2'>Yes</option>" +
																				"<option value='3'>No</option>" +
																			"</select>" +
																		"</td>" +
																		"<td class='camera_operator_flag'>" +
																			"<select name='animator_set-2-camera_operator_flag' id='id_animator_set-2-camera_operator_flag'>" +
																				"<option value='' selected='selected'>---------</option>" +
																				"<option value='1'>Unknown</option>" +
																				"<option value='2'>Yes</option>" +
																				"<option value='3'>No</option>" +
																			"</select>" +
																		"</td>" +
																		"<td class='facilitator_flag'>" +
																			"<select name='animator_set-2-facilitator_flag' id='id_animator_set-2-facilitator_flag'>" +
																				"<option value='' selected='selected'>---------</option>" +
																				"<option value='1'>Unknown</option>" +
																				"<option value='2'>Yes</option>" +
																				"<option value='3'>No</option>" +
																			"</select>" +
																		"</td>" +
																		"<td class='phone_no'>" +
																			"<input id='id_animator_set-2-phone_no' type='text' class='vTextField' name='animator_set-2-phone_no' maxlength='100' />" +
																		"</td>" +
																		"<td class='address'>" +
																			"<input id='id_animator_set-2-address' type='text' class='vTextField' name='animator_set-2-address' maxlength='500' />" +
																		"</td>" +
																		"<td class='partner'>" +
																			"<select name='animator_set-2-partner' id='id_animator_set-2-partner'>" +
																				"<option value='' selected='selected'>---------</option>" +
																			"</select>" +
																		"</td>" +
																		"<td class='delete'></td>" +
																	"</tr>" +
																	"<tr class='row2 '>" +
																		"<td class='original'>" +
																			"<input type='hidden' name='animator_set-3-id' id='id_animator_set-3-id' />" +
																			"<input type='hidden' name='animator_set-3-village' id='id_animator_set-3-village' />" +
																		"</td>" +
																	"<td class='name'>" +
																		"<input id='id_animator_set-3-name' type='text' class='vTextField' name='animator_set-3-name' maxlength='100' />" +
																	"</td>" +
																	"<td class='age'>" +
																		"<input id='id_animator_set-3-age' type='text' class='vIntegerField' name='animator_set-3-age' />" +
																	"</td>" +
																	"<td class='gender'>" +
																		"<select name='animator_set-3-gender' id='id_animator_set-3-gender'>" +
																			"<option value='' selected='selected'>---------</option>" +
																			"<option value='M'>Male</option>" +
																			"<option value='F'>Female</option>" +
																		"</select>" +
																	"</td>" +
																	"<td class='csp_flag'>" +
																		"<select name='animator_set-3-csp_flag' id='id_animator_set-3-csp_flag'>" +
																			"<option value='' selected='selected'>---------</option>" +
																			"<option value='1'>Unknown</option>" +
																			"<option value='2'>Yes</option>" +
																			"<option value='3'>No</option>" +
																		"</select>" +
																	"</td>" +
																	"<td class='camera_operator_flag'>" +
																		"<select name='animator_set-3-camera_operator_flag' id='id_animator_set-3-camera_operator_flag'>" +
																			"<option value='' selected='selected'>---------</option>" +
																			"<option value='1'>Unknown</option>" +
																			"<option value='2'>Yes</option>" +
																			"<option value='3'>No</option>" +
																		"</select>" +
																	"</td>" +
																	"<td class='facilitator_flag'>" +
																		"<select name='animator_set-3-facilitator_flag' id='id_animator_set-3-facilitator_flag'>" +
																			"<option value='' selected='selected'>---------</option>" +
																			"<option value='1'>Unknown</option>" +
																			"<option value='2'>Yes</option>" +
																			"<option value='3'>No</option>" +
																		"</select>" +
																	"</td>" +
																	"<td class='phone_no'>" +
																		"<input id='id_animator_set-3-phone_no' type='text' class='vTextField' name='animator_set-3-phone_no' maxlength='100' />" +
																	"</td>" +
																	"<td class='address'>" +
																		"<input id='id_animator_set-3-address' type='text' class='vTextField' name='animator_set-3-address' maxlength='500' />" +
																	"</td>" +
																	"<td class='partner'>" +
																		"<select name='animator_set-3-partner' id='id_animator_set-3-partner'>" +
																			"<option value='' selected='selected'>---------</option>" +
																		"</select>" +
																	"</td>" +
																	"<td class='delete'></td>" +
																"</tr>" +
																"<tr class='row1 '>" +
																	"<td class='original'>" +
																		"<input type='hidden' name='animator_set-4-id' id='id_animator_set-4-id' />" +
																		"<input type='hidden' name='animator_set-4-village' id='id_animator_set-4-village' />" +
																	"</td>" +
																	"<td class='name'>" +
																		"<input id='id_animator_set-4-name' type='text' class='vTextField' name='animator_set-4-name' maxlength='100' />" +
																	"</td>" +
																	"<td class='age'>" +
																		"<input id='id_animator_set-4-age' type='text' class='vIntegerField' name='animator_set-4-age' />" +
																	"</td>" +
																	"<td class='gender'>" +
																		"<select name='animator_set-4-gender' id='id_animator_set-4-gender'>" +
																			"<option value='' selected='selected'>---------</option>" +
																			"<option value='M'>Male</option>" +
																			"<option value='F'>Female</option>" +
																		"</select>" +
																	"</td>" +
																	"<td class='csp_flag'>" +
																		"<select name='animator_set-4-csp_flag' id='id_animator_set-4-csp_flag'>" +
																			"<option value='' selected='selected'>---------</option>" +
																			"<option value='1'>Unknown</option>" +
																			"<option value='2'>Yes</option>" +
																			"<option value='3'>No</option>" +
																		"</select>" +
																	"</td>" +
																	"<td class='camera_operator_flag'>" +
																		"<select name='animator_set-4-camera_operator_flag' id='id_animator_set-4-camera_operator_flag'>" +
																			"<option value='' selected='selected'>---------</option>" +
																			"<option value='1'>Unknown</option>" +
																			"<option value='2'>Yes</option>" +
																			"<option value='3'>No</option>" +
																		"</select>" +
																	"</td>" +
																	"<td class='facilitator_flag'>" +
																		"<select name='animator_set-4-facilitator_flag' id='id_animator_set-4-facilitator_flag'>" +
																			"<option value='' selected='selected'>---------</option>" +
																			"<option value='1'>Unknown</option>" +
																			"<option value='2'>Yes</option>" +
																			"<option value='3'>No</option>" +
																		"</select>" +
																	"</td>" +
																	"<td class='phone_no'>" +
																		"<input id='id_animator_set-4-phone_no' type='text' class='vTextField' name='animator_set-4-phone_no' maxlength='100' />" +
																	"</td>" +
																	"<td class='address'>" +
																		"<input id='id_animator_set-4-address' type='text' class='vTextField' name='animator_set-4-address' maxlength='500' />" +
																	"</td>" +
																	"<td class='partner'>" +
																		"<select name='animator_set-4-partner' id='id_animator_set-4-partner'>" +
																			"<option value='' selected='selected'>---------</option>" +
																		"</select>" +
																	"</td>" +
																	"<td class='delete'></td>" +
																"</tr>" +
															"</table>" +
														"</fieldset>" +
													"</div>" +
												"</div>" +	
												"<div class='submit-row' >" +
													"<input id='save' type='button' value='Save' class='default' name='_save' />" +
												"</div>" +
												"<script type='text/javascript'>document.getElementById('id_village_name').focus();</script>" +
												"<script type='text/javascript'>" +
												"</script>" +
											"</div>" +
									"</div>" +
									"<br class='clear' />" +
								"</div>" +
								"<script src='/media/js/admin/DateTimeShortcuts.js' type='text/javascript'></script>" +	
								"<script type='text/javascript'>DateTimeShortcuts.init()</script>";
}
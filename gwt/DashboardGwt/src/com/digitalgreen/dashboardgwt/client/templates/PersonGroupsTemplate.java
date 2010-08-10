package com.digitalgreen.dashboardgwt.client.templates;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.PersonsData;
import com.digitalgreen.dashboardgwt.client.data.PersonGroupsData;
import com.digitalgreen.dashboardgwt.client.data.VillagesData;
import com.digitalgreen.dashboardgwt.client.servlets.PersonGroups;
import com.digitalgreen.dashboardgwt.client.servlets.Villages;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.Hyperlink;

public class PersonGroupsTemplate extends BaseTemplate{
	
	public PersonGroupsTemplate(RequestContext requestContext) {
		super(requestContext);
		ArrayList personData = new ArrayList();
		personData.add((new PersonsData()).getNewData());
		this.formTemplate = new Form((new PersonGroupsData()).getNewData(), 
				new Object[] {personData});
	}
	
	@Override
	public void fill() {
		String templateType = "person group";
		String templatePlainType = "dashboard/persongroup/add/";
		RequestContext requestContext = new RequestContext();
		HashMap args = new HashMap();
		args.put("action", "add");
		requestContext.setArgs(args);
		requestContext.setForm(this.formTemplate);
		PersonGroups addPersonsGroupsServlet = new PersonGroups(requestContext);
		RequestContext saveRequestContext = new RequestContext(RequestContext.METHOD_POST);
		saveRequestContext.setForm(this.formTemplate);
		PersonGroups savePersonGroup = new PersonGroups(saveRequestContext);
		
		// Draw the content of the template depending on the request type (GET/POST)
		super.fillDGTemplate(templateType, persongroupsListHtml, persongroupsAddHtml, addDataToElementID);
		// Add it to the rootpanel
		super.fill();
		//Now add listings
		List<Hyperlink> links =  this.fillListings();
		// Now add hyperlinks
		super.fillDgListPage(templatePlainType, templateType, persongroupsListFormHtml, addPersonsGroupsServlet, links);
		// Now add any submit control buttons
		super.fillDgFormPage(savePersonGroup);
	}
	
	protected List<Hyperlink> fillListings() {		
		HashMap queryArgs = this.getRequestContext().getArgs();
		String queryArg = (String)queryArgs.get("action");
		List<Hyperlink> links = new ArrayList<Hyperlink>();
		// If we're unsure, just default to list view
		if(queryArg.equals("list")) {
			// 	Add Listings
			List personGroups = (List)queryArgs.get("listing");			
			if(personGroups != null){
				String tableRows ="";
				String style;
				PersonGroupsData.Data personGroup;
				RequestContext requestContext = null;
				for (int row = 0; row < personGroups.size(); ++row) {
					if(row%2==0)
						style= "row2";
					else
						style = "row1";
					personGroup = (PersonGroupsData.Data)personGroups.get(row);
					requestContext = new RequestContext();
					requestContext.getArgs().put("action", "edit");
					requestContext.getArgs().put("id", personGroup.getId());
					requestContext.setForm(this.formTemplate);
					links.add(this.createHyperlink("<a href='#dashboard/persongroups/" + personGroup.getId() + "/'>" +
							personGroup.getPersonGroupName() + "</a>",
							"dashboard/persongroups/" + personGroup.getId() + "/",
							new PersonGroups(requestContext)));
					tableRows += "<tr class='" +style+ "'>" +
					  "<td><input type='checkbox' class='action-select' value='"+ personGroup.getId() + "' name='_selected_action' /></td>" +
					  "<th id = 'row" + row + "'></th>" +
					  "<td>"+ personGroup.getVillage().getVillageName() + "</td>" + 
					"</tr>";
				}
				persongroupsListFormHtml = persongroupsListFormHtml + tableRows + "</tbody></table>";
			}
		}
		return links;
	}
	
	final private String addDataToElementID[] = {"id_village","id_person_set-0-village","id_person_set-1-village","id_person_set-2-village",
			"id_person_set-3-village","id_person_set-4-village","id_person_set-5-village","id_person_set-6-village","id_person_set-7-village",
			"id_person_set-8-village","id_person_set-9-village"};
	
	private String persongroupsListFormHtml = "<div class = 'toolbar'><label for='searchbar'>" +
										"<img alt='Search' src='/media/img/admin/icon_searchbox.png'></label>" +
										"<input type='text' id='searchbar' value='' name='q' size='40'>" +
										"<input id='search' type='button' value='Search'>" +
									"</div>"+
									"<div class='actions'>" +
									"<label>Action: <select name='action'>" +
										"<option value='' selected='selected'>---------</option>" +
										"<option value='delete_selected'>Delete selected Person groups</option>" +
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
													"Group name" +
												"</a>" +
											"</th>" +
											"<th>" +
												"<a href='?ot=asc&amp;o=2'>" +
													"Village" +
												"</a>" +
											"</th>" +
										"</tr>" +
									"</thead>" +
									"<tbody>";
	
	final private String persongroupsListHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
									"<div id='content' class='flex'>" +
										"<h1>Select Person Group to change</h1>" +
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
	
	final private String persongroupsAddHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
								"<div id='content' class='colM'>" +
									"<h1>Add Person group</h1>" +
									"<div id='content-main'>" +
										//"<form enctype='multipart/form-data' action='' method='post' id='persongroups_form'>" +
											"<div>" +
												"<fieldset class='module aligned '>" +
													"<div class='form-row group_name  '>" +
														"<div>" +
															"<label for='id_group_name' class='required'>Group name:</label><input id='id_group_name' type='text' class='vTextField' name='group_name' maxlength='100' />" +
														"</div>" +
													"</div>" +
													"<div class='form-row days  '>" +
														"<div>" +
															"<label for='id_days'>Days:</label><select name='days' id='id_days'>" +
															"<option value='' selected='selected'>---------</option>" +
															"<option value='Monday'>Monday</option>" +
															"<option value='Tuesday'>Tuesday</option>" +
															"<option value='Wednesday'>Wednesday</option>" +
															"<option value='Thursday'>Thursday</option>" +
															"<option value='Friday'>Friday</option>" +
															"<option value='Saturday'>Saturday</option>" +
															"<option value='Sunday'>Sunday</option>" +
															"</select>" +
														"</div>" +
													"</div>" +
													"<div class='form-row timings  '>" +
														"<div>" +
															"<label for='id_timings'>Timings:</label><input id='id_timings' type='text' class='vTimeField' name='timings' size='8' />" +
															
														"</div>" +
													"</div>" +
													"<div class='form-row village  '>" +
														"<div>" +
															"<label for='id_village' class='required'>Village:</label><select name='village' id='id_village'>" +
																"<option value='' selected='selected'>---------</option>" +
															"</select>" +
														"</div>" +
													"</div>" +
												"</fieldset>" +
												"<div class='inline-group'>" +
													"<div class='tabular inline-related last-related'>" +
														"<input type='hidden' name='person_set-TOTAL_FORMS' value='30' id='id_person_set-TOTAL_FORMS' /><input type='hidden' name='person_set-INITIAL_FORMS' value='0' id='id_person_set-INITIAL_FORMS' />" +
														"<fieldset class='module'>" +
														"<h2>Persons</h2>" +
															"<table>" +
																"<thead>" +
																	"<tr>" +
																		"<th colspan='2'>Person name</th>" +
																		"<th >Father name</th>" +
																		"<th >Age</th>" +
																		"<th >Gender</th>" +
																		"<th >Phone no</th>" +
																		"<th >Address</th>" +
																		"<th >Land holdings</th>" +
																		"<th >Village</th>" +
																		"<th>Delete?</th>" +
																	"</tr>" +
																"</thead>" +

																"<tr class='row1 '>" +							////////////////////////////////////////////////1
																	"<td class='original'>" +
																		"<input type='hidden' name='person_set-0-id' id='id_person_set-0-id' />" +
																		"<input type='hidden' name='person_set-0-group' id='id_person_set-0-group' />" +
																	"</td>" +
																	"<td class='person_name'>" +
																		"<input id='id_person_set-0-person_name' type='text' class='vTextField' name='person_set-0-person_name' maxlength='100' />" +
																	"</td>" +
																	"<td class='father_name'>" +
																		"<input id='id_person_set-0-father_name' type='text' class='vTextField' name='person_set-0-father_name' maxlength='100' />" +
																	"</td>" +
																	"<td class='age'>" +
																		"<input id='id_person_set-0-age' type='text' class='vIntegerField' name='person_set-0-age' />" +
																	"</td>" +
																	"<td class='gender'>" +
																		"<select name='person_set-0-gender' id='id_person_set-0-gender'>" +
																			"<option value='' selected='selected'>---------</option>" +
																			"<option value='M'>Male</option>" +
																			"<option value='F'>Female</option>" +
																		"</select>" +
																	"</td>" +
																	"<td class='phone_no'>" +
																		"<input id='id_person_set-0-phone_no' type='text' class='vTextField' name='person_set-0-phone_no' maxlength='100' />" +
																	"</td>" +
																	"<td class='address'>" +
																		"<input id='id_person_set-0-address' type='text' class='vTextField' name='person_set-0-address' maxlength='500' />" +
																	"</td>" +
																	"<td class='land_holdings'>" +
																		"<input id='id_person_set-0-land_holdings' type='text' class='vIntegerField' name='person_set-0-land_holdings' />" +
																	"</td>" +
																	"<td class='village'>" +
																		"<select name='person_set-0-village' id='id_person_set-0-village'>" +
																			"<option value='' selected='selected'>---------</option>" +
																		"</select>" +
																	"</td>" +
																	"<td class='delete'></td>" +
																"</tr>" +

																"<tr class='row2 '>" +							////////////////////////////////////////////////2
																	"<td class='original'>" +
																		"<input type='hidden' name='person_set-1-id' id='id_person_set-1-id' />" +
																		"<input type='hidden' name='person_set-1-group' id='id_person_set-1-group' />" +
																	"</td>" +
																	"<td class='person_name'>" +
																		"<input id='id_person_set-1-person_name' type='text' class='vTextField' name='person_set-1-person_name' maxlength='100' />" +
																	"</td>" +
																	"<td class='father_name'>" +
																		"<input id='id_person_set-1-father_name' type='text' class='vTextField' name='person_set-1-father_name' maxlength='100' />" +
																	"</td>" +
																	"<td class='age'>" +
																		"<input id='id_person_set-1-age' type='text' class='vIntegerField' name='person_set-1-age' />" +
																	"</td>" +
																	"<td class='gender'>" +
																		"<select name='person_set-1-gender' id='id_person_set-1-gender'>" +
																			"<option value='' selected='selected'>---------</option>" +
																			"<option value='M'>Male</option>" +
																			"<option value='F'>Female</option>" +
																		"</select>" +
																	"</td>" +
																	"<td class='phone_no'>" +
																		"<input id='id_person_set-1-phone_no' type='text' class='vTextField' name='person_set-1-phone_no' maxlength='100' />" +
																	"</td>" +
																	"<td class='address'>" +
																		"<input id='id_person_set-1-address' type='text' class='vTextField' name='person_set-1-address' maxlength='500' />" +
																	"</td>" +
																	"<td class='land_holdings'>" +
																		"<input id='id_person_set-1-land_holdings' type='text' class='vIntegerField' name='person_set-1-land_holdings' />" +
																	"</td>" +
																	"<td class='village'>" +
																		"<select name='person_set-1-village' id='id_person_set-1-village'>" +
																			"<option value='' selected='selected'>---------</option>" +
																		"</select>" +
																	"</td>" +
																	"<td class='delete'></td>" +
																"</tr>" +

																"<tr class='row1 '>" +							////////////////////////////////////////////////3
																	"<td class='original'>" +
																		"<input type='hidden' name='person_set-2-id' id='id_person_set-2-id' />" +
																		"<input type='hidden' name='person_set-2-group' id='id_person_set-2-group' />" +
																	"</td>" +
																	"<td class='person_name'>" +
																		"<input id='id_person_set-2-person_name' type='text' class='vTextField' name='person_set-2-person_name' maxlength='100' />" +
																	"</td>" +
																	"<td class='father_name'>" +
																		"<input id='id_person_set-2-father_name' type='text' class='vTextField' name='person_set-2-father_name' maxlength='100' />" +
																	"</td>" +
																	"<td class='age'>" +
																		"<input id='id_person_set-2-age' type='text' class='vIntegerField' name='person_set-2-age' />" +
																	"</td>" +
																	"<td class='gender'>" +
																		"<select name='person_set-2-gender' id='id_person_set-2-gender'>" +
																			"<option value='' selected='selected'>---------</option>" +
																			"<option value='M'>Male</option>" +
																			"<option value='F'>Female</option>" +
																		"</select>" +
																	"</td>" +
																	"<td class='phone_no'>" +
																		"<input id='id_person_set-2-phone_no' type='text' class='vTextField' name='person_set-2-phone_no' maxlength='100' />" +
																	"</td>" +
																	"<td class='address'>" +
																		"<input id='id_person_set-2-address' type='text' class='vTextField' name='person_set-2-address' maxlength='500' />" +
																	"</td>" +
																	"<td class='land_holdings'>" +
																		"<input id='id_person_set-2-land_holdings' type='text' class='vIntegerField' name='person_set-2-land_holdings' />" +
																	"</td>" +
																	"<td class='village'>" +
																		"<select name='person_set-2-village' id='id_person_set-2-village'>" +
																			"<option value='' selected='selected'>---------</option>" +
																		"</select>" +
																	"</td>" +
																	"<td class='delete'></td>" +
																"</tr>" +

																"<tr class='row2 '>" +							////////////////////////////////////////////////4
																	"<td class='original'>" +
																		"<input type='hidden' name='person_set-3-id' id='id_person_set-3-id' />" +
																		"<input type='hidden' name='person_set-3-group' id='id_person_set-3-group' />" +
																	"</td>" +
																	"<td class='person_name'>" +
																		"<input id='id_person_set-3-person_name' type='text' class='vTextField' name='person_set-3-person_name' maxlength='100' />" +
																	"</td>" +
																	"<td class='father_name'>" +
																		"<input id='id_person_set-3-father_name' type='text' class='vTextField' name='person_set-3-father_name' maxlength='100' />" +
																	"</td>" +
																	"<td class='age'>" +
																		"<input id='id_person_set-3-age' type='text' class='vIntegerField' name='person_set-3-age' />" +
																	"</td>" +
																	"<td class='gender'>" +
																		"<select name='person_set-3-gender' id='id_person_set-3-gender'>" +
																			"<option value='' selected='selected'>---------</option>" +
																			"<option value='M'>Male</option>" +
																			"<option value='F'>Female</option>" +
																		"</select>" +
																	"</td>" +
																	"<td class='phone_no'>" +
																		"<input id='id_person_set-3-phone_no' type='text' class='vTextField' name='person_set-3-phone_no' maxlength='100' />" +
																	"</td>" +
																	"<td class='address'>" +
																		"<input id='id_person_set-3-address' type='text' class='vTextField' name='person_set-3-address' maxlength='500' />" +
																	"</td>" +
																	"<td class='land_holdings'>" +
																		"<input id='id_person_set-3-land_holdings' type='text' class='vIntegerField' name='person_set-3-land_holdings' />" +
																	"</td>" +
																	"<td class='village'>" +
																		"<select name='person_set-3-village' id='id_person_set-3-village'>" +
																			"<option value='' selected='selected'>---------</option>" +
																		"</select>" +
																	"</td>" +
																	"<td class='delete'></td>" +
																"</tr>" +

																"<tr class='row1 '>" +							////////////////////////////////////////////////5
																	"<td class='original'>" +
																		"<input type='hidden' name='person_set-4-id' id='id_person_set-4-id' />" +
																		"<input type='hidden' name='person_set-4-group' id='id_person_set-4-group' />" +
																	"</td>" +
																	"<td class='person_name'>" +
																		"<input id='id_person_set-4-person_name' type='text' class='vTextField' name='person_set-4-person_name' maxlength='100' />" +
																	"</td>" +
																	"<td class='father_name'>" +
																		"<input id='id_person_set-4-father_name' type='text' class='vTextField' name='person_set-4-father_name' maxlength='100' />" +
																	"</td>" +
																	"<td class='age'>" +
																		"<input id='id_person_set-4-age' type='text' class='vIntegerField' name='person_set-4-age' />" +
																	"</td>" +
																	"<td class='gender'>" +
																		"<select name='person_set-4-gender' id='id_person_set-4-gender'>" +
																			"<option value='' selected='selected'>---------</option>" +
																			"<option value='M'>Male</option>" +
																			"<option value='F'>Female</option>" +
																		"</select>" +
																	"</td>" +
																	"<td class='phone_no'>" +
																		"<input id='id_person_set-4-phone_no' type='text' class='vTextField' name='person_set-4-phone_no' maxlength='100' />" +
																	"</td>" +
																	"<td class='address'>" +
																		"<input id='id_person_set-4-address' type='text' class='vTextField' name='person_set-4-address' maxlength='500' />" +
																	"</td>" +
																	"<td class='land_holdings'>" +
																		"<input id='id_person_set-4-land_holdings' type='text' class='vIntegerField' name='person_set-4-land_holdings' />" +
																	"</td>" +
																	"<td class='village'>" +
																		"<select name='person_set-4-village' id='id_person_set-4-village'>" +
																			"<option value='' selected='selected'>---------</option>" +
																		"</select>" +
																	"</td>" +
																	"<td class='delete'></td>" +
																"</tr>" +

																"<tr class='row2 '>" +							////////////////////////////////////////////////6
																	"<td class='original'>" +
																		"<input type='hidden' name='person_set-5-id' id='id_person_set-5-id' />" +
																		"<input type='hidden' name='person_set-5-group' id='id_person_set-5-group' />" +
																	"</td>" +
																	"<td class='person_name'>" +
																		"<input id='id_person_set-5-person_name' type='text' class='vTextField' name='person_set-5-person_name' maxlength='100' />" +
																	"</td>" +
																	"<td class='father_name'>" +
																		"<input id='id_person_set-5-father_name' type='text' class='vTextField' name='person_set-5-father_name' maxlength='100' />" +
																	"</td>" +
																	"<td class='age'>" +
																		"<input id='id_person_set-5-age' type='text' class='vIntegerField' name='person_set-5-age' />" +
																	"</td>" +
																	"<td class='gender'>" +
																		"<select name='person_set-5-gender' id='id_person_set-5-gender'>" +
																			"<option value='' selected='selected'>---------</option>" +
																			"<option value='M'>Male</option>" +
																			"<option value='F'>Female</option>" +
																		"</select>" +
																	"</td>" +
																	"<td class='phone_no'>" +
																		"<input id='id_person_set-5-phone_no' type='text' class='vTextField' name='person_set-5-phone_no' maxlength='100' />" +
																	"</td>" +
																	"<td class='address'>" +
																		"<input id='id_person_set-5-address' type='text' class='vTextField' name='person_set-5-address' maxlength='500' />" +
																	"</td>" +
																	"<td class='land_holdings'>" +
																		"<input id='id_person_set-5-land_holdings' type='text' class='vIntegerField' name='person_set-5-land_holdings' />" +
																	"</td>" +
																	"<td class='village'>" +
																		"<select name='person_set-5-village' id='id_person_set-5-village'>" +
																			"<option value='' selected='selected'>---------</option>" +
																		"</select>" +
																	"</td>" +
																	"<td class='delete'></td>" +
																"</tr>" +

																"<tr class='row1 '>" +							////////////////////////////////////////////////7
																	"<td class='original'>" +
																		"<input type='hidden' name='person_set-6-id' id='id_person_set-6-id' />" +
																		"<input type='hidden' name='person_set-6-group' id='id_person_set-6-group' />" +
																	"</td>" +
																	"<td class='person_name'>" +
																		"<input id='id_person_set-6-person_name' type='text' class='vTextField' name='person_set-6-person_name' maxlength='100' />" +
																	"</td>" +
																	"<td class='father_name'>" +
																		"<input id='id_person_set-6-father_name' type='text' class='vTextField' name='person_set-6-father_name' maxlength='100' />" +
																	"</td>" +
																	"<td class='age'>" +
																		"<input id='id_person_set-6-age' type='text' class='vIntegerField' name='person_set-6-age' />" +
																	"</td>" +
																	"<td class='gender'>" +
																		"<select name='person_set-6-gender' id='id_person_set-6-gender'>" +
																			"<option value='' selected='selected'>---------</option>" +
																			"<option value='M'>Male</option>" +
																			"<option value='F'>Female</option>" +
																		"</select>" +
																	"</td>" +
																	"<td class='phone_no'>" +
																		"<input id='id_person_set-6-phone_no' type='text' class='vTextField' name='person_set-6-phone_no' maxlength='100' />" +
																	"</td>" +
																	"<td class='address'>" +
																		"<input id='id_person_set-6-address' type='text' class='vTextField' name='person_set-6-address' maxlength='500' />" +
																	"</td>" +
																	"<td class='land_holdings'>" +
																		"<input id='id_person_set-6-land_holdings' type='text' class='vIntegerField' name='person_set-6-land_holdings' />" +
																	"</td>" +
																	"<td class='village'>" +
																		"<select name='person_set-6-village' id='id_person_set-6-village'>" +
																			"<option value='' selected='selected'>---------</option>" +
																		"</select>" +
																	"</td>" +
																	"<td class='delete'></td>" +
																"</tr>" +

																"<tr class='row2 '>" +							////////////////////////////////////////////////8
																	"<td class='original'>" +
																		"<input type='hidden' name='person_set-7-id' id='id_person_set-7-id' />" +
																		"<input type='hidden' name='person_set-7-group' id='id_person_set-7-group' />" +
																	"</td>" +
																	"<td class='person_name'>" +
																		"<input id='id_person_set-7-person_name' type='text' class='vTextField' name='person_set-7-person_name' maxlength='100' />" +
																	"</td>" +
																	"<td class='father_name'>" +
																		"<input id='id_person_set-7-father_name' type='text' class='vTextField' name='person_set-7-father_name' maxlength='100' />" +
																	"</td>" +
																	"<td class='age'>" +
																		"<input id='id_person_set-7-age' type='text' class='vIntegerField' name='person_set-7-age' />" +
																	"</td>" +
																	"<td class='gender'>" +
																		"<select name='person_set-7-gender' id='id_person_set-7-gender'>" +
																			"<option value='' selected='selected'>---------</option>" +
																			"<option value='M'>Male</option>" +
																			"<option value='F'>Female</option>" +
																		"</select>" +
																	"</td>" +
																	"<td class='phone_no'>" +
																		"<input id='id_person_set-7-phone_no' type='text' class='vTextField' name='person_set-7-phone_no' maxlength='100' />" +
																	"</td>" +
																	"<td class='address'>" +
																		"<input id='id_person_set-7-address' type='text' class='vTextField' name='person_set-7-address' maxlength='500' />" +
																	"</td>" +
																	"<td class='land_holdings'>" +
																		"<input id='id_person_set-7-land_holdings' type='text' class='vIntegerField' name='person_set-7-land_holdings' />" +
																	"</td>" +
																	"<td class='village'>" +
																		"<select name='person_set-7-village' id='id_person_set-7-village'>" +
																			"<option value='' selected='selected'>---------</option>" +
																		"</select>" +
																	"</td>" +
																	"<td class='delete'></td>" +
																"</tr>" +

																"<tr class='row1 '>" +							////////////////////////////////////////////////9
																	"<td class='original'>" +
																		"<input type='hidden' name='person_set-8-id' id='id_person_set-8-id' />" +
																		"<input type='hidden' name='person_set-8-group' id='id_person_set-8-group' />" +
																	"</td>" +
																	"<td class='person_name'>" +
																		"<input id='id_person_set-8-person_name' type='text' class='vTextField' name='person_set-8-person_name' maxlength='100' />" +
																	"</td>" +
																	"<td class='father_name'>" +
																		"<input id='id_person_set-8-father_name' type='text' class='vTextField' name='person_set-8-father_name' maxlength='100' />" +
																	"</td>" +
																	"<td class='age'>" +
																		"<input id='id_person_set-8-age' type='text' class='vIntegerField' name='person_set-8-age' />" +
																	"</td>" +
																	"<td class='gender'>" +
																		"<select name='person_set-8-gender' id='id_person_set-8-gender'>" +
																			"<option value='' selected='selected'>---------</option>" +
																			"<option value='M'>Male</option>" +
																			"<option value='F'>Female</option>" +
																		"</select>" +
																	"</td>" +
																	"<td class='phone_no'>" +
																		"<input id='id_person_set-8-phone_no' type='text' class='vTextField' name='person_set-8-phone_no' maxlength='100' />" +
																	"</td>" +
																	"<td class='address'>" +
																		"<input id='id_person_set-8-address' type='text' class='vTextField' name='person_set-8-address' maxlength='500' />" +
																	"</td>" +
																	"<td class='land_holdings'>" +
																		"<input id='id_person_set-8-land_holdings' type='text' class='vIntegerField' name='person_set-8-land_holdings' />" +
																	"</td>" +
																	"<td class='village'>" +
																		"<select name='person_set-8-village' id='id_person_set-8-village'>" +
																			"<option value='' selected='selected'>---------</option>" +
																		"</select>" +
																	"</td>" +
																	"<td class='delete'></td>" +
																"</tr>" +

																"<tr class='row2 '>" +							////////////////////////////////////////////////10
																	"<td class='original'>" +
																		"<input type='hidden' name='person_set-9-id' id='id_person_set-9-id' />" +
																		"<input type='hidden' name='person_set-9-group' id='id_person_set-9-group' />" +
																	"</td>" +
																	"<td class='person_name'>" +
																		"<input id='id_person_set-9-person_name' type='text' class='vTextField' name='person_set-9-person_name' maxlength='100' />" +
																	"</td>" +
																	"<td class='father_name'>" +
																		"<input id='id_person_set-9-father_name' type='text' class='vTextField' name='person_set-9-father_name' maxlength='100' />" +
																	"</td>" +
																	"<td class='age'>" +
																		"<input id='id_person_set-9-age' type='text' class='vIntegerField' name='person_set-9-age' />" +
																	"</td>" +
																	"<td class='gender'>" +
																		"<select name='person_set-9-gender' id='id_person_set-9-gender'>" +
																			"<option value='' selected='selected'>---------</option>" +
																			"<option value='M'>Male</option>" +
																			"<option value='F'>Female</option>" +
																		"</select>" +
																	"</td>" +
																	"<td class='phone_no'>" +
																		"<input id='id_person_set-9-phone_no' type='text' class='vTextField' name='person_set-9-phone_no' maxlength='100' />" +
																	"</td>" +
																	"<td class='address'>" +
																		"<input id='id_person_set-9-address' type='text' class='vTextField' name='person_set-9-address' maxlength='500' />" +
																	"</td>" +
																	"<td class='land_holdings'>" +
																		"<input id='id_person_set-9-land_holdings' type='text' class='vIntegerField' name='person_set-9-land_holdings' />" +
																	"</td>" +
																	"<td class='village'>" +
																		"<select name='person_set-9-village' id='id_person_set-9-village'>" +
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
											"<script type='text/javascript'>document.getElementById('id_group_name').focus();</script>" +
											"<script type='text/javascript'>" +
											"</script>" +
										"</div>" +
									//"</form>" +
								"</div>" +
								"<br class='clear' />" +
							"</div>";
}

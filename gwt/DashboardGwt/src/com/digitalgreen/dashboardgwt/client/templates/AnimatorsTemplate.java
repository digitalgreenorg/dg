package com.digitalgreen.dashboardgwt.client.templates;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.AnimatorAssignedVillagesData;
import com.digitalgreen.dashboardgwt.client.data.AnimatorsData;
import com.digitalgreen.dashboardgwt.client.data.PersonsData;
import com.digitalgreen.dashboardgwt.client.servlets.Animators;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

public class AnimatorsTemplate extends BaseTemplate {
	
	public AnimatorsTemplate(RequestContext requestContext){
		super(requestContext);
	}
	
	@Override
	public void fill(){
		
		String templateType = "Animator";
		String templatePlainType = "dashboard/animators/add";
		RequestContext requestContext = new RequestContext();
		HashMap args = new HashMap();
		args.put("action", "add");
		requestContext.setArgs(args);
		Animators addAnimatorsServlet = new Animators(requestContext);
		RequestContext saveRequestContext = new RequestContext(RequestContext.METHOD_POST);
		ArrayList animatorAssignedVillageData = new ArrayList();
		animatorAssignedVillageData.add((new AnimatorAssignedVillagesData()).getNewData());
		Form saveForm = new Form((new AnimatorsData()).getNewData(), 
				new Object[] {animatorAssignedVillageData});
		saveRequestContext.setForm(saveForm);
		Animators saveAnimator = new Animators(saveRequestContext);
		// Draw the content of the template depending on the request type (GET/POST)
		super.fillDGTemplate(templateType, animatorsListHtml, animatorsAddHtml, addDataToElementID);
		// Add it to the rootpanel
		super.fill();		
		this.fillListings();
		// Now add hyperlinks
		super.fillDGLinkControls(templatePlainType, templateType, animatorsListFormHtml, addAnimatorsServlet);
		// Now add any submit control buttons
		super.fillDgFormFields(saveAnimator);
	}
	
	protected void fillListings() {
		
		HashMap queryArgs = this.getRequestContext().getArgs();
		String queryArg = (String)queryArgs.get("action");
		// If we're unsure, just default to list view
		if(queryArg == null || queryArg != "add") {
			// 	Add Listings
			List animators = (List)queryArgs.get("listing");			
			if(animators != null){
				String tableRows ="";
				String style;
				AnimatorsData.Data animator;
				for (int row = 0; row < animators.size(); ++row) {
					if(row%2==0)
						style= "row2";
					else
						style = "row1";
					animator = (AnimatorsData.Data)animators.get(row);
					tableRows += "<tr class='" +style+ "'>" +
					  "<td><input type='checkbox' class='action-select' value='"+ animator.getId() + "' name='_selected_action' /></td>" +
						"<th><a href='/admin/dashboard/animator/"+ animator.getId() +"/'>" + animator.getAnimatorName()+"</a></th>" +
						"<td>"+ animator.getPartner().getPartnerName() + "</td>" + 
						"<td>"+ animator.getVillage().getVillageName() + "</td>" + 
					"</tr>";
				}
				animatorsListFormHtml = animatorsListFormHtml + tableRows + "</tbody></table>";
			}
		}
	}
	
	final private String addDataToElementID [] = {"id_partner","id_village","id_animatorassignedvillage_set-0-village",
			"id_animatorassignedvillage_set-1-village","id_animatorassignedvillage_set-2-village"};

	private String animatorsListFormHtml = "<div class='actions'>" +
								"<label>Action: <select name='action'>" +
									"<option value='' selected='selected'>---------</option>" +
									"<option value='delete_selected'>Delete selected animators</option>" +
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
											"Name" +
											"</a>" +
										"</th>" +
										"<th>" +
											"<a href='?ot=asc&amp;o=2'>" +
											"Partner" +
											"</a>" +
										"</th>" +
										"<th>" +
											"<a href='?ot=asc&amp;o=3'>" +
											"Home village" +
											"</a>" +
										"</th>" +
									"</tr>" +
								"</thead>";
								
	private String animatorsListHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
								"<div id='content' class='flex'>" +
									"<h1>Select Animators to change</h1>" +
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
	
	final static private String animatorsAddHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
							"<div id='content' class='colM'>" +
								"<h1>Add Animator</h1>" +
								"<div id='content-main'>" +
									//"<form enctype='multipart/form-data' action='' method='post' id='animator_form'>" +
										"<div>" +
											"<fieldset class='module aligned '>" +
												"<div class='form-row name  '>" +
													"<div>" +
														"<label for='id_name' class='required'>Name:</label><input id='id_name' type='text' class='vTextField' name='name' maxlength='100' />" +
													"</div>" +
												"</div>" +
												"<div class='form-row age  '>" +
													"<div>" +
														"<label for='id_age'>Age:</label><input id='id_age' type='text' class='vIntegerField' name='age' />" +
													"</div>" +
												"</div>" +
												"<div class='form-row gender  '>" +
													"<div>" +
														"<label for='id_gender' class='required'>Gender:</label><select name='gender' id='id_gender'>" +
															"<option value='' selected='selected'>---------</option>" +
															"<option value='M'>Male</option>" +
															"<option value='F'>Female</option>" +
														"</select>" +
													"</div>" +
												"</div>" +
												"<div class='form-row csp_flag  '>" +
													"<div>" +
														"<label for='id_csp_flag'>Csp flag:</label><select name='csp_flag' id='id_csp_flag'>" +
															"<option value='1' selected='selected'>Unknown</option>" +
															"<option value='2'>Yes</option>" +
															"<option value='3'>No</option>" +
														"</select>" +
													"</div>" +
												"</div>" +
												"<div class='form-row camera_operator_flag  '>" +
													"<div>" +
														"<label for='id_camera_operator_flag'>Camera operator flag:</label><select name='camera_operator_flag' id='id_camera_operator_flag'>" +
															"<option value='1' selected='selected'>Unknown</option>" +
															"<option value='2'>Yes</option>" +
															"<option value='3'>No</option>" +
														"</select>" +
													"</div>" +
												"</div>" +
												"<div class='form-row facilitator_flag  '>" +
													"<div>" +
														"<label for='id_facilitator_flag'>Facilitator flag:</label><select name='facilitator_flag' id='id_facilitator_flag'>" +
															"<option value='1' selected='selected'>Unknown</option>" +
															"<option value='2'>Yes</option>" +
															"<option value='3'>No</option>" +
														"</select>" +
													"</div>" +
												"</div>" +
												"<div class='form-row phone_no  '>" +
													"<div>" +
														"<label for='id_phone_no'>Phone no:</label><input id='id_phone_no' type='text' class='vTextField' name='phone_no' maxlength='100' />" +
													"</div>" +
												"</div>" +
												"<div class='form-row address  '>" +
													"<div>" +
														"<label for='id_address'>Address:</label><input id='id_address' type='text' class='vTextField' name='address' maxlength='500' />" +
													"</div>" +
												"</div>" +
												"<div class='form-row partner  '>" +
													"<div>" +
														"<label for='id_partner' class='required'>Partner:</label><select name='partner' id='id_partner'>" +
															"<option value='' selected='selected'>---------</option>" +
														"</select>" +
													"</div>" +
												"</div>" +
												"<div class='form-row village  '>" +
													"<div>" +
														"<label for='id_village' class='required'>Home village:</label><select name='village' id='id_village'>" +
															"<option value='' selected='selected'>---------</option>" +
														"</select>" +
													"</div>" +
												"</div>" +
											"</fieldset>" +
											"<div class='inline-group'>" +
												"<h2>Animator Assigned Villages</h2>" +
												"<input type='hidden' name='animatorassignedvillage_set-TOTAL_FORMS' value='3' id='id_animatorassignedvillage_set-TOTAL_FORMS' /><input type='hidden' name='animatorassignedvillage_set-INITIAL_FORMS' value='0' id='id_animatorassignedvillage_set-INITIAL_FORMS' />" +
												"<div class='inline-related'>" +
													"<h3><b>Animator Assigned Village:</b>&nbsp; #1" +
													"</h3>" +
													"<fieldset class='module aligned '>" +  
														"<div class='form-row village  '>" +
															"<div>" +
																"<label for='id_animatorassignedvillage_set-0-village' class='required'>Village:</label><select name='animatorassignedvillage_set-0-village' id='id_animatorassignedvillage_set-0-village'>" +
																	"<option value='' selected='selected'>---------</option>" +
																"</select>" +
															"</div>" +
														"</div>" +
														"<div class='form-row start_date  '>" +
															"<div>" +
																"<label for='id_animatorassignedvillage_set-0-start_date'>Start date:</label><input id='id_animatorassignedvillage_set-0-start_date' type='text' class='vDateField' name='animatorassignedvillage_set-0-start_date' size='10' />" +
															"</div>" +
														"</div>" +
													"</fieldset>" +
													"<input type='hidden' name='animatorassignedvillage_set-0-id' id='id_animatorassignedvillage_set-0-id' />" +
													"<input type='hidden' name='animatorassignedvillage_set-0-animator' id='id_animatorassignedvillage_set-0-animator' />" +
												"</div>" +
												"<div class='inline-related'>" +
													"<h3><b>Animator Assigned Village:</b>&nbsp; #2" +
													"</h3>" +
													"<fieldset class='module aligned '>" +
														"<div class='form-row village  '>" +
															"<div>" +
																"<label for='id_animatorassignedvillage_set-1-village' class='required'>Village:</label><select name='animatorassignedvillage_set-1-village' id='id_animatorassignedvillage_set-1-village'>" +
																	"<option value='' selected='selected'>---------</option>" +
																"</select>" +
															"</div>" +
														"</div>" +
														"<div class='form-row start_date  '>" +
															"<div>" +
																"<label for='id_animatorassignedvillage_set-1-start_date'>Start date:</label><input id='id_animatorassignedvillage_set-1-start_date' type='text' class='vDateField' name='animatorassignedvillage_set-1-start_date' size='10' />" +
															"</div>" +      
														"</div>" +
													"</fieldset>" +  
													"<input type='hidden' name='animatorassignedvillage_set-1-id' id='id_animatorassignedvillage_set-1-id' />" +
													"<input type='hidden' name='animatorassignedvillage_set-1-animator' id='id_animatorassignedvillage_set-1-animator' />" +
												"</div>" +
												"<div class='inline-related last-related'>" +
													"<h3><b>Animator Assigned Village:</b>&nbsp; #3" +
													"</h3>" +
													"<fieldset class='module aligned '>" +
														"<div class='form-row village  '>" +
															"<div>" +
																"<label for='id_animatorassignedvillage_set-2-village' class='required'>Village:</label><select name='animatorassignedvillage_set-2-village' id='id_animatorassignedvillage_set-2-village'>" +
																	"<option value='' selected='selected'>---------</option>" +
																"</select>" +
															"</div>" +
														"</div>" +
														"<div class='form-row start_date  '>" +
															"<div>" +
																"<label for='id_animatorassignedvillage_set-2-start_date'>Start date:</label><input id='id_animatorassignedvillage_set-2-start_date' type='text' class='vDateField' name='animatorassignedvillage_set-2-start_date' size='10' />" +
															"</div>" +
														"</div>" +
													"</fieldset>" +
													"<input type='hidden' name='animatorassignedvillage_set-2-id' id='id_animatorassignedvillage_set-2-id' />" +
													"<input type='hidden' name='animatorassignedvillage_set-2-animator' id='id_animatorassignedvillage_set-2-animator' />" +
												"</div>" +
											"</div>" +
											"<div class='submit-row' >" +
											"<input id='save' value='Save' class='default' name='_save' />" +
											"</div>" +
											"<script type='text/javascript'>document.getElementById('id_name').focus();</script>" +
											"<script type='text/javascript'>" +
											"</script>" +
										"</div>" +
									//"</form>" +
								"</div>" +
							"</div>"+
							"<script src='/media/js/admin/DateTimeShortcuts.js' type='text/javascript'></script>" +	
							"<script type='text/javascript'>DateTimeShortcuts.init()</script>";
}

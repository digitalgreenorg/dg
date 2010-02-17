package com.digitalgreen.dashboardgwt.client.templates;

import java.util.HashMap;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.servlets.AnimatorAssignedVillages;

public class AnimatorAssignedVillagesTemplate extends BaseTemplate {
	public AnimatorAssignedVillagesTemplate(RequestContext requestContext) {
		super(requestContext);
	}
	
	@Override
	public void fill() {
		String templatePlainType = "animator assigned villages";
		String templateType = "animator_assigned_villages";
		RequestContext requestContext = new RequestContext();
		HashMap args = new HashMap();
		args.put("action", "add");
		requestContext.setArgs(args);
		AnimatorAssignedVillages addAnimatorAssignedVillagesServlet = new AnimatorAssignedVillages(requestContext);
		AnimatorAssignedVillages region = new AnimatorAssignedVillages(new RequestContext(RequestContext.METHOD_POST, 
				getPostForm()));
		// Draw the content of the template depending on the request type (GET/POST)
		super.fillDGTemplate(templateType, animatorassignedvillageListHtml, animatorassignedvillageAddHtml);
		// Add it to the rootpanel
		super.fill();
		// Now add hyperlinks
		super.fillDGLinkControls(templateType, templatePlainType, animatorassignedvillageListFormHtml, addAnimatorAssignedVillagesServlet);
		// Now add any submit control buttons
		super.fillDGSubmitControls(region);
	}
	
	final static private String animatorassignedvillageListFormHtml = "<div class='actions'>" +
								"<label>Action: <select name='action'>" +
									"<option value='' selected='selected'>---------</option>" +
									"<option value='delete_selected'>Delete selected animator assigned villages</option>" +
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
												"Animator" +
											"</a>" +
										"</th>" +
										"<th>" +
											"<a href='?ot=asc&amp;o=2'>" +
												"Village" +
											"</a>" +
										"</th>" +
									"</tr>" +
								"</thead>" +
								"<tbody>" +
									"<div id='data-rows'" +
									"</div>" +
								"</tbody>" +
							"</table>";
	
	// Fill ids:  listing-form-body, add-link
	final static private String animatorassignedvillageListHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
							"<div id='content' class='flex'>" +
							"<h1>Select Animator Assigned Village to change</h1>" +
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
	
	final static private String animatorassignedvillageAddHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
						"<div id='content' class='colM'>" +
							"<h1>Add Animator Assigned Village</h1>" +
							"<div id='content-main'>" +
								"<form enctype='multipart/form-data' action='' method='post' id='animatorassignedvillage_form'>" +
								"<div>" +
									"<fieldset class='module aligned '>" +
										"<div class='form-row animator  '>" +
											"<div>" +
												"<label for='id_animator' class='required'>Animator:</label><select name='animator' id='id_animator'>" +
												"<option value='' selected='selected'>---------</option>" +
												"</select><a href='/admin/dashboard/animator/add/' class='add-another' id='add_id_animator' onclick='return showAddAnotherPopup(this);'> <img src='/media/img/admin/icon_addlink.gif' width='10' height='10' alt='Add Another'/></a>" +
											"</div>" +
										"</div>" +
										"<div class='form-row village  '>" +
											"<div>" +
												"<label for='id_village' class='required'>Village:</label><select name='village' id='id_village'>" +
												"<option value='' selected='selected'>---------</option>" +
												"</select><a href='/admin/dashboard/village/add/' class='add-another' id='add_id_village' onclick='return showAddAnotherPopup(this);'> <img src='/media/img/admin/icon_addlink.gif' width='10' height='10' alt='Add Another'/></a>" +
											"</div>" +
										"</div>" +
										"<div class='form-row start_date  '>" +
											"<div>" +
												"<label for='id_start_date'>Start date:</label><input id='id_start_date' type='text' class='vDateField' name='start_date' size='10' />" +
											"</div>" +
										"</div>" +
									"</fieldset>" +
									"<div class='submit-row' >" +
										"<input type='submit' value='Save' class='default' name='_save' />" +
										"<input id='save_a' type='submit' value='Save and add another' name='_addanother'/>" +
										"<input id='save_c' type='submit' value='Save and continue editing' name='_continue' />" +
									"</div>" +
									"<script type='text/javascript'>document.getElementById('id_animator').focus();</script>" +
									"<script type='text/javascript'>" +
									"</script>" +
								"</div>" +
								"</form>" +
							"</div>" +
						"</div>";
}

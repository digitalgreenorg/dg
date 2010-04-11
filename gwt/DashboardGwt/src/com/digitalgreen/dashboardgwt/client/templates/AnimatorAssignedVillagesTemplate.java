package com.digitalgreen.dashboardgwt.client.templates;

import java.util.HashMap;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.AnimatorAssignedVillagesData;
import com.digitalgreen.dashboardgwt.client.data.AnimatorAssignedVillagesData;
import com.digitalgreen.dashboardgwt.client.servlets.AnimatorAssignedVillages;
import com.digitalgreen.dashboardgwt.client.servlets.AnimatorAssignedVillages;
import com.google.gwt.user.client.History;
import com.google.gwt.user.client.Window;

public class AnimatorAssignedVillagesTemplate extends BaseTemplate {
	public AnimatorAssignedVillagesTemplate(RequestContext requestContext) {
		super(requestContext);
	}
	
	@Override
	public void fill() {
	
		String templateType = "AnimatorAssignedVillage";
		String templatePlainType = "dashboard/animatorassignedvillage/add";
		RequestContext requestContext = new RequestContext();
		HashMap args = new HashMap();
		args.put("action", "add");
		requestContext.setArgs(args);
		AnimatorAssignedVillages addAnimatorAssignedVillagesServlet1 = new AnimatorAssignedVillages(requestContext);
		RequestContext saveRequestContext = new RequestContext(RequestContext.METHOD_POST);
		Form saveForm = new Form((new AnimatorAssignedVillagesData()).getNewData());
		saveRequestContext.setForm(saveForm);
		AnimatorAssignedVillages saveAnimatorAssignedVillage = new AnimatorAssignedVillages(saveRequestContext);
		// Draw the content of the template depending on the request type (GET/POST)
		super.fillDGTemplate(templateType, animatorassignedvillageListHtml, animatorassignedvillageAddHtml, addDataToElementID);

		// Add it to the rootpanel
		super.fill();		
		this.fillListings();		
		// Now add hyperlinks
		super.fillDGLinkControls(templatePlainType, templateType, animatorassignedvillageListFormHtml, addAnimatorAssignedVillagesServlet1);
		// Now add any submit control buttons
		super.fillDGSubmitControls(saveAnimatorAssignedVillage);
	}
	
	
	protected void fillListings() {
		HashMap queryArgs = this.getRequestContext().getArgs();
		String queryArg = (String)queryArgs.get("action");
		// If we're unsure, just default to list view
		if(queryArg == null || queryArg != "add") {
			// 	Add Listings
			List animatorAssignedVillages = (List)queryArgs.get("listing");			
			if(animatorAssignedVillages  != null){
				String tableRows ="";
				String style;
				AnimatorAssignedVillagesData.Data animatorAssignedVillage;
				for (int row = 0; row < animatorAssignedVillages.size(); ++row) {
					if(row%2==0)
						style= "row2";
					else
						style = "row1";
					animatorAssignedVillage = (AnimatorAssignedVillagesData.Data) animatorAssignedVillages.get(row);
					tableRows += "<tr class='" +style+ "'>" +
								  "<td><input type='checkbox' class='action-select' value='"+ animatorAssignedVillage.getId() + "' name='_selected_action' /></td>" +
									"<th><a href='/admin/dashboard/animatorAssignedVillage/"+ animatorAssignedVillage.getId() +"/'>" + animatorAssignedVillage.getAnimator().getAnimatorName()+"</a></th>" +
									"<td>"+ animatorAssignedVillage.getVillage().getVillageName() + "</td>" +
								"</tr>";
				}
				animatorassignedvillageListFormHtml = animatorassignedvillageListFormHtml + tableRows + "</tbody></table>";
			}
		}
	}
	
	
	
	final private String addDataToElementID[] = {"id_animator","id_village"};
	
	private String animatorassignedvillageListFormHtml = "<div class='actions'>" +
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
								"<tbody>";
								
	
	// Fill ids:  listing-form-body, add-link
	private String animatorassignedvillageListHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
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
	
	private String animatorassignedvillageAddHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
						"<div id='content' class='colM'>" +
							"<h1>Add Animator Assigned Village</h1>" +
							"<div id='content-main'>" +
								//"<form enctype='multipart/form-data' action='' method='post' id='animatorassignedvillage_form'>" +
								//"<div>" +
									"<fieldset class='module aligned '>" +
										"<div class='form-row animator  '>" +
											"<div>" +
												"<label for='id_animator' class='required'>Animator:</label><select name='animator' id='id_animator'>" +
												"<option value='' selected='selected'>---------</option>" +
												"</select>" +
											"</div>" +
										"</div>" +
										"<div class='form-row village  '>" +
											"<div>" +
												"<label for='id_village' class='required'>Village:</label><select name='village' id='id_village'>" +
												"<option value='' selected='selected'>---------</option>" +
												"</select>" +
											"</div>" +
										"</div>" +
										"<div class='form-row start_date  '>" +
											"<div>" +
												"<label for='id_start_date'>Start date:</label><input id='id_start_date' type='text' class='vDateField' name='start_date' size='10' />" +
											"</div>" +
										"</div>" +
									"</fieldset>" +
									"<div class='submit-row' >" +
										"<input id='save' value='Save' class='default' name='_save' />" +
									"</div>" +
									"<script type='text/javascript'>document.getElementById('id_animator').focus();</script>" +
									"<script type='text/javascript'>" +
									"</script>" +
								"</div>" +
								//"</form>" +
							//"</div>" +
						"</div>"+
						"<script src='/media/js/admin/DateTimeShortcuts.js' type='text/javascript'></script>" +	
						"<script type='text/javascript'>DateTimeShortcuts.init()</script>";
}

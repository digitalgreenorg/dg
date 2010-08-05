package com.digitalgreen.dashboardgwt.client.templates;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.AnimatorAssignedVillagesData;
import com.digitalgreen.dashboardgwt.client.data.AnimatorAssignedVillagesData;
import com.digitalgreen.dashboardgwt.client.servlets.AnimatorAssignedVillages;
import com.digitalgreen.dashboardgwt.client.data.AnimatorAssignedVillagesData;
import com.digitalgreen.dashboardgwt.client.servlets.AnimatorAssignedVillages;
import com.google.gwt.user.client.History;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.Hyperlink;

public class AnimatorAssignedVillagesTemplate extends BaseTemplate {

	public AnimatorAssignedVillagesTemplate(RequestContext requestContext) {
		super(requestContext);
		this.formTemplate = new Form((new AnimatorAssignedVillagesData()).getNewData());
	}
	
	@Override
	public void fill() {
	
		String templateType = "AnimatorAssignedVillage";
		String templatePlainType = "dashboard/animatorassignedvillage/add";
		RequestContext requestContext = new RequestContext();
		HashMap args = new HashMap();
		args.put("action", "add");
		requestContext.setArgs(args);
		requestContext.setForm(this.formTemplate);
		RequestContext saveRequestContext = new RequestContext(RequestContext.METHOD_POST);
		AnimatorAssignedVillages addAnimatorAssignedVillagesServlet1 = new AnimatorAssignedVillages(requestContext);
		saveRequestContext.setForm(this.formTemplate);
		AnimatorAssignedVillages saveAnimatorAssignedVillage = new AnimatorAssignedVillages(saveRequestContext);
		// Draw the content of the template depending on the request type (GET/POST)
		super.fillDGTemplate(templateType, animatorassignedvillageListHtml, animatorassignedvillageAddHtml, addDataToElementID);
		// Add it to the rootpanel
		super.fill();
		//Now add listings
		List<Hyperlink> links = this.fillListings();
		// Now add hyperlinks
		super.fillDgListPage(templatePlainType, templateType, animatorassignedvillageListFormHtml, addAnimatorAssignedVillagesServlet1, links);
		// Now add any submit control buttons
		super.fillDgFormPage(saveAnimatorAssignedVillage);
	}
	
	protected List<Hyperlink> fillListings() {
		HashMap queryArgs = this.getRequestContext().getArgs();
		String queryArg = (String)queryArgs.get("action");
		List<Hyperlink> links = new ArrayList<Hyperlink>();
		// If we're unsure, just default to list view
		if(queryArg.equals("list")) {
			// 	Add Listings
			List animatorAssignedVillages = (List)queryArgs.get("listing");			
			if(animatorAssignedVillages  != null){
				String tableRows ="";
				String style;
				AnimatorAssignedVillagesData.Data animatorAssignedVillage;
				RequestContext requestContext = null;
				for (int row = 0; row < animatorAssignedVillages.size(); ++row) {
					if(row%2==0)
						style= "row2";
					else
						style = "row1";
					animatorAssignedVillage = (AnimatorAssignedVillagesData.Data) animatorAssignedVillages.get(row);
					requestContext = new RequestContext();
					requestContext.getArgs().put("action", "edit");
					requestContext.getArgs().put("id", animatorAssignedVillage.getId());
					requestContext.setForm(this.formTemplate);
					links.add(this.createHyperlink("<a href='#dashboard/animatorassignedvillage/" + animatorAssignedVillage.getId() + "/'>" +
							animatorAssignedVillage.getAnimator().getAnimatorName() +"</a>",
							"dashboard/animatorassignedvillage/" + animatorAssignedVillage.getId() +"/",
							new AnimatorAssignedVillages(requestContext)));
					tableRows += "<tr class='" + style + "'>" +
								  "<td><input type='checkbox' class='action-select' value='" + animatorAssignedVillage.getId() + "' name='_selected_action' /></td>" +
								  "<th id = 'row" + row + "'></th>" +
									"<td>" + animatorAssignedVillage.getVillage().getVillageName() + "</td>" +
								"</tr>";
				}
				animatorassignedvillageListFormHtml = animatorassignedvillageListFormHtml + tableRows + "</tbody></table>";
			}
		}
		return links;
	}
	
	
	
	final private String addDataToElementID[] = {"id_animator","id_village"};
	
	private String animatorassignedvillageListFormHtml = "<div class = 'toolbar'><label for='searchbar'>" +
									"<img alt='Search' src='/media/img/admin/icon_searchbox.png'></label>" +
									"<input type='text' id='searchbar' value='' name='q' size='40'>" +
									"<input id='search' type='button' value='Search'>" +
								"</div>"+
								"<div class='actions'>" +
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
								   "<div>" +
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
												"<label for='id_village' class='required'>Village:</label>" +
												"<select name='village' id='id_village'>" +
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
										"<input id='save' type='button' value='Save' class='default' name='_save' />" +
									"</div>" +
									"<script type='text/javascript'>document.getElementById('id_animator').focus();</script>" +
									"<script type='text/javascript'>" +
									"</script>" +
							"</div>" +
						"</div>";
}
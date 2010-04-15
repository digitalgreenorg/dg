package com.digitalgreen.dashboardgwt.client.templates;

import java.util.HashMap;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.TrainingAnimatorsTrainedData;
import com.digitalgreen.dashboardgwt.client.data.TrainingsData;
import com.digitalgreen.dashboardgwt.client.servlets.Trainings;

public class TrainingTemplate extends BaseTemplate{
	
	public TrainingTemplate(RequestContext requestContext) {
		super(requestContext);
	}
	
	@Override
	public void fill() {

		String templateType = "Training";
		String templatePlainType = "dashboard/training/add/";
		RequestContext requestContext = new RequestContext();
		HashMap args = new HashMap();
		args.put("action", "add");
		requestContext.setArgs(args);
		Trainings addTrainingsServlet = new Trainings(requestContext);
		RequestContext saveRequestContext = new RequestContext(RequestContext.METHOD_POST);
		Form saveForm = new Form((new TrainingsData()).new Data());
		saveRequestContext.setForm(saveForm);
		Trainings saveTraining = new Trainings(saveRequestContext);
		// Draw the content of the template depending on the request type (GET/POST)
		super.fillDGTemplate(templateType, trainingListHtml, trainingAddHtml, addDataToElementID);
		// Add it to the rootpanel
		super.fill();
		this.fillListings();
		// Now add hyperlinks
		super.fillDGLinkControls(templatePlainType, templateType, trainingListFormHtml, addTrainingsServlet);
		// Now add any submit control buttons
		super.fillDGSubmitControls(saveTraining);
	}
	
	protected void fillListings() {
		HashMap queryArgs = this.getRequestContext().getArgs();
		String queryArg = (String)queryArgs.get("action");
		// If we're unsure, just default to list view
		if(queryArg == null || queryArg != "add") {
			// 	Add Listings
			List trainings = (List)queryArgs.get("listing");			
			if(trainings  != null){
				String tableRows ="";
				String style;
				TrainingsData.Data training;
				for (int row = 0; row < trainings.size(); ++row) {
					if(row%2==0)
						style= "row2";
					else
						style = "row1";
					training = (TrainingsData.Data) trainings.get(row);
					tableRows += "<tr class='" +style+ "'>" +
								  "<td><input type='checkbox' class='action-select' value='"+ training.getId() + "' name='_selected_action' /></td>" +
									"<th><a href='/admin/dashboard/training/"+ training.getId() +"/'>" + training.getTrainingStartDate()+"</a></th>" +
									"<td>"+ training.getVillage().getVillageName() + "</td>" +
								"</tr>";
				}
				trainingListFormHtml = trainingListFormHtml + tableRows + "</tbody></table>";
			}
		}
	}
	
	final private String addDataToElementID[] = {"id_village","id_development_manager_present","id_field_officer_present","id_animators_trained"};
	
	private String trainingListFormHtml = "<div class='actions'>" +
								"<label>Action: <select name='action'>" +
									"<option value='' selected='selected'>---------</option>" +
									"<option value='delete_selected'>Delete selected trainings</option>" +
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
											"Date" +
										"</a>" +
									"</th>" +
									"<th>" +
										"<a href='?ot=asc&amp;o=2'>" +
											"Village" +
										"</a>" +
									"</th>" +
									"<th>" +
										"<a href='?ot=asc&amp;o=3'>" +
											"Location" +
										"</a>" +
									"</th>" +
								"</tr>" +
							"</thead>" +
							"<tbody>";							
	
	final private String trainingListHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
								"<div id='content' class='flex'>" +
									"<h1>Select Training to change</h1>" +
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
	
	final private String trainingAddHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
								"<div id='content' class='colM'>" +
									"<h1>Add Training</h1>" +
									"<div id='content-main'>" +
										//"<form enctype='multipart/form-data' action='' method='post' id='training_form'>" +
											"<div>" +
												"<fieldset class='module aligned '>" +
													"<div class='form-row training_purpose  '>" +
														"<div>" +
															"<label for='id_training_purpose'>Training purpose:</label><textarea id='id_training_purpose' rows='10' cols='40' name='training_purpose' class='vLargeTextField'></textarea>" +
														"</div>" +
													"</div>" +
													"<div class='form-row training_outcome  '>" +
														"<div>" +
															"<label for='id_training_outcome'>Training outcome:</label><textarea id='id_training_outcome' rows='10' cols='40' name='training_outcome' class='vLargeTextField'></textarea>" +
														"</div>" +
													"</div>" +
													"<div class='form-row training_start_date  '>" +
														"<div>" +
															"<label for='id_training_start_date' class='required'>Training start date:</label><input id='id_training_start_date' type='text' class='vDateField' name='training_start_date' size='10' />" +
														"</div>" +
													"</div>" +
													"<div class='form-row training_end_date  '>" +
														"<div>" +
															"<label for='id_training_end_date' class='required'>Training end date:</label><input id='id_training_end_date' type='text' class='vDateField' name='training_end_date' size='10' />" +
														"</div>" +
													"</div>" +
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
        											"<div class='form-row development_manager_present  '>" +
        												"<div>" +
        													"<label for='id_development_manager_present'>Development manager present:</label><select name='development_manager_present' id='id_development_manager_present'>" +
        														"<option value='' selected='selected'>---------</option>" +
        													"</select>" +
        												"</div>" +
        											"</div>" +
        											"<div class='form-row field_officer_present  '>" +
        												"<div>" +
        													"<label for='id_field_officer_present' class='required'>Field officer present:</label><select name='field_officer_present' id='id_field_officer_present'>" +
        														"<option value='' selected='selected'>---------</option>" +
        													"</select>" +
        												"</div>" +
        											"</div>" +
        											"<div class='form-row animators_trained  '>" +
        												"<div>" +
        													"<label for='id_animators_trained' class='required'>Animators trained:</label><select multiple='multiple' name='animators_trained' id='id_animators_trained'>" +
        													"</select>" +
        												"</div>" +
        											"</div>" +
        										"</fieldset>" +
        										"<div class='submit-row' >" +
        										"<input id='save' value='Save' class='default' name='_save' />" +
        										"</div>" +
        										"<script type='text/javascript'>document.getElementById('id_training_purpose').focus();</script>" +
        										"<script type='text/javascript'>" +
        										"</script>" +
        									"</div>" +
        								//"</form>" +
        							"</div>" +
        							"<br class='clear' />" +
        						"</div>"+
								"<script src='/media/js/admin/DateTimeShortcuts.js' type='text/javascript'></script>" +	
								"<script type='text/javascript'>DateTimeShortcuts.init()</script>";

}
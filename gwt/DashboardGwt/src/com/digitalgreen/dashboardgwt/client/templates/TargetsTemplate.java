package com.digitalgreen.dashboardgwt.client.templates;

import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.TargetsData;
import com.digitalgreen.dashboardgwt.client.servlets.Targets;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.Hyperlink;

public class TargetsTemplate extends BaseTemplate {
	
	public TargetsTemplate(RequestContext requestContext) {
		super(requestContext);
		this.formTemplate = new Form((new TargetsData()).getNewData());
	}
	
	@Override
	public void fill() {
		String templateType = "Target";
		String templatePlainType = "dashboard/target/add/";
		RequestContext requestContext = new RequestContext();
		HashMap args = new HashMap();
		args.put("action", "add");
		requestContext.setArgs(args);
		requestContext.setForm(this.formTemplate);
		Targets addTargetsServlet = new Targets(requestContext);
		RequestContext saveRequestContext = new RequestContext(RequestContext.METHOD_POST);
		Form saveForm = new Form((new TargetsData()).getNewData());
		saveRequestContext.setForm(this.formTemplate);
		String queryString = this.getRequestContext().getForm().getQueryString();
		if(queryString != null ) {
			String modifiedQueryString = "";
			String[] temp = queryString.split("&");
			for(int i=0; i < temp.length ; i++ ) {
				if(i==1) {
					String[] st = temp[i].split("=");
					String[] month_year = st[1].split("-");
					modifiedQueryString += "month_year_year="+month_year[0]+"&month_year_month="+month_year[1]+"&";
				} else {
					modifiedQueryString = (i == temp.length-1)? modifiedQueryString+temp[i] : modifiedQueryString+temp[i]+"&";											
				}
			}
			this.getRequestContext().getForm().setQueryString(modifiedQueryString);
		}		
		Targets saveTarget = new Targets(saveRequestContext);
		// Draw the content of the template depending on the request type (GET/POST)
		super.fillDGTemplate(templateType, targetsListHtml, targetsAddHtml, addDataToElementID);
		// Add it to the rootpanel
		super.fill();
		//Now add listings
		List<Hyperlink> links =  this.fillListings();
		// Now add hyperlinks
		super.fillDgListPage(templatePlainType, templateType, targetsListFormHtml, addTargetsServlet, links);
		// Now add any submit control buttons
		this.displayCalendar();
		super.fillDgFormPage(saveTarget);
	}
	
	protected List<Hyperlink> fillListings() {
		HashMap queryArgs = this.getRequestContext().getArgs();
		String queryArg = (String)queryArgs.get("action");
		List<Hyperlink> links = new ArrayList<Hyperlink>();
		// If we're unsure, just default to list view
		if(queryArg.equals("list")) {
			// 	Add Listings
			List targets = (List)queryArgs.get("listing");			
			if(targets  != null){
				String tableRows ="";
				String style;
				TargetsData.Data target;
				RequestContext requestContext = null;
				for (int row = 0; row <targets.size(); ++row) {
					if(row%2==0)
						style= "row2";
					else
						style = "row1";
					target = (TargetsData.Data) targets.get(row);
					Date d = new Date(target.getMonthYear());
					String[] monthYear = d.toString().split(" ");
					requestContext = new RequestContext();
					requestContext.getArgs().put("action", "edit");
					requestContext.getArgs().put("id", target.getId());
					requestContext.setForm(this.formTemplate);
					links.add(this.createHyperlink("<a href='#dashboard/target/" + target.getId() + "/'>" + 
							monthYear[1]+"  "+monthYear[5] + "</a>",
							"dashboard/target/" + target.getId() + "/",
							new Targets(requestContext)));
					tableRows += "<tr class='" +style+ "'>" +
								  "<td><input type='checkbox' class='action-select' value='"+ target.getId() + "' name='_selected_action' /></td>" +
								  "<th id = 'row" + row + "'></th>"+ 
									"<td>"+ target.getDistrict().getDistrictName() + "</td>"+
									"</tr>";
				}
				targetsListFormHtml = targetsListFormHtml + tableRows + "</tbody></table>";
			}
		}
		return links;
	}
	//Loading javascript for displaying calendar in Google chrome browser
	public static native void displayCalendar() /*-{
		$wnd.DateTimeShortcuts.init();		
	}-*/;
	final private String addDataToElementID[] = {"id_district"};
	
	private String targetsListFormHtml = "<div class='actions'>" +
    							"<label>Action: <select name='action'>" +
    								"<option value='' selected='selected'>---------</option>" +
    								"<option value='delete_selected'>Delete selected targets</option>" +
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
    										"<a href='?ot=asc&amp;o=2'>" +
    											"Month &amp; Year" +
    										"</a>" +
    									"</th>" +
    									"<th>" +
    										"<a href='?ot=asc&amp;o=3'>" +
    											"District" +
    										"</a>" +
    									"</th>" +
    								"</tr>" +
    							"</thead>" +
    							"<tbody>" ;
	
	final private String targetsListHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
								"<div id='content' class='flex'>" +
									"<h1>Select Target to change</h1>" +
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
	
	final private String targetsAddHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
    							"<div id='content' class='colM'>" +
    								"<h1>Add target</h1>" +
    								"<div id='content-main'>" +
    									"<fieldset class='module aligned '>" +
    											"<div class='form-row month_year'>" +
    												"<div>" +
		    											"<label for='id_month_year_month' class='required'>Month &amp; Year:</label>" +
		    											"<select name='month_year_month' id='id_month_year_month'>" +
			    											"<option value='0'>---</option>" +
			    											"<option value='01'>January</option>" +
			    											"<option value='02'>February</option>" +
			    											"<option value='03'>March</option>" +
			    											"<option value='04'>April</option>" +
			    											"<option value='05'>May</option>" +
			    											"<option value='06'>June</option>" +
			    											"<option value='07'>July</option>" +
			    											"<option value='08'>August</option>" +
			    											"<option value='09'>September</option>" +
			    											"<option value='10'>October</option>" +
			    											"<option value='11'>November</option>" +
			    											"<option value='12'>December</option>" +
		    											"</select>" +
		    											"<select name='month_year_year' id='id_month_year_year'>" +
			    											"<option value='0'>---</option>" +
			    											"<option value='2008'>2008</option>" +
			    											"<option value='2009'>2009</option>" +
			    											"<option value='2010'>2010</option>" +
			    											"<option value='2011'>2011</option>" +
			    											"<option value='2012'>2012</option>" +
			    											"<option value='2013'>2013</option>" +
			    										"</select>" +
	    											"</div>" +
    											"</div>  "+
    											"<div class='form-row district  '>" +
	    											"<div><label for='id_district' class='required'>District:</label>" +
		    											"<select name='district' id='id_district'>" +
		    											"</select>" +
	    											"</div>" +
    											"</div>"+
    											"</fieldset>" +
    											"<fieldset class='module aligned '>" +
    											"<h2>New Villages</h2>"+
    												"<div class='form-row clusters_identification  '>" +
    												"<div>" +
    												"<label for='id_clusters_identification'>Villages Identification:</label>" +
    												"<input id='id_clusters_identification' type='text' class='vIntegerField' " +
    												"name='clusters_identification' />" +
    												"</div>" +
    												"</div>" +
    												"<div class='form-row dg_concept_sharing  '>" +
    												"<div><label for='id_dg_concept_sharing'>DG Concept Sharing:</label>" +
    												"<input id='id_dg_concept_sharing' type='text' class='vIntegerField' name='dg_concept_sharing' />" +
    												"</div>" +
    												"</div>" +
    												"<div class='form-row csp_identification  '>" +
    												"<div><label for='id_csp_identification'>CSP Identified:</label>" +
    												"<input id='id_csp_identification' type='text' class='vIntegerField' " +
    												"name='csp_identification' />" +
    												"</div>" +
    												"</div>" +
    												"<div class='form-row dissemination_set_deployment  '>" +
    												"<div>" +
    												"<label for='id_dissemination_set_deployment'>Dissemination set deployment:</label>" +
    												"<input id='id_dissemination_set_deployment' type='text' class='vIntegerField' name='dissemination_set_deployment' />" +
    												"</div>" +
    												"</div>" +
    												"</fieldset>" +
    												"<fieldset class='module aligned '>" +
    												"<div class='form-row village_operationalization  '>" +
    												"<div>" +
    												"<label for='id_village_operationalization'>Village operationalization:</label>" +
    												"<input id='id_village_operationalization' type='text' class='vIntegerField' " +
    												"name='village_operationalization' />" +
    												"</div>" +
    												"</div>" +
    												"</fieldset>" +
    												"<fieldset class='module aligned '>" +
    												"<h2>Videos</h2>" +
    												"<div class='form-row video_uploading  '>" +
    												"<div>" +
    												"<label for='id_video_uploading'>Video uploading:</label>" +
    												"<input id='id_video_uploading' type='text' class='vIntegerField' " +
    												"name='video_uploading' />" +
    												"</div>" +
    												"</div>" +
    												"<div class='form-row video_production  '>" +
    												"<div>" +
    												"<label for='id_video_production'>Video production:</label><input id='id_video_production' type='text' class='vIntegerField' name='video_production' />" +
    												"</div>" +
    												"</div>" +
    												"<div class='form-row storyboard_preparation  '>" +
    												"<div>" +
    												"<label for='id_storyboard_preparation'>Storyboard preparation:</label>" +
    												"<input id='id_storyboard_preparation' type='text' class='vIntegerField' " +
    												"name='storyboard_preparation' />" +
    												"</div>" +
    												"</div>" +
    												"<div class='form-row video_shooting  '>" +
    												"<div>" +
    												"<label for='id_video_shooting'>Video shooting:</label>" +
    												"<input id='id_video_shooting' type='text' class='vIntegerField' name='video_shooting' />" +
    												"</div>" +
    												"</div>" +
    												"<div class='form-row video_editing  '>" +
    												"<div>" +
    												"<label for='id_video_editing'>Video editing:</label>" +
    												"<input id='id_video_editing' type='text' class='vIntegerField' name='video_editing' />" +
    												"</div>" +
    												"</div>" +
    												"<div class='form-row video_quality_checking  '>" +
    												"<div>" +
    												"<label for='id_video_quality_checking'>Video quality checking:</label>" +
    												"<input id='id_video_quality_checking' type='text' class='vIntegerField' " +
    												"name='video_quality_checking' />" +
    												"</div>" +
    												"</div>" +
    												"</fieldset>" +
    												"<fieldset class='module aligned '>" +
    												"<h2>Disseminations</h2>" +
    												"<div class='form-row disseminations  '>" +
    												"<div>" +
    												"<label for='id_disseminations'>Disseminations:</label>" +
    												"<input id='id_disseminations' type='text' class='vIntegerField' name='disseminations' />" +
    												"</div>" +
    												"</div>" +
    												"<div class='form-row avg_attendance_per_dissemination  '>" +
    												"<div>" +
    												"<label for='id_avg_attendance_per_dissemination'>Average Attendance per Dissemination:</label>" +
    												"<input id='id_avg_attendance_per_dissemination' type='text' class='vIntegerField' " +
    												"name='avg_attendance_per_dissemination' />" +
    												"</div>" +
    												"</div>" +
    												"<div class='form-row exp_interest_per_dissemination  '>" +
    												"<div>" +
    												"<label for='id_exp_interest_per_dissemination'>Expressed Interest per Dissemination:</label>" +
    												"<input id='id_exp_interest_per_dissemination' type='text' class='vIntegerField' " +
    												"name='exp_interest_per_dissemination' />" +
    												"</div>" +
    												"</div>" +
    												"<div class='form-row adoption_per_dissemination  '>" +
    												"<div>" +
    												"<label for='id_adoption_per_dissemination'>Adoption per Dissemination:</label>" +
    												"<input id='id_adoption_per_dissemination' type='text' class='vIntegerField' " +
    												"name='adoption_per_dissemination' />" +
    												"</div>" +
    												"</div>" +
    												"</fieldset>" +
    												"<fieldset class='module aligned '>" +
    												"<h2>Training</h2>" +
    												"<div class='form-row crp_training  '>" +
    												"<div>" +
    												"<label for='id_crp_training'>CRP Training:</label>" +
    												"<input id='id_crp_training' type='text' class='vIntegerField' name='crp_training' />" +
    												"</div>" +
    												"</div>" +
    												"<div class='form-row crp_refresher_training  '>" +
    												"<div>" +
    												"<label for='id_crp_refresher_training'>CRP Refresher Training:</label>" +
    												"<input id='id_crp_refresher_training' type='text' class='vIntegerField' " +
    												"name='crp_refresher_training' />" +
    												"</div>" +
    												"</div>" +
    												"<div class='form-row csp_training  '>" +
    												"<div>" +
    												"<label for='id_csp_training'>CSP Training:</label>" +
    												"<input id='id_csp_training' type='text' class='vIntegerField' name='csp_training' />" +
    												"</div>" +
    												"</div>" +
    												"<div class='form-row csp_refresher_training  '>" +
    												"<div>" +
    												"<label for='id_csp_refresher_training'>CSP Refresher Training:</label>" +
    												"<input id='id_csp_refresher_training' type='text' class='vIntegerField' " +
    												"name='csp_refresher_training' />" +
    												"</div>" +
    												"</div>" +
    												"<div class='form-row editor_training  '>" +
    												"<div>" +
    												"<label for='id_editor_training'>Editor training:</label>" +
    												"<input id='id_editor_training' type='text' class='vIntegerField' name='editor_training' />" +
    												"</div>" +
    												"</div>" +
    												"<div class='form-row editor_refresher_training  '>" +
    												"<div>" +
    												"<label for='id_editor_refresher_training'>Editor refresher training:</label>" +
    												"<input id='id_editor_refresher_training' type='text' class='vIntegerField'" +
    												" name='editor_refresher_training' />" +
    												"</div>" +
    												"</div>" +
    												"</fieldset>" +
    												"<fieldset class='module aligned '>" +
    												"<div class='form-row villages_certification  '>" +
    												"<div>" +
    												"<label for='id_villages_certification'>Villages certification:</label>" +
    												"<input id='id_villages_certification' type='text' class='vIntegerField' " +
    												"name='villages_certification' />" +
    												"</div>" +
    												"</div>" +
    												"</fieldset>" +
    												"<fieldset class='module aligned '>" +
    												"<h2>Qualitative Feedback</h2>" +
    												"<div class='form-row what_went_well  '>" +
    												"<div>" +
    												"<label for='id_what_went_well'>What went well and why?:</label>" +
    												"<textarea id='id_what_went_well' rows='10' cols='40' name='what_went_well' " +
    												"class='vLargeTextField'></textarea>" +
    												"</div>" +
    												"</div>" +
    												"<div class='form-row what_not_went_well  '>" +
    												"<div>" +
    												"<label for='id_what_not_went_well'>What did NOT go well and why?:</label>" +
    												"<textarea id='id_what_not_went_well' rows='10' cols='40' name='what_not_went_well' " +
    												"class='vLargeTextField'></textarea>" +
    												"</div>" +
    												"</div><div class='form-row challenges  '>" +
    												"<div>" +
    												"<label for='id_challenges'>Challenges:</label>" +
    												"<textarea id='id_challenges' rows='10' cols='40' name='challenges' class='vLargeTextField'></textarea>" +
    												"</div>" +
    												"</div>" +
    												"<div class='form-row support_requested  '>" +
    												"<div>" +
    												"<label for='id_support_requested'>Support requested:</label>" +
    												"<textarea id='id_support_requested' rows='10' cols='40' name='support_requested' " +
    												"class='vLargeTextField'></textarea>" +
    												"</div>" +
    												"</div>" +
    												"</fieldset>"+    												
    												"<div class='submit-row' >" +
													"<input id='save' type='button' value='Save' class='default' name='_save' />" +
												"</div>" +
												"<script type='text/javascript'>document.getElementById('id_month_year').focus();</script>" +
												"<script type='text/javascript'>" +
												"</script>" +
											//"</div>" +
										//"</form>" +
									"</div>" +
									"<br class='clear' />" +
								"</div>"; 
}

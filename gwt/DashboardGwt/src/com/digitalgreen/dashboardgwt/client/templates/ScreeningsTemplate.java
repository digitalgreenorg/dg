package com.digitalgreen.dashboardgwt.client.templates;

import java.util.HashMap;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.servlets.Regions;
import com.digitalgreen.dashboardgwt.client.servlets.Screenings;
import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.Button;
import com.google.gwt.user.client.ui.FormPanel;
import com.google.gwt.user.client.ui.HTMLPanel;
import com.google.gwt.user.client.ui.Hyperlink;
import com.google.gwt.user.client.ui.RootPanel;

public class ScreeningsTemplate extends BaseTemplate {
	private FormPanel postForm = null;
	private HTMLPanel displayHtml = null;
	
	public ScreeningsTemplate(RequestContext requestContext) {
		super(requestContext);
	}
	
	public FormPanel getPostForm() {
		return this.postForm;
	}
	
	private void fillUserDefined() {
		HashMap queryArgs = this.getRequestContext().getArgs();
		String queryArg = (String)queryArgs.get("action");
		// If we're unsure, just default to list view
		if(queryArg == null || queryArg != "add") {
			HTMLPanel listFormHtml = new HTMLPanel(screeningsListFormHtml);
			RootPanel.get("listing-form-body").insert(listFormHtml, 0);
			Hyperlink addLink = new Hyperlink();
			addLink.setHTML("<a class='addlink' href='#add-screenings-link'> Add screening </a>");
			// Take them to the add page for screenings
			addLink.addClickHandler(new ClickHandler() {
				public void onClick(ClickEvent event) {
					// Assume a GET request so call the empty constructer
					RequestContext requestContext = new RequestContext();
					HashMap args = new HashMap();
					// Prepare the servlet to render the add page
					args.put("action", "add");
					requestContext.setArgs(args);
					// Now give the servlet control
					Screenings screening = new Screenings(requestContext);
					screening.response();
				}
			});
			RootPanel.get("add-link").add(addLink);
		}
	}
	
	@Override
	public void fill() {
		HashMap queryArgs = this.getRequestContext().getArgs();
		String queryArg = (String)queryArgs.get("action");
		String requestMethod = this.getRequestContext().getMethodTypeCtx();
		if(requestMethod == RequestContext.METHOD_GET) {
			if(queryArg == "add") {
				this.postForm = new FormPanel();
				this.postForm.setAction(RequestContext.getServerUrl() + "add_screening");
				this.postForm.setEncoding(FormPanel.ENCODING_MULTIPART);
				this.postForm.setMethod(FormPanel.METHOD_POST);
				this.displayHtml = new HTMLPanel(screeningsAddHtml);
				this.postForm.add(this.displayHtml);
				super.setContentPanel(this.postForm);
				super.setContentClassName("colM");
				this.fillSubmitControls();
			}else {
				this.displayHtml = new HTMLPanel(screeningsListHtml);
				super.setContentPanel(this.displayHtml);
				super.setContentClassName("flex");
			}
		}
		super.fill();
		fillUserDefined();
	}
	
	@Override
	public void fillSubmitControls() {
		if(this.getRequestContext().getMethodTypeCtx() == RequestContext.METHOD_GET) {
			Button b = new Button("Save");
		    b.setStyleName("button default");
		    b.addClickHandler(new ClickHandler() {
				public void onClick(ClickEvent event) {
					Regions region = new Regions(new RequestContext(RequestContext.METHOD_POST, 
														   getPostForm()));
					region.response();
				}
		    });
			super.setSubmitControlsPanel(b);
			super.fillSubmitControls();
		}
	}
	
	// Fill ids:  data-rows
	final static private String screeningsListFormHtml = "<div class='actions'>" +
						"<label>Action: <select name='action'>" +
							"<option value='' selected='selected'>---------</option>" +
							"<option value='delete_selected'>Delete selected screenings</option>" +
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
						"<tbody>" +
							"<div id='data-rows'" +       // Insert data rows here
							"</div>" +
						"</tbody>" +
					"</table>";

	// Fill ids:  listing-form-body, add-link
	final static private String screeningsListHtml = "<h1>Select screening to change</h1>" +
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
			"</div>";
	
	
	final static private String screeningsAddHtml = "<h1>Add Screening</h1>" +
			"<div id='content-main'>" +
			"<div>" +
			"<fieldset class='module aligned '>" +
			"<div class='form-row date  '>" +
			"<div>" +
			"<label for='id_date' class='required'>Date:</label><input id='id_date' type='text' class='vDateField' name='date' size='10' />" +
			"</div>" +
			"</div>" +
			"<div class='form-row start_time  '>" +
			"<div>" +
			"<label for='id_start_time' class='required'>Start time:</label><input id='id_start_time' type='text' class='vTimeField' name='start_time' size='8' />" +
			"</div>" +
			"</div>" +
			"<div class='form-row end_time  '>" +
			"<div>" +
			"<label for='id_end_time' class='required'>End time:</label><input id='id_end_time' type='text' class='vTimeField' name='end_time' size='8' />" +
			"</div>" +
			"</div>" +
			"<div class='form-row location  '>" +
			"<div>" +
			"<label for='id_location'>Location:</label><input id='id_location' type='text' class='vTextField' name='location' maxlength='200' />" +
			"</div>" +
			"</div>" +
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
			" $('#del_village').show()" +
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
			"<div class='form-row animator  '>" +
			"<div>" +
			"<label for='id_animator' class='required'>Animator:</label><select disabled='true' name='animator' id='id_animator'>" +
			"<option value='' selected='selected'>---------</option>" +
			"</select>" +
			"</div>" +
			"</div>" +
			"<div class='form-row videoes_screened  '>" +
			"<div>" +
			"<label for='id_videoes_screened' class='required'>Videoes screened:</label><select multiple='multiple' name='videoes_screened' id='id_videoes_screened'>" +
			"</select><script type='text/javascript'>addEvent(window, 'load', function(e) {SelectFilter.init('id_videoes_screened', 'videoes screened', 0, '/media/'); });</script>" +
			"<a href='/admin/dashboard/video/add/' class='add-another' id='add_id_videoes_screened' onclick='return showAddAnotherPopup(this);'> <img src='/media/img/admin/icon_addlink.gif' width='10' height='10' alt='Add Another'/></a>" +
			"<p class='help'> Hold down 'Control', or 'Command' on a Mac, to select more than one.</p>" +
			"</div>" +
			"</div>" +
			"<div class='form-row target_person_attendance  '>" +
			"<div>" +
			"<label for='id_target_person_attendance'>Target person attendance:</label><input id='id_target_person_attendance' type='text' class='vIntegerField' name='target_person_attendance' />" +
			"</div>" +
			"</div>" +
			"<div class='form-row target_audience_interest  '>" +
			"<div>" +
			"<label for='id_target_audience_interest'>Target audience interest:</label><input id='id_target_audience_interest' type='text' class='vIntegerField' name='target_audience_interest' />" +
			"</div>" +
			"</div>" +
			"<div class='form-row target_adoptions  '>" +
			"<div>" +
			"<label for='id_target_adoptions'>Target adoptions:</label><input id='id_target_adoptions' type='text' class='vIntegerField' name='target_adoptions' />" +
			"</div>" +
			"</div>" +
			"<div class='form-row fieldofficer  '>" +
			"<div>" +
			"<label for='id_fieldofficer'>Fieldofficer:</label><select name='fieldofficer' id='id_fieldofficer'>" +
			"<option value='' selected='selected'>---------</option>" +
			"</select><a href='/admin/dashboard/fieldofficer/add/' class='add-another' id='add_id_fieldofficer' onclick='return showAddAnotherPopup(this);'> <img src='/media/img/admin/icon_addlink.gif' width='10' height='10' alt='Add Another'/></a>" +
			"</div>" +
			"</div>" +
			"<div class='form-row farmer_groups_targeted  '>" +
			"<div>" +
			"<label for='id_farmer_groups_targeted' class='required'>Farmer groups targeted:</label><select multiple='multiple' onchange='filter_person();' name='farmer_groups_targeted' id='id_farmer_groups_targeted'>" +
			"</select>" +
			"</div>" +
			"</div>" +
			"</fieldset>" +
			"<div class='inline-group'>" +
			"<div class='tabular inline-related last-related'>" +
			"<input type='hidden' name='personmeetingattendance_set-TOTAL_FORMS' value='2' id='id_personmeetingattendance_set-TOTAL_FORMS' />" +
			"<input type='hidden' name='personmeetingattendance_set-INITIAL_FORMS' value='0' id='id_personmeetingattendance_set-INITIAL_FORMS' />" +
			"<fieldset class='module'>" +
			"<h2>Person meeting attendances</h2>" +
			"<table>" +
			"<thead><tr>" +
			"<th colspan='2'>Person</th>" +
			"<th >Expressed interest practice</th>" +
			"<th >Expressed interest</th>" +
			"<th >Expressed adoption practice</th>" +
			"<th >Expressed adoption</th>" +
			"<th >Expressed question practice</th>" +
			"<th >Expressed question</th>" +
			"<th>Delete?</th>" +
			"</tr></thead>" +
			"<tbody>" +
			"<tr class='row1 '>" +
			"<td class='original'>" +
			"<input type='hidden' name='personmeetingattendance_set-0-id' id='id_personmeetingattendance_set-0-id' />" +
			"<input type='hidden' name='personmeetingattendance_set-0-screening' id='id_personmeetingattendance_set-0-screening' />" +
			"</td>" +
			"<td class='person'>" +
			"<select name='personmeetingattendance_set-0-person' id='id_personmeetingattendance_set-0-person'>" +
			"<option value='' selected='selected'>---------</option>" +
			"</select><a href='/admin/dashboard/person/add/' class='add-another' id='add_id_personmeetingattendance_set-0-person' onclick='return showAddAnotherPopup(this);'> <img src='/media/img/admin/icon_addlink.gif' width='10' height='10' alt='Add Another'/></a>" +
			"</td>" +
			"<td class='expressed_interest_practice'>" +
			"<select name='personmeetingattendance_set-0-expressed_interest_practice' id='id_personmeetingattendance_set-0-expressed_interest_practice'>" +
			"<option value='' selected='selected'>---------</option>" +
			"</select><a href='/admin/dashboard/practices/add/' class='add-another' id='add_id_personmeetingattendance_set-0-expressed_interest_practice' onclick='return showAddAnotherPopup(this);'> <img src='/media/img/admin/icon_addlink.gif' width='10' height='10' alt='Add Another'/></a>" +
			"</td>" +
			"<td class='expressed_interest'>" +
			"<input id='id_personmeetingattendance_set-0-expressed_interest' type='text' class='vTextField' name='personmeetingattendance_set-0-expressed_interest' maxlength='500' />" +
			"</td>" +
			"<td class='expressed_adoption_practice'>" +
			"<select name='personmeetingattendance_set-0-expressed_adoption_practice' id='id_personmeetingattendance_set-0-expressed_adoption_practice'>" +
			"<option value='' selected='selected'>---------</option>" +
			"</select><a href='/admin/dashboard/practices/add/' class='add-another' id='add_id_personmeetingattendance_set-0-expressed_adoption_practice' onclick='return showAddAnotherPopup(this);'> <img src='/media/img/admin/icon_addlink.gif' width='10' height='10' alt='Add Another'/></a>" +
			"</td>" +
			"<td class='expressed_adoption'>" +
			"<input id='id_personmeetingattendance_set-0-expressed_adoption' type='text' class='vTextField' name='personmeetingattendance_set-0-expressed_adoption' maxlength='500' />" +
			"</td>" +
			"<td class='expressed_question_practice'>" +
			"<select name='personmeetingattendance_set-0-expressed_question_practice' id='id_personmeetingattendance_set-0-expressed_question_practice'>" +
			"<option value='' selected='selected'>---------</option>" +
			"</select><a href='/admin/dashboard/practices/add/' class='add-another' id='add_id_personmeetingattendance_set-0-expressed_question_practice' onclick='return showAddAnotherPopup(this);'> <img src='/media/img/admin/icon_addlink.gif' width='10' height='10' alt='Add Another'/></a>" +
			"</td>" +
			"<td class='expressed_question'>" +
			"<input id='id_personmeetingattendance_set-0-expressed_question' type='text' class='vTextField' name='personmeetingattendance_set-0-expressed_question' maxlength='500' />" +
			"</td>" +
			"<td class='delete'>" +
			"</td>" +
			"</tr>" +
			"<tr class='row2 '>" +
			"<td class='original'>" +
			"<input type='hidden' name='personmeetingattendance_set-1-id' id='id_personmeetingattendance_set-1-id' />" +
			"<input type='hidden' name='personmeetingattendance_set-1-screening' id='id_personmeetingattendance_set-1-screening' />" +
			"</td>" +
			"<td class='person'>" +
			"<select name='personmeetingattendance_set-1-person' id='id_personmeetingattendance_set-1-person'>" +
			"<option value='' selected='selected'>---------</option>" +
			"</select><a href='/admin/dashboard/person/add/' class='add-another' id='add_id_personmeetingattendance_set-1-person' onclick='return showAddAnotherPopup(this);'> <img src='/media/img/admin/icon_addlink.gif' width='10' height='10' alt='Add Another'/></a>" +
			"</td>" +
			"<td class='expressed_interest_practice'>" +
			"<select name='personmeetingattendance_set-1-expressed_interest_practice' id='id_personmeetingattendance_set-1-expressed_interest_practice'>" +
			"<option value='' selected='selected'>---------</option>" +
			"</select><a href='/admin/dashboard/practices/add/' class='add-another' id='add_id_personmeetingattendance_set-1-expressed_interest_practice' onclick='return showAddAnotherPopup(this);'> <img src='/media/img/admin/icon_addlink.gif' width='10' height='10' alt='Add Another'/></a>" +
			"</td>" +
			"<td class='expressed_interest'>" +
			"<input id='id_personmeetingattendance_set-0-expressed_interest' type='text' class='vTextField' name='personmeetingattendance_set-0-expressed_interest' maxlength='500' />" +
			"</td>" +
			"<td class='expressed_adoption_practice'>" +
			"<select name='personmeetingattendance_set-0-expressed_adoption_practice' id='id_personmeetingattendance_set-0-expressed_adoption_practice'>" +
			"<option value='' selected='selected'>---------</option>" +
			"</select><a href='/admin/dashboard/practices/add/' class='add-another' id='add_id_personmeetingattendance_set-0-expressed_adoption_practice' onclick='return showAddAnotherPopup(this);'> <img src='/media/img/admin/icon_addlink.gif' width='10' height='10' alt='Add Another'/></a>" +
			"</td>" +
			"<td class='expressed_adoption'>" +
			"<input id='id_personmeetingattendance_set-0-expressed_adoption' type='text' class='vTextField' name='personmeetingattendance_set-0-expressed_adoption' maxlength='500' />" +
			"</td>" +
			"<td class='expressed_question_practice'>" +
			"<select name='personmeetingattendance_set-0-expressed_question_practice' id='id_personmeetingattendance_set-0-expressed_question_practice'>" +
			"<option value='' selected='selected'>---------</option>" +
			"</select><a href='/admin/dashboard/practices/add/' class='add-another' id='add_id_personmeetingattendance_set-0-expressed_question_practice' onclick='return showAddAnotherPopup(this);'> <img src='/media/img/admin/icon_addlink.gif' width='10' height='10' alt='Add Another'/></a>" +
			"</td>" +
			"<td class='expressed_question'>" +
			"<input id='id_personmeetingattendance_set-0-expressed_question' type='text' class='vTextField' name='personmeetingattendance_set-0-expressed_question' maxlength='500' />" +
			"</td>" +
			"<td class='delete'>" +
			"</td>" +
			"</tr>" +
			"</tbody>" +
			"</table>" +
			"</fieldset>" +
			"</div>" +
			"</div>" +
			"<script type='text/javascript'>document.getElementById('id_date').focus();</script>" +
			"<script type='text/javascript'>" +
			"</script>" +
			"</div>" +
			"</div><script type='text/javascript' src='/media/js/dynamic_inlines_with_sort.js'></script>" +
			"</div>";
}
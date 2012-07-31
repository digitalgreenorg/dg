package com.digitalgreen.dashboardgwt.client.templates;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.BaseData;
import com.digitalgreen.dashboardgwt.client.data.PersonAdoptPracticeData;
import com.digitalgreen.dashboardgwt.client.data.PersonMeetingAttendanceData;
import com.digitalgreen.dashboardgwt.client.data.ScreeningsData;
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
	public ScreeningsTemplate(RequestContext requestContext) {
		super(requestContext);
		ArrayList personMeetingAttendanceData = new ArrayList();
		personMeetingAttendanceData.add((new PersonMeetingAttendanceData()).getNewData());
		this.formTemplate = new Form((new ScreeningsData()).getNewData(),
				new Object[] {personMeetingAttendanceData});
	}
		
	@Override
	public void fill() {
		String templateType = "Screening";
		String templatePlainType = "dashboard/screening/add/";
		RequestContext requestContext = new RequestContext();
		HashMap args = new HashMap();
		args.put("action", "add");
		requestContext.setArgs(args);
		requestContext.setForm(this.formTemplate);
		Screenings addScreeningServlet = new Screenings(requestContext);
		RequestContext saveRequestContext = new RequestContext(RequestContext.METHOD_POST);
		saveRequestContext.setForm(this.formTemplate);
		Screenings saveScreening = new Screenings(saveRequestContext);
		// Draw the content of the template depending on the request type (GET/POST)
		
		
		super.fillDGTemplate(templateType, screeningsListHtml, screeningsAddHtml, addDataToElementID);
		//Now add listings
		List<Hyperlink> links =  this.fillListings();
		// Add it to the rootpanel
		super.fill();
		
		// Now add hyperlinks
		super.fillDgListPage(templatePlainType, templateType, screeningsListFormHtml, addScreeningServlet, links);
		// Now add any submit control buttons
		this.displayCalendar();
		super.fillDgFormPage(saveScreening);	
		if(!this.getRequestContext().getArgs().get("action").equals("list")) {
			String id ="0";
			if(this.requestContext.getArgs().get("action").equals("edit")) {
				id = (String) this.requestContext.getArgs().get("id");
			}
			ScreeningsTemplate.loadPerson(id);
		}
	}
	
	public List<Hyperlink> fillListings(){
		HashMap queryArgs = this.getRequestContext().getArgs();
		String queryArg = (String)queryArgs.get("action");
		List<Hyperlink> links = new ArrayList<Hyperlink>();
		// If we're unsure, just default to list view
		if(queryArg.equals("list")) {
			// 	Add Listings
			List screenings = (List)queryArgs.get("listing");			
			if(screenings  != null){
				String tableRows ="";
				String style;
				ScreeningsData.Data screening;
				RequestContext requestContext = null;
				for (int row = 0; row <screenings.size(); ++row) {
					if(row%2==0)
						style= "row2";
					else
						style = "row1";
					screening = (ScreeningsData.Data) screenings.get(row);
					requestContext = new RequestContext();
					requestContext.getArgs().put("action", "edit");
					requestContext.getArgs().put("id", screening.getId());
					requestContext.setForm(this.formTemplate);
					links.add(this.createHyperlink("<a href='#dashboard/screening/"+ screening.getId() +"/'>" +
							screening.getDate() + "</a>", "dashboard/screening/"+ screening.getId() +"/", new Screenings(requestContext)));
					tableRows += "<tr class='" +style+ "'>" +
								  "<td><input type='checkbox' class='action-select' value='"+ screening.getId() + "' name='_selected_action' /></td>" +
								  "<th id = 'row" + row + "'></th>" + 
									"<td>"+ screening.getVillage().getVillageName() + "</td>"+
									"<td>"+ screening.getLocation()+"</td>" +
								"</tr>";
				}
				screeningsListFormHtml = screeningsListFormHtml + tableRows + "</tbody></table>";
			}
		}
		return links;
	}
	
	public static native void loadPerson(String id) /*-{
			$wnd.screening_page_offline.init(id);
	}-*/;
	
	//Loading javascript for displaying calendar in Google chrome browser
	public static native void displayCalendar() /*-{
		$wnd.DateTimeShortcuts.init();		
	}-*/;
	
	final private String addDataToElementID[] = {"id_village", "id_animator", "id_videoes_screened", "id_fieldofficer", "id_farmer_groups_targeted"};
	
	// Fill ids:  data-rows
	private String screeningsListFormHtml = "<div class = 'toolbar'><label for='searchbar'>" +
							"<img alt='Search' src='/media/img/admin/icon_searchbox.png'></label>" +
							"<input type='text' id='searchbar' value='' name='q' size='40'>" +
							"<input id='search' type='button' value='Search'>" +
						"</div>"+
						"<div class='actions'>" +
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
						"<tbody>";

	// Fill ids:  listing-form-body, add-link
	final private String screeningsListHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
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
	
	public static native void callScreeningFilter(String queryString) /*-{
			$wnd.init(queryString);
	}-*/;
	
	final private String screeningsAddHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
							"<link href='/media/css/screening_page.css' type='text/css' media='all' rel='stylesheet' />" +
							//"<script src='/media/coco/dashboardgwt/gears_init.js' type='text/javascript'></script>"+
							//"<script src='/media/js/jquery.js' type='text/javascript'></script>" +
							"<div id='content' class='colM'>" +
							"<h1>Add screening</h1>" +
						    "<div id='content-main'>" +
								"<fieldset class='module aligned '>" +
									"<div class='form-row date  '>" +
										"<div>" +
											"<label for='id_date' class='required'>Date:</label>" +
											"<input id='id_date' type='text' class='vDateField' name='date' size='10' />" +
										"</div>" +
									"</div>" +
									"<div class='form-row start_time  '>" +
										"<div>" +
											"<label for='id_start_time' class='required'>Start time:</label>" +
											"<input id='id_start_time' type='text' class='vTimeField' name='start_time' size='8' />" +
										"</div>" +
									"</div>" +
									"<div class='form-row end_time  '>" +
										"<div>" +
											"<label for='id_end_time' class='required'>End time:</label>" +
											"<input id='id_end_time' type='text' class='vTimeField' name='end_time' size='8' />" +
										"</div>" +
									"</div>" +
									"<div class='form-row location  '>" +
										"<div>" +
											"<label for='id_location'>Location:</label>" +
											"<input id='id_location' type='text' class='vTextField' name='location' maxlength='200' />" +
										"</div>" +
									"</div>" +
									"<div class='form-row village  '>" +
										"<div>" +
											"<label for='id_village' class='required'>Village:</label>"+
											"<select name='village' id='id_village'>" +
												"<option value='' selected='selected'>---------</option>" +
											"</select>" +
/*											
											"<input type='hidden' name='village' id='id_village' />" +
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
											"filter();" +
												"}" +
											"});" +
											"$('#del_village').click(function(ele, event) {" +
												"$('#id_village').val('');" +
												"$('#del_village').hide();" +
												"$('#lookup_village').val('');" +
											"});" +
										"</script>" +
*/											
										"</div>" +
									"</div>" +
									"<div class='form-row animator  '>" +
										"<div>" +
											"<label for='id_animator' class='required'>Animator:</label>" +
											"<select name='animator' id='id_animator'>" +
												"<option value='' selected='selected'>---------</option>" +
											"</select>" +
										"</div>" +
									"</div>" +
									"<div class='form-row videoes_screened  '>" +
										"<div>" +
											"<label for='id_videoes_screened' class='required'>Videoes screened:</label>" +
											"<select multiple='multiple' name='videoes_screened' id='id_videoes_screened'>" +
											"</select>" +
											//"<script type='text/javascript'>addEvent(window, 'load', function(e) {SelectFilter.init('id_videoes_screened', 'videoes screened', 0, '/media/'); });" +
											//"</script>" +
											"</a>" +
											"<p class='help'> Hold down 'Control', or 'Command' on a Mac, to select more than one.</p>" +
										"</div>" +
									"</div>" +
									"<div class='form-row fieldofficer  '>" +
										"<div>" +
											"<label for='id_fieldofficer'>Fieldofficer:</label>" +
											"<select name='fieldofficer' id='id_fieldofficer'>" +
												"<option value='' selected='selected'>---------</option>" +
											"</select>" +
											"</a>" +
										"</div>" +
									"</div>" +
									"<div class='form-row farmer_groups_targeted  '>" +
										"<div>" +
											"<label for='id_farmer_groups_targeted' class='required'>Farmer groups targeted:</label>" +
											//"<select multiple='multiple' onchange='filter_person();' name='farmer_groups_targeted' id='id_farmer_groups_targeted'>" +
											"<select id='id_farmer_groups_targeted' name='farmer_groups_targeted' multiple='multiple'>" +
											"</select>" +
										"</div>" +
									"</div>" +
								"</fieldset>" +
								"<div class='inline-group'>" +
									"<div class='tabular inline-related last-related'>" +
										"<input type='hidden' name='personmeetingattendance_set-TOTAL_FORMS' value='0' id='id_personmeetingattendance_set-TOTAL_FORMS' />" +
										"<input type='hidden' name='personmeetingattendance_set-INITIAL_FORMS' value='0' id='id_personmeetingattendance_set-INITIAL_FORMS' />" +
										"<fieldset class='module'>" +
											"<h2>Person meeting attendances</h2>" +
											"<table>" +
												"<thead>" +
													"<tr>" +
														"<th>Delete?</th>" +
														"<th>Sr No.</th>" +
														"<th >Person</th>" +
														"<th >Expressed Adopted Video</th>" +
														"<th >Question Asked</th>" +
														"<th >Interested?</th>" +
													"</tr>" +
												"</thead>" +
											"</table>" +
										"</fieldset>" +
									"</div>" +
								"</div>" +
								"<div class='submit-row' >" +
									"<input id='save' type='button' value='Save' class='default' name='_save' />" +
								"</div>" +
								"<script type='text/javascript'>document.getElementById('id_date').focus();</script>" +
							"</div>" +
							"<br class='clear' />" +
						"</div>"  ;
}
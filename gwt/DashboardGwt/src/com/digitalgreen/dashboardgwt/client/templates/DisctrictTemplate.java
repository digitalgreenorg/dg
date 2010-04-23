package com.digitalgreen.dashboardgwt.client.templates;

import java.util.HashMap;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.servlets.Districts;

public class DisctrictTemplate extends BaseTemplate{
	
	public DisctrictTemplate(RequestContext requestContext) {
		super(requestContext);
	}
	
	@Override
	public void fill() {
		String templateType = "District";
		String templatePlainType = "dashboard/district/add/";
		RequestContext requestContext = new RequestContext();
		HashMap args = new HashMap();
		args.put("action", "add");
		requestContext.setArgs(args);
		Districts addDistrictsServlet = new Districts(requestContext);
		Districts saveDistrict = new Districts(new RequestContext(RequestContext.METHOD_POST));
		// Draw the content of the template depending on the request type (GET/POST)
		super.fillDGTemplate(templateType, districtListHtml, districtAddHtml, addDataToElementID);
		// Add it to the rootpanel
		super.fill();
		// Now add hyperlinks
		super.fillDgListPage(templatePlainType, templateType, districtListFormHtml, addDistrictsServlet);
		// Now add any submit control buttons
		super.fillDgFormPage(saveDistrict);
	}

	final private String addDataToElementID[] = null;
	
	final static private String districtListFormHtml = "<div class='actions'>" +
								"<label>Action: <select name='action'>" +
									"<option value='' selected='selected'>---------</option>" +
									"<option value='delete_selected'>Delete selected districts</option>" +
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
												"District name" +
											"</a>" +
										"</th>" +
										"<th>" +
											"<a href='?ot=asc&amp;o=2'>" +
												"State" +
											"</a>" +
										"</th>" +
										"<th>" +
											"<a href='?ot=asc&amp;o=3'>" +
												"Fieldofficer" +
											"</a>" +
										"</th>" +
										"<th>" +
											"<a href='?ot=asc&amp;o=4'>" +
												"Partner" +
											"</a>" +
										"</th>" +
									"</tr>" +
								"</thead>" +
								"<tbody>" +
									"<div id='data-rows'" +       // Insert data rows here
									"</div>" +
								"</tbody>" +
							"</table>";
	
	final static private String districtListHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
								"<div id='content' class='flex'>" +
									"<h1>Select region to change</h1>" +
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
	
	final static private String districtAddHtml =  "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
						"<div id='content' class='colM'>" +
						"<h1>Add district</h1>" +
							"<div id='content-main'>" +
								"<form enctype='multipart/form-data' action='' method='post' id='district_form'>" +
									"<div>" +
										"<fieldset class='module aligned '>" +
											"<div class='form-row district_name  '>" +
												"<div>" +
													"<label for='id_district_name' class='required'>District name:</label><input id='id_district_name' type='text' class='vTextField' name='district_name' maxlength='100' />" +
												"</div>" +
											"</div>" +
											"<div class='form-row start_date  '>" +
												"<div>" +
													"<label for='id_start_date'>Start date:</label><input id='id_start_date' type='text' class='vDateField' name='start_date' size='10' />" +
													"<span>&nbsp;" +
														"<a href='javascript:DateTimeShortcuts.handleCalendarQuickLink(0, 0);'>Today</a>&nbsp;|&nbsp;" +
														"<a href='javascript:DateTimeShortcuts.openCalendar(0);' id='calendarlink0'>" +
														"<img src='/media/img/admin/icon_calendar.gif' alt='Calendar'></a>" +
													"</span>" +
												"</div>" +
											"</div>" +
											"<div class='form-row state  '>" +
												"<div>" +
													"<label for='id_state' class='required'>State:</label><select name='state' id='id_state'>" +
														"<option value='' selected='selected'>---------</option>" +
													"</select>" +
													"</div>" +
											"</div>" +
											"<div class='form-row fieldofficer  '>" +
												"<div>" +
													"<label for='id_fieldofficer' class='required'>Fieldofficer:</label><select name='fieldofficer' id='id_fieldofficer'>" +
														"<option value='' selected='selected'>---------</option>" +
													"</select>" +
												"</div>" +
											"</div>" +
											"<div class='form-row fieldofficer_startday  '>" +
												"<div>" +
													"<label for='id_fieldofficer_startday'>Fieldofficer startday:</label><input id='id_fieldofficer_startday' type='text' class='vDateField' name='fieldofficer_startday' size='10' />" +
													"<span>&nbsp;" +
														"<a href='javascript:DateTimeShortcuts.handleCalendarQuickLink(0, 0);'>Today</a>&nbsp;|&nbsp;" +
														"<a href='javascript:DateTimeShortcuts.openCalendar(0);' id='calendarlink0'>" +
														"<img src='/media/img/admin/icon_calendar.gif' alt='Calendar'></a>" +
													"</span>" +
												"</div>" +
											"</div>" +
											"<div class='form-row partner  '>" +
												"<div>" +
													"<label for='id_partner' class='required'>Partner:</label><select name='partner' id='id_partner'>" +
														"<option value='' selected='selected'>---------</option>" +
													"</select>" +
												"</div>" +
											"</div>" +
										"</fieldset>" +
										"<div class='submit-row' >" +
											"<input type='submit' value='Save' class='default' name='_save' />" +
										"</div>" +
										"<script type='text/javascript'>document.getElementById('id_district_name').focus();</script>" +
										"<script type='text/javascript'>" +
										"</script>" +
									"</div>" +
								"</form>" +
							"</div>" +
						"</div>";
}
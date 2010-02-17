package com.digitalgreen.dashboardgwt.client.templates;

public class PersonGroupsTemplate {
	
	final static private String persongroupsListFormHtml = "<div class='actions'>" +
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
									"<tbody>" +
										"<div id='data-rows'" +       // Insert data rows here
										"</div>" +
									"</tbody>" +
								"</table>";
	
	final static private String persongroupsListHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
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
	
	final static private String persongroupsAddHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
								"<div id='content' class='colM'>" +
									"<h1>Add Person group</h1>" +
									"<div id='content-main'>" +
										"<form enctype='multipart/form-data' action='' method='post' id='persongroups_form'>" +
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
															"</select><a href='/admin/dashboard/village/add/' class='add-another' id='add_id_village' onclick='return showAddAnotherPopup(this);'> <img src='/media/img/admin/icon_addlink.gif' width='10' height='10' alt='Add Another'/></a>" +
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
																		"</select><a href='/admin/dashboard/village/add/' class='add-another' id='add_id_person_set-0-village' onclick='return showAddAnotherPopup(this);'> <img src='/media/img/admin/icon_addlink.gif' width='10' height='10' alt='Add Another'/></a>" +
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
																		"</select><a href='/admin/dashboard/village/add/' class='add-another' id='add_id_person_set-1-village' onclick='return showAddAnotherPopup(this);'> <img src='/media/img/admin/icon_addlink.gif' width='10' height='10' alt='Add Another'/></a>" +
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
																		"</select><a href='/admin/dashboard/village/add/' class='add-another' id='add_id_person_set-2-village' onclick='return showAddAnotherPopup(this);'> <img src='/media/img/admin/icon_addlink.gif' width='10' height='10' alt='Add Another'/></a>" +
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
																		"</select><a href='/admin/dashboard/village/add/' class='add-another' id='add_id_person_set-3-village' onclick='return showAddAnotherPopup(this);'> <img src='/media/img/admin/icon_addlink.gif' width='10' height='10' alt='Add Another'/></a>" +
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
																		"</select><a href='/admin/dashboard/village/add/' class='add-another' id='add_id_person_set-4-village' onclick='return showAddAnotherPopup(this);'> <img src='/media/img/admin/icon_addlink.gif' width='10' height='10' alt='Add Another'/></a>" +
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
																		"</select><a href='/admin/dashboard/village/add/' class='add-another' id='add_id_person_set-5-village' onclick='return showAddAnotherPopup(this);'> <img src='/media/img/admin/icon_addlink.gif' width='10' height='10' alt='Add Another'/></a>" +
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
																		"</select><a href='/admin/dashboard/village/add/' class='add-another' id='add_id_person_set-6-village' onclick='return showAddAnotherPopup(this);'> <img src='/media/img/admin/icon_addlink.gif' width='10' height='10' alt='Add Another'/></a>" +
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
																		"</select><a href='/admin/dashboard/village/add/' class='add-another' id='add_id_person_set-7-village' onclick='return showAddAnotherPopup(this);'> <img src='/media/img/admin/icon_addlink.gif' width='10' height='10' alt='Add Another'/></a>" +
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
																		"</select><a href='/admin/dashboard/village/add/' class='add-another' id='add_id_person_set-8-village' onclick='return showAddAnotherPopup(this);'> <img src='/media/img/admin/icon_addlink.gif' width='10' height='10' alt='Add Another'/></a>" +
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
																		"</select><a href='/admin/dashboard/village/add/' class='add-another' id='add_id_person_set-9-village' onclick='return showAddAnotherPopup(this);'> <img src='/media/img/admin/icon_addlink.gif' width='10' height='10' alt='Add Another'/></a>" +
																	"</td>" +
																	"<td class='delete'></td>" +
																"</tr>" +

																"<tr class='row1 '>" +							////////////////////////////////////////////////11
																	"<td class='original'>" +
																		"<input type='hidden' name='person_set-10-id' id='id_person_set-10-id' />" +
																		"<input type='hidden' name='person_set-10-group' id='id_person_set-10-group' />" +
																	"</td>" +
																	"<td class='person_name'>" +
																		"<input id='id_person_set-10-person_name' type='text' class='vTextField' name='person_set-10-person_name' maxlength='100' />" +
																	"</td>" +
																	"<td class='father_name'>" +
																		"<input id='id_person_set-10-father_name' type='text' class='vTextField' name='person_set-10-father_name' maxlength='100' />" +
																	"</td>" +
																	"<td class='age'>" +
																		"<input id='id_person_set-10-age' type='text' class='vIntegerField' name='person_set-10-age' />" +
																	"</td>" +
																	"<td class='gender'>" +
																		"<select name='person_set-10-gender' id='id_person_set-10-gender'>" +
																			"<option value='' selected='selected'>---------</option>" +
																			"<option value='M'>Male</option>" +
																			"<option value='F'>Female</option>" +
																		"</select>" +
																	"</td>" +
																	"<td class='phone_no'>" +
																		"<input id='id_person_set-10-phone_no' type='text' class='vTextField' name='person_set-10-phone_no' maxlength='100' />" +
																	"</td>" +
																	"<td class='address'>" +
																		"<input id='id_person_set-10-address' type='text' class='vTextField' name='person_set-10-address' maxlength='500' />" +
																	"</td>" +
																	"<td class='land_holdings'>" +
																		"<input id='id_person_set-10-land_holdings' type='text' class='vIntegerField' name='person_set-10-land_holdings' />" +
																	"</td>" +
																	"<td class='village'>" +
																		"<select name='person_set-10-village' id='id_person_set-10-village'>" +
																			"<option value='' selected='selected'>---------</option>" +
																		"</select><a href='/admin/dashboard/village/add/' class='add-another' id='add_id_person_set-10-village' onclick='return showAddAnotherPopup(this);'> <img src='/media/img/admin/icon_addlink.gif' width='10' height='10' alt='Add Another'/></a>" +
																	"</td>" +
																	"<td class='delete'></td>" +
																"</tr>" +

																"<tr class='row2 '>" +							////////////////////////////////////////////////12
																	"<td class='original'>" +
																		"<input type='hidden' name='person_set-11-id' id='id_person_set-11-id' />" +
																		"<input type='hidden' name='person_set-11-group' id='id_person_set-11-group' />" +
																	"</td>" +
																	"<td class='person_name'>" +
																		"<input id='id_person_set-11-person_name' type='text' class='vTextField' name='person_set-11-person_name' maxlength='100' />" +
																	"</td>" +
																	"<td class='father_name'>" +
																		"<input id='id_person_set-11-father_name' type='text' class='vTextField' name='person_set-11-father_name' maxlength='100' />" +
																	"</td>" +
																	"<td class='age'>" +
																		"<input id='id_person_set-11-age' type='text' class='vIntegerField' name='person_set-11-age' />" +
																	"</td>" +
																	"<td class='gender'>" +
																		"<select name='person_set-11-gender' id='id_person_set-11-gender'>" +
																			"<option value='' selected='selected'>---------</option>" +
																			"<option value='M'>Male</option>" +
																			"<option value='F'>Female</option>" +
																		"</select>" +
																	"</td>" +
																	"<td class='phone_no'>" +
																		"<input id='id_person_set-11-phone_no' type='text' class='vTextField' name='person_set-11-phone_no' maxlength='100' />" +
																	"</td>" +
																	"<td class='address'>" +
																		"<input id='id_person_set-11-address' type='text' class='vTextField' name='person_set-11-address' maxlength='500' />" +
																	"</td>" +
																	"<td class='land_holdings'>" +
																		"<input id='id_person_set-11-land_holdings' type='text' class='vIntegerField' name='person_set-11-land_holdings' />" +
																	"</td>" +
																	"<td class='village'>" +
																		"<select name='person_set-11-village' id='id_person_set-11-village'>" +
																			"<option value='' selected='selected'>---------</option>" +
																		"</select><a href='/admin/dashboard/village/add/' class='add-another' id='add_id_person_set-11-village' onclick='return showAddAnotherPopup(this);'> <img src='/media/img/admin/icon_addlink.gif' width='10' height='10' alt='Add Another'/></a>" +
																	"</td>" +
																	"<td class='delete'></td>" +
																"</tr>" +

																"<tr class='row1 '>" +							////////////////////////////////////////////////13
																	"<td class='original'>" +
																		"<input type='hidden' name='person_set-12-id' id='id_person_set-12-id' />" +
																		"<input type='hidden' name='person_set-12-group' id='id_person_set-12-group' />" +
																	"</td>" +
																	"<td class='person_name'>" +
																		"<input id='id_person_set-12-person_name' type='text' class='vTextField' name='person_set-12-person_name' maxlength='100' />" +
																	"</td>" +
																	"<td class='father_name'>" +
																		"<input id='id_person_set-12-father_name' type='text' class='vTextField' name='person_set-12-father_name' maxlength='100' />" +
																	"</td>" +
																	"<td class='age'>" +
																		"<input id='id_person_set-12-age' type='text' class='vIntegerField' name='person_set-12-age' />" +
																	"</td>" +
																	"<td class='gender'>" +
																		"<select name='person_set-12-gender' id='id_person_set-12-gender'>" +
																			"<option value='' selected='selected'>---------</option>" +
																			"<option value='M'>Male</option>" +
																			"<option value='F'>Female</option>" +
																		"</select>" +
																	"</td>" +
																	"<td class='phone_no'>" +
																		"<input id='id_person_set-12-phone_no' type='text' class='vTextField' name='person_set-12-phone_no' maxlength='100' />" +
																	"</td>" +
																	"<td class='address'>" +
																		"<input id='id_person_set-12-address' type='text' class='vTextField' name='person_set-12-address' maxlength='500' />" +
																	"</td>" +
																	"<td class='land_holdings'>" +
																		"<input id='id_person_set-12-land_holdings' type='text' class='vIntegerField' name='person_set-12-land_holdings' />" +
																	"</td>" +
																	"<td class='village'>" +
																		"<select name='person_set-12-village' id='id_person_set-12-village'>" +
																			"<option value='' selected='selected'>---------</option>" +
																		"</select><a href='/admin/dashboard/village/add/' class='add-another' id='add_id_person_set-12-village' onclick='return showAddAnotherPopup(this);'> <img src='/media/img/admin/icon_addlink.gif' width='10' height='10' alt='Add Another'/></a>" +
																	"</td>" +
																	"<td class='delete'></td>" +
																"</tr>" +

																"<tr class='row2 '>" +							////////////////////////////////////////////////14
																	"<td class='original'>" +
																		"<input type='hidden' name='person_set-13-id' id='id_person_set-13-id' />" +
																		"<input type='hidden' name='person_set-13-group' id='id_person_set-13-group' />" +
																	"</td>" +
																	"<td class='person_name'>" +
																		"<input id='id_person_set-13-person_name' type='text' class='vTextField' name='person_set-13-person_name' maxlength='100' />" +
																	"</td>" +
																	"<td class='father_name'>" +
																		"<input id='id_person_set-13-father_name' type='text' class='vTextField' name='person_set-13-father_name' maxlength='100' />" +
																	"</td>" +
																	"<td class='age'>" +
																		"<input id='id_person_set-13-age' type='text' class='vIntegerField' name='person_set-13-age' />" +
																	"</td>" +
																	"<td class='gender'>" +
																		"<select name='person_set-13-gender' id='id_person_set-13-gender'>" +
																			"<option value='' selected='selected'>---------</option>" +
																			"<option value='M'>Male</option>" +
																			"<option value='F'>Female</option>" +
																		"</select>" +
																	"</td>" +
																	"<td class='phone_no'>" +
																		"<input id='id_person_set-13-phone_no' type='text' class='vTextField' name='person_set-13-phone_no' maxlength='100' />" +
																	"</td>" +
																	"<td class='address'>" +
																		"<input id='id_person_set-13-address' type='text' class='vTextField' name='person_set-13-address' maxlength='500' />" +
																	"</td>" +
																	"<td class='land_holdings'>" +
																		"<input id='id_person_set-13-land_holdings' type='text' class='vIntegerField' name='person_set-13-land_holdings' />" +
																	"</td>" +
																	"<td class='village'>" +
																		"<select name='person_set-13-village' id='id_person_set-13-village'>" +
																			"<option value='' selected='selected'>---------</option>" +
																		"</select><a href='/admin/dashboard/village/add/' class='add-another' id='add_id_person_set-13-village' onclick='return showAddAnotherPopup(this);'> <img src='/media/img/admin/icon_addlink.gif' width='10' height='10' alt='Add Another'/></a>" +
																	"</td>" +
																	"<td class='delete'></td>" +
																"</tr>" +

																"<tr class='row1 '>" +							////////////////////////////////////////////////15
																	"<td class='original'>" +	
																		"<input type='hidden' name='person_set-14-id' id='id_person_set-14-id' />" +
																		"<input type='hidden' name='person_set-14-group' id='id_person_set-14-group' />" +
																	"</td>" +
																	"<td class='person_name'>" +
																		"<input id='id_person_set-14-person_name' type='text' class='vTextField' name='person_set-14-person_name' maxlength='100' />" +
																	"</td>" +
																	"<td class='father_name'>" +
																		"<input id='id_person_set-14-father_name' type='text' class='vTextField' name='person_set-14-father_name' maxlength='100' />" +
																	"</td>" +
																	"<td class='age'>" +
																		"<input id='id_person_set-14-age' type='text' class='vIntegerField' name='person_set-14-age' />" +
																	"</td>" +
																	"<td class='gender'>" +
																		"<select name='person_set-14-gender' id='id_person_set-14-gender'>" +
																			"<option value='' selected='selected'>---------</option>" +
																			"<option value='M'>Male</option>" +
																			"<option value='F'>Female</option>" +
																		"</select>" +
																	"</td>" +
																	"<td class='phone_no'>" +
																		"<input id='id_person_set-14-phone_no' type='text' class='vTextField' name='person_set-14-phone_no' maxlength='100' />" +
																	"</td>" +
																	"<td class='address'>" +
																		"<input id='id_person_set-14-address' type='text' class='vTextField' name='person_set-14-address' maxlength='500' />" +
																	"</td>" +
																	"<td class='land_holdings'>" +
																		"<input id='id_person_set-14-land_holdings' type='text' class='vIntegerField' name='person_set-14-land_holdings' />" +
																	"</td>" +
																	"<td class='village'>" +
																		"<select name='person_set-14-village' id='id_person_set-14-village'>" +
																			"<option value='' selected='selected'>---------</option>" +
																		"</select><a href='/admin/dashboard/village/add/' class='add-another' id='add_id_person_set-14-village' onclick='return showAddAnotherPopup(this);'> <img src='/media/img/admin/icon_addlink.gif' width='10' height='10' alt='Add Another'/></a>" +
																	"</td>" +
																	"<td class='delete'></td>" +
																"</tr>" +

																"<tr class='row2 '>" +							////////////////////////////////////////////////16
																	"<td class='original'>" +
																		"<input type='hidden' name='person_set-15-id' id='id_person_set-15-id' />" +
																		"<input type='hidden' name='person_set-15-group' id='id_person_set-15-group' />" +
																	"</td>" +
																	"<td class='person_name'>" +
																		"<input id='id_person_set-15-person_name' type='text' class='vTextField' name='person_set-15-person_name' maxlength='100' />" +
																	"</td>" +
																	"<td class='father_name'>" +
																		"<input id='id_person_set-15-father_name' type='text' class='vTextField' name='person_set-15-father_name' maxlength='100' />" +
																	"</td>" +
																	"<td class='age'>" +
																		"<input id='id_person_set-15-age' type='text' class='vIntegerField' name='person_set-15-age' />" +
																	"</td>" +
																	"<td class='gender'>" +
																		"<select name='person_set-15-gender' id='id_person_set-15-gender'>" +
																			"<option value='' selected='selected'>---------</option>" +
																			"<option value='M'>Male</option>" +
																			"<option value='F'>Female</option>" +
																		"</select>" +
																	"</td>" +
																	"<td class='phone_no'>" +
																		"<input id='id_person_set-15-phone_no' type='text' class='vTextField' name='person_set-15-phone_no' maxlength='100' />" +
																	"</td>" +
																	"<td class='address'>" +
																		"<input id='id_person_set-15-address' type='text' class='vTextField' name='person_set-15-address' maxlength='500' />" +
																	"</td>" +
																	"<td class='land_holdings'>" +
																		"<input id='id_person_set-15-land_holdings' type='text' class='vIntegerField' name='person_set-15-land_holdings' />" +
																	"</td>" +
																	"<td class='village'>" +
																		"<select name='person_set-15-village' id='id_person_set-15-village'>" +
																			"<option value='' selected='selected'>---------</option>" +
																		"</select><a href='/admin/dashboard/village/add/' class='add-another' id='add_id_person_set-15-village' onclick='return showAddAnotherPopup(this);'> <img src='/media/img/admin/icon_addlink.gif' width='10' height='10' alt='Add Another'/></a>" +
																	"</td>" +
																	"<td class='delete'></td>" +
																"</tr>" +

																"<tr class='row1 '>" +							////////////////////////////////////////////////17
																	"<td class='original'>" +
																		"<input type='hidden' name='person_set-16-id' id='id_person_set-16-id' />" +
																		"<input type='hidden' name='person_set-16-group' id='id_person_set-16-group' />" +
																	"</td>" +
																	"<td class='person_name'>" +
																		"<input id='id_person_set-16-person_name' type='text' class='vTextField' name='person_set-16-person_name' maxlength='100' />" +
																	"</td>" +
																	"<td class='father_name'>" +
																		"<input id='id_person_set-16-father_name' type='text' class='vTextField' name='person_set-16-father_name' maxlength='100' />" +
																	"</td>" +
																	"<td class='age'>" +
																		"<input id='id_person_set-16-age' type='text' class='vIntegerField' name='person_set-16-age' />" +
																	"</td>" +
																	"<td class='gender'>" +
																		"<select name='person_set-16-gender' id='id_person_set-16-gender'>" +
																			"<option value='' selected='selected'>---------</option>" +
																			"<option value='M'>Male</option>" +
																			"<option value='F'>Female</option>" +
																		"</select>" +
																	"</td>" +
																	"<td class='phone_no'>" +
																		"<input id='id_person_set-16-phone_no' type='text' class='vTextField' name='person_set-16-phone_no' maxlength='100' />" +
																	"</td>" +
																	"<td class='address'>" +
																		"<input id='id_person_set-16-address' type='text' class='vTextField' name='person_set-16-address' maxlength='500' />" +
																	"</td>" +
																	"<td class='land_holdings'>" +
																		"<input id='id_person_set-16-land_holdings' type='text' class='vIntegerField' name='person_set-16-land_holdings' />" +
																	"</td>" +
																	"<td class='village'>" +
																		"<select name='person_set-16-village' id='id_person_set-16-village'>" +
																			"<option value='' selected='selected'>---------</option>" +
																		"</select><a href='/admin/dashboard/village/add/' class='add-another' id='add_id_person_set-16-village' onclick='return showAddAnotherPopup(this);'> <img src='/media/img/admin/icon_addlink.gif' width='10' height='10' alt='Add Another'/></a>" +
																	"</td>" +
																	"<td class='delete'></td>" +
																"</tr>" +

																"<tr class='row2 '>" +							////////////////////////////////////////////////18
																	"<td class='original'>" +
																		"<input type='hidden' name='person_set-17-id' id='id_person_set-17-id' />" +
																		"<input type='hidden' name='person_set-17-group' id='id_person_set-17-group' />" +
																	"</td>" +
																	"<td class='person_name'>" +
																		"<input id='id_person_set-17-person_name' type='text' class='vTextField' name='person_set-17-person_name' maxlength='100' />" +
																	"</td>" +
																	"<td class='father_name'>" +
																		"<input id='id_person_set-17-father_name' type='text' class='vTextField' name='person_set-17-father_name' maxlength='100' />" +
																	"</td>" +
																	"<td class='age'>" +
																		"<input id='id_person_set-17-age' type='text' class='vIntegerField' name='person_set-17-age' />" +
																	"</td>" +
																	"<td class='gender'>" +
																		"<select name='person_set-17-gender' id='id_person_set-17-gender'>" +
																			"<option value='' selected='selected'>---------</option>" +	
																			"<option value='M'>Male</option>" +
																			"<option value='F'>Female</option>" +
																		"</select>" +
																	"</td>" +
																	"<td class='phone_no'>" +
																		"<input id='id_person_set-17-phone_no' type='text' class='vTextField' name='person_set-17-phone_no' maxlength='100' />" +
																	"</td>" +
																	"<td class='address'>" +
																		"<input id='id_person_set-17-address' type='text' class='vTextField' name='person_set-17-address' maxlength='500' />" +
																	"</td>" +
																	"<td class='land_holdings'>" +
																		"<input id='id_person_set-17-land_holdings' type='text' class='vIntegerField' name='person_set-17-land_holdings' />" +
																	"</td>" +
																	"<td class='village'>" +
																		"<select name='person_set-17-village' id='id_person_set-17-village'>" +
																			"<option value='' selected='selected'>---------</option>" +
																		"</select><a href='/admin/dashboard/village/add/' class='add-another' id='add_id_person_set-17-village' onclick='return showAddAnotherPopup(this);'> <img src='/media/img/admin/icon_addlink.gif' width='10' height='10' alt='Add Another'/></a>" +
																	"</td>" +
																	"<td class='delete'></td>" +
																"</tr>" +

																"<tr class='row1 '>" +							////////////////////////////////////////////////19
																	"<td class='original'>" +
																		"<input type='hidden' name='person_set-18-id' id='id_person_set-18-id' />" +
																		"<input type='hidden' name='person_set-18-group' id='id_person_set-18-group' />" +
																	"</td>" +
																	"<td class='person_name'>" +
																		"<input id='id_person_set-18-person_name' type='text' class='vTextField' name='person_set-18-person_name' maxlength='100' />" +
																	"</td>" +
																	"<td class='father_name'>" +
																		"<input id='id_person_set-18-father_name' type='text' class='vTextField' name='person_set-18-father_name' maxlength='100' />" +
																	"</td>" +
																	"<td class='age'>" +
																		"<input id='id_person_set-18-age' type='text' class='vIntegerField' name='person_set-18-age' />" +
																	"</td>" +
																	"<td class='gender'>" +
																		"<select name='person_set-18-gender' id='id_person_set-18-gender'>" +
																			"<option value='' selected='selected'>---------</option>" +
																			"<option value='M'>Male</option>" +
																			"<option value='F'>Female</option>" +
																		"</select>" +
																	"</td>" +
																	"<td class='phone_no'>" +
																		"<input id='id_person_set-18-phone_no' type='text' class='vTextField' name='person_set-18-phone_no' maxlength='100' />" +
																	"</td>" +
																	"<td class='address'>" +
																		"<input id='id_person_set-18-address' type='text' class='vTextField' name='person_set-18-address' maxlength='500' />" +
																	"</td>" +
																	"<td class='land_holdings'>" +
																		"<input id='id_person_set-18-land_holdings' type='text' class='vIntegerField' name='person_set-18-land_holdings' />" +
																	"</td>" +
																	"<td class='village'>" +
																		"<select name='person_set-18-village' id='id_person_set-18-village'>" +
																			"<option value='' selected='selected'>---------</option>" +
																		"</select><a href='/admin/dashboard/village/add/' class='add-another' id='add_id_person_set-18-village' onclick='return showAddAnotherPopup(this);'> <img src='/media/img/admin/icon_addlink.gif' width='10' height='10' alt='Add Another'/></a>" +
																	"</td>" +
																	"<td class='delete'></td>" +
																"</tr>" +

																"<tr class='row2 '>" +							////////////////////////////////////////////////20
																	"<td class='original'>" +
																		"<input type='hidden' name='person_set-19-id' id='id_person_set-19-id' />" +
																		"<input type='hidden' name='person_set-19-group' id='id_person_set-19-group' />" +
																	"</td>" +
																	"<td class='person_name'>" +
																		"<input id='id_person_set-19-person_name' type='text' class='vTextField' name='person_set-19-person_name' maxlength='100' />" +
																	"</td>" +
																	"<td class='father_name'>" +
																		"<input id='id_person_set-19-father_name' type='text' class='vTextField' name='person_set-19-father_name' maxlength='100' />" +
																	"</td>" +
																	"<td class='age'>" +
																		"<input id='id_person_set-19-age' type='text' class='vIntegerField' name='person_set-19-age' />" +
																	"</td>" +
																	"<td class='gender'>" +
																		"<select name='person_set-19-gender' id='id_person_set-19-gender'>" +
																			"<option value='' selected='selected'>---------</option>" +
																			"<option value='M'>Male</option>" +
																			"<option value='F'>Female</option>" +
																		"</select>" +
																	"</td>" +
																	"<td class='phone_no'>" +
																		"<input id='id_person_set-19-phone_no' type='text' class='vTextField' name='person_set-19-phone_no' maxlength='100' />" +
																	"</td>" +
																	"<td class='address'>" +
																		"<input id='id_person_set-19-address' type='text' class='vTextField' name='person_set-19-address' maxlength='500' />" +
																	"</td>" +
																	"<td class='land_holdings'>" +
																		"<input id='id_person_set-19-land_holdings' type='text' class='vIntegerField' name='person_set-19-land_holdings' />" +
																	"</td>" +
																	"<td class='village'>" +
																		"<select name='person_set-19-village' id='id_person_set-19-village'>" +
																			"<option value='' selected='selected'>---------</option>" +
																		"</select><a href='/admin/dashboard/village/add/' class='add-another' id='add_id_person_set-19-village' onclick='return showAddAnotherPopup(this);'> <img src='/media/img/admin/icon_addlink.gif' width='10' height='10' alt='Add Another'/></a>" +
																	"</td>" +
																	"<td class='delete'></td>" +
																"</tr>" +

																"<tr class='row1 '>" +							////////////////////////////////////////////////21
																	"<td class='original'>" +
																		"<input type='hidden' name='person_set-20-id' id='id_person_set-20-id' />" +
																		"<input type='hidden' name='person_set-20-group' id='id_person_set-20-group' />" +
																	"</td>" +
																	"<td class='person_name'>" +
																		"<input id='id_person_set-20-person_name' type='text' class='vTextField' name='person_set-20-person_name' maxlength='100' />" +
																	"</td>" +
																	"<td class='father_name'>" +
																		"<input id='id_person_set-20-father_name' type='text' class='vTextField' name='person_set-20-father_name' maxlength='100' />" +
																	"</td>" +
																	"<td class='age'>" +
																		"<input id='id_person_set-20-age' type='text' class='vIntegerField' name='person_set-20-age' />" +
																	"</td>" +
																	"<td class='gender'>" +
																		"<select name='person_set-20-gender' id='id_person_set-20-gender'>" +
																			"<option value='' selected='selected'>---------</option>" +
																			"<option value='M'>Male</option>" +
																			"<option value='F'>Female</option>" +
																		"</select>" +
																	"</td>" +
																	"<td class='phone_no'>" +
																		"<input id='id_person_set-20-phone_no' type='text' class='vTextField' name='person_set-20-phone_no' maxlength='100' />" +
																	"</td>" +
																	"<td class='address'>" +
																		"<input id='id_person_set-20-address' type='text' class='vTextField' name='person_set-20-address' maxlength='500' />" +
																	"</td>" +
																	"<td class='land_holdings'>" +
																		"<input id='id_person_set-20-land_holdings' type='text' class='vIntegerField' name='person_set-20-land_holdings' />" +
																	"</td>" +
																	"<td class='village'>" +
																		"<select name='person_set-20-village' id='id_person_set-20-village'>" +
																			"<option value='' selected='selected'>---------</option>" +
																		"</select><a href='/admin/dashboard/village/add/' class='add-another' id='add_id_person_set-20-village' onclick='return showAddAnotherPopup(this);'> <img src='/media/img/admin/icon_addlink.gif' width='10' height='10' alt='Add Another'/></a>" +
																	"</td>" +
																	"<td class='delete'></td>" +
																"</tr>" +

																"<tr class='row2 '>" +							////////////////////////////////////////////////22
																	"<td class='original'>" +
																		"<input type='hidden' name='person_set-21-id' id='id_person_set-21-id' />" +
																		"<input type='hidden' name='person_set-21-group' id='id_person_set-21-group' />" +
																	"</td>" +
																	"<td class='person_name'>" +
																		"<input id='id_person_set-21-person_name' type='text' class='vTextField' name='person_set-21-person_name' maxlength='100' />" +
																	"</td>" +
																	"<td class='father_name'>" +
																		"<input id='id_person_set-21-father_name' type='text' class='vTextField' name='person_set-21-father_name' maxlength='100' />" +
																	"</td>" +
																	"<td class='age'>" +
																		"<input id='id_person_set-21-age' type='text' class='vIntegerField' name='person_set-21-age' />" +
																	"</td>" +
																	"<td class='gender'>" +
																		"<select name='person_set-21-gender' id='id_person_set-21-gender'>" +
																			"<option value='' selected='selected'>---------</option>" +
																			"<option value='M'>Male</option>" +
																			"<option value='F'>Female</option>" +
																		"</select>" +
																	"</td>" +
																	"<td class='phone_no'>" +
																		"<input id='id_person_set-21-phone_no' type='text' class='vTextField' name='person_set-21-phone_no' maxlength='100' />" +
																	"</td>" +
																	"<td class='address'>" +
																		"<input id='id_person_set-21-address' type='text' class='vTextField' name='person_set-21-address' maxlength='500' />" +
																	"</td>" +
																	"<td class='land_holdings'>" +
																		"<input id='id_person_set-21-land_holdings' type='text' class='vIntegerField' name='person_set-21-land_holdings' />" +
																	"</td>" +
																	"<td class='village'>" +
																		"<select name='person_set-21-village' id='id_person_set-21-village'>" +
																			"<option value='' selected='selected'>---------</option>" +
																		"</select><a href='/admin/dashboard/village/add/' class='add-another' id='add_id_person_set-21-village' onclick='return showAddAnotherPopup(this);'> <img src='/media/img/admin/icon_addlink.gif' width='10' height='10' alt='Add Another'/></a>" +
																	"</td>" +
																	"<td class='delete'></td>" +
																"</tr>" +

																"<tr class='row1 '>" +							////////////////////////////////////////////////23
																	"<td class='original'>" +
																		"<input type='hidden' name='person_set-22-id' id='id_person_set-22-id' />" +
																		"<input type='hidden' name='person_set-22-group' id='id_person_set-22-group' />" +
																	"</td>" +
																	"<td class='person_name'>" +
																		"<input id='id_person_set-22-person_name' type='text' class='vTextField' name='person_set-22-person_name' maxlength='100' />" +
																	"</td>" +
																	"<td class='father_name'>" +
																		"<input id='id_person_set-22-father_name' type='text' class='vTextField' name='person_set-22-father_name' maxlength='100' />" +
																	"</td>" +
																	"<td class='age'>" +
																		"<input id='id_person_set-22-age' type='text' class='vIntegerField' name='person_set-22-age' />" +
																	"</td>" +
																	"<td class='gender'>" +
																		"<select name='person_set-22-gender' id='id_person_set-22-gender'>" +
																			"<option value='' selected='selected'>---------</option>" +
																			"<option value='M'>Male</option>" +
																			"<option value='F'>Female</option>" +
																		"</select>" +
																	"</td>" +
																	"<td class='phone_no'>" +
																		"<input id='id_person_set-22-phone_no' type='text' class='vTextField' name='person_set-22-phone_no' maxlength='100' />" +
																	"</td>" +
																	"<td class='address'>" +
																		"<input id='id_person_set-22-address' type='text' class='vTextField' name='person_set-22-address' maxlength='500' />" +
																	"</td>" +
																	"<td class='land_holdings'>" +
																		"<input id='id_person_set-22-land_holdings' type='text' class='vIntegerField' name='person_set-22-land_holdings' />" +
																	"</td>" +
																	"<td class='village'>" +
																		"<select name='person_set-22-village' id='id_person_set-22-village'>" +
																			"<option value='' selected='selected'>---------</option>" +
																		"</select><a href='/admin/dashboard/village/add/' class='add-another' id='add_id_person_set-22-village' onclick='return showAddAnotherPopup(this);'> <img src='/media/img/admin/icon_addlink.gif' width='10' height='10' alt='Add Another'/></a>" +
																	"</td>" +
																	"<td class='delete'></td>" +
																"</tr>" +

																"<tr class='row2 '>" +							////////////////////////////////////////////////24
																	"<td class='original'>" +
																		"<input type='hidden' name='person_set-23-id' id='id_person_set-23-id' />" +
																		"<input type='hidden' name='person_set-23-group' id='id_person_set-23-group' />" +
																	"</td>" +
																	"<td class='person_name'>" +
																		"<input id='id_person_set-23-person_name' type='text' class='vTextField' name='person_set-23-person_name' maxlength='100' />" +
																	"</td>" +
																	"<td class='father_name'>" +
																		"<input id='id_person_set-23-father_name' type='text' class='vTextField' name='person_set-23-father_name' maxlength='100' />" +
																	"</td>" +
																	"<td class='age'>" +
																		"<input id='id_person_set-23-age' type='text' class='vIntegerField' name='person_set-23-age' />" +
																	"</td>" +
																	"<td class='gender'>" +
																		"<select name='person_set-23-gender' id='id_person_set-23-gender'>" +
																			"<option value='' selected='selected'>---------</option>" +
																			"<option value='M'>Male</option>" +
																			"<option value='F'>Female</option>" +
																		"</select>" +
																	"</td>" +
																	"<td class='phone_no'>" +
																		"<input id='id_person_set-23-phone_no' type='text' class='vTextField' name='person_set-23-phone_no' maxlength='100' />" +
																	"</td>" +
																	"<td class='address'>" +
																		"<input id='id_person_set-23-address' type='text' class='vTextField' name='person_set-23-address' maxlength='500' />" +
																	"</td>" +
																	"<td class='land_holdings'>" +
																		"<input id='id_person_set-23-land_holdings' type='text' class='vIntegerField' name='person_set-23-land_holdings' />" +
																	"</td>" +
																	"<td class='village'>" +
																		"<select name='person_set-23-village' id='id_person_set-23-village'>" +
																			"<option value='' selected='selected'>---------</option>" +
																		"</select><a href='/admin/dashboard/village/add/' class='add-another' id='add_id_person_set-23-village' onclick='return showAddAnotherPopup(this);'> <img src='/media/img/admin/icon_addlink.gif' width='10' height='10' alt='Add Another'/></a>" +
																	"</td>" +
																	"<td class='delete'></td>" +
																"</tr>" +

																"<tr class='row1 '>" +							////////////////////////////////////////////////25
																	"<td class='original'>" +
																		"<input type='hidden' name='person_set-24-id' id='id_person_set-24-id' />" +
																		"<input type='hidden' name='person_set-24-group' id='id_person_set-24-group' />" +
																	"</td>" +
																	"<td class='person_name'>" +
																		"<input id='id_person_set-24-person_name' type='text' class='vTextField' name='person_set-24-person_name' maxlength='100' />" +
																	"</td>" +
																	"<td class='father_name'>" +
																		"<input id='id_person_set-24-father_name' type='text' class='vTextField' name='person_set-24-father_name' maxlength='100' />" +
																	"</td>" +
																	"<td class='age'>" +
																		"<input id='id_person_set-24-age' type='text' class='vIntegerField' name='person_set-24-age' />" +
																	"</td>" +
																	"<td class='gender'>" +
																		"<select name='person_set-24-gender' id='id_person_set-24-gender'>" +
																			"<option value='' selected='selected'>---------</option>" +
																			"<option value='M'>Male</option>" +
																			"<option value='F'>Female</option>" +
																		"</select>" +
																	"</td>" +
																	"<td class='phone_no'>" +
																		"<input id='id_person_set-24-phone_no' type='text' class='vTextField' name='person_set-24-phone_no' maxlength='100' />" +
																	"</td>" +
																	"<td class='address'>" +
																		"<input id='id_person_set-24-address' type='text' class='vTextField' name='person_set-24-address' maxlength='500' />" +
																	"</td>" +
																	"<td class='land_holdings'>" +	
																		"<input id='id_person_set-24-land_holdings' type='text' class='vIntegerField' name='person_set-24-land_holdings' />" +
																	"</td>" +
																	"<td class='village'>" +
																		"<select name='person_set-24-village' id='id_person_set-24-village'>" +
																			"<option value='' selected='selected'>---------</option>" +
																		"</select><a href='/admin/dashboard/village/add/' class='add-another' id='add_id_person_set-24-village' onclick='return showAddAnotherPopup(this);'> <img src='/media/img/admin/icon_addlink.gif' width='10' height='10' alt='Add Another'/></a>" +
																	"</td>" +
																	"<td class='delete'></td>" +
																"</tr>" +

																"<tr class='row2 '>" +							////////////////////////////////////////////////26
																	"<td class='original'>" +
																		"<input type='hidden' name='person_set-25-id' id='id_person_set-25-id' />" +
																		"<input type='hidden' name='person_set-25-group' id='id_person_set-25-group' />" +
																	"</td>" +
																	"<td class='person_name'>" +
																		"<input id='id_person_set-25-person_name' type='text' class='vTextField' name='person_set-25-person_name' maxlength='100' />" +
																	"</td>" +
																	"<td class='father_name'>" +
																		"<input id='id_person_set-25-father_name' type='text' class='vTextField' name='person_set-25-father_name' maxlength='100' />" +
																	"</td>" +
																	"<td class='age'>" +
																		"<input id='id_person_set-25-age' type='text' class='vIntegerField' name='person_set-25-age' />" +
																	"</td>" +
																	"<td class='gender'>" +
																		"<select name='person_set-25-gender' id='id_person_set-25-gender'>" +
																			"<option value='' selected='selected'>---------</option>" +
																			"<option value='M'>Male</option>" +
																			"<option value='F'>Female</option>" +
																		"</select>" +
																	"</td>" +
																	"<td class='phone_no'>" +
																		"<input id='id_person_set-25-phone_no' type='text' class='vTextField' name='person_set-25-phone_no' maxlength='100' />" +
																	"</td>" +
																	"<td class='address'>" +
																		"<input id='id_person_set-25-address' type='text' class='vTextField' name='person_set-25-address' maxlength='500' />" +
																	"</td>" +
																	"<td class='land_holdings'>" +
																		"<input id='id_person_set-25-land_holdings' type='text' class='vIntegerField' name='person_set-25-land_holdings' />" +
																	"</td>" +
																	"<td class='village'>" +
																		"<select name='person_set-25-village' id='id_person_set-25-village'>" +
																			"<option value='' selected='selected'>---------</option>" +
																		"</select><a href='/admin/dashboard/village/add/' class='add-another' id='add_id_person_set-25-village' onclick='return showAddAnotherPopup(this);'> <img src='/media/img/admin/icon_addlink.gif' width='10' height='10' alt='Add Another'/></a>" +
																	"</td>" +
																	"<td class='delete'></td>" +
																"</tr>" +

																"<tr class='row1 '>" +							////////////////////////////////////////////////27
																"<td class='original'>" +
																	"<input type='hidden' name='person_set-26-id' id='id_person_set-26-id' />" +
																	"<input type='hidden' name='person_set-26-group' id='id_person_set-26-group' />" +
																"</td>" +
																"<td class='person_name'>" +
																	"<input id='id_person_set-26-person_name' type='text' class='vTextField' name='person_set-26-person_name' maxlength='100' />" +
																"</td>" +
																"<td class='father_name'>" +
																	"<input id='id_person_set-26-father_name' type='text' class='vTextField' name='person_set-26-father_name' maxlength='100' />" +
																"</td>" +
																"<td class='age'>" +
																	"<input id='id_person_set-26-age' type='text' class='vIntegerField' name='person_set-26-age' />" +
																"</td>" +
																"<td class='gender'>" +
																	"<select name='person_set-26-gender' id='id_person_set-26-gender'>" +
																		"<option value='' selected='selected'>---------</option>" +
																		"<option value='M'>Male</option>" +
																		"<option value='F'>Female</option>" +
																	"</select>" +
																"</td>" +
																"<td class='phone_no'>" +
																	"<input id='id_person_set-26-phone_no' type='text' class='vTextField' name='person_set-26-phone_no' maxlength='100' />" +
																"</td>" +
																"<td class='address'>" +
																	"<input id='id_person_set-26-address' type='text' class='vTextField' name='person_set-26-address' maxlength='500' />" +
																"</td>" +
																"<td class='land_holdings'>" +
																	"<input id='id_person_set-26-land_holdings' type='text' class='vIntegerField' name='person_set-26-land_holdings' />" +
																"</td>" +
																"<td class='village'>" +
																	"<select name='person_set-26-village' id='id_person_set-26-village'>" +
																		"<option value='' selected='selected'>---------</option>" +
																	"</select><a href='/admin/dashboard/village/add/' class='add-another' id='add_id_person_set-26-village' onclick='return showAddAnotherPopup(this);'> <img src='/media/img/admin/icon_addlink.gif' width='10' height='10' alt='Add Another'/></a>" +
																"</td>" +
																"<td class='delete'></td>" +
															"</tr>" +

															"<tr class='row2 '>" +							////////////////////////////////////////////////28
																"<td class='original'>" +
																	"<input type='hidden' name='person_set-27-id' id='id_person_set-27-id' />" +
																	"<input type='hidden' name='person_set-27-group' id='id_person_set-27-group' />" +
																"</td>" +
																"<td class='person_name'>" +
																	"<input id='id_person_set-27-person_name' type='text' class='vTextField' name='person_set-27-person_name' maxlength='100' />" +
																"</td>" +
																"<td class='father_name'>" +
																	"<input id='id_person_set-27-father_name' type='text' class='vTextField' name='person_set-27-father_name' maxlength='100' />" +
																"</td>" +
																"<td class='age'>" +
																	"<input id='id_person_set-27-age' type='text' class='vIntegerField' name='person_set-27-age' />" +
																"</td>" +
																"<td class='gender'>" +
																	"<select name='person_set-27-gender' id='id_person_set-27-gender'>" +
																		"<option value='' selected='selected'>---------</option>" +
																		"<option value='M'>Male</option>" +
																		"<option value='F'>Female</option>" +
																	"</select>" +
																"</td>" +
																"<td class='phone_no'>" +
																	"<input id='id_person_set-27-phone_no' type='text' class='vTextField' name='person_set-27-phone_no' maxlength='100' />" +
																"</td>" +
																"<td class='address'>" +
																	"<input id='id_person_set-27-address' type='text' class='vTextField' name='person_set-27-address' maxlength='500' />" +
																"</td>" +
																"<td class='land_holdings'>" +
																	"<input id='id_person_set-27-land_holdings' type='text' class='vIntegerField' name='person_set-27-land_holdings' />" +
																"</td>" +
																"<td class='village'>" +
																	"<select name='person_set-27-village' id='id_person_set-27-village'>" +
																		"<option value='' selected='selected'>---------</option>" +
																	"</select><a href='/admin/dashboard/village/add/' class='add-another' id='add_id_person_set-27-village' onclick='return showAddAnotherPopup(this);'> <img src='/media/img/admin/icon_addlink.gif' width='10' height='10' alt='Add Another'/></a>" +
																"</td>" +
																"<td class='delete'></td>" +
															"</tr>" +

															"<tr class='row1 '>" +							////////////////////////////////////////////////29
																"<td class='original'>" +
																	"<input type='hidden' name='person_set-28-id' id='id_person_set-28-id' />" +
																	"<input type='hidden' name='person_set-28-group' id='id_person_set-28-group' />" +
																"</td>" +
																"<td class='person_name'>" +
																	"<input id='id_person_set-28-person_name' type='text' class='vTextField' name='person_set-28-person_name' maxlength='100' />" +
																"</td>" +
																"<td class='father_name'>" +
																	"<input id='id_person_set-28-father_name' type='text' class='vTextField' name='person_set-28-father_name' maxlength='100' />" +
																"</td>" +
																"<td class='age'>" +
																	"<input id='id_person_set-28-age' type='text' class='vIntegerField' name='person_set-28-age' />" +
																"</td>" +
																"<td class='gender'>" +
																	"<select name='person_set-28-gender' id='id_person_set-28-gender'>" +
																		"<option value='' selected='selected'>---------</option>" +
																		"<option value='M'>Male</option>" +
																		"<option value='F'>Female</option>" +
																	"</select>" +
																"</td>" +
																"<td class='phone_no'>" +
																	"<input id='id_person_set-28-phone_no' type='text' class='vTextField' name='person_set-28-phone_no' maxlength='100' />" +
																"</td>" +
																"<td class='address'>" +
																	"<input id='id_person_set-28-address' type='text' class='vTextField' name='person_set-28-address' maxlength='500' />" +
																"</td>" +
																"<td class='land_holdings'>" +
																	"<input id='id_person_set-28-land_holdings' type='text' class='vIntegerField' name='person_set-28-land_holdings' />" +
																"</td>" +
																"<td class='village'>" +
																	"<select name='person_set-28-village' id='id_person_set-28-village'>" +
																		"<option value='' selected='selected'>---------</option>" +
																	"</select><a href='/admin/dashboard/village/add/' class='add-another' id='add_id_person_set-28-village' onclick='return showAddAnotherPopup(this);'> <img src='/media/img/admin/icon_addlink.gif' width='10' height='10' alt='Add Another'/></a>" +
																"</td>" +
																"<td class='delete'></td>" +
															"</tr>" +

															"<tr class='row2 '>" +							////////////////////////////////////////////////30
																"<td class='original'>" +
																	"<input type='hidden' name='person_set-29-id' id='id_person_set-29-id' />" +
																	"<input type='hidden' name='person_set-29-group' id='id_person_set-29-group' />" +
																"</td>" +
																"<td class='person_name'>" +
																	"<input id='id_person_set-29-person_name' type='text' class='vTextField' name='person_set-29-person_name' maxlength='100' />" +
																"</td>" +
																"<td class='father_name'>" +
																	"<input id='id_person_set-29-father_name' type='text' class='vTextField' name='person_set-29-father_name' maxlength='100' />" +
																"</td>" +
																"<td class='age'>" +
																	"<input id='id_person_set-29-age' type='text' class='vIntegerField' name='person_set-29-age' />" +
																"</td>" +
																"<td class='gender'>" +
																	"<select name='person_set-29-gender' id='id_person_set-29-gender'>" +
																		"<option value='' selected='selected'>---------</option>" +
																		"<option value='M'>Male</option>" +
																		"<option value='F'>Female</option>" +
																	"</select>" +
																"</td>" +
																"<td class='phone_no'>" +
																	"<input id='id_person_set-29-phone_no' type='text' class='vTextField' name='person_set-29-phone_no' maxlength='100' />" +
																"</td>" +
																"<td class='address'>" +
																	"<input id='id_person_set-29-address' type='text' class='vTextField' name='person_set-29-address' maxlength='500' />" +
																"</td>" +
																"<td class='land_holdings'>" +
																	"<input id='id_person_set-29-land_holdings' type='text' class='vIntegerField' name='person_set-29-land_holdings' />" +
																"</td>" +
																"<td class='village'>" +
																	"<select name='person_set-29-village' id='id_person_set-29-village'>" +
																		"<option value='' selected='selected'>---------</option>" +
																	"</select><a href='/admin/dashboard/village/add/' class='add-another' id='add_id_person_set-29-village' onclick='return showAddAnotherPopup(this);'> <img src='/media/img/admin/icon_addlink.gif' width='10' height='10' alt='Add Another'/></a>" +
																"</td>" +
																"<td class='delete'></td>" +
															"</tr>" +

														"</table>" +
													"</fieldset>" +
												"</div>" +
											"</div>" +
											"<div class='submit-row' >" +
												"<input type='submit' value='Save' class='default' name='_save' />" +
											"</div>" +
											"<script type='text/javascript'>document.getElementById('id_group_name').focus();</script>" +
											"<script type='text/javascript'>" +
											"</script>" +
										"</div>" +
									"</form>" +
								"</div>" +
								"<br class='clear' />" +
							"</div>";
}

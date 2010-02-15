package com.digitalgreen.dashboardgwt.client.templates;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.google.gwt.user.client.ui.HTMLPanel;
import com.google.gwt.user.client.ui.RootPanel;

public class IndexTemplate extends BaseTemplate {
	
	public IndexTemplate(RequestContext requestContext) {
		super(requestContext);
	}
	
	@Override
	public void fill() {
		super.setBodyStyle("dashboard");
		HTMLPanel indexHtml = new HTMLPanel(indexContentHtml);
		super.setContentPanel(indexHtml);
		super.fill();
	}
	
	final static private String indexContentHtml = "<div id='content' class='colMS'>" +
							"<h1>Administration</h1>" +
								"<div id='content-main'>" +
									"<div class='module'>" +
										"<table summary='Models available in the Auth application.'>" +
											"<caption><a href='auth/' class='section'>Auth</a></caption>" +
												"<tr>" +
													"<th scope='row'><a id='g-1' href='#auth/group'>Groups</a></th>" +
														"<td><a id='g-2' href='#auth/group/add/' class='addlink'>Add</a></td>" +
														"<td><a id='g-3' href='#auth/group/' class='changelink'>Change</a></td>" +
												"</tr>" +
     											"<tr>" +
     												"<th scope='row'><a id='u-1' href='#auth/user/'>Users</a></th>" +
     													"<td><a id='u-2' href='#auth/user/add/' class='addlink'>Add</a></td>" +
     													"<td><a id='u-3' href='#auth/user/' class='changelink'>Change</a></td>" +
     											"</tr>" +
     									"</table>" +
     								"</div>" +
     								"<div class='module'>" +
     								"<table summary='Models available in the Dashboard application.'>" +
     									"<caption><a href='dashboard/' class='section'>Dashboard</a></caption>" +
     										"<tr>" +
     											"<th scope='row'><a id='aa-1' href='http://localhost:8888/DashboardGwt.html/#dashboard/animatorassignedvillage/'>Animator assigned villages</a></th>" +
     											"<td><a id='aa-2' href='DashboardGwt.html/#dashboard/animatorassignedvillage/add/' class='addlink'>Add</a></td>" +
     											"<td><a id='aa-3' href='DashboardGwt.html/#dashboard/animatorassignedvillage/' class='changelink'>Change</a></td>" +
     										"</tr>" +
     										"<tr>" +
     											"<th scope='row'><a id='a-1' href='#dashboard/animator/'>Animators</a></th>" +
     											"<td><a id='a-2' href='#dashboard/animator/add/' class='addlink'>Add</a></td>" +
     											"<td><a id='a-3' href='#dashboard/animator/' class='changelink'>Change</a></td>" +
     										"</tr>" +
     										"<tr>" +
     											"<th scope='row'><a id='b-1' href='#dashboard/block/'>Blocks</a></th>" +
     											"<td><a id='b-2' href='#dashboard/block/add/' class='addlink'>Add</a></td>" +
     											"<td><a id='b-3' href='#dashboard/block/' class='changelink'>Change</a></td>" +
     										"</tr>" +
     										"<tr>" +
     											"<th scope='row'><a id='dm-1' href='#dashboard/developmentmanager/'>Development managers</a></th>" +
     											"<td><a id='dm-2' href='#dashboard/developmentmanager/add/' class='addlink'>Add</a></td>" +
     											"<td><a id='dm-3' href='#dashboard/developmentmanager/' class='changelink'>Change</a></td>" +
     										"</tr>" +
     										"<tr>" +
     											"<th scope='row'><a id='d-1' href='#dashboard/district/'>Districts</a></th>"  +
     											"<td><a id='d-2' href='#dashboard/district/add/' class='addlink'>Add</a></td>" +
     											"<td><a id='d-3' href='#dashboard/district/' class='changelink'>Change</a></td>" +
     										"</tr>" +
     										"<tr>" +
     											"<th scope='row'><a id='e-1' href='#dashboard/equipment/'>Equipments</a></th>" +
     											"<td><a id='e-2' href='#dashboard/equipment/add/' class='addlink'>Add</a></td>" +
     											"<td><a id='e-3' href='#dashboard/equipment/' class='changelink'>Change</a></td>" +
     										"</tr>" +
     										"<tr>" +
     											"<th scope='row'><a id='f-1' href='#dashboard/fieldofficer/'>Field officers</a></th>" +
     											"<td><a id='f-2' href='#dashboard/fieldofficer/add/' class='addlink'>Add</a></td>" +
     											"<td><a id='f-3' href='#dashboard/fieldofficer/' class='changelink'>Change</a></td>" +
     										"</tr>" +
     										"<tr>" +
     											"<th scope='row'><a id='l=1' href='#dashboard/language/'>Languages</a></th>" +
     											"<td><a id='l-2' href='#dashboard/language/add/' class='addlink'>Add</a></td>" +
     											"<td><a id='l-3' href='#dashboard/language/' class='changelink'>Change</a></td>" +
     										"</tr>" +
     										"<tr>" +
     											"<th scope='row'><a id='p-1' href='#dashboard/partners/'>Partners</a></th>" +
     											"<td><a id='p-2' href='#dashboard/partners/add/' class='addlink'>Add</a></td>" +
     											"<td><a id='p-3' href='#dashboard/partners/' class='changelink'>Change</a></td>" +
     										"</tr>" +
     										"<tr>" +
     											"<th scope='row'><a id='pg-1' href='#dashboard/persongroups/'>Person groups</a></th>" +
     											"<td><a id='pg-2' href='#dashboard/persongroups/add/' class='addlink'>Add</a></td>" +
     											"<td><a id='pg-3' href='#dashboard/persongroups/' class='changelink'>Change</a></td>" +
     										"</tr>" +
     										"<tr>" +
     											"<th scope='row'><a id='pe-1' href='#dashboard/person/'>Persons</a></th>" +
     											"<td><a id='pe-2' href='#dashboard/person/add/' class='addlink'>Add</a></td>" +
     											"<td><a id='pe-3' href='#dashboard/person/' class='changelink'>Change</a></td>" +
     										"</tr>" +
     										"<tr>" +
     											"<th scope='row'><a id='pr-1' href='#dashboard/practices/'>Practices</a></th>" +
     											"<td><a id='pr-2' href='#dashboard/practices/add/' class='addlink'>Add</a></td>" +
     											"<td><a id='pr-3' href='#dashboard/practices/' class='changelink'>Change</a></td>" +
     										"</tr>" +
     										"<tr>" +
     											"<th scope='row'><a id='r-1' href='#dashboard/region/'>Regions</a></th>" +
     											"<td><a id='r-2' href='#dashboard/region/add/' class='addlink'>Add</a></td>" +
     											"<td><a id='r-3' href='#dashboard/region/' class='changelink'>Change</a></td>" +
     										"</tr>" +
     										"<tr>" +
     											"<th scope='row'><a id='sc-1' href='#dashboard/screening/'>Screenings</a></th>" +
     											"<td><a id='sc-2' href='#dashboard/screening/add/' class='addlink'>Add</a></td>" +
     											"<td><a id='sc-3' href='#dashboard/screening/' class='changelink'>Change</a></td>" +
     										"</tr>" +
     										"<tr>" +
     											"<th scope='row'><a id='st-1' href='#dashboard/state/'>States</a></th>" +
     											"<td><a id='st-2' href='#dashboard/state/add/' class='addlink'>Add</a></td>" +
     											"<td><a id='st-3' href='#dashboard/state/' class='changelink'>Change</a></td>" +
     										"</tr>" +
     										"<tr>" +
     											"<th scope='row'><a id='t-1' href='#dashboard/training/'>Trainings</a></th>" +
     											"<td><a id='t-2' href='#dashboard/training/add/' class='addlink'>Add</a></td>" +
     											"<td><a id='t-3' href='#dashboard/training/' class='changelink'>Change</a></td>" +
     										"</tr>" +
     										"<tr>" +
     											"<th scope='row'><a id='v-1' href='#dashboard/video/'>Videos</a></th>" +
     											"<td><a id='v-2' href='#dashboard/video/add/' class='addlink'>Add</a></td>" +
     											"<td><a id='v-3' href='#dashboard/video/' class='changelink'>Change</a></td>" +
     										"</tr>" +
     										"<tr>" +
     											"<th scope='row'><a id='vi-1' href='#dashboard/village/'>Villages</a></th>" +
     											"<td><a id='vi-2' href='#dashboard/village/add/' class='addlink'>Add</a></td>" +
     											"<td><a id='vi-3' href='#dashboard/village/' class='changelink'>Change</a></td>" +
     										"</tr>" +
     									"</table>" +
     								"</div>" +
     							"</div>";
}
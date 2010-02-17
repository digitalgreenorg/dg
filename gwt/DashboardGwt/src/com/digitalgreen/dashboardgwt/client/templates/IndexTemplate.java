package com.digitalgreen.dashboardgwt.client.templates;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.servlets.AnimatorAssignedVillages;
import com.digitalgreen.dashboardgwt.client.servlets.BaseServlet;
import com.digitalgreen.dashboardgwt.client.servlets.Regions;
import com.digitalgreen.dashboardgwt.client.servlets.Screenings;
import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.Button;
import com.google.gwt.user.client.ui.HTMLPanel;
import com.google.gwt.user.client.ui.Hyperlink;
import com.google.gwt.user.client.ui.RootPanel;

public class IndexTemplate extends BaseTemplate {
	
	public IndexTemplate(RequestContext requestContext) {
		super(requestContext);
	}
	
	private void addHyperlink(String id, String linkTxt, String tokenTxt, final BaseServlet servlet) {
		Hyperlink link = new Hyperlink(linkTxt, true, tokenTxt); 
		link.addClickHandler(new ClickHandler() {
			public void onClick(ClickEvent event) {
				servlet.response();
			}	
		});
		RootPanel.get(id).add(link);
	}
	
	@Override
	public void fill() {
		super.setBodyStyle("dashboard");
		HTMLPanel indexHtml = new HTMLPanel(indexContentHtml);
		super.setContentPanel(indexHtml);
		super.fill();
		RequestContext requestContext = null;
		addHyperlink("g-1", "<a href='#auth/group'>Groups</a>", "auth/group", new BaseServlet());
		addHyperlink("g-2", "<a href='#auth/group/add/' class='addlink'>Add</a>", "auth/group/add", new BaseServlet());
		addHyperlink("u-1", "<a href='#auth/user/'>Users</a>", "auth/user", new BaseServlet());
		addHyperlink("u-2", "<a href='#auth/user/add/' class='addlink'>Add</a>", "auth/user", new BaseServlet());
		addHyperlink("aa-1", "<a  href='#dashboard/animatorassignedvillage/'>Animator assigned villages</a>", "dashboard/animatorassignedvillage", new AnimatorAssignedVillages());
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "add");
		addHyperlink("aa-2", "<a  href='#dashboard/animatorassignedvillage/add' class='addlink'>Add</a>", "dashboard/animatorassignedvillage/add", new AnimatorAssignedVillages(requestContext));
		addHyperlink("a-1", "<a href='#dashboard/animator/'>Animators</a>", "dashboard/animator", new BaseServlet());
		addHyperlink("a-2", "<a href='#dashboard/animator/add' class='addlink'>Add</a>", "dashboard/animator/add", new BaseServlet());
		addHyperlink("b-1", "<a href='#dashboard/block/'>Blocks</a>", "dashboard/block", new BaseServlet());
		addHyperlink("b-2", "<a href='#dashboard/block/add' class='addlink'>Add</a>", "dashboard/block/add", new BaseServlet());
		addHyperlink("d-1", "<a href='#dashboard/developmentmanager/'>Development managers</a>", "dashboard/developmentmanager", new BaseServlet());
		addHyperlink("d-2", "<a href='#dashboard/developmentmanager/add' class='addlink'>Add</a>", "dashboard/developmentmanager/add", new BaseServlet());
		addHyperlink("di-1", "<a href='#dashboard/district/'>Districts</a>", "dashboard/district", new BaseServlet());
		addHyperlink("di-2", "<a href='#dashboard/district/add' class='addlink'>Add</a>", "dashboard/district/add", new BaseServlet());
		addHyperlink("e-1", "<a href='#dashboard/equipment/'>Equipments</a>", "dashboard/equipment", new BaseServlet());
		addHyperlink("e-2", "<a href='#dashboard/equipment/add' class='addlink'>Add</a>", "dashboard/equipment/add", new BaseServlet());
		addHyperlink("f-1", "<a href='#dashboard/fieldofficer/'>Field officers</a>", "dashboard/fieldofficer", new BaseServlet());
		addHyperlink("f-2", "<a href='#dashboard/fieldofficer/add' class='addlink'>Add</a>", "dashboard/fieldofficer/add", new BaseServlet());
		addHyperlink("l-1", "<a href='#dashboard/language/'>Languages</a>", "dashboard/language", new BaseServlet());
		addHyperlink("l-2", "<a href='#dashboard/language/add' class='addlink'>Add</a>", "dashboard/language/add", new BaseServlet());
		addHyperlink("p-1", "<a href='#dashboard/partners/'>Partners</a>", "dashboard/partners", new BaseServlet());		
		addHyperlink("p-2", "<a href='#dashboard/partners/add' class='addlink'>Add</a>", "dashboard/partners/add", new BaseServlet());
		addHyperlink("pg-1","<a href='#dashboard/persongroups/'>Person groups</a>", "dashboard/persongroups", new BaseServlet());
		addHyperlink("pg-2","<a href='#dashboard/persongroups/add' class='addlink'>Add</a>", "dashboard/persongroups/add", new BaseServlet());
		addHyperlink("pe-1", "<a href='#dashboard/person/'>Persons</a>", "dashboard/person", new BaseServlet());
		addHyperlink("pe-2", "<a href='#dashboard/person/add' class='addlink'>Add</a>", "dashboard/person/add", new BaseServlet());
		addHyperlink("pr-1", "<a href='#dashboard/practices/'>Practices</a>", "dashboard/practices", new BaseServlet());
		addHyperlink("pr-2", "<a href='#dashboard/practices/add' class='addlink'>Add</a>", "dashboard/practices/add", new BaseServlet());
		addHyperlink("r-1", "<a href='#dashboard/region/'>Regions</a>", "dashboard/region", new Regions());
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "add");
		addHyperlink("r-2", "<a href='#dashboard/region/add' class='addlink'>Add</a>", "dashboard/region/add", new Regions(requestContext));
		addHyperlink("s-1", "<a href='#dashboard/screening/'>Screenings</a>", "dashboard/screening", new Screenings());
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "add");
		addHyperlink("s-2", "<a href='#dashboard/screening/add' class='addlink'>Add</a>", "dashboard/screening/add", new Screenings(requestContext));
		addHyperlink("st-1", "<a id='st-1' href='#dashboard/state/'>States</a>", "dashboard/state", new BaseServlet());
		addHyperlink("st-2", "<a id='st-2' href='#dashboard/state/add' class='addlink'>Add</a>", "dashboard/state/add", new BaseServlet());
		addHyperlink("t-1", "<a href='#dashboard/training/'>Trainings</a>", "dashboard/training", new BaseServlet());
		addHyperlink("t-2", "<a href='#dashboard/training/add' class='addlink'>Add</a>", "dashboard/training/add", new BaseServlet());
		addHyperlink("v-1", "<a href='#dashboard/video/'>Videos</a>", "dashboard/video", new BaseServlet());
		addHyperlink("v-2", "<a href='#dashboard/video/add' class='addlink'>Add</a>", "dashboard/video/add", new BaseServlet());
		addHyperlink("vi-1", "<a href='#dashboard/village/'>Villages</a>", "dashboard/village", new BaseServlet());
		addHyperlink("vi-2", "<a href='#dashboard/village/add' class='addlink'>Add</a>", "dashboard/village/add", new BaseServlet());
	}
	
	final static private String indexContentHtml = "<div id='content' class='colMS'>" +
							"<h1>Administration</h1>" +
								"<div id='content-main'>" +
									"<div class='module'>" +
										"<table summary='Models available in the Auth application.'>" +
											"<caption><a href='auth/' class='section'>Auth</a></caption>" +
												"<tr>" +
													"<th id='g-1' scope='row'>" +
													"</th>" +
													"<td id='g-2'>" +
													"</td>" +
												"</tr>" +
     											"<tr>" +
     												"<th id='u-1' scope='row'>" +
     												"</th>" +
     												"<td id='u-2'>" +
     												"</td>" +
     											"</tr>" +
     									"</table>" +
     								"</div>" +
     								"<div class='module'>" +
     								"<table summary='Models available in the Dashboard application.'>" +
     									"<caption><a href='dashboard/' class='section'>Dashboard</a></caption>" +
     										"<tr>" +
     											"<th id='aa-1' scope='row'>" +
     											"</th>" +
     											"<td id='aa-2'>" +
     											"</td>" +
     										"</tr>" +
     										"<tr>" +
     											"<th id='a-1' scope='row'>" +
     											"</th>" +
     											"<td id='a-2'>" +
     											"</td>" +
     										"</tr>" +
     										"<tr>" +
     											"<th id='b-1' scope='row'>" +
     											"</th>" +
     											"<td id='b-2'>" +
     											"</td>" +
     										"</tr>" +
     										"<tr>" +
     											"<th id='d-1' scope='row'>" +
     											"</th>" +
     											"<td id='d-2'>" +
     											"</td>" +
     										"</tr>" +
     										"<tr>" +
     											"<th id='di-1' scope='row'>" +
     											"</th>"  +
     											"<td id='di-2'>" +
     											"</td>" +
     										"</tr>" +
     										"<tr>" +
     											"<th id='e-1' scope='row'>" +
     											"</th>" +
     											"<td id='e-2'>" +
     											"</td>" +
     										"</tr>" +
     										"<tr>" +
     											"<th id='f-1' scope='row'>" +
     											"</th>" +
     											"<td id='f-2'>" +
     											"</td>" +
     										"</tr>" +
     										"<tr>" +
     											"<th id='l-1' scope='row'>" +
     											"</th>" +
     											"<td id='l-2'>" +
     											"</td>" +
     										"</tr>" +
     										"<tr>" +
     											"<th id='p-1' scope='row'>" +
     											"</th>" +
     											"<td id='p-2'>" +
     											"</td>" +
     										"</tr>" +
     										"<tr>" +
     											"<th id='pg-1' scope='row'>" +
     											"</th>" +
     											"<td id='pg-2'>" +
     											"</td>" +
     										"</tr>" +
     										"<tr>" +
     											"<th id='pe-1' scope='row'>" +
     											"</th>" +
     											"<td id='pe-2'>" +
     											"</td>" +
     										"</tr>" +
     										"<tr>" +
     											"<th id='pr-1'scope='row'>" +
     											"</th>" +
     											"<td id='pr-2'>" +
     											"</td>" +
     										"</tr>" +
     										"<tr>" +
     											"<th id='r-1' scope='row'>" +
     											"</th>" +
     											"<td id='r-2'>" +
     											"</td>" +
     										"</tr>" +
     										"<tr>" +
     											"<th id='s-1' scope='row'>" +
     											"</th>" +
     											"<td id='s-2'>" +
     											"</td>" +
     										"</tr>" +
     										"<tr>" +
     											"<th id='st-1' scope='row'>" +
     											"</th>" +
     											"<td id='st-2'>" +
     											"</td>" +
     										"</tr>" +
     										"<tr>" +
     											"<th id='t-1' scope='row'>" +
     											"</th>" +
     											"<td id='t-2'>" +
     											"</td>" +
     										"</tr>" +
     										"<tr>" +
     											"<th id='v-1' scope='row'>" +
     											"</th>" +
     											"<td id='v-2'>" +
     											"</td>" +
     										"</tr>" +
     										"<tr>" +
     											"<th id='vi-1' scope='row'>" +
     											"</th>" +
     											"<td id='vi-2'>" +
     											"</td>" +
     										"</tr>" +
     									"</table>" +
     								"</div>" +
     							"</div>";
}
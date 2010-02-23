package com.digitalgreen.dashboardgwt.client.templates;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.servlets.AnimatorAssignedVillages;
import com.digitalgreen.dashboardgwt.client.servlets.Animators;
import com.digitalgreen.dashboardgwt.client.servlets.BaseServlet;
import com.digitalgreen.dashboardgwt.client.servlets.Blocks;
import com.digitalgreen.dashboardgwt.client.servlets.DevelopmentManagers;
import com.digitalgreen.dashboardgwt.client.servlets.Districts;
import com.digitalgreen.dashboardgwt.client.servlets.Equipments;
import com.digitalgreen.dashboardgwt.client.servlets.FieldOfficers;
import com.digitalgreen.dashboardgwt.client.servlets.Languages;
import com.digitalgreen.dashboardgwt.client.servlets.Partners;
import com.digitalgreen.dashboardgwt.client.servlets.PersonGroups;
import com.digitalgreen.dashboardgwt.client.servlets.Persons;
import com.digitalgreen.dashboardgwt.client.servlets.Practices;
import com.digitalgreen.dashboardgwt.client.servlets.Regions;
import com.digitalgreen.dashboardgwt.client.servlets.Screenings;
import com.digitalgreen.dashboardgwt.client.servlets.States;
import com.digitalgreen.dashboardgwt.client.servlets.Trainings;
import com.digitalgreen.dashboardgwt.client.servlets.Videos;
import com.digitalgreen.dashboardgwt.client.servlets.Villages;
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
		super.usrStr.setText("digitalgreen.");
		super.setContentPanel(indexHtml);
		super.fill();
		RequestContext requestContext = null;
		addHyperlink("aa-1", "<a  href='#dashboard/animatorassignedvillage/'>Animator assigned villages</a>", "dashboard/animatorassignedvillage", new AnimatorAssignedVillages());
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "add");
		addHyperlink("aa-2", "<a  href='#dashboard/animatorassignedvillage/add' class='addlink'>Add</a>", "dashboard/animatorassignedvillage/add", new AnimatorAssignedVillages(requestContext));
		addHyperlink("a-1", "<a href='#dashboard/animator/'>Animators</a>", "dashboard/animator", new Animators());
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "add");
		addHyperlink("a-2", "<a href='#dashboard/animator/add' class='addlink'>Add</a>", "dashboard/animator/add", new Animators(requestContext));
		addHyperlink("b-1", "<a href='#dashboard/block/'>Blocks</a>", "dashboard/block", new Blocks());
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "add");
		addHyperlink("b-2", "<a href='#dashboard/block/add' class='addlink'>Add</a>", "dashboard/block/add", new Blocks(requestContext));
		addHyperlink("d-1", "<a href='#dashboard/developmentmanager/'>Development managers</a>", "dashboard/developmentmanager", new DevelopmentManagers());
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "add");
		addHyperlink("d-2", "<a href='#dashboard/developmentmanager/add' class='addlink'>Add</a>", "dashboard/developmentmanager/add", new DevelopmentManagers(requestContext));
		addHyperlink("di-1", "<a href='#dashboard/district/'>Districts</a>", "dashboard/district", new Districts());
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "add");
		addHyperlink("di-2", "<a href='#dashboard/district/add' class='addlink'>Add</a>", "dashboard/district/add", new Districts(requestContext));
		addHyperlink("e-1", "<a href='#dashboard/equipment/'>Equipments</a>", "dashboard/equipment", new Equipments());
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "add");
		addHyperlink("e-2", "<a href='#dashboard/equipment/add' class='addlink'>Add</a>", "dashboard/equipment/add", new Equipments(requestContext));
		addHyperlink("f-1", "<a href='#dashboard/fieldofficer/'>Field officers</a>", "dashboard/fieldofficer", new FieldOfficers());
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "add");
		addHyperlink("f-2", "<a href='#dashboard/fieldofficer/add' class='addlink'>Add</a>", "dashboard/fieldofficer/add", new FieldOfficers(requestContext));
		addHyperlink("l-1", "<a href='#dashboard/language/'>Languages</a>", "dashboard/language", new Languages());
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "add");
		addHyperlink("l-2", "<a href='#dashboard/language/add' class='addlink'>Add</a>", "dashboard/language/add", new Languages(requestContext));
		addHyperlink("p-1", "<a href='#dashboard/partners/'>Partners</a>", "dashboard/partners", new Partners());
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "add");
		addHyperlink("p-2", "<a href='#dashboard/partners/add' class='addlink'>Add</a>", "dashboard/partners/add", new Partners(requestContext));
		addHyperlink("pg-1","<a href='#dashboard/persongroups/'>Person groups</a>", "dashboard/persongroups", new PersonGroups());
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "add");
		addHyperlink("pg-2","<a href='#dashboard/persongroups/add' class='addlink'>Add</a>", "dashboard/persongroups/add", new PersonGroups(requestContext));
		addHyperlink("pe-1", "<a href='#dashboard/person/'>Persons</a>", "dashboard/person", new Persons());
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "add");
		addHyperlink("pe-2", "<a href='#dashboard/person/add' class='addlink'>Add</a>", "dashboard/person/add", new Persons(requestContext));
		addHyperlink("pr-1", "<a href='#dashboard/practices/'>Practices</a>", "dashboard/practices", new Practices());
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "add");
		addHyperlink("pr-2", "<a href='#dashboard/practices/add' class='addlink'>Add</a>", "dashboard/practices/add", new Practices(requestContext));
		addHyperlink("r-1", "<a href='#dashboard/region/'>Regions</a>", "dashboard/region", new Regions());
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "add");
		addHyperlink("r-2", "<a href='#dashboard/region/add' class='addlink'>Add</a>", "dashboard/region/add", new Regions(requestContext));
		addHyperlink("s-1", "<a href='#dashboard/screening/'>Screenings</a>", "dashboard/screening", new Screenings());
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "add");
		addHyperlink("s-2", "<a href='#dashboard/screening/add' class='addlink'>Add</a>", "dashboard/screening/add", new Screenings(requestContext));
		addHyperlink("st-1", "<a id='st-1' href='#dashboard/state/'>States</a>", "dashboard/state", new States());
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "add");
		addHyperlink("st-2", "<a id='st-2' href='#dashboard/state/add' class='addlink'>Add</a>", "dashboard/state/add", new States(requestContext));
		addHyperlink("t-1", "<a href='#dashboard/training/'>Trainings</a>", "dashboard/training", new Trainings());
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "add");
		addHyperlink("t-2", "<a href='#dashboard/training/add' class='addlink'>Add</a>", "dashboard/training/add", new Trainings(requestContext));
		addHyperlink("v-1", "<a href='#dashboard/video/'>Videos</a>", "dashboard/video", new Videos());
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "add");
		addHyperlink("v-2", "<a href='#dashboard/video/add' class='addlink'>Add</a>", "dashboard/video/add", new Videos(requestContext));
		addHyperlink("vi-1", "<a href='#dashboard/village/'>Villages</a>", "dashboard/village", new Villages());
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "add");
		addHyperlink("vi-2", "<a href='#dashboard/village/add' class='addlink'>Add</a>", "dashboard/village/add", new Villages(requestContext));
	}
	
	final static private String indexContentHtml = "<div id='content' class='colMS'>" +
							"<h1>Administration</h1>" +
								"<div id='content-main'>" +
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
package com.digitalgreen.dashboardgwt.client.templates;

import com.digitalgreen.dashboardgwt.client.common.ApplicationConstants;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.servlets.AnimatorAssignedVillages;
import com.digitalgreen.dashboardgwt.client.servlets.Animators;
import com.digitalgreen.dashboardgwt.client.servlets.BaseServlet;
import com.digitalgreen.dashboardgwt.client.servlets.Blocks;
import com.digitalgreen.dashboardgwt.client.servlets.DashboardError;
import com.digitalgreen.dashboardgwt.client.servlets.DevelopmentManagers;
import com.digitalgreen.dashboardgwt.client.servlets.Districts;
import com.digitalgreen.dashboardgwt.client.servlets.Equipments;
import com.digitalgreen.dashboardgwt.client.servlets.FieldOfficers;
import com.digitalgreen.dashboardgwt.client.servlets.Index;
import com.digitalgreen.dashboardgwt.client.servlets.Languages;
import com.digitalgreen.dashboardgwt.client.servlets.Partners;
import com.digitalgreen.dashboardgwt.client.servlets.PersonAdoptPractices;
import com.digitalgreen.dashboardgwt.client.servlets.PersonGroups;
import com.digitalgreen.dashboardgwt.client.servlets.Persons;
import com.digitalgreen.dashboardgwt.client.servlets.Practices;
import com.digitalgreen.dashboardgwt.client.servlets.Regions;
import com.digitalgreen.dashboardgwt.client.servlets.Screenings;
import com.digitalgreen.dashboardgwt.client.servlets.States;
import com.digitalgreen.dashboardgwt.client.servlets.Targets;
import com.digitalgreen.dashboardgwt.client.servlets.Trainings;
import com.digitalgreen.dashboardgwt.client.servlets.Videos;
import com.digitalgreen.dashboardgwt.client.servlets.Villages;
import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.user.client.Timer;
import com.google.gwt.user.client.ui.HTMLPanel;
import com.google.gwt.user.client.ui.Hyperlink;
import com.google.gwt.user.client.ui.Image;
import com.google.gwt.user.client.ui.Label;
import com.google.gwt.user.client.ui.RootPanel;
import com.digitalgreen.dashboardgwt.client.common.events.ProgressEvent;
import com.digitalgreen.dashboardgwt.client.common.events.EventBus;
import com.digitalgreen.dashboardgwt.client.data.IndexData;
import com.digitalgreen.dashboardgwt.client.data.IndexData.Data;

// Our Index page has some added event properties to listen for progress events 
// dispatched from Synchronisation.  Since Download/Upload both spawn from Index,  
// it seems reasonable to have an IndexTemplate object listen for these progress events.
public class IndexTemplate extends BaseTemplate implements ProgressEvent.Handler {
	
	public IndexTemplate() {
		super();
	}
	
	public IndexTemplate(RequestContext requestContext) {
		super(requestContext);
	}

	private static native void progressBar(int value) /*-{
		return $wnd.progressBarSet(value);
	}-*/;
	
	@Override
	public void onProgressEvent(ProgressEvent progressEvent) {
		IndexTemplate.progressBar(progressEvent.getProgressMark());
	}
	
	private void goOfflineOnline(){
		HTMLPanel bodyHtml = new HTMLPanel(this.bodyContentHtml);
		RootPanel.get("controlPanel").add(bodyHtml);
		Image onlineOfflineButton = Image.wrap(RootPanel.get("onlineOfflineButtonId").getElement());
		final Image downloadButton = Image.wrap(RootPanel.get("downloadButtonId").getElement());
		final Image uploadButton = Image.wrap(RootPanel.get("uploadButtonId").getElement());
		String modeText = "";
		if(!ApplicationConstants.getCurrentOnlineStatus()) {
			onlineOfflineButton.setUrl("/media/img/admin/online-icon.png");
			downloadButton.setStyleName("buttonHideClass");
			uploadButton.setStyleName("buttonHideClass");
			modeText = "Connected in offline mode";
		} else {
			onlineOfflineButton.setUrl("/media/img/admin/offline-icon.png");
			downloadButton.setStyleName("buttonShowClass");
			uploadButton.setStyleName("buttonShowClass");
			modeText = "Connected in online mode";
		}
		onlineOfflineButton.setStyleName("onlineOfflineButtonClass");
		if(!(Boolean)this.requestContext.getArgs().get("showOfflineReady")) {
			onlineOfflineButton.setStyleName("buttonHideClass");
			uploadButton.setStyleName("buttonHideClass");
		}
		modeText += "<span id='dotsId'><img class='dotsClass' src='/media/img/admin/dots.gif' /></span>";
		HTMLPanel modeTextHtml = new HTMLPanel(modeText);
		modeTextHtml.getElement().setId("modeTextAndDotsId");
		modeTextHtml.setStyleName("modeTextClass");
		RootPanel.get("modeTextId").insert(modeTextHtml, 0);
		onlineOfflineButton.setPixelSize(350, 80);
		
		Timer t = new Timer() {
			@Override
			public void run() {
				Image modeIcon;
				String modeIconUrl = "";
				RootPanel.get("dotsId").clear();
				if(!ApplicationConstants.getCurrentOnlineStatus()) {
					modeIcon = new Image("/media/img/admin/offline-mode-icon.png");				
				} else {
					modeIcon = new Image("/media/img/admin/online-mode-icon.png");	
				}
				RootPanel.get("modeIconId").clear();
				RootPanel.get("modeIconId").insert(modeIcon, 0);
			}
		};
		t.schedule(1000);
		
		onlineOfflineButton.addClickHandler(new ClickHandler() {
		      public void onClick(ClickEvent event) {
		    	   RequestContext requestContext = new RequestContext(RequestContext.METHOD_POST);
		    	   BaseTemplate operationUi = new BaseTemplate();
		    	   if (ApplicationConstants.getCurrentOnlineStatus()){
		    		   operationUi.showGlassDoorMessage("<img style='margin-bottom: -3px;' src='/media/img/admin/ajax-loader.gif' /> Going offline.  Your offline settings are being downloaded." +
		    		   		"<br /><div id='progressBar'></div>");
		    		   EventBus.get().addHandler(ProgressEvent.TYPE, new IndexTemplate());
		    		   requestContext.getArgs().put("action", "gooffline");
		    	   }
		    	   else{
		    		   operationUi.showGlassDoorMessage("<img style='margin-bottom: -3px;' src='/media/img/admin/ajax-loader.gif' /> Going online");
		    		   requestContext.getArgs().put("action", "goonline");
		    	   }
		    		   
		    	   Index index = new Index(requestContext);
		    	   index.response();
		      }
	    });
		
		uploadButton.addClickHandler(new ClickHandler() {
		      public void onClick(ClickEvent event) {
		    	  if(!ApplicationConstants.getCurrentOnlineStatus()) {
		    		  return;
		    	  }
		    	  BaseTemplate operationUi = new BaseTemplate();
		    	  operationUi.showGlassDoorMessage("<img style='margin-bottom: -3px;' src='/media/img/admin/ajax-loader.gif' /> Uploading your data to the main server" +
		    	  		"<br /><div id='progressBar'></div>");
		    	  EventBus.get().addHandler(ProgressEvent.TYPE, new IndexTemplate());
		    	  RequestContext requestContext = new RequestContext(RequestContext.METHOD_POST);
		    	  requestContext.getArgs().put("action", "sync");
		    	  Index index = new Index(requestContext);
		    	  index.response();
		      }
	    });
		
		downloadButton.addClickHandler(new ClickHandler() {
		      public void onClick(ClickEvent event) {
		    	  if(!ApplicationConstants.getCurrentOnlineStatus()) {
		    		  return;
		    	  }
		    	  BaseTemplate operationUi = new BaseTemplate();
		    	  operationUi.showGlassDoorMessage("<img style='margin-bottom: -3px;' src='/media/img/admin/ajax-loader.gif' /> Downloading your data from the main server" +
		    	  		"<br /><div id='progressBar'></div>");
		    	  EventBus.get().addHandler(ProgressEvent.TYPE, new IndexTemplate());
		    	  RequestContext requestContext = new RequestContext(RequestContext.METHOD_POST);
		    	  requestContext.getArgs().put("action", "resync");
		    	  Index index = new Index(requestContext);
		    	  index.response();
		      }		      
	    });
	}
	
	private void addHyperlink(String id, String linkTxt, String tokenTxt, final BaseServlet servlet) {
		Hyperlink link = new Hyperlink(linkTxt, true, tokenTxt); 
		link.addClickHandler(new ClickHandler() {
			public void onClick(ClickEvent event) {
				Template.addLoadingMessage();
				servlet.response();
			}	
		});
		RootPanel.get(id).add(link);
	}
	
	@Override
	public void fill() {
		IndexData.Data indexPageData = (Data) this.requestContext.getArgs().get("index_page_data");
		super.setBodyStyle("dashboard");
		HTMLPanel indexHtml = new HTMLPanel(indexContentHtml);
		super.setContentPanel(indexHtml);
		super.fill();
		RequestContext requestContext = null;
		requestContext = new RequestContext();
		
		requestContext.getArgs().put("action", "list");
		requestContext.getArgs().put("pageNum", "1");
		addHyperlink("aa-1", "<a  href='#dashboard/animatorassignedvillage/'>Animator assigned villages</a>", "dashboard/animatorassignedvillage", new AnimatorAssignedVillages(requestContext));
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "add");
		addHyperlink("aa-2", "<a  href='#dashboard/animatorassignedvillage/add' class='addlink'>Add</a>", "dashboard/animatorassignedvillage/add", new AnimatorAssignedVillages(requestContext));
		
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "list");
		requestContext.getArgs().put("pageNum", "1");
		addHyperlink("a-1", "<a href='#dashboard/animator/'>Animators</a>", "dashboard/animator", new Animators(requestContext));
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "add");
		addHyperlink("a-2", "<a href='#dashboard/animator/add' class='addlink'>Add</a>", "dashboard/animator/add", new Animators(requestContext));
		
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "list");
		requestContext.getArgs().put("pageNum", "1");
		addHyperlink("b-1", "<a href='#dashboard/block/'>Blocks</a>", "dashboard/block", new Blocks(requestContext));
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "add");
		addHyperlink("b-2", "<a href='#dashboard/block/add' class='addlink'>Add</a>", "dashboard/block/add", new Blocks(requestContext));
		
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "list");
		requestContext.getArgs().put("pageNum", "1");
		addHyperlink("d-1", "<a href='#dashboard/developmentmanager/'>Development managers</a>", "dashboard/developmentmanager", new DevelopmentManagers(requestContext));
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "add");
		addHyperlink("d-2", "<a href='#dashboard/developmentmanager/add' class='addlink'>Add</a>", "dashboard/developmentmanager/add", new DevelopmentManagers(requestContext));
		
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "list");
		requestContext.getArgs().put("pageNum", "1");
		addHyperlink("di-1", "<a href='#dashboard/district/'>Districts</a>", "dashboard/district", new Districts(requestContext));
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "add");
		addHyperlink("di-2", "<a href='#dashboard/district/add' class='addlink'>Add</a>", "dashboard/district/add", new Districts(requestContext));
		
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "list");
		requestContext.getArgs().put("pageNum", "1");
		addHyperlink("e-1", "<a href='#dashboard/equipment/'>Equipments</a>", "dashboard/equipment", new Equipments(requestContext));
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "add");
		addHyperlink("e-2", "<a href='#dashboard/equipment/add' class='addlink'>Add</a>", "dashboard/equipment/add", new Equipments(requestContext));

		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "list");
		requestContext.getArgs().put("pageNum", "1");
		addHyperlink("f-1", "<a href='#dashboard/fieldofficer/'>Field officers</a>", "dashboard/fieldofficer", new FieldOfficers(requestContext));
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "add");
		addHyperlink("f-2", "<a href='#dashboard/fieldofficer/add' class='addlink'>Add</a>", "dashboard/fieldofficer/add", new FieldOfficers(requestContext));

		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "list");
		requestContext.getArgs().put("pageNum", "1");
		addHyperlink("l-1", "<a href='#dashboard/language/'>Languages</a>", "dashboard/language", new Languages(requestContext));
		requestContext = new RequestContext();	
		requestContext.getArgs().put("action", "add");
		addHyperlink("l-2", "<a href='#dashboard/language/add' class='addlink'>Add</a>", "dashboard/language/add", new Languages(requestContext));
		
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "list");
		requestContext.getArgs().put("pageNum", "1");
		addHyperlink("p-1", "<a href='#dashboard/partners/'>Partners</a>", "dashboard/partners", new Partners(requestContext));
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "add");
		addHyperlink("p-2", "<a href='#dashboard/partners/add' class='addlink'>Add</a>", "dashboard/partners/add", new Partners(requestContext));
		
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "list");
		requestContext.getArgs().put("pageNum", "1");
		addHyperlink("pg-1","<a href='#dashboard/persongroups/'>Person groups</a>", "dashboard/persongroups", new PersonGroups(requestContext));
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "add");
		addHyperlink("pg-2","<a href='#dashboard/persongroups/add' class='addlink'>Add</a>", "dashboard/persongroups/add", new PersonGroups(requestContext));
		
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "list");
		requestContext.getArgs().put("pageNum", "1");
		addHyperlink("pe-1", "<a href='#dashboard/person/'>Persons</a>", "dashboard/person", new Persons(requestContext));
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "add");
		addHyperlink("pe-2", "<a href='#dashboard/person/add' class='addlink'>Add</a>", "dashboard/person/add", new Persons(requestContext));
	
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "list");
		requestContext.getArgs().put("pageNum", "1");
		addHyperlink("pr-1", "<a href='#dashboard/practices/'>Practices</a>", "dashboard/practices", new Practices(requestContext));
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "add");
		addHyperlink("pr-2", "<a href='#dashboard/practices/add' class='addlink'>Add</a>", "dashboard/practices/add", new Practices(requestContext));

		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "list");
		requestContext.getArgs().put("pageNum", "1");
		addHyperlink("r-1", "<a href='#dashboard/region/'>Regions</a>", "dashboard/region", new Regions(requestContext));
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "add");
		addHyperlink("r-2", "<a href='#dashboard/region/add' class='addlink'>Add</a>", "dashboard/region/add", new Regions(requestContext));
		
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "list");
		requestContext.getArgs().put("pageNum", "1");
		addHyperlink("s-1", "<a href='#dashboard/screening/'>Screenings</a>", "dashboard/screening", new Screenings(requestContext));
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "add");
		addHyperlink("s-2", "<a href='#dashboard/screening/add' class='addlink'>Add</a>", "dashboard/screening/add", new Screenings(requestContext));
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "list");
		requestContext.getArgs().put("pageNum", "1");
		addHyperlink("st-1", "<a id='st-1' href='#dashboard/state/'>States</a>", "dashboard/state", new States(requestContext));
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "add");
		addHyperlink("st-2", "<a id='st-2' href='#dashboard/state/add' class='addlink'>Add</a>", "dashboard/state/add", new States(requestContext));

		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "list");
		requestContext.getArgs().put("pageNum", "1");
		addHyperlink("t-1", "<a href='#dashboard/training/'>Trainings</a>", "dashboard/training", new Trainings(requestContext));
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "add");
		addHyperlink("t-2", "<a href='#dashboard/training/add' class='addlink'>Add</a>", "dashboard/training/add", new Trainings(requestContext));

		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "list");
		requestContext.getArgs().put("pageNum", "1");
		addHyperlink("v-1", "<a href='#dashboard/video/'>Videos</a>", "dashboard/video", new Videos(requestContext));
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "add");
		addHyperlink("v-2", "<a href='#dashboard/video/add' class='addlink'>Add</a>", "dashboard/video/add", new Videos(requestContext));

		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "list");
		requestContext.getArgs().put("pageNum", "1");
		addHyperlink("vi-1", "<a href='#dashboard/village/'>Villages</a>", "dashboard/village", new Villages(requestContext));
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "add");
		addHyperlink("vi-2", "<a href='#dashboard/village/add' class='addlink'>Add</a>", "dashboard/village/add", new Villages(requestContext));
		
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "list");
		requestContext.getArgs().put("pageNum", "1");
		addHyperlink("tar-1", "<a href='#dashboard/target/'>Targets</a>", "dashboard/target", new Targets(requestContext));
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "add");
		addHyperlink("tar-2", "<a href='#dashboard/target/add' class='addlink'>Add</a>", "dashboard/target/add", new Targets(requestContext));
		
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "list");
		requestContext.getArgs().put("pageNum", "1");
		addHyperlink("pap-1", "<a  href='#dashboard/personadoptpractice/'>Person Adopt Practice</a>", "dashboard/personadoptpractice", new PersonAdoptPractices(requestContext));
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "add");
		addHyperlink("pap-2", "<a  href='#dashboard/personadoptpractice/add' class='addlink'>Add</a>", "dashboard/personadoptpractice/add", new PersonAdoptPractices(requestContext));
		
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "add");
		requestContext.getArgs().put("pageNum", "1");
		addHyperlink("der-1", "<a href='#dashboard/error/'>Data Inconsistencies</a>", "dashboard/error", new DashboardError(requestContext));
		String tot_errors = indexPageData.getDashboardErrorCount();
		Label error_label = new Label();
		//Determine style
		if(tot_errors!=null && Integer.parseInt(tot_errors)!=0)
			error_label.addStyleName("error");
		else
			error_label.addStyleName("noerror");
		//Determine suffix
		if(tot_errors==null)
			tot_errors = "NA";
		else if(Integer.parseInt(tot_errors) > 1)
			tot_errors += " errors";
		else
			tot_errors += " error";
		
		error_label.setText(tot_errors);
		RootPanel.get("der-2").add(error_label);
		
		
		HTMLPanel h = new HTMLPanel("<div id='controlPanel'></div>");
		h.setStyleName("mainControlPanelArea");
		RootPanel.get("sub-container").add(h);
		HTMLPanel bulletsHtml = new HTMLPanel(this.bulletsBodyHtml);
		bulletsHtml.setStyleName("bulletsClass");
		RootPanel.get("sub-container").add(bulletsHtml);
		goOfflineOnline();
	}
	
	final static private String bulletsBodyHtml = 
		"<div class='instructionsClass'>Instructions & Tips</div>" + 
		"<div id='bullet1' class='bulletPointClass'>" +
			"<img src='/media/img/admin/bulletpoint.png' />" + 
			"<div id='text1' class='textClass'>" +
				"Before going offline, click on the 'Download' button to download a local copy " +
				"of the main server to your browser.  Then click on the 'Go Offline' button to access " +
				"and add information in offline mode." + 
			"</div>" + 
		"</div>" +
		"<div id='bullet2' class='bulletPointClass'>" +
			"<img src='/media/img/admin/bulletpoint.png' />" + 
			"<div id='text2' class='textClass'>" +
				"You can now edit or add " +
				"information in offline mode.  After you're done, click on the 'Go Online' button to " +
				"upload any newly edited or added information to the main server.  You can do this by clicking " +
				"on the 'Upload' button." +
			"</div>" + 
		"</div>" +
		"<div id='bullet3' class='bulletPointClass'>" +
			"<img src='/media/img/admin/bulletpoint.png' />" + 
			"<div id='text3' class='textClass'>" +
				"Make sure you have internet access before clicking on the 'Go Online' button.  Some level of " +
				"internet access is necessary to download and upload data to the main server." +
			"</div>" + 
		"</div>";
		
	
	final static private String bodyContentHtml = 
		"<div style='font-size: 20px; width: 375px; color: rgb(65, 118, 144);'>Welcome to COCO, DigitalGreen's " +
				"connect-online, connect-offline system -- from anywhere, to everywhere.</div>" +	
		"<table cellspacing='0' cellpadding='0' class='controlPanelClass'>" +
			"<tbody>" +
				"<tr>" +
					"<td align='center' style='vertical-align: top; border-width: 0px; padding: 0px;'>" +
						"<table cellspacing='0' cellpadding='0' width='100%' height='40px'>" +
							"<tbody>" +
								"<tr>" +
									"<td style='width:100%; align: left; border-width: 0px; padding: 0px; padding-top: 2px;'>" +
										"<div id='modeTextId'>" +
											"<div id='modeIconId' style='float: right; margin-right: 15px;'>" +
											"</div>" +
										"</div>" +
									"</td>" +
								"</tr>" +
							"</tbody>" +
						"</table>" +
					"</td>" +
				"</tr>" +
				"<tr>" +
					"<td align='center' style='vertical-align: top; border-width: 0px'>" +
						"<table cellspacing='0' cellpadding='0'>" +
							"<tbody>" +
								"<tr>" +
									"<td align='left' style='vertical-align: top; border-width: 0px; padding-top: 0px;'>" +
										"<img id='onlineOfflineButtonId' src='' />" +
									"</td>" +
								"</tr>" +
							"</tbody>" +
						"</table>" +
					"</td>" +
				"</tr>" +
				"<tr>" +
					"<td align='left' style='vertical-align: top; border-width: 0px; padding-top: 0px;'>" +
						"<table cellspacing='0' cellpadding='0'>" +
							"<tbody>" +
								"<tr>" +
									"<td align='left' style='vertical-align: top; border-width: 0px;'>" +
										"<img id='downloadButtonId' src='/media/img/admin/download-icon.png' width='150px' height='60px' />" +
									"</td>" +
									"<td width='30px' style='border-width: 0px;'></td>" + 
									"<td align='left' style='vertical-align: top; border-width: 0px;'>" +
										"<img id='uploadButtonId' src='/media/img/admin/upload-icon.png' width='150px' height='60px' />" +
									"</td>" +
								"</tr>" +
							"</tbody>" +
						"</table>" +
					"</td>" +
				"</tr>" +
			"</tbody>" +
		"</table>";
	
	final static private String indexContentHtml = "<div id='content' style='float:left;'>" +
							"<h1>Administration</h1>" +
								"<div id='content-main'>" +
									"<div class='module'>" +
     								"<table summary='Models available in the Dashboard application.'>" +
     									"<caption><a href='dashboard/' class='section'>Dashboard</a></caption>" +
     										"<tr>" +
	     										"<th id='r-1' scope='row'>" +
	 											"</th>" +
	 											"<td id='r-2'>" +
	 											"</td>" +
	 										"</tr>" +
     										"<tr>" +
     											"<th id='st-1' scope='row'>" +
     											"</th>" +
     											"<td id='st-2'>" +
     											"</td>" +
     										"</tr>" +
     										"<tr>" +
 											
     											"<th id='di-1' scope='row'>" +
     											"</th>" +
     											"<td id='di-2'>" +
     											"</td>" +
     										"</tr>" +
     										"<tr>" +
     											"<th id='b-1' scope='row'>" +
     											"</th>" +
     											"<td id='b-2'>" +
     											"</td>" +
     										"</tr>" +
     										"<tr>" +
     											"<th id='vi-1' scope='row'>" +
     											"</th>"  +
     											"<td id='vi-2'>" +
     											"</td>" +
     										"</tr>" +
     										"<tr>" +
     											"<th id='a-1' scope='row'>" +
     											"</th>" +
     											"<td id='a-2'>" +
     											"</td>" +
     										"</tr>" +
     										"<tr>" +
     											"<th id='aa-1' scope='row'>" +
     											"</th>" +
     											"<td id='aa-2'>" +
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
	 											"<th id='pap-1'scope='row'>" +
	 											"</th>" +
	 											"<td id='pap-2'>" +
	 											"</td>" +
	 										"</tr>" +
     										"<tr>" +
     											"<th id='l-1' scope='row'>" +
     											"</th>" +
     											"<td id='l-2'>" +
     											"</td>" +
     										"</tr>" +
     										"<tr>" +
     											"<th id='v-1' scope='row'>" +
     											"</th>" +
     											"<td id='v-2'>" +
     											"</td>" +
     										"</tr>" +
     										"<tr>" +
     											"<th id='s-1' scope='row'>" +
     											"</th>" +
     											"<td id='s-2'>" +
     											"</td>" +
     										"</tr>" +
     										"<tr>" +
     											"<th id='e-1' scope='row'>" +
     											"</th>" +
     											"<td id='e-2'>" +
     											"</td>" +
     										"</tr>" +
     										"<tr>" +
     											"<th id='t-1' scope='row'>" +
     											"</th>" +
     											"<td id='t-2'>" +
     											"</td>" +
     										"</tr>" +
     										"<tr>" +
 												"<th id='tar-1' scope='row'>" +
 												"</th>" +
 												"<td id='tar-2'>" +
 												"</td>" +
 											"</tr>" +
     										"<tr>" +
 											"<th id='p-1' scope='row'>" +
 											"</th>" +
 											"<td id='p-2'>" +
 											"</td>" +
 										"</tr>" +
 										"<tr>" +
											"<th id='d-1' scope='row'>" +
											"</th>" +
											"<td id='d-2'>" +
											"</td>" +
										"</tr>" +
										"<tr>" +
											"<th id='f-1' scope='row'>" +
											"</th>" +
											"<td id='f-2'>" +
											"</td>" +
										"</tr>" +
     									"</table>" +
     								"</div>" +
     							"</div>" +
     							"<div id='dashboard-tools' style='clear:both; width:100%;'>" +
								"<div class='module'>" +
 								"<table summary='Tools available in the Dashboard application.'>" +
 									"<caption><a href='#' class='section'>Tools</a></caption>" +
 									"<tr>" +
										"<th id='der-1' scope='row'>" +
										"</th>" +
										"<td id='der-2'>" +
										"</td>" +
									"</tr>" +
										"</table>" +
									"</div>" +
								"</div>";

}
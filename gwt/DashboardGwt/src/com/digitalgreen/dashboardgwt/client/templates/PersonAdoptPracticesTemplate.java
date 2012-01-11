package com.digitalgreen.dashboardgwt.client.templates;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map.Entry;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.PersonAdoptPracticeData;
import com.digitalgreen.dashboardgwt.client.servlets.PersonAdoptPractices;
import com.google.gwt.event.dom.client.ChangeEvent;
import com.google.gwt.event.dom.client.ChangeHandler;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.HTMLPanel;
import com.google.gwt.user.client.ui.Hyperlink;
import com.google.gwt.user.client.ui.ListBox;
import com.google.gwt.user.client.ui.RootPanel;
import com.google.gwt.user.client.ui.VerticalPanel;

public class PersonAdoptPracticesTemplate extends BaseTemplate {
	
	private LinkedHashMap<String, ListBox> addPageFilterListBoxMap = null;

	public PersonAdoptPracticesTemplate(RequestContext requestContext) {
		super(requestContext);
		this.formTemplate = new Form((new PersonAdoptPracticeData()).getNewData());
	}
	
	@Override
	public void fill() {
		String templateType = "PersonAdoptPractice";
		String templatePlainType = "dashboard/personadoptpractice/add";
		RequestContext requestContext = new RequestContext();
		HashMap args = new HashMap();
		args.put("action", "add");
		requestContext.setArgs(args);
		requestContext.setForm(this.formTemplate);
		RequestContext saveRequestContext = new RequestContext(RequestContext.METHOD_POST);
		PersonAdoptPractices addPersonAdoptPracticesServlet1 = new PersonAdoptPractices(requestContext);
		saveRequestContext.setForm(this.formTemplate);
		PersonAdoptPractices savePersonAdoptPractice = new PersonAdoptPractices(saveRequestContext);
		// Draw the content of the template depending on the request type (GET/POST)
		fillDGTemplate(templateType, personadoptpracticeListHtml, personadoptpracticeAddHtml, personadoptpracticeFilterHtmL, addDataToElementID);
		// Add it to the rootpanel
		super.fill();
		//Now add listings
		List<Hyperlink> links = this.fillListings();
		// Now add hyperlinks
		super.fillDgListPage(templatePlainType, templateType, personadoptpracticeListFormHtml, addPersonAdoptPracticesServlet1, links);
		this.displayCalendar();
		// Now add any submit control buttons
		super.fillDgFormPage(savePersonAdoptPractice);
		this.initializeFilters();
	}
	
	private void fillDGTemplate(String templateType, 
			  String listHtml,
			  String addHtml,
			  String filterHtml, String addDataToElementID[]) {
		HashMap queryArgs = this.getRequestContext().getArgs();
		if(queryArgs.get("action").equals("add") && !this.getRequestContext().hasErrorMessages()) {
			super.fillDGTemplate(templateType, listHtml, addHtml, new String[0]);
			HTMLPanel filterPanel = new HTMLPanel(filterHtml);
			String addData = (String)queryArgs.get("addPageData");
			if(addData != null) {
				HTMLPanel h = new HTMLPanel(addData);
				filterPanel.getElementById("id_district").setInnerHTML(h.getElementById("id_district").getInnerHTML());
			}

			VerticalPanel vPanel = new VerticalPanel();
			vPanel.add(filterPanel);
			vPanel.add(super.getContentPanel());
			super.setContentPanel(vPanel);
		}
		else {
			super.fillDGTemplate(templateType, listHtml, addHtml, addDataToElementID);
		}
	}
	
	@Override
	public void ajaxFill(RequestContext ajaxRC) {
		super.ajaxFill(ajaxRC);
		Object action = ajaxRC.getArgs().get("action");
		ListBox newBox = null;
		BaseTemplate operationsUI = new BaseTemplate();
		operationsUI.hideGlassDoorMessage();
		if(action.equals("person-select")) {
			newBox = this.addPageFilterListBoxMap.get("id_video");
		}
		else if(action.equals("district-select")) {
			newBox = this.addPageFilterListBoxMap.get("id_block");
		}
		else if(action.equals("block-select")) {
			newBox = this.addPageFilterListBoxMap.get("id_village");
		}
		else if(action.equals("village-select")) {
			newBox = this.addPageFilterListBoxMap.get("id_person_group");
		}
		else if(action.equals("person_group-select")) {
			newBox = this.addPageFilterListBoxMap.get("id_person");
		}
		
		if(newBox != null) {
			newBox.setEnabled(true);
			newBox.getElement().setInnerHTML(ajaxRC.getArgs().get("ajax_data").toString());
		}
		
		
	}
	
	public void initializeFilters() {
		boolean addCase = false;
		if(this.requestContext.getArgs().get("action").equals("add")) {
			addCase = true;
		}
		else if(this.requestContext.getArgs().get("action").equals("edit")) {
			addCase = false;
		}
		else {
			return;
		}
		
		this.addPageFilterListBoxMap = new LinkedHashMap<String, ListBox>();
		if(addCase  && !this.requestContext.hasErrorMessages()) {
			this.addPageFilterListBoxMap.put("id_district", ListBox.wrap(RootPanel.get("id_district").getElement()));
			this.addPageFilterListBoxMap.put("id_block", ListBox.wrap(RootPanel.get("id_block").getElement()));
			this.addPageFilterListBoxMap.put("id_village", ListBox.wrap(RootPanel.get("id_village").getElement()));
			this.addPageFilterListBoxMap.put("id_person_group", ListBox.wrap(RootPanel.get("id_person_group").getElement()));
		}
		this.addPageFilterListBoxMap.put("id_person", ListBox.wrap(RootPanel.get("id_person").getElement()));
		this.addPageFilterListBoxMap.put("id_video", ListBox.wrap(RootPanel.get("id_video").getElement()));
		
		for (Entry<String, ListBox> pair : this.addPageFilterListBoxMap.entrySet()) {
			if(pair.getKey() != "id_district" && addCase && !this.requestContext.hasErrorMessages()) {
				pair.getValue().setEnabled(false);
			}
			
			if(pair.getKey() != "id_video") {
				pair.getValue().addChangeHandler(new filterListBoxOnChangeHandler((HashMap<String, ListBox>) this.addPageFilterListBoxMap.clone(), this));
			}
				
		}
		
	}
	
	private class filterListBoxOnChangeHandler implements ChangeHandler {
		private HashMap<String, ListBox> allListBoxMap = null;
		private BaseTemplate callerTemplate = null;
		
		public filterListBoxOnChangeHandler(HashMap<String, ListBox> objects,BaseTemplate in_callerTemplate) {
			this.allListBoxMap = objects;
			this.callerTemplate = in_callerTemplate;
		}
		

		@Override
		public void onChange(ChangeEvent event) {
			ListBox source = (ListBox) event.getSource();
			String source_id = source.getElement().getId();
			ListBox next = null;
			
			boolean startDisable = false;
			ListBox[] allListBox = allListBoxMap.values().toArray(new ListBox[allListBoxMap.size()]);
			for(int i=0; i < allListBox.length; i++) {
				if(startDisable) {
					allListBox[i].setItemSelected(0, true);
					allListBox[i].setEnabled(false);
				}
				else {
					if(allListBox[i].getElement().getId().equals(source_id)) {
						next = allListBox[i+1];
						startDisable = true;
					}
				}
			}
			
			//Set the remaining ones to zero index and disable them
			int selectedIndex = source.getSelectedIndex();
			if(selectedIndex == 0 || selectedIndex == -1) {
				return;
			}
			
			BaseTemplate operationsUI = new BaseTemplate();
			operationsUI.showGlassDoorMessage("Loading " + next.getElement().getId().substring(3).replace('_', ' ') + "s..");
			
			RequestContext requestContext = new RequestContext();
			requestContext.getArgs().put("action", source_id.substring(3)+"-select");
			requestContext.getArgs().put(source_id.substring(3)+"_id", source.getValue(source.getSelectedIndex()).toString());
			
			//This is a special case for Person Group select, if the desired farmer doesn't belong to any group, we'll filter all
			//farmers belonging to the selected village with group_id = null
			if(requestContext.getArgs().get("action").equals("person_group-select")) {
				ListBox villageListBox = this.allListBoxMap.get("id_village");
				requestContext.getArgs().put("village_id", villageListBox.getValue(villageListBox.getSelectedIndex()).toString());
			}
			
			PersonAdoptPractices pap = new PersonAdoptPractices(requestContext);
			pap.ajaxResponse(callerTemplate);
			
		}
	}
	
	protected List<Hyperlink> fillListings() {
		HashMap queryArgs = this.getRequestContext().getArgs();
		String queryArg = (String)queryArgs.get("action");
		List<Hyperlink> links = new ArrayList<Hyperlink>();
		// If we're unsure, just default to list view
		if(queryArg.equals("list")) {
			// 	Add Listings
			List personAdoptPractices = (List)queryArgs.get("listing");			
			if(personAdoptPractices  != null){
				String tableRows ="";
				String style;
				PersonAdoptPracticeData.Data personAdoptPractice;
				RequestContext requestContext = null;
				String group="",village="";
				for (int row = 0; row < personAdoptPractices.size(); ++row) {
					if(row%2==0)
						style= "row2";
					else
						style = "row1";
					personAdoptPractice = (PersonAdoptPracticeData.Data) personAdoptPractices.get(row);
					if(personAdoptPractice.getGroup() == null){
						group = "null";
					} else {
						group = personAdoptPractice.getGroup().getPersonGroupName();
					}
						village = personAdoptPractice.getVillage().getVillageName();
						
					requestContext = new RequestContext();
					requestContext.getArgs().put("action", "edit");
					requestContext.getArgs().put("id", personAdoptPractice.getId());
					requestContext.setForm(this.formTemplate);
					links.add(this.createHyperlink("<a href='#dashboard/personadoptpractice/" + personAdoptPractice.getId() + "/'>" +
							personAdoptPractice.getPerson().getPersonName() +"</a>",
							"dashboard/personadoptpractice/" + personAdoptPractice.getId() +"/",
							new PersonAdoptPractices(requestContext)));
					String video;
					if(personAdoptPractice.getVideo() == null){
						video = "null";
					} else {
						video = personAdoptPractice.getVideo().getTitle();
					}
					tableRows += "<tr class='" + style + "'>" +
									  "<td><input type='checkbox' class='action-select' value='" + personAdoptPractice.getId() + "' name='_selected_action' /></td>" +
									  "<th id = 'row" + row + "'></th>" +
									  "<td>"+ group + "</td>"+
									  "<td>"+ village + "</td>" +
										"<td>" + video + "</td>" +
									"</tr>";
				}
				personadoptpracticeListFormHtml = personadoptpracticeListFormHtml + tableRows + "</tbody></table>";
			}
		}
		return links;
	}	
	//Loading javascript for displaying calendar in Google chrome browser
	public static native void displayCalendar() /*-{
		$wnd.DateTimeShortcuts.init();		
	}-*/;
	final private String addDataToElementID[] = {"id_person", "id_video"};
	
	private String personadoptpracticeListFormHtml = "<div class = 'toolbar'><label for='searchbar'>" +
									"<img alt='Search' src='/media/img/admin/icon_searchbox.png'></label>" +
									"<input type='text' id='searchbar' value='' name='q' size='40'>" +
									"<input id='search' type='button' value='Search'>" +
								"</div>"+
								"<div class='actions'>" +
								"<label>Action: <select name='action'>" +
									"<option value='' selected='selected'>---------</option>" +
									"<option value='delete_selected'>Delete selected person adopt practices</option>" +
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
												"Person" +
											"</a>" +
										"</th>" +
										"<th>" +
										"<a href='?ot=asc&amp;o=2'>" +
											"Group" +
										"</a>" +
									"</th>" +
									"<th>" +
										"<a href='?ot=asc&amp;o=3'>" +
											"Village" +
										"</a>" +
									"</th>" +
										"<th>" +
										"<a href='?ot=asc&amp;o=2'>" +
											"Video" +
										"</a>" +
									"</th>" +
									"</tr>" +
								"</thead>" +
								"<tbody>";

	
	// Fill ids:  listing-form-body, add-link
	private String personadoptpracticeListHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
							"<div id='content' class='flex'>" +
							"<h1>Select Person Adopt Practices to change</h1>" +
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
	
	private String personadoptpracticeFilterHtmL = "<div id='filter_html'>"+
												   "<label for='id_district' class='required'>District:</label>" +
														"<select name='district' id='id_district'>" +
														"<option value='' selected='selected'>---------</option>" +
														"</select>" +
													"<label for='id_block' class='required'>Block:</label>" +
														"<select name='block' id='id_block'>" +
														"<option value='' selected='selected'>---------</option>" +
														"</select>" +
													"<label for='id_village' class='required'>Village:</label>" +
														"<select name='village' id='id_village'>" +
														"<option value='' selected='selected'>---------</option>" +
														"</select>" +
													"<label for='id_person_group' class='required'>Person Group:</label>" +
														"<select name='person_group' id='id_person_group'>" +
														"<option value='' selected='selected'>---------</option>" +
														"</select>" +
												 "</div>";
	
												
	
	private String personadoptpracticeAddHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
						"<div id='content' class='colM'>" +
							"<h1>Add Person Adopt Practice</h1>" +
							"<div id='content-main'>" +
								   "<div>" +
									"<fieldset class='module aligned '>" +
										"<div class='form-row person  '>" +
											"<div>" +
												"<label for='id_person' class='required'>Person:</label>" +
												"<select name='person' id='id_person'>" +
												"<option value='' selected='selected'>---------</option>" +
												"</select>" +
											"</div>" +
										"</div>" +
										"<div class='form-row video '>" +
										"<div>" +
											"<label for='id_video' class='required' >Video:</label>" +
											"<select name='video' id='id_video'>" +
											"<option value='' selected='selected'>---------</option>" +
											"</select>" +
										"</div>" +
									"</div>" +
										"<div class='form-row prior_adoption_flag  '>" +
											"<div>" +
												"<label for='id_prior_adoption_flag' >Prior adoption flag:</label>" +
												"<select id='id_prior_adoption_flag' name='prior_adoption_flag'>" +
												"<option selected='selected' value=''>---------</option>" +
												"<option value='1'>Unknown</option>" +
												"<option value='2'>Yes</option>" +
												"<option value='3'>No</option>" +
												"</select>" +
											"</div>" +
										"</div>"+
										"<div class='form-row date_of_adoption  '>" +
											"<div>" +
												"<label for='id_date_of_adoption' class='required'>Date Of Adoption:</label>" +
												"<input id='id_date_of_adoption' type='text' class='vDateField' name='date_of_adoption' size='10' />"+
											"</div>" +
										"</div>" +
										"<div class='form-row quality  '>" +
											"<div>" +
											"<label for='id_0-quality'>Quality:</label>" +
											"<input type='text' maxlength='200' name='quality' class='vTextField' id='id_quality'>" +
											"</div>" +
										"</div>"+
										"<div class='form-row quantity  '>" +
											"<div>" +
											"<label for='id_quantity'>Quantity:</label>" +
											"<input type='text' name='quantity' class='vIntegerField' id='id_quantity'>" +
											"</div>" +
										"</div>"+
										"<div class='form-row quantity_unit  '>" +
											"<div>" +
											"<label for='id_quantity_unit'>Quantity unit:</label>" +
											"<input type='text' maxlength='150' name='quantity_unit' class='vTextField' id='id_quantity_unit'>" +
											"</div>" +
										"</div>"+
									"</fieldset>" +
									"<div class='submit-row' >"+
										"<input id='save' type='button' value='Save' class='default' name='_save' />" +
									"</div>" +
								"</div>" +
						"</div>";
}
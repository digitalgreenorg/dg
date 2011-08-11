package com.digitalgreen.dashboardgwt.client.templates;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.PersonAdoptPracticeData;
import com.digitalgreen.dashboardgwt.client.servlets.PersonAdoptPractices;
import com.google.gwt.core.client.Scheduler;
import com.google.gwt.core.client.Scheduler.ScheduledCommand;
import com.google.gwt.dev.util.Callback;
import com.google.gwt.event.dom.client.ChangeEvent;
import com.google.gwt.event.dom.client.ChangeHandler;
import com.google.gwt.user.client.Element;
import com.google.gwt.user.client.History;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.Hyperlink;
import com.google.gwt.user.client.ui.ListBox;
import com.google.gwt.user.client.ui.RootPanel;

public class PersonAdoptPracticesTemplate extends BaseTemplate {

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
		super.fillDGTemplate(templateType, personadoptpracticeListHtml, personadoptpracticeAddHtml, addDataToElementID);
		// Add it to the rootpanel
		super.fill();
		//Now add listings
		List<Hyperlink> links = this.fillListings();
		// Now add hyperlinks
		super.fillDgListPage(templatePlainType, templateType, personadoptpracticeListFormHtml, addPersonAdoptPracticesServlet1, links);
		this.displayCalendar();
		// Now add any submit control buttons
		super.fillDgFormPage(savePersonAdoptPractice);
		this.addPracticeFilter();
	}
	
	@Override
	public void ajaxFill(RequestContext ajaxRC) {
		super.ajaxFill(ajaxRC);
		if(ajaxRC.getArgs().get("action").equals("person-select")) {
			BaseTemplate operationsUI = new BaseTemplate();
			operationsUI.hideGlassDoorMessage();
			String html = ajaxRC.getArgs().get("ajax_data").toString();
			final ListBox practiceSelect = ListBox.wrap(RootPanel.get("id_practice").getElement());
			practiceSelect.setEnabled(true);
			practiceSelect.getElement().setInnerHTML(html);
		}
	}
	
	public void addPracticeFilter() {
		if(this.requestContext.getArgs().get("action").equals("add")) {
			final ListBox practiceSelect = ListBox.wrap(RootPanel.get("id_practice").getElement());
			practiceSelect.setEnabled(false);
			
			final ListBox personSelect = ListBox.wrap(RootPanel.get("id_person").getElement());
			
			final BaseTemplate callerTemplate = this;
			
			personSelect.addChangeHandler(new ChangeHandler() {
				
				@Override
				public void onChange(ChangeEvent event) {
					int selectedIndex = personSelect.getSelectedIndex();
					
					if(selectedIndex == 0 || selectedIndex == -1) {
						practiceSelect.setEnabled(false);
						return;
					}
					
					BaseTemplate operationsUI = new BaseTemplate();
					operationsUI.showGlassDoorMessage("Loading Agricultural Practices..");
					
					RequestContext requestContext = new RequestContext();
					requestContext.getArgs().put("action", "person-select");
					requestContext.getArgs().put("person_id", personSelect.getValue(personSelect.getSelectedIndex()).toString());
					PersonAdoptPractices pap = new PersonAdoptPractices(requestContext);
					pap.ajaxResponse(callerTemplate);
				}
			});
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
					tableRows += "<tr class='" + style + "'>" +
									  "<td><input type='checkbox' class='action-select' value='" + personAdoptPractice.getId() + "' name='_selected_action' /></td>" +
									  "<th id = 'row" + row + "'></th>" +
									  "<td>"+ group + "</td>"+
									  "<td>"+ village + "</td>" +
										"<td>" + personAdoptPractice.getPractice().getPracticeName() + "</td>" +
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
	final private String addDataToElementID[] = {"id_person","id_practice"};
	
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
												"Practice" +
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
										"<div class='form-row practice  '>" +
											"<div>" +
												"<label for='id_practice' class='required'>Practice:</label>" +
												"<select name='practice' id='id_practice'>" +
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
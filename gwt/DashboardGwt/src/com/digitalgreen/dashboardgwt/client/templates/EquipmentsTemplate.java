package com.digitalgreen.dashboardgwt.client.templates;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.EquipmentsData;
import com.digitalgreen.dashboardgwt.client.servlets.BaseServlet;
import com.digitalgreen.dashboardgwt.client.servlets.Equipments;
import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.Button;
import com.google.gwt.user.client.ui.Hyperlink;
import com.google.gwt.user.client.ui.RootPanel;

public class EquipmentsTemplate extends BaseTemplate{
	
	public EquipmentsTemplate(RequestContext requestContext) {
		super(requestContext);
		this.formTemplate = new Form((new EquipmentsData()).getNewData());
	}
	
	@Override
	public void fill() {
		String templateType = "Equipment";
		String templatePlainType = "dashboard/equipment/add/";
		RequestContext requestContext = new RequestContext();
		HashMap args = new HashMap();
		args.put("action", "add");
		requestContext.setArgs(args);
		requestContext.setForm(this.formTemplate);
		Equipments addEquipmentsServlet = new Equipments(requestContext);
		RequestContext saveRequestContext = new RequestContext(RequestContext.METHOD_POST);
		saveRequestContext.setForm(this.formTemplate);
		Equipments saveEquipment = new Equipments(saveRequestContext);
				
		// Draw the content of the template depending on the request type (GET/POST)
		super.fillDGTemplate(templateType, equipmentsListHtml, equipmentsAddHtml, addDataToElementID);
		// Add it to the rootpanel
		super.fill();
		
		//Now add listings
		List<Hyperlink> links =  this.fillListings();
		// Now add hyperlinks
		super.fillDgListPage(templatePlainType, templateType, equipmentsListFormHtml, addEquipmentsServlet, links);
		// Now add any submit control buttons
		this.displayCalendar();
		fillDgFormPage(saveEquipment);
	}
	
	protected List<Hyperlink> fillListings() {
		HashMap queryArgs = this.getRequestContext().getArgs();
		String queryArg = (String)queryArgs.get("action");
		List<Hyperlink> links = new ArrayList<Hyperlink>();
		// If we're unsure, just default to list view
		if(queryArg.equals("list")) {
			// 	Add Listings
			List equipments = (List)queryArgs.get("listing");			
			if(equipments  != null){
				String tableRows ="";
				String style;
				EquipmentsData.Data equipment;
				RequestContext requestContext = null;
				for (int row = 0; row < equipments.size(); ++row) {
					if(row%2==0)
						style= "row2";
					else
						style = "row1";
					equipment = (EquipmentsData.Data) equipments.get(row);
					requestContext = new RequestContext();
					requestContext.getArgs().put("action", "edit");
					requestContext.getArgs().put("id", equipment.getId());
					requestContext.setForm(this.formTemplate);
					links.add(this.createHyperlink("<a href='#dashboard/equipment/" + equipment.getId() + "/'>" +
							equipmentType[Integer.parseInt(equipment.getEquipmentType())-1] + "</a>", 
							"dashboard/equipment/" + equipment.getId() + "/",
							new Equipments(requestContext)));
					tableRows += "<tr class='" + style + "'>" +
								  "<td><input type='checkbox' class='action-select' value='"+ equipment.getId() + "' name='_selected_action' /></td>" +
								  "<th id = 'row" + row + "'></th>" +
									"<td>"+ equipment.getModelNo()+ "</td>" +
									"<td>"+ equipment.getInvoiceNo()+ "</td>" +
									"<td>"+ equipment.getVillage().getVillageName() + "</td>" +
									"<td>"+ equipment.getProcurementDate() + "</td>" +
									"<td>"+ equipment.getRemarks() + "</td>" +
								"</tr>";
					
					}
				equipmentsListFormHtml = equipmentsListFormHtml + tableRows + "</tbody></table>";
			}
		}
		return links;
	}
	
	@Override 
	protected void fillDgFormPage(final BaseServlet servlet) {
		super.fillDgFormPage(servlet);
		Button b = Button.wrap(RootPanel.get("save_and_add_another").getElement());
		b.addClickHandler(new ClickHandler() {
			// This gets executed on a POST request.
			public void onClick(ClickEvent event) {
				Template.addLoadingMessage();
				// The query string can only be formed if we're on the page with 
				// the add-form id, set when we got a GET request on the page
				String formQueryString = BaseTemplate.getFormString("add-form");
				servlet.getRequestContext().getForm().setQueryString(formQueryString);
				//to save and add another button.
				servlet.getRequestContext().getArgs().put("redirect_to", "add");
				servlet.response();
			}
	    });		
	}
	
	//Loading javascript for displaying calendar in Google chrome browser
	public static native void displayCalendar() /*-{
		$wnd.DateTimeShortcuts.init();		
	}-*/;	

	final private String addDataToElementID[] = {"id_village", "id_equipmentholder"};
	
	final private String equipmentType[] = {"Pico Projector", "Speaker", "Camera", "Tripod", 
	"Battery", "Battery Charger", "Laptop", "Computer", "Television set", "DVD player", 
	"Headphone", "Microphone", "Hard disk", "Pen drive", "UPS", "Cycle", "Chair",
	"Table", "Almirah", "Bag", "Other" };
	
	private String equipmentsListFormHtml = "<div class = 'toolbar'><label for='searchbar'>" +
									"<img alt='Search' src='/media/img/admin/icon_searchbox.png'></label>" +
									"<input type='text' id='searchbar' value='' name='q' size='40'>" +
									"<input id='search' type='button' value='Search'>" +
								"</div>" +
								"<div class='actions'>" +
									"<p> Search by Id, Village, Model No, Invoice No, ProcurementDate, Remarks </p>" +
								"</div>"+
								"<table cellspacing='0'>" + 
									"<thead>" + 
										"<tr>" + 
											"<th>" +
												"<input type='checkbox' id='action-toggle' />" + 
											"</th>" +
											"<th>" +
												"<a href='?ot=asc&amp;o=1'> Equipment type </a>" +
											"</th>" +
											"<th>" +
												"<a href='?ot=asc&amp;o=2'> Make / Model No </a>" +
											"</th>" +
											"<th>" +
												"<a href='?ot=asc&amp;o=3'> Invoice no </a>" +
												"</th>" +
											"<th>" +
												"<a href='?ot=asc&amp;o=4'> Village </a>" +
											"</th>" +
											"<th>" +
											"<a href='?ot=asc&amp;o=6'> Procurement Date </a>" +
											"</th>" +
											"<th>" +
												"<a href='?ot=asc&amp;o=6'> Remarks </a>" +
											"</th>" +
										"</tr>" + 
									"</thead>" + 
									"<tbody>";
	
	final private String equipmentsListHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
									"<div id='content' class='flex'>" +
										"<h1>Select Equipment to change</h1>" +
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
	
	final private String equipmentsAddHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" + 
	"<div id='content' class='colM'>" +
		"<h1>Add equipment</h1>" +
		"<div id='content-main'>" +
			"<fieldset class='module aligned '>" +
				"<div class='form-row equipment_type  '>" +
					"<div>" +
						"<label for='id_equipment_type' class='required'>Equipment type:</label>" +
						"<select name='equipment_type' id='id_equipment_type'>" +
							"<option value='' selected='selected'>---------</option>" +
							"<option value='1'>Pico Projector</option>" +
							"<option value='2'>Speaker</option>" +
							"<option value='3'>Camera</option>" + 
							"<option value='4'>Tripod</option>" + 
							"<option value='5'>Battery</option>" +
							"<option value='6'>Battery Charger</option>" +
							"<option value='7'>Laptop</option>" +
							"<option value='8'>Computer</option>" +
							"<option value='9'>Television set</option>" +
							"<option value='10'>DVD player</option>" +
							"<option value='11'>Headphone</option>" +
							"<option value='12'>Microphone</option>" +
							"<option value='13'>Hard disk</option>" +
							"<option value='14'>Pen drive</option>" +
							"<option value='15'>UPS</option>" +
							"<option value='16'>Cycle</option>" +
							"<option value='17'>Chair</option>" +
							"<option value='18'>Table</option>" +
							"<option value='19'>Almirah</option>" +
							"<option value='20'>Bag</option>" +
							"<option value='21'>Other</option>" +
						"</select>" +
					"</div>" +
				"</div>" +
				
				"<div class='form-row other_equipment'>" +
					"<div>" +
						"<label for='id_other_equipment'>Specify the equipment if &#39;Other&#39; equipment type has been selected :</label>" +
						"<input id='id_other_equipment' type='text' class='vTextField' name='other_equipment' maxlength='300' />" +								          
					"</div>" +
				"</div>" +
				
				"<div class='form-row invoice_no'>"+
                	"<div>" +
                		"<label class='required' for='id_invoice_no'>Invoice no:</label><input type='text' maxlength='300' " +
                			"name='invoice_no' class='vTextField' id='id_invoice_no'>" +
                	"</div>" +
                "</div>"+
				
				"<div class='form-row model_no'>" +
				 	"<div>" +									          
				 		"<label for='id_model_no'>Make / Model No :</label>" +
				 		"<input id='id_model_no' type='text' class='vTextField' name='model_no' maxlength='300' />" +
				 	"</div>" +
				"</div>" +
				
				"<div class='form-row serial_no'>"+
			    	"<div>"+
			              "<label for='id_serial_no'>Serial no:</label>" +
			              "<input id='id_serial_no' type='text' class='vTextField' name='serial_no' maxlength='300' />" +
			        "</div>" +
			    "</div>" +
			  
			    "<div class='form-row cost'>" +
			    	"<div>"+
			    		"<label for='id_cost'>Cost:</label>" +
			    		"<input type='text' name='cost' id='id_cost' />" +
			    	"</div>" +
			    "</div>" +
			  
			    "<div class='form-row purpose  '>" +
			    	"<div>" +
			    		"<label for='id_purpose'>Purpose:</label>" +
			    		"<select name='purpose' id='id_purpose'> " +
			    			"<option value='' selected='selected'>---------</option>"+
			    			"<option value='1'>DG Delhi office</option>" +
			    			"<option value='2'>DG Bangalore office</option>" +
			    			"<option value='3'>DG Bhopal office</option>" +
			    			"<option value='4'>DG Bhubaneswar office</option>" +
			    			"<option value='5'>Partners office</option>" +
			    			"<option value='6'>Field</option>" +
			    			"<option value='7'>Individual</option>" +
			    		"</select>" +
			    	"</div>" +
			    "</div>" +
			  
			    "<div class='form-row additional_accessories  '>" +
			    	"<div>" +
			    		"<label for='id_additional_accessories'>Additional Accessories Supplied:</label>" +
			    		"<input id='id_additional_accessories' type='text' class='vTextField' name='additional_accessories' maxlength='500' />"+
			         "</div>" +
			    "</div>" +
			  
			    "<div class='form-row is_reserve  '>" +
			    	"<div>" +
			    		"<input type='checkbox' name='is_reserve' id='id_is_reserve' />" +
			    		"<label for='id_is_reserve' class='vCheckboxLabel'>Is the equipment in Reserve?</label>" +
			    	"</div>" +
			    "</div>" +
			  
			    "<div class='form-row procurement_date  '>"+
			    	"<div>" +
			    		"<label for='id_procurement_date'>Procurement date:</label>" +
			    		"<input id='id_procurement_date' type='text' class='vDateField' name='procurement_date' size='10' />"+
			    	"</div>" +
			    "</div>" +
			  
			    "<div class='form-row transfer_date  '>" +
			    	"<div>" +
			    		"<label for='id_transfer_date'>Transfer from DG to Partner date:</label>" +
			    		"<input id='id_transfer_date' type='text' class='vDateField' name='transfer_date' size='10' />"+
			    	"</div>" +
			    "</div>" +
			  
			    "<div class='form-row installation_date  '> " +
			    	"<div>" +
			    		"<label for='id_installation_date'>Field Installation Date:</label>" +
			    		"<input id='id_installation_date' type='text' class='vDateField' name='installation_date' size='10' />" +
			    	"</div>" +
			    "</div>" +
			    
			    "<div class='form-row warranty_expiration_date  '>" +
			    	"<div>" +
			    		"<label for='id_warranty_expiration_date'>Warranty expiration date:</label>" +
			    		"<input id='id_warranty_expiration_date' type='text' class='vDateField' name='warranty_expiration_date' size='10' />" +
			         "</div>" +
			     "</div>" +
			     
			     "<div class='form-row village  '>" +
			     	"<div>" +
			     		"<label for='id_village'>Village:</label>" +
			     		"<select name='village' id='id_village'>" +
			     			"<option value='' selected='selected'>---------</option>" +
			     		"</select>"+
			     	"</div>" +
			     "</div>" +

				"<div class='form-row equipmentholder  '>" +
					"<div>" +
						"<label for='id_equipmentholder'>Equipmentholder:</label><select name='equipmentholder' id='id_equipmentholder'>" +
							"<option value='' selected='selected'>---------</option>" +
						"</select>" +
					"</div>" +
				"</div>" +
				
				"<div class='form-row remarks  '>" +
					"<div>" +
						"<label for='id_remarks'>Remarks:</label>" +
						"<textarea id='id_remarks' rows='10' cols='40' name='remarks' class='vLargeTextField'></textarea>" +
					"</div>" +
				"</div>" +
				
			"</fieldset>" +
			"<div class='submit-row' >" +
			"<input id='save' type='button' value='Save' class='default' name='_save' />"	+
			"<input id='save_and_add_another' type='button' value='Save and add another' class='default' name='save_and_add_another' />"	+
			"</div>" +			
			
		"</div>" +
		"<br class='clear' />" +
	"</div>";
}
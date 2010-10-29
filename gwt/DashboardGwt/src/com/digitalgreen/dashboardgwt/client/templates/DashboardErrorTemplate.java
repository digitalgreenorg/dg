package com.digitalgreen.dashboardgwt.client.templates;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map.Entry;

import com.digitalgreen.dashboardgwt.client.common.ApplicationConstants;
import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.DashboardErrorData;
import com.digitalgreen.dashboardgwt.client.servlets.BaseServlet;
import com.digitalgreen.dashboardgwt.client.servlets.DashboardError;
import com.digitalgreen.dashboardgwt.client.servlets.Screenings;
import com.digitalgreen.dashboardgwt.client.servlets.Videos;
import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.HTML;
import com.google.gwt.user.client.ui.HTMLPanel;
import com.google.gwt.user.client.ui.HorizontalPanel;
import com.google.gwt.user.client.ui.Hyperlink;
import com.google.gwt.user.client.ui.Label;
import com.google.gwt.user.client.ui.RootPanel;
import com.google.gwt.user.client.ui.VerticalPanel;

public class DashboardErrorTemplate extends BaseTemplate{
	
	public DashboardErrorTemplate(RequestContext requestContext) {
		super(requestContext);
		this.formTemplate = new Form((new DashboardErrorData()).getNewData());
	}
	private static BaseServlet getObjectServlet(String object_name, RequestContext rq) {
		if(object_name.equals("screening")) {
			return new Screenings(rq);
		}
		else if(object_name.equals("video"))
			return new Videos(rq);
		else
			return null;
	}
	
	@Override
	public void fill() {
		String templateType = "DashboardError";
		
		// Draw the content of the template depending on the request type (GET/POST)
		super.fillDGTemplate(templateType, null, dashboardErrorListHtml, null);
		// Add it to the rootpanel
		super.fill();
		//Now add listings
		HashMap<String, Hyperlink> links = this.fillListings();

		// Now add hyperlinks
		HTMLPanel listFormHtml = new HTMLPanel(dashboardErrorListFormHtml);
		RootPanel.get("listing-form-body").insert(listFormHtml, 0);
		Iterator<Entry<String, Hyperlink>> iter = links.entrySet().iterator();
		while(iter.hasNext()) {
			Entry<String,Hyperlink> link = iter.next();
			if(link.getValue()!=null)
				RootPanel.get(link.getKey()).add(link.getValue());
			else
				RootPanel.get(link.getKey()).add(new Label("None"));
		}
		
		addPaginationHTML();
		
		// Now add any submit control buttons
		RequestContext saveRequestContext = new RequestContext(RequestContext.METHOD_POST);
		saveRequestContext.getArgs().put("pageNum", this.requestContext.getArgs().get("pageNum"));
		saveRequestContext.setForm(this.formTemplate);
		DashboardError saveDashboardError = new DashboardError(saveRequestContext);
		
		super.fillDgFormPage(saveDashboardError);
	}
	
	private void addPaginationHTML(){
		String templatePlainType = "Error";
		List<Hyperlink> pageLinks = new ArrayList<Hyperlink>();
		HashMap queryArgs = this.requestContext.getArgs();
		int totalRows = Integer.parseInt((String)queryArgs.get("totalRows"));
		int pageSize = ApplicationConstants.getPageSize();
		int maxPagesToDisplayPerRow = ApplicationConstants.getMaxPagesToDisplayPerRow();
		int numberOfPages = ((totalRows%pageSize) > 0)?(totalRows/pageSize)+1:(totalRows/pageSize);
		//For displaying total number of rows of child class
		String totalCountHtml = "<b>"+Integer.toString(totalRows)+" "+ templatePlainType+"s</b>" ;
		VerticalPanel vPanel = new VerticalPanel();
		//Need Paging if number of pages are greater than 1
		if(numberOfPages > 1) {
			//create Links for number of pages
			DashboardError servlet = new DashboardError();
			for(int i=1; i <= numberOfPages ; i++){
				String linkText = "<a href='#page/"+ Integer.toString(i) +"/'>" + Integer.toString(i) + "</a>";
				String tokenText = "page/"+ Integer.toString(i) +"/";
				pageLinks.add(createPageHyperlink(linkText, tokenText, servlet, Integer.toString(i),(String)queryArgs.get("operation"),(String)queryArgs.get("searchText")));
			}				
			//Adding links to Html by horizontal panel and vertical panel
			//Maximum number of pages in single horizontal row is 49
			int numberOfHpanels = (pageLinks.size()/maxPagesToDisplayPerRow)+1;
			for(int j=0; j< numberOfHpanels; j++) {
				HorizontalPanel hpanel = new HorizontalPanel();
				hpanel.setBorderWidth(1);
				for(int i = 0; i < maxPagesToDisplayPerRow; i++){
					if(j == 0 && i == 0) {
						hpanel.add(new HTML(totalCountHtml));
					}
					int linkIndex = (j*maxPagesToDisplayPerRow)+i;
					if(linkIndex < pageLinks.size()) {
						hpanel.add((Hyperlink)pageLinks.get(linkIndex));
					}						
				}
				vPanel.add(hpanel);
			}
		}
		else {
			vPanel.add(new HTML(totalCountHtml));
		}			
		RootPanel.get("pagination-footer").add(vPanel);
	}
	
	@Override
	public Hyperlink createPageHyperlink(String linkText, String tokenText, final BaseServlet servlet, 
			final String pageNum, final String operation, final String searchText) {
		Hyperlink addLink = new Hyperlink(linkText, true, tokenText);
		addLink.addClickHandler(new ClickHandler() {
			public void onClick(ClickEvent event) {
				Template.addLoadingMessage();
				RequestContext paginationRequestContext = new RequestContext();
				if(operation == "search") {
					paginationRequestContext.getArgs().put("operation","search");
					paginationRequestContext.getArgs().put("searchText",searchText);
				}
				paginationRequestContext.getArgs().put("action","add");
				paginationRequestContext.getArgs().put("pageNum",pageNum);
				servlet.setRequestContext(paginationRequestContext);
				servlet.response();
			}
		});
		return addLink;
	}
	
	protected HashMap<String, Hyperlink> fillListings() {
		HashMap queryArgs = this.getRequestContext().getArgs();
		String queryArg = (String)queryArgs.get("action");
		HashMap<String, Hyperlink> links = new HashMap<String, Hyperlink>();
		// If we're unsure, just default to list view
		if(queryArg.equals("add")) {
			// 	Add Listings
			List errors = (List)queryArgs.get("listing");
			if(errors  != null){
				StringBuilder tableRows = new StringBuilder(1000);
				String style;
				DashboardErrorData.Data error = null;
				for (int row = 0; row < errors.size(); ++row) {
					if(row%2==0)
						style= "row2";
					else
						style = "row1";
					error = (DashboardErrorData.Data) errors.get(row);
					tableRows.append("<tr class='" +style+ "'>" +
									  "<td>"+error.getErrorMsg()+"</td>" +
										"<td id='obj1row"+Integer.toString(row)+"'></td>" +
										"<td id='obj2row"+Integer.toString(row)+"'></td>" +
										"<td><input class='action-select' value='"+error.getId()+"' name='errorid' type='checkbox'"+((error.isError())?" checked='checked'":"")+"></td>" +
									"</tr>");
					String linkText1 = "<a href='#dashboard/"+error.getContentType1()+"/"+error.getObjectId1()+"/'>"+error.getContentType1()+" 1</a>";
					//String linkText1 = error.getContentType1()+" 1";
					String tokenText1 = "dashboard/"+error.getContentType1()+"/"+error.getObjectId1()+"/";
					RequestContext requestContext1 = new RequestContext();
					requestContext1.getArgs().put("action", "edit");
					requestContext1.getArgs().put("id", error.getObjectId1());
					Hyperlink link1 = createHyperlink(linkText1, tokenText1, getObjectServlet(error.getContentType1(), requestContext1));
					//Hyperlink link1 = getObjectTemplate(error.getContentType1(), requestContext1).getAddOrEditLink(linkText1, tokenText1);
					links.put("obj1row"+Integer.toString(row), link1);
					if(error.getObjectId2()!=null && error.getContentType2()!=null) {
						String linkText2 = "<a href='#dashboard/"+error.getContentType2()+"/"+error.getObjectId2()+"/'>"+error.getContentType2()+" 2</a>";
						//String linkText2 = error.getContentType2()+" 2";
						String tokenText2 = "dashboard/"+error.getContentType2()+"/"+error.getObjectId2()+"/";
						RequestContext requestContext2 = new RequestContext();
						requestContext2.getArgs().put("action", "edit");
						requestContext2.getArgs().put("id", error.getObjectId2());
						Hyperlink link2 = createHyperlink(linkText2, tokenText2, getObjectServlet(error.getContentType2(), requestContext2));
						//Hyperlink link2 = getObjectTemplate(error.getContentType2(), requestContext2).getAddOrEditLink(linkText2, tokenText2);
						links.put("obj2row"+Integer.toString(row), link2);
					}
					else
						links.put("obj2row"+Integer.toString(row), null);
				}
				dashboardErrorListFormHtml = dashboardErrorListFormHtml + tableRows.toString() + "</tbody></table>";
			}
		}
		return links;
	}
	
	
	
	// A list of Element IDs that need to receive the data before the template is loaded. 
	//final private String addDataToElementID[] = {};
	
	private String dashboardErrorListFormHtml = "<table cellspacing='0'>" +
															"<thead>" +
															"<tr>" +
																"<th>Error Msg</th>" +
																"<th>Object 1</th>" +
																"<th>Object 2</th>" +
																"<th>Not an Error</th>" +
															"</tr>" +
															"</thead>" +
															"<tbody>";
	final private String dashboardErrorListHtml = "<link rel='stylesheet' type='text/css' href='/media/css/base.css'>" +
			"<link rel='stylesheet' type='text/css' href='/media/css/changelists.css'>" +
				"<div id='container'>" +
				"<div id='content' class='flex'>" +
					"<h1>Data Inconsistencies</h1>" +
					"<div id='incosistency-note'><b>Note:</b> If you think that the reported error is a valid case, mark it as 'Not an Error' and click 'Save'. Otherwise resolve the errors by modifying the data entries. The error entry will <b>NOT</b> be removed immediately. Please ignore it, it will be removed from this page within 24 hours.</div>" +
					"<br>" +
					"<div id='content-main'>" +
						"<div class='module' id='dashboardErrorTable'>" +
								"<div id='listing-form-body'>" +  // Insert form data here
								"</div>" +
						"</div>" +
						"<div class='submit-row' >" +
							"<input id='save' type='button' value='Save' class='default' name='_save' />" +
						"</div>"+
					"</div>" +
				"</div>";

}
package com.digitalgreen.dashboardgwt.client.templates;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.BaseData;
import com.digitalgreen.dashboardgwt.client.data.PersonAdoptPracticeData;
import com.digitalgreen.dashboardgwt.client.data.PersonMeetingAttendanceData;
import com.digitalgreen.dashboardgwt.client.data.ScreeningsData;
import com.digitalgreen.dashboardgwt.client.servlets.Regions;
import com.digitalgreen.dashboardgwt.client.servlets.Screenings;
import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.Button;
import com.google.gwt.user.client.ui.FormPanel;
import com.google.gwt.user.client.ui.HTML;
import com.google.gwt.user.client.ui.HTMLPanel;
import com.google.gwt.user.client.ui.Hyperlink;
import com.google.gwt.user.client.ui.InlineHTML;
import com.google.gwt.user.client.ui.RootPanel;

public class ScreeningsTemplate extends BaseTemplate {
	public ScreeningsTemplate(RequestContext requestContext) {
		super(requestContext);
		ArrayList personMeetingAttendanceData = new ArrayList();
		personMeetingAttendanceData.add((new PersonMeetingAttendanceData()).getNewData());
		this.formTemplate = new Form((new ScreeningsData()).getNewData(),
				new Object[] {personMeetingAttendanceData});
	}
		
	@Override
	/*public void fill() {
		String templateType = "Screening";
		String templatePlainType = "dashboard/screening/add/";
		RequestContext requestContext = new RequestContext();
		HashMap args = new HashMap();
		args.put("action", "add");
		requestContext.setArgs(args);
		requestContext.setForm(this.formTemplate);
		Screenings addScreeningServlet = new Screenings(requestContext);
		RequestContext saveRequestContext = new RequestContext(RequestContext.METHOD_POST);
		saveRequestContext.setForm(this.formTemplate);
		Screenings saveScreening = new Screenings(saveRequestContext);
		// Draw the content of the template depending on the request type (GET/POST)
		
		
		super.fillDGTemplate(templateType, screeningsListHtml, screeningsAddHtml, addDataToElementID);
		//Now add listings
		List<Hyperlink> links =  this.fillListings();
		// Add it to the rootpanel
		super.fill();
		
		// Now add hyperlinks
		super.fillDgListPage(templatePlainType, templateType, screeningsListFormHtml, addScreeningServlet, links);
		// Now add any submit control buttons
		this.displayCalendar();
		super.fillDgFormPage(saveScreening);	
		if(!this.getRequestContext().getArgs().get("action").equals("list")) {
			String id ="0";
			if(this.requestContext.getArgs().get("action").equals("edit")) {
				id = (String) this.requestContext.getArgs().get("id");
			}
			ScreeningsTemplate.loadPerson(id);
		}
		//call_datatable();
	}*/
	public void fill(boolean connectivity) {
		//Window.alert("fill()");
		String templateType = "Screening";
		String templatePlainType = "dashboard/screening/add/";
		RequestContext requestContext = new RequestContext();
		HashMap args = new HashMap();
		args.put("action", "add");
		requestContext.setArgs(args);
		requestContext.setForm(this.formTemplate);
		Screenings addScreeningServlet = new Screenings(requestContext);
		RequestContext saveRequestContext = new RequestContext(RequestContext.METHOD_POST);
		saveRequestContext.setForm(this.formTemplate);
		Screenings saveScreening = new Screenings(saveRequestContext);
		// Draw the content of the template depending on the request type (GET/POST)
		
		
		super.fillDGTemplate(templateType, screeningsListHtml, screeningsAddHtml, addDataToElementID);
		//Now add listings
		
		List<Hyperlink> links =  this.fillListings(connectivity);
		// Add it to the rootpanel
		super.fill();
		
		// Now add hyperlinks
		super.fillDgListPage(templatePlainType, templateType, screeningsListFormHtml, addScreeningServlet, links);
		// Now add any submit control buttons
		this.displayCalendar();
		super.fillDgFormPage(saveScreening);	
		if(!this.getRequestContext().getArgs().get("action").equals("list")) {
			String id ="0";
			if(this.requestContext.getArgs().get("action").equals("edit")) {
				id = (String) this.requestContext.getArgs().get("id");
			}
			ScreeningsTemplate.loadPerson(id);
		}
		else{
			if(!connectivity){
				//Window.alert("offline datatable call");
				call_datatable();
			
			}
			else
				call_datatable_online("/dashboard/getscreeningsforperfonline_server/",this);
		}
		//Window.alert("finished");
	}
	
	public List<Hyperlink> fillListings(boolean connectivity){
		HashMap queryArgs = this.getRequestContext().getArgs();
		String queryArg = (String)queryArgs.get("action");
		List<Hyperlink> links = new ArrayList<Hyperlink>();
		// If we're unsure, just default to list view
		if(queryArg.equals("list")&&!connectivity) {
			// 	Add Listings
			List screenings = (List)queryArgs.get("listing");			
			if(screenings  != null){
				String tableRows ="";
				String style;
				ScreeningsData.Data screening;
				//List<ScreeningsData.Data> screenings_for_array= new ArrayList<ScreeningsData.Data>();
				//List<String> try1 = new ArrayList<String>();
				RequestContext requestContext = null;
				for (int row = 0; row <screenings.size(); ++row) {
					if(row%2==0)
						style= "row2";
					else
						style = "row1";
					screening = (ScreeningsData.Data) screenings.get(row);
					requestContext = new RequestContext();
					requestContext.getArgs().put("action", "edit");
					requestContext.getArgs().put("id", screening.getId());
					requestContext.setForm(this.formTemplate);
					links.add(this.createHyperlink("<a href='#dashboard/screening/"+ screening.getId() +"/'>" +
							screening.getId()+ "</a>", "dashboard/screening/"+ screening.getId() +"/", new Screenings(requestContext)));
					tableRows += "<tr>" +
								  "<th id = 'row" + row + "'></th>" +
								  	"<td>"+ screening.getDate()  +"</td>"+
									"<td>"+ screening.getVillage().getVillageName() + "</td>"+
									"<td>"+ screening.getLocation()+"</td>" +
								"</tr>";
					//screenings_for_array.add(screening);
					//try1.add(screening.getVillage().getVillageName());
				}
				//screeningsListFormHtml = screeningsListFormHtml +"</tbody></table>";
				//screeningJsArray(try1);
				
				screeningsListFormHtml = screeningsListFormHtml + tableRows + "</tbody></table>";
				
			}
		}
		
		if(queryArg.equals("list")&&connectivity)
			screeningsListFormHtml = screeningsListFormHtml+ "</tbody></table>";
		
		return links;
	}
	
	 /*var vil = screening.getVillage().getVillageName();
    var date =screening.getDate();
    var loc= screening.getLocation();
    var tuple = new Array();
    tuple[0] = date;
    tuple[1] = vil;
    tuple[2] = loc;
    table_data.push(tuple);
    */
	
	public static native void call_datatable_online(String url,ScreeningsTemplate inst) /*-{
	//var start =new Date().getTime();
	//$wnd.alert(str);
	$wnd.$('#table1').dataTable({
     "sAjaxSource": url,
     "bProcessing": true,
     "bServerSide": true,
      //     "fnInitComplete": function(oSettings, json) {
      //alert( 'DataTables has finished its initialisation.' );
      //$entry(inst.@com.digitalgreen.dashboardgwt.client.data.BaseData::datatable_manipulate()());
    //},
     "fnRowCallback": function( nRow, aData, iDisplayIndex, iDisplayIndexFull ) {
     
     	//$wnd.$(nRow).attr('id', 'row'+iDisplayIndex);
      	$wnd.$($wnd.$(nRow).children()[0]).attr('id', 'row'+iDisplayIndex);
      	      	$wnd.$($wnd.$(nRow).children()[0]).css('font-weight', 'bold');
      	//var str = inst.@com.digitalgreen.dashboardgwt.client.templates.ScreeningsTemplate::datatable_manipulate_row(ILjava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)(iDisplayIndex,aData[0],aData[1],aData[2],aData[3]);
        //$wnd.alert(nRow +typeof(nRow));
        //$wnd.alert(iDisplayIndex);
        //$wnd.alert(iDisplayIndexFull);
       // $wnd.$(nRow).html( str );
        
        
     
    },    //"sAjaxSource": "scripts/server_processing.php"
      
          
    "fnDrawCallback": function( oSettings ) {
    	
      //alert( 'DataTables has redrawn the table'+String(oSettings['_iDisplayLength']));
      var str = inst.@com.digitalgreen.dashboardgwt.client.templates.ScreeningsTemplate::datatable_manipulate_row(I)(oSettings['_iDisplayLength']);
       
    }
      
     });
	//var end =new Date().getTime();
	//var time = end-start;
	//$wnd.alert("time= "+time);
	
	
	}-*/;
	
	
	public void datatable_manipulate_row(int page_length)
	{
		/*Window.alert(String.valueOf(RootPanel.get("table1").getElement().getChildCount()));
		//Window.alert(RootPanel.get("table1").getElement().getChild(2).toString());
		Window.alert((RootPanel.get("table1").getElement().getInnerHTML()));
		Window.alert(String.valueOf(RootPanel.get("table1").getElement().getChild(1).getChildCount()));//getFirstChild().getFirstChild().getNodeValue());
		Window.alert(String.valueOf(RootPanel.get("table1").getElement().getChild(1).getFirstChild().getChildCount()));
		com.google.gwt.dom.client.Element row = RootPanel.get("table1").getElement().getChild(1).getFirstChild().getFirstChild().getParentElement();//setNodeValue("nice!!!");//getNodeValue());
	    Window.alert(row.getInnerHTML());
	    row.setInnerHTML(" <td class=' sorting_1'><a href='http://www.google.com'>10000000043562<a></td><td class=''>2011-02-16</td><td class=''>Shrey </td>");*/
		for(int index=0;index<page_length;index++)
		{
			String id= (RootPanel.get("row"+index).getElement().getInnerText());
			//Window.alert(RootPanel.get("row"+index).getElement().getNodeValue());
			RequestContext requestContext = null;
			requestContext = new RequestContext();
			requestContext.getArgs().put("action", "edit");
			requestContext.getArgs().put("id", id);
			requestContext.setForm(this.formTemplate);
		
			//Window.alert(id+date);
			Hyperlink link= (this.createHyperlink("<a href='#dashboard/screening/"+ id +"/'>" +
					id + "</a>", "dashboard/screening/"+ id +"/", new Screenings(requestContext)));
			
			/*String row="<th>"+link.getHTML()+"</th>" + 
					  	"<td>"+ date +"</td>"+
						"<td>"+ village + "</td>"+
						"<td>"+ location+"</td>" ;
				*/	
			//InlineHTML h_row= new InlineHTML();
			//HTML  html_row = new HTML(row);
			//Window.alert(row);
			//Window.alert(link.getHTML());
			//Window.alert(new InlineHTML("<tr><td>shrey</td></tr>").toString());
			//for(int i = 0; i < links.size(); i++){
			//RootPanel.get("table_body").add(html_row);
			RootPanel.get("row"+index).getElement().setInnerText("");
			RootPanel.get("row"+index).add(link);
		}
		//}
		
		//return row;
		
	}
	
	
	public static native void call_datatable() /*-{
	//var start =new Date().getTime();
	$wnd.$('#table1').dataTable({"bDeferRender": true,});
	//var end =new Date().getTime();
	//var time = end-start;
	//$wnd.alert("time= "+time);
	
	
	}-*/;
	
	public static native void screeningJsArray(List<String> all_screenings) /*-{
		try{
			$wnd.alert("running");
	var table_data = new Array();
	//for( i=0;i<all_screenings.length;i++)
	{
       var tuple = new Array();
    	tuple[0] = "date1";
    	tuple[1] = "village1";
    	tuple[2]="location1";
    	//tuple[3]="dum1";
       table_data.push(tuple);
    	
	
	}
	$wnd.$('#table1').dataTable({
             "aaData": table_data,
             "bStateSave": true,});
             $wnd.alert("done");
	}
             catch(e){
             	$wnd.alert('An error has occurred: '+e.message)
             } 
		
}-*/;
	
	public static native void loadPerson(String id) /*-{
			$wnd.screening_page_offline.init(id);
	}-*/;
	
	//Loading javascript for displaying calendar in Google chrome browser
	public static native void displayCalendar() /*-{
		$wnd.DateTimeShortcuts.init();		
	}-*/;
	
	final private String addDataToElementID[] = {"id_village", "id_animator", "id_videoes_screened", "id_fieldofficer", "id_farmer_groups_targeted"};
	
	// Fill ids:  data-rows
	private String screeningsListFormHtml = "<div class='actions'>" +
						"<label>Action: <select name='action'>" +
							"<option value='' selected='selected'>---------</option>" +
							"<option value='delete_selected'>Delete selected screenings</option>" +
							"</select>" +
						"</label>" +
						"<button type='submit' class='button' title='Run the selected action' name='index' value='0'>Go</button>" +
					"</div>" +
					"<table id='table1' class='display'>" +
						"<thead>" +
							"<tr>" +
									"<th>" +
										"ID" +
									"</th>" +
										"<th>"+
											"Date"+
										"</th>"+
								"<th>" +
										"Village" +
								"</th>" +
								"<th>" +
										"Location" +
									"</a>" +
								"</th>" +
							"</tr>" +
						"</thead>" +
						"<tbody id='table_body'>";

	// Fill ids:  listing-form-body, add-link
	final private String screeningsListHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
					"<div id='content' class='flex'>" +
						"<h1>Select screening to change</h1>" +
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
	
	public static native void callScreeningFilter(String queryString) /*-{
			$wnd.init(queryString);
	}-*/;
	
	final private String screeningsAddHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
							"<link href='/media/css/screening_page.css' type='text/css' media='all' rel='stylesheet' />" +
							//"<script src='/media/coco/dashboardgwt/gears_init.js' type='text/javascript'></script>"+
							//"<script src='/media/js/jquery.js' type='text/javascript'></script>" +
							"<div id='content' class='colM'>" +
							"<h1>Add screening</h1>" +
						    "<div id='content-main'>" +
								"<fieldset class='module aligned '>" +
									"<div class='form-row date  '>" +
										"<div>" +
											"<label for='id_date' class='required'>Date:</label>" +
											"<input id='id_date' type='text' class='vDateField' name='date' size='10' />" +
										"</div>" +
									"</div>" +
									"<div class='form-row start_time  '>" +
										"<div>" +
											"<label for='id_start_time' class='required'>Start time:</label>" +
											"<input id='id_start_time' type='text' class='vTimeField' name='start_time' size='8' />" +
										"</div>" +
									"</div>" +
									"<div class='form-row end_time  '>" +
										"<div>" +
											"<label for='id_end_time' class='required'>End time:</label>" +
											"<input id='id_end_time' type='text' class='vTimeField' name='end_time' size='8' />" +
										"</div>" +
									"</div>" +
									"<div class='form-row location  '>" +
										"<div>" +
											"<label for='id_location'>Location:</label>" +
											"<input id='id_location' type='text' class='vTextField' name='location' maxlength='200' />" +
										"</div>" +
									"</div>" +
									"<div class='form-row village  '>" +
										"<div>" +
											"<label for='id_village' class='required'>Village:</label>"+
											"<select name='village' id='id_village'>" +
												"<option value='' selected='selected'>---------</option>" +
											"</select>" +
/*											
											"<input type='hidden' name='village' id='id_village' />" +
											"<style type='text/css' media='screen'>" +
											"#lookup_village {" +
												"padding-right:16px;" +
												"background: url(" +
													"/media/img/admin/selector-search.gif" +
												") no-repeat right;" +
											"}" +
											"#del_village {" +
												"display: none;" +
											"}" +
										"</style>" +
										"<input type='text' id='lookup_village' value='' />" +
										"<a href='#' id='del_village'>" +
											"<img src='/media/img/admin/icon_deletelink.gif' />" +
										"</a>" +
										"<script type='text/javascript' src='/media/js/jquery.autocomplete.js'></script>"+
										"<script type='text/javascript'>" +
											"if ($('#lookup_village').val()) {" +
												"$('#del_village').show()" +
											"}" +
											"$('#lookup_village').autocomplete('/dashboard/search/', {" +
												"extraParams: {" +
													"search_fields: 'village_name'," +
													"app_label: 'dashboard'," +
													"model_name: 'village'," +
												"}," +
											"}).result(function(event, data, formatted) {" +
												"if (data) {" +
													"$('#id_village').val(data[1]);" +
													"$('#del_village').show();" +
											"filter();" +
												"}" +
											"});" +
											"$('#del_village').click(function(ele, event) {" +
												"$('#id_village').val('');" +
												"$('#del_village').hide();" +
												"$('#lookup_village').val('');" +
											"});" +
										"</script>" +
*/											
										"</div>" +
									"</div>" +
									"<div class='form-row animator  '>" +
										"<div>" +
											"<label for='id_animator' class='required'>Animator:</label>" +
											"<select name='animator' id='id_animator'>" +
												"<option value='' selected='selected'>---------</option>" +
											"</select>" +
										"</div>" +
									"</div>" +
									"<div class='form-row videoes_screened  '>" +
										"<div>" +
											"<label for='id_videoes_screened' class='required'>Videoes screened:</label>" +
											"<select multiple='multiple' name='videoes_screened' id='id_videoes_screened'>" +
											"</select>" +
											//"<script type='text/javascript'>addEvent(window, 'load', function(e) {SelectFilter.init('id_videoes_screened', 'videoes screened', 0, '/media/'); });" +
											//"</script>" +
											"</a>" +
											"<p class='help'> Hold down 'Control', or 'Command' on a Mac, to select more than one.</p>" +
										"</div>" +
									"</div>" +
									"<div class='form-row fieldofficer  '>" +
										"<div>" +
											"<label for='id_fieldofficer'>Fieldofficer:</label>" +
											"<select name='fieldofficer' id='id_fieldofficer'>" +
												"<option value='' selected='selected'>---------</option>" +
											"</select>" +
											"</a>" +
										"</div>" +
									"</div>" +
									"<div class='form-row farmer_groups_targeted  '>" +
										"<div>" +
											"<label for='id_farmer_groups_targeted' class='required'>Farmer groups targeted:</label>" +
											//"<select multiple='multiple' onchange='filter_person();' name='farmer_groups_targeted' id='id_farmer_groups_targeted'>" +
											"<select id='id_farmer_groups_targeted' name='farmer_groups_targeted' multiple='multiple'>" +
											"</select>" +
										"</div>" +
									"</div>" +
								"</fieldset>" +
								"<div class='inline-group'>" +
									"<div class='tabular inline-related last-related'>" +
										"<input type='hidden' name='personmeetingattendance_set-TOTAL_FORMS' value='0' id='id_personmeetingattendance_set-TOTAL_FORMS' />" +
										"<input type='hidden' name='personmeetingattendance_set-INITIAL_FORMS' value='0' id='id_personmeetingattendance_set-INITIAL_FORMS' />" +
										"<fieldset class='module'>" +
											"<h2>Person meeting attendances</h2>" +
											"<table>" +
												"<thead>" +
													"<tr>" +
														"<th>Delete?</th>" +
														"<th>Sr No.</th>" +
														"<th >Person</th>" +
														"<th >Expressed Adopted Video</th>" +
														"<th >Question Asked</th>" +
														"<th >Interested?</th>" +
													"</tr>" +
												"</thead>" +
											"</table>" +
										"</fieldset>" +
									"</div>" +
								"</div>" +
								"<div class='submit-row' >" +
									"<input id='save' type='button' value='Save' class='default' name='_save' />" +
								"</div>" +
								"<script type='text/javascript'>document.getElementById('id_date').focus();</script>" +
							"</div>" +
							"<br class='clear' />" +
						"</div>"  ;
}
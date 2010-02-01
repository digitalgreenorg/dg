package com.digitalgreen.dashboardgwt.client;

import com.google.gwt.core.client.EntryPoint;
//import com.google.gwt.core.client.GWT;
import com.google.gwt.dom.client.Element;
import com.google.gwt.dom.client.Node;
import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.FormPanel;
import com.google.gwt.user.client.ui.RootPanel;
import com.google.gwt.user.client.ui.TextBox;
import com.google.gwt.user.client.ui.Button;
import com.google.gwt.user.client.ui.FormPanel.SubmitCompleteEvent;
import com.google.gwt.user.client.ui.FormPanel.SubmitEvent;
import com.google.gwt.user.client.ui.FormPanel.SubmitHandler;
import com.google.gwt.user.client.ui.HTML;
import com.google.gwt.user.client.ui.HTMLPanel;

import com.google.gwt.gears.client.Factory;
import com.google.gwt.gears.client.GearsException;
import com.google.gwt.gears.client.database.Database;
import com.google.gwt.gears.client.database.DatabaseException;
import com.google.gwt.gears.client.database.ResultSet;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.Grid;


/**
 * Entry point classes define <code>onModuleLoad()</code>.
 */
public class DashboardGwt implements EntryPoint {
	
	/**
	 * This is the entry point method.
	 */
	//private Database db;
	
	public void onModuleLoad() {
		
		/*
		 * Wrap the Child elements before the parent element.
		 * Button is wrapped before the form is wrapped.
		 * */

		Button b = new Button("Save");
	    b.setStyleName("button default");
	    
		//Element e_form = RootPanel.get("region_form").getElement();
		//final FormPanel f = FormPanel.wrap(e_form);
	    final FormPanel f = new FormPanel();
		f.setAction("http://174.129.13.106:8000/feeds/test/49/");
	    f.setEncoding(FormPanel.ENCODING_MULTIPART);
	    f.setMethod(FormPanel.METHOD_POST);

	    final HTMLPanel h = new HTMLPanel("<div>" +
	    					"<fieldset class='module aligned '>" +
	    					"<div class='form-row region_name  '>" +
	    					"<div>" +
	    					"<label for='id_region_name' class='required'>Region name:</label><input id='id_region_name' type='text' class='vTextField' name='region_name' maxlength='100' />" +
	    					"</div>" +
	    					"</div>" +
	    					"<div class='form-row start_date'>" +
	    					"<div><label for='id_start_date'>Start date:</label><input id='id_start_date' type='text' class='vDateField' name='start_date' size='10' />" +
	    					"</div>" +
	    					"</fieldset>" +
	    					"</div>");
	    f.add(h);
	    RootPanel.get("content-main").add(f);
	    RootPanel.get("submit-button").add(b);
	    
	    b.addClickHandler(new ClickHandler() {
		      public void onClick(ClickEvent event) {
		    	   Window.alert("form submit 1");
		    	   f.submit();
			      }
	    });
	    
	    f.addSubmitHandler(new FormPanel.SubmitHandler() {	
			public void onSubmit(SubmitEvent event) {
				// TODO Auto-generated method stub				
	    		Window.alert("form submit 2");
	    		
	    		// TODO Form validation
	    		
	    		// TO Save the data into local database
	    		
	    		/*try {
	    		      db = Factory.getInstance().createDatabase();
	    		      db.open("digitalgreen");
	    		      // The 'int' type will store up to 8 byte ints depending on the magnitude of the 
	    		      // value added.
	    		      db.execute("CREATE TABLE REGION ( REGION_ID INTEGER PRIMARY KEY AUTOINCREMENT, REGION_NAME VARCHAR(50) NOT NULL, START_DATE DATE );");
	    		    } catch (GearsException e) {
	    		      Window.alert(e.toString());
	    		    }
	    		    
	    		    // Add an entry to the database
	    		    try {
	    		      db.execute("INSERT INTO REGION (REGION_NAME, START_DATE) VALUES (?, ?)", new String[] {
	    		          Long.toString(System.currentTimeMillis())});
	    		    }
	    		    catch (DatabaseException e) {
	    		      Window.alert(e.toString());
	    		    } */
	    		    
	    	}
	    });
	    
	    f.addSubmitCompleteHandler(new FormPanel.SubmitCompleteHandler() {
	    	public void onSubmitComplete(SubmitCompleteEvent event) {
	    		Window.alert("hi");
	    		//Element e = RootPanel.get("id_region_name").getElement();
	    		TextBox t = TextBox.wrap(h.getElementById("id_region_name"));
	    		Window.alert("here it is" + t.getText());
	    		Window.alert("Date : " + TextBox.wrap(h.getElementById("id_start_date")).getText());
	    	}
	    });
	    

	}	
}

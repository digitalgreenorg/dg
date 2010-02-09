package com.digitalgreen.dashboardgwt.client;

import java.util.ArrayList;
import java.util.List;

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
	private Database db;
	public void onModuleLoad() {
		
		/*
		 * Wrap the Child elements before the parent element.
		 * Button is wrapped before the form is wrapped.
		 * */

		Button b = new Button("Save");
	    b.setStyleName("button default");
	       
	    final FormPanel f = new FormPanel();
		f.setAction("http://174.129.13.106/feeds/test/49/");
	    f.setEncoding(FormPanel.ENCODING_MULTIPART);
	    f.setMethod(FormPanel.METHOD_POST);

	    final HTMLPanel h = new HTMLPanel(Regions.REGION_CONTENT_HTML);

	    f.add(h);
	    RootPanel.get("content").addStyleName("colM");
	    RootPanel.get("content").insert(new HTMLPanel(Regions.REGION_CONTENT_TITLE), 0);
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
				
	    		Window.alert("form submit 2");
	    		// TODO Form validation
	    		
	    		// TO Save the data into local database
	    		
	    		TextBox region = TextBox.wrap(h.getElementById("id_region_name"));
	    		TextBox date =  TextBox.wrap(h.getElementById("id_start_date"));
	    			
	    			try {
	    		      db = Factory.getInstance().createDatabase();
	    		      db.open("digitalgreen");
	    		      
	    		      db.execute("CREATE TABLE IF NOT EXISTS REGION ( REGION_ID INTEGER PRIMARY KEY AUTOINCREMENT, REGION_NAME VARCHAR(50) NOT NULL, START_DATE DATE );");
	    			} catch (GearsException e) {
	    		      Window.alert(e.toString());
	    			}
	    		    
	    		    // Add an entry to the database
	    		    try {
	    		      db.execute("INSERT INTO REGION (REGION_NAME, START_DATE) VALUES (?, ?)", region.getText(), date.getText());
	    		    }
	    		    catch (DatabaseException e) {
	    		      Window.alert(e.toString());
	    		    }
	    	}
	    });
	    
	    f.addSubmitCompleteHandler(new FormPanel.SubmitCompleteHandler() {
	    	public void onSubmitComplete(SubmitCompleteEvent event) {
	    		Window.alert("hi");
	    		
	    		// Fetch previous results from the database.
    		    List<String> results = new ArrayList<String>();
    		    String str = "";
    		    String tr_class ;
    		    int i = 0;
    		    try {

    		      ResultSet rs = db.execute("select * from REGION");
    		      for (i = 0; rs.isValidRow(); ++i, rs.next()) {
    		        results.add(rs.getFieldAsString(1));
    		        
    		        if (i%2==0)
    		        	tr_class = "row1";
    		        else
    		        	tr_class = "row2";
    		        
    		        str = str + 
    		              "<tr class='" + tr_class + "'>" + 
    		        		"<td><input class='action-select' value='"+rs.getFieldAsInt(0)+"' name='_selected_action' type='checkbox'></td><th><a href='/admin/dashboard/region/" + rs.getFieldAsInt(0) + "/'>" + rs.getFieldAsString(1) + "</a></th>" +
    		        	  "</tr>";
    		        //Window.alert(results.get(i));
    		      }
    		      rs.close();
    		      //Window.alert(str);
    		    } catch (DatabaseException e) {
    		      Window.alert(e.toString());
    		    }
    		    
    		    str = Regions.REGION_LISTING_HTML + str + "</tbody></table><p class='paginator'>" + i + " regions" + "</p>";
    		    RootPanel.get("submit-button").clear();
    		    RootPanel.get("content-main").clear();
    		    RootPanel.get("content").clear();
				FormPanel f2 = new FormPanel();
				f2.setAction("http://174.129.13.106/feeds/test_gwt/49/");
			    f2.setEncoding(FormPanel.ENCODING_MULTIPART);
			    f2.setMethod(FormPanel.METHOD_POST);
				HTMLPanel h = new HTMLPanel(str);
			    f2.add(h);
			    
			    RootPanel.get("content").setStyleName("flex");
			    RootPanel.get("content").insert(new HTMLPanel(Regions.REGION_LISTING_TITLE), 0);
			    RootPanel.get("content-main").add(new HTMLPanel(Regions.REGION_LISTING_DIV));
			    RootPanel.get("changelist").insert(f2, 0);
			    
	    	}
	    });
	    

	}	
}

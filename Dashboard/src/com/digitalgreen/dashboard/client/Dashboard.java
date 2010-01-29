package com.digitalgreen.dashboard.client;

import com.google.gwt.core.client.EntryPoint;
import com.google.gwt.core.client.GWT;
import com.google.gwt.dom.client.Element;
import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.FormPanel;
import com.google.gwt.user.client.ui.RootPanel;
import com.google.gwt.user.client.ui.TextBox;
import com.google.gwt.user.client.ui.Button;
import com.google.gwt.user.client.ui.FormPanel.SubmitEvent;
import com.google.gwt.user.client.ui.FormPanel.SubmitHandler;

/**
 * Entry point classes define <code>onModuleLoad()</code>.
 */
public class Dashboard implements EntryPoint {
	
	/**
	 * This is the entry point method.
	 */
	
	Element e_form = RootPanel.get("region_form").getElement();
	FormPanel f = FormPanel.wrap(e_form);
	
	public void onModuleLoad() {
		
		f.setAction("http://174.129.13.106:8000/feeds/animators/49/");

	    // Because we're going to add a FileUpload widget, we'll need to set the
	    // form to use the POST method, and multipart MIME encoding.
	    f.setEncoding(FormPanel.ENCODING_MULTIPART);
	    f.setMethod(FormPanel.METHOD_POST);
		
	    Element e = RootPanel.get("save_button").getElement();
	    Button b = Button.wrap(e);
	    
	    	    
	    b.addClickHandler(new ClickHandler() {
		      public void onClick(ClickEvent event) {
			        Window.alert("Hi");
			        f.submit();
			      }});
	    
	    	    
	}
}

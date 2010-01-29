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
	
	
	
	public void onModuleLoad() {
		
		Element e_form = RootPanel.get("region_form").getElement();
		final FormPanel f = FormPanel.wrap(e_form);
		
		f.setAction("http://174.129.13.106:8000/feeds/animators/49/");
	    f.setEncoding(FormPanel.ENCODING_MULTIPART);
	    f.setMethod(FormPanel.METHOD_POST);
		
	    Element e = RootPanel.get("save_button").getElement();
	    Button b = Button.wrap(e);
	    
	    f.addSubmitHandler(new SubmitHandler() {
	    	public void onSubmit(SubmitEvent event) {
	    		Window.alert("form submit 2");
	    }});
	    	    	    
	    b.addClickHandler(new ClickHandler() {
		      public void onClick(ClickEvent event) {
		    	   Window.alert("form submit 1");
			        f.submit();
			      }});
	    
	    
	    
	}
}

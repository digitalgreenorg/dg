package com.digitalgreen.dashboardgwt.client.templates;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.servlets.Login;
import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.user.client.ui.Button;
import com.google.gwt.user.client.ui.FormPanel;
import com.google.gwt.user.client.ui.HTMLPanel;

public class LoginTemplate extends BaseTemplate {
	private FormPanel postForm = null;
	private HTMLPanel formHtml = null;
	
	public LoginTemplate(RequestContext requestContext) {
		super(requestContext);
	}

	public FormPanel getPostForm() {
		return this.postForm;
	}

	@Override
	public void fill() {
		this.postForm = new FormPanel();
		this.postForm.setAction(this.getRequestContext().getFormAction());
	    this.postForm.setEncoding(FormPanel.ENCODING_MULTIPART);
	    this.postForm.setMethod(FormPanel.METHOD_POST);
	    this.formHtml = new HTMLPanel(loginFormHtml);
	    this.postForm.add(this.formHtml);
		super.setContentPanel(this.postForm);
	    super.fill();
		this.fillSubmitControls();
	}

	@Override
	public void fillSubmitControls() {
		// Add submit controls html here
		Button b = new Button("Save");
	    b.setStyleName("button default");
	    b.addClickHandler(new ClickHandler() {
			public void onClick(ClickEvent event) {
				Login l = new Login(new RequestContext(RequestContext.METHOD_POST, 
													   getPostForm()));
				l.response();
			}
	    });
		super.setSubmitControlsPanel(b);
		super.fillSubmitControls();
	}
	
	final static String loginFormHtml = "";
}

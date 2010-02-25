package com.digitalgreen.dashboardgwt.client.servlets;

import java.util.HashMap;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.IndexData;
import com.digitalgreen.dashboardgwt.client.servlets.BaseServlet;
import com.digitalgreen.dashboardgwt.client.templates.IndexTemplate;
import com.google.gwt.user.client.Window;

public class Index extends BaseServlet {	
	public Index(){
		super();
	}
	
	public Index(RequestContext requestContext){
		super(requestContext);
	}
	
	@Override
	public void response () {
		super.response();
		String method = this.getMethodTypeCtx();
		
		if (!this.isLoggedIn()) {
			super.redirectTo(new Login());
		} 
		else {
			if(method == RequestContext.METHOD_POST) {
				HashMap queryArgs = (HashMap)this.requestContext.getArgs();
				String queryArg = (String)queryArgs.get("action");
				if(queryArg == "gooffline"){
					IndexData.createTables();
				}
			}
			else{
				this.fillTemplate(new IndexTemplate(this.requestContext));
			}
		}
	}
}
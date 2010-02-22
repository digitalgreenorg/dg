package com.digitalgreen.dashboardgwt.client.servlets;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.templates.AnimatorsTemplate;

public class Animators extends BaseServlet{
	
	public Animators(){
		super();
	}
	
	public Animators(RequestContext requestContext){
		super(requestContext);		
	}
	
	@Override
	public void response(){
		super.response();
		
		if(!this.isLoggedIn()){
			super.redirectTo(new Login());
		}else{
			this.fillTemplate(new AnimatorsTemplate(this.requestContext));
		}
	}

}

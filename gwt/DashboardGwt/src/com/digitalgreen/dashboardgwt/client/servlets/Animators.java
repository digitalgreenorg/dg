package com.digitalgreen.dashboardgwt.client.servlets;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.templates.AnimatorsTemplate;

public class Animators extends BaseServlet{
	protected static String createSql = "CREATE TABLE `ANIMATOR` (" +
								 		"`id` int(11) NOT NULL PRIMARY KEY, " +
								 		"`NAME` varchar(100) NOT NULL, " +
								 		"`AGE` int(11) default NULL, " +
								 		"`GENDER` varchar(1) NOT NULL, " +
								 		"`CSP_FLAG` tinyint(1) default NULL, " +
								 		"`CAMERA_OPERATOR_FLAG` tinyint(1) default NULL, " +
								 		"`FACILITATOR_FLAG` tinyint(1) default NULL, " +
								 		"`PHONE_NO` varchar(100) NOT NULL, " +
								 		"`ADDRESS` varchar(500) NOT NULL, " +
								 		"`partner_id` int(11) NOT NULL, " +
								 		"`home_village_id` int(11) NOT NULL, " +
								 		"`equipmentholder_id` int(11) default NULL, " +
								 		"KEY `ANIMATOR_partner_id` (`partner_id`), " +
								 		"KEY `ANIMATOR_home_village_id` (`home_village_id`), " +
								 		"KEY `ANIMATOR_equipmentholder_id` (`equipmentholder_id`))";
	
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

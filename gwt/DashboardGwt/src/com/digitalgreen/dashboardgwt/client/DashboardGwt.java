package com.digitalgreen.dashboardgwt.client;

import java.util.HashMap;

import com.google.gwt.core.client.EntryPoint;
import com.digitalgreen.dashboardgwt.client.servlets.Blocks;
import com.digitalgreen.dashboardgwt.client.servlets.Index;
import com.digitalgreen.dashboardgwt.client.common.ApplicationConstants;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.BaseData;
import com.digitalgreen.dashboardgwt.client.servlets.*;


public class DashboardGwt implements EntryPoint {
	// Some globals
	public HashMap hMap = new HashMap();

	public void onModuleLoad() {
		setup();
		Index index  = new Index();
		index.response();
	}

	/* Sets the status of the application as online / offline
	 * This function is called every time the application is refreshed */ 
	private void setup(){
		try{
			BaseData.dbCheck();
			BaseData instance = new BaseData();
			if(instance.checkIfUserTableExists()) {
				int status = instance.getApplicationStatus();
				if(status == 0){
					ApplicationConstants.toggleConnection(false);
				}
				else{
					ApplicationConstants.toggleConnection(true);
				}	
			}
			else{
				ApplicationConstants.toggleConnection(true);
			}
			ApplicationConstants.createMappingBetweenTableIDAndDataObject();
		}catch(Exception e){
			ApplicationConstants.toggleConnection(true);
			ApplicationConstants.createMappingBetweenTableIDAndDataObject();

		}
	}
	
	private void createHashMap() {
		RequestContext requestContext = null;
		// AnimatorAssignedVillages
		hMap.put("dashboard/animatorassignedvillage", new AnimatorAssignedVillages());
		// Add AnimatorAssignedVillages
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "add");
		hMap.put("dashboard/animatorassignedvillage/add", new AnimatorAssignedVillages(requestContext));
		
		// Animators
		hMap.put("", new Animators());
		// Add Animators
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "add");
		hMap.put("", new Animators(requestContext));
		
		// Blocks
		hMap.put("", new Blocks());
		// Add Blocks
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "add");
		hMap.put("", new Blocks(requestContext));
		
		// DevelopmentManagers
		hMap.put("", new DevelopmentManagers());
		// Add DevelopmentManagers
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "add");
		hMap.put("", new DevelopmentManagers(requestContext));
		
		// Districts
		hMap.put("", new Districts());
		// Add Districts
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "add");
		hMap.put("", new Districts(requestContext));
		
		// Equipments
		hMap.put("", new Equipments());
		// Add Equipments
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "add");
		hMap.put("", new Equipments(requestContext));
		
		// FieldOfficers
		hMap.put("", new FieldOfficers());
		// Add FieldOfficers
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "add");
		hMap.put("", new FieldOfficers(requestContext));
		
		// Languages
		hMap.put("", new Languages());
		// Add Languages
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "add");
		hMap.put("", new Languages(requestContext));
		
		// Partners
		hMap.put("", new Partners());
		// Add Partners
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "add");
		hMap.put("", new Partners(requestContext));
		
		// PersonGroups
		hMap.put("", new PersonGroups());
		// Add PersonGroups
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "add");
		hMap.put("", new PersonGroups(requestContext));
		
		// Persons
		hMap.put("", new Persons());
		// Add Persons
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "add");
		hMap.put("", new Persons(requestContext));
		
		// Regions
		hMap.put("", new Regions());
		// Add Regions
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "add");
		hMap.put("", new Regions(requestContext));
		
		// Screenings
		hMap.put("", new Screenings());
		// Add Screenings
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "add");
		hMap.put("", new Screenings(requestContext));
		
		// States
		hMap.put("", new States());
		// Add States
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "add");
		hMap.put("", new States(requestContext));
		
		// Trainings
		hMap.put("", new Trainings());
		// Add Trainings
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "add");
		hMap.put("", new Trainings(requestContext));
		
		// Videos
		hMap.put("", new Videos());
		// Add Videos
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "add");
		hMap.put("", new Videos(requestContext));
		
		// Villages
		hMap.put("", new Villages());
		// Add Villages
		requestContext = new RequestContext();
		requestContext.getArgs().put("action", "add");
		hMap.put("", new Villages(requestContext));
	}
}

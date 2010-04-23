package com.digitalgreen.dashboardgwt.client.templates;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.BlocksData;
import com.digitalgreen.dashboardgwt.client.servlets.Blocks;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.Hyperlink;

public class BlocksTemplate extends BaseTemplate{
	
	public BlocksTemplate(RequestContext requestContext) {
		super(requestContext);
	}
	
	@Override
	public void fill() {
		String templateType = "Block";
		String templatePlainType = "dashboard/block/add/";
		RequestContext requestContext = new RequestContext();
		HashMap args = new HashMap();
		args.put("action", "add");
		requestContext.setArgs(args);
		Blocks addBlocksServlet = new Blocks(requestContext);
		RequestContext saveRequestContext = new RequestContext(RequestContext.METHOD_POST);
		Form saveForm = new Form((new BlocksData()).getNewData());
		saveRequestContext.setForm(saveForm);
		Blocks saveBlock = new Blocks(saveRequestContext);
		
		// Draw the content of the template depending on the request type (GET/POST)
		super.fillDGTemplate(templateType, blocksListHtml, blocksAddHtml, addDataToElementID);
		// Add it to the rootpanel
		super.fill();
		//Now add listings
		List<Hyperlink> links =  this.fillListings();
		// Now add hyperlinks
		super.fillDgListPage(templatePlainType, templateType, blocksListFormHtml, addBlocksServlet, links);
		// Now add any submit control buttons
		super.fillDgFormPage(saveBlock);
	}
	
	protected List<Hyperlink> fillListings(){
		HashMap queryArgs = this.getRequestContext().getArgs();
		String queryArg = (String)queryArgs.get("action");
		List<Hyperlink> links = new ArrayList<Hyperlink>();
		if(queryArg == null || queryArg != "add") {
			List blocks = (List)queryArgs.get("listing");
			if(blocks  != null){
				String tableRows ="";
				String style;
				BlocksData.Data block;
				RequestContext requestContext = null;
				for (int row = 0; row < blocks.size(); ++row) {
					if(row%2==0)
						style= "row2";
					else
						style = "row1";
					block = (BlocksData.Data)blocks.get(row);
					requestContext = new RequestContext();
					requestContext.getArgs().put("action", "edit");
					requestContext.getArgs().put("id", block.getId());
					links.add(this.createHyperlink("<a href='#dashboard/block/"+ block.getId() +"/'>" +
							block.getBlockName() + "</a>", new Blocks(requestContext)));
					tableRows += "<tr class='" + style + "'>" +
								"<td><input type='checkbox' class='action-select' value='" + block.getId() + "' name='_selected_action' /></td>" +
								"<th id = 'row" + row + "'></th>" +
								"<td>" + block.getDistrict().getDistrictName()  + "</td>" +
								"</tr>";
				}
				blocksListFormHtml = blocksListFormHtml + tableRows + "</tbody></table>";
			}
		}
		return links;
	}
	
	final private String addDataToElementID[] = {"id_district"};
	
	private String blocksListFormHtml = "<div class='actions'>" +
								"<label>Action: <select name='action'>" +
									"<option value='' selected='selected'>---------</option>" +
									"<option value='delete_selected'>Delete selected blocks</option>" +
									"</select>" +
								"</label>" +
								"<button type='submit' class='button' title='Run the selected action' name='index' value='0'>Go</button>" +
								"</div>" +
								"<table cellspacing='0'>" +
									"<thead>" +
										"<tr>" +
											"<th>" +
												"<input type='checkbox' id='action-toggle' />" +
											"</th>" +
											"<th>" +
												"<a href='?ot=asc&amp;o=1'>" +
												"Block name" +
												"</a>" +
											"</th>" +
											"<th>" +
												"<a href='?ot=asc&amp;o=2'>" +
													"District" +
												"</a>" +
												"</th>" +
										"</tr>" +
									"</thead>" +
									"<tbody>";
	
	final private String blocksListHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
							"<div id='content' class='flex'>" +
								"<h1>Select Block to change</h1>" +
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
	
	final private String blocksAddHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
							"<div id='content' class='colM'>" +
								"<h1>Add Block</h1>" +
								"<div id='content-main'>" +
									"<fieldset class='module aligned '>" +
										"<div class='form-row block_name  '>" +
											"<div>" +
												"<label for='id_block_name' class='required'>Block name:</label><input id='id_block_name' type='text' class='vTextField' name='block_name' maxlength='100' />" +
											"</div>" +
										"</div>" +
										"<div class='form-row start_date  '>" +
											"<div>" +
												"<label for='id_start_date'>Start date:</label><input id='id_start_date' type='text' class='vDateField' name='start_date' size='10' />" +
											"</div>" +
										"</div>" +
										"<div class='form-row district  '>" +
											"<div>" +
												"<label for='id_district' class='required'>District:</label><select name='district' id='id_district'>" +
													"<option value='' selected='selected'>---------</option>" +
													"</select>" +
											"</div>" +
										"</div>" +
									"</fieldset>" +
									"<div class='submit-row' >" +
										"<input id='save' value='Save' class='default' name='_save' />" +
									"</div>" +
									"<script type='text/javascript'>document.getElementById('id_block_name').focus();</script>" +
								"</div>" +
							"</div>" +
							"<script src='/media/js/admin/DateTimeShortcuts.js' type='text/javascript'></script>" +	
							"<script type='text/javascript'>DateTimeShortcuts.init()</script>";
}

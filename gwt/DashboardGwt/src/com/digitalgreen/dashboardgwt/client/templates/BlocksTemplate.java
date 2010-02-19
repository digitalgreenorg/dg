package com.digitalgreen.dashboardgwt.client.templates;

import java.util.HashMap;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.servlets.Blocks;

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
		Blocks region = new Blocks(new RequestContext(RequestContext.METHOD_POST, 
				getPostForm()));
		// Draw the content of the template depending on the request type (GET/POST)
		super.fillDGTemplate(templateType, blocksListHtml, blocksAddHtml);
		// Add it to the rootpanel
		super.fill();
		// Now add hyperlinks
		super.fillDGLinkControls(templatePlainType, templateType, blocksListFormHtml, addBlocksServlet);
		// Now add any submit control buttons
		super.fillDGSubmitControls(region);
	}
	
	final static private String blocksListFormHtml = "<div class='actions'>" +
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
									"<tbody>"+
										"<div id='data-rows'" +       // Insert data rows here
										"</div>" +
									"</tbody>" +
								"</table>";
	
	final static private String blocksListHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
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
	
	final static private String blocksAddHtml = "<link rel='stylesheet' type='text/css' href='/media/css/forms.css' />" +
							"<div id='content' class='colM'>" +
								"<h1>Add Block</h1>" +
								"<div id='content-main'>" +
									"<form enctype='multipart/form-data' action='' method='post' id='block_form'>" +
										"<div>" +
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
															"</select><a href='/admin/dashboard/district/add/' class='add-another' id='add_id_district' onclick='return showAddAnotherPopup(this);'> <img src='/media/img/admin/icon_addlink.gif' width='10' height='10' alt='Add Another'/></a>" +
													"</div>" +
												"</div>" +
											"</fieldset>" +
											"<div class='submit-row' >" +
												"<input type='submit' value='Save' class='default' name='_save' />" +
											"</div>" +
											"<script type='text/javascript'>document.getElementById('id_block_name').focus();</script>" +
											"<script type='text/javascript'>" +
											"</script>" +
										"</div>" +
									"</form>" +
								"</div>" +
							"</div>";
}

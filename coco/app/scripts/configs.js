define([],
function() {
    
    /*
    var dummy_config = {
        entity_name : 
        //string = key of this object in all_config, name of objectstore in IDB
        //for - accessing this object 
        
        'rest_api_url': '/coco/api/v1/village/',
        //string - the rest url for this entity
    
        'dashboard_display': {
            listing: false,         //whether to provide listing option for this entity on dashboard
            add: false              //whether to provide add option for this entity on dashboard
        },
    
        -----------------------------------Listing configs---------------------------------
        page_header: 'Village',  
        //string = The name that needs to shown in headers 

        list_table_header_template: 'village_table_template',  
        //HTML template - The id of template used as coloumn headers in list page

        list_table_row_template: 'village_list_item_template',  
        //HTML template - The id of template used to create rows of list table. 
        //This template is passed the model json.
        -----------------------------------------------------------------------------------
    
        ----------------------------------Form configs-------------------------------------
        foreign_entities: {
            f_entity_name:{         //the entity_name of foreign element
                attribute_name:{    //the attribute name of this foreign element in json
                    
                    'placeholder': 'string - the id of element in form's html where the dropdown of this f_entity is inserted',
                    
                    'name_field': 'string - the attribute name in f_entity's json which needs to be shown in its dropdown',
                    
                    'dependency': [{    // whether this elements's dropdown depends on value of other form elements
                        'source_form_element': 'village',   // attribute name of source element in json
                        'dep_attr': 'village'   //the attribute name in json of dependent f_entity which refers to source f_entity
                        'src_attr' : //to compare dep_attr of dependent element with a particular attribute in source f_entity
                    }],
                    
                    'filter': { //whether to filter the objects of foreign entity before rendering into dropdown
                        attr: 'group',  //the attribute name in f_entity's json to filter on
                        value: null     //desired value of the attr
                    },
    
                    id_field: "person_id", // the name of id field for this f_entity in denormalised json                         
                }
            },
    
            f_entity_name:{         //the entity_name of foreign element
                attribute_name:{    //the attribute name of this foreign element in json
                    
                    'dependency': [{    // whether this elements's dropdown depends on value of other form elements
                        'source_form_element': 'village',   // attribute name of source element in json
                        'dep_attr': 'village'   //the attribute name in json of dependent f_entity which refers to source f_entity
                    }],

                    id_field: "person_id", // the name of id field for this f_entity in denormalised json     

                    //would not use options template to render its objects - would use the specfied template    
                    // won't be denormalised, wud be converted offline to online, 
                    //any field to be denormalised or converted offline to online can be declared - 
                    //this shd be clubbed and put as foreign entity of expanded.   
                    'expanded': { 
                        template: 'person_pma_template', // the template to use instead of options
                        placeholder: 'pmas',    // the id of placeholder in form's HTML
                        TODO: the following two should be merged and converted to same format as foreign_entities
                        denormalize: { // any field in expanded template to be denormalised     
                            "expressed_adoption_video": {
                                name_field: 'title' //used as key for name in denormalised object
                            }
                        },
                        foreign_fields: { // any more field in expanded template for offline to online conv
                            "expressed_adoption_video": {
                                entity_name: "video"  //the entity_name for this f_entity element
                            }
                        },
                        extra_fields: ["expressed_question", "interested", "expressed_adoption_video"]
                    }
                }
            }
        },    
        //object - describes the foreign keys in the json of this entity's model.
        //To convert between online offline namespaces, denormalize-normalize json    
    
        inline: {
            'entity': 'person',     //entity name of inline
    
            'default_num_rows': 10,         //default num of rows to show
    
            "template": "person_inline",    //id of template used to render inline
            //Include any jquery validation desired inside html of rows 
            //TODO: need to explain the <%index%> tags required in inlines
    
            "foreign_attribute": {
                'host_attribute': ["id", "group_name"],
                'inline_attribute': "group"
            },
            "header": "person_inline_header",
            'borrow_attributes': [{
                'host_attribute': 'village',
                'inline_attribute': 'village'
            }]
        },      
        //object - describes inlines to be included in this entity's form

        bulk:{},     
        //object - if multiple objects of this entity type can be saved through its add form, describe configs of object 
        ------------------------------------------------------------------------------------
    }
    */
    
    // //This template would be passed the json of inline model and shall produce the desired row
//     TODO: maybe instead of relying on users to use templating lang we should fill the rows ourselves in js code, like we are doing in form!

	var state_configs = {
	        'page_header': 'State',
	        'list_table_header_template': 'state_table_template', 
	        'list_table_row_template': 'state_list_item_template',
	    	//'add_template_name': 'state_add_edit_template',
	        //'edit_template_name': 'state_add_edit_template',
	        'rest_api_url': '/api/v1/State/',
	        'entity_name': 'state',
	        'dashboard_display': {
	            listing: false,
	            add: false
	        },
	        'sort_field': 'state_name'
	    };

	var project_configs = {
	        'page_header': 'Project',
	        'list_table_header_template': 'project_table_template', 
	        'list_table_row_template': 'project_list_item_template',
	    	//'add_template_name': 'project_add_edit_template',
	        //'edit_template_name': 'project_add_edit_template',
	        'rest_api_url': '/api/v1/Project/',
	        'entity_name': 'project',
	        'dashboard_display': {
	            listing: false,
	            add: false
	        },
	        'sort_field': 'project_name'
	    };
	
	var progress_configs = {
			'entity_name' : 'progress',
			'rest_api_url' : '/api/v1/Progress/',
			'dashboard_display' : {
	    		listing : true,
	    		add : true
	    	},
			'page_header': 'Progres',
			'list_table_header_template': 'progress_table_template',
			'list_table_row_template': 'progress_list_item_template',
	    	'add_template_name': 'progress_add_edit_template',
	        'edit_template_name': 'progress_add_edit_template',
	        'foreign_entities': {
	        	'state':{
	        		'state':{
	        			'placeholder': 'id_state',
	        			'name_field': 'state_name'
	        		},
	        	},
	        	'project':{
	        		'project':{
	        			'placeholder': 'id_project',
	        			'name_field': 'project_name'
	        		},
	        	},
	        },
	        'unique_together_fields': ['state.id', 'project.id', 'month', 'year'],
	        'sort_field': 'state',
	        'form_field_validation': {
	        	ignore: [],
	        	rules: {
	        		state: "required",
	        		project: "required",
	        		Two_1: {
	        			required: true,
	        			digits: true
	        		},
	        		Two_2: {
	        			required: true,
	        			digits: true
	        		},
		    		Two_3: {
		    			required: true,
		    			digits: true
		    		},
		    		Three_1: {
		    			required: true,
		    			digits: true
		    		},
	        		Three_2: {
		    			required: true,
		    			digits: true
		    		},
		    		Three_4: {
		    			required: true,
		    			digits: true
		    		},
		    		Three_5: {
		    			required: true,
		    			digits: true
		    		},
		    		Three_6: {
		    			required: true,
		    			digits: true
		    		},
		    		Three_7: {
		    			required: true,
		    			digits: true
		    		},
		    		Three_8: {
		    			required: true,
		    			digits: true
		    		},
		    		Four_1: {
		    			required: true,
		    			digits: true
		    		},
		    		Four_2: {
		    			required: true,
		    			digits: true
		    		},
		    		Four_3: {
		    			required: true,
		    			digits: true
		    		},
		    		Four_4: {
		    			required: true,
		    			digits: true
		    		},
		    		Four_5: {
		    			required: true,
		    			digits: true
		    		},
		    		Four_6: {
		    			required: true,
		    			digits: true
		    		},
			        Five_1: {
		    			required: true,
		    			digits: true
		    		},
			        Five_2: {
		    			required: true,
		    			digits: true
		    		},
			        Five_5: {
		    			required: true,
		    			digits: true
		    		},
			        Five_6: {
		    			required: true,
		    			digits: true
		    		},
			        Five_7: {
		    			required: true,
		    			digits: true
		    		},
			        Five_8: {
		    			required: true,
		    			digits: true
		    		},
			        Five_9: {
		    			required: true,
		    			digits: true
		    		},
			        Five_10: {
		    			required: true,
		    			number: true
		    		},
			        Five_11: {
		    			required: true,
		    			number: true
		    		},
			        Five_12: {
		    			required: true,
		    			number: true
		    		},
			        Five_13: {
		    			required: true,
		    			number: true
		    		},
			        Five_14: {
		    			required: true,
		    			number: true
		    		},
	        		Six_1: {
	        			required: true,
		    			digits: true
	        		},
			        Six_2: {
		    			required: true,
		    			digits: true
		    		},
			        Six_5: {
		    			required: true,
		    			digits: true
		    		},
			        Six_6: {
		    			required: true,
		    			digits: true
		    		},
			        Six_7: {
		    			required: true,
		    			digits: true
		    		},
			        Six_8: {
		    			required: true,
		    			digits: true
		    		},
			        Six_9: {
		    			required: true,
		    			digits: true
		    		},
			        Six_10: {
		    			required: true,
		    			number: true
		    		},
			        Six_11: {
		    			required: true,
		    			number: true
		    		},
			        Six_12: {
		    			required: true,
		    			number: true
		    		},
			        Six_13: {
		    			required: true,
		    			number: true
		    		},
			        Six_14: {
		    			required: true,
		    			number: true
		    		},
	        		Seven_1: {
	        			required: true,
	        			digits: true
	        		},
	        		Seven_2: {
	        			required: true,
	        			digits: true
	        		},
	        		Seven_3: {
	        			required: true,
	        			digits: true
	        		},
	        		Seven_4: {
	        			required: true,
	        			digits: true
	        		},
	        		Seven_5: {
	        			required: true,
	        			digits: true
	        		},
	        		Seven_6: {
	        			required: true,
	        			number: true
	        		},
	        		Seven_7: {
	        			required: true,
	        			digits: true
	        		},
	        		Seven_8: {
	        			required: true,
	        			digits: true
	        		},
	        		Seven_9: {
	        			required: true,
	        			number: true
	        		},
	        		month: "required",
	        		year: {
	        			required:true,
	        			datecheck: {month : "month"}
	        		}
	        	},

	        messages: {
	        	month: {
	        		required: "Please select the month for which data is being reported",
	        	},
	        	year: {
	        		required: "Please select the year for which data is being reported",
	        		datecheck: "Please enter correct and valid date"
	        	},
	        	state: "Please select the state for which data is being reported",
	        	project: "Please select the project name for which data is being reported",
	        	Two_1: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Two_2: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Two_3: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Three_1: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Three_2: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Three_4: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Three_5: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Three_6: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Three_7: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Three_8: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Four_1: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Four_2: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Four_3: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Four_4: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Four_5: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Four_6: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Five_1: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Five_2: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Five_5: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Five_6: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Five_7: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Five_8: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Five_9: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Five_10: {
	        		required: "This question is required, please enter the details",
	        		number: "Please enter a valid amount (Rs. in Lakhs)"
	        	},
	        	Five_11: {
	        		required: "This question is required, please enter the details",
	        		number: "Please enter a valid amount (Rs. in Lakhs)"
	        	},
	        	Five_12: {
	        		required: "This question is required, please enter the details",
	        		number: "Please enter a valid amount (Rs. in Lakhs)"
	        	},
	        	Five_13: {
	        		required: "This question is required, please enter the details",
	        		number: "Please enter a valid amount (Rs. in Lakhs)"
	        	},
	        	Five_14: {
	        		required: "This question is required, please enter the details",
	        		number: "Please enter a valid amount (Rs. in Lakhs)"
	        	},
	        	Six_1: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Six_2: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Six_5: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Six_6: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Six_7: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Six_8: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Six_9: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Six_10: {
	        		required: "This question is required, please enter the details",
	        		number: "Please enter a valid amount (Rs. in Lakhs)"
	        	},
	        	Six_11: {
	        		required: "This question is required, please enter the details",
	        		number: "Please enter a valid amount (Rs. in Lakhs)"
	        	},
	        	Six_12: {
	        		required: "This question is required, please enter the details",
	        		number: "Please enter a valid amount (Rs. in Lakhs)"
	        	},
	        	Six_13: {
	        		required: "This question is required, please enter the details",
	        		number: "Please enter a valid amount (Rs. in Lakhs)"
	        	},
	        	Six_14: {
	        		required: "This question is required, please enter the details",
	        		number: "Please enter a valid amount (Rs. in Lakhs)"
	        	},
	        	Seven_1: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Seven_2: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Seven_3: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Seven_4: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Seven_5: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Seven_6: {
	        		required: "This question is required, please enter the details",
	        		number: "Please enter a valid amount (Rs. in Lakhs)"
	        	},
	        	Seven_7: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Seven_8: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Seven_9: {
	        		required: "This question is required, please enter the details",
	        		number: "Please enter a valid amount (Rs. in Lakhs)"
	        	},
	        },

            highlight: function(element, errorClass, validClass) {
                $(element)
                    .parent('div')
                    .parent('div')
                    .addClass("error");

            },
            unhighlight: function(element, errorClass, validClass) {
                $(element)
                    .parent('div')
                    .parent('div')
                    .removeClass("error");

            },
            errorElement: "span",
            errorClass: "help-inline"
	    }
	};
	
	var progresstill13_configs = {
			'entity_name' : 'progresstill13',
			'rest_api_url' : '/api/v1/ProgressTill13/',
			'dashboard_display' : {
	    		listing : true,
	    		add : true
	    	},
			'page_header': 'Prev Prog',
			'list_table_header_template': 'progresstill13_table_template',
			'list_table_row_template': 'progresstill13_list_item_template',
	    	'add_template_name': 'progresstill13_add_edit_template',
	        'edit_template_name': 'progresstill13_add_edit_template',
	        'foreign_entities': {
	        	'state':{
	        		'state':{
	        			'placeholder': 'id_state',
	        			'name_field': 'state_name'
	        		},
	        	},
	        	'project':{
	        		'project':{
	        			'placeholder': 'id_project',
	        			'name_field': 'project_name'
	        		},
	        	},
	        },
	        'unique_together_fields': ['state.id', 'project.id', 'month', 'year'],
	        'sort_field': 'state',
	        'form_field_validation': {
	        	ignore: [],
	        	rules: {
	        		state: "required",
	        		project: "required",
	        		Two_1: {
	        			required: true,
	        			digits: true
	        		},
	        		Two_2: {
	        			required: true,
	        			digits: true
	        		},
		    		Two_3: {
		    			required: true,
		    			digits: true
		    		},
		    		Three_1: {
		    			required: true,
		    			digits: true
		    		},
	        		Three_2: {
		    			required: true,
		    			digits: true
		    		},
		    		Three_4: {
		    			required: true,
		    			digits: true
		    		},
		    		Three_5: {
		    			required: true,
		    			digits: true
		    		},
		    		Three_6: {
		    			required: true,
		    			digits: true
		    		},
		    		Three_7: {
		    			required: true,
		    			digits: true
		    		},
		    		Three_8: {
		    			required: true,
		    			digits: true
		    		},
		    		Four_1: {
		    			required: true,
		    			digits: true
		    		},
		    		Four_2: {
		    			required: true,
		    			digits: true
		    		},
		    		Four_3: {
		    			required: true,
		    			digits: true
		    		},
		    		Four_4: {
		    			required: true,
		    			digits: true
		    		},
		    		Four_5: {
		    			required: true,
		    			digits: true
		    		},
		    		Four_6: {
		    			required: true,
		    			digits: true
		    		},
			        Five_1: {
		    			required: true,
		    			digits: true
		    		},
			        Five_2: {
		    			required: true,
		    			digits: true
		    		},
			        Five_5: {
		    			required: true,
		    			digits: true
		    		},
			        Five_6: {
		    			required: true,
		    			digits: true
		    		},
			        Five_7: {
		    			required: true,
		    			digits: true
		    		},
			        Five_8: {
		    			required: true,
		    			digits: true
		    		},
			        Five_9: {
		    			required: true,
		    			digits: true
		    		},
			        Five_10: {
		    			required: true,
		    			number: true
		    		},
			        Five_11: {
		    			required: true,
		    			number: true
		    		},
			        Five_12: {
		    			required: true,
		    			number: true
		    		},
			        Five_13: {
		    			required: true,
		    			number: true
		    		},
			        Five_14: {
		    			required: true,
		    			number: true
		    		},
	        		Six_1: {
	        			required: true,
		    			digits: true
	        		},
			        Six_2: {
		    			required: true,
		    			digits: true
		    		},
			        Six_5: {
		    			required: true,
		    			digits: true
		    		},
			        Six_6: {
		    			required: true,
		    			digits: true
		    		},
			        Six_7: {
		    			required: true,
		    			digits: true
		    		},
			        Six_8: {
		    			required: true,
		    			digits: true
		    		},
			        Six_9: {
		    			required: true,
		    			digits: true
		    		},
			        Six_10: {
		    			required: true,
		    			number: true
		    		},
			        Six_11: {
		    			required: true,
		    			number: true
		    		},
			        Six_12: {
		    			required: true,
		    			number: true
		    		},
			        Six_13: {
		    			required: true,
		    			number: true
		    		},
			        Six_14: {
		    			required: true,
		    			number: true
		    		},
	        		Seven_1: {
	        			required: true,
	        			digits: true
	        		},
	        		Seven_2: {
	        			required: true,
	        			digits: true
	        		},
	        		Seven_3: {
	        			required: true,
	        			digits: true
	        		},
	        		Seven_4: {
	        			required: true,
	        			digits: true
	        		},
	        		Seven_5: {
	        			required: true,
	        			digits: true
	        		},
	        		Seven_6: {
	        			required: true,
	        			number: true
	        		},
	        		Seven_7: {
	        			required: true,
	        			digits: true
	        		},
	        		Seven_8: {
	        			required: true,
	        			digits: true
	        		},
	        		Seven_9: {
	        			required: true,
	        			number: true
	        		},
	        		month: "required",
	        		year: {
	        			required:true,
	        			datecheck: {month : "month"}
	        		}
	        	},

	        messages: {
	        	month: {
	        		required: "Please select the month for which data is being reported",
	        	},
	        	year: {
	        		required: "Please select the year for which data is being reported",
	        		datecheck: "Please enter correct and valid date"
	        	},
	        	state: "Please select the state for which data is being reported",
	        	project: "Please select the project name for which data is being reported",
	        	Two_1: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Two_2: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Two_3: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Three_1: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Three_2: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Three_4: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Three_5: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Three_6: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Three_7: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Three_8: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Four_1: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Four_2: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Four_3: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Four_4: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Four_5: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Four_6: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Five_1: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Five_2: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Five_5: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Five_6: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Five_7: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Five_8: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Five_9: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Five_10: {
	        		required: "This question is required, please enter the details",
	        		number: "Please enter a valid amount (Rs. in Lakhs)"
	        	},
	        	Five_11: {
	        		required: "This question is required, please enter the details",
	        		number: "Please enter a valid amount (Rs. in Lakhs)"
	        	},
	        	Five_12: {
	        		required: "This question is required, please enter the details",
	        		number: "Please enter a valid amount (Rs. in Lakhs)"
	        	},
	        	Five_13: {
	        		required: "This question is required, please enter the details",
	        		number: "Please enter a valid amount (Rs. in Lakhs)"
	        	},
	        	Five_14: {
	        		required: "This question is required, please enter the details",
	        		number: "Please enter a valid amount (Rs. in Lakhs)"
	        	},
	        	Six_1: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Six_2: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Six_5: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Six_6: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Six_7: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Six_8: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Six_9: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Six_10: {
	        		required: "This question is required, please enter the details",
	        		number: "Please enter a valid amount (Rs. in Lakhs)"
	        	},
	        	Six_11: {
	        		required: "This question is required, please enter the details",
	        		number: "Please enter a valid amount (Rs. in Lakhs)"
	        	},
	        	Six_12: {
	        		required: "This question is required, please enter the details",
	        		number: "Please enter a valid amount (Rs. in Lakhs)"
	        	},
	        	Six_13: {
	        		required: "This question is required, please enter the details",
	        		number: "Please enter a valid amount (Rs. in Lakhs)"
	        	},
	        	Six_14: {
	        		required: "This question is required, please enter the details",
	        		number: "Please enter a valid amount (Rs. in Lakhs)"
	        	},
	        	Seven_1: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Seven_2: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Seven_3: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Seven_4: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Seven_5: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Seven_6: {
	        		required: "This question is required, please enter the details",
	        		number: "Please enter a valid amount (Rs. in Lakhs)"
	        	},
	        	Seven_7: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Seven_8: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Seven_9: {
	        		required: "This question is required, please enter the details",
	        		number: "Please enter a valid amount (Rs. in Lakhs)"
	        	},
	        },

            highlight: function(element, errorClass, validClass) {
                $(element)
                    .parent('div')
                    .parent('div')
                    .addClass("error");

            },
            unhighlight: function(element, errorClass, validClass) {
                $(element)
                    .parent('div')
                    .parent('div')
                    .removeClass("error");

            },
            errorElement: "span",
            errorClass: "help-inline"
	    }
	};
	
	var target_configs = {
			'entity_name' : 'target',
			'rest_api_url' : '/api/v1/Target/',
			'dashboard_display' : {
	    		listing : true,
	    		add : true
	    	},
			'page_header': 'Target',
			'list_table_header_template': 'target_table_template',
			'list_table_row_template': 'target_list_item_template',
	    	'add_template_name': 'target_add_edit_template',
	        'edit_template_name': 'target_add_edit_template',
	        'foreign_entities': {
	        	'state':{
	        		'state':{
	        			'placeholder': 'id_state',
	        			'name_field': 'state_name'
	        		},
	        	},
	        	'project':{
	        		'project':{
	        			'placeholder': 'id_project',
	        			'name_field': 'project_name'
	        		},
	        	},
	        },
	        'unique_together_fields': ['state.id', 'project.id', 'year'],
	        'sort_field': 'state',
	        'form_field_validation': {
	        	ignore: [],
	        	rules: {
	        		state: "required",
	        		project: "required",
	        		Two_1: {
	        			required: true,
	        			digits: true
	        		},
	        		Two_2: {
	        			required: true,
	        			digits: true
	        		},
		    		Two_3: {
		    			required: true,
		    			digits: true
		    		},
		    		Three_1: {
		    			required: true,
		    			digits: true
		    		},
	        		Three_2: {
		    			required: true,
		    			digits: true
		    		},
		    		Three_4: {
		    			required: true,
		    			digits: true
		    		},
		    		Three_5: {
		    			required: true,
		    			digits: true
		    		},
		    		Three_6: {
		    			required: true,
		    			digits: true
		    		},
		    		Three_7: {
		    			required: true,
		    			digits: true
		    		},
		    		Three_8: {
		    			required: true,
		    			digits: true
		    		},
		    		Four_1: {
		    			required: true,
		    			digits: true
		    		},
		    		Four_2: {
		    			required: true,
		    			digits: true
		    		},
			        Five_5: {
		    			required: true,
		    			digits: true
		    		},
			        Five_6: {
		    			required: true,
		    			digits: true
		    		},
			        Five_7: {
		    			required: true,
		    			digits: true
		    		},
			        Five_8: {
		    			required: true,
		    			digits: true
		    		},
			        Five_9: {
		    			required: true,
		    			digits: true
		    		},
			        Five_10: {
		    			required: true,
		    			number: true
		    		},
			        Five_11: {
		    			required: true,
		    			number: true
		    		},
			        Five_12: {
		    			required: true,
		    			number: true
		    		},
			        Five_13: {
		    			required: true,
		    			number: true
		    		},
			        Five_14: {
		    			required: true,
		    			number: true
		    		},
			        Six_2: {
		    			required: true,
		    			digits: true
		    		},
			        Six_5: {
		    			required: true,
		    			digits: true
		    		},
			        Six_6: {
		    			required: true,
		    			digits: true
		    		},
			        Six_7: {
		    			required: true,
		    			digits: true
		    		},
			        Six_8: {
		    			required: true,
		    			digits: true
		    		},
			        Six_9: {
		    			required: true,
		    			digits: true
		    		},
			        Six_10: {
		    			required: true,
		    			number: true
		    		},
			        Six_11: {
		    			required: true,
		    			number: true
		    		},
			        Six_12: {
		    			required: true,
		    			number: true
		    		},
			        Six_13: {
		    			required: true,
		    			number: true
		    		},
			        Six_14: {
		    			required: true,
		    			number: true
		    		},
	        		Seven_1: {
	        			required: true,
	        			digits: true
	        		},
	        		Seven_2: {
	        			required: true,
	        			digits: true
	        		},
	        		Seven_3: {
	        			required: true,
	        			digits: true
	        		},
	        		Seven_4: {
	        			required: true,
	        			digits: true
	        		},
	        		Seven_5: {
	        			required: true,
	        			digits: true
	        		},
	        		Seven_6: {
	        			required: true,
	        			number: true
	        		},
	        		Seven_7: {
	        			required: true,
	        			digits: true
	        		},
	        		Seven_8: {
	        			required: true,
	        			digits: true
	        		},
	        		Seven_9: {
	        			required: true,
	        			number: true
	        		},
	        		Col4_SC: {
	        			required: true,
	        			digits: true
	        		},
	        		Col5_SC: {
	        			required: true,
	        			number: true
	        		},
	        		Col7_SC: {
	        			required: true,
	        			digits: true
	        		},
	        		Col8_SC: {
	        			required: true,
	        			number: true
	        		},
	        		Col4_ST: {
	        			required: true,
	        			digits: true
	        		},
	        		Col5_ST: {
	        			required: true,
	        			number: true
	        		},
	        		Col7_ST: {
	        			required: true,
	        			digits: true
	        		},
	        		Col8_ST: {
	        			required: true,
	        			number: true
	        		},
	        		Col4_Min: {
	        			required: true,
	        			digits: true
	        		},
	        		Col5_Min: {
	        			required: true,
	        			number: true
	        		},
	        		Col7_Min: {
	        			required: true,
	        			digits: true
	        		},
	        		Col8_Min: {
	        			required: true,
	        			number: true
	        		},
	        		Col4_Oth: {
	        			required: true,
	        			digits: true
	        		},
	        		Col5_Oth: {
	        			required: true,
	        			number: true
	        		},
	        		Col7_Oth: {
	        			required: true,
	        			digits: true
	        		},
	        		Col8_Oth: {
	        			required: true,
	        			number: true
	        		},
	        		Col4_PWD: {
	        			required: true,
	        			digits: true
	        		},
	        		Col5_PWD: {
	        			required: true,
	        			number: true
	        		},
	        		Col7_PWD: {
	        			required: true,
	        			digits: true
	        		},
	        		Col8_PWD: {
	        			required: true,
	        			number: true
	        		},
	        		year: {
	        			required: true,
	        			validateYear: true
	        		}
	        	},
	        messages: {
	        	year: {
	        		required: "Please select the year for which data is being reported",
	        		validateYear: "Please check year"
	        	},
	        	state: "Please select the state for which data is being reported",
	        	project: "Please select the project name for which data is being reported",
	        	Two_1: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Two_2: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Two_3: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Three_1: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Three_2: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Three_4: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Three_5: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Three_6: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Three_7: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Three_8: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Four_1: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Four_2: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Five_5: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Five_6: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Five_7: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Five_8: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Five_9: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Five_10: {
	        		required: "This question is required, please enter the details",
	        		number: "Please enter a valid amount (Rs. in Lakhs)"
	        	},
	        	Five_11: {
	        		required: "This question is required, please enter the details",
	        		number: "Please enter a valid amount (Rs. in Lakhs)"
	        	},
	        	Five_12: {
	        		required: "This question is required, please enter the details",
	        		number: "Please enter a valid amount (Rs. in Lakhs)"
	        	},
	        	Five_13: {
	        		required: "This question is required, please enter the details",
	        		number: "Please enter a valid amount (Rs. in Lakhs)"
	        	},
	        	Five_14: {
	        		required: "This question is required, please enter the details",
	        		number: "Please enter a valid amount (Rs. in Lakhs)"
	        	},
	        	Six_2: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Six_5: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Six_6: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Six_7: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Six_8: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Six_9: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Six_10: {
	        		required: "This question is required, please enter the details",
	        		number: "Please enter a valid amount (Rs. in Lakhs)"
	        	},
	        	Six_11: {
	        		required: "This question is required, please enter the details",
	        		number: "Please enter a valid amount (Rs. in Lakhs)"
	        	},
	        	Six_12: {
	        		required: "This question is required, please enter the details",
	        		number: "Please enter a valid amount (Rs. in Lakhs)"
	        	},
	        	Six_13: {
	        		required: "This question is required, please enter the details",
	        		number: "Please enter a valid amount (Rs. in Lakhs)"
	        	},
	        	Six_14: {
	        		required: "This question is required, please enter the details",
	        		number: "Please enter a valid amount (Rs. in Lakhs)"
	        	},
	        	Seven_1: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Seven_2: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Seven_3: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Seven_4: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Seven_5: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Seven_6: {
	        		required: "This question is required, please enter the details",
	        		number: "Please enter a valid amount (Rs. in Lakhs)"
	        	},
	        	Seven_7: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Seven_8: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
	        	},
	        	Seven_9: {
	        		required: "This question is required, please enter the details",
	        		number: "Please enter a valid amount (Rs. in Lakhs)"
	        	},
        		Col4_SC: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col5_SC: {
        			required: "This question is required, please enter the details",
        			number: "Please enter a valid amount (Rs. in Lakhs)"
        		},
        		Col7_SC: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col8_SC: {
        			required: "This question is required, please enter the details",
        			number: "Please enter a valid amount (Rs. in Lakhs)"
        		},
        		Col4_ST: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col5_ST: {
        			required: "This question is required, please enter the details",
        			number: "Please enter a valid amount (Rs. in Lakhs)"
        		},
        		Col7_ST: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col8_ST: {
        			required: "This question is required, please enter the details",
        			number: "Please enter a valid amount (Rs. in Lakhs)"
        		},
        		Col4_Min: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col5_Min: {
        			required: "This question is required, please enter the details",
        			number: "Please enter a valid amount (Rs. in Lakhs)"
        		},
        		Col7_Min: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col8_Min: {
        			required: "This question is required, please enter the details",
        			number: "Please enter a valid amount (Rs. in Lakhs)"
        		},
        		Col4_Oth: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col5_Oth: {
        			required: "This question is required, please enter the details",
        			number: "Please enter a valid amount (Rs. in Lakhs)"
        		},
        		Col7_Oth: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col8_Oth: {
        			required: "This question is required, please enter the details",
        			number: "Please enter a valid amount (Rs. in Lakhs)"
        		},
        		Col4_PWD: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col5_PWD: {
        			required: "This question is required, please enter the details",
        			number: "Please enter a valid amount (Rs. in Lakhs)"
        		},
        		Col7_PWD: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col8_PWD: {
        			required: "This question is required, please enter the details",
        			number: "Please enter a valid amount (Rs. in Lakhs)"
        		},
	        },

            highlight: function(element, errorClass, validClass) {
                $(element)
                    .parent('div')
                    .parent('div')
                    .addClass("error");

            },
            unhighlight: function(element, errorClass, validClass) {
                $(element)
                    .parent('div')
                    .parent('div')
                    .removeClass("error");

            },
            errorElement: "span",
            errorClass: "help-inline"
	    }
	};
	
	var hrdetails_configs = {
			'entity_name' : 'hrdetails',
			'rest_api_url' : '/api/v1/HrDetails/',
			'dashboard_display' : {
	    		listing : true,
	    		add : true
	    	},
			'page_header': 'HR Detail',
			'list_table_header_template': 'hrdetails_table_template',
			'list_table_row_template': 'hrdetails_list_item_template',
	    	'add_template_name': 'hrdetails_add_edit_template',
	        'edit_template_name': 'hrdetails_add_edit_template',
	        'foreign_entities': {
	        	'state':{
	        		'state':{
	        			'placeholder': 'id_state',
	        			'name_field': 'state_name'
	        		},
	        	},
	        	'project':{
	        		'project':{
	        			'placeholder': 'id_project',
	        			'name_field': 'project_name'
	        		},
	        	},
	        },
	        'unique_together_fields': ['state.id', 'project.id', 'month','year'],
	        'sort_field': 'state',
	        'form_field_validation': {
	        	ignore: [],
	        	rules: {
	        		month: "required",
	        		year: {
	        			required:true,
	        			datecheck: {month : "month"}
	        		},
	        		state: "required",
	        		project: "required",
	        		Col2_smmu: {
	        			required: true,
	        			digits: true
	        		},
	        		Col3_smmu: {
	        			required: true,
	        			digits: true
	        		},
	        		Col4_smmu: {
	        			required: true,
	        			digits: true
	        		},
	        		Col5_smmu: {
	        			required: true,
	        			digits: true
	        		},
	        		Col6_smmu: {
	        			required: true,
	        			digits: true
	        		},
	        		Col7_smmu: {
	        			required: true,
	        			digits: true
	        		},
	        		Col8_smmu: {
	        			required: true,
	        			digits: true
	        		},
	        		Col9_smmu: {
	        			required: true,
	        			digits: true
	        		},
	        		Col2_dmmu: {
	        			required: true,
	        			digits: true
	        		},
	        		Col3_dmmu: {
	        			required: true,
	        			digits: true
	        		},
	        		Col4_dmmu: {
	        			required: true,
	        			digits: true
	        		},
	        		Col5_dmmu: {
	        			required: true,
	        			digits: true
	        		},
	        		Col6_dmmu: {
	        			required: true,
	        			digits: true
	        		},
	        		Col7_dmmu: {
	        			required: true,
	        			digits: true
	        		},
	        		Col8_dmmu: {
	        			required: true,
	        			digits: true
	        		},
	        		Col9_dmmu: {
	        			required: true,
	        			digits: true
	        		},
	        		Col2_bmmu: {
	        			required: true,
	        			digits: true
	        		},
	        		Col3_bmmu: {
	        			required: true,
	        			digits: true
	        		},
	        		Col4_bmmu: {
	        			required: true,
	        			digits: true
	        		},
	        		Col5_bmmu: {
	        			required: true,
	        			digits: true
	        		},
	        		Col6_bmmu: {
	        			required: true,
	        			digits: true
	        		},
	        		Col7_bmmu: {
	        			required: true,
	        			digits: true
	        		},
	        		Col8_bmmu: {
	        			required: true,
	        			digits: true
	        		},
	        		Col9_bmmu: {
	        			required: true,
	        			digits: true
	        		},
	        		Col2_bmmup: {
	        			required: true,
	        			digits: true
	        		},
	        		Col3_bmmup: {
	        			required: true,
	        			digits: true
	        		},
	        		Col4_bmmup: {
	        			required: true,
	        			digits: true
	        		},
	        		Col5_bmmup: {
	        			required: true,
	        			digits: true
	        		},
	        		Col6_bmmup: {
	        			required: true,
	        			digits: true
	        		},
	        		Col7_bmmup: {
	        			required: true,
	        			digits: true
	        		},
	        		Col8_bmmup: {
	        			required: true,
	        			digits: true
	        		},
	        		Col9_bmmup: {
	        			required: true,
	        			digits: true
	        		}
	        	},
	        messages: {
	        	month: "Please select the month for which data is being reported",
	        	year: {
	        		required: "Please select the year for which data is being reported",
	        		datecheck: "Please enter correct and valid date"
	        	},
	        	state: "Please select the state for which data is being reported",
	        	project: "Please select the project name for which data is being reported",
	        	Col2_smmu: {
	        		required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"
        		},
        		Col3_smmu: {
        			required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"        		
	        	},
        		Col4_smmu: {
        			required: "This question is required, please enter the details",
	        		digits: "Please enter only digits"        		
	        	},
				Col5_smmu: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col6_smmu: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col7_smmu: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col8_smmu: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col9_smmu: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col2_dmmu: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col3_dmmu: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col4_dmmu: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col5_dmmu: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col6_dmmu: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col7_dmmu: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col8_dmmu: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col9_dmmu: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col2_bmmu: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col3_bmmu: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col4_bmmu: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col5_bmmu: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col6_bmmu: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col7_bmmu: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col8_bmmu: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col9_bmmu: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col2_bmmup: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col3_bmmup: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col4_bmmup: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col5_bmmup: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col6_bmmup: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col7_bmmup: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col8_bmmup: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col9_bmmup: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		}
	        },

            highlight: function(element, errorClass, validClass) {
                $(element)
                    .parent('div')
                    .parent('div')
                    .addClass("error");

            },
            unhighlight: function(element, errorClass, validClass) {
                $(element)
                    .parent('div')
                    .parent('div')
                    .removeClass("error");

            },
            errorElement: "span",
            errorClass: "help-inline"
	    }
	};
	
	var financialassistance_configs = {
			'entity_name' : 'financialassistance',
			'rest_api_url' : '/api/v1/FinancialAssistance/',
			'dashboard_display' : {
	    		listing : true,
	    		add : true
	    	},
			'page_header': 'Fin Asst',
			'list_table_header_template': 'financialassistance_table_template',
			'list_table_row_template': 'financialassistance_list_item_template',
	    	'add_template_name': 'financialassistance_add_edit_template',
	        'edit_template_name': 'financialassistance_add_edit_template',
	        'foreign_entities': {
	        	'state':{
	        		'state':{
	        			'placeholder': 'id_state',
	        			'name_field': 'state_name'
	        		},
	        	},
	        	'project':{
	        		'project':{
	        			'placeholder': 'id_project',
	        			'name_field': 'project_name'
	        		},
	        	},
	        },
	        'unique_together_fields': ['state.id', 'project.id', 'month','year'],
	        'sort_field': 'state',
	        'form_field_validation': {
	        	ignore: [],
	        	rules: {
	        		month: "required",
	        		year: {
	        			required:true,
	        			datecheck: {month : "month"}
	        		},
	        		state: "required",
	        		project: "required",
	        		Col2_SC: {
	        			required: true,
	        			digits: true
	        		},
	        		Col3_SC: {
	        			required: true,
	        			digits: true
	        		},
	        		Col4_SC: {
	        			required: true,
	        			digits: true
	        		},
	        		Col5_SC: {
	        			required: true,
	        			number: true
	        		},
	        		Col6_SC: {
	        			required: true,
	        			digits: true
	        		},
	        		Col7_SC: {
	        			required: true,
	        			digits: true
	        		},
	        		Col8_SC: {
	        			required: true,
	        			number: true
	        		},
					Col2_ST: {
	        			required: true,
	        			digits: true
	        		},
	        		Col3_ST: {
	        			required: true,
	        			digits: true
	        		},
	        		Col4_ST: {
	        			required: true,
	        			digits: true
	        		},
	        		Col5_ST: {
	        			required: true,
	        			number: true
	        		},
	        		Col6_ST: {
	        			required: true,
	        			digits: true
	        		},
	        		Col7_ST: {
	        			required: true,
	        			digits: true
	        		},
	        		Col8_ST: {
	        			required: true,
	        			number: true
	        		},
					Col2_Min: {
	        			required: true,
	        			digits: true
	        		},
	        		Col3_Min: {
	        			required: true,
	        			digits: true
	        		},
	        		Col4_Min: {
	        			required: true,
	        			digits: true
	        		},
	        		Col5_Min: {
	        			required: true,
	        			number: true
	        		},
	        		Col6_Min: {
	        			required: true,
	        			digits: true
	        		},
	        		Col7_Min: {
	        			required: true,
	        			digits: true
	        		},
	        		Col8_Min: {
	        			required: true,
	        			number: true
	        		},
					Col2_Oth: {
	        			required: true,
	        			digits: true
	        		},
	        		Col3_Oth: {
	        			required: true,
	        			digits: true
	        		},
	        		Col4_Oth: {
	        			required: true,
	        			digits: true
	        		},
	        		Col5_Oth: {
	        			required: true,
	        			number: true
	        		},
	        		Col6_Oth: {
	        			required: true,
	        			digits: true
	        		},
	        		Col7_Oth: {
	        			required: true,
	        			digits: true
	        		},
	        		Col8_Oth: {
	        			required: true,
	        			number: true
	        		},
					Col2_PWD: {
	        			required: true,
	        			digits: true
	        		},
	        		Col3_PWD: {
	        			required: true,
	        			digits: true
	        		},
	        		Col4_PWD: {
	        			required: true,
	        			digits: true
	        		},
	        		Col5_PWD: {
	        			required: true,
	        			number: true
	        		},
	        		Col6_PWD: {
	        			required: true,
	        			digits: true
	        		},
	        		Col7_PWD: {
	        			required: true,
	        			digits: true
	        		},
	        		Col8_PWD: {
	        			required: true,
	        			number: true
	        		}
	        	},
	        	groups: {
	        		nrlm_date: "month year"
	        	},
	        messages: {
	        	nrlm_date: "",
	        	month: "Please select the month for which data is being reported",
	        	year: {
	        		required: "Please select the year for which data is being reported",
	        		datecheck: "Please enter correct and valid date"
	        	},
	        	state: "Please select the state for which data is being reported",
	        	project: "Please select the project name for which data is being reported",
				Col2_SC: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col3_SC: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col4_SC: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col5_SC: {
        			required: "This question is required, please enter the details",
        			number: "Please enter a valid amount (Rs. in Lakhs)"
        		},
        		Col6_SC: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col7_SC: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col8_SC: {
        			required: "This question is required, please enter the details",
        			number: "Please enter a valid amount (Rs. in Lakhs)"
        		},
				Col2_ST: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col3_ST: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col4_ST: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col5_ST: {
        			required: "This question is required, please enter the details",
        			number: "Please enter a valid amount (Rs. in Lakhs)"
        		},
        		Col6_ST: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col7_ST: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col8_ST: {
        			required: "This question is required, please enter the details",
        			number: "Please enter a valid amount (Rs. in Lakhs)"
        		},
				Col2_Min: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col3_Min: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col4_Min: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col5_Min: {
        			required: "This question is required, please enter the details",
        			number: "Please enter a valid amount (Rs. in Lakhs)"
        		},
        		Col6_Min: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col7_Min: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col8_Min: {
        			required: "This question is required, please enter the details",
        			number: "Please enter a valid amount (Rs. in Lakhs)"
        		},
				Col2_Oth: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col3_Oth: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col4_Oth: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col5_Oth: {
        			required: "This question is required, please enter the details",
        			number: "Please enter a valid amount (Rs. in Lakhs)"
        		},
        		Col6_Oth: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col7_Oth: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col8_Oth: {
        			required: "This question is required, please enter the details",
        			number: "Please enter a valid amount (Rs. in Lakhs)"
        		},
				Col2_PWD: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col3_PWD: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col4_PWD: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col5_PWD: {
        			required: "This question is required, please enter the details",
        			number: "Please enter a valid amount (Rs. in Lakhs)"
        		},
        		Col6_PWD: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col7_PWD: {
        			required: "This question is required, please enter the details",
        			digits: "Please enter only digits"
        		},
        		Col8_PWD: {
        			required: "This question is required, please enter the details",
        			number: "Please enter a valid amount (Rs. in Lakhs)"
        		}
	        },

            highlight: function(element, errorClass, validClass) {
                $(element)
                    .parent('div')
                    .parent('div')
                    .addClass("error");
            },
            unhighlight: function(element, errorClass, validClass) {
                $(element)
                    .parent('div')
                    .parent('div')
                    .removeClass("error");
            },
            errorElement: "span",
            errorClass: "help-inline"
	    }
	};
        var misc = {
        download_chunk_size: 2000,
        background_download_interval: 5 * 60 * 1000,
        inc_download_url: "/get_log/",
        afterFullDownload: function(start_time, download_status){
            return saveTimeTaken();
            function saveTimeTaken(){
                var record_endpoint = "/coco/record_full_download_time/"; 
                return $.post(record_endpoint, {
                    start_time : start_time,
                    end_time : new Date().toJSON().replace("Z", "")
                })    
            }
        },
        onLogin: function(Offline, Auth){
            getLastDownloadTimestamp()
                .done(function(timestamp){
                    askServer(timestamp);
                });
            var that = this;    
            function askServer(timestamp){
                $.get(that.reset_database_check_url,{
                    lastdownloadtimestamp: timestamp
                })
                    .done(function(resp){
                        if(resp=="1")
                            Offline.reset_database();
                    });
            }   
            function getLastDownloadTimestamp()
            {
                var dfd = new $.Deferred();
                Offline.fetch_object("meta_data", "key", "last_full_download_start")
                    .done(function(model){
                        dfd.resolve(model.get("timestamp"));
                    })
                    .fail(function(model, error){
                    
                    });
                return dfd;    
            } 
        },
        reset_database_check_url: '/coco/reset_database_check/',
    };

    return {
        state: state_configs,
        project: project_configs,
        progress: progress_configs,
        target: target_configs,
        //hrunit: hrunit_configs,
        hrdetails: hrdetails_configs,
        financialassistance: financialassistance_configs,
        progresstill13: progresstill13_configs,
        misc:misc
    }

});

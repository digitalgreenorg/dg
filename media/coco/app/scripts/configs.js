define([],
function() {
    var village_configs = {
        'page_header': 'Village',
        'table_template_name': 'village_table_template',
        'list_item_template_name': 'village_list_item_template',
        'rest_api_url': '/api/v1/village/',
        'entity_name': 'village'
    };
    // var video_list_view_configs = {
//         'page_header': 'Video',
//         'backbone_collection': video_collection.video_offline_collection,
//         'table_template_name': 'video_table_template',
//         'list_item_template_name': 'video_list_item_template'
//     };
    var group_configs = {
        'page_header': 'Group',
        'table_template_name': 'group_table_template',
        'list_item_template_name': 'group_list_item_template',
        'rest_api_url': '/api/v1/group/',
        'entity_name': 'group'
        
    };
//     var screening_list_view_configs = {
//         'page_header': 'Screening',
//         'backbone_collection': screening_collection.screening_offline_collection,
//         'table_template_name': 'screening_table_template',
//         'list_item_template_name': 'screening_list_item_template',
//     };

    var mediator_configs = {
        'page_header': 'Mediator',
        'table_template_name': 'mediator_table_template',
        'list_item_template_name': 'mediator_list_item_template',
        'add_edit_template_name': 'mediator_add_edit_template',
        'rest_api_url': '/api/v1/mediator/',
        'entity_name': 'mediator',
        'foreign_entities':{
            'village': {
                "assigned_villages" : {'placeholder':'id_ass_villages','name_field':'village_name'},        //name of html element in form/ attribute name in json: {placeholder: "id of html element in form", name_field: "attribute in foreign entity's json "} 
            }
         },
        'unique_togther_fields':[],
        'form_field_validation': {
        }
    };
  
    var person_configs = {
        'page_header': 'Person',
        'table_template_name': 'person_table_template',
        'list_item_template_name': 'person_list_item_template',
        'add_edit_template_name': 'person_add_edit_template2',
        'rest_api_url': '/api/v1/person/',
        'entity_name': 'person',
        'foreign_entities':{
            'village': {
                'village': {'placeholder':'id_village','name_field':'village_name'},
            },
            'group': {
                'group': {'placeholder':'id_group','name_field':'group_name'}
            }
         },
        'unique_togther_fields':[],
        'form_field_validation': {
			rules: {
				person_name: {
					required: true,
					minlength: 2,
					maxlength: 100,
                    // allowedChar:true
				},
				
				father_name: {
					required: true,
					minlength: 2,
					maxlength: 100,
                    // allowedChar:true
				},
				age: {
					digits: true,
					min:1,
					max:100
				},
				gender: "required",
				phone_no: {
					digits: true,
					maxlength: 10
				},
				village: {
					required: true
				}
			},
			messages: {
				person_name: {
					required: 'Enter group Name',
					minlength: 'Group Name  should be atleast 2 characters',
					maxlength: 'Group Name should be atmax 100 characters',
					allowedChar: 'Group name should only contain alphabets and local language characters'
				},
				father_name: {
					required: 'Father Name is required',
					minlength: "Father Name  should be atleast 2 characters",
					maxlength: 'Father Name should be atmax 100 characters',
					allowedChar: 'Father name should only contain alphabets and local language characters'
				},
				age: {
					digits: "Age should contain digits only",
					min:"Age should not be less than 1 year",
					max:"Age should not be more than 100 years"
				},
				phone_number_person: {
					digits: 'phone number should contain only digits',
					maxlength: "phone number should not contain more than 10 digits"
				},
				village: {
					required: "Please enter village"
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
    
    // var personadoptvideo_list_view_configs = {
    //     'page_header': 'Adoption',
    //     'backbone_collection': personadoptvideo_collection.personadoptvideo_offline_collection,
    //     'table_template_name': 'personadoptvideo_table_template',
    //     'list_item_template_name': 'personadoptvideo_list_item_template'
    // };
    // var animator_list_view_configs = {
    //     'page_header': 'Animator',
    //     'backbone_collection': animator_collection.animator_offline_collection,
    //     'table_template_name': 'animator_table_template',
    //     'list_item_template_name': 'animator_list_item_template'
    // };
    
    return {
        
        person:person_configs,
        village:village_configs,
        group:group_configs,
        mediator:mediator_configs    
    }

});

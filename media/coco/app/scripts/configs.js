define([],
function() {
    var village_configs = {
        'page_header': 'Village',
        'table_template_name': 'village_table_template',
        'list_item_template_name': 'village_list_item_template',
        'rest_api_url': '/api/v1/village/',
        'entity_name': 'village',
        'dashboard_display': {listing: false, add: false}
    };
    // var video_list_view_configs = {
//         'page_header': 'Video',
//         'backbone_collection': video_collection.video_offline_collection,
//         'table_template_name': 'video_table_template',
//         'list_item_template_name': 'video_list_item_template'
//     };
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
        'add_template_name': 'mediator_add_edit_template',
        'edit_template_name': 'mediator_add_edit_template',
        'rest_api_url': '/api/v1/mediator/',
        'entity_name': 'mediator',
        'unique_togther_fields':['name', 'gender'],
        'foreign_entities':{
            'village': {
                "assigned_villages" : {'placeholder':'id_ass_villages','name_field':'village_name'},        //name of html element in form/ attribute name in json: {placeholder: "id of html element in form", name_field: "attribute in foreign entity's json "} 
            }
         },
        'form_field_validation': {
            rules: {
                name: {
                    required: true,
                    minlength: 2,
                    maxlength: 100,
                    allowedChar: true
                },
                gender: "required",
                phone_no: {
                    digits: true,
                    maxlength: 10
                },
                assigned_villages: "required",
            },
            messages: {
                name: {
                    required: 'Enter Mediator Name',
                    minlength: 'Mediator Name  should be atleast 2 characters',
                    maxlength: 'Mediator Name should be atmax 100 characters',
                    allowedChar: 'Mediator name should only contain alphabets and local language characters'
                },
                gender: "Enter Gender",
                phone_no: {
                    digits: 'phone number should contain only digits',
                    maxlength: "phone number should not contain more than 10 digits"
                },
                assigned_villages: "Enter Assigned Villages",
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
  
    var video_configs = {
        'page_header': 'Video',
        'table_template_name': 'video_table_template',
        'list_item_template_name': 'video_list_item_template',
        'add_template_name': 'video_add_edit_template',
        'edit_template_name': 'video_add_edit_template',
        'rest_api_url': '/api/v1/video/',
        'entity_name': 'video',
        'unique_togther_fields':['title', 'video_production_start_date', 'video_production_end_date', 'village.id'],
        'foreign_entities':{
            'mediator': {
                "facilitator" : {'placeholder':'id_facilitator','name_field':'name'},        
                "cameraoperator" : {'placeholder':'id_cameraoperator','name_field':'name'},
            },
            'person': {
                "farmers_shown" : {'placeholder':'id_farmers_shown','name_field':'person_name'},
            },
            'village': {
                "village" : {'placeholder':'id_village','name_field':'village_name'},
            },
            'language': {
                "language": {'placeholder':'id_language','name_field':'language_name'}
            }                    
                                
                        
         },
        'form_field_validation': {
            rules: {
                title: {
                    required: true,
                    minlength: 2,
                    maxlength: 200,
                    // allowedChar: true
                },
                video_type: "required",
                video_production_start_date: {
                    required: true,
                    // validateDate: true
                },
                video_production_end_date: {
                    required: true,
                    // validateDate: true
                },
                language: "required",
                summary: {
                    minlength: 2,
                    maxlength: 500,
                    // allowedChar: true
                },
                village: "required",
                facilitator: "required",
                cameraoperator: "required",
                farmers_shown: "required",
                actors: "required",
                video_suitable_for: "required",
                approval_date: {
                    // validateDate: true
                },
                youtubeid: {
                    maxlength: 20
                }
            },
            messages: {
                title: {
                    required: 'Enter Video Title',
                    minlength: 'Video title should be atleast 2 characters',
                    maxlength: 'Video title should be atmax 200 characters',
                    // allowedChar: 'Video title should only contain alphabets and local language characters'
                },
                video_type: "Enter Video Type",
                video_production_start_date: {
                    required: 'Enter Video Production Start Date',
                    validateDate: "Enter Video Production Start Date in the form of yyyy-mm-dd"
                },
                video_production_end_date: {
                    required: 'Enter Video Production End Date',
                    validateDate: "Enter Video Production End Date in the form of yyyy-mm-dd"
                },
                language: "Enter Language",
                summary: {
                    minlength: "summary should be atleast 2 characters",
                    maxlength: "summary should be atmax 500 characters",
                    // allowedChar: "summary should not contain special characters"
                },
                village: "Enter Village",
                facilitator: "Enter Facilitator",
                cameraoperator: "Enter Camera Operator",
                farmers_shown: "Enter Persons Shown",
                actors: "Enter Actors",
                video_suitable_for: "Enter Video Suitable For",
                approval_date: {
                    validateDate: "Enter Approval Date in the form of yyyy-mm-dd"
                },
                youtubeid: {
                    maxlength: "youtubeid should be not more than 20 characters"
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
    
    var language_configs = {
        'page_header': 'Laguage',
        'table_template_name': 'language_table_template',
        'list_item_template_name': 'language_list_item_template',
        'add_template_name': 'language_add_edit_template',
        'edit_template_name': 'language_add_edit_template',
        'rest_api_url': '/api/v1/language/',
        'entity_name': 'language',
        'foreign_entities':{},
        'form_field_validation': {
        },
        'dashboard_display': {listing: false, add: false}
    };
  
  //name of html element in form/ attribute name in json: {placeholder: "id of html element in form", name_field: "attribute in foreign entity's json "}
    var group_configs = {
      'page_header': 'Group',
      'table_template_name': 'group_table_template',
      'list_item_template_name': 'group_list_item_template',
      'add_template_name': 'group_add_edit_template',
      'edit_template_name': 'group_add_edit_template',
      'rest_api_url': '/api/v1/group/',
      'entity_name': 'group',
      'inc_table_name': 'persongroups',
      'unique_togther_fields':['group_name', 'village.id'],
      'foreign_entities':{
          'village': {
              'village': {'placeholder':'id_village','name_field':'village_name'},
          },
      },
      'inline':{
          'entity': 'person', 'num_rows':10, "template": "person_inline", "foreign_attribute":{ 'host_attribute':["id","group_name"], 'inline_attribute': "group"}, "header" : "person_inline_header", 'borrow_attributes':[{'host_attribute':'village','inline_attribute':'village'}]
      },
      'form_field_validation': {
            rules: {
                group_name: {
                    required: true,
                minlength: 2,
                    maxlength: 100,
                    allowedChar: true
                },
                village: "required"
            },
            messages: {
                name: {
                    required: 'Enter group Name',
                    minlength: 'Group Name  should be atleast 2 characters',
                    maxlength: 'Group Name should be atmax 100 characters',
                    allowedChar: 'Group name should only contain alphabets and local language characters'
                },
                village: "Enter village"
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

    var screening_configs = {
      'page_header': 'Screening',
      'table_template_name': 'screening_table_template',
      'list_item_template_name': 'screening_list_item_template',
      'add_template_name': 'screening_add_edit_template',
      'edit_template_name': 'screening_add_edit_template',
      'rest_api_url': '/api/v1/screening/',
      'entity_name': 'screening',
      'unique_togther_fields':['date', 'start_time', 'end_time', 'village.id', 'animator.id'],
      'foreign_entities':{
          'village': {
              'village': {'placeholder':'id_village','name_field':'village_name'},
          },
          'video': {
              'videoes_screened': {'placeholder':'id_videoes_screened','name_field':'title'},
          },
          'mediator': {
              'animator': {
                  'placeholder':'id_animator',
                  'name_field':'name',
                  'dependency':[{
                      'source_entity': 'village',
                      'source_form_element': 'village',      
                      'dep_attr': 'assigned_villages'      
                  }]      
              }
          },
          'group': {
              farmer_groups_targeted:{
                  'placeholder':'id_group',
                  'name_field':'group_name',
                  'dependency':[{
                      'source_entity': 'village',
                      'source_form_element': 'village',      
                      'dep_attr': 'village'      
                  }]      
              }
          },
          'person': {
              person:{
                  'placeholder':'id_person',
                  'name_field':'person_name',
                  'dependency':[{
                      'source_entity': 'village',
                      'source_form_element': 'village',      
                      'dep_attr': 'village'      
                   }],
                   'filter':{attr:'group',value:null }
              },
              farmers_attendance: {
                   dependency: [
                        {
                           'source_entity': 'group',
                           'source_form_element': 'farmer_groups_targeted',      
                           'dep_attr': 'group'      
                        },
                        {
                             'source_entity': 'person',
                             'source_form_element': 'person',      
                             'dep_attr': 'id'      
                        }
                   ],
                  id_field : "person_id",                   // for offline_to_online conversion      
                  'expanded' : {                                // won't be denormalised, wud be converted offline to online, render wud use a template declared and nt options template, any field to be denormalised or converted offline to online can be declared - this shd be clubbed and put as foreign entity of expanded.  
                      template : 'person_pma_template',
                      placeholder : 'pmas',
                      denormalize: {                            // any field in expanded template to be denormalised     
                          "expressed_adoption_video" :{ 
                              name_field : 'title'
                          }
                      },
                      foreign_fields:{                          // any more field in expanded template for offline to online conv
                            "expressed_adoption_video" : {
                                entity_name: "video"
                            }  
                      },
                      extra_fields: ["expressed_question", "interested", "expressed_adoption_video"]                    
                  }          
              }
          }  
      },      
    };
    
    var adoption_configs = {
        'page_header': 'Adoption',
        'table_template_name': 'adoption_table_template',
        'list_item_template_name': 'adoption_list_item_template',
        'add_template_name': 'adoption_add_template',
        'edit_template_name': 'adoption_edit_template',
        'rest_api_url': '/api/v1/adoption/',
        'entity_name': 'adoption',
        'inc_table_name': 'personadoptpractice',
        'unique_togther_fields':['person.id', 'video.id', 'date_of_adoption'],    
          add: {
            'foreign_entities':{
                'village': {
                  'village': {'placeholder':'id_village','name_field':'village_name'},
                },
                'group': {
                  'group': {
                      'placeholder':'id_group',
                      'name_field':'group_name',
                      'dependency':[{
                          'source_entity': 'village',
                          'source_form_element': 'village',      
                          'dep_attr': 'village'      
                      }]   
                  }
                },
                'person': {
                    float_person:{
                        'placeholder':'id_person',
                        'name_field':'person_name',
                        'dependency':[{
                            'source_entity': 'village',
                            'source_form_element': 'village',      
                            'dep_attr': 'village'      
                         }],
                         'filter':{attr:'group',value:null }
                    },
                    farmers_attendance: {
                        only_render: true,
                        dependency: [
                             {
                                'source_entity': 'group',
                                'source_form_element': 'group',      
                                'dep_attr': 'group'      
                             },
                             {
                                  'source_entity': 'person',
                                  'source_form_element': 'float_person',      
                                  'dep_attr': 'id'      
                             }
                        ],
                        id_field : "person_id",                   // for offline_to_online conversion      
                        'expanded' : {                                // won't be denormalised, wud be converted offline to online, render wud use a template declared and nt options template, any field to be denormalised or converted offline to online can be declared - this shd be clubbed and put as foreign entity of expanded.  
                            template : 'adoption_inline',
                            placeholder : 'bulk',
                            denormalize: {                            // any field in expanded template to be denormalised     
                                "expressed_adoption_video" :{ 
                                    name_field : 'title'
                                }
                            },
                            foreign_fields:{                          // any more field in expanded template for offline to online conv
                                  "expressed_adoption_video" : {
                                      entity_name: "video"
                                  }  
                            },
                            extra_fields: ["expressed_question", "interested", "expressed_adoption_video"]                    
                        }          
                    }
                }    
            },
            // 'inline':{
//                 no_render : true, 'entity': 'adoption', 'num_rows':10, "template": "adoption_inline", "foreign_attribute":{ 'host_attribute':[], 'inline_attribute': null}, "header" : "adoption_inline_header", 'borrow_attributes':[]
//             }
            'bulk':{
                foreign_fields:{                          // any more field in expanded template for offline to online conv
                      "video" : {
                          video:{'name_field':'title'}
                      },
                      "person" : {
                          person:{'name_field':'person_name'}
                      }            
                },
            }        
          },
          edit:{
            'foreign_entities':{
                'person': {
                  'person': {'placeholder':'id_person','name_field':'person_name'},
                },
                'video': {
                    'video': {
                        'placeholder':'id_video',
                        // 'sub_attr': 'videos_seen',
                        'name_field':'title',
                        'dependency':[{
                            'source_entity': 'person',
                            'source_form_element': 'person',      
                            'dep_attr': 'id',
                            'rev_sub_attr': 'videos_seen',                
                        }]   
                    }      
                }      
            }
         }    
            
    };
  
    var person_configs = {
        'page_header': 'Person',
        'table_template_name': 'person_table_template',
        'list_item_template_name': 'person_list_item_template',
        'add_template_name': 'person_add_edit_template2',
        'edit_template_name': 'person_add_edit_template2',
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
        'unique_togther_fields':['person_name', 'father_name', 'village.id', 'group.id'],
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
					required: 'Enter person Name',
					minlength: 'Person Name  should be atleast 2 characters',
					maxlength: 'Person Name should be atmax 100 characters',
					allowedChar: 'Person name should only contain alphabets and local language characters'
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
    
    var misc = {
        download_size : 2000,
        background_download_interval:5*60*1000
    };
    
    return {
        village: village_configs,
        mediator: mediator_configs,
        video: video_configs,
        group: group_configs,
        person: person_configs,
        screening: screening_configs,
        adoption: adoption_configs,
        language: language_configs,
        misc: misc            
    }

});

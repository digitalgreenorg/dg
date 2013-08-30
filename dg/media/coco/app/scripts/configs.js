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

    var village_configs = {
        'page_header': 'Village',
        'list_table_header_template': 'village_table_template', 
        'list_table_row_template': 'village_list_item_template',
        'rest_api_url': '/coco/api/v1/village/',
        'entity_name': 'village',
        'dashboard_display': {
            listing: false,
            add: false
        },
        'sort_field': 'village_name'
    };

    var mediator_configs = {
        'page_header': 'Mediator',
        'list_table_header_template': 'mediator_table_template',
        'list_table_row_template': 'mediator_list_item_template',
        'add_template_name': 'mediator_add_edit_template',
        'edit_template_name': 'mediator_add_edit_template',
        'rest_api_url': '/coco/api/v1/mediator/',
        'entity_name': 'mediator',
        'unique_together_fields': ['name', 'gender', 'district.id'],
        'sort_field': 'name',
        'inc_table_name': 'animator',
        'foreign_entities': {
            'village': {
                "assigned_villages": {
                    'placeholder': 'id_ass_villages',
                    'name_field': 'village_name'
                }, //name of html element in form/ attribute name in json: {placeholder: "id of html element in form", name_field: "attribute in foreign entity's json "} 
            },
            district: {
                district :{
                    placeholder : 'id_district',
                    name_field : 'district_name' 
                }
            }
        },
        'form_field_validation': {
            ignore: [],
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
                district: "required"
            },
            messages: {
                name: {
                    required: 'Mediator name is required',
                    minlength: 'Mediator name should contain at least 2 characters',
                    maxlength: 'Mediator name should contain at most 100 characters',
                    allowedChar: 'Mediator name should contain only english and local language characters'
                },
                gender: "Gender is required",
                phone_no: {
                    digits: 'Phone number should contain only digits',
                    maxlength: "Phone number should not contain more than 10 digits"
                },
                assigned_villages: "Assigned villages are required",
                district: "District is required"
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
        'list_table_header_template': 'video_table_template',
        'list_table_row_template': 'video_list_item_template',
        'add_template_name': 'video_add_edit_template',
        'edit_template_name': 'video_add_edit_template',
        'rest_api_url': '/coco/api/v1/video/',
        'entity_name': 'video',
        'unique_together_fields': ['title', 'video_production_start_date', 'video_production_end_date', 'village.id'],
        'sort_field': 'title',
        'foreign_entities': {
            'mediator': {
                "facilitator": {
                    'placeholder': 'id_facilitator',
                    'name_field': 'name'
                },
                "cameraoperator": {
                    'placeholder': 'id_cameraoperator',
                    'name_field': 'name'
                },
            },
            'person': {
                "farmers_shown": {
                    'placeholder': 'id_farmers_shown',
                    'name_field': 'person_name',
                    'dependency': [{
                        'source_form_element': 'village',
                        'dep_attr': 'village'
                    }]
                },
            },
            'village': {
                "village": {
                    'placeholder': 'id_village',
                    'name_field': 'village_name'
                },
            },
            'language': {
                "language": {
                    'placeholder': 'id_language',
                    'name_field': 'language_name'
                }
            }


        },
        'form_field_validation': {
            ignore: [],
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
					dateOrder: {video_production_start_date : "video_production_start_date"}
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
					dateOrder: {video_production_start_date : "video_production_end_date"}
                    // validateDate: true
                },
                youtubeid: {
                    maxlength: 20
                }
            },
            messages: {
                title: {
                    required: 'Video title is required',
                    minlength: 'Video title should contain at least 2 characters',
                    maxlength: 'Video title should contain at most 200 characters',
                    // allowedChar: 'Video title should only contain alphabets and local language characters'
                },
                video_type: "Video type is required",
                video_production_start_date: {
                    required: 'Video production start date is required',
                    validateDate: "Enter video production start date in the form of YYYY-MM-DD"
                },
                video_production_end_date: {
                    required: 'Video production end date is required',
                    validateDate: "Enter video production end date in the form of YYYY-MM-DD",
					dateOrder: "End date should be later than start date"
                },
                language: "Language is required",
                summary: {
                    minlength: "Summary should contain at least 2 characters",
                    maxlength: "Summary should contain at most 500 characters",
                    // allowedChar: "summary should not contain special characters"
                },
                village: "Village is required",
                facilitator: "Facilitator is required",
                cameraoperator: "Camera operator is required",
                farmers_shown: "Persons shown are required",
                actors: "Actors are required",
                video_suitable_for: "Video suitable for is required",
                approval_date: {
                    validateDate: "Enter Approval Date in the form of YYYY-MM-DD",
					dateOrder: "Approval date should be later than end date"
                },
                youtubeid: {
                    maxlength: "YoutubeID should contain at most 20 characters"
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
        'rest_api_url': '/coco/api/v1/language/',
        'entity_name': 'language',
        'sort_field': 'language_name',
        'dashboard_display': {
            listing: false,
            add: false
        }
    };

    var district_configs = {
        'rest_api_url': '/coco/api/v1/district/',
        'entity_name': 'district',
        'sort_field': 'district_name',
        'dashboard_display': {
            listing: false,
            add: false
        }
    };

    var group_configs = {
        'page_header': 'Group',
        'list_table_header_template': 'group_table_template',
        'list_table_row_template': 'group_list_item_template',
        'add_template_name': 'group_add_edit_template',
        'edit_template_name': 'group_add_edit_template',
        'rest_api_url': '/coco/api/v1/group/',
        'entity_name': 'group',
        'inc_table_name': 'persongroups',
        'unique_together_fields': ['group_name', 'village.id'],
        'sort_field': 'group_name',
        'foreign_entities': {
            'village': {
                'village': {
                    'placeholder': 'id_village',
                    'name_field': 'village_name'
                },
            },
        },
        'inline': {
            'entity': 'person',
            'default_num_rows': 10,
            "template": "person_inline",
            "joining_attribute": {
                'host_attribute': ["id", "group_name"],
                'inline_attribute': "group"
            },
            "header": "person_inline_header",
            'borrow_attributes': [{
                'host_attribute': 'village',
                'inline_attribute': 'village'
            }],
            foreign_entities: { //used at convert_namespace, denormalize only
                village: {
                    village: {
                        placeholder: 'id_village',
                        name_field: 'village_name'
                    },
                },
                group: {
                    group: {
                        placeholder: 'id_group',
                        name_field: 'group_name'
                    }
                }
            }
        },
        'form_field_validation': {
            ignore: ".donotvalidate",
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
                    required: 'Group name is required',
                    minlength: 'Group name  should contain at least 2 characters',
                    maxlength: 'Group name should contain at most 100 characters',
                    allowedChar: 'Group name should contain only english and local language characters'
                },
                village: "Village is required"
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
            errorClass: "help-inline",
        }


    };

    var screening_configs = {
        'page_header': 'Screening',
        'list_table_header_template': 'screening_table_template',
        'list_table_row_template': 'screening_list_item_template',
        'add_template_name': 'screening_add_edit_template',
        'edit_template_name': 'screening_add_edit_template',
        'rest_api_url': '/coco/api/v1/screening/',
        'entity_name': 'screening',
        download_chunk_size: 1000,
        'unique_together_fields': ['date', 'start_time', 'end_time', 'village.id', 'animator.id'],
        afterSave: function(off_json, Offline){
            var dfd = new $.Deferred();
            var videos_shown = off_json.videoes_screened;
            console.log("recvd off_json in afterSave - "+JSON.stringify(off_json));
            update_attendees()
                .done(function(){
                    dfd.resolve();
                })
                .fail(function(){
                    dfd.reject();
                });
            return dfd.promise();

            function update_attendees(){
                var all_update_dfds = [];
                $.each(off_json.farmers_attendance, function(index, per){
                    all_update_dfds.push(update_attendee(per));    
                });
                return $.when.apply($,all_update_dfds);
            }
            
            function update_attendee(per){
                var p_dfd = new $.Deferred();
                Offline.fetch_object("person", "id", parseInt(per.person_id))
                    .done(function(p_model){
                        console.log("old p -"+JSON.stringify(p_model));
                        var videos_seen = p_model.get("videos_seen");
                        if(videos_seen)
                        {
                            var videos_seen_ids = _.pluck(videos_seen, 'id');
                            $.each(videos_shown, function(index, vid){
                                if($.inArray(vid.id, videos_seen_ids)==-1)
                                    videos_seen.push(vid);
                            });
                        }
                        else
                            videos_seen = videos_shown;
                        p_model.set("videos_seen", videos_seen);
                        Offline.save(p_model, "person", p_model.toJSON())
                            .done(function(p_model){
                                console.log("new p -"+JSON.stringify(p_model));
                                p_dfd.resolve();
                            })
                            .fail(function(error){
                                console.log("error updating person in after save - "+error);
                                p_dfd.reject(error);
                            });
                    })
                    .fail(function(error){
                        console.log("error fetching person in after save - "+error);
                        p_dfd.reject(error);
                    });
                return p_dfd;    
            };
        },
        'foreign_entities': {
            'village': {
                'village': {
                    'placeholder': 'id_village',
                    'name_field': 'village_name'
                },
            },
            'video': {
                'videoes_screened': {
                    'placeholder': 'id_videoes_screened',
                    'name_field': 'title'
                },
            },
            'mediator': {
                'animator': {
                    'placeholder': 'id_animator',
                    'name_field': 'name',
                    'dependency': [{
                        'source_form_element': 'village',
                        'dep_attr': 'assigned_villages'
                    }]
                }
            },
            'group': {
                farmer_groups_targeted: {
                    'placeholder': 'id_group',
                    'name_field': 'group_name',
                    'dependency': [{
                        'source_form_element': 'village',
                        'dep_attr': 'village'
                    }]
                }
            },
            'person': {
                person: {
                    'placeholder': 'id_person',
                    'name_field': 'person_name',
                    'dependency': [{
                        'source_form_element': 'village',
                        'dep_attr': 'village'
                    }],
                    'filter': {
                        attr: 'group',
                        value: null
                    }
                },
                farmers_attendance: {
                    dependency: [{
                        'source_form_element': 'farmer_groups_targeted',
                        'dep_attr': 'group'
                    }, {
                        'source_form_element': 'person',
                        'dep_attr': 'id'
                    }],
                    id_field: "person_id", // for convert_namespace conversion      
                    'expanded': { // won't be denormalised, wud be converted offline to online, render wud use a template declared and nt options template, any field to be denormalised or converted offline to online can be declared - this shd be clubbed and put as foreign entity of expanded.  
                        template: 'person_pma_template',
                        placeholder: 'pmas',
                        denormalize: { // any field in expanded template to be denormalised     
                            "expressed_adoption_video": {
                                name_field: 'title'
                            }
                        },
                        foreign_entities: { // any more field in expanded template for offline to online conv
                            video:{
                                "expressed_adoption_video": {
                                    entity_name: "video",
                                    name_field: 'title'
                                }
                            }
                        },
                        extra_fields: ["expressed_question", "interested", "expressed_adoption_video"]
                    }
                }
            }
        },
        'form_field_validation': {
            ignore: [],
            rules: {
                date: {
                    required: true,
                    validateDate: true
                },
                start_time: {
                    required: true,
                    validateTime: true
                },
                end_time: {
                    required: true,
                    validateTime: true,
					timeOrder: {start_time : "start_time"}
                },
                animator: "required",
                village: "required",
                videoes_screened: "required",

            },
            messages: {
				date: {
					required: 'Screening date is required',
					validateDate: 'Enter screening date in the form of YYYY-MM-DD',
				},
				start_time: {
					required: 'Screening start time is required',
					validateTime: 'Enter the start time in the form of HH:MM. Use 24 hour format',
				},
				end_time: {
					required: 'Screening end time is required',
					validateTime: 'Enter the end time in the form of HH:MM. Use 24 hour format',
					timeOrder: 'End time should be later than start time',
				},
				animator: "Mediator is required",
				village:"Village is required",
				videoes_screened:"Videos screened is required",
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

    var adoption_configs = {
        'page_header': 'Adoption',
        'list_table_header_template': 'adoption_table_template',
        'list_table_row_template': 'adoption_list_item_template',
        'add_template_name': 'adoption_add_template',
        'edit_template_name': 'adoption_edit_template',
        'rest_api_url': '/coco/api/v1/adoption/',
        'entity_name': 'adoption',
        'inc_table_name': 'personadoptpractice',
        'unique_together_fields': ['person.id', 'video.id', 'date_of_adoption'],
        form_field_validation: {
            ignore: [],
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
            errorClass: "help-block",
            display: "block"
        },
        add: {
            'foreign_entities': {
                'village': {
                    'village': {
                        'placeholder': 'id_village',
                        'name_field': 'village_name'
                    },
                },
                'group': {
                    'group': {
                        'placeholder': 'id_group',
                        'name_field': 'group_name',
                        'dependency': [{
                            'source_form_element': 'village',
                            'dep_attr': 'village'
                        }]
                    }
                },
                'person': {
                    float_person: {
                        'placeholder': 'id_person',
                        'name_field': 'person_name',
                        'dependency': [{
                            'source_form_element': 'village',
                            'dep_attr': 'village'
                        }],
                        'filter': {
                            attr: 'group',
                            value: null
                        }
                    },
                    farmers_attendance: {
                        dependency: [{
                            'source_form_element': 'group',
                            'dep_attr': 'group'
                        }, {
                            'source_form_element': 'float_person',
                            'dep_attr': 'id'
                        }],
                        id_field: "person_id", // for convert_namespace conversion      
                        'expanded': { // won't be denormalised, wud be converted offline to online, render wud use a template declared and nt options template, any field to be denormalised or converted offline to online can be declared - this shd be clubbed and put as foreign entity of expanded.  
                            template: 'adoption_inline',
                            placeholder: 'bulk'
                        }
                    }
                }
            },
            'bulk': {
                foreign_fields: { //foreign fields in the individual objects
                    "video": {
                        video: {
                            'name_field': 'title'
                        }
                    },
                    "person": {
                        person: {
                            'name_field': 'person_name'
                        }
                    },
                    village: {
                        village:{
                            'name_field': 'village_name'
                        }
                    },
                    group: {
                        group:{
                            'name_field': 'group_name'
                        }
                    }
                },
                borrow_fields: ['village', 'group']
            }
        },
        edit: {
            'foreign_entities': {
                'person': {
                    'person': {
                        'placeholder': 'id_person',
                        'name_field': 'person_name'
                    },
                },
                'video': {
                    'video': {
                        'placeholder': 'id_video',
                        // 'sub_attr': 'videos_seen',
                        'name_field': 'title',
                        'dependency': [{
                            'source_form_element': 'person',
                            'dep_attr': 'id',
                            'src_attr': 'videos_seen',
                        }]
                    }
                }
            }
        }

    };

    var person_configs = {
        'page_header': 'Person',
        'list_table_header_template': 'person_table_template',
        'list_table_row_template': 'person_list_item_template',
        'add_template_name': 'person_add_edit_template',
        'edit_template_name': 'person_add_edit_template',
        'rest_api_url': '/coco/api/v1/person/',
        'entity_name': 'person',
        'foreign_entities': {
            'village': {
                'village': {
                    'placeholder': 'id_village',
                    'name_field': 'village_name'
                },
            },
            'group': {
                'group': {
                    'placeholder': 'id_group',
                    'name_field': 'group_name',
					'dependency': [{
                        'source_form_element': 'village',
                        'dep_attr': 'village'
                    }]
                }
            }
        },
        'unique_together_fields': ['person_name', 'father_name', 'village.id'],
        'sort_field': 'person_name',
        'form_field_validation': {
            ignore: [],
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
                    min: 1,
                    max: 100
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
					required: 'Person name is required',
					minlength: 'Person name  should contain at least 2 characters',
					maxlength: 'Person Name should contain at most 100 characters',
					allowedChar: 'Person name should contain only english and local language characters'
				},
				father_name: {
					required: "Father's name is required",
					minlength: "Father's name should contain at least 2 characters",
					maxlength: "Father's name should contain at most 100 characters",
					allowedChar: "Father's name should contain only english and local language characters"
				},
				age: {
					digits: "Age should contain only digits",
					min:"Age should not be less than 1 year",
					max:"Age should not be more than 100 years"
				},
				gender:{
					required: "Gender is required"
				},
				phone_number_person: {
					digits: 'Phone number should contain digits only',
					maxlength: "Phone number should not contain more than 10 digits"
				},
				village: {
					required: "Village is required"
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
        reset_database_check_url: '/coco/reset_database_check/',
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
                        console.log(resp);
                        if(resp=="1")
                        {
                            alert("Your database will be redownloaded because of some changes in data.");
                            Offline.reset_database();
                        }
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
        }
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
        district: district_configs,
        misc: misc
    }

});

define([],
function() {
	var VideoContentApproval_configs = {
		'page_header': 'Video Content Approval',
        'config_English': 'Video Content Approval',
		'add_template_name': 'video_content_approval_add_edit_template',
        'edit_template_name': 'video_content_approval_add_edit_template',
        'rest_api_url': '/qacoco/api/v1/VideoContentApproval/',
        'labels_English': {add_row:"Add Empty Rows"},
        'list_elements_English': [{'header':'Video','element':'video.title'},{'header':'Reviewer','element':'qareviewername.name'}],
        'entity_name': 'VideoContentApproval',
        'inc_table_name': 'videocontentapproval',
        'dashboard_display': {
            listing: true,
            add: true
        },
    
        'foreign_entities':{
            'video':{
                "video":{
                    'placeholder': 'id_video',
                    'name_field': 'title'
                },
            },
            'qareviewername':{
            	"qareviewername":{
            		'placeholder': 'id_qareviewername',
            		'name_field': 'name'

            	},
            },
            'nonnegotiable': {
                "nonnegotiable":{
                        dependency: [{
                            'source_form_element': 'video',
                            'dep_attr': 'video'
                        }],
                        id_field: "id",
                        'expanded': { // won't be denormalised, wud be converted offline to online, render wud use a template declared and nt options template, any field to be denormalised or converted offline to online can be declared - this shd be clubbed and put as foreign entity of expanded.  
                            template: 'nn_template',
                            placeholder: 'nns_verification',
                            extra_fields: ["physically_verifiable"]
                        }
                }
            }     
        },

        'form_field_validation': {
            ignore: [],
            rules: {
                qareviewername: "required",
                video: "required"    
            },
            messages: {
                video: "Video name is required",
                qareviewername: "Reviewer name is required"      
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
            errorClass: "help-inline red-color",
            errorPlacement: function(label, element) {
                element.parent().append(label);
            }
        }
    };

    var VideoQualityReview_configs = {
        'page_header': 'Video Quality Review',
        'config_English': 'Video Quality Review',
        'add_template_name': 'Video_Quality_Review_add_edit_template',
        'edit_template_name': 'Video_Quality_Review_add_edit_template',
        'rest_api_url': '/qacoco/api/v1/VideoQualityReview/',
        'labels_English': {add_row:"Add Empty Rows"},
        'list_elements_English': [{'header':'Video','element':'video.title'},{'header':'Reviewer','element':'qareviewername.name'},{'header':'Total Score','element':'total_score'},{'header':'Video Grade','element':'video_grade'},{'header':'Approved for Dissemination','element':'approval'}],
        'entity_name': 'VideoQualityReview',
        'inc_table_name': 'videoqualityreview',
        'dashboard_display': {
            listing: true,
            add: true
        },
        
        'foreign_entities':{
            'video':{
                "video":{
                    'placeholder': 'id_video',
                    'name_field': 'title'
                },
            
            },
            'qareviewername':{
                "qareviewername":{
                    'placeholder': 'id_qareviewername',
                    'name_field': 'name'

                }
            }
        },
        'form_field_validation': {
            ignore: [],
            rules: {
                qareviewername: "required",
                video: "required",
                approval: "required"   
            },
            messages: {
                video: "Video name is required",
                qareviewername: "Reviewer name is required",
                approval: "Approval is required"      
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
            errorClass: "help-inline red-color",
            errorPlacement: function(label, element) {
                element.parent().append(label);
            }
        }
    };

    var DisseminationQuality_configs = {
        'page_header': 'Dissemination Quality',
        'config_English': 'Dissemination Quality',
        'add_template_name': 'Dissemination_Quality_add_edit_template',
        'edit_template_name': 'Dissemination_Quality_add_edit_template',
        'rest_api_url': '/qacoco/api/v1/DisseminationQuality/',
        'labels_English': {add_row:"Add Empty Rows"},
        'list_elements_English': [{'header':'Video','element':'video.title'},{'header':'Date','element':'date'}, {'header':'Total Score','element':'total_score'},{'header':'Dissemination Grade','element':'video_grade'}],
        'entity_name': 'DisseminationQuality',
        'inc_table_name': 'disseminationquality',
        'dashboard_display': {
            listing: true,
            add: true
        },
        
        'foreign_entities':{
            'video':{
                "video":{
                    'placeholder': 'id_video',
                    'name_field': 'title'
                },
            },
            'village':{
                "village":{
                    'placeholder': 'id_village',
                    'name_field': 'village_name',
                    'dependency': [{
                        'source_form_element': 'block',
                        'dep_attr': 'block'
                    }]
                }
            },
            'mediator':{
                "mediator":{
                    'placeholder': 'id_mediator',
                    'name_field': 'name',
                    'dependency': [{
                        'source_form_element': 'village',
                        'dep_attr': 'assigned_villages'
                    }]
                }
            },
            'block':{
                "block":{
                'placeholder' : 'id_block',
                'name_field' : 'block_name'
                },
            },
            'qareviewername':{
                "qareviewername":{
                    'placeholder': 'id_qareviewername',
                    'name_field': 'name'

                }
            }
    },
    'form_field_validation': {
            ignore: [],
            rules: {
                block: "required",
                village: "required",
                mediator: "required",
                qareviewername: "required",
                date: "required",
                video: "required"    
            },
            messages: {
                video: "Video name is required",
                block: "Block name is required",
                village: "Village name is required",
                mediator: "Mediator name is required",
                date: "Date is required",
                qareviewername: "Reviewer name is required"      
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
            errorClass: "help-inline red-color",
            errorPlacement: function(label, element) {
                element.parent().append(label);
            }
        }
    };

    var AdoptionVerification_configs = {
        'page_header': 'Adoption Verification',
        'config_English': 'Adoption Verification',
        'add_template_name': 'Adoption_Verification_add_edit_template',
        'edit_template_name': 'Adoption_Verification_add_edit_template',
        'rest_api_url': '/qacoco/api/v1/AdoptionVerification/',
        'labels_English': {add_row:"Add Empty Rows"},
        'list_elements_English': [{'header':'Person','element':'person.person_name'},{'header':'Reviewer','element':'qareviewername.name'},{'header':'Video','element':'video.title'},{'header':'Village','element':'village.village_name'},{'header':'Block','element':'block.block_name'}],
        'entity_name': 'AdoptionVerification',
        'inc_table_name': 'adoptionverification',
        'dashboard_display': {
            listing: true,
            add: true
        },
        
        'foreign_entities':{
            'video':{
                "video":{
                'placeholder' : 'id_video',
                'name_field' : 'title'
                },
            },

            'block':{
                "block":{
                    'placeholder': 'id_block',
                    'name_field': 'block_name'
                },
            },
            'village':{
                "village":{
                    'placeholder': 'id_village',
                    'name_field': 'village_name',
                    'dependency': [{
                        'source_form_element': 'block',
                        'dep_attr': 'block'
                    }]
                },
            },
            'mediator':{
                "mediator":{
                    'placeholder': 'id_mediator',
                    'name_field': 'name',
                    'dependency': [{
                        'source_form_element': 'village',
                        'dep_attr': 'assigned_villages'
                    }]
                },
            },
            'group':{
                "group":{
                    'placeholder': 'id_group',
                    'name_field': 'group_name',
                    'dependency': [{
                        'source_form_element': 'village',
                        'dep_attr': 'village'
                    }]
                },
            },
            'person':{
                "person":{
                    'placeholder': 'id_person',
                    'name_field': 'person_name',
                    'dependency': [{
                        'source_form_element': 'village',
                        'dep_attr': 'village'
                    }]
                },
            },
            'qareviewername':{
                "qareviewername":{
                    'placeholder': 'id_qareviewername',
                    'name_field': 'name'

                },
            },
            'nonnegotiable': {
                "nonnegotiable":{
                        dependency: [{
                            'source_form_element': 'video',
                            'dep_attr': 'video'
                        }],
                        id_field: "nonnegotiable_id",
                        'expanded': { // won't be denormalised, wud be converted offline to online, render wud use a template declared and nt options template, any field to be denormalised or converted offline to online can be declared - this shd be clubbed and put as foreign entity of expanded.  
                            template: 'nn_verification_template',
                            placeholder: 'nns_verification',
                            extra_fields: ["physically_verifiable","adopted"]
                        }
                }
            }            
    },
    'form_field_validation': {
            ignore: [],
            rules: {
                qareviewername: "required",
                block: "required",
                village: "required",
                mediator: "required",
                group: "required",
                person: "required",
                verification_date: "required",
                video: "required"    
            },
            messages: {
                video: "Video name is required",
                qareviewername: "Reviewer name is required",
                block: "Block name is required",
                village: "Village name is required",
                group: "Group name is required",
                person: "Person name is required",
                mediator: "Mediator name is required",
                verification_date: "Adoption Verification date is required"     
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
            errorClass: "help-inline red-color",
            errorPlacement: function(label, element) {
                element.parent().append(label);
            }
        }
    };
	var video_configs = {
        'config_English': 'Videos',
        'labels_English': {add_row:"Add Empty Rows"},
        'rest_api_url': '/qacoco/api/v1/video/',
        'entity_name': 'video',
        'sort_field': 'title',
        'dashboard_display': {
            listing: false,
            add: false
        }
    };
    var group_configs = {
        'config_English': 'Groups',
        'labels_English': {add_row:"Add Empty Rows"},
        'rest_api_url': '/qacoco/api/v1/group/',
        'entity_name': 'group',
        'sort_field': 'group_name',
        'dashboard_display': {
            listing: false,
            add: false
        }
    };
    var person_configs = {
        'config_English': 'Persons',
        'labels_English': {add_row:"Add Empty Rows"},
        'rest_api_url': '/qacoco/api/v1/person/',
        'entity_name': 'person',
        'sort_field': 'person_name',
        'dashboard_display': {
            listing: false,
            add: false
        }
    };
    var nonnegotiable_configs = {
        'config_English': 'Non Negotiables',
        'labels_English': {add_row:"Add Empty Rows"},
        'rest_api_url': '/qacoco/api/v1/nonnegotiable/',
        'entity_name': 'nonnegotiable',
        'sort_field': 'non_negotiable',
        'foreign_entities': {
                'video': {
                    'video': {
                        'placeholder': 'id_video',
                        'name_field': 'title'
                    }
                }
            },
        'dashboard_display': {
            listing: false,
            add: false
        }
    };

    var mediator_configs = {
        'config_English': 'Mediators',
        'labels_English': {add_row:"Add Empty Rows"},
        'rest_api_url': '/qacoco/api/v1/mediator/',
        'entity_name': 'mediator',
        'sort_field': 'name',
        'dashboard_display': {
            listing: false,
            add: false
        }
    };
    
    var block_configs = {
        'config_English': 'Blocks',
        'labels_English': {add_row:"Add Empty Rows"},
        'rest_api_url': '/qacoco/api/v1/block/',
        'entity_name': 'block',
        'sort_field': 'block_name',
        'dashboard_display': {
            listing: false,
            add: false
        }
    };
    
    var village_configs = {
        'config_English': 'Villages',
        'labels_English': {add_row:"Add Empty Rows"},
        'rest_api_url': '/qacoco/api/v1/village/',
        'entity_name': 'village',
        'sort_field': 'village_name',
        'dashboard_display': {
            listing: false,
            add: false
        }
    };

    var qareviewername_configs = {
        'config_English': 'QA Reviewer Name',
        'labels_English': {add_row:"Add Empty Rows"},
        'rest_api_url': '/qacoco/api/v1/qareviewername/',
        'entity_name': 'qareviewername',
        'sort_field': 'name',
        'dashboard_display': {
            listing: false,
            add: false
        }
    };

    var misc = {
        download_chunk_size: 2000,
        languages: ['English'],
        meta_default: 'English',
        meta_English: {stop: "Stop",close:"close", sync: "Sync", save: "Save and Add Another", help:"Help", logout:"Logout", download:"Downloading...",upload:"Uploading...", inprogress:"In Progress", done:"Done", edit:"Edit", 
                       delete_download:"Delete and Download Database", save_again:"Save Again", discard:"Discard", upload_total:"Data items to be uploaded", upload_done:"Data Uploaded", upload_pending:"Data pending to be uploaded",
                       error:"Error!!", upload_error:"Internet connectivity lost. Please try after sometime!", copy_clipboard:"Copy to clipboard", excel_download:"Download in excel", search: 'Search: ', enteries:"Enteries: ",total_enteries:"Total Enteries: ",
                       next:"Next", previous:"Previous", list_page_help:"For multiple column sorting, press and hold the shift key while sorting each column.",
                       line_1:"Welcome to QACOCO", line_2:"COCO helps you to seamlessly enter data in conditions of intermittent connectivity.",
                       line_3:"Add data", line_4:"To add some data, click on (+) sign next to the type of data that you want to add.",
                       line_5:"View Data", line_6:"To view, sort and search through your data, click on the data link in the sidebar.",
                       line_7:"Sync data", line_8:"To sync data with the server, click on the sync button. While syncing, if some data is rejected by the server, you will get the opportunity to correct the data, or in case of duplicate entries, to discard it. The number in the button shows how many entries are yet to be uploaded. Clicking on the sync button will also download the database if it is not completely downloaded.",
                       line_9:"We value your feedback", line_10:"Do share your feedback by mailing us at <a href='mailto:system@digitalgreen.org'>system@digitalgreen.org</a>",
                       line_11:"Database last deleted and downloaded at", line_12:"Database last synced at",
                       line_13:"Entries to upload"},
        background_download_interval: 5 * 60 * 1000,
        inc_download_url: "/qa_get_log/",
        afterFullDownload: function(start_time, download_status){
            return saveTimeTaken();
            function saveTimeTaken(){
                var record_endpoint = "/qacoco/record_full_download_time/"; 
                return $.post(record_endpoint, {
                    start_time : start_time,
                    end_time : new Date().toJSON().replace("Z", "")
                })    
            }
        },
        reset_database_check_url: '/qacoco/reset_database_check/',
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
        VideoContentApproval : VideoContentApproval_configs,
        VideoQualityReview   : VideoQualityReview_configs,
        DisseminationQuality : DisseminationQuality_configs,
        AdoptionVerification : AdoptionVerification_configs,
        video : video_configs,
        block : block_configs,
        village : village_configs,
        mediator: mediator_configs,
        group : group_configs,
        person : person_configs,
        qareviewername: qareviewername_configs,
        nonnegotiable: nonnegotiable_configs,
        misc: misc
    }

});
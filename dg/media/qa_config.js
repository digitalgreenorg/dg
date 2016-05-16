define([],
function() {
	var VideoContentApproval_configs = {
		'page_header': 'Video Content Approval',
		'add_template_name': 'video_content_approval_add_edit_template',
        'edit_template_name': 'video_content_approval_add_edit_template',
        'rest_api_url': '/qacoco/api/v1/VideoContentApproval/',
        'list_elements': [{'header':'Video','element':'video.title'},{'header':'Reviewer','element':'reviewer'}],
        'entity_name': 'VideoContentApproval',
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
            'qareviewer':{
            	"qareviewer":{
            		'placeholder': 'id_qareviewer',
            		'name_field': 'reviewer_name',

            		},
            	},
        },

        'form_field_validation': {
            ignore: [],
            rules: {
                qareviewer: "required",
                category: "required",
                sub_category: "required",
                video: "required"    
            },
            messages: {
                video: "Video name is required",
                qareviewer: "Reviewer name is required",
                category: "Category is required",
                sub_category: "Sub Category is required"      
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
        'rest_api_url': '/qacoco/api/v1/video/',
        'entity_name': 'video',
        'sort_field': 'title',
        'dashboard_display': {
            listing: false,
            add: false
        }
    };
    
    var block_configs = {
        'rest_api_url': '/qacoco/api/v1/block/',
        'entity_name': 'block',
        'sort_field': 'block_name',
        'dashboard_display': {
            listing: false,
            add: false
        }
    };
    var village_configs = {
        'rest_api_url': '/qacoco/api/v1/village/',
        'entity_name': 'village',
        'sort_field': 'village_name',
        'dashboard_display': {
            listing: false,
            add: false
        }
    };

    var qareviewer_configs = {
        'rest_api_url': '/qacoco/api/v1/qareviewer/',
        'entity_name': 'qareviewer',
        'sort_field': 'reviewer_name',
        'dashboard_display': {
            listing: false,
            add: false
        }
    };

    var misc = {
        download_chunk_size: 2000,
        background_download_interval: 5 * 60 * 1000,
        inc_download_url: "/get_log/",
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
        video : video_configs,
        block : block_configs,
        village : village_configs,
        qareviewer: qareviewer_configs,
        misc: misc
    }

});
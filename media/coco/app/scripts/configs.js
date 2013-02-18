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

    var person_configs = {
        'page_header': 'Person',
        'table_template_name': 'person_table_template',
        'list_item_template_name': 'person_list_item_template',
        'add_edit_template_name': 'person_add_edit_template',
        'rest_api_url': '/api/v1/person/',
        'entity_name': 'person',
        'foreign_entities':{
            'village': {'placeholder':'id_village','name_field':'village_name'},
            'group': {'placeholder':'id_group','name_field':'group_name'}
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
        group:group_configs
    }

});

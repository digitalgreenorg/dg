define(['collections/person_collection', 'collections/animator_collection', 
'collections/personadoptvideo_collection', 'collections/persongroup_collection', 
'collections/screening_collection', 'collections/video_collection', 'collections/village_collection'],

function(person_collection, animator_collection, personadoptvideo_collection, persongroup_collection,
screening_collection, video_collection, village_collection) {
    var village_list_view_configs = {
        'page_header': 'Village',
        'backbone_collection': village_collection.village_offline_collection,
        'table_template_name': 'village_table_template',
        'list_item_template_name': 'village_list_item_template',
    };
    var video_list_view_configs = {
        'page_header': 'Video',
        'backbone_collection': video_collection.video_offline_collection,
        'table_template_name': 'video_table_template',
        'list_item_template_name': 'video_list_item_template'
    };
    var persongroup_list_view_configs = {
        'page_header': 'Group',
        'backbone_collection': persongroup_collection.persongroup_offline_collection,
        'table_template_name': 'persongroup_table_template',
        'list_item_template_name': 'persongroup_list_item_template'
    };
    var screening_list_view_configs = {
        'page_header': 'Screening',
        'backbone_collection': screening_collection.screening_offline_collection,
        'table_template_name': 'screening_table_template',
        'list_item_template_name': 'screening_list_item_template',
    };
    var person_list_view_configs = {
        'page_header': 'Person',
        'backbone_collection': person_collection.person_offline_collection,
        'table_template_name': 'person_table_template',
        'list_item_template_name': 'person_list_item_template',
        'add_edit_template_name': 'person_add_edit_template'
    };
    var personadoptvideo_list_view_configs = {
        'page_header': 'Adoption',
        'backbone_collection': personadoptvideo_collection.personadoptvideo_offline_collection,
        'table_template_name': 'personadoptvideo_table_template',
        'list_item_template_name': 'personadoptvideo_list_item_template'
    };
    var animator_list_view_configs = {
        'page_header': 'Animator',
        'backbone_collection': animator_collection.animator_offline_collection,
        'table_template_name': 'animator_table_template',
        'list_item_template_name': 'animator_list_item_template'
    };
    
    return {
        
        person_list_view_configs:person_list_view_configs,
        village_list_view_configs:village_list_view_configs
    }

});

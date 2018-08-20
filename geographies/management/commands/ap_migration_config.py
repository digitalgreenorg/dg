migration_config = {
    'District' : {
        'field': 'district_id',
        'foreign_key_models' : [
            {'app_label': 'geographies', 'model': 'block'}, 
            {'app_label': 'people', 'model': 'animator'},
            {'app_label': 'training', 'model': 'training'}
        ],
    },

    'Block' : {
        'field': 'block_id',
        'foreign_key_models' : [
            {'app_label': 'geographies', 'model': 'village'}
        ]
    },

    'Village': {
        'field': 'village_id',
        'foreign_key_models' :[
            {'app_label': 'activities', 'model': 'screening'},
            {'app_label': 'videos', 'model': 'video'},
            {'app_label': 'people', 'model': 'person'}
        ], 
        'm2m_models' : [
            {'model': 'cocouser', 'field': 'villages', 'app_label': 'coco', 'm2m_table': 'coco_cocouser_villages'},
            {'model': 'animator', 'field': 'assigned_villages', 'app_label': 'people', 'm2m_table' : 'people_animatorassignedvillage'}
        ],
    }
}
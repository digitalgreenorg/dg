from dg.settings import MEDIA_ROOT

models = {

	# 'Gaddidar': {'display_value': 'Gaddidar', 'col_name': 'id', 'dependencies': {'GaddidarCommission': 'gaddidar_id', 'GaddidarShareOutliers': 'gaddidar_id', 'CombinedTransaction': 'gaddidar_id'}},
	# 'LoopUser': {'display_value': 'Aggregator', 'col_name': 'user_id', 'dependencies': {'GaddidarCommission': 'gaddidar_id', 'GaddidarShareOutliers': 'gaddidar_id'}},
	'Farmer': {'display_value': 'Farmer', 
				'col_name': 'id', 
				'dependencies': {'CombinedTransaction': {'app': 'loop',
														'column': 'farmer_id'}, 
								'BroadcastAudience': {'app': 'loop',
													'column': 'farmer_id'}
								}
			  },
	'Crop': {'display_value': 'Crop', 
				'col_name': 'id', 
				'dependencies': {'CombinedTransaction': {'app': 'loop',
														'column': 'crop_id'}, 
								'PriceInfoLog': {'app': 'loop_ivr',
												'column': 'crop_id'}
								}
			}

}

MERGE_LOG_FILE = '%s/loop/merge_log.log'%(MEDIA_ROOT,)

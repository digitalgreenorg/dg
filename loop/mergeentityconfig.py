models = {

	'Gaddidar': {'display_value': 'Gaddidar', 'col_name': 'id', 'dependencies': {'GaddidarCommission': 'gaddidar_id', 'GaddidarShareOutliers': 'gaddidar_id', 'CombinedTransaction': 'gaddidar_id'}},
	'LoopUser': {'display_value': 'Aggregator', 'col_name': 'user_id', 'dependencies': {'GaddidarCommission': 'gaddidar_id', 'GaddidarShareOutliers': 'gaddidar_id'}},
	'Farmer': {'display_value': 'Farmer', 'col_name': 'id', 'dependencies': {'CombinedTransaction': 'farmer_id', 'BroadcastAudience': 'farmer_id'}}

}
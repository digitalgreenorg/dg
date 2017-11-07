import pandas as pd
import numpy as np
import Tables
import Crop_Outliers

daily_aggregator_market_crop_rate_query_result = Tables.daily_aggregator_market_crop_rate_query_result
remove_crop_outliers = Crop_Outliers.remove_crop_outliers

ct_data_filtered = remove_crop_outliers(ct_data=daily_aggregator_market_crop_rate_query_result, state_id=1, rate_deviation_threshold=15, deviation_factor_threshold=0.3, quantity_rate_deviation_threshold=5)

print ct_data_filtered.head()

# # deviation_2.to_csv('Crop Rate Deviation 3.csv', index= False)
# # outlier_ct_data_2.to_csv('Crop Rate Deviation 4.csv', index= False)
#
# # print combined_transactions_data.count(axis=1)
# #
# # combined_transactions_data.to_csv('Filtered CT Data.csv', index= False)
# # outlier_ct_data.to_csv('Crop Rate Deviation 2.csv', index= False)
# # #
# # print standard_deviation.head()

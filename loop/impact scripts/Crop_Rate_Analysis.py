import pandas as pd
import numpy as np
import Tables
import Crop_Outliers

daily_aggregator_market_crop_rate_query_result = Tables.daily_aggregator_market_crop_rate_query_result
remove_crop_outliers = Crop_Outliers.remove_crop_outliers

ct_data_filtered = remove_crop_outliers(ct_data=daily_aggregator_market_crop_rate_query_result, state_id=1, rate_deviation_threshold=12, deviation_factor_threshold=0.3, quantity_rate_deviation_threshold=5)

print ct_data_filtered.head()

average_rate = ct_data_filtered.groupby(['Date', 'Market Real', 'Crop']).agg(
    {'Quantity Real': ['sum'], 'Amount': ['sum']}).reset_index()
average_rate.columns = average_rate.columns.droplevel(1)
average_rate = average_rate.rename(
    columns={'Quantity Real': 'Total Quantity', 'Amount': 'Total Amount'})
average_rate['Av Rate'] = average_rate['Total Amount'] / average_rate['Total Quantity']


ct_data_filtered = ct_data_filtered.merge(average_rate, on=['Date', 'Market Real', 'Crop'])
ct_data_filtered['Deviation'] = (
    np.square(ct_data_filtered['Price'] - ct_data_filtered['Av Rate']) *
    ct_data_filtered['Quantity Real'])

# Deviation_quantity_rate has weighted standard deviation as it considers each kg of crop as a separate point.
# Mean of Total Quantity and Av Rate will be Total Quantity and Av Rate as it is uniform in the group.
deviation_quantity_rate = ct_data_filtered.groupby(['Date', 'Market Real', 'Crop']).agg(
    {'Deviation': ['sum'], 'Total Quantity': ['mean'], 'Av Rate': ['mean']}).reset_index()
deviation_quantity_rate.columns = deviation_quantity_rate.columns.droplevel(1)
deviation_quantity_rate['std'] = np.sqrt(deviation_quantity_rate['Deviation'] / deviation_quantity_rate['Total Quantity'])
deviation_quantity_rate = deviation_quantity_rate.sort_values(by='std', ascending=False)

deviation_quantity_rate.to_csv('CT Filtered Data.csv', index= False)


# # deviation_2.to_csv('Crop Rate Deviation 3.csv', index= False)
# # outlier_ct_data_2.to_csv('Crop Rate Deviation 4.csv', index= False)
#
# # print ct_data_filtered.count(axis=1)
# #
# # ct_data_filtered.to_csv('Filtered CT Data.csv', index= False)
# # outlier_ct_data.to_csv('Crop Rate Deviation 2.csv', index= False)
# # #
# # print standard_deviation.head()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# The entire function could be divided into smaller functions but that could be done later.
def remove_crop_outliers(ct_data=None, state_id=1, rate_deviation_threshold=15, deviation_factor_threshold=0.3, quantity_rate_deviation_threshold=5):
    # Converts SQL query output in a dataframe
    daily_aggregator_market_crop_rate_query_result = list(ct_data)
    columnlist_ct = ['Date', 'Aggregator', 'Market Real', 'Crop', 'Quantity Real', 'Price', 'Amount', 'State']
    combined_transactions_data = pd.DataFrame(daily_aggregator_market_crop_rate_query_result, columns=columnlist_ct)

    # Filters out data of other states
    combined_transactions_data = combined_transactions_data[combined_transactions_data['State'] == state_id]

    # combined_transactions_data = combined_transactions_data[(combined_transactions_data['Crop']==2)]
    combined_transactions_data.to_csv('before_outliers_removal.csv') #Recording data in CSV file
    combined_transactions_data['datetime'] = combined_transactions_data['Date'].astype('datetime64[ns]')
    combined_transactions_data['datetime'] = combined_transactions_data['datetime'].astype('int64')
    combined_transactions_data.plot(use_index=False,kind='scatter',x='datetime',y='Price',figsize=(18,8))
    # plt.show()


    # Check whether amount is always equal to quantity*rate or not.
    # ct_data_filtered['Amount'] = ct_data_filtered['Quantity Real'] * ct_data_filtered[
    #     'Price']

    # Finds deviation for date-market-crop combination without giving any weight to quantity
    deviation_rate = combined_transactions_data.groupby(['Date', 'Market Real', 'Crop']).agg(
        {'Price': ['std', 'mean']}).reset_index()

    # There could be a better way of renaming columns in pandas.
    deviation_rate.columns = deviation_rate.columns.map('_'.join)
    deviation_rate = deviation_rate.rename(columns={'Date_': 'Date', 'Market Real_': 'Market Real', 'Crop_': 'Crop'})
    deviation_rate = deviation_rate.sort_values(by='Price_std', ascending=False)

    # Identifying all rows in ct where deviation from mean is greater than standard deviation and where standard
    # deviation is above the minimum threshold.
    deviation_rate = deviation_rate[deviation_rate['Price_std'] > rate_deviation_threshold]
    outlier_ct_data = pd.merge(combined_transactions_data, deviation_rate, how='inner',
                               on=['Date', 'Market Real', 'Crop'])
    outlier_ct_data['Mean-Deviation'] = outlier_ct_data['Price_mean'] - outlier_ct_data['Price']
    outlier_ct_data = outlier_ct_data[abs(outlier_ct_data['Mean-Deviation']) > outlier_ct_data['Price_std']]

    outlier_ct_data.to_csv('outliers.csv') #Recording outliers in a CSV file

    # print outlier_ct_data.count()
    # print outlier_ct_data

    # Removing these identified outliers from ct_data_filtered.
    outlier_merged = outlier_ct_data.merge(combined_transactions_data, on=columnlist_ct).loc[:, 'Date': 'State']
    combined_transactions_data = combined_transactions_data[~combined_transactions_data.isin(outlier_merged)].dropna()

    # First level of outlier removal is over. Now, we will find deviation for date-market-combination by giving
    # weights to volume too.

    # To compute deviation, we first find average rate for each day-market-crop combination
    average_rate = combined_transactions_data.groupby(['Date', 'Market Real', 'Crop']).agg(
        {'Quantity Real': ['sum'], 'Amount': ['sum']}).reset_index()
    average_rate.columns = average_rate.columns.droplevel(1)
    average_rate = average_rate.rename(
        columns={'Quantity Real': 'Total Quantity', 'Amount': 'Total Amount'})
    average_rate['Av Rate'] = average_rate['Total Amount'] / average_rate['Total Quantity']


    combined_transactions_data = combined_transactions_data.merge(average_rate, on=['Date', 'Market Real', 'Crop'])
    combined_transactions_data['Deviation'] = (
    np.square(combined_transactions_data['Price'] - combined_transactions_data['Av Rate']) *
    combined_transactions_data['Quantity Real'])

    # Deviation_quantity_rate has weighted standard deviation as it considers each kg of crop as a separate point.
    # Mean of Total Quantity and Av Rate will be Total Quantity and Av Rate as it is uniform in the group.
    deviation_quantity_rate = combined_transactions_data.groupby(['Date', 'Market Real', 'Crop']).agg(
        {'Deviation': ['sum'], 'Total Quantity': ['mean'], 'Av Rate': ['mean']}).reset_index()
    deviation_quantity_rate.columns = deviation_quantity_rate.columns.droplevel(1)
    deviation_quantity_rate['std'] = np.sqrt(deviation_quantity_rate['Deviation'] / deviation_quantity_rate['Total Quantity'])
    deviation_quantity_rate = deviation_quantity_rate.sort_values(by='std', ascending=False)

    # Inserting standard deviation against each row and identifying rows which are outliers
    outlier_ct_data_2 = combined_transactions_data.merge(deviation_quantity_rate, on=['Date', 'Market Real', 'Crop'])
    outlier_ct_data_2 = outlier_ct_data_2.rename(columns={'Av Rate_x': 'Av Rate'})
    cols = list(outlier_ct_data_2.loc[:, 'Date':'State']) + ['Av Rate'] + ['std']
    outlier_ct_data_2 = outlier_ct_data_2[cols]
    outlier_ct_data_2['Mean-Deviation'] = outlier_ct_data_2['Price'] - outlier_ct_data_2['Av Rate']
    outlier_ct_data_2['Deviation Factor'] = np.square(outlier_ct_data_2['Mean-Deviation']) / (
    outlier_ct_data_2['Av Rate'] * outlier_ct_data_2['std'])

    # Keeping only outliers in outlier_ct_data_2
    outlier_ct_data_2 = outlier_ct_data_2[
        (outlier_ct_data_2['Deviation Factor'] > deviation_factor_threshold) & (outlier_ct_data_2['std'] > quantity_rate_deviation_threshold)]

    # Mapping outliers rows in combined_transactions and filtering them out.
    outlier_merged_2 = outlier_ct_data_2.merge(combined_transactions_data, on=columnlist_ct)
    combined_transactions_data = combined_transactions_data[
        ~combined_transactions_data.isin(outlier_merged_2)].dropna()
    combined_transactions_data = combined_transactions_data.loc[:, 'Date': 'State']

    # print outlier_ct_data_2.head()
    outlier_ct_data_2.to_csv('outliers_2.csv') #Recording outliers in a CSV file
    combined_transactions_data.to_csv('after_outliers_removal.csv') # Recording data after removal of outliers in CSV file
    combined_transactions_data['datetime'] = combined_transactions_data['Date'].astype('datetime64[ns]')
    combined_transactions_data['datetime'] = combined_transactions_data['datetime'].astype('int64')
    combined_transactions_data.plot(use_index=False,kind='scatter',x='datetime',y='Price',figsize=(18,8))
    # plt.show()

    return combined_transactions_data

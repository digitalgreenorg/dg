import pandas as pd
import numpy as np
import Tables
import Transport_Cost

# TODO: Remove rate outliers
# TODO: Optimise on multiple markets and not on one market
# TODO: Insert geography in aggregator-wise analysis
# TODO: Insert names in all sheets
# TODO: Get market count only when all rates of all crops are available
# TODO: If rate is not available, then take rates of T-1, T+1

daily_aggregator_crop_data = Tables.daily_aggregator_crop_data
daily_market_crop_data = Tables.daily_market_crop_data
daily_aggregator_data = Tables.daily_aggregator_data
vehicle_market_cost = Transport_Cost.vehicle_market_cost
daily_market_transport_cost = Transport_Cost.daily_market_transport_cost
aggregator_list = Tables.aggregator_list
market_list = Tables.market_list

# Finds the ideal market that returns maximum amount for all the crops sold by an aggregator per visit

crop_count_per_visit = daily_aggregator_crop_data.groupby(['Date', 'Aggregator', 'Market Real']).agg({'Crop_1': ['count']}).reset_index()
crop_count_per_visit.columns = crop_count_per_visit.columns.droplevel(1)
crop_count_per_visit = crop_count_per_visit.rename(columns = {'Crop_1': 'Crop Count'})
# print crop_count_per_visit.head()

# For each D-A-M-C combination, merged_data has list of markets and the average rate where these crops could have been sold.
merged_data = pd.merge(daily_aggregator_crop_data, daily_market_crop_data, how='inner', left_on= ['Date','Crop_1'], right_on= ['Date','Crop_2'])
merged_data['Amount'] = merged_data['Quantity Real']*merged_data['Av Rate']
merged_data_crop_count_per_market = merged_data.groupby(['Date', 'Aggregator', 'Market Real', 'Market']).agg({'Crop_2': ['count']}).reset_index()
merged_data_crop_count_per_market.columns = merged_data_crop_count_per_market.columns.droplevel(1)
merged_data_crop_count_per_market = merged_data_crop_count_per_market.rename(columns = {'Crop_2': 'Crop Count 2'})

# List of markets where we have rates of all crops that were sold.
merged_data_filtered_market_list = pd.merge(crop_count_per_visit, merged_data_crop_count_per_market, how='inner', on= ['Date', 'Aggregator', 'Market Real'])
merged_data_filtered_market_list = merged_data_filtered_market_list[merged_data_filtered_market_list['Crop Count'] == merged_data_filtered_market_list['Crop Count 2']]
# print merged_data_filtered_market_list

# merged_data = pd.merge(daily_aggregator_crop_data, daily_market_crop_data, how='outer', left_on= ['Date','Crop_1'], right_on= ['Date','Crop_2'])
# merged_data['Amount'] = merged_data['Quantity Real']*merged_data['Av Rate']
# print merged_data.head()


grouped_1 = merged_data.groupby(['Date', 'Aggregator', 'Market Real', 'Market'])['Amount'].agg(np.sum).reset_index()
# print grouped_1.size

# For each D-A-M combination, grouped_1 has market-wise predicted amount for markets where we know rates of all crops
grouped_1 = pd.merge(grouped_1, merged_data_filtered_market_list, how= 'inner', on= ['Date', 'Aggregator', 'Market Real', 'Market'])
# print grouped_1.head()

# Grouped_1 with quantity
grouped_1_with_quantity = grouped_1.merge(daily_aggregator_data, how= 'inner', on= ['Date', 'Aggregator', 'Market Real'])
cols = list(grouped_1_with_quantity.loc[:, 'Date':'Amount']) + list(grouped_1_with_quantity.loc[:, 'Daily_Quantity':'State'])
grouped_1_with_quantity = grouped_1_with_quantity[cols]
# print grouped_1_with_quantity.head()

# For each predicted market, grouped_1_with_quantity_cost has vehicles which could have been used.
# Market combinations will be present even if no vehicle data is there for that A-M combination.
grouped_1_with_quantity_cost = grouped_1_with_quantity.merge(vehicle_market_cost, how= 'left', on= ['Aggregator', 'Market'])
# print grouped_1_with_quantity_cost.head()
#
# cols = list(grouped_1_with_quantity_cost.loc[:, 'Date':'Amount']) + list(grouped_1_with_quantity_cost.loc[:, 'Daily_Quantity': 'Vehicle ID']) + ['Transport Cost_median'] + ['Vehicle'] + ['Quantity Limit']
# grouped_1_with_quantity_cost = grouped_1_with_quantity_cost[cols]
#
# # print grouped_1_with_quantity_cost.head()
# # print grouped_1.size
#
temp_1 = grouped_1_with_quantity_cost[grouped_1_with_quantity_cost['Daily_Quantity'] < grouped_1_with_quantity_cost['Quantity Limit']]

# # print temp_1.head()

temp_2 = temp_1.groupby(['Date', 'Aggregator', 'Market Real', 'Market']).agg({'Transport Cost_median': ['min']}).reset_index()
temp_2.columns = temp_2.columns.droplevel(1)


# print temp_2.head()
temp_2 = temp_2.merge(temp_1, how= 'inner', on= ['Date', 'Aggregator', 'Market Real', 'Market', 'Transport Cost_median'])
# print temp_2.head()

temp_2 = pd.merge(grouped_1_with_quantity, temp_2, how= 'left', on= ['Date', 'Aggregator', 'Market Real', 'Market'])
cols = list(temp_2.loc[:, 'Date':'Transport Cost_median']) + list(temp_2.loc[:, 'Vehicle ID':'Quantity Limit'])
temp_2 = temp_2[cols]
temp_2 = temp_2.rename(columns= {'Amount_x':'Amount', 'Daily_Quantity_x':'Daily_Quantity', 'Daily_Amount_x':'Daily_Amount', 'State_x':'State'})
# print temp_2.head()
#
temp_2['Transport Cost_median'].fillna(temp_2['Daily_Quantity'], inplace= True)
# print temp_2.isnull().sum()

temp_2 = temp_2.merge(daily_market_transport_cost, how= 'inner', on= ['Date', 'Aggregator', 'Market Real'])
# print temp_2.isnull().sum()

temp_2['Net Return Real'] = temp_2['Daily_Amount'] - temp_2['Transport Cost Real']
temp_2['Net Return Ideal'] = temp_2['Amount'] - temp_2['Transport Cost_median']

impact_data = temp_2.groupby(['Date', 'Aggregator', 'Market Real']).agg({'Net Return Ideal':['max'], 'Net Return Real': ['mean'],'Market': ['count']}).reset_index()
impact_data.columns = impact_data.columns.droplevel(1)
impact_data = impact_data.rename(columns= {'Market': 'Market Count'})
impact_data = impact_data.merge(temp_2, how= 'inner', on= ['Date', 'Aggregator', 'Market Real', 'Net Return Ideal']).loc[:, 'Date':'Market']
impact_data = impact_data.rename(columns= {'Net Return Real_x': 'Net Return Real'})
# # impact_data['Net Return Ideal'][impact_data['Market Real'] == impact_data['Market']] = impact_data['Net Return Real'][impact_data['Market Real'] == impact_data['Market']]
print impact_data.head()

aggregator_wise_impact = impact_data.groupby(['Aggregator']).agg({'Net Return Ideal': ['sum'], 'Net Return Real': ['sum'], 'Date': ['count']}).reset_index()
aggregator_wise_impact.columns = aggregator_wise_impact.columns.droplevel(1)
aggregator_wise_impact = aggregator_wise_impact.rename(columns = {'Date': 'Visits Count'})
aggregator_wise_impact['Delta %'] = (aggregator_wise_impact['Net Return Ideal']/aggregator_wise_impact['Net Return Real'] - 1)*100
# aggregator_wise_impact['Per Kg Delta'] = (aggregator_wise_impact['Ideal Amount'] - aggregator_wise_impact['Total Amount']) / aggregator_wise_impact['Total Quantity']
# print aggregator_wise_impact.head()

market_count_wise_impact = impact_data.groupby(['Market Count']).agg({'Net Return Ideal': ['sum'], 'Net Return Real': ['sum'], 'Date': ['count']}).reset_index()
market_count_wise_impact.columns = market_count_wise_impact.columns.droplevel(1)
market_count_wise_impact = market_count_wise_impact.rename(columns = {'Date': 'Total Visits'})
market_count_wise_impact['Delta %'] = (market_count_wise_impact['Net Return Ideal']/market_count_wise_impact['Net Return Real'] - 1)*100
# market_count_wise_impact['Per Kg Delta'] = (market_count_wise_impact['Ideal Amount'] - market_count_wise_impact['Total Amount']) / market_count_wise_impact['Total Quantity']

# print market_count_wise_impact.head()
print impact_data['Net Return Ideal'].agg(np.sum)/impact_data['Net Return Real'].agg(np.sum)
# #
aggregator_wise_impact.to_csv('Aggregator Wise Net Impact.csv', index= False)
market_count_wise_impact.to_csv('Market Count Wise Net Impact 1.csv', index= False)

#
# #
# # grouped_1 = grouped_1[(grouped_1['Date'] == merged_data_filtered_market_list['Date']) & (grouped_1['Aggregator'] == merged_data_filtered_market_list['Aggregator']) & (grouped_1['Market Real'] == merged_data_filtered_market_list['Market Real']) & (grouped_1['Market'] == merged_data_filtered_market_list['Market'])]
# # # print grouped_1.size
# # print grouped_1.head()
#
#
# #
# # grouped_2 = grouped_1.groupby(['Date', 'Aggregator', 'Market Real']).agg({'Amount':['max'],'Market': ['count']}).reset_index()
# # # print grouped_2.head()
# #
# # grouped_3 = pd.merge(grouped_2, grouped_1, how = 'inner', on= ['Date', 'Aggregator', 'Market Real', 'Amount'])
# # # print grouped_3.head()
# #
# # # Creates a final table that has ideal market details for each market visit
# # final_data = pd.merge(daily_aggregator_data, grouped_3, how='inner', on= ['Date', 'Aggregator', 'Market Real'])
# # final_data['% increase'] = (final_data['Amount']/final_data['Daily_Amount'] - 1)*100
# # # print final_data.head()
# #

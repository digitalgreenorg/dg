import pandas as pd
import numpy as np
import Tables

# TODO: Remove rate outliers
# TODO: Optimise on multiple markets and not on one market
# TODO: Insert geography in aggregator-wise analysis
# TODO: Insert names in all sheets
# TODO: Get market count only when all rates of all crops are available
# TODO: If rate is not available, then take rates of T-1, T+1

daily_aggregator_crop_query_result = list(Tables.daily_aggregator_crop_query_result)
daily_crop_market_query_result = list(Tables.daily_crop_market_query_result)
daily_aggregator_sales_query_result = list(Tables.daily_aggregator_sales_query_result)

# Converts SQL results into dataframes and filter out non-Bihar data
columnlist = ['Date', 'Aggregator', 'Market Real', 'Crop_1', 'Quantity Real', 'State']
daily_aggregator_crop_data = pd.DataFrame(daily_aggregator_crop_query_result, columns= columnlist)
daily_aggregator_crop_data = daily_aggregator_crop_data[daily_aggregator_crop_data['State'] == 1]

columnlist = ['Date', 'Market', 'Crop_2', 'Total_Quantity', 'Av Rate', 'State']
daily_market_crop_data = pd.DataFrame(daily_crop_market_query_result, columns=columnlist)
daily_market_crop_data = daily_market_crop_data[(daily_market_crop_data['State'] == 1) & (daily_market_crop_data['Av Rate'] < 50)]
#daily_market_crop_data = daily_market_crop_data[daily_market_crop_data['State'] == 1]


columnlist = ['Date', 'Aggregator', 'Market Real', 'Daily_Quantity', 'Daily_Amount', 'State']
daily_aggregator_data = pd.DataFrame(daily_aggregator_sales_query_result, columns= columnlist)
daily_aggregator_data = daily_aggregator_data[daily_aggregator_data['State'] == 1]


# Finds the ideal market that returns maximum amount for all the crops sold by an aggregator per visit

crop_count_per_visit = daily_aggregator_crop_data.groupby(['Date', 'Aggregator', 'Market Real']).agg({'Crop_1': ['count']}).reset_index()
crop_count_per_visit.columns = crop_count_per_visit.columns.droplevel(1)
crop_count_per_visit = crop_count_per_visit.rename(columns = {'Crop_1': 'Crop Count'})
# print crop_count_per_visit.head()

merged_data = pd.merge(daily_aggregator_crop_data, daily_market_crop_data, how='inner', left_on= ['Date','Crop_1'], right_on= ['Date','Crop_2'])
merged_data['Amount'] = merged_data['Quantity Real']*merged_data['Av Rate']
merged_data_crop_count_per_market = merged_data.groupby(['Date', 'Aggregator', 'Market Real', 'Market']).agg({'Crop_2': ['count']}).reset_index()
merged_data_crop_count_per_market.columns = merged_data_crop_count_per_market.columns.droplevel(1)
merged_data_crop_count_per_market = merged_data_crop_count_per_market.rename(columns = {'Crop_2': 'Crop Count 2'})

merged_data_filtered_market_list = pd.merge(crop_count_per_visit, merged_data_crop_count_per_market, how='inner', on= ['Date', 'Aggregator', 'Market Real'])
merged_data_filtered_market_list = merged_data_filtered_market_list[merged_data_filtered_market_list['Crop Count'] == merged_data_filtered_market_list['Crop Count 2']]
# print merged_data_filtered_market_list

# merged_data = pd.merge(daily_aggregator_crop_data, daily_market_crop_data, how='outer', left_on= ['Date','Crop_1'], right_on= ['Date','Crop_2'])
# merged_data['Amount'] = merged_data['Quantity Real']*merged_data['Av Rate']
# print merged_data.head()


grouped_1 = merged_data.groupby(['Date', 'Aggregator', 'Market Real', 'Market'])['Amount'].agg(np.sum).reset_index()
print grouped_1.size

grouped_1 = pd.merge(grouped_1, merged_data_filtered_market_list, how= 'inner', on= ['Date', 'Aggregator', 'Market Real', 'Market'])
print grouped_1.size

# grouped_1 = grouped_1[(grouped_1['Date'] == merged_data_filtered_market_list['Date']) & (grouped_1['Aggregator'] == merged_data_filtered_market_list['Aggregator']) & (grouped_1['Market Real'] == merged_data_filtered_market_list['Market Real']) & (grouped_1['Market'] == merged_data_filtered_market_list['Market'])]
# print grouped_1.size
# print grouped_1.head()

grouped_2 = grouped_1.groupby(['Date', 'Aggregator', 'Market Real']).agg({'Amount':['max'],'Market': ['count']}).reset_index()
grouped_2.columns = grouped_2.columns.droplevel(1)
grouped_2 = grouped_2.rename(columns = {'Market': 'Market Count'})
# print grouped_2.head()

grouped_3 = pd.merge(grouped_2, grouped_1, how = 'inner', on= ['Date', 'Aggregator', 'Market Real', 'Amount'])
# print grouped_3.head()

# Creates a final table that has ideal market details for each market visit
final_data = pd.merge(daily_aggregator_data, grouped_3, how='inner', on= ['Date', 'Aggregator', 'Market Real'])
final_data['% increase'] = (final_data['Amount']/final_data['Daily_Amount'] - 1)*100
print final_data.head()

aggregator_wise_impact = final_data.groupby(['Aggregator']).agg({'Daily_Quantity': ['sum'], 'Daily_Amount': ['sum'],'Amount':['sum'], 'Date': ['count']}).reset_index()
aggregator_wise_impact.columns = aggregator_wise_impact.columns.droplevel(1)
aggregator_wise_impact = aggregator_wise_impact.rename(columns = {'Daily_Quantity': 'Total Quantity', 'Daily_Amount': 'Total Amount', 'Amount': 'Ideal Amount', 'Date': 'Visits Count'})
aggregator_wise_impact['Delta %'] = (aggregator_wise_impact['Ideal Amount']/aggregator_wise_impact['Total Amount'] - 1)*100
aggregator_wise_impact['Per Kg Delta'] = (aggregator_wise_impact['Ideal Amount'] - aggregator_wise_impact['Total Amount']) / aggregator_wise_impact['Total Quantity']
print aggregator_wise_impact.head()

market_count_wise_impact = final_data.groupby(['Market Count']).agg({'Daily_Quantity': ['sum'], 'Daily_Amount': ['sum'],'Amount':['sum'], 'Date': ['count']}).reset_index()
market_count_wise_impact.columns = market_count_wise_impact.columns.droplevel(1)
market_count_wise_impact = market_count_wise_impact.rename(columns = {'Daily_Quantity': 'Total Quantity', 'Daily_Amount': 'Total Amount', 'Amount': 'Ideal Amount', 'Date': 'Total Visits'})
market_count_wise_impact['Delta %'] = (market_count_wise_impact['Ideal Amount']/market_count_wise_impact['Total Amount'] - 1)*100
market_count_wise_impact['Per Kg Delta'] = (market_count_wise_impact['Ideal Amount'] - market_count_wise_impact['Total Amount']) / market_count_wise_impact['Total Quantity']

print market_count_wise_impact.head()
print final_data['Amount'].agg(np.sum)/final_data['Daily_Amount'].agg(np.sum)

aggregator_wise_impact.to_csv('Aggregator Wise Impact.csv', index= False)
market_count_wise_impact.to_csv('Market Count Wise Impact.csv', index= False)
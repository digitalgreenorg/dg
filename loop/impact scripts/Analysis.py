import pandas as pd
import numpy as np
import Tables

daily_aggregator_crop_query_result = list(Tables.daily_aggregator_crop_query_result)
daily_crop_market_query_result = list(Tables.daily_crop_market_query_result)
daily_aggregator_sales_query_result = list(Tables.daily_aggregator_sales_query_result)

# Create condition to choose max number of markets per day
columnlist = ['Date', 'Aggregator', 'Market Real', 'Crop_1', 'Quantity Real', 'State']
daily_aggregator_crop_data = pd.DataFrame(daily_aggregator_crop_query_result, columns= columnlist)
daily_aggregator_crop_data = daily_aggregator_crop_data[daily_aggregator_crop_data['State'] == 1]

columnlist = ['Date', 'Market', 'Crop_2', 'Total_Quantity', 'Av Rate', 'State']
daily_market_crop_data = pd.DataFrame(daily_crop_market_query_result, columns=columnlist)
daily_market_crop_data = daily_market_crop_data[daily_market_crop_data['State'] == 1]

columnlist = ['Date', 'Aggregator', 'Market Real', 'Daily_Quantity', 'Daily_Amount', 'State']
daily_aggregator_data = pd.DataFrame(daily_aggregator_sales_query_result, columns= columnlist)
daily_aggregator_data = daily_aggregator_data[daily_aggregator_data['State'] == 1]

# Create condition that all crops must be necessary
#Columns in merged_data = Date  Aggregator  Crop_1  Quantity  Market  Crop_2    Total_Quantity    Av Rate        Amount
merged_data = pd.merge(daily_aggregator_crop_data, daily_market_crop_data, how='outer', left_on= ['Date','Crop_1'], right_on= ['Date','Crop_2'])
merged_data['Amount'] = merged_data['Quantity Real']*merged_data['Av Rate']
# print merged_data.head()

# Quantity not here because it could be wrong.
grouped_1 = merged_data.groupby(['Date', 'Aggregator', 'Market Real', 'Market'])['Amount'].agg(np.sum).reset_index()
# print grouped_1.head()

grouped_2 = grouped_1.groupby(['Date', 'Aggregator', 'Market Real']).agg({'Amount':['max'],'Market': ['count']}).reset_index()
grouped_2.columns = grouped_2.columns.droplevel(1)
grouped_2 = grouped_2.rename(columns = {'Market': 'Market Count'})
# print grouped_2.head()

grouped_3 = pd.merge(grouped_2, grouped_1, how = 'inner', on= ['Date', 'Aggregator', 'Market Real', 'Amount'])
# print grouped_3.head()

final_data = pd.merge(daily_aggregator_data, grouped_3, how='inner', on= ['Date', 'Aggregator', 'Market Real'])
final_data['% increase'] = (final_data['Amount']/final_data['Daily_Amount'] - 1)*100

aggregator_wise_impact = final_data.groupby(['Aggregator']).agg({'Daily_Quantity': ['sum'], 'Daily_Amount': ['sum'],'Amount':['sum']}).reset_index()
aggregator_wise_impact.columns = aggregator_wise_impact.columns.droplevel(1)
aggregator_wise_impact = aggregator_wise_impact.rename(columns = {'Daily_Quantity': 'Total Quantity', 'Daily_Amount': 'Total Amount', 'Amount': 'Ideal Amount'})
aggregator_wise_impact['Delta %'] = (aggregator_wise_impact['Ideal Amount']/aggregator_wise_impact['Total Amount'] - 1)*100
aggregator_wise_impact['Per Kg Delta'] = (aggregator_wise_impact['Ideal Amount'] - aggregator_wise_impact['Total Amount']) / aggregator_wise_impact['Total Quantity']
print aggregator_wise_impact.head()

print final_data.head()

market_count_wise_impact = final_data.groupby(['Market Count']).agg({'Daily_Quantity': ['sum'], 'Daily_Amount': ['sum'],'Amount':['sum']}).reset_index()
market_count_wise_impact.columns = market_count_wise_impact.columns.droplevel(1)
market_count_wise_impact = market_count_wise_impact.rename(columns = {'Daily_Quantity': 'Total Quantity', 'Daily_Amount': 'Total Amount', 'Amount': 'Ideal Amount'})
market_count_wise_impact['Delta %'] = (market_count_wise_impact['Ideal Amount']/market_count_wise_impact['Total Amount'] - 1)*100
market_count_wise_impact['Per Kg Delta'] = (market_count_wise_impact['Ideal Amount'] - market_count_wise_impact['Total Amount']) / market_count_wise_impact['Total Quantity']

print market_count_wise_impact
print final_data['Amount'].agg(np.sum)/final_data['Daily_Amount'].agg(np.sum)

aggregator_wise_impact.to_csv('Aggregator Wise Impact.csv', index= False)
market_count_wise_impact.to_csv('Market Count Wise Impact.csv', index= False)
# TODO: Remove rate outliers
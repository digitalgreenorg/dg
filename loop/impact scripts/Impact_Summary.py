import Impact
import pandas as pd

daily_transaction_corrected_data = Impact.daily_transaction_corrected_data
print len(daily_transaction_corrected_data.index) - daily_transaction_corrected_data.count()

# Removes rows where NA is there in any column
daily_transaction_corrected_data = daily_transaction_corrected_data.dropna()

daily_local_market_transactions_data = daily_transaction_corrected_data[daily_transaction_corrected_data['Market'] == daily_transaction_corrected_data['Local_Market']]

aggregator_wise_local_transport_savings = daily_local_market_transactions_data.groupby(['Aggregator']).agg({'Transport_Cost': 'sum', 'Predicted_TC': 'sum'}).reset_index()
aggregator_wise_local_transport_savings['% Savings'] = (1 - (aggregator_wise_local_transport_savings['Transport_Cost'] / aggregator_wise_local_transport_savings['Predicted_TC']))*100

local_market_visits_wise_farmer_count = daily_local_market_transactions_data.groupby(['Aggregator', 'Market', 'Date'])['Farmer'].nunique().reset_index()
local_market_visits_wise_savings = daily_local_market_transactions_data.groupby(['Aggregator', 'Market', 'Date']).agg({'Transport_Cost': 'sum', 'Predicted_TC': 'sum'}).reset_index()
local_market_visits_wise_savings = pd.merge(local_market_visits_wise_savings, local_market_visits_wise_farmer_count, on= ['Aggregator', 'Market', 'Date'])

print daily_local_market_transactions_data.head()

writer = pd.ExcelWriter('Impact_Loop_Jan_29.xlsx')
daily_transaction_corrected_data.to_excel(writer,'Impact_Data')
aggregator_wise_local_transport_savings.to_excel(writer, 'Aggregator Local Impact')
local_market_visits_wise_savings.to_excel(writer, 'Local Market Visits Wise Impact')
writer.save()
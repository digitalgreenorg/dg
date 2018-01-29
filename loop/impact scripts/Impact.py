import pandas as pd
import Tables, Transport_Cost, Functions, Crop_Rate_Outliers_Removal

# TODO: Include other states' vehicles in vehicle_to_fill_na_data. Needed to make it generic.
# TODO: Clean all data coming from Tables
# TODO: Predict rates when produce was not sold on that day using data of other days or rates of other markets
# TODO: Improve prediction of Transport Cost, remove outliers
# TODO: Integrate Gadidar Share in Analysis
# TODO: Vehichle should be state-wise in DB

# Importing dataframes from Tables file

# columnlist = ['Date', 'Aggregator', 'Farmer', 'Farmer_Quantity']
daily_farmer_quantity_data = Tables.daily_farmer_quantity_data

# columnlist = ['Date', 'Aggregator', 'Market', 'Quantity','Transport_Cost', 'TCPK', 'Farmer_Share', 'FSPK']
daily_aggregator_market_data = Tables.daily_aggregator_market_data

# columnlist = ['Date', 'Aggregator', 'Market', 'Gaddidar', 'Farmer', 'Crop', 'Quantity', 'Price', 'Amount']
daily_transaction_data = Tables.daily_transaction_data

# columnlist = ['Date', 'Aggregator', 'Market', 'DT_ID', 'Vehicle_ID', 'Vehicle_Name','Transport_Cost','Quantity', 'State' ]
daily_transportation_data = Tables.daily_transportation_data

# List of state-wise frequently used vehicles
vehicles_to_fill_na_data = {'State': [1,1,1,1], 'Vehicle_ID': [2, 3, 4, 5]}
vehicles_to_fill_na = pd.DataFrame(data= vehicles_to_fill_na_data)

# columnlist = ['Aggregator', 'Aggregator_Name', 'District_Name','State_ID', 'State_Name']
aggregator_list = Tables.aggregator_list

# columnlist = ['Market', 'Market_Name']
market_list = Tables.market_list

# Importing functions
get_clean_data = Crop_Rate_Outliers_Removal.get_clean_data
get_grouped_clean_data = Crop_Rate_Outliers_Removal.get_grouped_clean_data

fill_local_market_rate = Functions.fill_local_market_rate
find_predicted_cost = Functions.find_predicted_cost
fill_transport_data = Functions.fill_transport_data
fill_predicted_cost = Functions.fill_predicted_cost
get_aggregator_local_market = Functions.get_aggregator_local_market

get_transport_cost_amv = Transport_Cost.get_transport_cost_amv

# Eventually, we will remove outliers from ct data and then run everything on it.
daily_transaction_corrected_data = daily_transaction_data

# Step 1: Find rate in local market (non-Loop) for that date-aggregator-crop combination and integrate in daily_transaction_corrected data

# Step 1.1 Find aggregator-wise local markets
aggregator_local_market = get_aggregator_local_market(daily_aggregator_market_data)
# Step 1.2 Find rate in that local market
daily_market_crop_data = get_grouped_clean_data(daily_transaction_corrected_data)
daily_transaction_corrected_data = fill_local_market_rate(daily_market_crop_data, daily_transaction_corrected_data, aggregator_local_market)

# Step 2: Integrate transport cost, farmer share in daily_transaction_corrected_data
daily_transaction_corrected_data = fill_transport_data(daily_aggregator_market_data, daily_transaction_corrected_data)

# Step 3: Find cost of transportation for the farmer in non-Loop scenario and integrate it in transaction-level data
aggregator_market_vehicle_predicted_cost_quantity = get_transport_cost_amv(daily_transportation_data, vehicles_to_fill_na)
daily_farmer_quantity_data = find_predicted_cost(daily_farmer_quantity_data, aggregator_local_market,aggregator_market_vehicle_predicted_cost_quantity)

daily_transaction_corrected_data = fill_predicted_cost(daily_farmer_quantity_data, daily_transaction_corrected_data)

# print daily_transaction_corrected_data.head()

daily_transaction_corrected_data = pd.merge(daily_transaction_corrected_data, aggregator_list, on=['Aggregator'])
daily_transaction_corrected_data = pd.merge(daily_transaction_corrected_data, market_list, on=['Market'])

daily_transaction_corrected_data = daily_transaction_corrected_data[daily_transaction_corrected_data['State_ID'] == 1]






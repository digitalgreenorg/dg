import pandas as pd
import numpy as np
import Tables

# TODO: Remove outliers while finding transport cost for A-M combination
# TODO: Include data when multiple vehicles were used
# TODO: Automate capacity prediction of vehicles
# TODO: Predict cost when vehicle was not used for the A-M combination
# TODO: Remove motorcycle

# Quantity is total quantity for that D-A-M combination and not for the vehicle
# columnlist = ['Date', 'Aggregator', 'Market', 'Quantity', 'Vehicle_ID', 'Transport_Cost']
daily_transportation_data = Tables.daily_transportation_data

daily_vehicle_count = daily_transportation_data.groupby(['Date', 'Aggregator', 'Market']).agg({'DT_ID': 'count'}).reset_index()
daily_vehicle_count = daily_vehicle_count.rename(columns= {'DT_ID': 'Vehicle_Count'})

daily_vehicle_single_count = daily_vehicle_count[daily_vehicle_count['Vehicle_Count'] == 1]

daily_vehicle_single_data = pd.merge(daily_transportation_data, daily_vehicle_single_count, on= ['Date', 'Aggregator', 'Market'], how= 'inner')

vehicle_quantity_limits = daily_vehicle_single_data.groupby(['Vehicle_ID', 'Vehicle_Name'])['Quantity'].quantile(0.35).reset_index()
vehicle_quantity_limits = vehicle_quantity_limits.rename(columns = {'Quantity': 'Quantity_Min'})

vehicle_quantity_limits_75 = daily_vehicle_single_data.groupby(['Vehicle_ID'])['Quantity'].quantile(0.90).reset_index()
vehicle_quantity_limits = pd.merge(vehicle_quantity_limits, vehicle_quantity_limits_75, on= ['Vehicle_ID'])
vehicle_quantity_limits = vehicle_quantity_limits.rename(columns = {'Quantity': 'Quantity_Max'})

daily_vehicle_single_data = pd.merge(daily_vehicle_single_data, vehicle_quantity_limits, on=['Vehicle_ID', 'Vehicle_Name'])
daily_vehicle_single_data_filtered = daily_vehicle_single_data[(daily_vehicle_single_data['Quantity'] > daily_vehicle_single_data['Quantity_Min']) & (daily_vehicle_single_data['Quantity'] < daily_vehicle_single_data['Quantity_Max'])]

# Transport_cost_median is the predicted cost for vehicle for the given Aggregator-Market combination
vehicle_market_cost = daily_vehicle_single_data_filtered.groupby(['Aggregator', 'Market', 'Vehicle_ID', 'Vehicle_Name']).agg({'Transport_Cost': ['median'], 'Quantity_Min': ['median'], 'Quantity_Max': ['median']}).reset_index()
vehicle_market_cost.columns = vehicle_market_cost.columns.map('_'.join)
vehicle_market_cost = vehicle_market_cost.rename(columns = {'Aggregator_': 'Aggregator', 'Market_': 'Market', 'Vehicle_ID_': 'Vehicle_ID', 'Vehicle_Name_': 'Vehicle_Name', 'Transport_Cost_median': 'Predicted_TC', 'Quantity_Min_median': 'Quantity_Min', 'Quantity_Max_median':'Quantity_Limit'})

vehicle_market_cost = vehicle_market_cost[vehicle_market_cost['Vehicle_ID'] != 1]
# # Not sure why below code snippet is needed
# daily_market_transport_cost = daily_transportation_data.groupby(['Date','Aggregator', 'Market']).agg({'Transport_Cost': ['sum']}).reset_index()
# daily_market_transport_cost.columns = daily_market_transport_cost.columns.droplevel(1)
# daily_market_transport_cost = daily_market_transport_cost.rename(columns= {'Market': 'Market Real', 'Transport_Cost': 'Transport_Cost_Real'})

# total_market_transport_cost = daily_market_transport_cost.groupby(['Aggregator', 'Market Real']).agg({'Transport Cost Real': ['sum'], 'Quantity': ['sum']})
# total_market_transport_cost['CPK'] = total_market_transport_cost['Transport Cost Real']/total_market_transport_cost['Quantity']
# print total_market_transport_cost.sort_values(by='CPK', ascending= False)

# vehicle_market_cost.to_csv('Vehicle Cost Analysis.csv', index= False)

# print vehicle_market_cost.head()

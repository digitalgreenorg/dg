import pandas as pd
# import numpy as np
import Tables

# TODO: Remove outliers while finding transport cost for A-M combination
# TODO: Automate capacity prediction of vehicles
# TODO: Predict cost when vehicle was not used for the A-M combination

# List of vehicles and maximum capacity of each vehicle.
vehicle_list = [['Pickup', 4, 3000], ['Tata Ace', 5, 1800], ['Tempo', 2, 500], ['Jugaad', 3, 750]]
vehicle_data = pd.DataFrame(vehicle_list, columns= ['Vehicle', 'Vehicle_ID', 'Quantity_Limit'])

# Quantity is total quantity for that D-A-M combination and not for the vehicle
# columnlist = ['Date', 'Aggregator', 'Market', 'Quantity', 'Vehicle_ID', 'Transport_Cost']
daily_transportation_data = Tables.daily_transportation_data


# Transport_cost_median is the predicted cost for vehicle for the given Aggregator-Market combination
vehicle_market_cost = daily_transportation_data.groupby(['Aggregator', 'Market', 'Vehicle_ID']).agg({'Transport_Cost': ['median']}).reset_index()
vehicle_market_cost.columns = vehicle_market_cost.columns.map('_'.join)
vehicle_market_cost = vehicle_market_cost.rename(columns = {'Aggregator_': 'Aggregator', 'Market_': 'Market', 'Vehicle_ID_': 'Vehicle_ID', 'Transport_Cost_median': 'Predicted_TC'})

vehicle_market_cost = pd.merge(vehicle_data, vehicle_market_cost, how= 'left', on= 'Vehicle_ID')

# Not sure why below code snippet is needed
daily_market_transport_cost = daily_transportation_data.groupby(['Date','Aggregator', 'Market']).agg({'Transport_Cost': ['sum']}).reset_index()
daily_market_transport_cost.columns = daily_market_transport_cost.columns.droplevel(1)
daily_market_transport_cost = daily_market_transport_cost.rename(columns= {'Market': 'Market Real', 'Transport_Cost': 'Transport_Cost_Real'})

# total_market_transport_cost = daily_market_transport_cost.groupby(['Aggregator', 'Market Real']).agg({'Transport Cost Real': ['sum'], 'Quantity': ['sum']})
# total_market_transport_cost['CPK'] = total_market_transport_cost['Transport Cost Real']/total_market_transport_cost['Quantity']
# print total_market_transport_cost.sort_values(by='CPK', ascending= False)

# vehicle_market_cost.to_csv('Vehicle Cost Analysis.csv', index= False)

# print vehicle_market_cost.head()

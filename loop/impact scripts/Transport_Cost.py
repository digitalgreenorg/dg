import pandas as pd
import numpy as np

# TODO: Remove outliers using TCPK method before taking median while finding transport cost for A-M-V combination
# TODO: Include data when multiple vehicles were used
# TODO: Even where sample size for A-M-V is small, we should use predicted cost to find cost.
# TODO: Should also incorporate accuracy of median in transport cost prediction

# Quantity is total quantity for that D-A-M combination and not for the vehicle
# columnlist = ['Date', 'Aggregator', 'Market', 'Quantity', 'Vehicle_ID', 'Transport_Cost']

# All analysis is done on each state separately as data of multiple states are not coherent with each other.

# columnlist for daily_transportation_data= ['Date', 'Aggregator', 'Market', 'DT_ID', 'Vehicle_ID', 'Vehicle_Name','Transport_Cost','Quantity', 'State' ]
def get_transport_cost_amv(daily_transportation_data, vehicles_to_fill_na):
    daily_vehicle_single_data = get_single_vehicle_data(daily_transportation_data)
    vehicle_quantity_limits = find_vehicle_quantity_limits(daily_vehicle_single_data)
    aggregator_market_vehicle_cost_detailed = find_transport_cost_amv(daily_vehicle_single_data, vehicle_quantity_limits)
    aggregator_market_vehicle_cost = aggregator_market_vehicle_cost_detailed.drop(
        ['Vehicle_Name', 'Quantity_Min', 'Quantity_Limit'], axis=1)
    aggregator_market_vehicle_cost_na = find_predicted_transport_cost_amv(aggregator_market_vehicle_cost, vehicles_to_fill_na)
    aggregator_market_vehicle_cost = aggregator_market_vehicle_cost.append(aggregator_market_vehicle_cost_na)

    print 'Motorcycle List'
    aggregator_market_motorcycle_list = aggregator_market_vehicle_cost[aggregator_market_vehicle_cost['Vehicle_ID'] == 0]
    aggregator_market_motorcycle_list['Motorcycle Cost'] = 0.4*aggregator_market_motorcycle_list['Predicted_TC']
    aggregator_market_motorcycle_list['Vehicle_ID'] = 1
    aggregator_market_motorcycle_list['Predicted_TC'] = aggregator_market_motorcycle_list['Motorcycle Cost']
    aggregator_market_motorcycle_list = aggregator_market_motorcycle_list.drop(['Motorcycle Cost'], axis = 1)

    print aggregator_market_motorcycle_list

    aggregator_market_vehicle_cost = aggregator_market_vehicle_cost.append(aggregator_market_motorcycle_list)


    aggregator_market_vehicle_cost = pd.merge(aggregator_market_vehicle_cost, vehicle_quantity_limits, on= ['Vehicle_ID', 'State'])

    return aggregator_market_vehicle_cost

# Returns all the transportation data when only single vehicle was used so that we can know how much quantity was taken in the vehicle.
def get_single_vehicle_data(daily_transportation_data):
    # Find market vists when single vehicle were used and keep only that data from daily_transportation_data
    daily_vehicle_count = daily_transportation_data.groupby(['Date', 'Aggregator', 'Market']).agg(
        {'DT_ID': 'count'}).reset_index()
    daily_vehicle_count = daily_vehicle_count.rename(columns={'DT_ID': 'Vehicle_Count'})
    daily_vehicle_single_count = daily_vehicle_count[daily_vehicle_count['Vehicle_Count'] == 1]
    daily_vehicle_single_data = pd.merge(daily_transportation_data, daily_vehicle_single_count,
                                         on=['Date', 'Aggregator', 'Market'], how='inner')
    daily_vehicle_single_data.loc[(daily_vehicle_single_data['Vehicle_ID'] == 2) & (daily_vehicle_single_data['State'] == 1) & (daily_vehicle_single_data['Quantity'] < 400), 'Vehicle_ID'] = 0
    daily_vehicle_single_data.loc[
        (daily_vehicle_single_data['Vehicle_ID'] == 0) & (daily_vehicle_single_data['State'] == 1), 'Vehicle_Name'] = 'Tempo-Small'
    daily_vehicle_single_data = daily_vehicle_single_data[daily_vehicle_single_data['Vehicle_ID'] != 1]
    return daily_vehicle_single_data

def find_vehicle_quantity_limits(daily_vehicle_single_data):
    # Find minimum quantity for the vehicle (35 percentile) and maximum quantity for the vehicle (75 percentile)
    vehicle_quantity_limits = daily_vehicle_single_data.groupby(['Vehicle_ID', 'Vehicle_Name', 'State'])[
        'Quantity'].quantile(0.35).reset_index()
    vehicle_quantity_limits = vehicle_quantity_limits.rename(columns={'Quantity': 'Quantity_Min'})
    vehicle_quantity_limits_75 = daily_vehicle_single_data.groupby(['Vehicle_ID', 'State'])['Quantity'].quantile(
        0.75).reset_index()
    vehicle_quantity_limits = pd.merge(vehicle_quantity_limits, vehicle_quantity_limits_75, on=['Vehicle_ID', 'State'])
    vehicle_quantity_limits = vehicle_quantity_limits.rename(columns={'Quantity': 'Quantity_Limit'})

    motorcycle = {'Vehicle_ID': [1,], 'Vehicle_Name': ['Motorcycle',], 'State': [1,], 'Quantity_Limit': [150,], 'Quantity_Min': [0,]}
    motorcycle_df = pd.DataFrame(motorcycle)
    vehicle_quantity_limits = vehicle_quantity_limits.append(motorcycle_df)

    # Change quantity limits wherever it is wrong. Hard coded.
    vehicle_quantity_limits.loc[
        (vehicle_quantity_limits['Vehicle_ID'] == 2) & (vehicle_quantity_limits['State'] == 1), 'Quantity_Limit'] = 700
    vehicle_quantity_limits.loc[
        (vehicle_quantity_limits['Vehicle_ID'] == 2) & (vehicle_quantity_limits['State'] == 1), 'Quantity_Min'] = 400
    vehicle_quantity_limits.loc[
        (vehicle_quantity_limits['Vehicle_ID'] == 3) & (vehicle_quantity_limits['State'] == 1), 'Quantity_Limit'] = 1002
    vehicle_quantity_limits.loc[
        (vehicle_quantity_limits['Vehicle_ID'] == 3) & (vehicle_quantity_limits['State'] == 1), 'Quantity_Min'] = 500
    #vehicle_quantity_limits.loc[
    #    (vehicle_quantity_limits['Vehicle_ID'] == 1) & (vehicle_quantity_limits['State'] == 1), 'Quantity_Limit'] = 150
    #vehicle_quantity_limits.loc[
    #    (vehicle_quantity_limits['Vehicle_ID'] == 1) & (vehicle_quantity_limits['State'] == 1), 'Quantity_Min'] = 0
    vehicle_quantity_limits.loc[
        (vehicle_quantity_limits['Vehicle_ID'] == 0) & (vehicle_quantity_limits['State'] == 1), 'Quantity_Limit'] = 400
    vehicle_quantity_limits.loc[
        (vehicle_quantity_limits['Vehicle_ID'] == 0) & (vehicle_quantity_limits['State'] == 1), 'Quantity_Min'] = 150

    print 'Vehicle Quantity Limits'
    print vehicle_quantity_limits
    return vehicle_quantity_limits

    # print vehicle_quantity_limits

# Find transport cost for Aggregator-Market-Vehicle combinations where data is available
def find_transport_cost_amv(daily_vehicle_single_data, vehicle_quantity_limits):
    # Keep only that data in daily_vehicle_single_data where quantity lies in the range of quantity limits
    daily_vehicle_single_data = pd.merge(daily_vehicle_single_data, vehicle_quantity_limits, on=['Vehicle_ID', 'Vehicle_Name', 'State'])
    daily_vehicle_single_data_filtered = daily_vehicle_single_data[(daily_vehicle_single_data['Quantity'] > daily_vehicle_single_data['Quantity_Min']) & (daily_vehicle_single_data['Quantity'] < daily_vehicle_single_data['Quantity_Limit'])]

    # Predicted cost for vehicle for the given Aggregator-Market combination is the median transport cost of filtered data
    aggregator_market_vehicle_cost_detailed = daily_vehicle_single_data_filtered.groupby(['Aggregator', 'Market', 'Vehicle_ID', 'Vehicle_Name', 'State']).agg({'Transport_Cost': ['median'], 'Quantity_Min': ['median'], 'Quantity_Limit': ['median']}).reset_index()
    aggregator_market_vehicle_cost_detailed.columns = aggregator_market_vehicle_cost_detailed.columns.map('_'.join)
    aggregator_market_vehicle_cost_detailed = aggregator_market_vehicle_cost_detailed.rename(columns = {'Aggregator_': 'Aggregator', 'Market_': 'Market', 'Vehicle_ID_': 'Vehicle_ID', 'Vehicle_Name_': 'Vehicle_Name', 'State_': 'State', 'Transport_Cost_median': 'Predicted_TC', 'Quantity_Min_median': 'Quantity_Min', 'Quantity_Limit_median': 'Quantity_Limit'})
    return aggregator_market_vehicle_cost_detailed

# Purpose: If we have data for at least one vehicle for an aggregator-market combination, then this function predicts transport cost for other vehicles for that aggregator-market combination.
# aggregator_market_vehicle_cost: {Aggregator, Market, State, Vehicle_ID, Predicted_TC}
def find_predicted_transport_cost_amv(aggregator_market_vehicle_cost, vehicles_to_fill_na):

    # aggregator_market_vehicle_temp: Outer join between all possible aggregator-market combination and all possible vehicles to get all possible a-m-v combinations
    # A column 'temp' is added in both dataframes to facilitate outer join
    aggregator_market_temp = aggregator_market_vehicle_cost.groupby(['Aggregator', 'Market', 'State']).agg({'Predicted_TC': 'min'}).reset_index()
    aggregator_market_temp['temp'] = 1
    vehicles_to_fill_na['temp'] = 1
    aggregator_market_vehicle_temp = pd.merge(aggregator_market_temp, vehicles_to_fill_na, on= ['temp', 'State'])
    aggregator_market_vehicle_temp = aggregator_market_vehicle_temp.drop(['temp', 'Predicted_TC'], axis = 1)

    # print aggregator_market_vehicle_temp.head()

    # aggregator_market_vehicle_CostNA: Get all those a-m-v combinations for which cost is unknown and to be predicted
    aggregator_market_vehicle_CostNA = pd.merge(aggregator_market_vehicle_temp, aggregator_market_vehicle_cost, on= ['Aggregator', 'Market', 'State', 'Vehicle_ID'], how='left')
    aggregator_market_vehicle_CostNA = aggregator_market_vehicle_CostNA[aggregator_market_vehicle_CostNA['Predicted_TC'].isnull()]
    aggregator_market_vehicle_CostNA = aggregator_market_vehicle_CostNA.rename(columns = {'Vehicle_ID': 'Vehicle_ID_NA'})
    # print  aggregator_market_vehicle_CostNA.head()

    # Each unknown a-m-v is joined to all vehicles of that a-m combination for which cost is known.
    # {Aggregator, Market, State, Vehicle_ID_NA, Vehicle_ID}
    aggregator_market_vehicle_CostNA_CostKnown = pd.merge(aggregator_market_vehicle_CostNA, aggregator_market_vehicle_cost, on= ['Aggregator', 'Market', 'State'])

    # Finds a-m combinations for which we know cost of vehicle combinations created in above row
    # Cross product of aggregator_market_vehicle_cost to find all combinations of vehicles with available data for each Aggregator-Market
    aggregator_market_vehicle_cost_crossed = pd.merge(aggregator_market_vehicle_cost, aggregator_market_vehicle_cost,
                                                      on=['Aggregator', 'Market', 'State'])

    a_m_v_with_similar_cost = pd.merge(aggregator_market_vehicle_CostNA_CostKnown, aggregator_market_vehicle_cost_crossed, left_on= ['Vehicle_ID_NA', 'Vehicle_ID'], right_on= ['Vehicle_ID_x', 'Vehicle_ID_y'])

    # Predicted_TC_x_x: Cost of unknown vehicle for A-M where 1 vehicle was unknown
    # Predicted_TC_y_x: Cost of known vehicle for A-M where 1 vehicle was unknown
    # Predicted_TC_x_y: Cost of unknown vehicle for other A-M combinations where cost was known
    # Predicted_TC_y_y: Cost of known vehicle for other A-M combinations

    # Keeps only those rows where cost lies in the desired range
    a_m_v_with_similar_cost = a_m_v_with_similar_cost[(a_m_v_with_similar_cost['Predicted_TC_y_y'] > 0.5 * a_m_v_with_similar_cost['Predicted_TC_y_x'])& (a_m_v_with_similar_cost['Predicted_TC_y_y'] < 1.5 * a_m_v_with_similar_cost['Predicted_TC_y_x'])]


    # Uses data of other a-m-v combination to find transport cost for a-m-v combinations where rates were unknown
    a_m_v_c_na_merged_with_crossed_grouped = a_m_v_with_similar_cost.groupby(['Aggregator_x', 'Market_x', 'State_x', 'Vehicle_ID_NA', 'Vehicle_ID', 'Predicted_TC_y_x']).agg({'Predicted_TC_x_y': 'sum', 'Predicted_TC_y_y': 'sum', 'Vehicle_ID_y': 'count'}).reset_index()
    a_m_v_c_na_merged_with_crossed_grouped = a_m_v_c_na_merged_with_crossed_grouped.rename(columns = {'Aggregator_x': 'Aggregator', 'Market_x': 'Market', 'State_x': 'State', 'Vehicle_ID_y': 'Count'})

    # Predicted_TC_NA is the cost for unknown vehicle predicted by this unknown-known vehicle combination
    a_m_v_c_na_merged_with_crossed_grouped['Predicted_TC_NA'] = (a_m_v_c_na_merged_with_crossed_grouped['Predicted_TC_y_x'] * a_m_v_c_na_merged_with_crossed_grouped['Predicted_TC_x_y']) /a_m_v_c_na_merged_with_crossed_grouped['Predicted_TC_y_y']

    a_m_v_c_na_merged_with_crossed_grouped['Predicted_TC_NA*Count'] = a_m_v_c_na_merged_with_crossed_grouped['Predicted_TC_NA'] * a_m_v_c_na_merged_with_crossed_grouped['Count']

    aggregator_market_vehicle_cost_na_final = a_m_v_c_na_merged_with_crossed_grouped.groupby(['Aggregator', 'Market', 'State', 'Vehicle_ID_NA']).agg({'Predicted_TC_NA*Count': 'sum', 'Count': 'sum'}).reset_index()

    # Predicted_Cost_Final is the final cost for this vehicle.
    aggregator_market_vehicle_cost_na_final['Predicted_Cost_Final'] = aggregator_market_vehicle_cost_na_final['Predicted_TC_NA*Count'] / aggregator_market_vehicle_cost_na_final['Count']
    aggregator_market_vehicle_cost_na_final = aggregator_market_vehicle_cost_na_final.drop(['Count', 'Predicted_TC_NA*Count'], axis = 1)
    aggregator_market_vehicle_cost_na_final = aggregator_market_vehicle_cost_na_final.rename(columns= {'Predicted_Cost_Final': 'Predicted_TC', 'Vehicle_ID_NA': 'Vehicle_ID'})
    return aggregator_market_vehicle_cost_na_final
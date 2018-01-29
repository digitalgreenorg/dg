import pandas as pd
import numpy as np
from datetime import timedelta


def fill_transport_data(daily_aggregator_market_data, daily_transaction_corrected_data):
    daily_aggregator_market_data_temp = daily_aggregator_market_data[['Date', 'Aggregator', 'Market', 'TCPK', 'FSPK']]
    daily_transaction_corrected_data = pd.merge(daily_transaction_corrected_data, daily_aggregator_market_data_temp, on= ['Date', 'Aggregator', 'Market'])
    daily_transaction_corrected_data['Transport_Cost'] = daily_transaction_corrected_data['Quantity'] * daily_transaction_corrected_data['TCPK']
    daily_transaction_corrected_data['Farmer_Share'] = daily_transaction_corrected_data['Quantity'] * daily_transaction_corrected_data['FSPK']
    return daily_transaction_corrected_data

# Returns the market where aggregator has sold maximum produce in first 30 days.
# TODO: Check the ratio of produce sold in local market to the total quantity sold in 30 days. Put some minimum threshold on this ratio.
# TODO: Put some minimum threshold on number of market visits in first thirty days.
# TODO: Instead of 30 days as the filter, keep # market visits as the filter.

def get_aggregator_local_market(daily_aggregator_market_data):
    aggregator_first_date = daily_aggregator_market_data.groupby(['Aggregator']).agg({'Date': 'min'}).reset_index()
    aggregator_first_date = aggregator_first_date.rename(columns={'Date': 'First_Date'})

    daily_aggregator_market_data = pd.merge(daily_aggregator_market_data, aggregator_first_date, on=['Aggregator'])

    daily_aggregator_market_data = daily_aggregator_market_data[
        (daily_aggregator_market_data['Date'] - daily_aggregator_market_data['First_Date']) <= timedelta(days=30)]

    aggregator_local_market_data = daily_aggregator_market_data.groupby(['Aggregator', 'Market']).agg(
        {'Quantity': 'sum'}).reset_index()

    aggregator_first_month_data = daily_aggregator_market_data.groupby(['Aggregator']).agg(
        {'Quantity': 'sum'}).reset_index()
    aggregator_first_month_data = aggregator_first_month_data.rename(columns={'Quantity': 'Total_Quantity'})

    aggregator_local_market = aggregator_local_market_data.groupby(['Aggregator']).agg(
        {'Quantity': 'max'}).reset_index()
    aggregator_local_market = pd.merge(aggregator_local_market, aggregator_local_market_data,
                                       on=['Aggregator', 'Quantity'])
    aggregator_local_market = pd.merge(aggregator_local_market, aggregator_first_month_data, on=['Aggregator'])
    aggregator_local_market = aggregator_local_market.rename(columns={'Market': 'Local_Market'})
    aggregator_local_market = aggregator_local_market[['Aggregator', 'Local_Market']]

    return aggregator_local_market

# Finds rate for Date-Aggregator-Crop combination in local market. If market is same as local market, then rate is unchanged.
def fill_local_market_rate(daily_market_crop_data, daily_transaction_data, aggregator_local_market):
    daily_market_crop_data = daily_market_crop_data.rename(columns = {'Av_Ratemean': 'Predicted_Rate'})

    daily_aggregator_crop_data = daily_transaction_data.groupby(['Date', 'Aggregator', 'Crop']).agg({'Quantity': ['sum']}).reset_index()
    daily_aggregator_crop_data.columns = daily_aggregator_crop_data.columns.droplevel(1)

    daily_transaction_data = pd.merge(daily_transaction_data, aggregator_local_market, on= ['Aggregator'])
    daily_transaction_data = pd.merge(daily_transaction_data, daily_market_crop_data, how= 'left', left_on= ['Date', 'Crop', 'Local_Market'], right_on= ['Date', 'Crop', 'Market'])
    daily_transaction_data.loc[daily_transaction_data['Market_x'] == daily_transaction_data['Local_Market'], 'Predicted_Rate'] = daily_transaction_data['Price']
    daily_transaction_data['Predicted_Amount'] = daily_transaction_data['Quantity'] * daily_transaction_data['Predicted_Rate']
    daily_transaction_data = daily_transaction_data.drop(['Market_y', 'STDmean', 'Pricemax', 'Pricemin', 'Total_Quantitysum'], axis = 1)
    daily_transaction_data = daily_transaction_data.rename(columns= {'Market_x': 'Market'})
    return daily_transaction_data

# If vehicle was not used, then NA or next vehicle?
def find_predicted_cost(daily_farmer_quantity_data, aggregator_local_market, aggregator_market_vehicle_predicted_cost_quantity):

    # Finds vehicle whose quantity_limit > farmer_quantity for the day
    # Assigns this vehicle to this Date-Farmer combination and insert the cost for local market

    daily_farmer_quantity_data_temp = pd.merge(daily_farmer_quantity_data, aggregator_local_market, how='inner', on= ['Aggregator'])
    daily_farmer_quantity_data_temp = pd.merge(daily_farmer_quantity_data_temp, aggregator_market_vehicle_predicted_cost_quantity, how='inner', left_on= ['Aggregator', 'Local_Market'], right_on= ['Aggregator', 'Market'])
    daily_farmer_quantity_data_temp = daily_farmer_quantity_data_temp[daily_farmer_quantity_data_temp['Farmer_Quantity'] <= daily_farmer_quantity_data_temp['Quantity_Limit']]
    daily_farmer_quantity_data_temp_1 = daily_farmer_quantity_data_temp.groupby(['Date', 'Aggregator', 'Farmer']).agg({'Quantity_Limit': ['min']}).reset_index()
    daily_farmer_quantity_data_temp_1.columns = daily_farmer_quantity_data_temp_1.columns.droplevel(1)
    daily_farmer_quantity_data_temp = pd.merge(daily_farmer_quantity_data_temp, daily_farmer_quantity_data_temp_1, on= ['Date', 'Aggregator', 'Farmer', 'Quantity_Limit'])
    daily_farmer_quantity_data_temp = daily_farmer_quantity_data_temp[['Date', 'Aggregator', 'Farmer', 'Quantity_Limit', 'Local_Market', 'Vehicle_ID', 'Predicted_TC', 'Vehicle_Name']]
    daily_farmer_quantity_data = pd.merge(daily_farmer_quantity_data, daily_farmer_quantity_data_temp, on=['Date', 'Aggregator', 'Farmer'])

    # If quantity is less than 150 Kgs, then make vehicles as motorcycle and cost = Rs. 60
    daily_farmer_quantity_data.loc[daily_farmer_quantity_data['Farmer_Quantity'] <= 150, 'Predicted_TC'] = 60
    daily_farmer_quantity_data.loc[daily_farmer_quantity_data['Farmer_Quantity'] <= 150, 'Vehicle_ID'] = 1
    daily_farmer_quantity_data.loc[daily_farmer_quantity_data['Farmer_Quantity'] <= 150, 'Vehicle_Name'] = 'Motor Cycle'
    daily_farmer_quantity_data.loc[daily_farmer_quantity_data['Farmer_Quantity'] <= 150, 'Quantity_Limit'] = 150

    # daily_farmer_quantity_data['Predicted_TCPK'] = daily_farmer_quantity_data['Predicted_TC'] / daily_farmer_quantity_data['Farmer_Quantity']

    # If farmer's quantity < 0.85 * quantity_limit, then it will fill vehicle to 85%. If not, then it will fill completely. TCPK & Predicted_TC is changed accordingly.
    daily_farmer_quantity_data.loc[daily_farmer_quantity_data['Farmer_Quantity'] < 0.85 * daily_farmer_quantity_data['Quantity_Limit'], 'Predicted_TCPK'] = daily_farmer_quantity_data['Predicted_TC'] / (0.85* daily_farmer_quantity_data['Quantity_Limit'])
    daily_farmer_quantity_data.loc[daily_farmer_quantity_data['Farmer_Quantity'] >= 0.85 * daily_farmer_quantity_data[
        'Quantity_Limit'], 'Predicted_TCPK'] = daily_farmer_quantity_data['Predicted_TC'] / daily_farmer_quantity_data['Farmer_Quantity']
    daily_farmer_quantity_data['Predicted_TC'] = daily_farmer_quantity_data['Predicted_TCPK'] * daily_farmer_quantity_data['Farmer_Quantity']
    return daily_farmer_quantity_data

def fill_predicted_cost(daily_farmer_quantity_data, daily_transaction_corrected_data):
    # Add predicted_tcpk and corresponding predicted_tc in daily_transaction_data
    daily_transaction_corrected_data = pd.merge(daily_transaction_corrected_data, daily_farmer_quantity_data, on=['Date', 'Aggregator', 'Farmer'])
    daily_transaction_corrected_data = daily_transaction_corrected_data.drop(['Quantity_Limit', 'Vehicle_ID', 'Vehicle_Name', 'Local_Market_y'], axis= 1)
    daily_transaction_corrected_data = daily_transaction_corrected_data.rename(columns= {'Local_Market_x': 'Local_Market'})
    daily_transaction_corrected_data['Predicted_TC'] = daily_transaction_corrected_data['Quantity'] * daily_transaction_corrected_data['Predicted_TCPK']
    return daily_transaction_corrected_data

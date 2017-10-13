import datetime, time
import pandas as pd
import numpy as np
from operator import itemgetter
from loop.utils.loop_etl.aggregation_methods import *
from loop.dashboard.database_operations import *

def volume_amount_farmers_ts(**kwargs):
    result_data = {}
    df_result = query_myisam(**kwargs)
    try:
        df_result = df_result.groupby(['date'])['quantity','amount'].sum().reset_index()
        df_result['date'] = df_result['date'].astype('datetime64[ns]')
        df_result['date_time'] = df_result['date'].astype('int64')//10**6

        df_number_of_farmers = get_farmers_per_day(**kwargs)
        df_number_of_farmers['date'] = df_number_of_farmers['date'].astype('datetime64[ns]')
        df_number_of_farmers['date_time'] = df_number_of_farmers['date'].astype('int64')//10**6

        data_vol = []
        data_amount = []
        data_farmers = []
        for index, row in df_result.iterrows():
            data_vol.append([row['date_time'],row['quantity']])
            # data_amount.append([row['date_time'],row['amount']])
        for index, row in df_number_of_farmers.iterrows():
            data_farmers.append([row['date_time'],row['farmer_count']])

        result_data['chartName'] = "volFarmerTS"
        result_data['chartType'] = "StockChart"
        result_data['data'] = []
        volume = {}
        volume['data'] = data_vol
        volume['name'] = 'Volume'
        volume['yAxis'] = 0
        volume['type'] = 'areaspline'
        farmers = {}
        farmers['data'] = data_farmers
        farmers['name'] = 'Farmers'
        farmers['yAxis'] = 1
        farmers['type'] = 'column'
        result_data['data'].append(volume)
        result_data['data'].append(farmers)
    # result_data = [data_vol,data_amount]
    except:
        result_data["error"] = "No data found"
    return result_data

def cpk_spk_ts(**kwargs):
    result_data = {}

    df_result = query_myisam(**kwargs)
    try:
        df_result = df_result.groupby(['date','aggregator_id','mandi_id']).agg(cpk_spk_aggregation).reset_index()
        df_result.columns = df_result.columns.droplevel(1)
        df_result.drop(['aggregator_id','mandi_id'], axis=1,inplace=True)
        df_result = df_result.groupby(['date']).sum().reset_index()
        df_result['cpk'] = (df_result['aggregator_incentive'] + df_result['transportation_cost'])/df_result['quantity']
        df_result['spk'] = (df_result['farmer_share'] + df_result['gaddidar_share'])/df_result['quantity']
        df_result['date'] = df_result['date'].astype('datetime64[ns]')
        df_result['date_time'] = df_result['date'].astype('int64')//10**6

        data_cpk = []
        data_spk = []
        for index, row in df_result.iterrows():
            data_cpk.append([row['date_time'],row['cpk']])
            data_spk.append([row['date_time'],row['spk']])

        result_data['chartName'] = "cpkSpkTS"
        result_data['chartType'] = "StockChart"
        result_data['data'] = []
        cpk = {}
        cpk['data'] = data_cpk
        cpk['name'] = 'CPK'
        # cpk['yAxis'] = 0
        spk = {}
        spk['data'] = data_spk
        spk['name'] = 'SPK'
        # spk['yAxis'] = 1
        result_data['data'].append(cpk)
        result_data['data'].append(spk)
    except:
        result_data["error"] = "No data found"
    return result_data

def crop_price_range_ts(**kwargs):
    df_result = crop_prices_query(from_timeseries=1,**kwargs)
    final_data_list = {}
    df_result['date'] = df_result['date'].astype('datetime64[ns]')
    df_result['date'] = df_result['date'].astype('int64')//10**6
    df_result = df_result.set_index('crop_id')

    for index, row in df_result.iterrows():
        if str(index) not in final_data_list:
            final_data_list[str(index)] = []
            final_data_list[str(index)].extend([{}])
            final_data_list[str(index)][0]['data'] = []
            final_data_list[str(index)][0]['name'] = row['crop_name']
            final_data_list[str(index)][0]['yAxis'] = 0

        final_data_list[str(index)][0]['data'].append([row['date'],row['Avg_price'],row['Max_price'],row['Min_price'],row['Avg_price']])#,row['Min_price'],row['Avg_price']

    result_data = {}
    result_data['chartName'] = "crop_price_range_ts"
    result_data['chartType'] = "StockChart"
    result_data['data'] = final_data_list
    return result_data

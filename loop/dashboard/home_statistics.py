import datetime, time
import pandas as pd
import numpy as np
from operator import itemgetter
from loop.constants.constants import *
from loop.models import CombinedTransaction
from loop.utils.loop_etl.aggregation_methods import *
from loop.utils.utility import get_init_sql_ds, join_sql_ds
from loop.dashboard.database_operations import *
from loop.dashboard.utility_methods import *

def get_grouped_data(df_result_aggregate,day,df_farmers):
    start_date = df_result_aggregate['date'].min()
    # end_date = df_result_aggregate['date'].max()
    end_date = datetime.datetime.today()
    frequency = '-' + day + 'D'
    data_by_grouped_days = pd.DataFrame(pd.date_range(end_date,start_date,freq=frequency),columns={'start_date'})
    data_by_grouped_days['end_date'] = data_by_grouped_days['start_date'].shift(-1)
    data_by_grouped_days.fillna(value=0,inplace=True,axis=1)

    df_result_aggregate['date'] = df_result_aggregate['date'].astype('datetime64[ns]')
    for index,row in data_by_grouped_days.iterrows():
        end_date = row['end_date']
        start_date = row['start_date']

        data =  pd.Series(pd.DataFrame(df_result_aggregate.where((df_result_aggregate['date'] > end_date) & (df_result_aggregate['date'] <= start_date))).sum(numeric_only=True))

        data_by_grouped_days.loc[index,'amount__sum'] = round(data['amount'])
        data_by_grouped_days.loc[index,'quantity__sum'] = round(data['quantity'])
        data_by_grouped_days.loc[index,'farmer_share__sum'] = data['farmer_share']
        data_by_grouped_days.loc[index,'transportation_cost__sum'] = data['transportation_cost']
        data_by_grouped_days.loc[index,'gaddidar_share__sum'] = data['gaddidar_share']
        data_by_grouped_days.loc[index,'aggregator_incentive__sum'] = data['aggregator_incentive']

        data_by_grouped_days.loc[index,'active_cluster'] = df_result_aggregate.where((df_result_aggregate['date'] > end_date) & (df_result_aggregate['date'] <= start_date))['aggregator_id'].nunique()

        data_by_grouped_days.loc[index,'distinct_farmer_count'] = df_farmers.where((df_farmers['date'] > end_date) & (df_farmers['date']<=start_date))['farmer_id'].nunique()
        data_by_grouped_days.loc[index, 'cpk'] = (data['transportation_cost'] + data['aggregator_incentive']) / data['quantity']
        data_by_grouped_days.loc[index, 'spk'] = (data['gaddidar_share'] + data['farmer_share']) / (data['transportation_cost'] + data['aggregator_incentive']) * 100
    data_by_grouped_days = data_by_grouped_days.round(2)
    data_by_grouped_days = data_by_grouped_days.to_dict(orient='index')
    return data_by_grouped_days

def get_data_from_myisam(get_total, **kwargs):
    df_result = query_myisam(**kwargs)
    country_id, state_id, start_date, end_date, aggregators_list, mandis_list, crops_list, gaddidars_list, district_list = read_kwargs(kwargs)
    aggregations = {
        'quantity':{
            'quantity__sum':'sum'
        },
        'amount':{
            'amount__sum':'sum'
        },
        'gaddidar_share':{
            'gaddidar_share__sum':'sum'
        },
        'aggregator_incentive':{
            'aggregator_incentive__sum':'mean'
        },
        'transportation_cost':{
            'transportation_cost__sum':'mean'
        },
        'farmer_share':{
            'farmer_share__sum':'mean'
        }
    }

    # aggregate_cumm_vol_farmer = {
    #     'quantity':{
    #         'quantity__sum':'sum'
    #     },
    #     'cum_distinct_farmer':{
    #         'cum_vol_farmer':'mean'
    #     }
    # }
    cumm_vol_farmer = {}
    dictionary = {}
    try:
        if( len(df_result) > 0) :
        # MyISAM table contains CT, DT, Gaddidar, AggregatorIncentive.
            df_result_aggregate = df_result.groupby(['date','aggregator_id','mandi_id']).agg(aggregations).reset_index()
            df_result_aggregate.columns = df_result_aggregate.columns.droplevel(1)
        else :
            df_result_aggregate = df_result.astype(int).groupby(['date','aggregator_id','mandi_id']).agg(aggregations).reset_index()
            df_result_aggregate.columns = df_result_aggregate.columns.droplevel(1)

        if get_total == 0:
            #df_farmers = pd.DataFrame(list(CombinedTransaction.objects.values('date','farmer_id').order_by('date')))
            combinedTransactionData = CombinedTransaction.objects.filter(mandi__district__state__country=country_id)

            if(state_id) :
                combinedTransactionData = combinedTransactionData.filter(mandi__district__state=state_id)
            df_farmers = pd.DataFrame(list(combinedTransactionData.values('date','farmer_id').order_by('date')))
            df_farmers['date'] = df_farmers['date'].astype('datetime64[ns]')

            days = ['15','30','60']
            for day in days:
                data_by_grouped_days = get_grouped_data(df_result_aggregate,day,df_farmers)
                dictionary[day] = list(data_by_grouped_days.values())

            # Calcualting cummulative volume and farmer count
            # df_cum_vol_farmer = df_result.groupby('date').agg(aggregate_cumm_vol_farmer).reset_index()
            # df_cum_vol_farmer.columns = df_cum_vol_farmer.columns.droplevel(1)
            # df_cum_vol_farmer['cum_vol'] = df_cum_vol_farmer['quantity'].cumsum().round()
            # df_cum_vol_farmer.drop('quantity',axis=1,inplace=True);
            # cumm_vol_farmer = df_cum_vol_farmer.to_dict(orient='index')
        else:
            df_result_aggregate.drop(['mandi_id','aggregator_id'],axis=1,inplace=True)
            df = pd.DataFrame(df_result_aggregate.sum(numeric_only=True))
            dictionary = df.to_dict(orient='index')

    except Exception as e:
        print 'Exception : ', e
    return dictionary#, cumm_vol_farmer

def get_cummulative_vol_farmer(**kwargs):
    aggregate_cumm_vol_farmer = {
        'quantity':{
            'quantity__sum': 'sum'
        }
        ,
        'new_distinct_farmer':{
            'cum_vol_farmer': 'mean'
        }
    }
    agg_vol_farmer = {
        'quantity': 'sum',
        # 'new_distinct_farmer': 'mean'
    }
    result_data = {}
    df_result = query_myisam(**kwargs)
    try:
        df_cum_vol_farmer = df_result.groupby(['date','country_id','state_id']).agg(aggregate_cumm_vol_farmer).reset_index()
        df_cum_vol_farmer.columns = df_cum_vol_farmer.columns.droplevel(1)

        df_cum_vol_farmer['cum_distinct_farmer'] = df_cum_vol_farmer['new_distinct_farmer'].cumsum()
        df_cum_vol = df_cum_vol_farmer.groupby('date').agg(agg_vol_farmer).reset_index()

        df_cum_vol['cum_vol'] = df_cum_vol['quantity'].cumsum().round()
        # df_cum_vol_farmer['cum_distinct_farmer'] = df_cum_vol_farmer['new_distinct_farmer'].cumsum()

        df_cum_vol.drop('quantity',axis=1,inplace=True)
        df_cum_vol_farmer['date'] = df_cum_vol_farmer['date'].astype('datetime64[ns]')
        df_cum_vol_farmer['date_time'] = df_cum_vol_farmer['date'].astype('int64')//10**6

        df_cum_vol['date'] = df_cum_vol['date'].astype('datetime64[ns]')
        df_cum_vol['date_time'] = df_cum_vol['date'].astype('int64')//10**6

        data_farmers = []
        data_vol = []

        for index, row in df_cum_vol.iterrows():
            data_vol.append([row['date_time'],row['cum_vol']])

        for index, row in df_cum_vol_farmer.iterrows():
            # data_vol.append([row['date_time'],row['cum_vol']])
            data_farmers.append([row['date_time'],row['cum_distinct_farmer']])

        result_data['chartName'] = "cummulativeCount"
        result_data['chartType'] = "StockChart"
        result_data['data'] = []
        vol = {}
        vol['data'] = data_vol
        vol['name'] = 'Volume'
        vol['yAxis'] = 0
        farmer = {}
        farmer['data'] = data_farmers
        farmer['name'] = 'Farmers'
        farmer['yAxis'] = 1
        result_data['data'].append(vol)
        result_data['data'].append(farmer)
    except:
        result_data["error"] = "No data found"

    return result_data

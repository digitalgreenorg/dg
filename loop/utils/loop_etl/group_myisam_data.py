from dg.settings import DATABASES
import MySQLdb
import datetime, time
import pandas as pd
import numpy as np
from loop.models import CombinedTransaction

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

        data_by_grouped_days.loc[index,'amount__sum'] = data['amount']
        data_by_grouped_days.loc[index,'quantity__sum'] = data['quantity']
        data_by_grouped_days.loc[index,'farmer_share__sum'] = data['farmer_share']
        data_by_grouped_days.loc[index,'transportation_cost__sum'] = data['transportation_cost']
        data_by_grouped_days.loc[index,'gaddidar_share__sum'] = data['gaddidar_share']
        data_by_grouped_days.loc[index,'aggregator_incentive__sum'] = data['transportation_cost']

        data_by_grouped_days.loc[index,'active_cluster'] = df_result_aggregate.where((df_result_aggregate['date'] > end_date) & (df_result_aggregate['date'] <= start_date))['aggregator_id'].nunique()

        data_by_grouped_days.loc[index,'distinct_farmer_count'] = df_farmers.where((df_farmers['date'] > end_date) & (df_farmers['date']<=start_date))['farmer_id'].nunique()
        data_by_grouped_days.loc[index, 'cpk'] = (data['transportation_cost'] + data['transportation_cost']) / data['quantity']
        data_by_grouped_days.loc[index, 'spk'] = (data['gaddidar_share'] + data['farmer_share']) / data['quantity']
    data_by_grouped_days = data_by_grouped_days.round(2)
    data_by_grouped_days = data_by_grouped_days.to_dict(orient='index')
    return data_by_grouped_days

def query_myisam(country_id, from_date=None, to_date=None):
    database = DATABASES['default']['NAME']
    username = DATABASES['default']['USER']
    password = DATABASES['default']['PASSWORD']
    host = DATABASES['default']['HOST']
    port = DATABASES['default']['PORT']
    mysql_cn = MySQLdb.connect(host=host, port=port, user=username, passwd=password, db=database, charset='utf8', use_unicode=True)

    query = "SELECT * FROM loop_aggregated_myisam where country_id = " + str(country_id)
    if from_date:
        query = query + " and date between " + str(from_date) + " and " + str(to_date)

    df_result = pd.read_sql(query, con=mysql_cn)
    return df_result

def get_data_from_myisam(get_total, country_id):
    df_result = query_myisam(country_id)

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

    aggregate_cumm_vol_farmer = {
        'quantity':{
            'quantity__sum':'sum'
        },
        'cum_distinct_farmer':{
            'cum_vol_farmer':'mean'
        }
    }

    # MyISAM table contains CT, DT, Gaddidar, AggregatorIncentive.
    df_result_aggregate = df_result.groupby(['date','aggregator_id','mandi_id']).agg(aggregations).reset_index()
    df_result_aggregate.columns = df_result_aggregate.columns.droplevel(1)

    cumm_vol_farmer = {}
    if get_total == 0:
        #df_farmers = pd.DataFrame(list(CombinedTransaction.objects.values('date','farmer_id').order_by('date')))
        df_farmers = pd.DataFrame(list(CombinedTransaction.objects.filter(mandi__district__state__country=country_id).values('date','farmer_id').order_by('date')))
        df_farmers['date'] = df_farmers['date'].astype('datetime64[ns]')

        dictionary = {}
        days = ['15','30','60']
        for day in days:
            data_by_grouped_days = get_grouped_data(df_result_aggregate,day,df_farmers)
            dictionary[day] = list(data_by_grouped_days.values())

        # Calcualting cummulative volume and farmer count
        df_cum_vol_farmer = df_result.groupby('date').agg(aggregate_cumm_vol_farmer).reset_index()
        df_cum_vol_farmer.columns = df_cum_vol_farmer.columns.droplevel(1)
        df_cum_vol_farmer['cum_vol'] = df_cum_vol_farmer['quantity'].cumsum().round()
        df_cum_vol_farmer.drop('quantity',axis=1,inplace=True);
        cumm_vol_farmer = df_cum_vol_farmer.to_dict(orient='index')
    else:
        df_result_aggregate.drop(['mandi_id','aggregator_id'],axis=1,inplace=True)
        df = pd.DataFrame(df_result_aggregate.sum(numeric_only=True))
        dictionary = df.to_dict(orient='index')
    return dictionary, cumm_vol_farmer

def get_volume_aggregator(country_id):
    result_data = {}
    df_result = query_myisam(country_id)
    aggregation = {
        'quantity':{
            'quantity__sum':'sum'
        },
        # 'mandi_id':{
        #     'mandi_id_count':'count'
        # }
    }
    df_result = df_result.groupby(['aggregator_id','aggregator_name','mandi_id','mandi_name']).agg(aggregation).reset_index()
    df_result.columns = df_result.columns.droplevel(1)
    try:
        df_agg_quantity = df_result.groupby(['aggregator_id','aggregator_name']).agg(aggregation).reset_index()
        df_agg_quantity.columns = df_agg_quantity.columns.droplevel(1)
        df_agg_quantity.drop(['aggregator_id'],axis=1,inplace=True)
        df_agg_quantity.rename(columns={"aggregator_name":"name","quantity":"y"},inplace=True)
        df_agg_quantity['drilldown'] = df_agg_quantity['name'] + " volume"
        outer_data = {'outerData':{'series':[{"data":df_agg_quantity.to_dict(orient="record")}],'catergories':df_agg_quantity['name'].tolist()}}
        inner_data = {'innerData': []}
        vol_agg_mandi_dict = {name:dict(zip(g['mandi_name'],g['quantity'])) for name,g in df_result.groupby('aggregator_name')}
        for key,value in vol_agg_mandi_dict.iteritems():
            temp_dict_inner = {'data':[]}
            temp_dict_inner['name'] = key
            temp_dict_inner['id'] = key + ' volume'
            for k, v in value.iteritems():
                temp_dict_inner['data'].append([k,v])
            inner_data['innerData'].append(temp_dict_inner)
        result_data['volume_per_aggregator'] = outer_data
        result_data['volume_per_aggregator'].update(inner_data)
    except Exception as e:
        print e
    return result_data

def volume_amount_farmers_ts(country_id, from_date, to_date):
    result_data = {}
    df_result = query_myisam(country_id, from_date, to_date)
    df_result = df_result.groupby(['date'])['quantity','amount'].sum().reset_index()
    df_result['date'] = df_result['date'].astype('datetime64[ns]')
    df_result['date_time'] = df_result['date'].astype('int64')//10**6
    data_vol = []
    data_amount = []
    for index, row in df_result.iterrows():
        data_vol.append([row['date_time'],row['quantity']])
        data_amount.append([row['date_time'],row['amount']])
    result_data['chartName'] = "volFarmerTS"
    result_data['chartType'] = "StockChart"
    result_data['data'] = []
    volume = {}
    volume['data'] = data_vol
    volume['name'] = 'Volume'
    amount = {}
    amount['data'] = data_amount
    amount['name'] = 'Amount'
    result_data['data'].append(volume)
    result_data['data'].append(amount)
    # result_data = [data_vol,data_amount]
    return result_data

def cpk_spk_ts(country_id, from_date, to_date):
    result_data = {}
    aggregation = {
        'transportation_cost':{
            'transportation_cost__sum':'mean'
        },
        'farmer_share':{
            'farmer_share__sum':'mean'
        },
        'aggregator_incentive':{
            'aggregator_incentive__sum':'mean'
        },
        'gaddidar_share':{
            'gaddidar_share__sum':'sum'
        },
        'quantity':{
            'quantity__sum':'sum'
        }
    }
    df_result = query_myisam(country_id, from_date, to_date)
    df_result = df_result.groupby(['date','aggregator_id','mandi_id']).agg(aggregation).reset_index()
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
    spk = {}
    spk['data'] = data_spk
    spk['name'] = 'SPK'
    result_data['data'].append(cpk)
    result_data['data'].append(spk)

    return result_data

def get_cummulative_vol_farmer(country_id):
    aggregate_cumm_vol_farmer = {
        'quantity':{
            'quantity__sum':'sum'
        },
        'cum_distinct_farmer':{
            'cum_vol_farmer':'mean'
        }
    }
    result_data = {}
    df_result = query_myisam(country_id)
    df_cum_vol_farmer = df_result.groupby('date').agg(aggregate_cumm_vol_farmer).reset_index()
    df_cum_vol_farmer.columns = df_cum_vol_farmer.columns.droplevel(1)
    df_cum_vol_farmer['cum_vol'] = df_cum_vol_farmer['quantity'].cumsum().round()
    df_cum_vol_farmer.drop('quantity',axis=1,inplace=True)
    df_cum_vol_farmer['date'] = df_cum_vol_farmer['date'].astype('datetime64[ns]')
    df_cum_vol_farmer['date_time'] = df_cum_vol_farmer['date'].astype('int64')//10**6

    data_farmers = []
    data_vol = []
    for index, row in df_cum_vol_farmer.iterrows():
        data_vol.append([row['date_time'],row['cum_vol']])
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

    return result_data

def aggregator_volume(country_id, start_date, end_date):
    

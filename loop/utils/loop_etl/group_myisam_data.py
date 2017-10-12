from dg.settings import DATABASES
import MySQLdb
import datetime, time
import pandas as pd
import numpy as np
from operator import itemgetter
from loop.utils.loop_etl.aggregation_methods import *
from loop.models import CombinedTransaction
from loop.utils.utility import get_init_sql_ds, join_sql_ds
from loop.constants.constants import *

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
        data_by_grouped_days.loc[index, 'spk'] = (data['gaddidar_share'] + data['farmer_share']) / (data['transportation_cost'] + data['aggregator_incentive'])
    data_by_grouped_days = data_by_grouped_days.round(2)
    data_by_grouped_days = data_by_grouped_days.to_dict(orient='index')
    return data_by_grouped_days

def sql_query(**kwargs):
    country_id, state_id, start_date, end_date, aggregators_list, mandis_list, crops_list, gaddidars_list = read_kwargs(kwargs)
    database = DATABASES['default']['NAME']
    username = DATABASES['default']['USER']
    password = DATABASES['default']['PASSWORD']
    host = DATABASES['default']['HOST']
    port = DATABASES['default']['PORT']
    mysql_cn = MySQLdb.connect(host=host, port=port, user=username, passwd=password, db=database, charset='utf8', use_unicode=True)

    sql_ds = get_init_sql_ds()
    sql_ds['select'].append('lct.user_created_id aggregator_id, lu.name_en aggregator_name, date, crop_id, crop_name, mandi_id,\
                    mandi_name_en mandi_name, quantity, farmer_id, lf.name farmer_name')
    sql_ds['from'].append('loop_combinedtransaction lct')
    sql_ds['join'].append(['loop_mandi lm', 'lm.id = lct.mandi_id'])
    sql_ds['join'].append(['loop_crop lcrp', 'lcrp.id = lct.crop_id'])
    sql_ds['join'].append(['loop_farmer lf', 'lf.id = lct.farmer_id'])
    sql_ds['join'].append(['loop_loopuser lu', 'lu.user_id = lct.user_created_id and lu.role = ' + str(ROLE_CHOICE_AGGREGATOR)])
    sql_ds['join'].append(['loop_district ld', 'ld.id = lm.district_id'])
    sql_ds['join'].append(['loop_state ls', 'ls.id = ld.state_id'])
    sql_ds['join'].append(['loop_country lc', 'lc.id = ls.country_id'])

    if len(aggregators_list) > 0:
        sql_ds['where'].append('lct.user_created_id in (' + ",".join(aggregators_list) + ")")
    if len(mandis_list) > 0:
        sql_ds['where'].append('lm.id in (' + ",".join(mandis_list) + ')')
    # if len(gaddidars_list) > 0:
    #     sql_ds['where'].append('gaddidar_id in (' + ",".join(gaddidars_list) + ')')

    if len(crops_list) > 0:
        sql_ds['where'].append('lcrp.id in (' + ",".join(crops_list) + ')')
    sql_ds['where'].append('lct.date between \'' + start_date + '\' and \'' + end_date + '\'')
    sql_ds['where'].append('country_id = ' + str(country_id))
    if(state_id) :
        sql_ds['where'].append('state_id = ' + str(state_id))

    query = join_sql_ds(sql_ds)
    df_result = pd.read_sql(query, con=mysql_cn)
    return df_result

def query_myisam(**kwargs):
    database = DATABASES['default']['NAME']
    username = DATABASES['default']['USER']
    password = DATABASES['default']['PASSWORD']
    host = DATABASES['default']['HOST']
    port = DATABASES['default']['PORT']
    mysql_cn = MySQLdb.connect(host=host, port=port, user=username, passwd=password, db=database, charset='utf8', use_unicode=True)

    # Constructing sql query
    sql_ds = get_init_sql_ds()
    sql_ds['select'].append('*')
    sql_ds['from'].append('loop_aggregated_myisam')
    sql_q = join_sql_ds(sql_ds)
    if(len(kwargs) > 0):
        country_id, state_id, start_date, end_date, aggregators_list, mandis_list, crops_list, gaddidars_list = read_kwargs(kwargs)
        if len(aggregators_list) > 0:
            sql_ds['where'].append('aggregator_id in (' + ",".join(aggregators_list) + ")")
        if len(mandis_list) > 0:
            sql_ds['where'].append('mandi_id in (' + ",".join(mandis_list) + ')')
        if len(gaddidars_list) > 0:
            sql_ds['where'].append('gaddidar_id in (' + ",".join(gaddidars_list) + ')')
        if start_date != None:
            sql_ds['where'].append('date between \'' + start_date + '\' and \'' + end_date + '\'')

        sql_ds['where'].append('country_id = ' + str(country_id))
        if(state_id) :
            sql_ds['where'].append('state_id = ' + str(state_id))
    sql_q = join_sql_ds(sql_ds)
    df_result = pd.read_sql(sql_q, con=mysql_cn)
    return df_result

def get_farmers_per_day(**kwargs):
    country_id, state_id, start_date, end_date, aggregators_list, mandis_list, crops_list, gaddidars_list = read_kwargs(kwargs)
    database = DATABASES['default']['NAME']
    username = DATABASES['default']['USER']
    password = DATABASES['default']['PASSWORD']
    host = DATABASES['default']['HOST']
    port = DATABASES['default']['PORT']
    mysql_cn = MySQLdb.connect(host=host, port=port, user=username, passwd=password, db=database, charset='utf8', use_unicode=True)

    # Constructing sql query
    sql_ds = get_init_sql_ds()
    sql_ds['select'].append('lct.date,count(distinct(lct.farmer_id)) as farmer_count')
    sql_ds['from'].append('loop_combinedtransaction lct')
    sql_ds['join'].append(['loop_mandi lm', 'lm.id = lct.mandi_id'])
    sql_ds['join'].append(['loop_crop lcrp', 'lcrp.id = lct.crop_id'])
    sql_ds['join'].append(['loop_farmer lf', 'lf.id = lct.farmer_id'])
    sql_ds['join'].append(['loop_loopuser lu', 'lu.user_id = lct.user_created_id and lu.role = ' + str(ROLE_CHOICE_AGGREGATOR)])
    sql_ds['join'].append(['loop_district ld', 'ld.id = lm.district_id'])
    sql_ds['join'].append(['loop_state ls', 'ls.id = ld.state_id'])
    sql_ds['join'].append(['loop_country lc', 'lc.id = ls.country_id'])
    sql_ds['group by'].append('date')

    if len(aggregators_list) > 0:
        sql_ds['where'].append('lct.user_created_id in (' + ",".join(aggregators_list) + ")")
    if len(mandis_list) > 0:
        sql_ds['where'].append('lm.id in (' + ",".join(mandis_list) + ')')
    if len(crops_list) > 0:
        sql_ds['where'].append('lcrp.id in (' + ",".join(crops_list) + ')')
    sql_ds['where'].append('lct.date between \'' + start_date + '\' and \'' + end_date + '\'')
    sql_ds['where'].append('country_id = ' + str(country_id))
    if(state_id) :
        sql_ds['where'].append('state_id = ' + str(state_id))

    query = join_sql_ds(sql_ds)
    df_result = pd.read_sql(query, con=mysql_cn)
    return df_result

def crop_prices_query(from_timeseries, **kwargs):
    country_id, state_id, start_date, end_date, aggregators_list, mandis_list, crops_list, gaddidars_list = read_kwargs(kwargs)
    database = DATABASES['default']['NAME']
    username = DATABASES['default']['USER']
    password = DATABASES['default']['PASSWORD']
    host = DATABASES['default']['HOST']
    port = DATABASES['default']['PORT']
    mysql_cn = MySQLdb.connect(host=host, port=port, user=username, passwd=password, db=database, charset='utf8', use_unicode=True)

    sql_ds = get_init_sql_ds()
    if from_timeseries:
        sql_ds['select'].append('crop_id, crop_name, date, min(price) Min_price, max(price) Max_price, avg(price) Avg_price, sum(quantity) Quantity')
        sql_ds['group by'].append('crop_id, date')
    else:
        sql_ds['select'].append('crop_id, crop_name, mandi_id, mandi_name_en mandi_name, min(price) Min_price, max(price) Max_price')
        sql_ds['group by'].append('crop_id, mandi_id')

    sql_ds['from'].append('loop_combinedtransaction lct')
    sql_ds['join'].append(['loop_mandi lm', 'lm.id = lct.mandi_id'])
    sql_ds['join'].append(['loop_crop lcrp', 'lcrp.id = lct.crop_id'])
    sql_ds['join'].append(['loop_loopuser lu', 'lu.user_id = lct.user_created_id and lu.role = ' + str(ROLE_CHOICE_AGGREGATOR)])
    sql_ds['join'].append(['loop_district ld', 'ld.id = lm.district_id'])
    sql_ds['join'].append(['loop_state ls', 'ls.id = ld.state_id'])
    sql_ds['join'].append(['loop_country lc', 'lc.id = ls.country_id'])

    if len(aggregators_list) > 0:
        sql_ds['where'].append('lct.user_created_id in (' + ",".join(aggregators_list) + ")")
    if len(mandis_list) > 0:
        sql_ds['where'].append('lm.id in (' + ",".join(mandis_list) + ')')
    # if len(gaddidars_list) > 0:
    #     sql_ds['where'].append('gaddidar_id in (' + ",".join(gaddidars_list) + ')')
    if len(crops_list) > 0:
        sql_ds['where'].append('lcrp.id in (' + ",".join(crops_list) + ')')
    sql_ds['where'].append('lct.date between \'' + start_date + '\' and \'' + end_date + '\'')
    sql_ds['where'].append('country_id = ' + str(country_id))
    if(state_id) :
        sql_ds['where'].append('state_id = ' + str(state_id))

    query = join_sql_ds(sql_ds)

    df_result = pd.read_sql(query, con=mysql_cn)
    return df_result

def get_data_from_myisam(get_total, **kwargs):
    df_result = query_myisam(**kwargs)
    country_id, state_id, start_date, end_date, aggregators_list, mandis_list, crops_list, gaddidars_list = read_kwargs(kwargs)
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

def read_kwargs(Kwargs):
    return Kwargs['country_id'], Kwargs['state_id'], Kwargs['start_date'], Kwargs['end_date'], Kwargs['aggregators_list'],Kwargs['mandis_list'],Kwargs['crops_list'], Kwargs['gaddidars_list']

def get_volume_aggregator(**kwargs):
    result_data = {}
    df_result = query_myisam(**kwargs)
    aggregation = {
        'quantity':{
            'quantity__sum':'sum'
        },
        # 'mandi_id':{
        #     'mandi_id_count':'count'
        # }
    }
    try:
        df_result = df_result.groupby(['aggregator_id','aggregator_name','mandi_id','mandi_name']).agg(aggregation).reset_index()
        df_result.columns = df_result.columns.droplevel(1)
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

def aggregator_volume(**kwargs):
    df_result = query_myisam(**kwargs)
    final_data_list = {}
    try:
        aggregator_groupby_data = df_result.groupby(['aggregator_id', 'aggregator_name'])['quantity'].sum().reset_index().sort('quantity', ascending=False)
        final_data_list = convert_to_dict(df_result=df_result, groupby_result=aggregator_groupby_data, graphname='aggrvol', outer_param='aggregator_name', inner_param='mandi_name', isdrillDown=True, parameter='quantity', series_name='Volume')
    except:
        final_data_list["error"] = "No data found"
    return final_data_list

def aggregator_amount(**kwargs):
    df_result = query_myisam(**kwargs)
    final_data_list = {}
    try:
        aggregator_groupby_data = df_result.groupby(['aggregator_id', 'aggregator_name'])['amount'].sum().reset_index().sort('amount', ascending=False)
        final_data_list = convert_to_dict(df_result=df_result, groupby_result=aggregator_groupby_data, graphname='aggramt', outer_param='aggregator_name', inner_param='mandi_name', isdrillDown=True, parameter='amount', series_name='Amount')
    except:
        final_data_list["error"] = "No data found"
    return final_data_list

def aggregator_visits(**kwargs):
    df_result = query_myisam(**kwargs)
    final_data_list = {}
    try:
        aggregator_groupby_data = df_result.groupby(['aggregator_id','aggregator_name', 'mandi_name'])['date'].nunique().to_frame().reset_index().sort('date', ascending=False)
        final_data_list = visitData(aggregator_groupby_data, 'aggrvisit', 'aggregator_name', 'mandi_name', 'date', True, 'date')
    except:
        final_data_list["error"] = "No data found"
    return final_data_list

def mandi_volume(**kwargs):
    df_result = query_myisam(**kwargs)
    final_data_list = {}
    try:
        aggregator_groupby_data = df_result.groupby(['mandi_id', 'mandi_name'])['quantity'].sum().reset_index().sort('quantity', ascending=False)
        final_data_list = convert_to_dict(df_result=df_result, groupby_result=aggregator_groupby_data, graphname='mandivolume', outer_param='mandi_name', inner_param='aggregator_name', isdrillDown=True, parameter='quantity', series_name='Volume')
    except:
        final_data_list["error"] = "No data found"
    return final_data_list

def mandi_visits(**kwargs):
    df_result = query_myisam(**kwargs)
    final_data_list = {}
    try:
        aggregator_groupby_data = df_result.groupby(['mandi_id','aggregator_name', 'mandi_name'])['date'].nunique().to_frame().reset_index()
        final_data_list = visitData(aggregator_groupby_data, 'mandivisit', 'mandi_name', 'aggregator_name', 'date', True, 'date')
    except:
        final_data_list["error"] = "No data found"
    return final_data_list

def crop_volume(**kwargs):
    df_result = sql_query(**kwargs)
    final_data_list = {}
    try:
        aggregator_groupby_data = df_result.groupby(['crop_id', 'crop_name'])['quantity'].sum().reset_index().sort('quantity', ascending=False)
        final_data_list = convert_to_dict(df_result=df_result, groupby_result=aggregator_groupby_data, graphname='cropvolume', outer_param='crop_name', inner_param='mandi_name', isdrillDown=True, parameter='quantity', series_name='Volume')
    except:
        final_data_list["error"] = "No data found"
    return final_data_list

def crop_farmer_count(**kwargs):
    df_result = sql_query(**kwargs)
    final_data_list = {}
    try:
        aggregator_groupby_data = df_result.groupby(['crop_id', 'crop_name'])['farmer_id'].nunique().to_frame().reset_index()
        final_data_list = visitData(aggregator_groupby_data, 'cropfarmercount', 'crop_name', '',  'farmer_id', False, 'farmer_id')
    except:
        final_data_list["error"] = "No data found"
    return final_data_list

def crop_prices(**kwargs):
    df_result = crop_prices_query(from_timeseries=0, **kwargs)
    final_data_list = {}
    try:
        crop_groupby_data = df_result.groupby(['crop_id', 'crop_name']).agg({'Min_price':'min', 'Max_price':'max'}).reset_index().sort('Max_price', ascending=False)
        outer_data = {'outerData':{'series':[], 'categories':crop_groupby_data['crop_name'].tolist()}}
        temp_dict_outer = {'name':'Crop price','data':[]}

        for index, row in crop_groupby_data.iterrows():
            temp_dict_outer['data'].append({'name':row['crop_name'],'high':int(row['Max_price']), 'low':int(row['Min_price']),'drilldown':row['crop_name'] + ' Count'})

        outer_data['outerData']['series'].append(temp_dict_outer)
        final_data_list['cropprices'] = outer_data
        # DrillDown
        inner_data = {'innerData': []}
        crop_mandi_groupby_data = df_result.groupby(['crop_id', 'crop_name'])
        for index, row in crop_mandi_groupby_data:
            temp_dict_inner = {'data': []}
            temp_dict_inner['id'] = index[1] + ' Count'
            for k, v in row.iterrows():
                temp_dict_inner['data'].append({'name':v['mandi_name'], 'high':v['Max_price'], 'low':v['Min_price']})
            inner_data['innerData'].append(temp_dict_inner)
        final_data_list['cropprices'].update(inner_data)

    except:
        final_data_list["error"] = "No data found"
    return final_data_list

def mandi_farmer_count(**kwargs):
    final_data_list = repeat_farmer_count('mandi_id', 'mandi_name', 'mandifarmercount', **kwargs)
    return final_data_list

def agg_farmer_count(**kwargs):
    final_data_list = repeat_farmer_count('aggregator_id', 'aggregator_name', 'aggrfarmercount', **kwargs)
    return final_data_list

def repeat_farmer_count(outer_param1, outer_param2, graphname, **kwargs):
    df_result = sql_query(**kwargs)
    final_data_list = {}
    try:
        aggregator_groupby_data = df_result.groupby([outer_param1, outer_param2, 'farmer_id', 'farmer_name']).agg({'date':pd.Series.nunique}).rename(columns={'date': 'repeat_count'}).reset_index()
        aggregator_farmer_count = aggregator_groupby_data.groupby([outer_param1, outer_param2]).agg({'repeat_count':'count'}).rename(columns={'repeat_count':'farmer_count'}).reset_index().sort('farmer_count', ascending=False)
        outer_data = {'outerData': {'series':[], 'categories':aggregator_farmer_count[outer_param2].tolist()}}
        temp_dict_outer = {'name': 'Total farmer Count', 'data':[]}

        for index, row in aggregator_farmer_count.iterrows():
            temp_dict_outer['data'].append({'name':row[outer_param2], 'high':int(row['farmer_count']),'low':0, 'drilldown':row[outer_param2] + ' Count'})
        outer_data['outerData']['series'].append(temp_dict_outer)

        temp_dict_outer = {'name':'Repeated Farmer Count', 'data':[]}
        repeat_farmer_count = aggregator_groupby_data[aggregator_groupby_data['repeat_count']>1].groupby([outer_param1, outer_param2]).agg({'repeat_count':'count'}).rename(columns={'repeat_count':'repeat_farmer_count'}).reset_index()
        for index, row in repeat_farmer_count.iterrows():
            temp_dict_outer['data'].append({'name':row[outer_param2], 'high':int(row['repeat_farmer_count']),'low':0, 'drilldown':row[outer_param2] + ' Repeat'})
        outer_data['outerData']['series'].append(temp_dict_outer)

        final_data_list[graphname] = outer_data

        # DrillDown data
        farmer_count_freq = aggregator_groupby_data.groupby(['repeat_count', outer_param1, outer_param2]).agg({'farmer_id':'count'}).rename(columns={'farmer_id':'farmer_count'}).reset_index()
        inner_data = {'innerData':[]}
        farmer_count_agg = farmer_count_freq.groupby([outer_param1, outer_param2])

        for index, row in farmer_count_agg:
            temp_dict_inner = {'data':[]}
            temp_dict_inner['name'] = index[1]
            temp_dict_inner['id'] = index[1] + ' Count'
            for k, v in row.iterrows():
                temp_dict_inner['data'].append({'name':v['repeat_count'], 'high':v['farmer_count'],'low':0})
            inner_data['innerData'].append(temp_dict_inner)

        final_data_list[graphname].update(inner_data)
    except:
        final_data_list["error"] = "No data Found"

    return final_data_list

def visitData(groupby_result, graphname, outer_param, inner_param, count_param, isdrillDown, sortParam):
    final_data_list = {}
    try:
        outer_data = {'outerData':{'series':[], 'categories':groupby_result[outer_param].tolist()}}
        total_data = {'message' : 'Visits ' + ' : ' + str(groupby_result[count_param].sum())}
        temp_dict_outer = {'name':'Visit','data':[]}

        aggregator_visit_data = groupby_result.groupby(outer_param)[count_param].sum().reset_index().sort(sortParam, ascending=False)
        for index, row in aggregator_visit_data.iterrows():
            temp_dict_outer['data'].append({'name':row[outer_param],'high':int(row[count_param]),'low':0,'drilldown':row[outer_param] + ' Count'})

        outer_data['outerData']['series'].append(temp_dict_outer)
        final_data_list[graphname] = outer_data
        final_data_list[graphname].update(total_data)
        if(isdrillDown):
            mandi_groupby_data = {name:dict(zip(g[inner_param],g[count_param])) for name,g in groupby_result.groupby([outer_param])}
            inner_data = createInnerdataDict(mandi_groupby_data, ' Count')

            final_data_list[graphname].update(inner_data)

    except:
        final_data_list["error"] = "No Data Found"
    return final_data_list

def convert_to_dict(df_result=None, groupby_result=None, graphname=None, outer_param=None, inner_param=None, isdrillDown=False, parameter=None, series_name=None):
    final_data_list = {}
    try:
        outer_data = {'outerData':{'series':[], 'categories':groupby_result[outer_param].tolist()}}
        total_data = {'message' : series_name + ' : ' + str(groupby_result[parameter].sum())}
        temp_dict_outer = {'name':series_name,'data':[]}

        for index, row in groupby_result.iterrows():
            temp_dict_outer['data'].append({'name':row[1],'high':int(row[2]),'low':0,'drilldown':row[1] + str(' ' + series_name)})

        outer_data['outerData']['series'].append(temp_dict_outer)
        final_data_list[graphname] = outer_data
        final_data_list[graphname].update(total_data)
        if(isdrillDown):
            df_result = df_result.groupby([outer_param, inner_param])[parameter].sum().reset_index()
            mandi_groupby_data = {name:dict(zip(g[inner_param],g[parameter])) for name,g in df_result.groupby([outer_param])}
            inner_data = createInnerdataDict(mandi_groupby_data, str(' '+ series_name))

            final_data_list[graphname].update(inner_data)
    except:
        final_data_list["error"] = "No data Found"
    return final_data_list

def createInnerdataDict(dictData, keyword):
    inner_data = {'innerData': []}

    for key,value in dictData.iteritems():
        temp_dict_inner = {'data':[]}
        temp_dict_inner['name'] = key
        temp_dict_inner['id'] = key + keyword
        for k, v in value.iteritems():
            temp_dict_inner['data'].append({'name':k,'high':round(v,2),'low':0})
        temp_dict_inner['data'].sort(key=itemgetter('high'),reverse=True)
        inner_data['innerData'].append(temp_dict_inner)

    return inner_data

def agg_spk_cpk(**kwargs):
    final_data_list = {}
    df_result = query_myisam(**kwargs)
    try:
        df_result = df_result.groupby(['date','aggregator_id','mandi_id','aggregator_name','mandi_name']).agg(cpk_spk_aggregation).reset_index()
        df_result.columns = df_result.columns.droplevel(1)

        df_result_agg = df_result.groupby(['aggregator_id','aggregator_name']).sum().reset_index()
        df_result_agg['cpk'] = (df_result_agg['aggregator_incentive'] + df_result_agg['transportation_cost'])/df_result_agg['quantity']
        df_result_agg['spk'] = (df_result_agg['farmer_share'] + df_result_agg['gaddidar_share'])/df_result_agg['quantity']
        df_result_agg = df_result_agg.sort('cpk', ascending=False)
        outer_data = {'outerData': {'series':[],'categories':df_result_agg['aggregator_name'].tolist()}}
        temp_dict_outer = {'name':'cpk','data':[]}
        for row in df_result_agg.iterrows():
            temp_dict_outer['data'].append({'name':row[1].aggregator_name,'high':round(row[1].cpk,3),'low':0,'drilldown':row[1].aggregator_name+' cpk'})
        outer_data['outerData']['series'].append(temp_dict_outer)

        temp_dict_outer = {'name':'spk','data':[]}
        for row in df_result_agg.iterrows():
            temp_dict_outer['data'].append({'name':row[1].aggregator_name,'high':round(row[1].spk,3),'low':0,'drilldown':row[1].aggregator_name+' spk'})
        outer_data['outerData']['series'].append(temp_dict_outer)

        final_data_list['aggrspkcpk'] = outer_data
        inner_data = {'innerData': []}

        df_result_mandi = df_result.groupby(['aggregator_id','mandi_id','aggregator_name','mandi_name']).sum().reset_index()
        df_result_mandi['cpk'] = (df_result_mandi['aggregator_incentive'] + df_result_mandi['transportation_cost'])/df_result_mandi['quantity']
        df_result_mandi['spk'] = (df_result_mandi['farmer_share'] + df_result_mandi['gaddidar_share'])/df_result_mandi['quantity']

        agg_mandi_cpk_dict = {name[1]: dict(zip(g['mandi_name'],g['cpk'])) for name,g in df_result_mandi.groupby(['aggregator_id','aggregator_name'])}
        agg_mandi_spk_dict = {name[1]: dict(zip(g['mandi_name'],g['spk'])) for name,g in df_result_mandi.groupby(['aggregator_id','aggregator_name'])}
        for key, value in agg_mandi_cpk_dict.iteritems():
            temp_dict_inner = {'data':[]}
            temp_dict_inner['name'] = key
            temp_dict_inner['id'] = str(key) + ' cpk'
            for k, v in value.iteritems():
                temp_dict_inner['data'].append({'name':k,'high':round(v,3),'low':0})
            temp_dict_inner['data'].sort(key=itemgetter('high'),reverse=True)
            inner_data['innerData'].append(temp_dict_inner)

        for key, value in agg_mandi_spk_dict.iteritems():
            temp_dict_inner = {'data':[]}
            temp_dict_inner['name'] = key
            temp_dict_inner['id'] = str(key) + ' spk'
            for k, v in value.iteritems():
                temp_dict_inner['data'].append({'name':k,'high':round(v,3),'low':0})
            temp_dict_inner['data'].sort(key=itemgetter('high'),reverse=True)
            inner_data['innerData'].append(temp_dict_inner)

        final_data_list['aggrspkcpk'].update(inner_data)
    except:
        final_data_list["error"] = "No data found"
    return final_data_list

def agg_cost(**kwargs):
    final_data_list = {}
    df_result = query_myisam(**kwargs)
    try:
        df_result = df_result.groupby(['date','aggregator_id','mandi_id','aggregator_name','mandi_name']).agg(cpk_spk_aggregation).reset_index()
        df_result.columns = df_result.columns.droplevel(1)

        df_result_agg = df_result.groupby(['aggregator_id','aggregator_name']).sum().reset_index()
        df_result_agg['cost'] = df_result_agg['aggregator_incentive'] + df_result_agg['transportation_cost']
        df_result_agg['recovered'] = df_result_agg['farmer_share'] + df_result_agg['gaddidar_share']
        df_result_agg = df_result_agg.sort('cost', ascending=False)
        outer_data = {'outerData': {'series':[],'categories':df_result_agg['aggregator_name'].tolist()}}
        temp_dict_outer = {'name':'cost','data':[]}
        for row in df_result_agg.iterrows():
            temp_dict_outer['data'].append({'name':row[1].aggregator_name,'high':round(row[1].cost,3),'low':0,'drilldown':row[1].aggregator_name+' cost'})
        outer_data['outerData']['series'].append(temp_dict_outer)

        temp_dict_outer = {'name':'recovered','data':[]}
        for row in df_result_agg.iterrows():
            temp_dict_outer['data'].append({'name':row[1].aggregator_name,'high':round(row[1].recovered,3),'low':0,'drilldown':row[1].aggregator_name+' recovered'})
        outer_data['outerData']['series'].append(temp_dict_outer)

        final_data_list['aggrrecoveredtotal'] = outer_data
        inner_data = {'innerData': []}

        df_result_mandi = df_result.groupby(['aggregator_id','mandi_id','aggregator_name','mandi_name']).sum().reset_index()
        df_result_mandi['cost'] = df_result_mandi['aggregator_incentive'] + df_result_mandi['transportation_cost']
        df_result_mandi['recovered'] = df_result_mandi['farmer_share'] + df_result_mandi['gaddidar_share']

        agg_mandi_cpk_dict = {name[1]: dict(zip(g['mandi_name'],g['cost'])) for name,g in df_result_mandi.groupby(['aggregator_id','aggregator_name'])}
        agg_mandi_spk_dict = {name[1]: dict(zip(g['mandi_name'],g['recovered'])) for name,g in df_result_mandi.groupby(['aggregator_id','aggregator_name'])}
        for key, value in agg_mandi_cpk_dict.iteritems():
            temp_dict_inner = {'data':[]}
            temp_dict_inner['name'] = key
            temp_dict_inner['id'] = str(key) + ' cost'
            for k, v in value.iteritems():
                temp_dict_inner['data'].append({'name':k,'high':round(v,3),'low':0})
            temp_dict_inner['data'].sort(key=itemgetter('high'),reverse=True)
            inner_data['innerData'].append(temp_dict_inner)

        for key, value in agg_mandi_spk_dict.iteritems():
            temp_dict_inner = {'data':[]}
            temp_dict_inner['name'] = key
            temp_dict_inner['id'] = str(key) + ' recovered'
            for k, v in value.iteritems():
                temp_dict_inner['data'].append({'name':k,'high':round(v,3),'low':0})
            temp_dict_inner['data'].sort(key=itemgetter('high'),reverse=True)
            inner_data['innerData'].append(temp_dict_inner)

        final_data_list['aggrrecoveredtotal'].update(inner_data)
    except:
        final_data_list["error"] = "No data found"
    return final_data_list

def cost_recovered_data(df_result, groupby_result, df_result_mandi, graphname, outer_param, inner_param, isdrillDown, drillDownparam1, drillDownparam2):
    final_data_list = {}
    try:
        outer_data = {'outerData': {'series':[],'categories':groupby_result[outer_param].tolist()}}
        temp_dict_outer = {'name':'cost','data':[]}
        for index, row in groupby_result.iterrows():
            temp_dict_outer['data'].append({'name':row[1],'high':round(row[8],3),'low':0,'drilldown':row[1]+' cost'})
        outer_data['outerData']['series'].append(temp_dict_outer)
        temp_dict_outer = {'name':'recovered','data':[]}
        for index, row in groupby_result.iterrows():
            temp_dict_outer['data'].append({'name':row[1],'high':round(row[9],3),'low':0,'drilldown':row[1]+' recovered'})
        outer_data['outerData']['series'].append(temp_dict_outer)

        inner_data = {'innerData':[]}
        final_data_list[graphname] = outer_data

        agg_mandi_cpk_dict = {name: dict(zip(g[inner_param],g[drillDownparam1])) for name,g in df_result_mandi.groupby([outer_param])}
        agg_mandi_spk_dict = {name: dict(zip(g[inner_param],g[drillDownparam2])) for name,g in df_result_mandi.groupby([outer_param])}

        #Adding all drilldown points to inner Data list
        inner_data['innerData'].extend(createInnerdataDict(agg_mandi_cpk_dict, ' cost')['innerData'])
        inner_data['innerData'].extend(createInnerdataDict(agg_mandi_spk_dict, ' recovered')['innerData'])

        final_data_list[graphname].update(inner_data)
    except:
        final_data_list["error"] = "No data found"
    return final_data_list

def mandi_cost(**kwargs):
    final_data_list = {}
    try:
        df_result = query_myisam(**kwargs)
        df_result = df_result.groupby(['date','aggregator_id','mandi_id','aggregator_name','mandi_name']).agg(cpk_spk_aggregation).reset_index()
        df_result.columns = df_result.columns.droplevel(1)

        df_result_agg = df_result.groupby(['mandi_id','mandi_name']).sum().reset_index()
        df_result_agg['cost'] = df_result_agg['aggregator_incentive'] + df_result_agg['transportation_cost']
        df_result_agg['recovered'] = df_result_agg['farmer_share'] + df_result_agg['gaddidar_share']

        df_result_mandi = df_result.groupby(['aggregator_id','mandi_id','aggregator_name','mandi_name']).sum().reset_index()
        df_result_mandi['cost'] = df_result_mandi['aggregator_incentive'] + df_result_mandi['transportation_cost']
        df_result_mandi['recovered'] = df_result_mandi['farmer_share'] + df_result_mandi['gaddidar_share']
        df_result_agg = df_result_agg.sort('cost', ascending=False)
        final_data_list = cost_recovered_data(df_result, df_result_agg, df_result_mandi, 'mandirecoveredtotal', 'mandi_name', 'aggregator_name', True, 'cost', 'recovered')
    except:
        final_data_list["error"] = "No data found"
    return final_data_list

def mandi_spk_cpk(**kwargs):
    df_result = query_myisam(**kwargs)
    final_data_list = {}
    try:
        df_result = df_result.groupby(['date','aggregator_id','mandi_id','aggregator_name','mandi_name']).agg(cpk_spk_aggregation).reset_index()
        df_result.columns = df_result.columns.droplevel(1)

        df_result_agg = df_result.groupby(['mandi_id','mandi_name']).sum().reset_index()
        df_result_agg['cpk'] = (df_result_agg['aggregator_incentive'] + df_result_agg['transportation_cost'])/df_result_agg['quantity']
        df_result_agg['spk'] = (df_result_agg['farmer_share'] + df_result_agg['gaddidar_share'])/df_result_agg['quantity']
        df_result_mandi = df_result.groupby(['aggregator_id','mandi_id','aggregator_name','mandi_name']).sum().reset_index()
        df_result_mandi['cpk'] = (df_result_mandi['aggregator_incentive'] + df_result_mandi['transportation_cost'])/df_result_mandi['quantity']
        df_result_mandi['spk'] = (df_result_mandi['farmer_share'] + df_result_mandi['gaddidar_share'])/df_result_mandi['quantity']
        df_result_agg = df_result_agg.sort('cpk', ascending=False)
        final_data_list = cost_recovered_data(df_result, df_result_agg, df_result_mandi, 'mandispkcpk', 'mandi_name', 'aggregator_name', True, 'cpk','spk')
    except:
        final_data_list["error"] = "No data found"
    return final_data_list

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

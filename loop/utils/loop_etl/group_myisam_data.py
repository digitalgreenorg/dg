from dg.settings import DATABASES
import MySQLdb
import datetime, time
import pandas as pd
import numpy as np
from loop.utils.loop_etl.aggregation_methods import *
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

def sql_query(country_id, from_date=None, to_date=None):
    database = DATABASES['default']['NAME']
    username = DATABASES['default']['USER']
    password = DATABASES['default']['PASSWORD']
    host = DATABASES['default']['HOST']
    port = DATABASES['default']['PORT']
    mysql_cn = MySQLdb.connect(host=host, port=port, user=username, passwd=password, db=database, charset='utf8', use_unicode=True)

    query = '''SELECT lct.user_created_id aggregator_id, lu.name_en aggregator_name, date, crop_id, crop_name, mandi_id,
				mandi_name_en mandi_name, quantity, farmer_id, lf.name farmer_name
                FROM loop_combinedtransaction lct 
                JOIN loop_mandi lm ON lm.id = lct.mandi_id 
                JOIN loop_crop lcrp ON lcrp.id = lct.crop_id
                JOIN loop_farmer lf ON lf.id = lct.farmer_id
                JOIN loop_loopuser lu ON lu.user_id = lct.user_created_id
            '''

    if from_date:
        query = query + " and date between " + str(from_date) + " and " + str(to_date)

    df_result = pd.read_sql(query, con=mysql_cn)
    return df_result

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

def crop_prices_query(country_id, from_date=None, to_date=None):
    database = DATABASES['default']['NAME']
    username = DATABASES['default']['USER']
    password = DATABASES['default']['PASSWORD']
    host = DATABASES['default']['HOST']
    port = DATABASES['default']['PORT']
    mysql_cn = MySQLdb.connect(host=host, port=port, user=username, passwd=password, db=database, charset='utf8', use_unicode=True)

    query = '''
                SELECT crop_id, crop_name, mandi_id, mandi_name_en mandi_name, min(price) Min_price, max(price) Max_price
                FROM loop_combinedtransaction lct
		        JOIN loop_crop lcr ON lcr.id= lct.crop_id and date between 20170101 and 20170201
		        JOIN loop_mandi lm ON lm.id = lct.mandi_id
                GROUP BY crop_id, mandi_id;
            '''
    # if from_date:
    #     query = query + " and date between " + str(from_date) + " and " + str(to_date)

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

    df_result = query_myisam(country_id, from_date, to_date)
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
    df_result = query_myisam(country_id, start_date, end_date)
    final_data_list = {}
    aggregator_groupby_data = df_result.groupby(['aggregator_id', 'aggregator_name'])['quantity'].sum().reset_index()

    return volumedata(df_result, aggregator_groupby_data, 'aggrvol', 'aggregator_name', 'mandi_name', True)
    
def aggregator_visits(country_id, start_date, end_date):
    df_result = query_myisam(country_id, start_date, end_date)
    final_data_list = {}
    aggregator_groupby_data = df_result.groupby(['aggregator_id','aggregator_name', 'mandi_name'])['date'].nunique().to_frame().reset_index()
    
    return visitData(aggregator_groupby_data, 'aggrvisit', 'aggregator_name', 'mandi_name', 'date', True)


def mandi_volume(country_id, start_date, end_date):
    df_result = query_myisam(country_id, start_date, end_date)
    final_data_list = {}
    aggregator_groupby_data = df_result.groupby(['mandi_id', 'mandi_name'])['quantity'].sum().reset_index()

    return volumedata(df_result, aggregator_groupby_data, 'mandivolume', 'mandi_name', 'aggregator_name', True)

def mandi_visits(country_id, start_date, end_date):
    df_result = query_myisam(country_id, start_date, end_date)
    final_data_list = {}
    aggregator_groupby_data = df_result.groupby(['mandi_id','aggregator_name', 'mandi_name'])['date'].nunique().to_frame().reset_index()
    
    return visitData(aggregator_groupby_data, 'mandivisit', 'mandi_name', 'aggregator_name', 'date', True)



def crop_volume(country_id, start_date, end_date):
    df_result = sql_query(country_id, start_date, end_date)
    final_data_list = {}
    aggregator_groupby_data = df_result.groupby(['crop_id', 'crop_name'])['quantity'].sum().reset_index()
    return volumedata(df_result, aggregator_groupby_data, 'cropvolume', 'crop_name', 'mandi_name', True)

def crop_farmer_count(country_id, start_date, end_date):
    df_result = sql_query(country_id, start_date, end_date)
    final_data_list = {}
    aggregator_groupby_data = df_result.groupby(['crop_id', 'crop_name'])['farmer_id'].nunique().to_frame().reset_index()
    return visitData(aggregator_groupby_data, 'cropfarmercount', 'crop_name', '',  'farmer_id', False)

def crop_prices(country_id, start_date, end_date):
    df_result = crop_prices_query(country_id, start_date, end_date)
    final_data_list = {}
    df_result.columns.values
    crop_groupby_data = df_result.groupby(['crop_id', 'crop_name']).agg({'Min_price':'min', 'Max_price':'max'}).reset_index()
    try:
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

def agg_farmer_count(country_id, start_date, end_date):
    df_result = sql_query(country_id, start_date, end_date)
    final_data_list = {}
    aggregator_groupby_data = df_result.groupby(['aggregator_id', 'aggregator_name', 'farmer_id', 'farmer_name']).agg({'date':pd.Series.nunique}).reset_index()
    aggregator_farmer_count = aggregator_groupby_data.groupby(['aggregator_id', 'aggregator_name']).agg({'date':'count'}).reset_index()
    try:
        outer_data = {'outerData': {'series':[], 'categories':aggregator_farmer_count['aggregator_name'].tolist()}}
        temp_dict_outer = {'name': 'Total farmer Count', 'data':[]}

        for index, row in aggregator_farmer_count.iterrows():
            temp_dict_outer['data'].append({'name':row['aggregator_name'], 'y':int(row['date']), 'drilldown':row['aggregator_name'] + ' Count'})
        outer_data['outerData']['series'].append(temp_dict_outer)

        temp_dict_outer = {'name':'Repeated Farmer Count', 'data':[]}
        repeat_farmer_count = aggregator_groupby_data[aggregator_groupby_data['date']>1].groupby(['aggregator_id', 'aggregator_name']).agg({'date':'count'}).reset_index()
        # print repeat_farmer_count.head()
        for index, row in repeat_farmer_count.iterrows():
            temp_dict_outer['data'].append({'name':row['aggregator_name'], 'y':int(row['date']), 'drilldown':row['aggregator_name'] + ' Repeat'})
        outer_data['outerData']['series'].append(temp_dict_outer)

        final_data_list['aggrfarmercount'] = outer_data

        # DrillDown data
        

        
    except:
        final_data_list["error"] = "No data Found"

    return final_data_list

def visitData(groupby_result, graphname, outer_param, inner_param, count_param, isdrillDown):
    final_data_list = {}
    try:
        outer_data = {'outerData':{'series':[], 'categories':groupby_result[outer_param].tolist()}}
        temp_dict_outer = {'name':'Aggregator Visit','data':[]}

        aggregator_visit_data = groupby_result.groupby(outer_param)[count_param].sum().reset_index()
        
        for index, row in aggregator_visit_data.iterrows():
            temp_dict_outer['data'].append({'name':row[outer_param],'y':int(row[count_param]),'drilldown':row[outer_param] + ' Count'})
        
        outer_data['outerData']['series'].append(temp_dict_outer)
        final_data_list[graphname] = outer_data
        if(isdrillDown):
            mandi_groupby_data = {name:dict(zip(g[inner_param],g[count_param])) for name,g in groupby_result.groupby([outer_param])}
            inner_data = createInnerdataDict(mandi_groupby_data, ' Count')

            final_data_list[graphname].update(inner_data)

    except:
        final_data_list["error"] = "No Data Found"
    return final_data_list

def volumedata(df_result, groupby_result, graphname, outer_param, inner_param, isdrillDown):
    final_data_list = {}

    try:
        outer_data = {'outerData':{'series':[], 'categories':groupby_result[outer_param].tolist()}}
        temp_dict_outer = {'name':'Aggregator Volume','data':[]}

        for index, row in groupby_result.iterrows():
            temp_dict_outer['data'].append({'name':row[1],'y':int(row[2]),'drilldown':row[1] + ' Volume'})
        
        outer_data['outerData']['series'].append(temp_dict_outer)
        final_data_list[graphname] = outer_data
        if(isdrillDown):
            df_result = df_result.groupby([outer_param, inner_param])['quantity'].sum().reset_index()
            mandi_groupby_data = {name:dict(zip(g[inner_param],g['quantity'])) for name,g in df_result.groupby([outer_param])}
            inner_data = createInnerdataDict(mandi_groupby_data, ' Volume')

            final_data_list[graphname].update(inner_data)

    except:
        final_data_list["error"] = "No Data Found"
    
    return final_data_list


def createInnerdataDict(dictData, keyword):
    inner_data = {'innerData': []}

    for key,value in dictData.iteritems():
        temp_dict_inner = {'data':[]}
        temp_dict_inner['name'] = key
        temp_dict_inner['id'] = key + keyword
        for k, v in value.iteritems():
            temp_dict_inner['data'].append([k,v])
        inner_data['innerData'].append(temp_dict_inner)
    
    return inner_data

def agg_spk_cpk(country_id, start_date, end_date):
    final_data_list = {}
    df_result = query_myisam(country_id, start_date, end_date)
    df_result = df_result.groupby(['date','aggregator_id','mandi_id','aggregator_name','mandi_name']).agg(cpk_spk_aggregation).reset_index()
    df_result.columns = df_result.columns.droplevel(1)

    df_result_agg = df_result.groupby(['aggregator_id','aggregator_name']).sum().reset_index()
    df_result_agg['cpk'] = (df_result_agg['aggregator_incentive'] + df_result_agg['transportation_cost'])/df_result_agg['quantity']
    df_result_agg['spk'] = (df_result_agg['farmer_share'] + df_result_agg['gaddidar_share'])/df_result_agg['quantity']

    outer_data = {'outerData': {'series':[],'categories':df_result_agg['aggregator_name'].tolist()}}
    temp_dict_outer = {'name':'cpk','data':[]}
    for row in df_result_agg.iterrows():
        temp_dict_outer['data'].append({'name':row[1].aggregator_name,'y':round(row[1].cpk,3),'drilldown':row[1].aggregator_name+' cpk'})
    outer_data['outerData']['series'].append(temp_dict_outer)

    temp_dict_outer = {'name':'spk','data':[]}
    for row in df_result_agg.iterrows():
        temp_dict_outer['data'].append({'name':row[1].aggregator_name,'y':round(row[1].spk,3),'drilldown':row[1].aggregator_name+' spk'})
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
            temp_dict_inner['data'].append([k,round(v,3)])
        inner_data['innerData'].append(temp_dict_inner)

    for key, value in agg_mandi_spk_dict.iteritems():
        temp_dict_inner = {'data':[]}
        temp_dict_inner['name'] = key
        temp_dict_inner['id'] = str(key) + ' spk'
        for k, v in value.iteritems():
            temp_dict_inner['data'].append([k,round(v,3)])
        inner_data['innerData'].append(temp_dict_inner)

    final_data_list['aggrspkcpk'].update(inner_data)

    return final_data_list

def agg_cost(country_id, start_date, end_date):
    final_data_list = {}
    df_result = query_myisam(country_id, start_date, end_date)
    df_result = df_result.groupby(['date','aggregator_id','mandi_id','aggregator_name','mandi_name']).agg(cpk_spk_aggregation).reset_index()
    df_result.columns = df_result.columns.droplevel(1)

    df_result_agg = df_result.groupby(['aggregator_id','aggregator_name']).sum().reset_index()
    df_result_agg['cost'] = df_result_agg['aggregator_incentive'] + df_result_agg['transportation_cost']
    df_result_agg['recovered'] = df_result_agg['farmer_share'] + df_result_agg['gaddidar_share']

    outer_data = {'outerData': {'series':[],'categories':df_result_agg['aggregator_name'].tolist()}}
    temp_dict_outer = {'name':'cost','data':[]}
    for row in df_result_agg.iterrows():
        temp_dict_outer['data'].append({'name':row[1].aggregator_name,'y':round(row[1].cost,3),'drilldown':row[1].aggregator_name+' cost'})
    outer_data['outerData']['series'].append(temp_dict_outer)

    temp_dict_outer = {'name':'recovered','data':[]}
    for row in df_result_agg.iterrows():
        temp_dict_outer['data'].append({'name':row[1].aggregator_name,'y':round(row[1].recovered,3),'drilldown':row[1].aggregator_name+' recovered'})
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
            temp_dict_inner['data'].append([k,round(v,3)])
        inner_data['innerData'].append(temp_dict_inner)

    for key, value in agg_mandi_spk_dict.iteritems():
        temp_dict_inner = {'data':[]}
        temp_dict_inner['name'] = key
        temp_dict_inner['id'] = str(key) + ' recovered'
        for k, v in value.iteritems():
            temp_dict_inner['data'].append([k,round(v,3)])
        inner_data['innerData'].append(temp_dict_inner)

    final_data_list['aggrrecoveredtotal'].update(inner_data)

    return final_data_list

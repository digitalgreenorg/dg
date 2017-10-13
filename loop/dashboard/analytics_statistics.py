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

def agg_farmer_count(**kwargs):
    final_data_list = repeat_farmer_count('aggregator_id', 'aggregator_name', 'aggrfarmercount', **kwargs)
    return final_data_list

def mandi_farmer_count(**kwargs):
    final_data_list = repeat_farmer_count('mandi_id', 'mandi_name', 'mandifarmercount', **kwargs)
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
            temp_dict_outer['data'].append({'name':row[outer_param2], 'y':int(row['farmer_count']),  'drilldown':row[outer_param2] + ' Count'})
        outer_data['outerData']['series'].append(temp_dict_outer)

        temp_dict_outer = {'name':'Repeated Farmer Count', 'data':[]}
        repeat_farmer_count = aggregator_groupby_data[aggregator_groupby_data['repeat_count']>1].groupby([outer_param1, outer_param2]).agg({'repeat_count':'count'}).rename(columns={'repeat_count':'repeat_farmer_count'}).reset_index()
        for index, row in repeat_farmer_count.iterrows():
            temp_dict_outer['data'].append({'name':row[outer_param2], 'y':int(row['repeat_farmer_count']), 'drilldown':row[outer_param2] + ' Repeat'})
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
                temp_dict_inner['data'].append({'name':v['repeat_count'], 'y':v['farmer_count']})
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
            temp_dict_outer['data'].append({'name':row[outer_param],'y':int(row[count_param]), 'drilldown':row[outer_param] + ' Count'})

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
            temp_dict_outer['data'].append({'name':row[1].aggregator_name,'y':round(row[1].cpk,3), 'drilldown':row[1].aggregator_name+' cpk'})
        outer_data['outerData']['series'].append(temp_dict_outer)

        temp_dict_outer = {'name':'spk','data':[]}
        for row in df_result_agg.iterrows():
            temp_dict_outer['data'].append({'name':row[1].aggregator_name,'y':round(row[1].spk,3), 'drilldown':row[1].aggregator_name+' spk'})
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
                temp_dict_inner['data'].append({'name':k,'y':round(v,3) })
            temp_dict_inner['data'].sort(key=itemgetter('y'),reverse=True)
            inner_data['innerData'].append(temp_dict_inner)

        for key, value in agg_mandi_spk_dict.iteritems():
            temp_dict_inner = {'data':[]}
            temp_dict_inner['name'] = key
            temp_dict_inner['id'] = str(key) + ' spk'
            for k, v in value.iteritems():
                temp_dict_inner['data'].append({'name':k,'y':round(v,3) })
            temp_dict_inner['data'].sort(key=itemgetter('y'),reverse=True)
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
            temp_dict_outer['data'].append({'name':row[1].aggregator_name,'y':round(row[1].cost,3), 'drilldown':row[1].aggregator_name+' cost'})
        outer_data['outerData']['series'].append(temp_dict_outer)

        temp_dict_outer = {'name':'recovered','data':[]}
        for row in df_result_agg.iterrows():
            temp_dict_outer['data'].append({'name':row[1].aggregator_name,'y':round(row[1].recovered,3), 'drilldown':row[1].aggregator_name+' recovered'})
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
                temp_dict_inner['data'].append({'name':k,'y':round(v,3) })
            temp_dict_inner['data'].sort(key=itemgetter('y'),reverse=True)
            inner_data['innerData'].append(temp_dict_inner)

        for key, value in agg_mandi_spk_dict.iteritems():
            temp_dict_inner = {'data':[]}
            temp_dict_inner['name'] = key
            temp_dict_inner['id'] = str(key) + ' recovered'
            for k, v in value.iteritems():
                temp_dict_inner['data'].append({'name':k,'y':round(v,3) })
            temp_dict_inner['data'].sort(key=itemgetter('y'),reverse=True)
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
            temp_dict_outer['data'].append({'name':row[1],'y':round(row[8],3), 'drilldown':row[1]+' cost'})
        outer_data['outerData']['series'].append(temp_dict_outer)
        temp_dict_outer = {'name':'recovered','data':[]}
        for index, row in groupby_result.iterrows():
            temp_dict_outer['data'].append({'name':row[1],'y':round(row[9],3), 'drilldown':row[1]+' recovered'})
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

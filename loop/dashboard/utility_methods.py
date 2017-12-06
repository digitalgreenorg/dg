import MySQLdb
import pandas as pd
import numpy as np
from operator import itemgetter
from dg.settings import DATABASES

def read_kwargs(Kwargs):
    return Kwargs['country_id'], Kwargs['state_id'], Kwargs['start_date'], Kwargs['end_date'], Kwargs['aggregators_list'],Kwargs['mandis_list'],Kwargs['crops_list'],\
     Kwargs['gaddidars_list'], Kwargs['district_list']

def get_result(query) :

    database = DATABASES['default']['NAME']
    username = DATABASES['default']['USER']
    password = DATABASES['default']['PASSWORD']
    host = DATABASES['default']['HOST']
    port = DATABASES['default']['PORT']
    mysql_cn = MySQLdb.connect(host=host, port=port, user=username, passwd=password, db=database, charset='utf8', use_unicode=True)
    df_result = pd.read_sql(query, con=mysql_cn)
    return df_result

def convert_to_dict(df_result=None, groupby_result=None, graphname=None, outer_param=None, inner_param=None, isdrillDown=False, parameter=None, series_name=None):
    final_data_list = {}
    try:
        outer_data = {'outerData':{'series':[], 'categories':groupby_result[outer_param].tolist()}}
        # total_data = {'message' : series_name + ' : ' + str(groupby_result[parameter].sum())}
        temp_dict_outer = {'name':series_name,'data':[]}

        for index, row in groupby_result.iterrows():
            temp_dict_outer['data'].append({'name':row[1],'y':int(row[2]),'drilldown':row[1] + str(' ' + series_name)})

        outer_data['outerData']['series'].append(temp_dict_outer)
        final_data_list[graphname] = outer_data
        # final_data_list[graphname].update(total_data)
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
            temp_dict_inner['data'].append({'name':k,'y':round(v,2)})
        temp_dict_inner['data'].sort(key=itemgetter('y'),reverse=True)
        inner_data['innerData'].append(temp_dict_inner)

    return inner_data

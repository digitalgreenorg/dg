from django.db import connection
from django.template import Template, Context
import types
import datetime
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

def construct_query(var, context_dict):
    return Template(var).render(Context(context_dict))


#This abstracts away sql part to return everything by cursor.fetchall()
#which is a tuple of tuples containing rovalues
def run_query_raw(query_string, *query_args):
    if(not query_string):
        return ()
    cursor = connection.cursor()
    cursor.execute(query_string, query_args)
    return cursor.fetchall()

#This generates a list of dictionaries of key=column_header_name, value = row_value
def run_query(query_string, *query_args):
    if(not query_string):
        return []
    return_list = []
    cursor = connection.cursor()
    cursor.execute(query_string, query_args)
    col_names = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    for row in rows:
        return_list.append(dict(zip(col_names,row)))
    return return_list

#this returns
#{ dict_key : (tuple of remaing columns), ...}
#dict_key should be the first column in returned value.
def run_query_dict(query_string, dict_key, *query_args):
    if(not query_string):
        return {}
    return_list = {}
    cursor = connection.cursor()
    cursor.execute(query_string,query_args)
    col_names = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    if(dict_key != col_names[0]):
        raise Exception, dict_key+" is not the first column in returned query's column list"
    for row in rows:
        return_list[row[0]] = row[1:]

    return return_list

#this returns
#{ dict_key : [list of remaing columns], ...}
#dict_key should be the first column in returned value.
def run_query_dict_list(query_string, dict_key, *query_args):
    if(not query_string):
        return {}
    return_list = {}
    cursor = connection.cursor()
    cursor.execute(query_string,query_args)
    col_names = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    if(dict_key != col_names[0]):
        raise Exception, dict_key+" is not the first column in returned query's column list"
    for row in rows:
        return_list[row[0]] = list(row[1:])

    return return_list


def get_init_sql_ds():
    sql = {}
    sql['select'] = []; sql['from'] = []; sql['force index']=[];sql['where'] = []; sql['join'] = [];
    sql['lojoin'] = []; sql['group by'] = []; sql['order by'] = []; sql['having'] = [];
    return sql

def join_sql_ds(sql_ds):
    return_val = [];
    return_val.append("SELECT " + ', '.join(sql_ds['select']) \
               +"\nFROM " + ', '.join(sql_ds['from']))
    if(sql_ds['force index']):
        return_val.append("force index "+", ".join(sql_ds['force index']))
    if(sql_ds['join']):
        return_val.append("JOIN "+"\nJOIN ".join([' ON '.join(x) for x in sql_ds['join']]))
    if(sql_ds['lojoin']):
        return_val.append("LEFT OUTER JOIN "+"\nLEFT OUTER JOIN ".join([' ON '.join(x) for x in sql_ds['lojoin']]))
    if(sql_ds['where']):
        return_val.append("WHERE "+ " AND ".join(sql_ds['where']))
    if(sql_ds['group by']):
        return_val.append("GROUP BY "+", ".join(sql_ds['group by']))
    if(sql_ds['order by']):
        return_val.append("ORDER BY "+", ".join(sql_ds['order by']))
    if(sql_ds['having']):
        return_val.append("HAVING "+" AND ".join(sql_ds['having']))

    return '\n'.join(return_val)

def get_sql_result(query_dict):
    res = list(run_query_raw(query_dict['query_string']))[0][0]
    data_dict = {}
    data_dict[query_dict['query_tag']] = res
    return (query_dict['query_tag'], res)

def get_sql_result_api(query_dict):
    res = list(run_query_raw(query_dict['query_string']))[0][0]
    data_dict = {}
    # data_dict[query_dict['query_tag']] = res
    data_dict[query_dict['component']] = {
                                            'tagName':query_dict['query_tag'],
                                            'value':res,
                                            'placeHolder':query_dict['component']
                                        }
    return (data_dict[query_dict['component']])

def multiprocessing_dict(**Kwargs):
    args_list = Kwargs['query_list']
    pool = ThreadPool(4)
    results = dict(pool.map(get_sql_result, args_list))
    pool.close()
    pool.join()
    return results

def multiprocessing_list(**Kwargs):
    args_list = Kwargs['query_list']
    pool = ThreadPool(4)
    results = pool.map(get_sql_result_api, args_list)
    pool.close()
    pool.join()
    return results

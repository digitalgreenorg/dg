from dg.dashboard.models import *
from django.db import connection

def run_query(query_string, *query_args):
    return_list = []
    cursor = connection.cursor()
    cursor.execute(query_string, query_args)
    col_names = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    for row in rows:
        return_list.append(dict(zip(col_names,row)))
    return return_list

def run_query_dict(query_string, dict_key, *query_args):
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
        
        
        
        
        
from django.db import connection
from django.template import Template, Context
import types
import datetime

def construct_query(var, context_dict):
    return Template(var).render(Context(context_dict))


#This abstracts away sql part to return everything by cursor.fetchall()
#which is a tuple of tuples containing row-values
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

#Attaches geography tables to filter the pass 'geog' with given 'id'
#If Modified, shoudl use the first letter of table names( e.g B for BLOCK). Other functions depend on this.
    #sql_ds = datastructure of sql that will be modified (see get_init_sql_ds() above)
    #par_table_id = table's alias in the query, which has village foreign key
    #date_filter_field = field which will be use to attached date filter in case 'from_date' and 'to_date' is not None
def attach_geog_date(sql_ds,par_table_id,date_filter_field,geog,id,from_date,to_date):
    if(from_date and to_date):
        sql_ds['where'].append(date_filter_field +" BETWEEN '"+from_date+"' AND '"+to_date+"'")
    geog_list = ["VILLAGE","BLOCK","DISTRICT","STATE", "COUNTRY"];
    if(geog is None or geog not in geog_list):
        return

    if(type(id) == types.ListType):
        sql_ds['where'].append("%s.%s_id in (%s)" %(par_table_id, geog.lower(), ','.join(id)))
    else:
        sql_ds['where'].append("%s.%s_id = %s" %(par_table_id, geog.lower(), str(id)))

#Function to get from_date and to_date from Request object
def get_dates_partners(request):
    if(not request):
        return None, None, None
    if 'from_date' in request.GET and request.GET['from_date'] \
    and 'to_date' in request.GET and request.GET['to_date']:
        from_date = request.GET['from_date']
        to_date = request.GET['to_date']
    else:
        from_date = str(datetime.date.today() - datetime.timedelta(365));
        to_date = str(datetime.date.today());

    partner_id = request.GET.getlist('partners')
    return from_date, to_date, partner_id;

def filter_partner_geog_date(sql_ds,par_table_id,date_filter_field,geog,id,from_date,to_date,partner_id):
    if(partner_id):
        if(geog == None):
            partner_sql = ["SELECT id FROM DISTRICT WHERE partner_id in ("+','.join(partner_id)+")"]
            attach_geog_date(sql_ds,par_table_id,date_filter_field,'DISTRICT',partner_sql,from_date,to_date)
            return
        elif(geog=="STATE"  or geog=="COUNTRY"):
            dist_part = []
            if geog=="COUNTRY":
                dist_part = run_query_raw("SELECT DISTINCT partner_id FROM DISTRICT D JOIN STATE S ON S.id = D.state_id WHERE country_id = "+str(id))
            else:
                dist_part = run_query_raw("SELECT DISTINCT partner_id FROM DISTRICT WHERE state_id = "+str(id))
            dist_part_list = [str(x[0]) for x in dist_part if str(x[0]) in partner_id]
            if(dist_part_list):
                partner_sql = ["SELECT id FROM DISTRICT WHERE partner_id in ("+','.join(dist_part_list)+")"]
                sql_ds['where'].append("district_id in ("+partner_sql[0]+")")

    attach_geog_date(sql_ds,par_table_id,date_filter_field,geog,id,from_date,to_date)


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

import MySQLdb
import pandas as pd
import numpy as np

from dg.settings import DATABASES
from loop.utils.utility import get_init_sql_ds, join_sql_ds
from loop.constants.constants import *
from loop.models import CombinedTransaction
from loop.dashboard.utility_methods import *

def sql_query(**kwargs):
    country_id, state_id, start_date, end_date, aggregators_list, mandis_list, crops_list,\
     gaddidars_list, district_list = read_kwargs(kwargs)

    sql_ds = get_init_sql_ds()
    sql_ds['select'].append('lct.user_created_id aggregator_id, lu.name_en aggregator_name, date, crop_id, crop_name, mandi_id,\
                    mandi_name_en mandi_name, quantity, farmer_id, lf.name farmer_name')
    sql_ds['from'].append('loop_combinedtransaction lct')
    sql_ds['join'].append(['loop_mandi lm', 'lm.id = lct.mandi_id'])
    sql_ds['join'].append(['loop_crop lcrp', 'lcrp.id = lct.crop_id'])
    sql_ds['join'].append(['loop_farmer lf', 'lf.id = lct.farmer_id'])
    sql_ds['join'].append(['loop_loopuser lu', 'lu.user_id = lct.user_created_id and lu.role = ' + str(ROLE_CHOICE_AGGREGATOR)])
    sql_ds['join'].append(['loop_village lv','lv.id = lu.village_id'])
    sql_ds['join'].append(['loop_block lb','lb.id = lv.block_id'])
    sql_ds['join'].append(['loop_district ld', 'ld.id = lb.district_id'])
    sql_ds['join'].append(['loop_state ls', 'ls.id = ld.state_id'])
    sql_ds['join'].append(['loop_country lc', 'lc.id = ls.country_id'])

    if len(aggregators_list) > 0:
        sql_ds['where'].append('lct.user_created_id in (' + ",".join(aggregators_list) + ")")
    if len(mandis_list) > 0:
        sql_ds['where'].append('lm.id in (' + ",".join(mandis_list) + ')')
    if len(gaddidars_list) > 0:
        sql_ds['where'].append('lct.gaddidar_id in (' + ",".join(gaddidars_list) + ')')
    if len(district_list) > 0:
        sql_ds['where'].append('ld.id in (' + ",".join(district_list) + ')')
    if len(crops_list) > 0:
        sql_ds['where'].append('lcrp.id in (' + ",".join(crops_list) + ')')
    sql_ds['where'].append('lct.date between \'' + start_date + '\' and \'' + end_date + '\'')
    sql_ds['where'].append('country_id = ' + str(country_id))
    if(state_id) :
        sql_ds['where'].append('state_id = ' + str(state_id))

    query = join_sql_ds(sql_ds)
    df_result = get_result(query)
    return df_result

def query_myisam(**kwargs):

    # Constructing sql query
    sql_ds = get_init_sql_ds()
    sql_ds['select'].append('*')
    sql_ds['from'].append('loop_aggregated_myisam')
    sql_q = join_sql_ds(sql_ds)
    if(len(kwargs) > 0):
        country_id, state_id, start_date, end_date, aggregators_list, mandis_list, crops_list, \
        gaddidars_list, district_list = read_kwargs(kwargs)
        if len(aggregators_list) > 0:
            sql_ds['where'].append('aggregator_id in (' + ",".join(aggregators_list) + ")")
        if len(mandis_list) > 0:
            sql_ds['where'].append('mandi_id in (' + ",".join(mandis_list) + ')')
        if len(gaddidars_list) > 0:
            sql_ds['where'].append('gaddidar_id in (' + ",".join(gaddidars_list) + ')')
        if len(district_list) > 0:
            sql_ds['where'].append('district_id in (' + ",".join(district_list) + ')')
        if start_date != None:
            sql_ds['where'].append('date between \'' + start_date + '\' and \'' + end_date + '\'')
        sql_ds['where'].append('country_id = ' + str(country_id))
        if(state_id) :
            sql_ds['where'].append('state_id = ' + str(state_id))
    query = join_sql_ds(sql_ds)
    df_result = get_result(query)
    return df_result

def get_farmers_per_day(**kwargs):
    country_id, state_id, start_date, end_date, aggregators_list, mandis_list, crops_list,\
     gaddidars_list, district_list = read_kwargs(kwargs)

    # Constructing sql query
    sql_ds = get_init_sql_ds()
    sql_ds['select'].append('lct.date,count(distinct(lct.farmer_id)) as farmer_count')
    sql_ds['from'].append('loop_combinedtransaction lct')
    sql_ds['join'].append(['loop_mandi lm', 'lm.id = lct.mandi_id'])
    sql_ds['join'].append(['loop_crop lcrp', 'lcrp.id = lct.crop_id'])
    sql_ds['join'].append(['loop_farmer lf', 'lf.id = lct.farmer_id'])
    sql_ds['join'].append(['loop_loopuser lu', 'lu.user_id = lct.user_created_id and lu.role = ' + str(ROLE_CHOICE_AGGREGATOR)])
    sql_ds['join'].append(['loop_village lv','lv.id = lu.village_id'])
    sql_ds['join'].append(['loop_block lb','lb.id = lv.block_id'])
    sql_ds['join'].append(['loop_district ld', 'ld.id = lb.district_id'])
    sql_ds['join'].append(['loop_state ls', 'ls.id = ld.state_id'])
    sql_ds['join'].append(['loop_country lc', 'lc.id = ls.country_id'])
    sql_ds['group by'].append('date')

    if len(aggregators_list) > 0:
        sql_ds['where'].append('lct.user_created_id in (' + ",".join(aggregators_list) + ")")
    if len(mandis_list) > 0:
        sql_ds['where'].append('lm.id in (' + ",".join(mandis_list) + ')')
    if len(crops_list) > 0:
        sql_ds['where'].append('lcrp.id in (' + ",".join(crops_list) + ')')
    if len(district_list) > 0:
        sql_ds['where'].append('ld.id in (' + ",".join(district_list) + ')')
    sql_ds['where'].append('lct.date between \'' + start_date + '\' and \'' + end_date + '\'')
    sql_ds['where'].append('country_id = ' + str(country_id))
    if(state_id) :
        sql_ds['where'].append('state_id = ' + str(state_id))

    query = join_sql_ds(sql_ds)
    df_result = get_result(query)
    return df_result

def crop_prices_query(from_timeseries, **kwargs):
    country_id, state_id, start_date, end_date, aggregators_list, mandis_list, crops_list,\
     gaddidars_list, district_list = read_kwargs(kwargs)

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
    sql_ds['join'].append(['loop_village lv','lv.id = lu.village_id'])
    sql_ds['join'].append(['loop_block lb','lb.id = lv.block_id'])
    sql_ds['join'].append(['loop_district ld', 'ld.id = lb.district_id'])
    sql_ds['join'].append(['loop_state ls', 'ls.id = ld.state_id'])
    sql_ds['join'].append(['loop_country lc', 'lc.id = ls.country_id'])

    if len(aggregators_list) > 0:
        sql_ds['where'].append('lct.user_created_id in (' + ",".join(aggregators_list) + ")")
    if len(mandis_list) > 0:
        sql_ds['where'].append('lm.id in (' + ",".join(mandis_list) + ')')
    if len(district_list) > 0:
        sql_ds['where'].append('ld.id in (' + ",".join(district_list) + ')')
    if len(gaddidars_list) > 0:
        sql_ds['where'].append('lct.gaddidar_id in (' + ",".join(gaddidars_list) + ')')
    if len(crops_list) > 0:
        sql_ds['where'].append('lcrp.id in (' + ",".join(crops_list) + ')')
    sql_ds['where'].append('lct.date between \'' + start_date + '\' and \'' + end_date + '\'')
    sql_ds['where'].append('country_id = ' + str(country_id))
    if(state_id) :
        sql_ds['where'].append('state_id = ' + str(state_id))

    query = join_sql_ds(sql_ds)

    df_result = get_result(query)
    return df_result

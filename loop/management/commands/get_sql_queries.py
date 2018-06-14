# from training.management.databases.utility import get_init_sql_ds, join_sql_ds

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


def get_cluster_sql() :
    sql_ds = get_init_sql_ds()
    sql_ds['select'].append('count(distinct llp.user_id)')
    sql_ds['from'].append('loop_loopuser llp')
    return sql_ds

def get_farmer_sql() :
    sql_ds = get_init_sql_ds()
    sql_ds['select'].append('count(distinct CT.farmer_id)')
    sql_ds['from'].append('loop_combinedtransaction CT')
    return sql_ds

def get_volume_sql() :
    sql_ds = get_init_sql_ds()
    sql_ds['select'].append('sum(lam.quantity)')
    sql_ds['from'].append('loop_aggregated_myisam lam')
    return sql_ds

def get_payment_sql() :
    sql_ds = get_init_sql_ds()
    sql_ds['select'].append('SUM(lam.amount)')
    sql_ds['from'].append('loop_aggregated_myisam lam')
    return sql_ds


def get_cluster_related_sql() :

    args_list = []

    # Cluster related sql

    args_dict = {}
    sql_ds = get_init_sql_ds()
    sql_ds['select'].append('*')
    sql_ds['from'].append('loop_aggregated_myisam lam')

    sql_q = join_sql_ds(sql_ds)

    return sql_q


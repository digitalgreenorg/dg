from training.management.databases.utility import get_init_sql_ds, join_sql_ds

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


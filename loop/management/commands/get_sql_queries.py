from training.management.databases.utility import get_init_sql_ds, join_sql_ds

def get_cluster_sql() :
    sql_ds = get_init_sql_ds()
    sql_ds['select'].append('select count(*)')
    sql_ds['from'].append('')
    return sql_ds

def get_farmers_sql() :
    sql_ds = get_init_sql_ds()
    sql_ds['select'].append('select count(*)')
    sql_ds['from'].append('')
    return sql_ds

def get_volume_sql() :
    sql_ds = get_init_sql_ds()
    sql_ds['select'].append('select count(*)')
    sql_ds['from'].append('')
    return sql_ds

def get_payment_sql() :
    sql_ds = get_init_sql_ds()
    sql_ds['select'].append('select count(*)')
    sql_ds['from'].append('')
    return sql_ds

gvimport MySQLdb

mysql_cn = MySQLdb.connect(host='localhost', port=3306, user='root',
                           passwd='root',
                           db='digitalgreen_local_21 aug',
                           charset='utf8',
                           use_unicode=True)

def onrun_query(query):
    cursor = mysql_cn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return result


daily_aggregator_crop_query = 'SELECT ct.date, ct.user_created_id, ct.mandi_id, ct.crop_id, SUM(ct.quantity), ls.id FROM ' \
                              'loop_combinedtransaction ct LEFT JOIN loop_farmer f ON f.id = ct.farmer_id ' \
                              'join loop_village as lv on lv.id=f.village_id join loop_block as lb on lb.id=lv.block_id ' \
                              'join loop_district as ld on ld.id=lb.district_id join loop_state as ls on ls.id=ld.state_id ' \
                              'GROUP BY ct.date , ct.crop_id , ct.user_created_id, ct.mandi_id '
daily_aggregator_crop_query_result = onrun_query(daily_aggregator_crop_query)

daily_crop_market_query = 'SELECT ct.date, ct.mandi_id, ct.crop_id, SUM(ct.quantity), SUM(ct.amount) / SUM(ct.quantity), ls.id ' \
                          'FROM loop_combinedtransaction ct LEFT JOIN loop_farmer f ON f.id = ct.farmer_id ' \
                          'join loop_village as lv on lv.id=f.village_id join loop_block as lb on lb.id=lv.block_id ' \
                          'join loop_district as ld on ld.id=lb.district_id join loop_state as ls on ls.id=ld.state_id ' \
                          'GROUP BY date , crop_id , mandi_id '
daily_crop_market_query_result = onrun_query(daily_crop_market_query)

daily_aggregator_sales_query = 'SELECT ct.date, ct.user_created_id, ct.mandi_id, SUM(ct.quantity), SUM(ct.amount), ls.id ' \
                               'FROM loop_combinedtransaction ct LEFT JOIN loop_farmer f ON f.id = ct.farmer_id ' \
                               'join loop_village as lv on lv.id=f.village_id join loop_block as lb on lb.id=lv.block_id ' \
                               'join loop_district as ld on ld.id=lb.district_id join loop_state as ls on ls.id=ld.state_id ' \
                               'GROUP BY date, user_created_id, mandi_id'
daily_aggregator_sales_query_result = onrun_query(daily_aggregator_sales_query)

# This file extracts data from SQL and converts them into required Panda data frames

import MySQLdb
import pandas as pd
import sys
import os
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.extend([DIR_PATH+"/../../"])
#from dg.settings import DATABASES
# import Crop_Rate_Analysis
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'digital_green_30_aug',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': 3306
    }
}

database = DATABASES['default']['NAME']
username = DATABASES['default']['USER']
password = DATABASES['default']['PASSWORD']
host = DATABASES['default']['HOST']
port = DATABASES['default']['PORT']

mysql_cn = MySQLdb.connect(host=host, port=port, user=username,
                           passwd=password,
                           db=database,
                           charset='utf8',
                           use_unicode=True)

def onrun_query(query):
    cursor = mysql_cn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return result
#
#columnlist_ct = ['Date', 'Aggregator', 'Market Real', 'Crop_1', 'Quantity Real', 'State']
#daily_aggregator_crop_data = outlier_ct_data.groupby(['Date', 'Aggregator', 'Market Real', 'Crop_1'])
#     pd.DataFrame(daily_aggregator_crop_query_result, columns= columnlist_ct)
# daily_aggregator_crop_data = daily_aggregator_crop_data[daily_aggregator_crop_data['State'] == 1]

# Purpose: To story daily quantity given by farmers. Predicted cost and time for transactions will depend on this.
# TODO: Won't work if a farmer gives produce to multiple aggregators in a day. Fix.
daily_farmer_quantity_query = 'SELECT date, user_created_id, farmer_id, SUM(quantity)FROM loop_combinedtransaction GROUP BY date , ' \
                               'user_created_id, farmer_id '
daily_farmer_quantity_query_result = onrun_query(daily_farmer_quantity_query)
columnlist = ['Date', 'Aggregator', 'Farmer', 'Farmer_Quantity']
daily_farmer_quantity_data = pd.DataFrame(list(daily_farmer_quantity_query_result), columns= columnlist)
daily_farmer_quantity_data['Date'] = pd.to_datetime(daily_farmer_quantity_data['Date'])

# Purpose: To get TCPK and FSPK for each D-A-M combination which will be later mapped to each transaction.
# Assumption: TC, AC and FS are uniform for every kg of a D-A-M combination. FS might depend on CA in future.
# Quantity isn't necessary. Just a temp variable to get others.
# ACPK is not added anywhere right now.
daily_aggregator_market_query = 'SELECT ct.date, ct.user_created_id, ct.mandi_id, SUM(ct.quantity) AS Q, dayt.TC, dayt.TC / SUM(' \
                  'ct.quantity), dayt.FS, dayt.FS / SUM(ct.quantity) FROM loop_combinedtransaction ct LEFT JOIN (SELECT dt.date D, ' \
                  'dt.user_created_id A, dt.mandi_id M, SUM(dt.transportation_cost) TC, SUM(dt.farmer_share) / COUNT(' \
                  'dt.id) FS, COUNT(dt.id) Vehicle_Count FROM loop_daytransportation dt GROUP BY dt.date , dt.user_created_id , dt.mandi_id) dayt ' \
                  'ON dayt.D = ct.date AND ct.mandi_id = dayt.M AND dayt.A = ct.user_created_id GROUP BY ct.date , ' \
                  'ct.user_created_id , ct.mandi_id'
daily_aggregator_market_query_result = onrun_query(daily_aggregator_market_query)
columnlist = ['Date', 'Aggregator', 'Market', 'Quantity','Transport_Cost', 'TCPK', 'Farmer_Share', 'FSPK']
daily_aggregator_market_data = pd.DataFrame(list(daily_aggregator_market_query_result), columns= columnlist)
daily_aggregator_market_data['Date'] = pd.to_datetime(daily_aggregator_market_data['Date'])


# Purpose: To have data for each transaction. Every data (ACPK, TCPK, FSPK, Predicted...) will be mapped on this level.
transaction_level_data_query = 'SELECT id, date, user_created_id, mandi_id, gaddidar_id, farmer_id, crop_id, quantity, price, amount ' \
                               'FROM loop_combinedtransaction'
transaction_level_data_query_result = onrun_query(transaction_level_data_query)
columnlist = ['ID', 'Date', 'Aggregator', 'Market', 'Gaddidar', 'Farmer', 'Crop', 'Quantity', 'Price', 'Amount']
daily_transaction_data = pd.DataFrame(list(transaction_level_data_query_result), columns= columnlist)
daily_transaction_data['Date'] = pd.to_datetime(daily_transaction_data['Date'])

aggregator_market_query = 'SELECT ct.user_created_id, ct.mandi_id, SUM(ct.quantity), COUNT(DISTINCT ct.date) FROM loop_combinedtransaction ct GROUP BY ct.user_created_id , ct.mandi_id'
aggregator_market_query_result = onrun_query(aggregator_market_query)
columnlist = ['Aggregator', 'Market', 'Total_Quantity', 'Visits']
aggregator_market_data = pd.DataFrame(list(aggregator_market_query_result), columns=columnlist)

daily_aggregator_crop_query = 'SELECT ct.date, ct.user_created_id, ct.mandi_id, ct.crop_id, SUM(ct.quantity), ls.id FROM ' \
                              'loop_combinedtransaction ct LEFT JOIN loop_farmer f ON f.id = ct.farmer_id ' \
                              'join loop_village as lv on lv.id=f.village_id join loop_block as lb on lb.id=lv.block_id ' \
                              'join loop_district as ld on ld.id=lb.district_id join loop_state as ls on ls.id=ld.state_id ' \
                              'GROUP BY ct.date , ct.crop_id , ct.user_created_id, ct.mandi_id, ls.id '
daily_aggregator_crop_query_result = onrun_query(daily_aggregator_crop_query)
columnlist = ['Date', 'Aggregator', 'Market Real', 'Crop_1', 'Quantity Real', 'State']
daily_aggregator_crop_data = pd.DataFrame(list(daily_aggregator_crop_query_result), columns= columnlist)
daily_aggregator_crop_data['Date'] = pd.to_datetime(daily_aggregator_crop_data['Date'])

daily_crop_market_query = 'SELECT ct.date, ct.mandi_id, ct.crop_id, SUM(ct.quantity), SUM(ct.amount) / SUM(ct.quantity), ls.id ' \
                          'FROM loop_combinedtransaction ct LEFT JOIN loop_farmer f ON f.id = ct.farmer_id ' \
                          'join loop_village as lv on lv.id=f.village_id join loop_block as lb on lb.id=lv.block_id ' \
                          'join loop_district as ld on ld.id=lb.district_id join loop_state as ls on ls.id=ld.state_id ' \
                          'GROUP BY ct.date , ct.crop_id , ct.mandi_id, ls.id '
daily_crop_market_query_result = onrun_query(daily_crop_market_query)
columnlist = ['Date', 'Market', 'Crop_2', 'Total_Quantity', 'Av Rate', 'State']
daily_market_crop_data = pd.DataFrame(list(daily_crop_market_query_result), columns=columnlist)
daily_market_crop_data['Date'] = pd.to_datetime(daily_market_crop_data['Date'])

daily_aggregator_sales_query = 'SELECT ct.date, ct.user_created_id, ct.mandi_id, SUM(ct.quantity), SUM(ct.amount), ls.id ' \
                               'FROM loop_combinedtransaction ct LEFT JOIN loop_farmer f ON f.id = ct.farmer_id ' \
                               'join loop_village as lv on lv.id=f.village_id join loop_block as lb on lb.id=lv.block_id ' \
                               'join loop_district as ld on ld.id=lb.district_id join loop_state as ls on ls.id=ld.state_id ' \
                               'GROUP BY ct.date, ct.user_created_id, ct.mandi_id, ls.id'
daily_aggregator_sales_query_result = onrun_query(daily_aggregator_sales_query)
columnlist = ['Date', 'Aggregator', 'Market Real', 'Daily_Quantity', 'Daily_Amount', 'State']
daily_aggregator_data = pd.DataFrame(list(daily_aggregator_sales_query_result), columns= columnlist)
daily_aggregator_data['Date'] = pd.to_datetime(daily_aggregator_data['Date'])


daily_aggregator_market_crop_rate_query = 'SELECT ct.date, ct.user_created_id, ct.mandi_id, ct.crop_id, ct.quantity, ct.price, ct.amount, ls.id FROM ' \
                                          'loop_combinedtransaction ct LEFT JOIN loop_farmer f ON f.id = ct.farmer_id ' \
                                          'join loop_village as lv on lv.id=f.village_id join loop_block as lb on lb.id=lv.block_id ' \
                                          'join loop_district as ld on ld.id=lb.district_id join loop_state as ls on ls.id=ld.state_id '
daily_aggregator_market_crop_rate_query_result = onrun_query(daily_aggregator_market_crop_rate_query)

daily_aggregator_market_farmer_crop_rate_query = 'SELECT ct.date, ct.user_created_id, ct.mandi_id, ct.farmer_id, ct.crop_id, ct.quantity, ct.price, ct.amount, ls.id FROM ' \
                                          'loop_combinedtransaction ct LEFT JOIN loop_farmer f ON f.id = ct.farmer_id ' \
                                          'join loop_village as lv on lv.id=f.village_id join loop_block as lb on lb.id=lv.block_id ' \
                                          'join loop_district as ld on ld.id=lb.district_id join loop_state as ls on ls.id=ld.state_id '
daily_aggregator_market_farmer_crop_rate_query_result = onrun_query(daily_aggregator_market_crop_rate_query)


daily_transport_vehicle_query = 'SELECT dt.date, dt.user_created_id, dt.mandi_id, dt.id, tv.vehicle_id, ' \
                                'v.vehicle_name_en, dt.transportation_cost, SUM(ct.quantity), s.id ' \
                                'FROM loop_daytransportation dt LEFT JOIN ' \
                                'loop_combinedtransaction ct ON ct.date = dt.date AND ' \
                                'ct.user_created_id = dt.user_created_id AND ct.mandi_id = dt.mandi_id LEFT JOIN ' \
                                'loop_transportationvehicle tv ON dt.transportation_vehicle_id = tv.id LEFT JOIN ' \
                                'loop_vehicle v ON v.id = tv.vehicle_id LEFT JOIN loop_loopuser u ON ' \
                                'u.user_id = dt.user_created_id LEFT JOIN loop_village vi ON vi.id = u.village_id ' \
                                'LEFT JOIN loop_block b ON b.id = vi.block_id LEFT JOIN loop_district d ON ' \
                                'd.id = b.district_id LEFT JOIN loop_state s ON s.id = d.state_id GROUP BY dt.id'
daily_transport_vehicle_query_result = onrun_query(daily_transport_vehicle_query)
columnlist = ['Date', 'Aggregator', 'Market', 'DT_ID', 'Vehicle_ID', 'Vehicle_Name','Transport_Cost','Quantity', 'State' ]
daily_transportation_data = pd.DataFrame(list(daily_transport_vehicle_query_result), columns= columnlist)


aggregator_query = 'SELECT u.user_id, u.name_en, ld.district_name, ls.id, ls.state_name_en FROM loop_loopuser u JOIN ' \
                    'loop_village AS lv ON lv.id = u.village_id JOIN loop_block AS lb ON lb.id = lv.block_id JOIN ' \
                    'loop_district AS ld ON ld.id = lb.district_id JOIN loop_state AS ls ON ls.id = ld.state_id '
aggregator_query_result = onrun_query(aggregator_query)
columnlist = ['Aggregator', 'Aggregator_Name', 'District_Name','State_ID', 'State_Name']
aggregator_list = pd.DataFrame(list(aggregator_query_result), columns= columnlist)

market_query = 'select m.id, m.mandi_name_en from loop_mandi m'
market_query_result = onrun_query(market_query)
columnlist = ['Market', 'Market_Name']
market_list = pd.DataFrame(list(market_query_result), columns= columnlist)

vehicle_query = 'select v.id, v.vehicle_name_en from loop_vehicle v'
vehicle_query_result = onrun_query(vehicle_query)
columnlist = ['ID', 'Name']
vehicle_data = pd.DataFrame(list(vehicle_query_result), columns= columnlist)

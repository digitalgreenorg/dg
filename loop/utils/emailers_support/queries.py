__author__ = 'Lokesh'

import MySQLdb
from dg.settings import DATABASES

mysql_cn = MySQLdb.connect(host=DATABASES['default']['HOST'], port=DATABASES['default']['PORT'], user=DATABASES['default']['USER'],
                           passwd=DATABASES['default']['PASSWORD'],
                           db=DATABASES['default']['NAME'],
                           charset='utf8',
                           use_unicode=True)


def onrun_query(query):
    cursor = mysql_cn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return result


daily_a_m_transport_share_query = '''SELECT
                    ct.user_created_id,
                    ct.mandi_id,
                    ct.date,
                    u.name_en,
                    m.mandi_name_en,
                    SUM(ct.quantity) AS Q,
                    dayt.TC,
                    'okay',
                    dayt.TC / SUM(ct.quantity)
                FROM
                    loop_combinedtransaction ct
                        LEFT JOIN
                    loop_loopuser u ON u.user_id = ct.user_created_id
                        LEFT JOIN
                    loop_mandi m ON m.id = ct.mandi_id
                        LEFT JOIN
                    (SELECT
                        dt.date D,
                            dt.user_created_id A,
                            dt.mandi_id M,
                            SUM(dt.transportation_cost) TC,
                            SUM(dt.farmer_share) / COUNT(dt.id) FS
                    FROM
                        loop_daytransportation dt
                    GROUP BY dt.date , dt.user_created_id , dt.mandi_id) dayt ON dayt.D = ct.date
                        AND ct.mandi_id = dayt.M
                        AND dayt.A = ct.user_created_id
                WHERE
                    u.role = 2
                GROUP BY ct.date , ct.user_created_id , ct.mandi_id
                ORDER BY ct.user_created_id , ct.mandi_id , dayt.TC / SUM(ct.quantity)'''

daily_a_m_farmerShare_query = '''SELECT
                            ct.user_created_id,
                            ct.mandi_id,
                            ct.date,
                            u.name_en,
                            m.mandi_name_en,
                            SUM(ct.quantity) AS Q,
                            dayt.TC,
                            dayt.FS,
                            dayt.FS / SUM(ct.quantity),
                            dayt.FS / dayt.TC
                        FROM
                            loop_combinedtransaction ct
                                LEFT JOIN
                            loop_loopuser u ON u.user_id = ct.user_created_id
                                LEFT JOIN
                            loop_mandi m ON m.id = ct.mandi_id
                                LEFT JOIN
                            (SELECT
                                dt.date D,
                                    dt.user_created_id A,
                                    dt.mandi_id M,
                                    SUM(dt.transportation_cost) TC,
                                    SUM(dt.farmer_share) / COUNT(dt.id) FS
                            FROM
                                loop_daytransportation dt
                            GROUP BY dt.date , dt.user_created_id , dt.mandi_id) dayt ON dayt.D = ct.date
                                AND ct.mandi_id = dayt.M
                                AND dayt.A = ct.user_created_id
                        WHERE
                            u.role = 2
                        GROUP BY ct.date , ct.user_created_id , ct.mandi_id
                        ORDER BY ct.user_created_id , ct.mandi_id , ct.date'''

a_m_count_query = '''SELECT
                    ct.user_created_id A,
                    ct.mandi_id M,
                    u.name_en,
                    m.mandi_name_en,
                    COUNT(DISTINCT ct.date)
                FROM
                    loop_combinedtransaction ct
                        LEFT JOIN
                    loop_loopuser u ON u.user_id = ct.user_created_id
                        LEFT JOIN
                    loop_mandi m ON m.id = ct.mandi_id
                WHERE
                    u.role = 2
                GROUP BY ct.user_created_id , ct.mandi_id
                ORDER BY ct.user_created_id , ct.mandi_id'''

query_for_incorrect_phone_all_per_aggregator = '''SELECT
                                Aggregator,
                                Village,
                                Farmer_ID,
                                Farmer,
                                t1.Farmer_Frequency,
                                Mobile_Number,
                                t3.Mobile_Frequency
                            FROM
                                (SELECT
                                    user_created_id,
                                        farmer_id f_id,
                                        COUNT(DISTINCT (date)) Farmer_Frequency
                                FROM
                                    loop_combinedtransaction lct
                                WHERE
                                    lct.date BETWEEN \'%s\' AND \'%s\'
                                GROUP BY user_created_id , farmer_id
                                HAVING Farmer_Frequency > 0) t1
                                    JOIN
                                (SELECT
                                    ll.name Aggregator,
                                        ll.id Loop_user_id,
                                        ll.user_id user_id,
                                        lv.village_name Village,
                                        lf.id Farmer_ID,
                                        lf.name Farmer,
                                        lf.phone Mobile_Number
                                FROM
                                    loop_loopuser ll
                                JOIN loop_loopuserassignedvillage llv ON ll.id = llv.loop_user_id
                                JOIN loop_farmer lf ON lf.village_id = llv.village_id
                                JOIN loop_village lv ON lf.village_id = lv.id
                                WHERE
                                    ll.role = 2 %s) t2 ON t1.f_id = t2.Farmer_ID
                                    AND t1.user_created_id = t2.user_id
                                    JOIN
                                (SELECT
                                        ll.user_id Loop_user,
                                        lf.phone Phone_no,
                                        COUNT(lf.phone) Mobile_Frequency
                                FROM
                                 loop_loopuser ll join
                                    loop_loopuserassignedvillage llv on ll.id=llv.loop_user_id
                                JOIN loop_farmer lf ON lf.village_id = llv.village_id
                                JOIN loop_village lv ON lf.village_id = lv.id
                                WHERE
                                    llv.loop_user_id <> 22
                                        AND lf.id IN (SELECT
                                            farmer_id
                                        FROM
                                            loop_combinedtransaction ct
                                        WHERE
                                        user_created_id=ll.user_id and
                                            date BETWEEN \'%s\' AND \'%s\' )
                                GROUP BY ll.user_id , lf.phone ) t3 ON t2.Mobile_Number = t3.Phone_no
                                    AND t3.Loop_user = t2.user_id
                            HAVING (t3.Mobile_Frequency > 1)
                                OR (t3.Mobile_Frequency = 1
                                AND (Mobile_Number <= 7000000000
                                OR Mobile_Number >= 9999999999))
                            ORDER BY Aggregator ASC, CAST(Mobile_Number AS signed) ASC'''


query_for_incorrect_phone_all_per_district = '''SELECT 
                District_name,
                Aggregator,
                Village,
                Farmer_ID,
                Farmer,
                t1.Farmer_Frequency,
                Mobile_Number,
                t3.Mobile_Frequency
            FROM
                (SELECT 
                    ld.id d_id,
                        ld.district_name_en District_name,
                        lct.user_created_id,
                        farmer_id f_id,
                        COUNT(DISTINCT (date)) Farmer_Frequency
                FROM
                    loop_combinedtransaction lct
                JOIN loop_farmer lf ON lf.id = lct.farmer_id
                JOIN loop_village lv ON lv.id = lf.village_id
                JOIN loop_block lb ON lb.id = lv.block_id
                JOIN loop_district ld ON ld.id = lb.district_id
                WHERE
                    lct.date BETWEEN \'%s\' AND \'%s\'
                GROUP BY d_id , lct.user_created_id , farmer_id
                HAVING Farmer_Frequency > 0) t1
                    JOIN
                (SELECT 
                    ld.id d_id,
                        ld.district_name_en,
                        ll.name Aggregator,
                        ll.id Loop_user_id,
                        ll.user_id user_id,
                        lv.village_name Village,
                        lf.id Farmer_ID,
                        lf.name Farmer,
                        lf.phone Mobile_Number
                FROM
                    loop_loopuser ll
                JOIN loop_loopuserassignedvillage llv ON ll.id = llv.loop_user_id
                JOIN loop_farmer lf ON lf.village_id = llv.village_id
                JOIN loop_village lv ON lf.village_id = lv.id
                JOIN loop_block lb ON lb.id = lv.block_id
                JOIN loop_district ld ON ld.id = lb.district_id
                WHERE
                    ll.role = 2 %s) t2 ON t1.f_id = t2.Farmer_ID
                    AND t1.user_created_id = t2.user_id
                    AND t1.d_id = t2.d_id
                    JOIN
                (SELECT 
                    ld.id d_id,
                        ld.district_name_en,
                        ll.user_id Loop_user,
                        lf.phone Phone_no,
                        COUNT(lf.phone) Mobile_Frequency
                FROM
                    loop_loopuser ll
                JOIN loop_loopuserassignedvillage llv ON ll.id = llv.loop_user_id
                JOIN loop_farmer lf ON lf.village_id = llv.village_id
                JOIN loop_village lv ON lf.village_id = lv.id
                JOIN loop_block lb ON lb.id = lv.block_id
                JOIN loop_district ld ON ld.id = lb.district_id
                WHERE
                    llv.loop_user_id <> 22
                        AND lf.id IN (SELECT 
                            farmer_id
                        FROM
                            loop_combinedtransaction ct
                        WHERE
                            user_created_id = ll.user_id
                                AND date BETWEEN \'%s\' AND \'%s\')
                GROUP BY d_id , ll.user_id , lf.phone) t3 ON t2.Mobile_Number = t3.Phone_no
                    AND t3.Loop_user = t2.user_id
                    AND t3.d_id = t2.d_id
            HAVING (t3.Mobile_Frequency > 1)
                OR (t3.Mobile_Frequency = 1
                AND (Mobile_Number <= 7000000000
                OR Mobile_Number >= 9999999999))
            ORDER BY District_name ASC , Aggregator ASC , CAST(Mobile_Number AS SIGNED) ASC
''' 

query_for_farmer_transaction_all_single_aggregator = '''
                                  SELECT
                                t1.Agg,
                                t1.date,
                                t1.Mandi,
                                t1.Farmer,
                                Total_Quantity,
                                Total_Amount,
                                ts / tv * Total_Quantity fs,
                                Total_Amount - (ts / tv * Total_Quantity) Net_Amount
                            FROM
                                (SELECT
                                    lct.user_created_id Agg,
                                        date,
                                        lm.mandi_name Mandi,
                                        lf.name Farmer,
                                        SUM(quantity) Total_Quantity,
                                        SUM(amount) Total_Amount
                                FROM
                                    loop_combinedtransaction lct
                                JOIN loop_farmer lf ON lf.id = lct.farmer_id
                                JOIN loop_mandi lm ON lct.mandi_id = lm.id
                                GROUP BY Agg , date , Mandi , lct.farmer_id) t1
                                    JOIN
                                (SELECT
                                    t2.user_ User_id,
                                        t2.date Date_,
                                        t2.mandi Mandi_,
                                        t2.Total_Volume tv,
                                        t3.Share_ ts
                                FROM
                                    (SELECT
                                    lct.user_created_id user_,
                                        date,
                                        lm.mandi_name mandi,
                                        SUM(quantity) Total_Volume
                                FROM
                                    loop_combinedtransaction lct
                                JOIN loop_mandi lm ON lm.id = lct.mandi_id
                                GROUP BY user_ , date , lct.mandi_id) t2
                                JOIN (SELECT
                                    dt.user_created_id,
                                        date,
                                        lm.mandi_name mandi_,
                                        AVG(farmer_share) Share_
                                FROM
                                    loop_daytransportation dt
                                JOIN loop_mandi lm ON dt.mandi_id = lm.id
                                GROUP BY user_created_id , date , dt.mandi_id) t3 ON t2.user_ = t3.user_created_id
                                    AND t2.date = t3.date
                                    AND t2.mandi = t3.mandi_) t4 ON t1.Agg = t4.User_id
                                    AND t1.date = t4.Date_
                                    AND t1.Mandi = t4.Mandi_
                            WHERE
                                t1.date BETWEEN \'%s\' AND \'%s\' %s'''







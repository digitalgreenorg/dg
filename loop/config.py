 # -*- coding: utf-8 -*-

DEFAULT_COLUMN_WIDTH = 9

header_dict_for_loop_email_mobile_numbers = [{'column_width': 15,
                                          'label': 'क्रम संख्या',
                                          },
                                         {'column_width': 15,
                                          
                                          'label': 'जमाकर्ता का नाम',
                                          },
                                         {'column_width': 15,
                                          'label': 'गांव का नाम',
                                          },
                                         {'column_width': 15,
                                          'label': 'किसान ID',
                                          },
                                         {'column_width': 15,
                                          'label': 'किसान का नाम',
                                          },
                                         {'column_width': 15,
                                          'label': 'मोबाइल नं',
                                          },
                                          {'column_width': 15,
                                          'label': 'सब्जी कितने दिन दी?',
                                          },
                                          {'column_width': 15,
                                          'label': 'कितने किसान में नंबर डला है?',
                                          }]


query_for_all_aggregator = '''SELECT 
                                Aggregator,
                                Village,
                                Farmer_ID,
                                Farmer,
                                Mobile_Number,
                                t1.Farmer_Frequency,
                                t3.Mobile_Frequency
                            FROM
                                (SELECT 
                                    user_created_id,
                                        farmer_id f_id,
                                        COUNT(distinct(date)) Farmer_Frequency
                                FROM
                                    loop_combinedtransaction lct
                                WHERE
                                    lct.date BETWEEN %s AND %s
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
                                    ll.name <> 'Loop Test') t2 ON t1.f_id = t2.Farmer_ID
                                    AND t1.user_created_id = t2.user_id
                                    JOIN
                                (SELECT 
                                    llv.loop_user_id Loop_user,
                                        lf.phone Phone_no,
                                        COUNT(lf.phone) Mobile_Frequency
                                FROM
                                    loop_loopuserassignedvillage llv
                                JOIN loop_farmer lf ON lf.village_id = llv.village_id
                                JOIN loop_village lv ON lf.village_id = lv.id
                                WHERE
                                    llv.loop_user_id <> 22
                                GROUP BY llv.loop_user_id , lf.phone) t3 ON t2.Mobile_Number = t3.Phone_no
                                    AND t3.Loop_user = t2.Loop_user_id
                            HAVING (t3.Mobile_Frequency > 1)
                                OR (t3.Mobile_Frequency = 1
                                AND (Mobile_Number <= 7000000000
                                OR Mobile_Number >= 9999999999))
                            ORDER BY Aggregator'''



query_for_single_aggregator = '''SELECT 
                                  Aggregator,
                                  Village,
                                  Farmer_ID,
                                  Farmer,
                                  Mobile_Number,
                                  t1.Farmer_Frequency,
                                  t3.Mobile_Frequency
                              FROM
                                  (SELECT 
                                      user_created_id,
                                          farmer_id f_id,
                                          COUNT(distinct(date)) Farmer_Frequency
                                  FROM
                                      loop_combinedtransaction lct
                                  WHERE
                                      lct.date BETWEEN %s AND %s
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
                                      ll.name <> 'Loop Test' and ll.name = \'%s\') t2 ON t1.f_id = t2.Farmer_ID
                                      AND t1.user_created_id = t2.user_id
                                      JOIN
                                  (SELECT 
                                      llv.loop_user_id Loop_user,
                                          lf.phone Phone_no,
                                          COUNT(lf.phone) Mobile_Frequency
                                  FROM
                                      loop_loopuserassignedvillage llv
                                  JOIN loop_farmer lf ON lf.village_id = llv.village_id
                                  JOIN loop_village lv ON lf.village_id = lv.id
                                  WHERE
                                      llv.loop_user_id <> 22
                                  GROUP BY llv.loop_user_id , lf.phone) t3 ON t2.Mobile_Number = t3.Phone_no
                                      AND t3.Loop_user = t2.Loop_user_id
                              HAVING (t3.Mobile_Frequency > 1)
                                  OR (t3.Mobile_Frequency = 1
                                  AND (Mobile_Number <= 7000000000
                                  OR Mobile_Number >= 9999999999))
                              ORDER BY Aggregator'''


RECIPIENTS = ['amandeep@digitalgreen.org', 'lokesh@digitalgreen.org']


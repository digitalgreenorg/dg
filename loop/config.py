 # -*- coding: utf-8 -*-


HEADER_STRING = "&CLoop India Bihar"
FOOTER_STRING = "&CThis is an automated generated sheet"
DEFAULT_COLUMN_WIDTH = 9

header_dict = {'aggregator':[{'column_width': 3,
                                          'formula': None,
                                          'label': 'S No',
                                          'total': False},
                                         {'column_width': 9,
                                          'formula': None,
                                          'label': 'Date',
                                          'total': False},
                                         {'column_width': 10,
                                         'formula': None,
                                         'label': 'Market',
                                         'total': False},
                                         {'column_width': 8,
                                          'formula': None,
                                          'label': 'Quantity [Q] (in Kg)',
                                          'total': True},
                                         {'column_width': 12,
                                          'formula': '0.25 * D',
                                          'label': 'Aggregator Payment [AP] (in Rs) (0.25*Q)',
                                          'total': True},
                                         {'column_width': 8,
                                          'formula': None,
                                          'label': 'Transport Cost [TC] (in Rs)',
                                          'total': True},
                                         {'column_width': 10,
                                          'formula': None,
                                          'label': "Farmers' Contribution [FC] (in Rs)",
                                          'total': True},
                                         {'column_width': 10,
                                          'formula': None,
                                          'label': 'Commission Agent Contribution [CAC] (in Rs)',
                                          'total': True},
                                         {'column_width': 10.7,
                                          'formula': 'E + F - G - H',
                                          'label': 'Total Payment (in Rs) (AP + TC - FC - CAC)',
                                          'total': True}],
              'gaddidar': [{'column_width': 9.4,
                                          'formula': None,
                                          'label': 'Date',
                                          'total': False},
                                         {'column_width': 18.3,
                                          'formula': None,
                                          'label': 'Commission Agent',
                                          'total': False},
                                         {'column_width': 11,
                                          'formula': None,
                                          'label': 'Market',
                                          'total': False},
                                         {'column_width': 10,
                                          'formula': None,
                                          'label': 'Quantity [Q] (in Kg)',
                                          'total': True},
                                         {'column_width': 13,
                                          'formula': None,
                                          'label': 'Commission Agent Discount [CAD] (in Rs/Kg)',
                                          'total': False},
                                         {'column_width': 16,
                                          'formula': 'D * E',
                                          'label': 'Commission Agent Contribution [CAC] (in Rs) (Q*CAD)',
                                          'total': True}],
              'transporter': [{'column_width': 9.4,
                                          'formula': None,
                                          'label': 'Date',
                                          'total': False},
                                         {'column_width': 11,
                                          'formula': None,
                                          'label': 'Market',
                                          'total': False},
                                         {'column_width': 18.3,
                                          'formula': None,
                                          'label': 'Transporter',
                                          'total': False},
                                         {'column_width': 11,
                                          'formula': None,
                                          'label': 'Vehicle Type',
                                          'total': False},
                                         {'column_width': 13,
                                          'formula': None,
                                          'label': 'Vehicle Number',
                                          'total': False},
                                         {'column_width': 13,
                                          'formula': None,
                                          'label': 'Tranport Cost (in Rs)',
                                          'total': True}]
            }


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


EXCEL_WORKBOOK_NAME = 'Farmer Mobile Number.xlsx'

AGGREGATOR_LIST = [  u'\u0930\u0902\u091c\u0940\u0924 \u0938\u093f\u0902\u0939', 
                     u'\u0926\u0947\u0935\u0947\u0928\u094d\u0926\u094d\u0930 \u0938\u093f\u0902\u0939',
                     u'\u0930\u093e\u092e \u0928\u093e\u0925 \u0938\u093f\u0902\u0939', 
                     u'Shyam Kumar', u'\u0917\u094c\u0924\u092e \u092a\u094d\u0930\u0938\u093e\u0926', 
                     u'\u0938\u0902\u0924\u094b\u0937 \u0915\u0941\u092e\u093e\u0930', 
                     u'\u0935\u093f\u0928\u0940\u0924 \u092e\u0939\u0924\u094b', 
                     u'\u0905\u0930\u0941\u0923', 
                     u'\u0938\u0942\u0930\u094d\u092f\u093e \u0928\u093e\u0930\u093e\u092f\u0923 \u0938\u093f\u0902\u0918', 
                     u'\u092e\u0943\u0924\u094d\u092f\u0941\u0902\u091c\u092f', 
                     u'\u0938\u0942\u0930\u091c \u0915\u0941\u092e\u093e\u0930', 
                     u'\u0935\u093f\u0915\u093e\u0938 \u092a\u094d\u0930\u0938\u093e\u0926', 
                     u'Rajaram Singh', 
                     u'\u0926\u093f\u0932\u0940\u092a'
                     ]

AGGREGATOR_LIST_EN = ['Ranjeet Singh', 'Devender Singh', 'Ram Nath Singh' , 'Shyam Kumar', 'Gautam Prasad', 'Santosh Kumar'
                    ,'Vineet Mahto', 'Arun', 'Suryanarayan Singh' , 'Mrityunjay', 'Suraj Kumar', 'Vikas Prasad'
                    , 'Rajaram Singh', 'Dileep']

DG_MEMBER_PHONE_LIST = '(9891256494 , 9013623264, 9810253264, 9555624943)'

AGGREGATOR_PHONE_LIST = '(7766885895, 9661416017, 7463892989, 7492963307, 8292724221, 8051162758, 7254855735, 7808128271, 0, 9534400947, 7091473978, 8002633290, 0, 7319753800, 9891256494)'

DEFAULT_FROM_EMAIL = 'amandeep@digitalgreen.org'

RECIPIENTS = ['amandeep@digitalgreen.org', 'lokesh@digitalgreen.org']


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
                                          'label': 'Sno',
                                          },
                                         {'column_width': 15,
                                          
                                          'label': 'Aggregator',
                                          },
                                         {'column_width': 15,
                                          'label': 'Village',
                                          },
                                         {'column_width': 15,
                                          'label': 'Farmer_ID',
                                          },
                                         {'column_width': 15,
                                          'label': 'Farmer',
                                          },
                                         {'column_width': 15,
                                          'label': 'Mobile Number',
                                          },
                                          {'column_width': 15,
                                          'label': 'Farmer Frequency ',
                                          },
                                          {'column_width': 15,
                                          'label': 'Mobile Number Frequency',
                                          }]



query_for_all_aggregator = '''SELECT 
                                Aggregator,
                                Village,
                                Farmer_ID,
                                Farmer,
                                Mobile_Number,
                                t2.Farmer_Frequency,
                                t3.Mobile_Frequency
                            FROM
                                (SELECT 
                                    ll.name_en Aggregator,
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
                                    ll.name_en <> 'Loop Test') t1
                                    JOIN
                                (SELECT 
                                    farmer_id f_id, COUNT(farmer_id) Farmer_Frequency
                                FROM
                                    loop_combinedtransaction lct
                                WHERE
                                    lct.date BETWEEN %s AND %s 
                                GROUP BY farmer_id) t2 ON t1.Farmer_ID = t2.f_id
                                    JOIN
                                (SELECT 
                                    phone, COUNT(phone) Mobile_Frequency
                                FROM
                                    loop_farmer
                                WHERE
                                    phone <= 7000000000
                                        OR phone >= 9999999999
                                        OR phone IN %s OR phone in %s
                                GROUP BY phone) t3 ON t1.Mobile_Number = t3.phone
                            HAVING t3.Mobile_Frequency > 0
                            ORDER BY Aggregator'''



query_for_single_aggregator = '''SELECT 
                                    Aggregator,
                                    Village,
                                    Farmer_ID,
                                    Farmer,
                                    Mobile_Number,
                                    t2.Farmer_Frequency,
                                    t3.Mobile_Frequency
                                FROM
                                    (SELECT 
                                        ll.name_en Aggregator,
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
                                        ll.name_en <> 'Loop Test' and ll.name_en = \'%s\') t1
                                        JOIN
                                    (SELECT 
                                        farmer_id f_id, COUNT(farmer_id) Farmer_Frequency
                                    FROM
                                        loop_combinedtransaction lct
                                    WHERE
                                        lct.date BETWEEN %s AND %s
                                    GROUP BY farmer_id) t2 ON t1.Farmer_ID = t2.f_id
                                        JOIN
                                    (SELECT 
                                        phone, COUNT(phone) Mobile_Frequency
                                    FROM
                                        loop_farmer
                                    WHERE
                                        phone <= 7000000000
                                            OR phone >= 9999999999
                                            OR phone IN %s OR phone in %s
                                    GROUP BY phone) t3 ON t1.Mobile_Number = t3.phone
                                HAVING t3.Mobile_Frequency > 0
                                ORDER BY Aggregator'''


EXCEL_WORKBOOK_NAME = 'Farmer Mobile Number.xlsx'

AGGREGATOR_LIST = ['Ranjeet Singh', 'Devender Singh', 'Ram Nath Singh' , 'Shyam Kumar', 'Gautam Prasad', 'Santosh Kumar'
                    ,'Vineet Mahto', 'Arun', 'Suryanarayan Singh' , 'Mrityunjay', 'Suraj Kumar', 'Vikas Prasad'
                    , 'Rajaram Singh', 'Dileep']

DG_MEMBER_PHONE_LIST = '(9891256494 , 9013623264, 9810253264, 9555624943)'

AGGREGATOR_PHONE_LIST = '(7766885895, 9661416017, 7463892989, 7492963307, 8292724221, 8051162758, 7254855735, 7808128271, 0, 9534400947, 7091473978, 8002633290, 0, 7319753800, 9891256494)'

DEFAULT_FROM_EMAIL = 'amandeep@digitalgreen.org'

RECIPIENTS = ['amandeep@digitalgreen.org']


 # -*- coding: utf-8 -*-
import json
import os
import sys
import MySQLdb
from dg.settings import *
from loop.models import *
import csv
from loop.config import *
from loop.sendmail import *
from django.core.management.base import BaseCommand, CommandError
import xlsxwriter
import time
from extract_data_from_date import *
from datetime import datetime, timedelta
import requests, copy, calendar


class Command(BaseCommand):

    #parse arguments from command line
    def add_arguments(self, parser):
        #create mutually exclusive command line switches
        group = parser.add_mutually_exclusive_group()
        group.add_argument('-fd',
            dest='from_date',
            default=None)

        group.add_argument('-nd',
            dest='num_days',
            default=0)

        parser.add_argument('-a',
            dest='aggregator',
            default='all')

        parser.add_argument('-td',
            dest='to_date',
            default=(datetime.now() - timedelta(days=1)).strftime('%Y%m%d'))


    
    #generate the excel for the given command line arguments
    def handle(self, *args, **options):
        generate_sheet_for = str(options.get('aggregator'))
        to_date = str(options.get('to_date'))
        num_days = int(options.get('num_days'))
        default_from_date = '20150701'
        header_json2 = {}
        data_json2 = {}
        header_json = {}
        data_json = {}
        final_json_to_send = {}
        final_json_to_send_second = {}
        excel_workbook_name = None
        excel_workbook_name_second = None

        if(options.get('from_date')):
            from_date=str(options.get('from_date'))
        else:
            from_date=to_date[0:6]+(datetime.now() - timedelta(days=0)).strftime('%Y%m%d')[-2:]

        if num_days < 0: 
            raise CommandError('-nd flag should be > 0')
        elif num_days != 0:
            temp_date = datetime.strptime(to_date, '%Y%m%d')
            from_date = (temp_date - timedelta(days=num_days)).strftime('%Y%m%d')

        #get time period in days and month
        # from_day = str(datetime.strptime(from_date, '%Y%m%d').day)
        # to_day = str(datetime.strptime(to_date, '%Y%m%d').day)

        # from_month = calendar.month_abbr[datetime.strptime(from_date, '%Y%m%d').month]
        # to_month = calendar.month_abbr[datetime.strptime(to_date, '%Y%m%d').month]

        # from_year = str(datetime.strptime(from_date, '%Y%m%d').year)
        # to_year = str(datetime.strptime(to_date, '%Y%m%d').year)

        start_date = get_data_from_date(from_date)
        from_day = start_date.get('day')
        from_month = start_date.get('month')
        from_year = start_date.get('year')

        end_date = get_data_from_date(to_date)
        to_day = end_date.get('day')
        to_month = end_date.get('month')
        to_year = end_date.get('year')

        default_start_date = get_data_from_date(default_from_date)
        default_from_day = default_start_date.get('day')
        default_from_month = default_start_date.get('month')
        default_from_year = default_start_date.get('year')
        

        AGGREGATOR_LIST = list(LoopUser.objects.exclude(role=1).values_list('name', flat=True))
        AGGREGATOR_LIST_EN = list(LoopUser.objects.exclude(role=1).values_list('name_en', flat=True))

        if type(generate_sheet_for) != str or type(from_date) != str or len(from_date) != 8 \
            or type(to_date) != str or len(to_date) != 8:
                raise CommandError('Invalid format for arguments')
        elif from_date > to_date:
                raise CommandError('Invalid date range given')
        elif generate_sheet_for != 'all' and generate_sheet_for not in AGGREGATOR_LIST_EN:
                raise CommandError('Aggregator not present in database')            

        query = None
        generate_sheet_for_all_flag = True 
        mysql_cn = MySQLdb.connect(host='localhost', port=3306, user='root',
                                           passwd=DATABASES['default']['PASSWORD'],
                                           db=DATABASES['default']['NAME'],
                                            charset = 'utf8',
                                             use_unicode = True)
        
        cur = mysql_cn.cursor()
        
        #determine the aggregator(s) for whom the sheet is generated
        if generate_sheet_for == 'all' or generate_sheet_for == None:
            query = query_for_transport_details_all_aggregator % (from_date, to_date)
            excel_workbook_name = 'Transport Details_' + from_day + '-' + from_month + '-' + from_year + \
                                                                ' to ' + to_day + '-' + to_month + '-' + to_year
        else:
            generate_sheet_for_all_flag = False
            generate_sheet_for = AGGREGATOR_LIST[AGGREGATOR_LIST_EN.index(generate_sheet_for)]
            query = query_for_transport_details_single_aggregator % (from_date, to_date, generate_sheet_for)
            excel_workbook_name = 'Transport Details_' + generate_sheet_for + '_ ' + from_day + '-' + \
                        from_month + '-' + from_year + ' to ' + to_day + '-' + to_month + '-' + to_year

    
        cur.execute(query)
        result = cur.fetchall()
        data = [list(row) for row in result]
        #create list copy for filtering
        temp_data = copy.deepcopy(data)
        if generate_sheet_for_all_flag is True:
            #Write data for all aggregators in sheet
            for sno in range(1,len(data) + 1):
                data[sno - 1].insert(0, str(sno))

            sheet_heading = 'गाड़ी के किराये की जानकारी_'+ from_day + '-' + from_month + '-' + from_year + \
                            ' to ' + to_day + '-' + to_month + '-' + to_year
            data_json['all'] = {'sheet_heading': sheet_heading,
                                    'sheet_name': 'सारे किसान', 'data': data
                                }
                    
            header_json['all'] = header_dict_for_transport_details
            #write data for every aggregator in their respective sheet
            for aggregator_name in AGGREGATOR_LIST:
                #filter data to get rows for the current aggregator
                filtered_data = [row for row in temp_data if row[0] == aggregator_name]
                filtered_data_copy = copy.deepcopy(filtered_data)
                for sno in range(1,len(filtered_data_copy) + 1):
                    filtered_data_copy[sno - 1].insert(0, str(sno))
                    
                sheet_heading = aggregator_name.encode('utf-8') + '_गाड़ी के किराये की जानकारी_' + from_day + '-' + from_month + \
                                                '-' + from_year + ' to ' + to_day + '-' + to_month + '-' + to_year 
                data_json[aggregator_name] = {'sheet_heading': sheet_heading,
                                    'sheet_name': aggregator_name, 'data': filtered_data_copy
                                }
                header_json[aggregator_name] = header_dict_for_transport_details
        else:
            #write data for a given aggregator from command line
            for sno in range(1,len(data) + 1):
                data[sno - 1].insert(0, str(sno))

            sheet_heading = generate_sheet_for.encode('utf-8') +'_गाड़ी के किराये की जानकारी_' + \
                                from_day + '-' + from_month + '-' + from_year + ' to ' + to_day + '-' +  \
                                to_month + '-' + to_year 
            data_json[generate_sheet_for] = {'sheet_heading': sheet_heading ,
                                    'sheet_name': generate_sheet_for, 'data': data
                                }
            
            header_json[generate_sheet_for] = header_dict_for_transport_details

        final_json_to_send['header'] = header_json
        final_json_to_send['data'] = data_json
        final_json_to_send['cell_format'] = {'bold':0, 'font_size': 10, 'border' : 1,
                                                    'text_wrap': True}


        # if generate_sheet_for == 'all' or generate_sheet_for == None:
        #     query = query_for_incorrect_phone_no_all_aggregator % (default_from_date, to_date, default_from_date, to_date)
        #     excel_workbook_name_second = 'Incorrect Mobile Numbers_' + default_from_day + '-' + default_from_month + '-' + default_from_year + \
        #                                                         ' to ' + to_day + '-' + to_month + '-' + to_year
        # else:
        #     generate_sheet_for_all_flag = False
        #     generate_sheet_for = AGGREGATOR_LIST[AGGREGATOR_LIST_EN.index(generate_sheet_for)]
        #     query = query_for_incorrect_phone_no_single_aggregator % (default_from_date, to_date, generate_sheet_for, default_from_date, to_date)
        #     excel_workbook_name_second = 'Incorrect_Mobile_Numbers_' + generate_sheet_for + '_ ' + default_from_day + '-' + \
        #                 default_from_month + '-' + default_from_year + ' to ' + to_day + '-' + to_month + '-' + to_year

        # cur2 = mysql_cn.cursor()                
        # cur2.execute(query)
        # result = cur2.fetchall()
        # data2 = [list(row) for row in result]
        # #create list copy for filtering
        # temp_data2 = copy.deepcopy(data2)
        # if generate_sheet_for_all_flag is True:
        #     #Write data for all aggregators in sheet
        #     for sno in range(1,len(data2) + 1):
        #         data2[sno - 1].insert(0, str(sno))
        #         if int(data2[sno - 1][6]) >= 9999999999:
        #             data2[sno - 1][6] = 'नंबर नहीं है'

        #     sheet_heading = 'गलत मोबाइल नंबर की लिस्ट_'+ default_from_day + '-' + default_from_month + '-' + default_from_year + \
        #                     ' to ' + to_day + '-' + to_month + '-' + to_year
        #     data_json2['all'] = {'sheet_heading': sheet_heading,
        #                             'sheet_name': 'सारे किसान', 'data': data2
        #                         }
                    
        #     header_json2['all'] = header_dict_for_loop_email_mobile_numbers
        #     #write data for every aggregator in their respective sheet
        #     for aggregator_name in AGGREGATOR_LIST:
        #         #filter data to get rows for the current aggregator
        #         filtered_data = [row for row in temp_data2 if row[0] == aggregator_name]
        #         filtered_data_copy = copy.deepcopy(filtered_data)
        #         for sno in range(1,len(filtered_data_copy) + 1):
        #             filtered_data_copy[sno - 1].insert(0, str(sno))
        #             if int(filtered_data_copy[sno - 1][6]) >= 9999999999:
        #                 filtered_data_copy[sno - 1][6] = 'नंबर नहीं है'
                    
        #         sheet_heading = aggregator_name.encode('utf-8') + '_गलत मोबाइल नंबर की लिस्ट_' + default_from_day + '-' + default_from_month + \
        #                                         '-' + default_from_year + ' to ' + to_day + '-' + to_month + '-' + to_year 
        #         data_json2[aggregator_name] = {'sheet_heading': sheet_heading,
        #                             'sheet_name': aggregator_name, 'data': filtered_data_copy
        #                         }
        #         header_json2[aggregator_name] = header_dict_for_loop_email_mobile_numbers
        # else:
        #     #write data for a given aggregator from command line
        #     for sno in range(1,len(data2) + 1):
        #         data2[sno - 1].insert(0, str(sno))
        #         if int(data2[sno - 1][6]) >= 9999999999:
        #             data2[sno - 1][6] = 'नंबर नहीं है'

        #     sheet_heading = generate_sheet_for.encode('utf-8') +'_गलत मोबाइल नंबर की लिस्ट_' + \
        #                         default_from_day + '-' + default_from_month + '-' + default_from_year + ' to ' + to_day + '-' +  \
        #                         to_month + '-' + to_year 
        #     data_json2[generate_sheet_for] = {'sheet_heading': sheet_heading ,
        #                             'sheet_name': generate_sheet_for, 'data': data2
        #                         }
            
        #     header_json2[generate_sheet_for] = header_dict_for_loop_email_mobile_numbers

        # final_json_to_send_second['header'] = header_json2
        # final_json_to_send_second['data'] = data_json2
        # final_json_to_send_second['cell_format'] = {'bold':0, 'font_size': 10, 'border' : 1,
        #                                             'text_wrap': True}

        

        #post request to library for excel generation
        try:
            r = requests.post('http://localhost:8000/loop/get_payment_sheet/', data=json.dumps(final_json_to_send, 
                                                                                    default=lambda x:str(x)))
            files = []
            excel_file = open(excel_workbook_name + '.xlsx', 'w')
            excel_file.write(r.content)
            excel_file.close()
            files.append(excel_file)
            # r = requests.post('http://localhost:5000/loop/get_payment_sheet/', data=json.dumps(final_json_to_send_second))
            # excel_file = open(excel_workbook_name_second + '.xlsx', 'w')
            # excel_file.write(r.content)
            # excel_file.close()
            # files.append(excel_file)


            #send email to concerned people with excel file attached    
            common_send_email('Transportation Details', 
                              RECIPIENTS_TEMP, files, [],EMAIL_HOST_USER,"","")
            os.remove(excel_workbook_name + '.xlsx')
            # os.remove(excel_workbook_name_second + '.xlsx')
        except Exception as e:
            raise CommandError(e)
        






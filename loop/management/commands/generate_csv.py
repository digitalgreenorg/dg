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
            default=(datetime.now() - timedelta(days=4)).strftime('%Y%m%d'))


    
    #generate the excel for the given command line arguments
    def handle(self, *args, **options):
        generate_sheet_for = str(options.get('aggregator'))
        to_date = str(options.get('to_date'))
        num_days = int(options.get('num_days'))
        header_json = {}
        data_json = {}
        final_json_to_send = {}
        excel_workbook_name = None
        if(options.get('from_date')):
            from_date=str(options.get('from_date'))
        else:
            from_date=to_date[0:6]+(datetime.now() - timedelta(days=3)).strftime('%Y%m%d')[-2:]


        if num_days < 0: 
            raise CommandError('-nd flag should be > 0')
        elif num_days != 0:
            temp_date = datetime.strptime(to_date, '%Y%m%d')
            from_date = (temp_date - timedelta(days=num_days)).strftime('%Y%m%d')

        #get time period in days and month
        from_day = str(datetime.strptime(from_date, '%Y%m%d').day)
        to_day = str(datetime.strptime(to_date, '%Y%m%d').day)

        from_month = calendar.month_abbr[datetime.strptime(from_date, '%Y%m%d').month]
        to_month = calendar.month_abbr[datetime.strptime(to_date, '%Y%m%d').month]

        from_year = str(datetime.strptime(from_date, '%Y%m%d').year)
        to_year = str(datetime.strptime(to_date, '%Y%m%d').year)

        AGGREGATOR_LIST = list(LoopUser.objects.exclude(name='Loop Test').values_list('name', flat=True))
        AGGREGATOR_LIST_EN = list(LoopUser.objects.exclude(name_en='Loop Test').values_list('name_en', flat=True))

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
            query = query_for_all_aggregator % (from_date, to_date, from_date, to_date)
            excel_workbook_name = 'Incorrect Mobile Numbers_' + from_day + '-' + from_month + '-' + from_year + \
                                                                ' to ' + to_day + '-' + to_month + '-' + to_year
        else:
            generate_sheet_for_all_flag = False
            generate_sheet_for = AGGREGATOR_LIST[AGGREGATOR_LIST_EN.index(generate_sheet_for)]
            query = query_for_single_aggregator % (from_date, to_date, generate_sheet_for, from_date, to_date)
            excel_workbook_name = 'Incorrect_Mobile_Numbers_' + generate_sheet_for + '_ ' + from_day + '-' + \
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
                if int(data[sno - 1][6]) >= 9999999999:
                    data[sno - 1][6] = 'नंबर नहीं है'

            sheet_heading = 'गलत मोबाइल नंबर की लिस्ट_'+ from_day + '-' + from_month + '-' + from_year + \
                            ' to ' + to_day + '-' + to_month + '-' + to_year
            data_json['all'] = {'sheet_heading': sheet_heading,
                                    'sheet_name': 'सारे किसान', 'data': data
                                }
                    
            header_json['all'] = header_dict_for_loop_email_mobile_numbers
            #write data for every aggregator in their respective sheet
            for aggregator_name in AGGREGATOR_LIST:
                #filter data to get rows for the current aggregator
                filtered_data = [row for row in temp_data if row[0] == aggregator_name]
                filtered_data_copy = copy.deepcopy(filtered_data)
                for sno in range(1,len(filtered_data_copy) + 1):
                    filtered_data_copy[sno - 1].insert(0, str(sno))
                    if int(filtered_data_copy[sno - 1][6]) >= 9999999999:
                        filtered_data_copy[sno - 1][6] = 'नंबर नहीं है'
                    
                sheet_heading = aggregator_name.encode('utf-8') + '_गलत मोबाइल नंबर की लिस्ट_' + from_day + '-' + from_month + \
                                                '-' + from_year + ' to ' + to_day + '-' + to_month + '-' + to_year 
                data_json[aggregator_name] = {'sheet_heading': sheet_heading,
                                    'sheet_name': aggregator_name, 'data': filtered_data_copy
                                }
                header_json[aggregator_name] = header_dict_for_loop_email_mobile_numbers
        else:
            #write data for a given aggregator from command line
            for sno in range(1,len(data) + 1):
                data[sno - 1].insert(0, str(sno))
                if int(data[sno - 1][6]) >= 9999999999:
                    data[sno - 1][6] = 'नंबर नहीं है'

            sheet_heading = generate_sheet_for.encode('utf-8') +'_गलत मोबाइल नंबर की लिस्ट_' + \
                                from_day + '-' + from_month + '-' + from_year + ' to ' + to_day + '-' +  \
                                to_month + '-' + to_year 
            data_json[generate_sheet_for] = {'sheet_heading': sheet_heading ,
                                    'sheet_name': generate_sheet_for, 'data': data
                                }
            
            header_json[generate_sheet_for] = header_dict_for_loop_email_mobile_numbers

        final_json_to_send['header'] = header_json
        final_json_to_send['data'] = data_json
        final_json_to_send['cell_format'] = {'bold':0, 'font_size': 10, 'border' : 1,
                                                    'text_wrap': True}

        #post request to library for excel generation
        try:
            r = requests.post('http://www.digitalgreen.org/loop/get_payment_sheet/', data=json.dumps(final_json_to_send))
            excel_file = open(excel_workbook_name + '.xlsx', 'w')
            excel_file.write(r.content)
            excel_file.close()
            #send email to concerned people with excel file attached    
            common_send_email('Farmers List with Incorrect Mobile Numbers', 
                              RECIPIENTS, excel_file, [],EMAIL_HOST_USER)
            os.remove(excel_workbook_name + '.xlsx')
        except Exception as e:
            raise CommandError('There is some problem, please contact the administrator')
        






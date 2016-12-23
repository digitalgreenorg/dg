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


class Command(BaseCommand):

    #parse arguments from command line
    def add_arguments(self, parser):
        #create mutually exclusive command line switches
        group = parser.add_mutually_exclusive_group()
        group.add_argument('-fd',
            dest='from_date',
            default=20150701)

        group.add_argument('-nd',
            dest='num_days',
            default=0)

        parser.add_argument('-a',
            dest='aggregator',
            default='all')

        parser.add_argument('-td',
            dest='to_date',
            default=time.strftime('%Y%m%d'))


    
    #generate the excel for the given command line arguments
    def handle(self, *args, **options):
        generate_sheet_for = str(options.get('aggregator'))
        from_date = str(options.get('from_date'))
        to_date = str(options.get('to_date'))
        num_days = int(options.get('num_days'))

        if num_days < 0: 
            raise CommandError('-nd flag should be > 0')
        elif num_days != 0:
            temp_date = datetime.strptime(to_date, '%Y%m%d')
            from_date = (temp_date - timedelta(days=num_days)).strftime('%Y%m%d')

        print from_date



        if type(generate_sheet_for) != str or type(from_date) != str or len(from_date) != 8 \
            or type(to_date) != str or len(to_date) != 8:
                raise CommandError('Invalid format for arguments')
        elif from_date > to_date:
                raise CommandError('Invalid date range given')
        elif generate_sheet_for != 'all' and generate_sheet_for not in AGGREGATOR_LIST:
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
            query = query_for_all_aggregator % (from_date, to_date, DG_MEMBER_PHONE_LIST, AGGREGATOR_PHONE_LIST)
        else:
            generate_sheet_for_all_flag = False
            query = query_for_single_aggregator % (generate_sheet_for, from_date, to_date, DG_MEMBER_PHONE_LIST, 
                                                    AGGREGATOR_PHONE_LIST)

        cur.execute(query)
                
        result = cur.fetchall()
        data = [row for row in result]

        workbook = xlsxwriter.Workbook(EXCEL_WORKBOOK_NAME)
        header_format = workbook.add_format({'bold':1, 'font_size': 10,'text_wrap': True})

        if generate_sheet_for_all_flag is True:
            #Write data for all aggregators in sheet
            ws = workbook.add_worksheet('All Data')
            ws = set_columns_width(ws_obj=ws)
            ws = write_headers_in_sheet(ws_obj=ws, format_str=header_format)
            ws = write_data_in_sheet(ws_obj=ws, sheet_data=data)

            #write data for every aggregator in their respective sheet
            for aggregator_name in AGGREGATOR_LIST:
                ws = workbook.add_worksheet(aggregator_name)
                ws = set_columns_width(ws_obj=ws)
                ws = write_headers_in_sheet(ws_obj=ws, format_str=header_format)

                #filter data to get rows for the current aggregator
                filtered_data = [row for row in data if row[0] == aggregator_name]
                ws = write_data_in_sheet(ws_obj=ws, sheet_data=filtered_data)

        else:
            #write data for a given aggregator from command line
            ws = workbook.add_worksheet(generate_sheet_for)
            ws = set_columns_width(ws_obj=ws)
            ws = write_headers_in_sheet(ws_obj=ws, format_str=header_format)
            ws = write_data_in_sheet(ws_obj=ws, sheet_data=data)

        workbook.close()
        #send email to concerned people with excel file attached    
        common_send_email('Farmers List with Incorrect Mobile Numbers', 
                        RECIPIENTS, EXCEL_WORKBOOK_NAME, [],EMAIL_HOST_USER)






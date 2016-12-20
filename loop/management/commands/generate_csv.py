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
from django.core.management.base import BaseCommand
import xlsxwriter


class Command(BaseCommand):

    #parse arguments from command line
    def add_arguments(self, parser):
        parser.add_argument('aggregator')

    
    #generate the csv for the given command line arguments
    #LIMT----this function will not handle the case when no command line args are given    
    def handle(self, *args, **options):
        generate_sheet_for = str(options.get('aggregator'))
        print generate_sheet_for
        query = None
        generate_sheet_for_all_flag = True 
        csv_file = None
        mysql_cn = MySQLdb.connect(host='localhost', port=3306, user='root',
                                           passwd=DATABASES['default']['PASSWORD'],
                                           db=DATABASES['default']['NAME'],
                                            charset = 'utf8',
                                             use_unicode = True)
        
        cur = mysql_cn.cursor()

        #determine the aggregator(s) for whom the sheet is generated
        if generate_sheet_for == 'all' or generate_sheet_for == None:
            query = query_for_all_aggregator % (DG_MEMBER_PHONE_LIST, AGGREGATOR_PHONE_LIST)
        else:
            generate_sheet_for_all_flag = False
            query = query_for_single_aggregator % (generate_sheet_for, DG_MEMBER_PHONE_LIST, AGGREGATOR_PHONE_LIST)

        print query
        cur.execute(query)
                
        result = cur.fetchall()
        data = [row for row in result]

        workbook = xlsxwriter.Workbook(EXCEL_WORKBOOK_NAME)
        header_format = workbook.add_format({'bold':1, 'font_size': 10,'text_wrap': True})

        if generate_sheet_for_all_flag is True:
            #Write data for all aggregators in sheet
            ws = workbook.add_worksheet('All Aggregators')
            ws = set_columns_width(ws_obj=ws)
            ws = write_headers_in_sheet(ws_obj=ws, format_str=header_format)
            ws = write_data_in_sheet(ws_obj=ws, sheet_data=data)

            #write data for every aggregator in the sheet
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
        #send email to concerned people with csv file attached    
        common_send_email('Farmers List with Incorrect Mobile Numbers', 
                         RECIPIENTS, EXCEL_WORKBOOK_NAME, [],EMAIL_HOST_USER)










        # #write data to csv
        # with open(generate_sheet_for+'.csv', 'wb') as file:
        #     headers = ['Aggregator', 'Village', 'Farmer_ID','Farmer','Mobile Number','Farmer Frequency','Mobile Number Frequency']
        #     wrt = csv.writer(file, delimiter=",")
        #     wrt.writerow(headers)
        #     data = [row for row in result]
        #     for item in range(len(data)):
        #         data[item] = list(data[item])
        #         sheet_row = []
        #         for row in range(len(data[item])):
        #             if type(data[item][row]) is long:
        #                 data[item][row] = str(data[item][row])
        #             sheet_row.append(data[item][row].encode('utf-8'))
        #         wrt.writerow(sheet_row)    

        #         #wrt.writerow(data[item])    
        #     file.close()
        #     csv_file = file

       


           









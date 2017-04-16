 # -*- coding: utf-8 -*-
import json
import os
import sys
import MySQLdb
from dg.settings import *
from loop.models import *
import csv
from loop.config import *
from loop.payment_template import prepare_value_data_generic, excel_processing, get_combined_data_and_sheets_formats
from loop.sendmail import *
from django.core.management.base import BaseCommand, CommandError
import xlsxwriter
import time
from extract_data_from_date import *
from datetime import datetime, timedelta
from django.template.loader import render_to_string, get_template

import requests, copy, calendar
from django.template.context import Context


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
            default=(datetime.now() - timedelta(days=6)).strftime('%Y%m%d'))



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
        data_list_for_email_body_current_duration = {}
        data_list_for_email_body_all_duration = {}
        final_body_list = []

        if(options.get('from_date')):
            from_date=str(options.get('from_date'))
        else:
            from_date=to_date[0:6]+(datetime.now() - timedelta(days=5)).strftime('%Y%m%d')[-2:]

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
        mysql_cn = MySQLdb.connect(host=DATABASES['default']['HOST'], port=DATABASES['default']['PORT'], user=DATABASES['default']['USER'],
                                           passwd=DATABASES['default']['PASSWORD'],
                                           db=DATABASES['default']['NAME'],
                                            charset = 'utf8',
                                             use_unicode = True)

        cur = mysql_cn.cursor()

        #determine the aggregator(s) for whom the sheet is generated
        if generate_sheet_for == 'all' or generate_sheet_for == None:
            query = query_for_incorrect_phone_no_all_aggregator % (from_date, to_date, from_date, to_date)
            excel_workbook_name = 'Incorrect Mobile Numbers_' + from_day + '-' + from_month + '-' + from_year + \
                                                                ' to ' + to_day + '-' + to_month + '-' + to_year
        else:
            generate_sheet_for_all_flag = False
            generate_sheet_for = AGGREGATOR_LIST[AGGREGATOR_LIST_EN.index(generate_sheet_for)]
            query = query_for_incorrect_phone_no_single_aggregator % (from_date, to_date, generate_sheet_for, from_date, to_date)
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
            data_list_for_email_body_current_duration['Total'] = len(data)
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
                data_list_for_email_body_current_duration[aggregator_name] = len(filtered_data)
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
            data_list_for_email_body_current_duration[generate_sheet_for] = len(data)

        final_json_to_send['header'] = header_json
        final_json_to_send['data'] = data_json
        final_json_to_send['cell_format'] = {'bold':0, 'font_size': 10, 'border' : 1,
                                                    'text_wrap': True}

#------------------------------------------------------one code ends and repetitive code begins here--------------------

        if generate_sheet_for == 'all' or generate_sheet_for == None:
            query = query_for_incorrect_phone_no_all_aggregator % (default_from_date, to_date, default_from_date, to_date)
            excel_workbook_name_second = 'Incorrect Mobile Numbers_' + default_from_day + '-' + default_from_month + '-' + default_from_year + \
                                                                ' to ' + to_day + '-' + to_month + '-' + to_year
        else:
            generate_sheet_for_all_flag = False
            generate_sheet_for = AGGREGATOR_LIST[AGGREGATOR_LIST_EN.index(generate_sheet_for)]
            query = query_for_incorrect_phone_no_single_aggregator % (default_from_date, to_date, generate_sheet_for, default_from_date, to_date)
            excel_workbook_name_second = 'Incorrect_Mobile_Numbers_' + generate_sheet_for + '_ ' + default_from_day + '-' + \
                        default_from_month + '-' + default_from_year + ' to ' + to_day + '-' + to_month + '-' + to_year

        cur2 = mysql_cn.cursor()
        cur2.execute(query)
        result = cur2.fetchall()
        data2 = [list(row) for row in result]
        #create list copy for filtering
        temp_data2 = copy.deepcopy(data2)
        if generate_sheet_for_all_flag is True:
            #Write data for all aggregators in sheet
            for sno in range(1,len(data2) + 1):
                data2[sno - 1].insert(0, str(sno))
                if int(data2[sno - 1][6]) >= 9999999999:
                    data2[sno - 1][6] = 'नंबर नहीं है'

            sheet_heading = 'गलत मोबाइल नंबर की लिस्ट_'+ default_from_day + '-' + default_from_month + '-' + default_from_year + \
                            ' to ' + to_day + '-' + to_month + '-' + to_year
            data_json2['all'] = {'sheet_heading': sheet_heading,
                                    'sheet_name': 'सारे किसान', 'data': data2
                                }

            header_json2['all'] = header_dict_for_loop_email_mobile_numbers
            data_list_for_email_body_all_duration['Total'] = len(data2)
            #write data for every aggregator in their respective sheet
            for aggregator_name in AGGREGATOR_LIST:
                #filter data to get rows for the current aggregator
                filtered_data = [row for row in temp_data2 if row[0] == aggregator_name]
                filtered_data_copy = copy.deepcopy(filtered_data)
                for sno in range(1,len(filtered_data_copy) + 1):
                    filtered_data_copy[sno - 1].insert(0, str(sno))
                    if int(filtered_data_copy[sno - 1][6]) >= 9999999999:
                        filtered_data_copy[sno - 1][6] = 'नंबर नहीं है'

                sheet_heading = aggregator_name.encode('utf-8') + '_गलत मोबाइल नंबर की लिस्ट_' + default_from_day + '-' + default_from_month + \
                                                '-' + default_from_year + ' to ' + to_day + '-' + to_month + '-' + to_year
                data_json2[aggregator_name] = {'sheet_heading': sheet_heading,
                                    'sheet_name': aggregator_name, 'data': filtered_data_copy
                                }
                header_json2[aggregator_name] = header_dict_for_loop_email_mobile_numbers
                data_list_for_email_body_all_duration[aggregator_name] = len(filtered_data)
        else:
            #write data for a given aggregator from command line
            for sno in range(1,len(data2) + 1):
                data2[sno - 1].insert(0, str(sno))
                if int(data2[sno - 1][6]) >= 9999999999:
                    data2[sno - 1][6] = 'नंबर नहीं है'

            sheet_heading = generate_sheet_for.encode('utf-8') +'_गलत मोबाइल नंबर की लिस्ट_' + \
                                default_from_day + '-' + default_from_month + '-' + default_from_year + ' to ' + to_day + '-' +  \
                                to_month + '-' + to_year
            data_json2[generate_sheet_for] = {'sheet_heading': sheet_heading ,
                                    'sheet_name': generate_sheet_for, 'data': data2
                                }

            header_json2[generate_sheet_for] = header_dict_for_loop_email_mobile_numbers
            data_list_for_email_body_current_duration[generate_sheet_for] = len(data2)


        final_json_to_send_second['header'] = header_json2
        final_json_to_send_second['data'] = data_json2
        final_json_to_send_second['cell_format'] = {'bold':0, 'font_size': 10, 'border' : 1,
                                                    'text_wrap': True}


        items = []
        if len(data_list_for_email_body_current_duration.keys()) > 1:
            for aggregator_name in AGGREGATOR_LIST:
                items.append({'name':AGGREGATOR_LIST_EN[AGGREGATOR_LIST.index(aggregator_name)], 'total': data_list_for_email_body_all_duration.get(aggregator_name),
                                'current': data_list_for_email_body_current_duration.get(aggregator_name)})

            items.append({'name':'Total', 'total': data_list_for_email_body_all_duration.get('Total'),
                                'current': data_list_for_email_body_current_duration.get('Total')})

        else:
            items.append({'name':AGGREGATOR_LIST_EN[AGGREGATOR_LIST.index(generate_sheet_for)], 'total': data_list_for_email_body_all_duration.get(generate_sheet_for),
                                'current': data_list_for_email_body_current_duration.get(generate_sheet_for)})

        html_template = 'loop/loop_html_body.html'
        final_html_raw = get_template(html_template)
        context = Context({'items': items})
        final_html = final_html_raw.render(context)

        #post request to library for excel generation
        try:
            # r = requests.post('http://localhost:8000/loop/get_payment_sheet/', data=json.dumps(final_json_to_send))
            # print r
            formatted_post_data = prepare_value_data_generic(final_json_to_send)

            # this will get combined web data and various formats
            data_dict = get_combined_data_and_sheets_formats(formatted_post_data)
            # accessing basic variables
            workbook = data_dict.get('workbook')
            print "1"
            name_of_sheets = data_dict.get('name_of_sheets')
            print "2"
            heading_of_sheets = data_dict.get('heading_of_sheets')
            print "3"
            heading_format = data_dict.get('heading_format')
            print "4"
            header_format = data_dict.get('header_format')
            print "5"
            row_format = data_dict.get('row_format')
            print "6"
            total_cell_format = data_dict.get('total_cell_format')
            print "7"
            excel_output = data_dict.get('excel_output')
            print "8"
            combined_data = data_dict.get('combined_data')
            print "9"
            combined_header = data_dict.get('combined_header')
            print "10"
            sheet_header = data_dict.get('sheet_header')
            print "11"
            sheet_footer = data_dict.get('sheet_footer')
            # now the sheet processes
            print "12"
            workbook = excel_processing(workbook, name_of_sheets, heading_of_sheets, heading_format,
                    row_format, total_cell_format, header_format, combined_data, combined_header, sheet_header, sheet_footer)
            print "13"
            # final closing the working
            workbook.close()
            print "14"

            files = []
            # excel_file = open(excel_workbook_name + '.xlsx', 'w')
            # excel_file.write(r.content)
            # excel_file.close()
            files.append(workbook)
            print "15"
            # r = requests.post('http://localhost:8000/loop/get_payment_sheet/', data=json.dumps(final_json_to_send_second))
            # excel_file = open(excel_workbook_name_second + '.xlsx', 'w')
            # excel_file.write(r.content)
            # excel_file.close()
            # files.append(excel_file)
            #send email to concerned people with excel file attached    
            common_send_email('Farmers List with Incorrect Mobile Numbers',
                              RECIPIENTS, files, [],EMAIL_HOST_USER, html=final_html, text=final_html)

            os.remove(excel_workbook_name + '.xlsx')
            os.remove(excel_workbook_name_second + '.xlsx')
        except Exception as e:
            raise CommandError('There is some problem, please contact the administrator')










# coding=utf-8
import math

from loop.sendmail import common_send_email
from loop.models import LoopUser
from loop.utils.emailers_support import date_setter
from django.core.management.base import BaseCommand
from loop.utils.emailers_support.queries import *
from loop.utils.emailers_support.excel_generator import *
from loop.config import *


class TransportCostOutlier():
    # parse arguments from command line
    def add_arguments(self, parser):
        #create mutually exclusive command line switches
        group = parser.add_mutually_exclusive_group()
        group.add_argument('-fd',
                           dest='from_date',
                           default=None)

        group.add_argument('-nd',
                           dest='num_days',
                           default=None)

        parser.add_argument('-a',
                            dest='aggregator',
                            default='all')

        parser.add_argument('-td',
                            dest='to_date',
                            default=None)

    #generate the excel for the given command line arguments
    def handle(self, *args, **options):
        from_to_date = date_setter.set_from_to_date(options.get('from_date'), options.get('to_date'),
                                                    options.get('num_days'))
        aggregators = LoopUser.objects.filter(role=2);
        if options.get('aggregator') == 'all' or options.get('aggregator') == None:
            aggregator_to_check_id_string = ''
            #workbook_name = get_workbook_name()
            workbook = create_workbook(header_dict_for_transport_outlier['workbook_name'] % (
            MEDIA_ROOT, '', str(from_to_date[0]), str(from_to_date[1])))
        else:
            aggregator_to_check = aggregators.get(name_en=options.get('aggregator'))
            aggregator_to_check_id_string = 'and ll.id = ' + str(aggregator_to_check.id) + ''
            workbook = create_workbook(header_dict_for_transport_outlier['workbook_name'] % (
            MEDIA_ROOT, str(aggregator_to_check.name), str(from_to_date[0]), str(from_to_date[1])))

        query_result_data = self.data_generator(from_to_date, aggregator_to_check_id_string)
        aggregator_wise_TShare_outliers = self.data_Manipulator(query_result_data, from_to_date)
        worksheet_name = {'All': 'Transport cost Outliers_' + str(from_to_date[0]) + "_" + str(from_to_date[1])}


        # Position of All is first as a co-incidence I think.
        # Set correct column widths
        # workbook = create_workbook('Farmer Share Outliers.xlsx')
        all_format = ['date_format', 'wrap_text']
        all_format_created = create_format(all_format, workbook)
        header_dict_for_transport_outlier['column_properties'][0]['format'] = all_format_created['date_format']
        for columns in header_dict_for_transport_outlier['column_properties']:
            columns['header_format'] = all_format_created['wrap_text']
        table_properties = {'data': None, 'autofilter': False, 'banded_rows': False, 'style': 'Table Style Light 15',
                            'columns': header_dict_for_transport_outlier['column_properties']}


        for aggregator in aggregators:
            table_position_to_start = {'row': 2, 'col': 0}
            worksheet_name[aggregator.name_en] = header_dict_for_transport_outlier['worksheet_name'] % (
            str(aggregator.name_en), str(from_to_date[0]), str(from_to_date[1]))

        table_position_to_start = {'row': 2, 'col': 0}
        create_xlsx(workbook, aggregator_wise_TShare_outliers, table_properties, table_position_to_start,
                    worksheet_name)

        # create_xlsx(workbook, data_set_all, table_properties, table_position_to_start, worksheet_name)
        file_to_send = header_dict_for_transport_outlier['workbook_name'] % (
        MEDIA_ROOT, '', str(from_to_date[0]), str(from_to_date[1]))
        common_send_email("Hello Logo", recipients=RECIPIENTS, files=[file_to_send], bcc=[],
                          from_email='lokesh@digitalgreen.org', html="", text='hello')

    # Parameters provided at command prompt
    # By default, daily_a_m_filtered must take entire time period because it will be used in impact code

    def data_generator(self, from_to_date, aggregator_to_check_id_string):
        query = daily_a_m_transport_share_query
        query_result = onrun_query(query)
        return query_result

    def data_Manipulator(self, daily_a_m_transportShare, time_period):
        # Position of relevant columns
        dam_aggregator_id_col = 0
        dam_mandi_id_col = 1
        dam_date_col = 2
        insert_row_from_this_col = 2
        dam_aggregator_name_col = 3
        dam_type_col = 7
        dam_TCPK_col = 8

        # List ordered by aggregator, market
        a_m_count_query_result = onrun_query(a_m_count_query)
        aggregator_id_col = 0
        mandi_id_col = 1
        count_col = 4

        # Dictionary {(aggregator id, market id): count of visits}
        keys = ('Aggregator', 'Market', 'C')
        a_m_count = convert_query_result_in_nested_dictionary(a_m_count_query_result, keys, 2)

        daily_a_m_filtered = []

        # This dictionary will contain aggregator-wise outliers data
        aggregator_wise_TCost_outliers = {}
        aggregator_wise_TCost_correct = {}

        # Purpose: Takes a list and returns the row for given percentile value
        # Parameters: dataset - list, it should be sorted
        #             column - element of list on which percentile would be computed
        #             start - first row of aggregator-market combination
        #             length - number of elements in list for this aggregator-market combination
        #             percentile - percentile value

        start_point = 0
        element = 8

        for line in a_m_count_query_result:
            total_count = line[count_col]
            median_value = self.get_percentile(daily_a_m_transportShare, element, start_point, total_count, 0.5)
            first_quartile_value = self.get_percentile(daily_a_m_transportShare, element, start_point, total_count,
                                                       0.25)
            third_quartile_value = self.get_percentile(daily_a_m_transportShare, element, start_point, total_count,
                                                       0.75)
            inter_quartile_range = None
            upper_fence = None
            lower_fence = None
            if median_value and first_quartile_value and third_quartile_value:
                inter_quartile_range = third_quartile_value - first_quartile_value
                upper_fence = third_quartile_value + 1.5 * inter_quartile_range
                lower_fence = first_quartile_value - 0.75 * inter_quartile_range
            a_m_count[(line[aggregator_id_col], line[mandi_id_col])].update((
            ('Q1', first_quartile_value), ('M', median_value), ('Q3', third_quartile_value),
            ('IQR', inter_quartile_range), ('UF', upper_fence), ('LF', lower_fence)))
            start_point += total_count
            if first_quartile_value > third_quartile_value:
                print line[aggregator_id_col], line[
                    mandi_id_col], total_count, first_quartile_value, third_quartile_value
        high_cpk = []
        low_cpk = []
        no_cpk = []
        ok_cpk = []

        # Identifies outliers from daily_a_m_query_result and appends them in aggregator_wise_outliers
        # daily_a_m_query_result is a list and not a dictionary because the order of traversal is important as list is sorted
        # outliers are sorted by market-cpk. To change sorting criteria, insertion in outliers table should be defined accordingly
        # aggregator-wise outliers key is aggregator name and not ID because key is mapped to each sheet name. Both of them needs to be unique.
        # So, we have to ensure that aggregator names are unique

        from_date = time_period[0]
        to_date = time_period[1]

        for line in daily_a_m_transportShare:
            if line[dam_date_col] >= from_date and line[dam_date_col] <= to_date:
                daily_a_m_filtered.append(line)

        # TODO: It should check whether transport cost was changed later by admin or not. If yes, it's not an outlier to worry about.
        for line in daily_a_m_filtered:
            daily_a_m_line = list(line)  # converts tuple into a list because we want to add a parameter in each row
            TCPK = round(daily_a_m_line[dam_TCPK_col], 2)
            daily_a_m_line[dam_TCPK_col] = TCPK
            aggregator_id = daily_a_m_line[dam_aggregator_id_col]
            mandi_id = daily_a_m_line[dam_mandi_id_col]
            aggregator_name = daily_a_m_line[dam_aggregator_name_col]
            date = daily_a_m_line[dam_date_col]
            if TCPK:  # Check: TCPK exists
                if TCPK > a_m_count[(aggregator_id, mandi_id)]['UF']:  # Check: TCPK > Upper Fence
                    daily_a_m_line[dam_type_col] = 'High CPK'
                    if aggregator_name in aggregator_wise_TCost_outliers.keys():  # Check: Aggregator ID exists
                        aggregator_wise_TCost_outliers[aggregator_name].append(
                            daily_a_m_line[insert_row_from_this_col:])
                    else:
                        aggregator_wise_TCost_outliers[aggregator_name] = [daily_a_m_line[insert_row_from_this_col:]]
                    high_cpk.append(daily_a_m_line[insert_row_from_this_col:])
                elif TCPK < a_m_count[(aggregator_id, mandi_id)]['LF']:  # Check: TCPK < Lower Fence
                    daily_a_m_line[dam_type_col] = 'Low CPK'
                    if aggregator_name in aggregator_wise_TCost_outliers.keys():
                        aggregator_wise_TCost_outliers[aggregator_name].append(
                            daily_a_m_line[insert_row_from_this_col:])
                    else:
                        aggregator_wise_TCost_outliers[aggregator_name] = [daily_a_m_line[insert_row_from_this_col:]]
                    low_cpk.append(daily_a_m_line[insert_row_from_this_col:])
                else:
                    if aggregator_name in aggregator_wise_TCost_correct.keys():
                        aggregator_wise_TCost_correct[(aggregator_id, mandi_id, date)].append(daily_a_m_line)
                    else:
                        aggregator_wise_TCost_correct[(aggregator_id, mandi_id, date)] = [daily_a_m_line]
                    ok_cpk.append(daily_a_m_line[insert_row_from_this_col:])

            else:
                daily_a_m_line[dam_type_col] = 'No CPK'
                if aggregator_name in aggregator_wise_TCost_outliers.keys():
                    aggregator_wise_TCost_outliers[aggregator_name].append(daily_a_m_line[insert_row_from_this_col:])
                else:
                    aggregator_wise_TCost_outliers[aggregator_name] = [daily_a_m_line[insert_row_from_this_col:]]
                no_cpk.append(daily_a_m_line[insert_row_from_this_col:])

        print 'high_cpk'
        print len(high_cpk)
        print 'low_cpk'
        print len(low_cpk)
        print 'no_cpk'
        print len(no_cpk)
        print 'ok_cpk'
        print len(ok_cpk)

        # Adds all No CPK, Low CPK, High CPK entries in this order. Sorting order within each of them is A-M
        aggregator_wise_TCost_outliers['All'] = no_cpk
        aggregator_wise_TCost_outliers['All'].extend(low_cpk)
        aggregator_wise_TCost_outliers['All'].extend(high_cpk)
        return aggregator_wise_TCost_outliers

    def get_percentile(self, dataset, column, start, length, percentile):
        if length == 0:
            return None
        percentile_position = (length - 1) * percentile
        floor = math.floor(percentile_position)
        ceiling = math.ceil(percentile_position)
        if column == -1:
            if floor == ceiling:
                return dataset[int(start + percentile_position)]
            elif dataset[int(start + floor)] and dataset[int(start + ceiling)]:
                d0 = dataset[int(start + floor)] * (ceiling - percentile_position)
                d1 = dataset[int(start + ceiling)] * (percentile_position - floor)
                return d0 + d1
            else:
                return None
        else:
            if floor == ceiling:
                return dataset[int(start + percentile_position)][int(column)]
            elif dataset[int(start + floor)][int(column)] and dataset[int(start + ceiling)][int(column)]:
                d0 = dataset[int(start + floor)][int(column)] * (ceiling - percentile_position)
                d1 = dataset[int(start + ceiling)][int(column)] * (percentile_position - floor)
                return d0 + d1
            else:
                return None

                # Finds all quartile values for each aggregator-market combination and updates in a_m_count
                # a_m_count_query_result is a list and not a dictionary because the order of traversal is important as list is sorted
                # TODO: 1.5 and 0.75 to be provided by user






























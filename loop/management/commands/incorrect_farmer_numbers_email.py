# coding=utf-8
import copy
import collections
import os
from django.template import Context
from django.template.loader import get_template
from dg.settings import MEDIA_ROOT

__author__ = 'Lokesh'

from loop.sendmail import common_send_email
from loop.models import LoopUser
from loop.utils.emailers_support import date_setter
from django.core.management.base import BaseCommand
from loop.utils.emailers_support.queries import *
from loop.utils.emailers_support.excel_generator import *
from loop.config import *
from dg.settings import *
from django.template import *
from django.template.loader import render_to_string, get_template
import requests, calendar
from django.template.context import Context


class Command(BaseCommand):
    # parse arguments from command line
    def add_arguments(self, parser):
        # create mutually exclusive command line switches
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

    # generate the excel for the given command line arguments
    def handle(self, *args, **options):
        from_to_date = date_setter.set_from_to_date(options.get('from_date'), options.get('to_date'),
                                                    options.get('num_days'))
        aggregators = LoopUser.objects.filter(role=2);
        email_file_list = []
        if options.get('aggregator') == 'all' or options.get('aggregator') == None:
            aggregator_to_check_id_string = ''
            items = []
            content_for_mail = self.file_creator_date_specific(['2015-07-01', from_to_date[1]], aggregator_to_check_id_string,
                                                aggregators)
            email_body_stats_alltime = content_for_mail[0]
            email_file_list.append(content_for_mail[1])

            content_for_mail = self.file_creator_date_specific(from_to_date, aggregator_to_check_id_string, aggregators)
            email_body_stats_currenttime = content_for_mail[0]
            email_file_list.append(content_for_mail[1])

            for element in email_body_stats_alltime:
                items.append({'name':element, 'total':email_body_stats_alltime[element], 'current': email_body_stats_currenttime[element] if email_body_stats_currenttime[element] is not None else '0'})

        else:
            items = []
            aggregator_to_check = aggregators.get(name_en=options.get('aggregator'))
            aggregator_to_check_id_string = 'and ll.id = ' + str(aggregator_to_check.id) + ''
            content_for_mail = self.file_creator_date_specific(['2015-07-01', from_to_date[1]], aggregator_to_check_id_string,
                                                aggregators)
            email_body_stats_alltime = content_for_mail[0]
            email_file_list.append(content_for_mail[1])

            content_for_mail = self.file_creator_date_specific(from_to_date, aggregator_to_check_id_string, aggregators)
            email_body_stats_currenttime = content_for_mail[0]
            email_file_list.append(content_for_mail[1])

            for element in email_body_stats_alltime:
                items.append({'name':element, 'total':email_body_stats_alltime[element], 'current': email_body_stats_currenttime[element] if email_body_stats_currenttime[element] is not None else 0})

        html_template = 'loop/loop_html_body.html'
        final_html_raw = get_template(html_template)
        context = Context({'items': items})
        final_html = final_html_raw.render(context)

        common_send_email("Farmers List with Incorrect Mobile Numbers", recipients=RECIPIENTS, files=email_file_list, bcc=[],
                          from_email=EMAIL_HOST_USER, html=final_html, text=final_html)
        for file_name_to_remove in email_file_list:
            os.remove(str(file_name_to_remove))

    def file_creator_date_specific(self, from_to_date, aggregator_to_check_id_string, aggregators):
        data_list_for_email_body = collections.OrderedDict()
        workbook = create_workbook(header_dict_for_loop_email_mobile_numbers['workbook_name'] % (
        MEDIA_ROOT, '', str(from_to_date[0]), str(from_to_date[1])))
        query_result_data = self.data_generator(from_to_date, aggregator_to_check_id_string)
        data_set_all = self.get_all_data(query_result_data)
        worksheet_name = {'All': u'सारे ग़लत मोबाइल नंबर की लिस्ट_' + str(from_to_date[0]) + "_" + str(from_to_date[1])}

        table_properties = {'data': None, 'autofilter': False, 'banded_rows': False,
                            'style': 'Table Style Light 15',
                            'columns': header_dict_for_loop_email_mobile_numbers['column_properties']}
        table_position_to_start = {'row': 2, 'col': 0}

        for aggregator in aggregators:
            structured_data_set = self.set_filtered_structured_data(data_set_all['All'], aggregator)
            data_list_for_email_body[aggregator.name_en] = len(structured_data_set)
            data_set_all[aggregator.name_en] = structured_data_set
            worksheet_name[aggregator.name_en] = header_dict_for_loop_email_mobile_numbers['worksheet_name'] % (
                str(aggregator.name_en), str(from_to_date[0]), str(from_to_date[1]))
        data_list_for_email_body['Total'] = len(data_set_all['All'])

        create_xlsx(workbook, data_set_all, table_properties, table_position_to_start, worksheet_name)

        file_to_send = header_dict_for_loop_email_mobile_numbers['workbook_name'] % (
            MEDIA_ROOT, '', str(from_to_date[0]), str(from_to_date[1]))
        return [data_list_for_email_body, file_to_send]

    def data_generator(self, from_to_date, aggregator_to_check_id_string):
        query = query_for_incorrect_phone_all_per_aggregator % (
            str(from_to_date[0]), str(from_to_date[1]), aggregator_to_check_id_string, str(from_to_date[0]),
            str(from_to_date[1]))
        query_result = onrun_query(query)
        return query_result

    def get_all_data(self, data_from_query_result):
        data = collections.OrderedDict()
        data['All'] = []
        i = 0
        for result in data_from_query_result:
            i = i + 1
            temp = list(result)
            if int(temp[5]) >= 9999999999:
                temp[5] = u'नंबर नहीं है'
            temp.insert(0, i)
            data['All'].append(temp)
        return data

    def set_filtered_structured_data(self, data_store, aggregator):
        i = 0
        filtered_data = [row for row in data_store if row[1] == aggregator.name]
        filtered_data = copy.deepcopy(filtered_data)
        for row in filtered_data:
            i = i + 1
            row[0] = i
        return filtered_data


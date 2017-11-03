# coding=utf-8
import copy
import collections

__author__ = 'Amandeep'

from loop.sendmail import common_send_email
from loop.models import LoopUser
from loop.utils.emailers_support import date_setter
from django.core.management.base import BaseCommand
from loop.utils.emailers_support.queries import *
from loop.utils.emailers_support.excel_generator import *
from loop.config import *
from dg.settings import MEDIA_ROOT, EMAIL_HOST_USER
import os

id_map = {}
obj = LoopUser.objects.exclude(role=1).values_list('name', 'user_id')
for item in obj:
    id_map[item[0]] = item[1]

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
            content_for_mail = self.file_creator_date_specific(from_to_date, aggregator_to_check_id_string, aggregators)
            email_file_list.append(content_for_mail[0])
        else:
            aggregator_to_check = aggregators.get(name_en=options.get('aggregator'))
            aggregator_to_check_id_string = 'AND t1.Agg = ' + str(aggregator_to_check.user_id) + ''
            content_for_mail = self.file_creator_date_specific(from_to_date, aggregator_to_check_id_string, aggregators)
            email_file_list.append(content_for_mail[0])

        common_send_email("Farmers Transaction Data", recipients=RECIPIENTS, files=email_file_list, bcc=[],
                          from_email=EMAIL_HOST_USER, html="", text="")
        for file_name_to_remove in email_file_list:
            os.remove(str(file_name_to_remove))

    def file_creator_date_specific(self, from_to_date, aggregator_to_check_id_string, aggregators):
        workbook = create_workbook(header_dict_for_farmer_transaction['workbook_name'] % (
        MEDIA_ROOT, '', str(from_to_date[0]), str(from_to_date[1])))
        query_result_data = self.data_generator(from_to_date, aggregator_to_check_id_string)
        data_set_all = self.get_all_data(query_result_data)
        worksheet_name = {'All': u'बिक्री का रिकॉर्ड_' + str(from_to_date[0]) + "_" + str(from_to_date[1])}

        table_properties = {'data': None, 'autofilter': False, 'banded_rows': False,
                            'style': 'Table Style Light 15',
                            'columns': header_dict_for_farmer_transaction['column_properties']}
        table_position_to_start = {'row': 2, 'col': 0}

        for aggregator in aggregators:
            structured_data_set = self.set_filtered_structured_data(data_set_all['All'], aggregator)
            data_set_all[aggregator.name_en] = structured_data_set
            worksheet_name[aggregator.name_en] = header_dict_for_farmer_transaction['worksheet_name'] % (
                str(aggregator.name_en), str(from_to_date[0]), str(from_to_date[1]))

        data_set_all.pop('All',None)
        create_xlsx(workbook, data_set_all, table_properties, table_position_to_start, worksheet_name)


        file_to_send = header_dict_for_farmer_transaction['workbook_name'] % (
            MEDIA_ROOT, '', str(from_to_date[0]), str(from_to_date[1]))
        return [file_to_send]

    def data_generator(self, from_to_date, aggregator_to_check_id_string):
        query = query_for_farmer_transaction_all_single_aggregator % (
            from_to_date[0], from_to_date[1], aggregator_to_check_id_string)
        query_result = onrun_query(query)
        return query_result

    def get_all_data(self, data_from_query_result):
        data = collections.OrderedDict()
        data['All'] = []
        i = 0
        for result in data_from_query_result:
            i = i + 1
            temp = list(result)
            #convert datetime to str to display in YYYY-MM-DD format.
            temp[1] = str(temp[1])             
            data['All'].append(temp)
        return data

    def set_filtered_structured_data(self, data_store, aggregator):
        i = 0
        filtered_data = [row for row in data_store if row[0] == id_map[aggregator.name]]
        filtered_data_copy = copy.deepcopy(filtered_data)
        for row in filtered_data_copy:
            i = i + 1
            row[0] = i
            #convert datetime to str to display in YYYY-MM-DD format.
            row[1] = str(row[1])
        return filtered_data_copy


# coding=utf-8
import copy
import os
from dg.settings import MEDIA_ROOT

__author__ = 'Lokesh'

from loop.sendmail import common_send_email
from loop.models import LoopUser
from loop.utils.emailers_support import date_setter
from django.core.management.base import BaseCommand
from loop.utils.emailers_support.queries import *
from loop.utils.emailers_support.excel_generator import *
from loop.config import *
from loop.utils.emailers_support import FarmerShareOutlierCompute
from loop.utils.emailers_support import TransportShareOutlierCompute


class Command(BaseCommand):
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
        email_file_list = []
        if options.get('aggregator') == 'all' or options.get('aggregator') == None:

            file_for_mail = self.file_creator_per_case(from_to_date, case='FarmerShare')
            email_file_list.append(file_for_mail)

            file_for_mail = self.file_creator_per_case(from_to_date, case='TransportCost')
            email_file_list.append(file_for_mail)

        else:
            print "Specific Aggregator case not handled"

        common_send_email("Farmer Share and Transport Cost Outliers", recipients=RECIPIENTS, files=email_file_list, bcc=[],
                          from_email='lokesh@digitalgreen.org', html="", text='Please find the attached sheet for farmer share outliers and Transport Cost outliers')
        for file_name_to_remove in email_file_list:
            os.remove(str(file_name_to_remove))

    def file_creator_per_case(self, from_to_date, case=''):

        if case == 'FarmerShare':
            workbook = create_workbook(header_dict_for_farmer_outlier['workbook_name'] % (
            MEDIA_ROOT, '', str(from_to_date[0]), str(from_to_date[1])))

            FSOC = FarmerShareOutlierCompute.FarmerShareOutlier()
            daily_a_m_farmerShare_query_result = onrun_query(daily_a_m_farmerShare_query)
            aggregator_wise_outliers = FSOC.data_Manipulator(daily_a_m_farmerShare_query_result, from_to_date)
            worksheet_name = {'All': 'Farmer Share Outliers_' + str(from_to_date[0]) + "_" + str(from_to_date[1])}
            file_to_send = header_dict_for_farmer_outlier['workbook_name'] % (
            MEDIA_ROOT, '', str(from_to_date[0]), str(from_to_date[1]))

            for elements in header_dict_for_farmer_outlier['column_properties']:
                if 'data_type' in elements.keys() and elements['data_type']=='Date':
                    date_format = workbook.add_format({'num_format': 'd mmm yy'})
                    elements['format'] = date_format
            table_properties = {'data': None, 'autofilter': False, 'banded_rows': False, 'style': 'Table Style Light 15',
                                'columns': header_dict_for_farmer_outlier['column_properties']}

        elif case == 'TransportCost':
            workbook = create_workbook(header_dict_for_transport_outlier['workbook_name'] % (
            MEDIA_ROOT, '', str(from_to_date[0]), str(from_to_date[1])))

            TSOC = TransportShareOutlierCompute.TransportCostOutlier()
            daily_a_m_transportShare_query_result = onrun_query(daily_a_m_transport_share_query)
            aggregator_wise_outliers = TSOC.data_Manipulator(daily_a_m_transportShare_query_result, from_to_date)
            worksheet_name = {'All': 'Transport Cost Outliers_' + str(from_to_date[0]) + "_" + str(from_to_date[1])}
            file_to_send = header_dict_for_transport_outlier['workbook_name'] % (
            MEDIA_ROOT, '', str(from_to_date[0]), str(from_to_date[1]))
            for elements in header_dict_for_transport_outlier['column_properties']:
                if 'data_type' in elements.keys() and elements['data_type']=='Date':
                    date_format = workbook.add_format({'num_format': 'd mmm yy'})
                    elements['format'] = date_format
            table_properties = {'data': None, 'autofilter': False, 'banded_rows': False, 'style': 'Table Style Light 15',
                                'columns': header_dict_for_transport_outlier['column_properties']}

        table_position_to_start = {'row': 2, 'col': 0}

        create_xlsx(workbook, aggregator_wise_outliers, table_properties, table_position_to_start,
                    worksheet_name)

        return file_to_send

        
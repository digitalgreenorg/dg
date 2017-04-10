# coding=utf-8
import copy

__author__ = 'Lokesh'

from loop.sendmail import common_send_email
from loop.models import LoopUser
from loop.utils.emailers_support import date_setter
from django.core.management.base import BaseCommand
from loop.utils.emailers_support.queries import *
from loop.utils.emailers_support.excel_generator import *
from loop.config import *

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
            default=None)

        parser.add_argument('-a',
            dest='aggregator',
            default='all')

        parser.add_argument('-td',
            dest='to_date',
            default=None)

    #generate the excel for the given command line arguments
    def handle(self, *args, **options):
        from_to_date = date_setter.set_from_to_date(options.get('from_date'),options.get('to_date'),options.get('num_days'))
        aggregators = LoopUser.objects.filter(role=2);
        if options.get('aggregator') == 'all' or options.get('aggregator') == None:
            aggregator_to_check_id_string = ''
            #workbook_name = get_workbook_name()
            workbook = create_workbook(header_dict_for_farmer_outlier['workbook_name']%(MEDIA_ROOT, '' ,str(from_to_date[0]),str(from_to_date[1])))
        else:
            aggregator_to_check = aggregators.get(name_en=options.get('aggregator'))
            aggregator_to_check_id_string = 'and ll.id = ' + str(aggregator_to_check.id) + ''
            workbook = create_workbook(header_dict_for_farmer_outlier['workbook_name']%(MEDIA_ROOT, str(aggregator_to_check.name) ,str(from_to_date[0]),str(from_to_date[1])))

        query_result_data = self.data_generator(from_to_date, aggregator_to_check_id_string)
        aggregator_wise_FShare_outliers = self.data_Manipulator(query_result_data, from_to_date)
        worksheet_name = {'All':'Farmer Share Outliers_' + str(from_to_date[0]) + "_" + str(from_to_date[1])}


# Position of All is first as a co-incidence I think.
# Set correct column widths
# workbook = create_workbook('Farmer Share Outliers.xlsx')
# all_format = ['date_format']
# all_format_created = create_format(all_format, workbook)
# column_properties = [{'header': 'Date', 'format': all_format_created['date_format']}, {'header': 'Aggregator'}, {'header': 'Market'}, {'header': 'Quantity'}, {'header': 'TCost'}, {'header': 'Farmer Share'}, {'header': 'FSPK'}, {'header': 'FSPTC'}]
        table_properties = {'data': None, 'autofilter': False, 'banded_rows': False, 'style': 'Table Style Light 15', 'columns': header_dict_for_farmer_outlier['column_properties']}
# column_width = {'A:A': 10.55, 'B:B': 9.36}
#         print aggregator_wise_FShare_outliers





        for aggregator in aggregators:
            table_position_to_start = {'row':2, 'col':0}
            worksheet_name[aggregator.name_en] = header_dict_for_farmer_outlier['worksheet_name']%(str(aggregator.name_en),str(from_to_date[0]), str(from_to_date[1]))


        table_position_to_start = {'row':2, 'col':0}
        create_xlsx(workbook, aggregator_wise_FShare_outliers, table_properties, table_position_to_start,  worksheet_name)

        # create_xlsx(workbook, data_set_all, table_properties, table_position_to_start, worksheet_name)
        file_to_send = header_dict_for_farmer_outlier['workbook_name']%(MEDIA_ROOT, '',str(from_to_date[0]),str(from_to_date[1]))
        common_send_email("Hello Logo", recipients= RECIPIENTS, files=[file_to_send], bcc=[], from_email='lokesh@digitalgreen.org', html="", text='hello')


    def data_generator(self, from_to_date, aggregator_to_check_id_string):
        # query = query_for_incorrect_phone_no_single_aggregator % (str(from_to_date[0]), str(from_to_date[1]), aggregator_to_check_id_string, str(from_to_date[0]), str(from_to_date[1]))
        # daily_a_m_farmerShare = daily_a_m_farmerShare_query
        daily_a_m_farmerShare_query_result = onrun_query(daily_a_m_farmerShare_query)
        # query_result = onrun_query(query)
        # print daily_a_m_farmerShare_query_result
        return daily_a_m_farmerShare_query_result


    def data_Manipulator(self, daily_a_m_farmerShare, time_period):
        # List ordered by aggregator, market, date
        # print daily_a_m_farmerShare
        # print time_period
        aggregator_id_col = 0
        market_col = 1
        date_col = 2
        aggregator_name_col = 3
        FSPK_col = 8
        FSPTC_col = 9


        # Dictionary {(aggregator id, market id): count of visits}
        a_m_count_query_result = onrun_query(a_m_count_query)
        keys = ('Aggregator', 'Market','C')
        a_m_count = convert_query_result_in_nested_dictionary(a_m_count_query_result, keys, 2)

        # initialisation
        start_point = 0
        count = 0
        aggregator_id = daily_a_m_farmerShare[0][aggregator_id_col]
        aggregator_name = daily_a_m_farmerShare[0][aggregator_name_col]
        market_id = daily_a_m_farmerShare[0][market_col]
        last_FSPK = daily_a_m_farmerShare[0][FSPK_col]
        last_FSPTC = daily_a_m_farmerShare[0][FSPTC_col]
        no_of_rows = a_m_count[(aggregator_id, market_id)]['C']

        aggregator_wise_FShare_outliers = {}
        daily_a_m_farmerShare_filtered = []

        from_date = time_period[0]
        to_date = time_period[1]

        for line in daily_a_m_farmerShare:
            print ">>>>>>>>>>>>>>>>>"
            print line[date_col]
            print type(line[date_col])
            print from_date
            print type(from_date)
            print to_date
            print ">>>>>>>>>>>>>>>>>>>>>>>"
            if line[date_col] >= from_date and line[date_col] <= to_date:
                daily_a_m_farmerShare_filtered.append(line)


        for line in daily_a_m_farmerShare_filtered:
            print line
            FSPK = line[FSPK_col]
            FSPTC = line[FSPTC_col]
            if count < no_of_rows + start_point:
                if FSPK != last_FSPK and FSPTC != last_FSPTC:
                    if aggregator_name in aggregator_wise_FShare_outliers.keys():  # Check: Aggregator ID exists
                        aggregator_wise_FShare_outliers[aggregator_name].append(line[2:])
                        aggregator_wise_FShare_outliers['All'].append(line[2:])
                    else:
                        aggregator_wise_FShare_outliers[aggregator_name] = [line[2:]]
                        if 'All' in aggregator_wise_FShare_outliers.keys():
                            aggregator_wise_FShare_outliers['All'].append(line[2:])
                        else:
                            aggregator_wise_FShare_outliers['All'] = [line[2:]]
            else:
                aggregator_id = line[aggregator_id_col]
                aggregator_name = line[aggregator_name_col]
                market_id = line[market_col]
                start_point += no_of_rows
                no_of_rows = a_m_count[(aggregator_id, market_id)]['C']
            count += 1
            last_FSPK = FSPK
            last_FSPTC = FSPTC
        return aggregator_wise_FShare_outliers

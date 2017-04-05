# coding=utf-8
__author__ = 'Lokesh'


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
            workbook = create_workbook(header_dict_for_loop_email_mobile_numbers['workbook_name']%(MEDIA_ROOT, '' ,str(from_to_date[0]),str(from_to_date[1])))
        else:
            aggregator_to_check = aggregators.get(name_en=options.get('aggregator'))
            print aggregator_to_check.id
            aggregator_to_check_id_string = 'and ll.id = ' + str(aggregator_to_check.id) + ''
            workbook = create_workbook(header_dict_for_loop_email_mobile_numbers['workbook_name']%(MEDIA_ROOT, str(aggregator_to_check.name) ,str(from_to_date[0]),str(from_to_date[1])))

        query_result_data = self.data_generator(from_to_date, aggregator_to_check_id_string)
        data_set_all = self.get_all_data(query_result_data)
        worksheet_name = {'All':'Hello velle logo'}

        for aggregator in aggregators:
            structured_data_set = self.set_filtered_structured_data(data_set_all['All'], aggregator)
            data_set_all[aggregator.name_en] = structured_data_set

            table_properties = {'data': None, 'autofilter': False, 'banded_rows': False, 'style': 'Table Style Light 15', 'columns': header_dict_for_loop_email_mobile_numbers['column_properties']}
            table_position_to_start = {'row':2, 'col':0}

            worksheet_name[aggregator.name_en] = header_dict_for_loop_email_mobile_numbers['worksheet_name']%(str(aggregator.name_en),str(from_to_date[0]), str(from_to_date[1]))
        create_xlsx(workbook, data_set_all, table_properties, table_position_to_start, worksheet_name)


    def data_generator(self, from_to_date, aggregator_to_check_id_string):
        query = query_for_incorrect_phone_no_single_aggregator % (str(from_to_date[0]), str(from_to_date[1]), aggregator_to_check_id_string, str(from_to_date[0]), str(from_to_date[1]))
        query_result = onrun_query(query)
        return query_result


    def get_all_data(self,data_from_query_result):
        data = {'All':[]}
        i=0
        print data_from_query_result[:10]
        for result in data_from_query_result[:20]:
            print type(result)
            i=i+1
            # if result[5] >= 9999999999:
            #     result[5] = u'नंबर नहीं है'
            temp = list(result)
            print temp
            print type(temp)
            print i
            temp.insert( 2, "akad bakkad")
            print temp
            print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>."
            print result
            data['All'].append(list(result))
        return data

    def set_filtered_structured_data(self, data_store, aggregator):
    #filter data to get rows for the current aggregator
        i=0
        filtered_data = [row for row in data_store if row[0] == aggregator.name]
        #filtered_data = copy.deepcopy(filtered_data)
        i+=1
        for row in filtered_data:
            row.insert(0,str(i))
        return filtered_data


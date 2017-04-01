# coding=utf-8
__author__ = 'Lokesh'


from loop.models import LoopUser
from loop.utils.emailers_support import date_setter
from django.core.management.base import BaseCommand
from loop.utils.emailers_support.queries import *
from loop.utils.emailers_support.excel_generator import *
from loop.config import *
from django_pandas.io import read_frame



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
        print from_to_date
        print options.get('aggregator')
        print str(from_to_date[0])
        if options.get('aggregator') == 'all' or options.get('aggregator') == None:
            aggregator_to_check = ''
            workbook = create_workbook(header_dict_for_loop_email_mobile_numbers['workbook_name_all'])
        else:
            aggregator_to_check = LoopUser.objects.get(role=2, name_en=options.get('aggregator'))
            print aggregator_to_check.id
            aggregator_to_check = 'and ll.id = ' + str(aggregator_to_check.id) + ''
            workbook = create_workbook(header_dict_for_loop_email_mobile_numbers['workbook_name_specific'])

        print aggregator_to_check
        query = query_for_incorrect_phone_no_single_aggregator % (str(from_to_date[0]), str(from_to_date[1]), aggregator_to_check, str(from_to_date[0]), str(from_to_date[1]))
        print query
        query_result = onrun_query(query)
        print query_result
        data = {"All":[]}

        # data = {}
        #
        # df = read_frame(query_result)
        # data['All'] = [df]
        # writer = create_pandas_workbook('Testing_workbook.xlsx')
        # df.to_excel(writer)
        # workbook2 = writer.book



        for result in query_result:
            data['All'].append(list(result))


        caption = 'Incorrect mobile numbers of all aggregators'
        column_properties = [{'column_width': 5,
                            'header': u'क्रम संख्या',
                            'col_seq':'A:A',
                           },
                           {'column_width': 13,
                            'header': u'जमाकर्ता का नाम',
                            'col_seq':'B:B',
                           },
                           {'column_width': 12,
                            'header': u'गांव का नाम',
                            'col_seq':'C:C',
                           },
                           {'column_width': 8,
                            'header': u'किसान ID',
                            'col_seq':'D:D',
                           },
                           {'column_width': 15,
                            'header': u'किसान का नाम',
                            'col_seq':'E:E',
                           },
                           {'column_width': 8,
                            'header': u'सब्जी कितने दिन दी?',
                            'col_seq':'F:F',
                           },
                           {'column_width': 10,
                            'header': u'मोबाइल नं',
                            'col_seq':'G:G',
                           },
                           {'column_width': 10,
                            'header': u'कितने किसान में नंबर डला है?',
                            'col_seq':'H:H',
                           }]

        table_properties = {'data': None, 'autofilter': False, 'banded_rows': False, 'style': 'Table Style Light 15', 'columns': column_properties}
#        column_width = {'A:A':5,'B:B':5,'C:C':5,'D:D':5,'E:E':5,'F:F':5,'G:G':5,'H:H':5}
        table_position_to_start = {'row':2, 'col':0}
#        data = {"All":[[1,2,3,4,5,6,7,8]]}
        print query_result
        print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
        create_xlsx(workbook, data, table_properties, table_position_to_start, caption)

        # worksheet = writer.sheets['Sheet1']
        #
        # create_xlsx2(workbook2, data, table_properties, table_position_to_start, caption)





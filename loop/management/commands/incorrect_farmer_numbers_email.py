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




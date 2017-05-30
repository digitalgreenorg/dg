import datetime
from datetime import timedelta
from pytz import timezone

from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.utils.timezone import now
from django.db.models import Count, Sum

import dg.settings
from loop.models import HelplineExpert, HelplineIncoming, HelplineOutgoing, HelplineCallLog

from loop.utils.ivr_helpline.helpline_data import helpline_data

class Command(BaseCommand):
    # parse arguments from command line
    def add_arguments(self, parser):
        # create mutually exclusive command line switches
        group = parser.add_mutually_exclusive_group()
        group.add_argument('-fd',
                           dest='from_date',
                           default=None)

        parser.add_argument('-td',
                            dest='to_date',
                            default=None)

        group.add_argument('-nd',
                           dest='last_n_days',
                           default=None)

        parser.add_argument('-a',
                            dest='all_data',
                            default=None)

        parser.add_argument('-e',
                            dest='to_email',
                            default=None)
    
    # generate the excel for the given command line arguments
    def handle(self, *args, **options):
        all_data = options.get('all_data')
        to_email = options.get('to_email')
        if all_data != None:
            total_calls = HelplineCallLog.objects.filter(call_type=0).count()
            total_unique_caller = HelplineCallLog.objects.filter(call_type=0).values_list('from_number').distinct().count()
            total_repeat_caller = HelplineCallLog.objects.filter(call_type=0).values('from_number').annotate(call_count=Count('from_number')).filter(call_count__gt=1).count()
            total_calls_from_repeat_caller = HelplineCallLog.objects.filter(call_type=0).values('from_number').annotate(call_count=Count('from_number')).filter(call_count__gt=1).aggregate(Sum('call_count')).get('call_count__sum')
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


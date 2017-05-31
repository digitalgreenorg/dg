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
            repeat_caller_contribute_percentage = round((total_calls_from_repeat_caller*100.0) / total_calls,2)
            total_calls_resolved = HelplineIncoming.objects.filter(call_status=1).count()
            call_resoved_per_expert = HelplineIncoming.objects.filter(call_status=1).values('resolved_by__name').annotate(call_count=Count('id'))
            call_count_per_no = HelplineCallLog.objects.filter(call_type=0).values('from_number').annotate(call_count=Count('from_number'))
            # Cluster-wise bifurcation of calls received(farmer count, number of calls)
            farmer_detail = Farmer.objects.values('phone','village_id')
            phone_to_village_map = dict()
            village_to_call_detail_map = dict()
            cluster_wise_call_detail = dict()
            for farmer in farmer_detail:
                phone_to_village_map[farmer['phone']] = farmer['village_id']
            for call in call_count_per_no:
                farmer_number = call['from_number']
                farmer_number_possibilities = [farmer_number.lstrip('0'), farmer_number, '0'+farmer_number, '91'+farmer_number.lstrip('0'), '+91'+farmer_number.lstrip('0')]
                for number in farmer_number_possibilities:
                    if number in phone_to_village_map:
                        if phone_to_village_map[number] not in village_to_call_detail_map:
                            village_to_call_detail_map[phone_to_village_map[number]] = {'farmer_count':1,'total_calls':call['call_count']}
                        else:
                            village_to_call_detail_map[phone_to_village_map[number]]['farmer_count'] += 1
                            village_to_call_detail_map[phone_to_village_map[number]]['total_calls'] += call['call_count']
                        break
            loopuser_assigned_village = LoopUserAssignedVillage.objects.values('loop_user_id','loop_user__name','village_id')
            for user in loopuser_assigned_village:
                if user['loop_user_id'] not in cluster_wise_call_detail:
                    cluster_wise_call_detail[user['loop_user_id']] = dict()
                    cluster_wise_call_detail[user['loop_user_id']]['cluster_name'] = user['loop_user__name']
                    cluster_wise_call_detail[user['loop_user_id']]['farmer_count'] = 0
                    cluster_wise_call_detail[user['loop_user_id']]['total_calls'] = 0
                if user['village_id'] in village_to_call_detail_map:
                    cluster_wise_call_detail[user['loop_user_id']]['farmer_count'] += village_to_call_detail_map[user['village_id']]['farmer_count']
                    cluster_wise_call_detail[user['loop_user_id']]['total_calls'] += village_to_call_detail_map[user['village_id']]['total_calls']

        
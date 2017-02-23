from loop.models import AggregatorIncentive, AggregatorShareOutliers, CombinedTransaction, IncentiveParameter, LoopUser, IncentiveModel
from django.db.models import Count, Sum, Avg
import inspect

def compute_aggregator_share():
    ai_queryset = AggregatorIncentive.objects.all()
    aso_queryset = AggregatorShareOutliers.objects.all()
    combined_ct_queryset = CombinedTransaction.objects.values(
        'date', 'user_created_id', 'mandi').order_by('-date').annotate(Sum('quantity'), Sum('amount'),
                                                                       Count('farmer_id', distinct=True))
    aggregator_incentive_result = []

    incentive_param_queryset = IncentiveParameter.objects.all()

    for CT in combined_ct_queryset:
        amount_sum = 0.0
        user = LoopUser.objects.get(user_id=CT['user_created_id'])
        if CT['date'] not in [aso.date for aso in aso_queryset.filter(mandi=CT['mandi'], aggregator=user.id)]:
            try:
                ai_list_set = ai_queryset.filter(start_date__lte=CT['date'], aggregator=user.id).order_by('-start_date')
                if (ai_list_set.count() > 0):
                    exec (ai_list_set[0].incentive_model.calculation_method)
                    paramter_list = inspect.getargspec(calculate_inc)[0]
                    for param in paramter_list:
                        param_to_apply = incentive_param_queryset.get(notation=param)
                        x = calculate_inc(CT[param_to_apply.notation_equivalent])
                    amount_sum += x
                else:
                    amount_sum += CT['quantity__sum']*0.25
            except Exception:
                pass
        else:
            try:
                aso_share_date_aggregator = aso_queryset.filter(
                    date=CT['date'], aggregator=user.id, mandi=CT['mandi']).values('amount', 'comment')
                if aso_share_date_aggregator.count():
                    amount_sum += aso_share_date_aggregator[0]['amount']
            except AggregatorShareOutliers.DoesNotExist:
                pass
        aggregator_incentive_result.append(
            {'date': CT['date'], 'user_created__id': CT['user_created_id'], 'mandi__id': CT['mandi'], 'aggregator_incentive': amount_sum})

    return aggregator_incentive_result

from loop.models import AggregatorIncentive, AggregatorShareOutliers, CombinedTransaction, IncentiveParameter, LoopUser, IncentiveModel
from django.db.models import Count, Sum, Avg
import inspect
import datetime
from loop.constants.constants import MODEL_TYPES_DAILY_PAY, DATE_INCORRECT_FARMER_PHONE_MODEL
import pandas as pd

def calculate_inc_default(V):
    return 0.25*V

def compute_aggregator_share():
    ai_queryset = AggregatorIncentive.objects.all()
    aso_queryset = AggregatorShareOutliers.objects.all()
    combined_ct_queryset = CombinedTransaction.objects.filter(Q(date__lt=DATE_INCORRECT_FARMER_PHONE_MODEL) | Q(date__gte=F(farmer__correct_phone_date))).values(
        'date', 'user_created_id', 'mandi').order_by('-date').annotate(Sum('quantity'), Sum('amount'),
                                                                       Count('farmer_id', distinct=True))
    aggregator_incentive_result = []
    daily_pay_list = []

    incentive_param_queryset = IncentiveParameter.objects.all()

    for CT in combined_ct_queryset:
        amount_sum = 0.0
        user = LoopUser.objects.get(user_id=CT['user_created_id'])
        ai_list_set = ai_queryset.filter(start_date__lte=CT['date'], aggregator=user.id).order_by('-start_date')
        if ai_list_set and ai_list_set[0].model_type == MODEL_TYPES_DAILY_PAY:
            # SEPARATE OUT ALL DAILY PAY CASES
            exec (ai_list_set[0].incentive_model.calculation_method)
            amount_sum = calculate_inc()
            daily_pay_list.append({'date': CT['date'], 'user_created__id': CT['user_created_id'], 'mandi__id': CT['mandi'], 'aggregator_incentive': amount_sum, 'aggregator_id':user.id})
            continue
        elif CT['date'] not in [aso.date for aso in aso_queryset.filter(mandi=CT['mandi'], aggregator=user.id)]:
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
                    amount_sum += calculate_inc_default(CT['quantity__sum'])
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

    daily_pay_df = pd.DataFrame(daily_pay_list)
    try:
        daily_pay_mandi_count = daily_pay_df.groupby(['date','user_created__id']).agg({'mandi__id':'count'}).reset_index()
        daily_pay_mandi_count.rename(columns={"mandi__id":"mandi__count"}, inplace=True)
        daily_pay_df = pd.merge(daily_pay_df, daily_pay_mandi_count, on=['date','user_created__id'], how='left')
        daily_pay_df['aggregator_incentive'] = daily_pay_df['aggregator_incentive'] / daily_pay_df['mandi__count']

        for index, row in daily_pay_df.iterrows():
            outlier = aso_queryset.filter(date=row['date'], aggregator=row['aggregator_id'], mandi=row['mandi__id']).values('amount','comment')
            if outlier.count():
                daily_pay_df.loc[index,'aggregator_incentive'] = outlier[0]['amount']

        daily_pay_df.drop(['mandi__count','aggregator_id'], axis=1, inplace=True)
        daily_pay_df = daily_pay_df.round({'aggregator_incentive':2})
        daily_pay = daily_pay_df.to_dict(orient='records')

        aggregator_incentive_result.extend(daily_pay)
    except Exception:
        pass

    return aggregator_incentive_result

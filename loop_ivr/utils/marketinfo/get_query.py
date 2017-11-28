from loop_ivr.utils.marketinfo.raw_sql import query_for_transactions
from datetime import datetime, timedelta

def query_for_rates(crop_list, mandi_list, date_range=3):
    today_date = datetime.now()

    query = query_for_transactions.format('(%s)'%(crop_list[0],) if len(crop_list) == 1 else crop_list, '(%s)'%(mandi_list[0],) if len(mandi_list) == 1 else mandi_list, tuple((today_date-timedelta(days=day)).strftime('%Y-%m-%d') for day in range(0,date_range)))

    return query

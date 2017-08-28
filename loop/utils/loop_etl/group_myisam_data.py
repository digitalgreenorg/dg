from dg.settings import DATABASES
import MySQLdb
import datetime, time
import pandas as pd
import numpy as np
from loop.models import CombinedTransaction

def get_grouped_data(df_result_aggregate,day,df_farmers):
    start_date = df_result_aggregate['date'].min()
    # end_date = df_result_aggregate['date'].max()
    end_date = datetime.datetime.today()
    frequency = '-' + day + 'D'
    data_by_grouped_days = pd.DataFrame(pd.date_range(end_date,start_date,freq=frequency),columns={'start_date'})
    data_by_grouped_days['end_date'] = data_by_grouped_days['start_date'].shift(-1)
    data_by_grouped_days.fillna(value=0,inplace=True,axis=1)

    df_result_aggregate['date'] = df_result_aggregate['date'].astype('datetime64[ns]')
    for index,row in data_by_grouped_days.iterrows():
        end_date = row['end_date']
        start_date = row['start_date']

        data =  pd.Series(pd.DataFrame(df_result_aggregate.where((df_result_aggregate['date'] > end_date) & (df_result_aggregate['date'] <= start_date))).sum(numeric_only=True))

        data_by_grouped_days.loc[index,'amount__sum'] = data['amount']
        data_by_grouped_days.loc[index,'quantity__sum'] = data['quantity']
        data_by_grouped_days.loc[index,'farmer_share__sum'] = data['farmer_share']
        data_by_grouped_days.loc[index,'transportation_cost__sum'] = data['transportation_cost']
        data_by_grouped_days.loc[index,'gaddidar_share__sum'] = data['gaddidar_share']
        data_by_grouped_days.loc[index,'aggregator_incentive__sum'] = data['aggregator_incentive']

        data_by_grouped_days.loc[index,'active_cluster'] = df_result_aggregate.where((df_result_aggregate['date'] > end_date) & (df_result_aggregate['date'] <= start_date))['aggregator_id'].nunique()

        data_by_grouped_days.loc[index,'distinct_farmer_count'] = df_farmers.where((df_farmers['date'] > end_date) & (df_farmers['date']<=start_date))['farmer_id'].nunique()

    data_by_grouped_days = data_by_grouped_days.round()
    data_by_grouped_days = data_by_grouped_days.to_dict(orient='index')
    return data_by_grouped_days


def get_data_from_myisam(get_total, country_id, state_id):
    database = DATABASES['default']['NAME']
    username = DATABASES['default']['USER']
    password = DATABASES['default']['PASSWORD']
    host = DATABASES['default']['HOST']
    port = DATABASES['default']['PORT']
    mysql_cn = MySQLdb.connect(host=host, port=port, user=username, passwd=password, db=database, charset='utf8', use_unicode=True)

    if(int(state_id) < 0):
        #only country filter
        df_result = pd.read_sql("SELECT * FROM loop_aggregated_myisam where country_id = " + str(country_id), con=mysql_cn)
    elif(int(state_id) > 0):
        df_result = pd.read_sql("SELECT * FROM loop_aggregated_myisam where country_id = " + str(country_id) + " AND state_id = " + str(state_id), con=mysql_cn)
    aggregations = {
        'quantity':{
            'quantity__sum':'sum'
        },
        'amount':{
            'amount__sum':'sum'
        },
        'gaddidar_share':{
            'gaddidar_share__sum':'sum'
        },
        'aggregator_incentive':{
            'aggregator_incentive__sum':'mean'
        },
        'transportation_cost':{
            'transportation_cost__sum':'mean'
        },
        'farmer_share':{
            'farmer_share__sum':'mean'
        }
    }

    aggregate_cumm_vol_farmer_state = {
        'quantity':'sum',
        'cum_distinct_farmer':'mean'
    }

    aggregate_cumm_vol_farmer = {
        'quantity':'sum',
        'cum_distinct_farmer':'sum'
    }

    # MyISAM table contains CT, DT, Gaddidar, AggregatorIncentive.
    df_result_aggregate = df_result.groupby(['date','aggregator_id','mandi_id']).agg(aggregations).reset_index()
    df_result_aggregate.columns = df_result_aggregate.columns.droplevel(1)

    cumm_vol_farmer = {}
    if get_total == 0:
        if(int(state_id) < 0):
            df_farmers = pd.DataFrame(list(CombinedTransaction.objects.filter(mandi__district__state__country=country_id).values('date','farmer_id').order_by('date')))
        elif(int(state_id) > 0):
            df_farmers = pd.DataFrame(list(CombinedTransaction.objects.filter(mandi__district__state=state_id).values('date','farmer_id').order_by('date')))

        dictionary = {}
        
        df_farmers['date'] = df_farmers['date'].astype('datetime64[ns]')
        days = ['7','15','30','60']
        for day in days:
            data_by_grouped_days = get_grouped_data(df_result_aggregate,day,df_farmers)
            dictionary[day] = list(data_by_grouped_days.values())

        # Calcualting cummulative volume and farmer count
        df_state_cum_vol_farmer = df_result.groupby(['date', 'state_id']).agg(aggregate_cumm_vol_farmer_state).reset_index()#.groupby('date').agg(aggregate_cumm_vol_farmer).reset_index()
        # Aggregate Manually
        df_cum_vol_farmer = pd.DataFrame(columns=('date', 'cum_distinct_farmer', 'cum_vol'))
        index = 0
        curr_date = df_state_cum_vol_farmer['date'][0]
        state_wise_farmer = {}
        cum_vol = 0
        for i, row in df_state_cum_vol_farmer.iterrows():
            if row['date'] == curr_date:
                cum_vol += row['quantity']
                state_wise_farmer[row['state_id']] = row['cum_distinct_farmer']
            else:
                df_cum_vol_farmer.loc[index, 'date'] = curr_date
                df_cum_vol_farmer.loc[index, 'cum_distinct_farmer'] = sum(state_wise_farmer.values())
                df_cum_vol_farmer.loc[index, 'cum_vol'] = cum_vol
                index += 1
                curr_date = row['date']
                cum_vol += row['quantity']
                state_wise_farmer[row['state_id']] = row['cum_distinct_farmer']
        df_cum_vol_farmer.loc[index, 'date'] = curr_date
        df_cum_vol_farmer.loc[index, 'cum_distinct_farmer'] = sum(state_wise_farmer.values())
        df_cum_vol_farmer.loc[index, 'cum_vol'] = cum_vol
        # df_cum_vol_farmer['cum_vol'] = df_cum_vol_farmer['quantity'].cumsum().round()
        # df_cum_vol_farmer.drop('quantity',axis=1,inplace=True);
        cumm_vol_farmer = df_cum_vol_farmer.to_dict(orient='index')
    else:
        df_result_aggregate.drop(['mandi_id','aggregator_id'],axis=1,inplace=True)
        df = pd.DataFrame(df_result_aggregate.sum(numeric_only=True))
        dictionary = df.to_dict(orient='index')
    return dictionary, cumm_vol_farmer

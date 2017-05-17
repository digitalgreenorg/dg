from training.management.databases.utility import get_init_sql_ds, join_sql_ds
def get_training_data_sql(**Kwargs):
    start_date = Kwargs['start_date']
    end_date = Kwargs['end_date']
    apply_filter = Kwargs['apply_filter']
    trainers_list = Kwargs['trainers_list']
    sql_query_list = []
    args_list = []

    # No. of Trainings
    args_dict = {}
    sql_ds = get_init_sql_ds()
    sql_ds['select'].append('count(distinct tt.id)')
    sql_ds['from'].append('training_training tt')
    sql_ds['join'].append(['training_score ts', 'ts.training_id = tt.id'])
    # sql_ds['where'].append('date between \'' + start_date + '\' and \'' + end_date + '\'')
    sql_q = join_sql_ds(sql_ds)
    args_dict['query_tag'] = 'No. of Trainings'
    args_dict['component'] = 'overallBar'
    args_dict['query_string'] = sql_q
    args_dict['apply_filter'] = apply_filter
    if(args_dict['apply_filter'] is False) :
        args_list.append(args_dict)

    # No. of Trainings
    args_dict = {}
    sql_ds = get_init_sql_ds()
    sql_ds['select'].append('count(distinct tt.id)')
    sql_ds['from'].append('training_training tt')
    sql_ds['join'].append(['training_score ts', 'ts.training_id = tt.id and ' + 'tt.date between \'' + start_date + '\' and \'' + end_date + '\''])
    if apply_filter:
        sql_ds['join'].append(['training_training_trainer ttt','ttt.training_id = tt.id'])
        sql_ds['where'].append('ttt.trainer_id in ' +"("+ ",".join(trainers_list) + ")")
        # sql_ds['where'].append('date between \'' + start_date + '\' and \'' + end_date + '\'')
    sql_q = join_sql_ds(sql_ds)
    # print sql_ds
    # print sql_q
    args_dict['query_tag'] = 'No. of Trainings'
    args_dict['component'] = 'recentBar'
    args_dict['query_string'] = sql_q
    args_dict['apply_filter'] = True
    args_list.append(args_dict)

    return args_list

def get_mediators_data_sql(**Kwargs):
    start_date = Kwargs['start_date']
    end_date = Kwargs['end_date']
    apply_filter = Kwargs['apply_filter']
    sql_query_list = []
    args_list = []

    args_dict = {}
    sql_ds = get_init_sql_ds()
    sql_ds['select'].append('count(distinct ts.participant_id)')
    sql_ds['from'].append('training_score ts')
    # sql_ds['join'].append(['training_training_participants ttps', 'ts.training_id = ttps.training_id'])
    sql_ds['where'].append('ts.score in (0, 1)')
    sql_q = join_sql_ds(sql_ds)
    args_dict['query_tag'] = 'No. of Mediators'
    args_dict['component'] = 'overallBar'
    args_dict['query_string'] = sql_q
    args_dict['apply_filter'] = apply_filter
    if(args_dict['apply_filter'] is False) :
        args_list.append(args_dict)

    args_dict = {}
    sql_ds = get_init_sql_ds()
    sql_ds['select'].append('count(distinct ts.participant_id)')
    sql_ds['from'].append('training_score ts')
    sql_ds['join'].append(['training_training tt', 'ts.training_id = tt.id  and ' + 'tt.date between \'' + start_date + '\' and \'' + end_date + '\''])
    sql_ds['where'].append('ts.score in (0, 1)')
    sql_q = join_sql_ds(sql_ds)
    args_dict['query_tag'] = 'No. of Mediators'
    args_dict['component'] = 'recentBar'
    args_dict['query_string'] = sql_q
    args_dict['apply_filter'] = True
    args_list.append(args_dict)

    return args_list


def get_pass_perc_data_sql(**Kwargs):
    start_date = Kwargs['start_date']
    end_date = Kwargs['end_date']
    apply_filter = Kwargs['apply_filter']
    sql_query_list = []
    args_list = []

    # Pass_percentage
    args_dict = {}
    sql_ds = get_init_sql_ds()
    sql_ds['select'].append('ts.participant_id, (sum(ts.score)) sum_score,count(ts.score) score_count')
    sql_ds['from'].append('training_score ts')
    sql_ds['where'].append('ts.score in (0, 1)')
    sql_ds['group by'].append('ts.participant_id') #check group by training_id is required or not
    sql_q = join_sql_ds(sql_ds)

    sql_ds = get_init_sql_ds()
    sql_ds['select'].append('cast(round((COUNT(CASE WHEN (T.sum_score / T.score_count) >= 0.7 then 1 ELSE NULL END) / count(*))*100, 2) as char(10))')
    sql_ds['from'].append('(' + sql_q + ') T')
    sql_q = join_sql_ds(sql_ds)
    args_dict['query_tag'] = 'Pass Percentage'
    args_dict['component'] = 'overallBar'
    args_dict['query_string'] = sql_q
    args_dict['apply_filter'] = apply_filter
    if(args_dict['apply_filter'] is False) :
        args_list.append(args_dict)

    args_dict = {}
    sql_ds = get_init_sql_ds()
    sql_ds['select'].append('ts.participant_id, (sum(ts.score)) sum_score,count(ts.score) score_count')
    sql_ds['from'].append('training_score ts')
    sql_ds['join'].append(['training_training tt', 'ts.training_id = tt.id  and ' + 'tt.date between \'' + start_date + '\' and \'' + end_date + '\''])
    sql_ds['where'].append('ts.score in (0, 1)')
    sql_ds['group by'].append('ts.participant_id') #check group by training_id is required or not
    sql_q = join_sql_ds(sql_ds)

    sql_ds = get_init_sql_ds()
    sql_ds['select'].append('cast(round((COUNT(CASE WHEN (T.sum_score / T.score_count) >= 0.7 then 1 ELSE NULL END) / count(*))*100, 2) as char(10))')
    sql_ds['from'].append('(' + sql_q + ') T')
    sql_q = join_sql_ds(sql_ds)
    args_dict['query_tag'] = 'Pass Percentage'
    args_dict['component'] = 'recentBar'
    args_dict['query_string'] = sql_q
    args_dict['apply_filter'] = True
    args_list.append(args_dict)

    return args_list

def get_avg_score_data_sql(**Kwargs):
    start_date = Kwargs['start_date']
    end_date = Kwargs['end_date']
    apply_filter = Kwargs['apply_filter']
    sql_query_list = []
    args_list = []

        # Avg Score
    args_dict = {}
    sql_ds = get_init_sql_ds()
    sql_ds['select'].append('ts.participant_id, (sum(ts.score)) sum_score,count(ts.score) score_count')
    sql_ds['from'].append('training_score ts')
    sql_ds['where'].append('ts.score in (0, 1)')
    sql_ds['group by'].append('ts.participant_id') #check group by training_id is required or not
    sql_q = join_sql_ds(sql_ds)

    sql_ds = get_init_sql_ds()
    sql_ds['select'].append('cast(round(avg(T.sum_score), 2) as char(10))')
    sql_ds['from'].append('(' + sql_q + ') T')
    sql_q = join_sql_ds(sql_ds)
    args_dict['query_tag'] = 'Avg Score'
    args_dict['component'] = 'overallBar'
    args_dict['query_string'] = sql_q
    args_dict['apply_filter'] = apply_filter
    if(args_dict['apply_filter'] is False) :
        args_list.append(args_dict)

    args_dict = {}
    sql_ds = get_init_sql_ds()
    sql_ds['select'].append('ts.participant_id, (sum(ts.score)) sum_score,count(ts.score) score_count')
    sql_ds['from'].append('training_score ts')
    sql_ds['join'].append(['training_training tt', 'ts.training_id = tt.id  and ' + 'tt.date between \'' + start_date + '\' and \'' + end_date + '\''])
    sql_ds['where'].append('ts.score in (0, 1)')
    sql_ds['group by'].append('ts.participant_id') #check group by training_id is required or not
    sql_q = join_sql_ds(sql_ds)

    sql_ds = get_init_sql_ds()
    sql_ds['select'].append('cast(round(avg(T.sum_score), 2) as char(10))')
    sql_ds['from'].append('(' + sql_q + ') T')
    sql_q = join_sql_ds(sql_ds)
    args_dict['query_tag'] = 'Avg Score'
    args_dict['component'] = 'recentBar'
    args_dict['query_string'] = sql_q
    args_dict['apply_filter'] = True
    args_list.append(args_dict)

    return args_list

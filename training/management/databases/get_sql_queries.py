from training.management.databases.utility import get_init_sql_ds, join_sql_ds

def read_kwargs(Kwargs):
    return Kwargs['start_date'], Kwargs['end_date'], Kwargs['apply_filter'],Kwargs['trainers_list'],Kwargs['states_list']

def get_training_data_sql(**Kwargs):
    start_date, end_date, apply_filter, trainers_list, states_list = read_kwargs(Kwargs)

    sql_query_list = []
    args_list = []

    # No. of Trainings
    args_dict = {}
    sql_ds = get_init_sql_ds()
    sql_ds['select'].append('count(distinct tt.id)')
    sql_ds['from'].append('training_training tt')
    sql_ds['join'].append(['training_score ts', 'ts.training_id = tt.id'])
    sql_q = join_sql_ds(sql_ds)
    args_dict['query_tag'] = 'Number of Trainings'
    args_dict['component'] = 'overall'
    args_dict['query_string'] = sql_q
    args_dict['apply_filter'] = apply_filter
    if args_dict['apply_filter'] is False :
        args_list.append(args_dict.copy())

    if apply_filter:
        if len(trainers_list) > 0:
            sql_ds['join'].append(['training_training_trainer ttt','ttt.training_id = tt.id'])
            sql_ds['where'].append('ttt.trainer_id in (' + ",".join(trainers_list) + ")")
        if len(states_list) > 0:
            sql_ds['join'].append(['people_animator pa', 'pa.id = ts.participant_id'])
            sql_ds['join'].append(['geographies_district gd','pa.district_id = gd.id'])
            sql_ds['join'].append(['geographies_state gs','gs.id = gd.state_id'])
            sql_ds['where'].append('gs.id in (' + ",".join(states_list) + ')')

    sql_ds['where'].append('tt.date between \'' + start_date + '\' and \'' + end_date + '\'')

    sql_q = join_sql_ds(sql_ds)
    # args_dict['query_tag'] = 'No. of Trainings'
    args_dict['component'] = 'recent'
    args_dict['query_string'] = sql_q
    # args_dict['apply_filter'] = True
    args_list.append(args_dict.copy())

    return args_list

def get_mediators_data_sql(**Kwargs):
    start_date, end_date, apply_filter, trainers_list, states_list = read_kwargs(Kwargs)

    sql_query_list = []
    args_list = []

    args_dict = {}
    sql_ds = get_init_sql_ds()
    sql_ds['select'].append('count(distinct ts.participant_id)')
    sql_ds['from'].append('training_score ts')
    sql_ds['where'].append('ts.score in (0, 1)')
    sql_q = join_sql_ds(sql_ds)
    args_dict['query_tag'] = 'Number of Mediators'
    args_dict['component'] = 'overall'
    args_dict['query_string'] = sql_q
    args_dict['apply_filter'] = apply_filter
    if args_dict['apply_filter'] is False :
        args_list.append(args_dict.copy())


    if apply_filter:
        if len(trainers_list) > 0:
            sql_ds['join'].append(['training_training_trainer ttt','ttt.training_id = ts.training_id'])
            sql_ds['where'].append('ttt.trainer_id in (' + ",".join(trainers_list) + ")")
        if len(states_list) > 0:
            sql_ds['join'].append(['people_animator pa', 'pa.id = ts.participant_id'])
            sql_ds['join'].append(['geographies_district gd','pa.district_id = gd.id'])
            sql_ds['join'].append(['geographies_state gs','gs.id = gd.state_id'])
            sql_ds['where'].append('gs.id in (' + ",".join(states_list) + ')')

    sql_ds['where'].append('tt.date between \'' + start_date + '\' and \'' + end_date + '\'')
    sql_ds['join'].append(['training_training tt', 'ts.training_id = tt.id'])

    sql_q = join_sql_ds(sql_ds)
    # args_dict['query_tag'] = 'No. of Mediators'
    args_dict['component'] = 'recent'
    args_dict['query_string'] = sql_q
    # args_dict['apply_filter'] = True
    args_list.append(args_dict)

    return args_list


def get_pass_perc_data_sql(**Kwargs):
    start_date, end_date, apply_filter, trainers_list, states_list = read_kwargs(Kwargs)
    sql_query_list = []
    args_list = []

    # Pass_percentage
    args_dict = {}
    # Nested Query
    inner_sql_ds = get_init_sql_ds()
    inner_sql_ds['select'].append('ts.participant_id, (sum(ts.score)) sum_score,count(ts.score) score_count')
    inner_sql_ds['from'].append('training_score ts')
    inner_sql_ds['where'].append('ts.score in (0, 1)')
    inner_sql_ds['group by'].append('ts.participant_id') #check group by training_id is required or not
    inner_sql_q = join_sql_ds(inner_sql_ds)

    sql_ds = get_init_sql_ds()
    sql_ds['select'].append('cast(round((COUNT(CASE WHEN (T.sum_score / T.score_count) >= 0.7 then 1 ELSE NULL END) / count(*))*100, 2) as char(10))')
    sql_ds['from'].append('(' + inner_sql_q + ') T')
    sql_q = join_sql_ds(sql_ds)
    args_dict['query_tag'] = 'Pass Percentage'
    args_dict['component'] = 'overall'
    args_dict['query_string'] = sql_q
    args_dict['apply_filter'] = apply_filter
    if args_dict['apply_filter'] is False :
        args_list.append(args_dict.copy())

    if apply_filter:
        if len(trainers_list) > 0:
            inner_sql_ds['join'].append(['training_training_trainer ttt','ttt.training_id = ts.training_id'])
            inner_sql_ds['where'].append('ttt.trainer_id in (' + ",".join(trainers_list) + ")")
        if len(states_list) > 0:
            inner_sql_ds['join'].append(['people_animator pa', 'pa.id = ts.participant_id'])
            inner_sql_ds['join'].append(['geographies_district gd','pa.district_id = gd.id'])
            inner_sql_ds['join'].append(['geographies_state gs','gs.id = gd.state_id'])
            inner_sql_ds['where'].append('gs.id in (' + ",".join(states_list) + ')')

    inner_sql_ds['where'].append('tt.date between \'' + start_date + '\' and \'' + end_date + '\'')
    inner_sql_ds['join'].append(['training_training tt', 'ts.training_id = tt.id'])

    inner_sql_q = join_sql_ds(inner_sql_ds)

    sql_ds = get_init_sql_ds()
    sql_ds['select'].append('cast(round((COUNT(CASE WHEN (T.sum_score / T.score_count) >= 0.7 then 1 ELSE NULL END) / count(*))*100, 2) as char(10))')
    sql_ds['from'].append('(' + inner_sql_q + ') T')
    sql_q = join_sql_ds(sql_ds)
    # args_dict['query_tag'] = 'Pass Percentage'
    args_dict['component'] = 'recent'
    args_dict['query_string'] = sql_q
    # args_dict['apply_filter'] = True
    args_list.append(args_dict)

    return args_list

def get_avg_score_data_sql(**Kwargs):
    start_date, end_date, apply_filter, trainers_list, states_list = read_kwargs(Kwargs)
    sql_query_list = []
    args_list = []

    # Avg Score
    args_dict = {}
    inner_sql_ds = get_init_sql_ds()
    inner_sql_ds['select'].append('ts.participant_id, (sum(ts.score)) sum_score,count(ts.score) score_count')
    inner_sql_ds['from'].append('training_score ts')
    inner_sql_ds['where'].append('ts.score in (0, 1)')
    inner_sql_ds['group by'].append('ts.participant_id') #check group by training_id is required or not
    inner_sql_q = join_sql_ds(inner_sql_ds)

    sql_ds = get_init_sql_ds()
    sql_ds['select'].append('cast(round(avg(T.sum_score), 2) as char(10))')
    sql_ds['from'].append('(' + inner_sql_q + ') T')
    sql_q = join_sql_ds(sql_ds)
    args_dict['query_tag'] = 'Average Score'
    args_dict['component'] = 'overall'
    args_dict['query_string'] = sql_q
    args_dict['apply_filter'] = apply_filter
    if args_dict['apply_filter'] is False :
        args_list.append(args_dict.copy())

    if apply_filter:
        if len(trainers_list) > 0:
            inner_sql_ds['join'].append(['training_training_trainer ttt','ttt.training_id = ts.training_id'])
            inner_sql_ds['where'].append('ttt.trainer_id in (' + ",".join(trainers_list) + ")")
        if len(states_list) > 0:
            inner_sql_ds['join'].append(['people_animator pa', 'pa.id = ts.participant_id'])
            inner_sql_ds['join'].append(['geographies_district gd','pa.district_id = gd.id'])
            inner_sql_ds['join'].append(['geographies_state gs','gs.id = gd.state_id'])
            inner_sql_ds['where'].append('gs.id in (' + ",".join(states_list) + ')')
    inner_sql_ds['where'].append('tt.date between \'' + start_date + '\' and \'' + end_date + '\'')
    inner_sql_ds['join'].append(['training_training tt', 'ts.training_id = tt.id'])

    inner_sql_q = join_sql_ds(inner_sql_ds)

    sql_ds = get_init_sql_ds()
    sql_ds['select'].append('cast(round(avg(T.sum_score), 2) as char(10))')
    sql_ds['from'].append('(' + inner_sql_q + ') T')
    sql_q = join_sql_ds(sql_ds)
    # args_dict['query_tag'] = 'Avg Score'
    args_dict['component'] = 'recent'
    args_dict['query_string'] = sql_q
    # args_dict['apply_filter'] = True
    args_list.append(args_dict)

    return args_list

def trainings_mediators_query(**kwargs):
    start_date, end_date, apply_filter, trainers_list, states_list = read_kwargs(kwargs)
    sql_query_list = []
    args_list = []

    args_dict = {}
    inner_sql_ds = get_init_sql_ds()
    inner_sql_ds['select'].append('tt.id t_id, ts.participant_id p_id, SUM(ts.score) Sum_')
    inner_sql_ds['from'].append('training_score ts')
    inner_sql_ds['join'].append(['training_training tt', 'ts.training_id = tt.id'])
    inner_sql_ds['where'].append('ts.score in (0, 1)')
    inner_sql_ds['group by'].append('tt.id , ts.participant_id')

    sql_ds = get_init_sql_ds()
    sql_ds['select'].append('gs.state_name state, ttr.name trainer, COUNT(DISTINCT T.p_id) mediators, COUNT(DISTINCT T.t_id) trainings, count(case when T.Sum_ >= 11 then 1 end) Above70')

    sql_ds['join'].append(['training_training_trainer ttt','ttt.training_id = T.t_id'])
    sql_ds['join'].append(['training_trainer ttr','ttr.id = ttt.trainer_id'])
    sql_ds['join'].append(['people_animator pa', 'pa.id = T.p_id'])
    sql_ds['join'].append(['geographies_district gd','pa.district_id = gd.id'])
    sql_ds['join'].append(['geographies_state gs','gs.id = gd.state_id'])
    sql_ds['group by'].append('gs.id , ttr.id')

    if apply_filter:
        inner_sql_ds['where'].append('tt.date between \'' + start_date + '\' and \'' + end_date + '\'')
        if len(trainers_list) > 0:
            sql_ds['where'].append('ttt.trainer_id in (' + ",".join(trainers_list) + ")")
        if len(states_list) > 0:
            sql_ds['where'].append('gs.id in (' + ",".join(states_list) + ')')

    inner_sql_q = join_sql_ds(inner_sql_ds)
    sql_ds['from'].append('(' + inner_sql_q + ') T')
    sql_q = join_sql_ds(sql_ds)
    return sql_q

def question_wise_data_query(**kwargs):
    start_date, end_date, apply_filter, trainers_list, states_list = read_kwargs(kwargs)
    sql_query_list = []
    args_list = []
    apply_filter = True
    args_dict = {}
    inner_sql_ds = get_init_sql_ds()
    inner_sql_ds['select'].append('tq.section section, tq.serial serial, (sum(ts.score)/ count(ts.participant_id) * 100) Percentage')
    inner_sql_ds['from'].append('training_score ts')
    inner_sql_ds['join'].append(['training_question tq', 'tq.id = ts.question_id and ts.score in (0, 1)'])
    inner_sql_ds['where'].append('ts.score in (0, 1)')
    inner_sql_ds['group by'].append('tq.section, tq.serial')

    if apply_filter:
        inner_sql_ds['where'].append('tt.date between \'' + start_date + '\' and \'' + end_date + '\'')
        inner_sql_ds['join'].append(['training_training tt', 'ts.training_id = tt.id'])
        if len(trainers_list) > 0:
            inner_sql_ds['join'].append(['training_training_trainer ttt','ttt.training_id = tt.id'])
            inner_sql_ds['where'].append('ttt.trainer_id in (' + ",".join(trainers_list) + ")")
        if len(states_list) > 0:
            inner_sql_ds['join'].append(['people_animator pa', 'pa.id = ts.participant_id'])
            inner_sql_ds['join'].append(['geographies_district gd','pa.district_id = gd.id'])
            inner_sql_ds['join'].append(['geographies_state gs','gs.id = gd.state_id'])
            inner_sql_ds['where'].append('gs.id in (' + ",".join(states_list) + ')')

    inner_sql_q = join_sql_ds(inner_sql_ds)

    sql_ds = get_init_sql_ds()
    sql_ds['select'].append('tq.text Questions, T.percentage Percentage')
    sql_ds['from'].append('(' + inner_sql_q + ') T')
    sql_ds['join'].append(['training_question tq', 'tq.section = T.section and tq.serial = T.serial'])
    sql_ds['where'].append('tq.language_id = 2')
    sql_q = join_sql_ds(sql_ds)
    return sql_q

def year_month_wise_data_query(**kwargs):
    start_date, end_date, apply_filter, trainers_list, states_list = read_kwargs(kwargs)
    sql_query_list = []
    args_list = []
    args_dict = {}
    sql_ds = get_init_sql_ds()
    sql_ds['select'].append('MONTHNAME(tt.date) month, YEAR(tt.date) year, COUNT(DISTINCT tt.id) trainings')
    sql_ds['from'].append('training_training tt')
    sql_ds['group by'].append('year , MONTH(tt.date), month')
    sql_ds['order by'].append('year , MONTH(tt.date)')

    if apply_filter:
        sql_ds['where'].append('tt.date between \'' + start_date + '\' and \'' + end_date + '\'')
        sql_ds['join'].append(['training_score ts', 'ts.training_id = tt.id'])
        if len(trainers_list) > 0:
            sql_ds['join'].append(['training_training_trainer ttt','ttt.training_id = tt.id'])
            sql_ds['where'].append('ttt.trainer_id in (' + ",".join(trainers_list) + ")")
        if len(states_list) > 0:
            sql_ds['join'].append(['people_animator pa', 'pa.id = ts.participant_id'])
            sql_ds['join'].append(['geographies_district gd','pa.district_id = gd.id'])
            sql_ds['join'].append(['geographies_state gs','gs.id = gd.state_id'])
            sql_ds['where'].append('gs.id in (' + ",".join(states_list) + ')')

    sql_q = join_sql_ds(sql_ds)
    return sql_q

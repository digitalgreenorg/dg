# coding=utf-8
import copy


from loop.sendmail import common_send_email
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
        aggregators = LoopUser.objects.filter(role=2);
        if options.get('aggregator') == 'all' or options.get('aggregator') == None:
            aggregator_to_check_id_string = ''
            #workbook_name = get_workbook_name()
            workbook = create_workbook(header_dict_for_loop_email_mobile_numbers['workbook_name']%(MEDIA_ROOT, '' ,str(from_to_date[0]),str(from_to_date[1])))
        else:
            aggregator_to_check = aggregators.get(name_en=options.get('aggregator'))
            aggregator_to_check_id_string = 'and ll.id = ' + str(aggregator_to_check.id) + ''
            workbook = create_workbook(header_dict_for_loop_email_mobile_numbers['workbook_name']%(MEDIA_ROOT, str(aggregator_to_check.name) ,str(from_to_date[0]),str(from_to_date[1])))

        query_result_data = self.data_generator(from_to_date, aggregator_to_check_id_string)
        data_set_all = self.get_all_data(query_result_data)
        worksheet_name = {'All':'Incorrect Mobile Numbers_' + str(from_to_date[0]) + "_" + str(from_to_date[1])}

        for aggregator in aggregators:
            structured_data_set = self.set_filtered_structured_data(data_set_all['All'], aggregator)
            data_set_all[aggregator.name_en] = structured_data_set

            table_properties = {'data': None, 'autofilter': False, 'banded_rows': False, 'style': 'Table Style Light 15', 'columns': header_dict_for_loop_email_mobile_numbers['column_properties']}
            table_position_to_start = {'row':2, 'col':0}
            worksheet_name[aggregator.name_en] = header_dict_for_loop_email_mobile_numbers['worksheet_name']%(str(aggregator.name_en),str(from_to_date[0]), str(from_to_date[1]))

        create_xlsx(workbook, data_set_all, table_properties, table_position_to_start, worksheet_name)
        file_to_send = header_dict_for_loop_email_mobile_numbers['workbook_name']%(MEDIA_ROOT, '',str(from_to_date[0]),str(from_to_date[1]))
        common_send_email("Hello Logo", recipients= RECIPIENTS, files=[file_to_send], bcc=[], from_email='lokesh@digitalgreen.org', html="", text='hello')


    # create_format = Functions.create_format

    # Parameters provided at command prompt
    # By default, daily_a_m_filtered must take entire time period because it will be used in impact code

    def data_generator(self, from_to_date, aggregator_to_check_id_string):
        query = daily_a_m_query
        query_result = onrun_query(query)
        return query_result


    # TODO: Use this too.
    aggregator_list = []

    # List ordered by aggregator, market, TCPK
    daily_a_m_query_result = daily_a_m_query_result

    # Position of relevant columns
    dam_aggregator_id_col = 0
    dam_mandi_id_col = 1
    dam_date_col = 2
    insert_row_from_this_col = 2
    dam_aggregator_name_col = 3
    dam_type_col = 7
    dam_TCPK_col = 8

    # List ordered by aggregator, market
    a_m_count_query_result = a_m_count_query_result
    aggregator_id_col = 0
    mandi_id_col = 1
    count_col = 4

    # Dictionary {(aggregator id, market id): count of visits}
    a_m_count = a_m_count

    daily_a_m_filtered = []

    # This dictionary will contain aggregator-wise outliers data
    aggregator_wise_TCost_outliers = {}
    aggregator_wise_TCost_correct = {}

    # Purpose: Takes a list and returns the row for given percentile value
    # Parameters: dataset - list, it should be sorted
    #             column - element of list on which percentile would be computed
    #             start - first row of aggregator-market combination
    #             length - number of elements in list for this aggregator-market combination
    #             percentile - percentile value


    def get_percentile(dataset, column, start, length, percentile):
        if length == 0:
            return None
        percentile_position = (length - 1) * percentile
        floor = math.floor(percentile_position)
        ceiling = math.ceil(percentile_position)
        if column == -1:
            if floor == ceiling:
                return dataset[int(start + percentile_position)]
            elif dataset[int(start + floor)] and dataset[int(start + ceiling)]:
                d0 = dataset[int(start + floor)] * (ceiling - percentile_position)
                d1 = dataset[int(start + ceiling)] * (percentile_position - floor)
                return d0 + d1
            else:
                return None
        else:
            if floor == ceiling:
                return dataset[int(start + percentile_position)][int(column)]
            elif dataset[int (start + floor)][int(column)] and dataset[int(start + ceiling)][int(column)]:
                d0 = dataset[int(start + floor)][int(column)] * (ceiling - percentile_position)
                d1 = dataset[int(start + ceiling)][int(column)] * (percentile_position - floor)
                return d0+d1
            else:
                return None

    start_point = 0
    element = 8

    # Finds all quartile values for each aggregator-market combination and updates in a_m_count
    # a_m_count_query_result is a list and not a dictionary because the order of traversal is important as list is sorted
    # TODO: 1.5 and 0.75 to be provided by user
    for line in a_m_count_query_result:
        total_count = line[count_col]
        median_value = get_percentile(daily_a_m_query_result, element, start_point,total_count,0.5)
        first_quartile_value = get_percentile(daily_a_m_query_result, element, start_point,total_count,0.25)
        third_quartile_value = get_percentile(daily_a_m_query_result, element, start_point,total_count,0.75)
        inter_quartile_range = None
        upper_fence = None
        lower_fence = None
        if median_value and first_quartile_value and third_quartile_value:
            inter_quartile_range = third_quartile_value - first_quartile_value
            upper_fence = third_quartile_value + 1.5*inter_quartile_range
            lower_fence = first_quartile_value - 0.75*inter_quartile_range
        a_m_count[(line[aggregator_id_col], line[mandi_id_col])].update((('Q1', first_quartile_value), ('M', median_value), ('Q3', third_quartile_value), ('IQR', inter_quartile_range), ('UF', upper_fence), ('LF', lower_fence)))
        start_point += total_count
        if first_quartile_value > third_quartile_value:
            print line[aggregator_id_col], line[mandi_id_col], total_count, first_quartile_value, third_quartile_value
    high_cpk = []
    low_cpk = []
    no_cpk = []
    ok_cpk = []

    # Identifies outliers from daily_a_m_query_result and appends them in aggregator_wise_outliers
    # daily_a_m_query_result is a list and not a dictionary because the order of traversal is important as list is sorted
    # outliers are sorted by market-cpk. To change sorting criteria, insertion in outliers table should be defined accordingly
    # aggregator-wise outliers key is aggregator name and not ID because key is mapped to each sheet name. Both of them needs to be unique.
    # So, we have to ensure that aggregator names are unique

    from_date = time_period[0]
    to_date = time_period[1]



    for line in daily_a_m_query_result:
        if line[dam_date_col] >= from_date and line[dam_date_col] <= to_date:
            daily_a_m_filtered.append(line)

    # TODO: It should check whether transport cost was changed later by admin or not. If yes, it's not an outlier to worry about.
    for line in daily_a_m_filtered:
        daily_a_m_line = list(line)  # converts tuple into a list because we want to add a parameter in each row
        TCPK = daily_a_m_line[dam_TCPK_col]
        aggregator_id = daily_a_m_line[dam_aggregator_id_col]
        mandi_id = daily_a_m_line[dam_mandi_id_col]
        aggregator_name = daily_a_m_line[dam_aggregator_name_col]
        date = daily_a_m_line[dam_date_col]
        if TCPK:  # Check: TCPK exists
            if TCPK > a_m_count[(aggregator_id, mandi_id)]['UF']:  # Check: TCPK > Upper Fence
                daily_a_m_line[dam_type_col] = 'High CPK'
                if aggregator_name in aggregator_wise_TCost_outliers.keys():  # Check: Aggregator ID exists
                    aggregator_wise_TCost_outliers[aggregator_name].append(daily_a_m_line[insert_row_from_this_col:])
                else:
                    aggregator_wise_TCost_outliers[aggregator_name] = [daily_a_m_line[insert_row_from_this_col:]]
                high_cpk.append(daily_a_m_line[insert_row_from_this_col:])
            elif TCPK < a_m_count[(aggregator_id, mandi_id)]['LF']:  # Check: TCPK < Lower Fence
                daily_a_m_line[dam_type_col] = 'Low CPK'
                if aggregator_name in aggregator_wise_TCost_outliers.keys():
                    aggregator_wise_TCost_outliers[aggregator_name].append(daily_a_m_line[insert_row_from_this_col:])
                else:
                    aggregator_wise_TCost_outliers[aggregator_name] = [daily_a_m_line[insert_row_from_this_col:]]
                low_cpk.append(daily_a_m_line[insert_row_from_this_col:])
            else:
                if aggregator_name in aggregator_wise_TCost_correct.keys():
                    aggregator_wise_TCost_correct[(aggregator_id, mandi_id,date)].append(daily_a_m_line)
                else:
                    aggregator_wise_TCost_correct[(aggregator_id, mandi_id, date)] = [daily_a_m_line]
                ok_cpk.append(daily_a_m_line[insert_row_from_this_col:])

        else:
            daily_a_m_line[dam_type_col] = 'No CPK'
            if aggregator_name in aggregator_wise_TCost_outliers.keys():
                aggregator_wise_TCost_outliers[aggregator_name].append(daily_a_m_line[insert_row_from_this_col:])
            else:
                aggregator_wise_TCost_outliers[aggregator_name] = [daily_a_m_line[insert_row_from_this_col:]]
            no_cpk.append(daily_a_m_line[insert_row_from_this_col:])

    print 'high_cpk'
    print len(high_cpk)
    print 'low_cpk'
    print len(low_cpk)
    print 'no_cpk'
    print len(no_cpk)
    print 'ok_cpk'
    print len(ok_cpk)

    # Adds all No CPK, Low CPK, High CPK entries in this order. Sorting order within each of them is A-M
    aggregator_wise_TCost_outliers['All'] = no_cpk
    aggregator_wise_TCost_outliers['All'].extend(low_cpk)
    aggregator_wise_TCost_outliers['All'].extend(high_cpk)

    # print aggregator_wise_TCost_correct

    # Position of All is first as a co-incidence I think.
    workbook = create_workbook('Transport Cost Outliers.xlsx')
    all_format = ['date_format']
    all_format_created = create_format(all_format, workbook)
    column_properties = [{'header': 'Date', 'format': all_format_created['date_format']}, {'header': 'Aggregator'}, {'header': 'Market'}, {'header': 'Quantity'}, {'header': 'TCost'}, {'header': 'Type'}, {'header': 'TCPK'}, {'header': 'FShare'}]
    table_properties = {'data': None, 'autofilter': False, 'banded_rows': False, 'style': 'Table Style Light 15', 'columns': column_properties}
    column_width = {'A:A': 10.55, 'B:B': 9.36}
    create_xlsx(workbook, aggregator_wise_TCost_outliers, table_properties, column_width_and_format = column_width)

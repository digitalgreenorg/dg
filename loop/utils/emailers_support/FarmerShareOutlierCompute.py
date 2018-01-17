__author__ = 'Lokesh'

from loop.utils.emailers_support.excel_generator import *
from loop.utils.emailers_support.queries import *


class FarmerShareOutlier(object):
    def data_Manipulator(self, daily_a_m_farmerShare, time_period):
        # List ordered by aggregator, market, date
        aggregator_id_col = 0
        market_col = 1
        date_col = 2
        aggregator_name_col = 3
        FSPK_col = 8
        FSPTC_col = 9

        # Dictionary {(aggregator id, market id): count of visits}
        a_m_count_query_result = onrun_query(a_m_count_query)
        keys = ('Aggregator', 'Market', 'C')
        a_m_count = convert_query_result_in_nested_dictionary(a_m_count_query_result, keys, 2)

        # initialisation
        start_point = 0
        count = 0
        aggregator_id = daily_a_m_farmerShare[0][aggregator_id_col]
        aggregator_name = daily_a_m_farmerShare[0][aggregator_name_col]
        market_id = daily_a_m_farmerShare[0][market_col]
        last_FSPK = daily_a_m_farmerShare[0][FSPK_col]
        last_FSPTC = daily_a_m_farmerShare[0][FSPTC_col]
        no_of_rows = a_m_count[(aggregator_id, market_id)]['C']

        aggregator_wise_FShare_outliers = {'All': []}
        daily_a_m_farmerShare_filtered = []

        from_date = time_period[0]
        to_date = time_period[1]

        for line in daily_a_m_farmerShare:
            if type(from_date) is str:
                if str(line[date_col]) >= from_date and str(line[date_col]) <= to_date:
                    daily_a_m_farmerShare_filtered.append(line)
            else:
                if line[date_col] >= from_date and line[date_col] <= to_date:
                    daily_a_m_farmerShare_filtered.append(line)

        for line in daily_a_m_farmerShare_filtered:
            FSPK = line[FSPK_col]
            FSPTC = line[FSPTC_col]
            if count < no_of_rows + start_point:
                if FSPK != last_FSPK and FSPTC != last_FSPTC:
                    aggregator_wise_FShare_outliers['All'].append(line[2:])
            else:
                aggregator_id = line[aggregator_id_col]
                aggregator_name = line[aggregator_name_col]
                market_id = line[market_col]
                start_point += no_of_rows
                no_of_rows = a_m_count[(aggregator_id, market_id)]['C']
            count += 1
            last_FSPK = FSPK
            last_FSPTC = FSPTC
        return aggregator_wise_FShare_outliers

import pandas as pd

# All functions within get_statistics functions are written in this file
from Crop_Rate_Outliers_Removal_Common_Function import *

group_by_list = ['Date', 'Market', 'Crop']
final_group_by = ['Crop','Market','Date']
columnlist_ct = ['Date', 'Aggregator', 'Market', 'Gaddidar', 'Farmer','Crop', 'Quantity', 'Price', 'Amount', 'Initial_Total_Quantity']



# This function groups cleaned data on Date-Market_Crop combination and returns Av_Rate
def get_grouped_clean_data(combined_transactions_data = None):
    try:
        combined_transactions_data = get_clean_data(combined_transactions_data)
        combined_transactions_data.fillna(0, inplace=True)
        combined_transactions_data = combined_transactions_data[combined_transactions_data['Flag'] == 1]

        # TODO: Total Quantity Sum is wrong because Total_Quantity already has summation
        combined_transactions_data = combined_transactions_data.groupby(group_by_list).agg(
            {'Av_Rate': ['mean'], 'STD': ['mean'], 'Price': ['max', 'min'], 'Total_Quantity': ['sum']}).reset_index()
        combined_transactions_data.columns = ["".join(agg) for agg in combined_transactions_data.columns.ravel()]

        # Arranging dataframe according to crop, market and date
        # combined_transactions_data = combined_transactions_data.groupby(final_group_by).apply(lambda x: x.sort_values(['Crop','Market_Real','Date'],ascending=[True,True,False])).reset_index(drop=True)
        combined_transactions_data = combined_transactions_data.sort_values(
            ['Crop', 'Market', 'Date', 'Total_Quantitysum'], ascending=[True, True, False, False])
        return combined_transactions_data
    except Exception as e:
        return None

# This function removes outliers from combined transactions data
def get_clean_data (combined_transactions_data = None):
    try:
        combined_transactions_data = flag_crop_outliers(combined_transactions_data)
        combined_transactions_data.fillna(0, inplace=True)
        combined_transactions_data = combined_transactions_data[combined_transactions_data['Flag'] == 1]
        return combined_transactions_data
    except Exception as e:
        return None

# This function puts appropriate flag in all combined transactions data
def flag_crop_outliers(combined_transactions_data):

    # combined_transactions_data['Date'] = pd.to_datetime(combined_transactions_data['Date'])

    # ...
    get_initial_total_quantity = combined_transactions_data.groupby(group_by_list).agg({'Quantity': ['sum']}).reset_index()
    get_initial_total_quantity.columns = get_initial_total_quantity.columns.droplevel(1)
    get_initial_total_quantity = get_initial_total_quantity.rename(columns = {'Quantity': 'Initial_Total_Quantity'})

    combined_transactions_data = pd.merge(combined_transactions_data, get_initial_total_quantity, on= group_by_list)
    combined_transactions_final_data = pd.DataFrame()
    combined_transactions_non_iteration_data = pd.DataFrame()

    # print 'Flag_Crop_Outliers'
    # print combined_transactions_data.head()
    #***
    combined_transactions_data = call_methods(combined_transactions_data, combined_transactions_final_data, combined_transactions_non_iteration_data)

    #for recursion_counter in range(0,3):
     #   combined_transactions_data.fillna(0,inplace=True)
      #  ct_data = combined_transactions_data[(combined_transactions_data['D/STD'] > 1.3)]
       # if ct_data is not None:
        #    combined_transactions_data = combined_transactions_data[(combined_transactions_data['D/STD'] <= 1.3)]
         #   combined_transactions_data = combined_transactions_data[columnlist_ct]
          #  combined_transactions_data = call_methods(combined_transactions_data)
        #else:
         #   break

    # combined_transactions_data = combined_transactions_data[(combined_transactions_data['D/STD'] <= 1.3)]
    # combined_transactions_data = combined_transactions_data[columnlist_ct]
    # combined_transactions_data = call_methods(combined_transactions_data)

    return combined_transactions_data

def call_methods(combined_transactions_data, combined_transactions_final_data, combined_transactions_non_iteration_data):
    combined_transactions_data = get_statistics(combined_transactions_data)
    combined_transactions_data = raise_flags(combined_transactions_data)

    #...
    combined_transactions_final_data = run_iterate(combined_transactions_data, combined_transactions_final_data, combined_transactions_non_iteration_data)
    #***

    # combined_transactions_data = combined_transactions_data[(combined_transactions_data['Flag']==1) | (combined_transactions_data['Flag']==5)]

    return combined_transactions_final_data

# This function inserts all statistics in combined_transactions_data: Mean, Total Quantity, Deviation, Max Deviation, STD, some ratios
def get_statistics(combined_transactions_data):
    ct_data_with_mean = combined_transactions_data.groupby(group_by_list).apply(compute_mean).reset_index(name='Av_Rate')
    combined_transactions_data = combined_transactions_data.merge(ct_data_with_mean,how='left',on=group_by_list)

    ct_with_total_quanity = combined_transactions_data.groupby(group_by_list).apply(
        compute_total_q).reset_index(name='Total_Quantity')
    combined_transactions_data = combined_transactions_data.merge(ct_with_total_quanity, how='left',
                                                                  on=group_by_list)

    combined_transactions_data = compute_deviation(combined_transactions_data)

    ct_with_max_deviation = combined_transactions_data.groupby(group_by_list).apply(compute_max_deviation).reset_index(name= 'Max_Deviation')
    combined_transactions_data = combined_transactions_data.merge(ct_with_max_deviation,how='left',on=group_by_list)

    ct_with_std = combined_transactions_data.groupby(group_by_list).apply(compute_std).reset_index(name= 'STD')
    combined_transactions_data = combined_transactions_data.merge(ct_with_std,how='left',on=group_by_list)

    combined_transactions_data = compute_ratios(combined_transactions_data)
    # print 'Get Statistics: '
    # print combined_transactions_data.head()
    return combined_transactions_data


# Flag = 0: Untouched
# Flag = 1: Okay
# Flag = 2: MI Outlier
# Flag = 3: Incorrect data. Ask admin
# Flag = 4: No clue. Try other method. Don't send to MI.
# Flag = 5: Iterate.

def raise_flags(combined_transactions_data):
    # All STD should get replaced by STD/Mean and/or D/Mean
    # For STD< 1, still find Flag #3 by checking D/Mean ratio?
    combined_transactions_data.loc[combined_transactions_data['STD'] <= 1, 'Flag'] = 1

    combined_transactions_data.loc[
        (combined_transactions_data['STD'] <= 2) & (combined_transactions_data['STD'] > 1) & (
            combined_transactions_data['Max_Deviation'] / combined_transactions_data['STD'] > 1.3), 'Flag'] = 5
    combined_transactions_data.loc[
        (combined_transactions_data['STD'] <= 2) & (combined_transactions_data['STD'] > 1) & (
            combined_transactions_data['Max_Deviation'] / combined_transactions_data['STD'] > 1) & (
            combined_transactions_data['Max_Deviation'] / combined_transactions_data['STD'] <= 1.3) & (combined_transactions_data['Deviation_Factor'] > 0.5), 'Flag'] = 2
    combined_transactions_data.loc[
        (combined_transactions_data['STD'] <= 2) & (combined_transactions_data['STD'] > 1) & (
            combined_transactions_data['Max_Deviation'] / combined_transactions_data['STD'] > 1) & (
            combined_transactions_data['Max_Deviation'] / combined_transactions_data['STD'] <= 1.3) & (
        combined_transactions_data['Deviation_Factor'] <= 0.5), 'Flag'] = 1
    combined_transactions_data.loc[
        (combined_transactions_data['STD'] <= 2) & (combined_transactions_data['STD'] > 1) & (
            combined_transactions_data['Max_Deviation'] / combined_transactions_data['STD'] <= 1), 'Flag'] = 1

    combined_transactions_data.loc[(combined_transactions_data['STD'] <= 3) & (combined_transactions_data['STD'] > 2) & (
        combined_transactions_data['Max_Deviation']/combined_transactions_data['STD'] <= 1.3), 'Flag'] = 4
    combined_transactions_data.loc[
        (combined_transactions_data['STD'] <= 3) & (combined_transactions_data['STD'] > 2) & (
            combined_transactions_data['Max_Deviation'] / combined_transactions_data['STD'] > 1.3), 'Flag'] = 5

    combined_transactions_data.loc[(combined_transactions_data['STD'] > 3) & (combined_transactions_data['STD'] <= 6.5) & (combined_transactions_data['Max_Deviation']/combined_transactions_data['STD'] > 1.3), 'Flag'] = 5
    combined_transactions_data.loc[
        (combined_transactions_data['STD'] > 3) & (combined_transactions_data['STD'] <= 6.5) & (
        combined_transactions_data['Max_Deviation'] / combined_transactions_data['STD'] <= 1.3), 'Flag'] = 4

    combined_transactions_data.loc[
        (combined_transactions_data['STD'] > 6.5) & (combined_transactions_data['STD'] <= 9) & (
        combined_transactions_data['Max_Deviation'] / combined_transactions_data['STD'] > 1.3), 'Flag'] = 5
    combined_transactions_data.loc[
        (combined_transactions_data['STD'] > 6.5) & (combined_transactions_data['STD'] <= 9) & (
            combined_transactions_data['Max_Deviation'] / combined_transactions_data['STD'] <= 1.3), 'Flag'] = 4

    combined_transactions_data.loc[(combined_transactions_data['STD'] > 9), 'Flag'] = 4

    # Should this be placed at the beginning of run_iterate function?
    combined_transactions_data.loc[combined_transactions_data['Total_Quantity'] < 0.6 * combined_transactions_data[
        'Initial_Total_Quantity'], 'Flag'] = 4

    # print 'Raise Flags'
    # print combined_transactions_data.head()
    return combined_transactions_data

# ...
def run_iterate(combined_transactions_data, combined_transactions_final_data, combined_transactions_non_iteration_data):

    combined_transactions_final_data = combined_transactions_final_data.append(combined_transactions_data[combined_transactions_data['Flag'] != 5])

    # Removes ct row with maximum deviation for date-market-crop combination
    combined_transactions_iteration_data = combined_transactions_data[(combined_transactions_data['Flag'] == 5) & (combined_transactions_data['Deviation'] < combined_transactions_data['Max_Deviation'])]
    combined_transactions_non_iteration_data = combined_transactions_non_iteration_data.append(combined_transactions_data[(combined_transactions_data['Flag'] == 5) & (combined_transactions_data['Deviation'] == combined_transactions_data['Max_Deviation'])])
    if combined_transactions_iteration_data is not None and not combined_transactions_iteration_data.empty:
        combined_transactions_iteration_data = combined_transactions_iteration_data[columnlist_ct]
        call_methods(combined_transactions_iteration_data, combined_transactions_final_data, combined_transactions_non_iteration_data)
    else:
        combined_transactions_non_iteration_data['Flag'] = 2
        grouped_combined_transactions_final_data = combined_transactions_final_data.groupby(group_by_list).agg({'Flag': ['max', 'min']}).reset_index()
        grouped_combined_transactions_final_data.columns = ["".join(agg) for agg in grouped_combined_transactions_final_data.columns.ravel()]
        combined_transactions_non_iteration_data = pd.merge(combined_transactions_non_iteration_data, grouped_combined_transactions_final_data, how='left', on= group_by_list)
        combined_transactions_non_iteration_data.loc[(combined_transactions_non_iteration_data['Flagmax'] == 4) & (combined_transactions_non_iteration_data['Flagmin'] == 4), 'Flag'] = 4
        combined_transactions_final_data = combined_transactions_final_data.append(combined_transactions_non_iteration_data)
    # print 'Iteration'
    # print combined_transactions_data.head()
    return combined_transactions_final_data
import Tables
import numpy as np
import pandas as pd

daily_aggregator_market_crop_rate_query_result = Tables.daily_aggregator_market_crop_rate_query_result

daily_aggregator_market_crop_rate_query_result = list(daily_aggregator_market_crop_rate_query_result)
columnlist_ct = ['Date', 'Aggregator', 'Market_Real', 'Crop', 'Quantity_Real', 'Price', 'Amount', 'State']
combined_transactions_data = pd.DataFrame(daily_aggregator_market_crop_rate_query_result, columns=columnlist_ct)
combined_transactions_data['Date'] = pd.to_datetime(combined_transactions_data['Date'])

# Filters out data of other states
combined_transactions_data = combined_transactions_data[combined_transactions_data['Market_Real'] == 3]

def compute_mean(group):
    Av_Rate = group.Amount.sum()/group.Quantity_Real.sum()
    return Av_Rate

def compute_total_q(group):
    Total_Quantity = group.Quantity_Real.sum()
    return Total_Quantity

def compute_deviation(group):
    group['Deviation'] = abs(group.Price - group.Av_Rate)
    return group

def compute_std(group):
    std = np.sqrt(((np.square(group.Deviation)*group.Quantity_Real).sum())/group.Quantity_Real.sum())
    return std

def compute_max_deviation(group):
    Max_Deviation = group.Deviation.max()
    return Max_Deviation

def compute_ratios(group):
    group['D/Av'] = group['Deviation'] / group['Av_Rate']
    group['D/STD'] = group['Deviation'] / group['STD']
    group['Deviation_Factor'] = group['D/Av'] * group['D/STD']
    group['STD/Av'] = group['STD'] / group['Av_Rate']
    group['Flag'] = 0
    group['Compute'] = 1
    return group


def calculate(combined_transactions_data):
    #combined_transactions_data = combined_transactions_data[combined_transactions_data['Compute'] == 1]

    combined_transactions_data_1 = combined_transactions_data.groupby(['Date', 'Market_Real', 'Crop']).apply(compute_mean).reset_index(name= 'Av_Rate')
    combined_transactions_data = combined_transactions_data.merge(combined_transactions_data_1,how='left',on=['Date','Market_Real','Crop'])

    combined_transactions_data_1 = combined_transactions_data.groupby(['Date', 'Market_Real', 'Crop']).apply(
        compute_total_q).reset_index(name='Total_Quantity')
    combined_transactions_data = combined_transactions_data.merge(combined_transactions_data_1, how='left',
                                                                  on=['Date', 'Market_Real', 'Crop'])

    combined_transactions_data = compute_deviation(combined_transactions_data)

    combined_transactions_data_1 = combined_transactions_data.groupby(['Date', 'Market_Real', 'Crop']).apply(compute_max_deviation).reset_index(name= 'Max_Deviation')
    combined_transactions_data = combined_transactions_data.merge(combined_transactions_data_1,how='left',on=['Date','Market_Real','Crop'])

    combined_transactions_data_1 = combined_transactions_data.groupby(['Date', 'Market_Real', 'Crop']).apply(compute_std).reset_index(name= 'STD')
    combined_transactions_data = combined_transactions_data.merge(combined_transactions_data_1,how='left',on=['Date','Market_Real','Crop'])

    combined_transactions_data = compute_ratios(combined_transactions_data)

    return combined_transactions_data

# Flag = 0: Untouched
# Flag = 1: Okay
# Flag = 2: MI Outlier
# Flag = 3: Incorrect data. Ask admin
# Flag = 4: No clue. Try other method. Don't send to MI.
# Flag = 5: Iterate.

def flag(combined_transactions_data):
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
    # combined_transactions_data.loc[(combined_transactions_data['STD'] > 9) & (combined_transactions_data['STD/Av'] <= 0.1), 'Flag'] = 1
    combined_transactions_data.to_csv("check_5.csv")
    return combined_transactions_data

    #combined_transactions_data_5 = combined_transactions_data[(combined_transactions_data['Flag']== 5) & (combined_transactions_data['Compute'] == 1)]
#print combined_transactions_data_5.head()
# combined_transactions_data.to_csv("first.csv")

def iterate(combined_transactions_data):

    cols = list(combined_transactions_data_5.loc[:, 'Date':'State'])
    combined_transactions_data = combined_transactions_data_5[cols]

    combined_transactions_data_1 = combined_transactions_data.groupby(['Date', 'Market_Real', 'Crop']).apply(compute_mean).reset_index(name= 'Av_Rate')
    combined_transactions_data = combined_transactions_data.merge(combined_transactions_data_1,how='left',on=['Date','Market_Real','Crop'])
    combined_transactions_data = compute_deviation(combined_transactions_data)

    combined_transactions_data_1 = combined_transactions_data.groupby(['Date', 'Market_Real', 'Crop']).apply(compute_max_deviation).reset_index(name= 'Max_Deviation')
    combined_transactions_data = combined_transactions_data.merge(combined_transactions_data_1,how='left',on=['Date','Market_Real','Crop'])

    combined_transactions_data_1 = combined_transactions_data.groupby(['Date', 'Market_Real', 'Crop']).apply(compute_std).reset_index(name= 'STD')
    combined_transactions_data = combined_transactions_data.merge(combined_transactions_data_1,how='left',on=['Date','Market_Real','Crop'])

    combined_transactions_data = compute_ratios(combined_transactions_data)
    combined_transactions_data.to_csv("second_1.csv")

combined_transactions_data = calculate(combined_transactions_data)
combined_transactions_data = flag(combined_transactions_data)



print '0:', (combined_transactions_data['Flag'] == 0).sum()
print '1:', (combined_transactions_data['Flag'] == 1).sum()
print '2:', (combined_transactions_data['Flag'] == 2).sum()
print '3:', (combined_transactions_data['Flag'] == 3).sum()
print '4:', (combined_transactions_data['Flag'] == 4).sum()
print '5:', (combined_transactions_data['Flag'] == 5).sum()
import pandas as pd
import numpy as np

def compute_mean(group):
    Av_Rate = group.Amount.sum()/group.Quantity.sum()
    return Av_Rate

def compute_total_q(group):
    Total_Quantity = group.Quantity.sum()
    return Total_Quantity

def compute_deviation(group):
    group['Deviation'] = abs(group.Price - group.Av_Rate)
    return group

def compute_std(group):
    std = np.sqrt(((np.square(group.Deviation)*group.Quantity).sum())/group.Quantity.sum())
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
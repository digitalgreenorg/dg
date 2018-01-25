import Tables
import pandas as pd
from datetime import timedelta
import Functions

get_aggregator_local_market = Functions.get_aggregator_local_market

#TODO: Have some filter on the basis of ratio of quantity to total quantity

daily_aggregator_market_data = Tables.daily_aggregator_market_data

aggregator_local_market = get_aggregator_local_market(daily_aggregator_market_data)

print aggregator_local_market.head()
# aggregator_local_market = pd.merge(aggregator_local_market, aggregator_list, on=['Aggregator'])
# aggregator_local_market = pd.merge(aggregator_local_market, market_list, left_on=['Local_Market'], right_on= ['Market'])
#
# writer = pd.ExcelWriter('Local_Market.xlsx')
# aggregator_local_market.to_excel(writer,'Sheet1')
# writer.save()
#
#
# print aggregator_local_market
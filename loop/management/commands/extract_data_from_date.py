import time, calendar
from datetime import datetime, timedelta

def get_data_from_date(date):
	day = str(datetime.strptime(date, '%Y%m%d').day)
	month = calendar.month_abbr[datetime.strptime(date, '%Y%m%d').month]
	year = str(datetime.strptime(date, '%Y%m%d').year)
	date_dict = {'day' : day, 'month' : month, 'year' : year}
	return date_dict


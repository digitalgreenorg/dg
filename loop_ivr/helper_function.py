__author__ = 'Vikas Saini'

from django.db import connection
from loop.utils.ivr_helpline.helpline_data import HELPLINE_LOG_FILE
from loop.helpline_view import send_sms

def get_valid_list(app_name, model_name, requested_item):
    model = get_model(app_name, model_name)
    id_list = set(model.objects.values_list('id', flat=True))
    requested_list = set(int(item) for item in requested_item.split('*') if item)
    if 0 in requested_list:
        return list(id_list)
    return list(id_list-requested_list)

def run_query(query):
	cursor = connection.cursor()
	cursor.execute(query)
    rows = cursor.fetchall()
    return rows

def send_info(to_number, content):
	index = 0
	from_number = '01139589707'
    while index < len(final_result):
		send_sms(from_number, to_number, content[index,index+1998])
		index += 1998
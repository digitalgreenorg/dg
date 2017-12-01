from django.core.management.base import BaseCommand
from django.db.models import F
from loop.models import Farmer

class Command(BaseCommand):
	def add_arguments(self, parser):
		parser.add_argument('-s',
							dest='state',
							default=1)
		
	def handle(self, *args, **options):
		state = options.get('state')

		farmers = self.get_farmers_with_invalid_phone_number(state)

		filter_args = {}
		filter_args["village__block__district__state"] = state
		filter_args["id__in"] = farmers

		Farmer.objects.filter().update(correct_phone_date=F('time_created'))
		Farmer.objects.filter(**filter_args).update(correct_phone_date=None)
		
	def validate_phone_number(self, phone, phone_digit, phone_start):
	    if len(phone) == int(phone_digit):
	        if phone.startswith(tuple(phone_start.split(","))):
	            return phone
	    return None

	def get_farmers_with_invalid_phone_number(self, state):
		all_phone_num = Farmer.objects.filter(village__block__district__state=state).values('id', 'phone', 'village__block__district__state__phone_digit', 'village__block__district__state__phone_start')
		dict_phone_num ={}
		for farmer in all_phone_num:
			farmer['phone'] = self.validate_phone_number(farmer['phone'], farmer['village__block__district__state__phone_digit'], farmer['village__block__district__state__phone_start'])
			if farmer['phone'] not in dict_phone_num.keys():
				dict_phone_num[farmer['phone']] = []
			dict_phone_num[farmer['phone']].append(farmer['id'])

		farmer_list = []
		for farmer in all_phone_num:
			#max 3 farmers can have same phone number
			if farmer['phone'] is None or len(dict_phone_num[farmer['phone']]) > 3:
				farmer_list.append(farmer['id'])
		return farmer_list
import csv
import datetime
import nptime
from activities.models import Screening
from django.core.management.base import BaseCommand

class Command(BaseCommand):
	def handle(self, *args, **options):
		csvfile = open('C:\Users\Abhishek\Desktop\\time_change.csv', 'rb')
		rows = csv.DictReader(csvfile)
		for row in rows:
			list_screening = row['group_concat(S.id)']
			screenings = map(int,list_screening.split(","))
			seconds = 363
			for i in range(len(screenings)-1):
				try:
					scr = Screening.objects.get(id = screenings[i])
					dummy_date = datetime.date(1,1,1)
					full_datetime = datetime.datetime.combine(dummy_date, scr.start_time)
					scr.start_time = (full_datetime + datetime.timedelta(seconds = seconds)).time()
					scr.save()
					seconds = seconds + 60
				except Exception as e:
					print screenings[i],e
			
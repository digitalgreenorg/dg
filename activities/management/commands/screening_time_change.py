import csv
import datetime
from django.db import connection
from activities.models import Screening
from django.core.management.base import BaseCommand

class Command(BaseCommand):
	def handle(self, *args, **options):
		#csvfile = open('C:\Users\Abhishek\Desktop\\time_change.csv', 'rb')
		cursor = connection.cursor()
		cursor.execute("select S.date, S.village_id, count(S.id), group_concat(S.id) \
			from activities_screening S \
			group by S.date, S.animator_id, S.village_id, S.start_time \
			having count(S.id)>1;")
		query_rows = cursor.fetchall()
		num_seconds = 0
		while (len(query_rows) > 0):
			for row in query_rows:
				list_screening = row[3]
				screenings = map(int,list_screening.split(","))
				seconds = 363 + num_seconds
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
			cursor = connection.cursor()
			cursor.execute("select S.date, S.village_id, count(S.id), group_concat(S.id) \
				from activities_screening S \
				group by S.date, S.animator_id, S.village_id, S.start_time \
				having count(S.id)>1;")
			query_rows = cursor.fetchall()
			print "remaining screenings", len(query_rows)
			num_seconds += 5 #if screenings are still remaining, increase the offset time by 5 seconds

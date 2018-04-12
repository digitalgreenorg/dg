from datetime import datetime 
from django.db.models import Q, F
from django.db import IntegrityError
from django.core.management.base import BaseCommand
from activities.models import *


class Command(BaseCommand):
	help = 'Saves date_of_verification in date_of_adoption field under PersonAdoptPractice'

	def handle(self, *args, **options):
		obj = PersonAdoptPractice.objects.exclude(date_of_verification__exact=None)\
					.filter(Q(date_of_adoption__isnull=False,
							  date_of_verification__isnull=False) & ~Q(date_of_adoption=F('date_of_verification')))
		if len(obj):
			for iterable in obj:
				try:
					iterable.date_of_adoption = iterable.date_of_verification
					iterable.save()
				except IntegrityError as e:
					print 'Error ::', e
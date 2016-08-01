from django.db.models import F
from django.core.management.base import BaseCommand
from datetime import date, timedelta
from django.db import IntegrityError

from activities.models import *

class Command(BaseCommand):
	def handle(self, *args, **options):

		animator = PersonAdoptPractice.objects.filter(date_of_adoption__gt=F('time_created')).values_list('id')
		print animator.count()
		c = 0
		for v in animator :
			try :
				obj = PersonAdoptPractice.objects.filter(id = v[0]).update( date_of_adoption = F('time_created'))
				print 'saved'
			except IntegrityError :
				c += 1
				obj = PersonAdoptPractice.objects.filter(id = v[0]).update( date_of_adoption = (F('time_created') - timedelta(days=c)))
				print 'duplicate changed and saved ! '
		print c
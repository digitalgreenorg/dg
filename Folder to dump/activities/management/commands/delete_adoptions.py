from activities.models import PersonAdoptPractice
from django.core.management.base import BaseCommand

class Command(BaseCommand):
	def handle(self, *args, **options):
		obj = PersonAdoptPractice.objects.filter(person__village__block__district_id = 71, video_id=3157, date_of_adoption__range = ('2015-10-01','2016-01-21'))
		print len(obj)
		obj.delete()
		print len(obj)

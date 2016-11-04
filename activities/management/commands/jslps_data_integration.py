from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
	def handle(self, *args, **options):	
		print "Geography,jslps_geo"
		call_command('jslps_geo')

		print "Groups,jslps_groups"
		call_command('jslps_groups')

		print "People,jslps_people"
		call_command('jslps_people')

		print "Mediators,jslps_mediators"
		call_command('jslps_mediators')

		print "Videos and Non negotiable,jslps_videos_nn"
		call_command('jslps_videos_nn')

		print "Screening and pma,jslps_screening_pma"
		call_command('jslps_screening_pma')
		
		print "Adoption,jslps_adoptions"
		call_command('jslps_adoptions')
	
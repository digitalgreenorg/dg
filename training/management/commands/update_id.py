from dg.settings import *

from django.core.management.base import BaseCommand

from django.db import models

from training.models import *


class Command(BaseCommand):
	def handle(self, *args, **options):
		id_map = {'28891':'54852',
					'28892':'54859',
					'28893':'54872',
					'28895':'54870',
					'28896':'54866',
					'28897':'54860',
					'28898':'54869',
					'28899':'54875',
					'28900':'54855',
					'28901':'54867',
					'28903':'54865',
					'28906':'54873',
					'28907':'54854',
					'28908':'54862',
					'28909':'54853',
					'28910':'54864',
					'28911':'54871',
					'28913':'54874',
					'28914':'54861'
				}
		base_obj = Score.objects.filter(training_id=241)
		for key, value in id_map.items():
			obj = base_obj.filter(animator_id=int(value)).update(animator_id=int(key))


# python imports
# django imports
from django.core.management.base import BaseCommand
# project imports
from coco.data_lag import DataLag


class Command(BaseCommand):
    help = 'Prepare the data for export'

    def handle(self, *args, **options):
        hnn_obj = DataLag()
        hnn_obj.run()
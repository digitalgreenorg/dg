# python imports
# django imports
from django.core.management.base import BaseCommand
# project imports
from coco.hnn_data_insert import InsertHNNData


class Command(BaseCommand):
    help = 'Prepare the data for export'

    def handle(self, *args, **options):
        hnn_obj = InsertHNNData()
        hnn_obj.run()
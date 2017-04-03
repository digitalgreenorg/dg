	# python imports
# django imports
from django.core.management.base import BaseCommand
# project imports
from coco.video_data import FetchVideoData


class Command(BaseCommand):
    help = 'Prepare the data for export'

    def handle(self, *args, **options):
        hnn_obj = FetchVideoData()
        hnn_obj.run()
# python imports
# django imports
from django.core.management.base import BaseCommand
# project imports
from coco.category_relationship import RelationShipDataCategory


class Command(BaseCommand):
    help = 'Prepare the data for export'

    def handle(self, *args, **options):
        hnn_obj = RelationShipDataCategory()
        hnn_obj.run()
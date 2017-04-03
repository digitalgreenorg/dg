# python imports
# django imports
from django.core.management.base import BaseCommand
# project imports
from coco.fetch_partner_data import PartnerData


class Command(BaseCommand):
    help = 'Prepare the data for export'

    def handle(self, *args, **options):
        partner_obj = PartnerData()
        partner_obj.run()
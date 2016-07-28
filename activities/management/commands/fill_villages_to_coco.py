import os
import unicodecsv as csv

from xlrd import *
from geographies.models import *
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        filename = 'activities/excel_data/add_villages_to_coco.xlsx'
        path = os.path.abspath(filename)
        excel_book = open_workbook(filename)
        worksheet = excel_book.sheet_by_index(0)

        error_file = 'activities/management/add_villages_to_coco_error.csv'
        error_file_path = os.path.abspath(error_file)
        c = csv.writer(open(error_file_path, 'w'),
                            quoting=csv.QUOTE_ALL)

        state = State.objects.get(id=4)
        for r in range(1, worksheet.nrows):
            d_name = worksheet.cell(r, 1).value
            b_name = worksheet.cell(r, 2).value
            v_name = worksheet.cell(r, 3).value

            districts = dict(District.objects.filter(
                state_id=state.id).values_list('id', 'district_name'))

            if d_name not in districts.values():
                try:
                    dist = District(district_name=d_name, state=state)
                    dist.save()
                    print d_name, ' saved district'
                except Exception as e:
                    print d_name, e
                    c.writerows(['District :-', d_name, e])

            district = District.objects.filter(
                state_id=state.id).get(district_name=d_name)
            blocks = dict(Block.objects.filter(
                district_id=district.id).values_list('id', 'block_name'))
            if b_name not in blocks.values():
                try:
                    new_block = Block(block_name=b_name, district=district)
                    new_block.save()
                    print b_name, ' saved Block'
                except Exception as e:
                    print b_name, e
                    c.writerows(['Block :-', b_name, e])

            block = Block.objects.filter(
                district_id=district.id).get(block_name=b_name)
            villages = dict(Village.objects.filter(
                block_id=block.id).values_list('id', 'village_name'))
            if v_name not in villages.values():
                try:
                    vill = Village(village_name=v_name, block=block)
                    vill.save()
                    print v_name, ' Saved Village'
                except Exception as e:
                    print v_name, e
                    c.writerows(['Village :-', v_name, e])

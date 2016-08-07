import os
import unicodecsv as csv

from xlrd import *
from loop.models import *
import datetime
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        filename = 'loop/excel_data/Aggregator_Data.xlsx'
        filepath = os.path.abspath(filename)
        excel_workbook = open_workbook(filepath)
        worksheet = excel_workbook.sheet_by_index(1)

        error_file = 'loop/management/add_loop_data_error.csv'
        error_file_path = os.path.abspath(error_file)
        c = csv.writer(open(error_file_path, 'w'),
                       quoting=csv.QUOTE_ALL)
        timestamp_ct = 1470383019

        for r in range(1, 10):
            date = worksheet.cell(r, 0).value
            farmer_id = worksheet.cell(r, 2).value
            village_id = worksheet.cell(r, 4).value
            crop_id = worksheet.cell(r, 6).value
            quantity = worksheet.cell(r, 7).value
            price = worksheet.cell(r, 8).value
            amount = quantity * price
            mandi_id = worksheet.cell(r, 11).value
            aggregator_id = worksheet.cell(r, 13).value

            crop = Crop.objects.get(id=crop_id)
            village = Village.objects.get(id=village_id)
            farmer = Farmer.objects.get(id=farmer_id)
            mandi = Mandi.objects.get(id=mandi_id)
            user = LoopUser.objects.get(user_id=aggregator_id)
            gaddidar = Gaddidar.objects.get(id=1)
            status = 1
            print int(date), quantity, price, farmer, crop, village, mandi, user
            print datetime.datetime(int(date))
            # print datetime.datetime.strptime(date, '%d-%m-%Y')
            # try:
            #     # if(farmer!=null && crop!=null && village!=null && mandi!=null && user!=null){
            #         transaction=CombinedTransaction(farmer=farmer,crop=crop,mandi=mandi,date=date,quantity=quantity,price=price,amount=amount,status=status,payment_date=date,timestamp=timestamp_ct)
            #         transaction.save()
            #         timestamp_ct+=1
            #         print "CT added successfully"
            #         # }
            # except Exception as e:
            #     print "CT : ",e
            #     c.writerows(['CT :-', e])

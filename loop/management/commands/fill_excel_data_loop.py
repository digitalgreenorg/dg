import os
import csv
import ast
from xlrd import *
from loop.models import *
import datetime
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        filename = 'loop/excel_data/Shyam_All_CT.csv'
        filepath = os.path.abspath(filename)
        excel_workbook = csv.reader(open(filepath))
        # excel_workbook = open_workbook(filepath)
        # worksheet = excel_workbook.sheet_by_index(1)

        error_file = 'loop/management/add_loop_data_error.csv'
        error_file_path = os.path.abspath(error_file)
        c = csv.writer(open(error_file_path, 'w'),
                       quoting=csv.QUOTE_MINIMAL)

        timestamp_ct = 1470638795

        excel_workbook.next()

        for r in excel_workbook:
            date = r[0]
            farmer_id = r[2]
            village_id = r[4]
            crop_id = r[6]
            quantity = float(r[7])
            price = float(r[8])
            amount = float(quantity) * float(price)
            mandi_id = r[11]
            aggregator_id = r[13]
            gaddidar_id = r[14]

            crop = Crop.objects.get(id=int(crop_id))
            village = Village.objects.get(id=int(village_id))
            farmer = Farmer.objects.get(id=int(farmer_id))
            mandi = Mandi.objects.get(id=int(mandi_id))
            gaddidar = Gaddidar.objects.get(id=int(gaddidar_id))
            # user = LoopUser.objects.get(user_id=int(aggregator_id))
            status = 1

            # print aggregator_id,price,quantity,amount,mandi_id,gaddidar_id,farmer_id,crop_id
            # print datetime.datetime.strptime(date, '%d-%m-%y').date()

            try:
                if(farmer is not None and crop is not None and village is not None and mandi is not None and aggregator_id is not None and gaddidar is not None):
                    transaction_date = datetime.datetime.strptime(
                        date, '%d-%m-%y').date()
                    print transaction_date
                    try:
                        prev_transaction = CombinedTransaction.objects.get(user_created_id=aggregator_id, date=transaction_date, quantity=quantity, price=price, farmer=farmer, crop=crop, mandi=mandi, gaddidar=gaddidar)
                        print "Duplicate Found for CT"
                        c.writerow(['CT :- Duplicate :', prev_transaction.id])
                    except Exception as e:
                        print '----'
                        # if prev_transaction is None:
                        transaction = CombinedTransaction(user_created_id=aggregator_id, farmer=farmer, crop=crop, mandi=mandi, date=transaction_date,
                                                          quantity=quantity, price=price, amount=amount, status=status, payment_date=transaction_date, timestamp=timestamp_ct, gaddidar=gaddidar)
                        transaction.save()
                        timestamp_ct += 1
                        print "CT added successfully"
                        # else:

            except Exception as e:
                print "CT --", e
                c.writerow(['CT - Exception '])

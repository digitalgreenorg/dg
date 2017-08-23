from django.core.management.base import BaseCommand
from loop.models import LoopUser, Mandi, LoopUserAssignedMandi, District, Mandi, Village, LoopUserAssignedVillage, Gaddidar
from openpyxl import load_workbook
from django.db.models import get_model
import sys
import math

import pandas as pd

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-m', dest='mandi', default=None, type=str)
        parser.add_argument('-g', dest='gaddidar', default=None, type=str)
        parser.add_argument('-am', dest='aggregator_mandi', default=None, type=str)
        parser.add_argument('-av', dest='aggregator_village', default=None, type=str)

    def set_status(self, df, index, stat, excep):
        df.set_value(index, 'Status', stat)
        df.set_value(index, 'Exception', excep)

    def create_entry(self, model, kwargs):
        try:
            model_obj = get_model('loop', model)
            model_obj.create(**kwargs)
            self.set_status(df, i, 'Pass', None)
        except Exception as e:
            self.set_status(df, i, 'Fail', str(e))

    def import_mandi(self, df):
        all_districts = District.objects.values('id', 'district_name')
        dict_districts = {}
        for district in all_districts:
            dict_districts[district['district_name']] = district['id']

        for i, row in df.iterrows():
            try:
                district_name = row['District'].strip()
                mandi_name = row['Market Name (Regional)'].strip()
                mandi_name_en = row['Market Name (English)'].strip()
                if dict_districts.get(district_name):
                    district_id = dict_districts[district_name]
                else:
                    self.set_status(df, i, 'Fail', 'District not found')
                    continue
                mandi = Mandi(mandi_name=mandi_name, mandi_name_en=mandi_name_en, district_id=district_id, is_visible=1)
                mandi.save()
                self.set_status(df, i, 'Pass', None)
            except Exception as e:
                self.set_status(df, i, 'Fail', str(e))

    def import_gaddidar(self, df):
        all_mandis = Mandi.objects.values('id', 'mandi_name')
        default_gaddidar_phone = '0000000000'
        dict_mandis = {}
        for mandi in all_mandis:
            dict_mandis[mandi['mandi_name']] = mandi['id']

        for i, row in df.iterrows():
            try:
                market_name = row['Market Name'].strip()
                trader_name = row['Trader Name (Regional)'].strip()
                trader_name_en = row['Trader Name (English)'].strip()
                if dict_mandis.get(market_name):
                    mandi_id = dict_mandis[market_name]
                else:
                    self.set_status(df, i, 'Fail', 'Mandi not found')
                    continue
                if "Phone Number" in df.columns.values:
                    if math.isnan(row['Phone Number']):
                        gaddidar_phone = default_gaddidar_phone
                    else:
                        gaddidar_phone = int(row['Phone Number'])
                else:
                    gaddidar_phone = default_gaddidar_phone
                gaddidar = Gaddidar(gaddidar_name=trader_name, gaddidar_name_en=trader_name_en, gaddidar_phone=gaddidar_phone,mandi_id=mandi_id, is_visible=1)
                gaddidar.save()
                self.set_status(df, i, 'Pass', '')
            except Exception as e:
                self.set_status(df, i, 'Fail', str(e))
                
    def import_user_assigned_mandi(self, df):
        all_aggregators = LoopUser.objects.values('id', 'name')
        dict_aggregators = {}
        agg_wise_mandi = {}
        for aggregator in all_aggregators:
            dict_aggregators[aggregator['name']] = aggregator['id']
            agg_wise_mandi[aggregator['id']] = []

        all_mandis = Mandi.objects.values('id', 'mandi_name')
        dict_mandis = {}
        for mandi in all_mandis:
            dict_mandis[mandi['mandi_name']] = mandi['id']

        loop_user_mandi = LoopUserAssignedMandi.objects.values('mandi','loop_user')
        for item in loop_user_mandi:
            agg_wise_mandi[item['loop_user']].append(item['mandi'])

        for i, row in df.iterrows():
            try:
                aggregator_name = row['Name (Regional)'].strip()
                mandi_name = row['Market (Regional)'].strip()
                if dict_aggregators.get(aggregator_name):
                    aggregator_id = dict_aggregators[aggregator_name]
                else:
                    self.set_status(df, i, 'Fail', 'Aggregator not found')
                    continue
                if dict_mandis.get(mandi_name):
                    mandi_id = dict_mandis[mandi_name]
                else:
                    self.set_status(df, i, 'Fail', 'Mandi not found')
                    continue    
                if  mandi_id not in agg_wise_mandi[aggregator_id]:
                    agg_wise_mandi[aggregator_id].append(mandi_id)
                    aggregator_mandi = LoopUserAssignedMandi(loop_user_id = aggregator_id, mandi_id = mandi_id)
                    aggregator_mandi.save()
                    self.set_status(df, i, 'Pass', '')
                else:
                    self.set_status(df, i, 'Fail', 'Combination exists')

            except Exception as e:
                self.set_status(df, i, 'Fail', str(e))

    def import_user_assigned_village(self, df):
        all_aggregators = LoopUser.objects.values('id', 'name')
        dict_aggregators = {}
        agg_wise_village = {}
        for aggregator in all_aggregators:
            dict_aggregators[aggregator['name']] = aggregator['id']
            agg_wise_village[aggregator['id']] = []

        all_villages = Village.objects.values('id', 'village_name')
        dict_villages = {}
        for village in all_villages:
            dict_villages[village['village_name']] = village['id']

        loop_user_village = LoopUserAssignedVillage.objects.values('village','loop_user')        
        for item in loop_user_village:
            agg_wise_village[item['loop_user']].append(item['village'])

        for i, row in df.iterrows():
            try:
                aggregator_name = row['Name (Regional)'].strip()
                village_name = row['Village Name (Regional)'].strip()
                if dict_aggregators.get(aggregator_name):
                    aggregator_id = dict_aggregators[aggregator_name]
                else:
                    self.set_status(df, i, 'Fail', 'Aggregator not found')
                    continue
                if dict_villages.get(village_name):
                    village_id = dict_villages[village_name]
                else:
                    self.set_status(df, i, 'Fail', 'Village not found')
                    continue    
                if village_id not in agg_wise_village[aggregator_id]:
                    agg_wise_village[aggregator_id].append(agg_wise_village)
                    aggregator_mandi = LoopUserAssignedVillage(loop_user_id = aggregator_id, village_id = village_id)
                    aggregator_mandi.save()
                    self.set_status(df, i, 'Pass', '')
                else:
                    self.set_status(df, i, 'Fail', 'Combination exists')
            except Exception as e:
                self.set_status(df, i, 'Fail', str(e))

    def import_data(self, input_file, output_filename, sheetname, option):
        df = input_file.parse(sheetname)

        self.functions[option](self, df)

        book = load_workbook(output_filename)
        writer = pd.ExcelWriter(output_filename, engine='openpyxl')
        writer.book = book
        writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
        df.to_excel(writer, sheet_name=sheetname)
        writer.save()

    functions = {'mandi': import_mandi, 'gaddidar': import_gaddidar, 'aggregator_mandi': import_user_assigned_mandi, 'aggregator_village': import_user_assigned_village}
    
    def handle(self, *args, **options):
        input_filename = 'Maharashtra Admin Data Sheet.xlsx'
        output_filename = "MaharashtraDataImportStatus.xlsx"
        try:
            input_file = pd.ExcelFile(input_filename)
            output_file = pd.ExcelWriter(output_filename)
            output_file.save()
        except Exception  as e:
            sys.exit()

        if options.get('mandi') != None:
            sheetname = options.get('mandi')
            self.import_data(input_file, output_filename, sheetname, 'mandi')
        if options.get('gaddidar') != None:
            sheetname = options.get('gaddidar')
            self.import_data(input_file, output_filename, sheetname, 'gaddidar')
        if options.get('aggregator_mandi') != None:
            sheetname = options.get('aggregator_mandi')
            self.import_data(input_file, output_filename, sheetname, 'aggregator_mandi')
        if options.get('aggregator_village') != None:
            sheetname = options.get('aggregator_village')
            self.import_data(input_file, output_filename, sheetname, 'aggregator_village')
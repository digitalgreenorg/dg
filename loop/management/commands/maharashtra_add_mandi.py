from django.core.management.base import BaseCommand
from loop.models import District, Mandi

import pandas as pd
import sys

class Command(BaseCommand):

    def handle(self, *args, **options):
        df = pd.DataFrame()
        filename = 'Maharashtra Admin Data Sheet.xlsx'
        try:
            df = pd.read_excel(filename, sheetname='Markets')
        except Exception  as e:
            sys.exit()
        headers = list(df.columns.values)
        status = [None]*len(df[headers[0]])
        df['Status'] = pd.Series(status).values
        df['Exception'] = pd.Series(status).values

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
                    df.set_value(i, 'Status', 'Fail')
                    df.set_value(i, 'Exception', "district not found")
                    continue
                mandi = Mandi(mandi_name=mandi_name, mandi_name_en=mandi_name_en, district_id=district_id, is_visible=1)
                mandi.save()
                df.set_value(i, 'Status', 'Pass')
            except Exception as e:
                df.set_value(i, 'Status', 'Fail')
                df.set_value(i, 'Exception', str(e))
        excel_writer = pd.ExcelWriter("MarketsStatus.xlsx")
        df.to_excel(excel_writer = excel_writer, sheet_name= 'Sheet1', index = False)
        excel_writer.save()
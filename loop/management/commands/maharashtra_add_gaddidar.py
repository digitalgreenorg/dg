from django.core.management.base import BaseCommand
from loop.models import Mandi, Gaddidar

import pandas as pd

class Command(BaseCommand):

    def handle(self, *args, **options):
        df = pd.DataFrame()
        filename = 'Maharashtra Admin Data Sheet.xlsx'
        try:
            df = pd.read_excel(filename, sheetname='Traders')
        except Exception  as e:
            sys.exit()
        headers = list(df.columns.values)
        status = [None]*len(df[headers[0]])
        df['Status'] = pd.Series(status).values
        df['Exception'] = pd.Series(status).values

        all_mandis = Mandi.objects.values('id', 'mandi_name')
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
                    df.set_value(i, 'Status', 'Fail')
                    df.set_value(i, 'Exception', 'mandi not found')
                    continue
                gaddidar = Gaddidar(gaddidar_name=trader_name, gaddidar_name_en=trader_name_en, gaddidar_phone='0000000000',mandi_id=mandi_id, is_visible=1)
                gaddidar.save()
                df.set_value(i, 'Status', 'Pass')
            except Exception as e:
                df.set_value(i, 'Status', 'Fail')
                df.set_value(i, 'Exception', str(e))
        excel_writer = pd.ExcelWriter("GaddidarsStatus.xlsx")
        df.to_excel(excel_writer = excel_writer, sheet_name= 'Sheet1', index = False)
        excel_writer.save()
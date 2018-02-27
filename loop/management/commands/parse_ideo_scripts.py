from django.core.management.base import BaseCommand
from random import sample
import os
import pandas as pd
import MySQLdb
import dg.settings
from django.db import connection


class Command(BaseCommand):

    def add_arguments(self, parser):

        # to get filenames
        parser.add_argument('filename', nargs='+', type=str)

        # to parse script type
        parser.add_argument('--referral', '-r', action='store_true', dest='r')
        parser.add_argument('--transport_codes', '-t', action='store_true', dest='t')
        parser.add_argument('--generate_transport_codes', '-g', action='store_true', dest='g')

    def handle(self, *args, **options):
        for filename in options['filename']:
            if options['r']:
                self.parse_referral_sheet(filename)
            elif options['t']:
                self.parse_transport_sheet(filename)
            elif options['g']:
                self.generate_transport_codes()

    def parse_referral_sheet(self, filename):
        referral_columns = [u'Name (of referring farmer)', u'Mobile # (of referring farmer)',
                            u'Name (of referred farmer)', u'Mobile # (of referred farmer)']
        columns, parsed_data = self.parse_data(filename)

        # validating the data format
        if len(set(columns) & set(referral_columns)) != 4:
            print "Invalid file, please check header or number of columns"
        else:
            # Inserting data into the table
            referral_query = '''UPDATE loop_farmer 
                                SET referred_by = %s 
                                WHERE phone = %s'''

            # Operations to extract just the required columns,
            # i.e., phone numbers of farmers
            temp_data = [parsed_data[:,0],parsed_data[:,2]]
            extracted_data = zip(*temp_data)
            self.run_query_multiple(referral_query, extracted_data)

    def parse_transport_sheet(self, filename):
        referral_columns = [u'Farmer QR Code', u'Free Transport Code', u'Date Used']
        columns, parsed_data = self.parse_data(filename)

        # validating the data format
        if len(set(columns) & set(referral_columns)) != 3:
            print "Invalid file, please check header or number of columns"
        else:
            # todo
            #   1. make text_local_id and qr_code not required
            #   2. make code primary key
            transport_query = '''INSERT INTO loop_farmertransportcode (qr_code, code, dateUsed)
                                 VALUES (%s, %s, %s)
                                 ON DUPLICATE KEY UPDATE qr_code=qr_code'''

            # Inserting data into the table
            # transport_query ='''UPDATE loop_farmertransportcode
            #                    SET dateUsed=%s
            #                    WHERE code=%s AND qr_code=%s'''

            # Operations to extract just the required columns,
            # i.e., phone numbers of farmers
            self.run_query_multiple(transport_query, parsed_data)

    def parse_data(self, filename):
        ext_allwd = ['xlsx', 'xls']
        file_ext = os.path.splitext(filename)[-1]
        data = []
        if file_ext not in ext_allwd or file_ext == '.csv':
            print "Invalid file format!!"
        else:
            try:
                # Parsing data into list to be inserted
                if file_ext in ext_allwd:
                    columns, data = self.parse_excel(filename)
                else:
                    columns, data = self.parse_csv(filename)
                return columns, data
            except Exception, err:
                print err

    def parse_excel(self, filename):
        xl = pd.ExcelFile(filename)
        df = xl.parse(0)
        return df.columns, df.values

    def parse_csv(self, filename):
        df = pd.read_csv(filename)
        return df.columns, df.values

    def generate_transport_codes(self):
        # codes start from 10010, no particular reason for selecting this
        codes = sample(range(10010, 20010), 2000)
        transport_code_query = '''INSERT INTO loop_farmertransportcode (code) VALUES (%s)'''
        self.run_query_multiple(transport_code_query,codes)

    def init_cursor(self):
        self.mysql_cn = MySQLdb.connect(host=dg.settings.DATABASES['default']['HOST'],
                                        port=dg.settings.DATABASES['default']['PORT'],
                                        user=dg.settings.DATABASES['default']['USER'],
                                        passwd=dg.settings.DATABASES['default']['PASSWORD'],
                                        db=dg.settings.DATABASES['default']['NAME'],
                                        charset='utf8',
                                        use_unicode=True)
        self.cursor = self.mysql_cn.cursor()

    def close_connections(self):
        self.cursor.close()
        self.mysql_cn.close()

    def run_query(self, query, args):
        try:
            self.init_cursor()
            self.cursor.execute(query, args)
            self.cursor.commit()
        except Exception, err:
            print err
        finally:
            self.close_connections()

    def run_query_multiple(self, query, arg_list):
        try:
            self.init_cursor()
            for args in arg_list:
                self.cursor.execute(query, args)
            self.cursor.commit()
        except Exception, err:
            print err
        finally:
            self.close_connections()

    def __init__(self):
        super(Command, self).__init__()
        self.cursor = None
        self.mysql_cn = None
